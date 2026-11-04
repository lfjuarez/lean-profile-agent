"""Chat answers come only from retrieved sections, cite them, and decline otherwise."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from profile_agent.chat import ProfileChat, suggest_followups
from profile_agent.kb import KnowledgeBase
from profile_agent.retrieval import Index


class FakeBackend:
    """Captures the prompt and plays back a scripted answer."""

    def __init__(
        self, answer: str = "Leandro holds nine certifications [1]. Highest first [1]."
    ) -> None:
        self.answer = answer
        self.calls: list[dict] = []
        self.stop_reason = "end_turn"

    def stream(self, system: str, messages: list[dict]) -> Iterator[str]:
        self.calls.append({"system": system, "messages": messages})
        for piece in self.answer.split(" "):
            yield piece + " "


@pytest.fixture(scope="module")
def indexes(kb_en: KnowledgeBase, kb_es: KnowledgeBase) -> dict[str, Index]:
    return {"en": Index(kb_en), "es": Index(kb_es)}


def collect(chat: ProfileChat, question: str, lang: str | None = None, history: list | None = None):
    messages = list(history or []) + [{"role": "user", "content": question}]
    return list(chat.stream(messages, lang=lang))


def test_prompt_contains_only_knowledge_base_text(indexes, kb_en: KnowledgeBase) -> None:
    backend = FakeBackend()
    chat = ProfileChat(indexes, backend=backend)
    collect(chat, "Which Splunk certifications do you hold?", lang="en")
    assert len(backend.calls) == 1
    user_turn = backend.calls[0]["messages"][-1]["content"]
    assert '<source n="1"' in user_turn
    assert "Which Splunk certifications do you hold?" in user_turn
    # every source block is verbatim text of a KB section
    import re

    bodies = re.findall(r"<source n=\"\d+\"[^>]*>\n(.*?)\n</source>", user_turn, re.S)
    assert bodies
    kb_texts = {c.text for c in kb_en.chunks}
    for body in bodies:
        assert body in kb_texts


def test_citations_map_to_real_sources(indexes) -> None:
    backend = FakeBackend(answer="Nine certifications [1], instructor since 2025 [2]. Again [1].")
    chat = ProfileChat(indexes, backend=backend)
    events = collect(chat, "Which Splunk certifications do you hold?", lang="en")
    types = [e.type for e in events]
    assert types[:2] == ["retrieved", "text"] and types[-1] == "done"
    sources = next(e for e in events if e.type == "sources").data
    assert [s["n"] for s in sources] == [1, 2]
    assert all(isinstance(s["doc_title"], str) and s["section_title"] for s in sources)
    assert sources[0]["doc_id"] == "certifications"
    done = events[-1].data
    assert done["grounded"] is True
    assert done["lang"] == "en"


def test_uncited_source_numbers_are_dropped(indexes) -> None:
    backend = FakeBackend(answer="Only this [1] and a bogus [9].")
    chat = ProfileChat(indexes, backend=backend)
    events = collect(chat, "What are your rates?", lang="en")
    sources = next(e for e in events if e.type == "sources").data
    assert [s["n"] for s in sources] == [1]


def test_offtopic_gets_a_short_source_free_turn_that_steers_back(indexes) -> None:
    backend = FakeBackend("Pizza is outside my documents, but detections are not [1]. Ask me!")
    chat = ProfileChat(indexes, backend=backend)
    events = collect(chat, "What is your favourite pizza topping?", lang="en")
    assert len(backend.calls) == 1
    call = backend.calls[0]
    # nothing to cite, nothing to invent from
    assert "<source" not in call["messages"][-1]["content"]
    assert "state no fact about me" in call["system"]
    text = "".join(e.data for e in events if e.type == "text")
    assert "[1]" not in text and text.startswith("Pizza")
    assert events[-1].data["grounded"] is False
    followups = next(e for e in events if e.type == "followups").data
    assert any("contact" in f.lower() for f in followups)
    assert next(e for e in events if e.type == "sources").data == []


def test_offtopic_falls_back_to_the_fixed_text(indexes) -> None:
    class Broken(FakeBackend):
        def stream(self, system, messages):
            raise RuntimeError("down")
            yield ""  # pragma: no cover

    chat = ProfileChat(indexes, backend=Broken())
    events = collect(chat, "What is your favourite pizza?", lang="en")
    text = "".join(e.data for e in events if e.type == "text")
    assert "documented experience" in text and "my " in text


def test_declines_in_spanish(indexes) -> None:
    backend = FakeBackend("La pala la dejo para otro día. ¿Querés saber de mis proyectos?")
    events = collect(ProfileChat(indexes, backend=backend), "¿Cuál es tu pizza favorita?")
    assert "Rioplatense Spanish" in backend.calls[0]["system"]
    text = "".join(e.data for e in events if e.type == "text")
    assert text.startswith("La pala")
    assert events[-1].data["lang"] == "es"


def test_language_is_detected_when_missing(indexes) -> None:
    backend = FakeBackend()
    chat = ProfileChat(indexes, backend=backend)
    events = collect(chat, "¿Qué certificaciones de Splunk tenés?")
    assert events[-1].data["lang"] == "es"
    user_turn = backend.calls[0]["messages"][-1]["content"]
    assert 'lang="es"' in user_turn
    assert "Certificaciones" in user_turn


def test_history_is_passed_without_sources(indexes) -> None:
    backend = FakeBackend()
    chat = ProfileChat(indexes, backend=backend)
    history = [
        {"role": "user", "content": "What are your rates?"},
        {"role": "assistant", "content": "USD 45 to 70 per hour [1]."},
    ]
    collect(chat, "And for training?", lang="en", history=history)
    msgs = backend.calls[0]["messages"]
    assert msgs[0]["role"] == "user" and "<source" not in msgs[0]["content"]
    assert msgs[1]["role"] == "assistant"
    assert msgs[-1]["role"] == "user" and "<source" in msgs[-1]["content"]


def test_followups_come_from_knowledge_base_and_skip_the_asked_one(
    kb_en: KnowledgeBase, indexes
) -> None:
    hits = indexes["en"].search("Which Splunk certifications do you hold?", k=6)
    asked = "Which Splunk certifications do you hold?"
    chips = suggest_followups(kb_en, hits, asked=asked, n=3)
    assert len(chips) == 3
    assert asked not in chips
    all_questions = {q for d in kb_en.docs for q in d.questions}
    assert set(chips) <= all_questions
    assert chips[0] in kb_en.get("certifications").questions


def test_backend_error_becomes_error_event(indexes) -> None:
    class Boom(FakeBackend):
        def stream(self, system, messages):
            raise RuntimeError("down")
            yield  # pragma: no cover

    chat = ProfileChat(indexes, backend=Boom())
    events = collect(chat, "What are your rates?", lang="en")
    assert events[-1].type == "error"
    assert "down" not in events[-1].data["message"]


def test_overlong_or_empty_input_is_rejected(indexes) -> None:
    chat = ProfileChat(indexes, backend=FakeBackend())
    with pytest.raises(ValueError):
        collect(chat, "x" * 1001, lang="en")
    with pytest.raises(ValueError):
        collect(chat, "   ", lang="en")


def test_provider_selection_from_env(monkeypatch) -> None:
    from profile_agent.chat import AnthropicBackend
    from profile_agent.providers import OpenAICompatBackend, backend_from_env

    monkeypatch.delenv("PROFILE_PROVIDER", raising=False)
    assert isinstance(backend_from_env(), AnthropicBackend)
    gem = backend_from_env("gemini")
    assert isinstance(gem, OpenAICompatBackend) and "googleapis" in gem.url
    with pytest.raises(ValueError):
        backend_from_env("nope")


def test_openai_compat_without_key_is_not_configured(indexes, monkeypatch) -> None:
    from profile_agent.providers import OpenAICompatBackend

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    chat = ProfileChat(indexes, backend=OpenAICompatBackend("openrouter"))
    events = collect(chat, "What are your rates?", lang="en")
    assert events[-1].type == "error" and events[-1].data["code"] == "not_configured"


def test_dominant_document_is_sent_whole(indexes) -> None:
    backend = FakeBackend(answer="Companies [1].")
    chat = ProfileChat(indexes, backend=backend)
    collect(chat, "Which companies have you worked for?", lang="en")
    user_turn = backend.calls[0]["messages"][-1]["content"]
    assert "Mercado Libre" in user_turn
    assert "CyberStone" in user_turn and "MetroGAS" in user_turn


def test_profile_question_includes_the_summary(indexes) -> None:
    backend = FakeBackend(answer="Summary [1].")
    chat = ProfileChat(indexes, backend=backend)
    collect(chat, "¿Qué hacés, en un párrafo?", lang="es")
    assert 'section="Resumen"' in backend.calls[0]["messages"][-1]["content"]


def test_empty_model_answer_becomes_error(indexes) -> None:
    chat = ProfileChat(indexes, backend=FakeBackend(answer=""))
    events = collect(chat, "What are your rates?", lang="en")
    assert events[-1].type == "error" and events[-1].data["code"] == "unavailable"


def test_comma_separated_citations_are_recognised(indexes) -> None:
    chat = ProfileChat(indexes, backend=FakeBackend(answer="Rates and hours [1, 2]."))
    events = collect(chat, "What are your rates?", lang="en")
    sources = next(e for e in events if e.type == "sources").data
    assert [s["n"] for s in sources] == [1, 2]


def test_unknown_followup_does_not_borrow_the_previous_topic(indexes) -> None:
    backend = FakeBackend()
    chat = ProfileChat(indexes, backend=backend)
    history = [
        {"role": "user", "content": "¿Sos instructor oficial de Splunk?"},
        {"role": "assistant", "content": "Sí [1]."},
    ]
    events = collect(chat, "¿Cuál es tu signo del zodíaco?", lang="es", history=history)
    # only the short off-topic turn, without the earlier conversation or any section
    assert len(backend.calls) == 1 and len(backend.calls[0]["messages"]) == 1
    assert events[-1].data["grounded"] is False


def test_system_prompt_forbids_citing_when_declining() -> None:
    from profile_agent.chat import SYSTEM_PROMPT

    assert "do not cite" in SYSTEM_PROMPT.lower()


@pytest.mark.parametrize("name", ["Edenor", "TripleTen", "edenor"])
def test_forbidden_names_are_redacted_even_when_streamed_in_pieces(indexes, name: str) -> None:
    class Splitter(FakeBackend):
        def stream(self, system, messages):
            self.calls.append({"system": system, "messages": messages})
            text = f"The sources do not mention {name} at all [1]."
            yield from text  # worst case: one character per chunk

    chat = ProfileChat(indexes, backend=Splitter())
    events = collect(chat, "What are your rates?", lang="en")
    text = "".join(e.data for e in events if e.type == "text")
    assert name.lower() not in text.lower()
    assert "that company" in text


def test_system_prompt_covers_interview_and_personal_questions() -> None:
    from profile_agent.chat import SYSTEM_PROMPT

    low = SYSTEM_PROMPT.lower()
    assert "anecdote" in low and "personal" in low and "rank" in low
    assert "first person" in low and "ai assistant" in low


def test_openai_compat_retries_busy_responses(indexes, monkeypatch) -> None:
    import contextlib

    import httpx

    from profile_agent import providers

    statuses = [429, 503, 200]

    class Resp:
        def __init__(self, status: int) -> None:
            self.status_code = status

        def read(self) -> bytes:
            return b"busy"

        def iter_lines(self):
            yield 'data: {"choices":[{"delta":{"content":"Rates [1]."},"finish_reason":"stop"}]}'
            yield "data: [DONE]"

    @contextlib.contextmanager
    def fake_stream(*args, **kwargs):
        yield Resp(statuses.pop(0))

    monkeypatch.setattr(httpx, "stream", fake_stream)
    monkeypatch.setattr(providers.time, "sleep", lambda s: None)
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    chat = ProfileChat(indexes, backend=providers.OpenAICompatBackend("gemini"))
    events = collect(chat, "What are your rates?", lang="en")
    assert events[-1].type == "done", events[-1]
    assert statuses == []


@pytest.mark.parametrize(
    ("lang", "question"),
    [("es", "¿Cuántas personas tenía tu equipo?"), ("en", "How big was the team you led?")],
)
def test_team_size_question_reaches_leadership_section(indexes, lang: str, question: str) -> None:
    chat = ProfileChat(indexes, backend=None)
    ids = [h.chunk.id for h in chat.retrieve(question, lang)]
    assert any(i.startswith("ways-of-working#") for i in ids[:6]), ids


def test_expansion_keeps_original_top_hits(indexes) -> None:
    chat = ProfileChat(indexes, backend=None)
    raw = indexes["en"].search("Which companies have you worked for?", k=6)
    expanded = chat.retrieve("Which companies have you worked for?", "en")
    assert {h.chunk.id for h in raw} <= {h.chunk.id for h in expanded}


def test_long_previous_answer_does_not_break_followup(indexes) -> None:
    backend = FakeBackend()
    chat = ProfileChat(indexes, backend=backend)
    history = [
        {"role": "user", "content": "How did you automate triage with SOAR?"},
        {"role": "assistant", "content": "Long answer [1]. " * 300},
    ]
    events = collect(chat, "What results did it achieve after 90 days?", lang="en", history=history)
    assert events[-1].type == "done"
    sent = backend.calls[0]["messages"][1]["content"]
    assert len(sent) <= 3000
