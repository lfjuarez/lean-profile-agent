"""Retrieval returns the right document for real questions and refuses nonsense."""

from __future__ import annotations

import pytest

from profile_agent.kb import KnowledgeBase
from profile_agent.retrieval import Index, detect_lang, tokenize


@pytest.fixture(scope="module")
def idx_en(kb_en: KnowledgeBase) -> Index:
    return Index(kb_en)


@pytest.fixture(scope="module")
def idx_es(kb_es: KnowledgeBase) -> Index:
    return Index(kb_es)


@pytest.mark.parametrize(
    ("question", "doc_id"),
    [
        ("Which Splunk certifications do you hold?", "certifications"),
        ("What are your rates?", "rates"),
        ("How did you automate phishing triage with Splunk SOAR?", "case-soar-triage"),
        (
            "Have you designed a multi-site Splunk architecture with disaster recovery?",
            "case-multisite-platform",
        ),
        ("How can I contact you?", "contact"),
        ("Tell me about your current role", "experience"),
    ],
)
def test_english_questions_hit_expected_document(idx_en: Index, question: str, doc_id: str) -> None:
    hits = idx_en.search(question, k=3)
    assert hits, "expected at least one hit"
    assert hits[0].chunk.doc_id == doc_id, [h.chunk.id for h in hits]


@pytest.mark.parametrize(
    ("question", "doc_id"),
    [
        ("¿Qué certificaciones de Splunk tenés?", "certifications"),
        ("¿Cuánto cuesta un health check de Splunk?", "services"),
        ("¿Cómo automatizaste el triage con SOAR?", "case-soar-triage"),
        ("¿Cómo te contacto?", "contact"),
    ],
)
def test_spanish_questions_hit_expected_document(idx_es: Index, question: str, doc_id: str) -> None:
    hits = idx_es.search(question, k=3)
    assert hits
    assert hits[0].chunk.doc_id == doc_id, [h.chunk.id for h in hits]


def test_accents_do_not_matter(idx_es: Index) -> None:
    with_accent = idx_es.search("certificación", k=1)
    without = idx_es.search("certificacion", k=1)
    assert with_accent[0].chunk.id == without[0].chunk.id


def test_nonsense_is_not_answerable(idx_en: Index) -> None:
    hits = idx_en.search("purple elephant lasagna recipe moon landing", k=3)
    assert not idx_en.is_answerable(hits)


def test_real_question_is_answerable(idx_en: Index) -> None:
    hits = idx_en.search("What is your availability per week?", k=3)
    assert idx_en.is_answerable(hits)


def test_stopwords_alone_are_not_answerable(idx_en: Index) -> None:
    hits = idx_en.search("the and of to", k=3)
    assert not idx_en.is_answerable(hits)


def test_tokenize_folds_case_and_accents() -> None:
    assert tokenize("Certificación SPLUNK") == ["certificacion", "splunk"]


def test_detect_lang() -> None:
    assert detect_lang("¿Cuáles son tus tarifas por hora?") == "es"
    assert detect_lang("What are your hourly rates?") == "en"
    assert detect_lang("MITRE ATT&CK", default="es") == "es"


@pytest.mark.parametrize("question", ["donde reside?", "¿Dónde vivís?", "¿Dónde estás ubicado?"])
def test_location_synonyms_find_the_location_section(idx_es: Index, question: str) -> None:
    hits = idx_es.search(question, k=3)
    assert hits and idx_es.is_answerable(hits, question)
    assert {h.chunk.id for h in hits} & {"profile#idiomas-y-ubicacion", "contact#datos-de-contacto"}


@pytest.mark.parametrize("question", ["Where do you live?", "Where are you based?"])
def test_location_synonyms_in_english(idx_en: Index, question: str) -> None:
    hits = idx_en.search(question, k=3)
    assert hits and idx_en.is_answerable(hits, question)
    assert {h.chunk.id for h in hits} & {
        "profile#languages-and-location",
        "contact#contact-details",
    }


@pytest.mark.parametrize(
    ("question", "doc_id"),
    [
        ("¿De qué país sos?", "profile"),
        ("¿Qué estudiaste?", "profile"),
        ("¿Sabés programar en Python?", "skills"),
        ("¿Dónde trabajás hoy?", "experience"),
        ("¿Cuánto pretendés cobrar por mes?", "rates"),
        ("Describe your leadership style", "ways-of-working"),
        ("How do you coach new team members?", "ways-of-working"),
    ],
)
def test_paraphrases_reach_the_right_document(question: str, doc_id: str, kb_en, kb_es) -> None:
    from profile_agent.chat import ProfileChat
    from profile_agent.retrieval import detect_lang

    lang = detect_lang(question)
    chat = ProfileChat({"en": Index(kb_en), "es": Index(kb_es)}, backend=None)
    hits = chat.retrieve(question, lang)
    assert hits, question
    assert doc_id in {h.chunk.doc_id for h in hits[:4]}, [h.chunk.id for h in hits]
