"""The MCP tools are read-only views over the knowledge base."""

from __future__ import annotations

import json
from typing import Any

import pytest
from mcp.types import CallToolResult

from profile_agent.mcp_server import build_server

EXPECTED_TOOLS = {
    "profile_summary",
    "search_experience",
    "list_case_studies",
    "get_case_study",
    "availability_and_rates",
    "contact",
}


@pytest.fixture(scope="module")
def server():
    return build_server()


async def call(server, name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    result = await server.call_tool(name, args or {})
    assert isinstance(result, CallToolResult)
    assert not result.is_error, result
    if result.structured_content is not None:
        return result.structured_content
    return json.loads(result.content[0].text)  # type: ignore[union-attr]


async def test_exposes_exactly_the_six_read_only_tools(server) -> None:
    tools = await server.list_tools()
    assert {t.name for t in tools} == EXPECTED_TOOLS
    for t in tools:
        assert t.annotations is not None and t.annotations.read_only_hint is True, t.name
        assert t.description and len(t.description) > 40, t.name


async def test_profile_summary_is_ordered_and_bilingual(server) -> None:
    en = await call(server, "profile_summary", {"lang": "en"})
    es = await call(server, "profile_summary", {"lang": "es"})
    assert en["name"] == "Leandro Federico Juárez"
    assert en["certifications"][:3] == [
        "Splunk Core Certified Consultant",
        "Splunk Enterprise Certified Architect",
        "Splunk Certified Instructor",
    ]
    assert "Splunk Core Certified Consultant" in en["summary"]
    assert "Maestría" in es["summary"]
    assert en["contact"]["email"] == "l.federico.juarez@gmail.com"
    assert en["source"] == "profile"


async def test_search_experience_returns_cited_sections(server) -> None:
    out = await call(server, "search_experience", {"query": "Splunk SOAR playbooks energy"})
    assert out["lang"] == "en"
    assert out["results"], out
    top = out["results"][0]
    assert {"id", "doc", "section", "text", "score"} <= set(top)
    assert any(r["doc_id"] == "case-soar-triage" for r in out["results"])


async def test_search_experience_detects_spanish(server) -> None:
    out = await call(
        server, "search_experience", {"query": "¿Qué certificaciones de Splunk tenés?"}
    )
    assert out["lang"] == "es"
    assert out["results"][0]["doc_id"] == "certifications"


async def test_search_experience_reports_no_match(server) -> None:
    out = await call(server, "search_experience", {"query": "pizza toppings"})
    assert out["results"] == []
    assert "documented" in out["note"]


async def test_search_experience_caps_k(server) -> None:
    out = await call(server, "search_experience", {"query": "Splunk", "k": 500})
    assert len(out["results"]) <= 10


async def test_list_and_get_case_studies(server) -> None:
    listed = await call(server, "list_case_studies", {"lang": "en"})
    ids = [c["id"] for c in listed["case_studies"]]
    assert ids == ["case-detection-coverage", "case-multisite-platform", "case-soar-triage"]
    assert all(c["title"] and c["summary"] for c in listed["case_studies"])

    one = await call(server, "get_case_study", {"id": "case-soar-triage", "lang": "es"})
    assert one["id"] == "case-soar-triage"
    assert [s["title"] for s in one["sections"]][0] == "Contexto"
    assert "sintéticas" in one["sections"][0]["text"]

    missing = await call(server, "get_case_study", {"id": "case-nope"})
    assert "error" in missing and "case-detection-coverage" in missing["error"]


async def test_availability_and_rates(server) -> None:
    out = await call(server, "availability_and_rates", {"lang": "en"})
    assert "20 to 30 hours" in out["availability"]
    assert "USD 45 to 70" in out["hourly_rate"]
    assert isinstance(out["packages"], list) and len(out["packages"]) >= 8
    assert out["packages"][0].startswith("Splunk health check")


async def test_contact_has_no_secrets_and_is_stable(server) -> None:
    out = await call(server, "contact")
    assert out == {
        "name": "Leandro Federico Juárez",
        "email": "l.federico.juarez@gmail.com",
        "linkedin": "https://www.linkedin.com/in/leandrofjuarez",
        "location": "Buenos Aires, Argentina (remote)",
        "languages": ["Spanish (native)", "English (advanced)"],
        "cv": {"en": "/cv/Leandro_Juarez_CV_EN.pdf", "es": "/cv/Leandro_Juarez_CV_ES.pdf"},
    }


async def test_unknown_language_falls_back_to_english(server) -> None:
    out = await call(server, "profile_summary", {"lang": "fr"})
    assert out["lang"] == "en"
