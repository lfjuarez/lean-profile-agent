"""Lean's hard rules, enforced over the knowledge base, the page and the system prompt."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from profile_agent.chat import DECLINE_TEXT, SYSTEM_PROMPT
from profile_agent.kb import default_kb_dir

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "src" / "profile_agent" / "static"

CERT_ORDER = [
    "Splunk Core Certified Consultant",
    "Enterprise Certified Architect",
    "Splunk Certified Instructor",
]


def public_texts() -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in sorted(default_kb_dir().rglob("*.md")):
        texts[str(path.relative_to(ROOT))] = path.read_text(encoding="utf-8")
    for path in sorted(STATIC.iterdir()):
        if path.suffix in {".html", ".js", ".css"}:
            texts[str(path.relative_to(ROOT))] = path.read_text(encoding="utf-8")
    texts["README.md"] = (ROOT / "README.md").read_text(encoding="utf-8")
    texts["chat.py:SYSTEM_PROMPT"] = SYSTEM_PROMPT
    for lang, text in DECLINE_TEXT.items():
        texts[f"chat.py:DECLINE_TEXT[{lang}]"] = text
    return texts


@pytest.mark.parametrize("forbidden", ["TripleTen", "Edenor"])
def test_forbidden_names_never_appear(forbidden: str) -> None:
    offenders = [name for name, text in public_texts().items() if forbidden.lower() in text.lower()]
    assert offenders == [], f"{forbidden!r} found in {offenders}"


def test_target_minds_only_in_the_experience_document() -> None:
    offenders = [name for name, text in public_texts().items() if "target minds" in text.lower()]
    assert set(offenders) <= {"knowledge/en/experience.md", "knowledge/es/experience.md"}, offenders


def test_no_soar_certification_claim() -> None:
    pattern = re.compile(r"(certif\w*\s+(?:\w+\s+){0,3}SOAR|SOAR\s+(?:\w+\s+){0,3}certif\w*)", re.I)
    for name, text in public_texts().items():
        for m in pattern.finditer(text):
            line_end = text.find("\n", m.end())
            line = text[text.rfind("\n", 0, m.start()) + 1 : line_end if line_end >= 0 else None]
            if line.rstrip().endswith("?"):
                continue  # a question about it is fine; only statements are checked
            context = text[max(0, m.start() - 40) : m.end() + 40]
            # the only allowed statements say explicitly that there is NO certification
            denial = r"\b(does not hold|no tiene|never as|nunca como|not a certification)\b"
            assert re.search(denial, context, re.I), (
                f"{name}: possible SOAR certification claim: ...{context}..."
            )


def test_certifications_keep_the_agreed_order() -> None:
    for name, text in public_texts().items():
        positions = [text.find(c) for c in CERT_ORDER]
        if all(p >= 0 for p in positions):
            assert positions == sorted(positions), f"{name}: certifications out of order"


def test_honest_copy_never_promises_zero_hallucinations() -> None:
    for name, text in public_texts().items():
        assert "zero hallucination" not in text.lower(), name
        assert "cero alucinacion" not in text.lower().replace("ó", "o"), name
