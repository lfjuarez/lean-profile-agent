"""Read-only MCP server over the knowledge base (Streamable HTTP, mounted by ``web.py``).

Every tool answers from the same curated markdown the chat uses. Nothing here reads secrets or
calls the model; the server can be added to Claude Desktop, ChatGPT or any MCP client.
"""

from __future__ import annotations

import re
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .kb import LANGS, KnowledgeBase, load_kb
from .retrieval import Index, detect_lang

NAME = "Leandro Federico Juárez"
MAX_RESULTS = 10
CV_PATHS = {"en": "/cv/Leandro_Juarez_CV_EN.pdf", "es": "/cv/Leandro_Juarez_CV_ES.pdf"}
READ_ONLY = ToolAnnotations(
    read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False
)

INSTRUCTIONS = (
    "Read-only access to the documented professional profile of Leandro Federico Juárez "
    "(Splunk Core Certified Consultant, Enterprise Certified Architect, Splunk Certified "
    "Instructor; SIEM, SOAR, detection engineering and AI engineering). Answers come only from "
    "his curated documents, with the document and section for every result; say so when "
    "something is not covered. Use lang='es' for Spanish, 'en' for English (default)."
)


def _lang(value: str | None) -> str:
    return value if value in LANGS else "en"


def _sections(kb: KnowledgeBase, doc_id: str) -> dict[str, str]:
    return {s.id: s.text for s in kb.get(doc_id).sections}


def build_server(kbs: dict[str, KnowledgeBase] | None = None) -> MCPServer:
    kbs = kbs or {lang: load_kb(lang) for lang in LANGS}
    indexes = {lang: Index(kb) for lang, kb in kbs.items()}
    server = MCPServer("lean-profile", instructions=INSTRUCTIONS, version="0.1.0")

    @server.tool(annotations=READ_ONLY)
    def profile_summary(lang: str = "en") -> dict[str, Any]:
        """Who Leandro is in one call: summary, what he does, differentiators, certifications
        in order, education, languages, location and contact.

        Args:
            lang: 'en' (default) or 'es'. Unknown values fall back to English.

        Every text comes from the 'profile' and 'certifications' documents of his knowledge base.
        """
        lang = _lang(lang)
        kb = kbs[lang]
        profile = _sections(kb, "profile")
        certs_text = kb.get("certifications").sections[0].text
        certs = [m.group(1).strip() for m in re.finditer(r"^\d+\.\s+([^(\n.]+)", certs_text, re.M)]
        return {
            "name": NAME,
            "lang": lang,
            "headline": kb.get("profile").title,
            "summary": profile[next(iter(profile))],
            "sections": {s.title: s.text for s in kb.get("profile").sections},
            "certifications": certs,
            "contact": {
                "email": "l.federico.juarez@gmail.com",
                "linkedin": "https://www.linkedin.com/in/leandrofjuarez",
            },
            "source": "profile",
        }

    @server.tool(annotations=READ_ONLY)
    def search_experience(query: str, lang: str = "", k: int = 5) -> dict[str, Any]:
        """Search Leandro's documented experience, skills, services, projects and case studies.

        Args:
            query: Free text, in English or Spanish (language is detected when lang is empty).
            lang: 'en' or 'es'; leave empty to detect from the query.
            k: Number of sections to return (default 5, maximum 10).

        Returns ranked sections with the document and section they come from, so the caller can
        cite them. An empty list with a note means the question is not covered by his documents.
        """
        lang = _lang(lang) if lang else detect_lang(query, default="en")
        index = indexes[lang]
        limit = max(1, min(int(k), MAX_RESULTS))
        hits = index.search(query, k=limit)
        answerable = index.is_answerable(hits, query)
        results = [
            {
                "id": h.chunk.id,
                "doc_id": h.chunk.doc_id,
                "doc": h.chunk.doc_title,
                "section": h.chunk.section_title,
                "score": round(h.score, 3),
                "text": h.chunk.text,
            }
            for h in (hits if answerable else [])
        ]
        note = (
            "Results come from Leandro's curated documents; cite doc and section."
            if results
            else (
                "Not covered by Leandro's documented experience. "
                "Ask him directly (see the contact tool)."
            )
        )
        return {"query": query, "lang": lang, "results": results, "note": note}

    @server.tool(annotations=READ_ONLY)
    def list_case_studies(lang: str = "en") -> dict[str, Any]:
        """List the published case studies (id, title, one-paragraph context).

        Args:
            lang: 'en' (default) or 'es'.

        Figures in the case studies are synthetic; the method, design decisions and deliverables
        are the real ones, as each case states. Use get_case_study(id) for the full text.
        """
        lang = _lang(lang)
        cases = [
            {"id": d.id, "title": d.title, "summary": d.sections[0].text}
            for d in kbs[lang].case_studies()
        ]
        return {"lang": lang, "case_studies": cases}

    @server.tool(annotations=READ_ONLY)
    def get_case_study(id: str, lang: str = "en") -> dict[str, Any]:
        """Full text of one case study, section by section.

        Args:
            id: One of the ids returned by list_case_studies (e.g. 'case-soar-triage').
            lang: 'en' (default) or 'es'.
        """
        lang = _lang(lang)
        kb = kbs[lang]
        ids = [d.id for d in kb.case_studies()]
        if id not in ids:
            return {"error": f"unknown case study {id!r}; valid ids: {', '.join(ids)}"}
        doc = kb.get(id)
        return {
            "id": doc.id,
            "lang": lang,
            "title": doc.title,
            "sections": [{"id": s.id, "title": s.title, "text": s.text} for s in doc.sections],
        }

    @server.tool(annotations=READ_ONLY)
    def availability_and_rates(lang: str = "en") -> dict[str, Any]:
        """Whether rates and availability are published. They are not: the answer is a short
        note with how to get in touch privately.

        Args:
            lang: 'en' (default) or 'es'.
        """
        lang = _lang(lang)
        sec = _sections(kbs[lang], "rates")
        return {
            "lang": lang,
            "published": False,
            "note": next(iter(sec.values())),
            "contact": "l.federico.juarez@gmail.com",
            "source": "rates",
        }

    @server.tool(annotations=READ_ONLY)
    def contact() -> dict[str, Any]:
        """How to reach Leandro: email, LinkedIn, location, languages and CV download paths.

        The CV paths are relative to the web app that hosts this MCP server.
        """
        return {
            "name": NAME,
            "email": "l.federico.juarez@gmail.com",
            "linkedin": "https://www.linkedin.com/in/leandrofjuarez",
            "location": "Buenos Aires, Argentina (remote)",
            "languages": ["Spanish (native)", "English (advanced)"],
            "cv": dict(CV_PATHS),
        }

    return server
