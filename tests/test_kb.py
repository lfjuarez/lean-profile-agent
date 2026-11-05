"""The knowledge base loads from markdown and both languages stay in sync."""

from __future__ import annotations

import pytest

from profile_agent.kb import KnowledgeBase, load_kb

EXPECTED_DOC_IDS = {
    "profile",
    "certifications",
    "experience",
    "skills",
    "ways-of-working",
    "interview",
    "projects",
    "services",
    "rates",
    "contact",
    "case-detection-coverage",
    "case-multisite-platform",
    "case-soar-triage",
}


def test_loads_every_document_with_front_matter(kb_en: KnowledgeBase) -> None:
    assert {d.id for d in kb_en.docs} == EXPECTED_DOC_IDS
    profile = kb_en.get("profile")
    assert profile.title == "Profile summary"
    assert profile.lang == "en"
    assert len(profile.questions) >= 3


def test_sections_become_chunks_with_stable_ids(kb_en: KnowledgeBase) -> None:
    chunks = kb_en.chunks
    ids = [c.id for c in chunks]
    assert len(ids) == len(set(ids)), "chunk ids must be unique"
    summary = next(c for c in chunks if c.id == "profile#summary")
    assert summary.doc_id == "profile"
    assert summary.section_title == "Summary"
    assert "Splunk Core Certified Consultant" in summary.text
    assert not summary.text.startswith("#")


def test_chunk_text_excludes_front_matter(kb_en: KnowledgeBase) -> None:
    for chunk in kb_en.chunks:
        assert "questions:" not in chunk.text
        assert "---" not in chunk.text.splitlines()[0]


def test_case_studies_are_marked(kb_en: KnowledgeBase) -> None:
    cases = kb_en.case_studies()
    assert [c.id for c in cases] == [
        "case-detection-coverage",
        "case-multisite-platform",
        "case-soar-triage",
    ]


def test_languages_have_identical_structure(kb_en: KnowledgeBase, kb_es: KnowledgeBase) -> None:
    assert [d.id for d in kb_en.docs] == [d.id for d in kb_es.docs]
    for en, es in zip(kb_en.docs, kb_es.docs, strict=True):
        assert len(en.sections) == len(es.sections), f"{en.id}: section count differs"
        assert len(en.questions) == len(es.questions), f"{en.id}: question count differs"


def test_unknown_language_is_rejected() -> None:
    with pytest.raises(ValueError):
        load_kb("fr")


def test_unknown_doc_raises(kb_en: KnowledgeBase) -> None:
    with pytest.raises(KeyError):
        kb_en.get("nope")


def test_no_rates_or_availability_are_published() -> None:
    """Lean shares his projects as gifts; the site publishes no prices, rates or hours."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    texts = [p.read_text() for p in (root / "knowledge").rglob("*.md")]
    texts += [(root / "src/profile_agent/static" / f).read_text() for f in ("index.html", "app.js")]
    banned = re.compile(r"USD \d|EUR \d|por hora|per hour|20 a 30 horas|20 to 30 hours")
    for text in texts:
        assert not banned.search(text), banned.search(text).group(0)
