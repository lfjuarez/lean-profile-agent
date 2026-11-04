"""FastAPI app: the page, the chat API (SSE), the CV files and the MCP endpoint, in one process."""

from __future__ import annotations

import contextlib
import json
import logging
import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import BaseModel, Field

from .chat import Backend, ProfileChat, validate_messages
from .kb import LANGS, load_kb
from .mcp_server import CV_PATHS, build_server
from .ratelimit import DailyCap, TokenBucket
from .retrieval import Index

log = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).with_name("static")
MATRIX_COLUMNS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("Perfil", "Profile", ("profile",)),
    ("Certificaciones", "Certifications", ("certifications",)),
    ("Experiencia", "Experience", ("experience",)),
    ("Competencias", "Skills", ("skills",)),
    ("Cómo trabajo", "How I work", ("ways-of-working",)),
    ("Servicios", "Services", ("services",)),
    ("Contratación", "Hiring", ("rates", "contact")),
    (
        "Casos",
        "Case studies",
        ("case-detection-coverage", "case-multisite-platform", "case-soar-triage"),
    ),
)
CASE_SHORT = {
    "case-detection-coverage": ("Cobertura MITRE", "MITRE coverage"),
    "case-multisite-platform": ("Plataforma multi-site", "Multi-site platform"),
    "case-soar-triage": ("Triage con SOAR", "SOAR triage"),
    "rates": ("Tarifas", "Rates"),
    "contact": ("Contacto", "Contact"),
}
STARTER_DOCS = (
    "profile",
    "case-soar-triage",
    "ways-of-working",
    "experience",
    "certifications",
    "skills",
)


def default_cv_dir() -> Path:
    env = os.environ.get("PROFILE_CV_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[2] / "cv"


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=20)
    lang: str | None = None


def _client_ip(scope: dict[str, Any]) -> str:
    for name, value in scope.get("headers", []):
        if name == b"x-forwarded-for":
            return value.decode().split(",")[0].strip()
    client = scope.get("client")
    return client[0] if client else "unknown"


class RateLimitMiddleware:
    """Pure ASGI middleware: one token bucket per client for the chat API and one for MCP."""

    def __init__(self, app: Any, chat: TokenBucket, mcp: TokenBucket) -> None:
        self.app = app
        self.chat = chat
        self.mcp = mcp

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] == "http":
            path = scope.get("path", "")
            bucket = None
            if path == "/api/chat" and scope.get("method") == "POST":
                bucket = self.chat
            elif path == "/mcp" or path.startswith("/mcp/"):
                bucket = self.mcp
            if bucket is not None:
                allowed, retry = bucket.allow(_client_ip(scope))
                if not allowed:
                    response = JSONResponse(
                        {"error": "rate_limited", "retry_after": round(retry, 1)},
                        status_code=429,
                        headers={"Retry-After": str(max(1, int(retry + 0.999)))},
                    )
                    await response(scope, receive, send)
                    return
        await self.app(scope, receive, send)


def _sse(event: str, data: Any) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def create_app(
    backend: Backend | None = None,
    chat_limit: tuple[int, int] = (10, 300),
    mcp_limit: tuple[int, int] = (60, 60),
    daily_limit: int | None = None,
    cv_dir: Path | None = None,
) -> FastAPI:
    kbs = {lang: load_kb(lang) for lang in LANGS}
    indexes = {lang: Index(kb) for lang, kb in kbs.items()}
    chat = ProfileChat(indexes, backend=backend)
    cv_root = (cv_dir or default_cv_dir()).resolve()
    daily = DailyCap(daily_limit or int(os.environ.get("CHAT_DAILY_LIMIT", "300")))

    mcp_server = build_server(kbs)
    mcp_app = mcp_server.streamable_http_app(
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        # Public, read-only, no sessions and no secrets: DNS-rebinding protection would only
        # block legitimate hosts (the Cloud Run domain, a custom domain) for no gain.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        host="0.0.0.0",  # noqa: S104 - informs the SDK we are not a localhost-only server
    )

    @contextlib.asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        async with mcp_server.session_manager.run():
            yield

    app = FastAPI(title="lean-profile-agent", docs_url=None, redoc_url=None, lifespan=lifespan)
    app.state.chat = chat
    app.state.kbs = kbs

    @app.get("/healthz")
    @app.get("/health")  # Cloud Run's front end reserves paths ending in "z"
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    async def home() -> FileResponse:
        # Revalidate on every visit (cheap thanks to ETag) so edits show up without a hard reload.
        return FileResponse(
            STATIC_DIR / "index.html",
            media_type="text/html",
            headers={"Cache-Control": "no-cache"},
        )

    @app.get("/api/suggestions")
    async def suggestions(lang: str = "en") -> dict[str, Any]:
        lang = lang if lang in kbs else "en"
        kb = kbs[lang]
        questions = [kb.get(doc_id).questions[0] for doc_id in STARTER_DOCS]
        return {"lang": lang, "questions": questions}

    @app.get("/api/matrix")
    async def matrix(lang: str = "en") -> dict[str, Any]:
        lang = lang if lang in kbs else "en"
        kb = kbs[lang]
        columns = []
        for col_n, (label_es, label_en, doc_ids) in enumerate(MATRIX_COLUMNS, start=1):
            cells = []
            for doc_id in doc_ids:
                doc = kb.get(doc_id)
                group = CASE_SHORT.get(doc_id, (None, None))[0 if lang == "es" else 1]
                for sec in doc.sections:
                    cells.append(
                        {
                            "id": f"{doc.id}#{sec.id}",
                            "code": f"LJ-{col_n}{len(cells) + 1:02d}",
                            "title": sec.title,
                            "doc_title": doc.title,
                            "group": group,
                        }
                    )
            columns.append({"label": label_es if lang == "es" else label_en, "cells": cells})
        return {"lang": lang, "columns": columns}

    @app.post("/api/chat")
    async def chat_endpoint(body: ChatRequest) -> StreamingResponse:
        messages = [m.model_dump() for m in body.messages]
        try:
            validate_messages(messages)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not daily.allow():
            raise HTTPException(
                status_code=503, detail="daily chat limit reached; try again tomorrow"
            )

        def generate() -> Iterator[str]:
            for event in chat.stream(messages, lang=body.lang):
                yield _sse(event.type, event.data)

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/cv/{name}")
    async def cv(name: str) -> FileResponse:
        allowed = {Path(p).name for p in CV_PATHS.values()}
        if name not in allowed:
            raise HTTPException(status_code=404)
        path = cv_root / name
        if not path.is_file():
            raise HTTPException(status_code=404, detail="CV not available on this server")
        return FileResponse(path, media_type="application/pdf", filename=name)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.mount("/", mcp_app)  # serves exactly /mcp; everything else unmatched is a 404

    app.add_middleware(
        RateLimitMiddleware,
        chat=TokenBucket(capacity=chat_limit[0], per_seconds=chat_limit[1]),
        mcp=TokenBucket(capacity=mcp_limit[0], per_seconds=mcp_limit[1]),
    )
    return app


def _configure_logging() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"), format="%(levelname)s %(name)s: %(message)s"
    )


app: FastAPI | None = None


def get_app() -> FastAPI:
    """Uvicorn factory target: ``uvicorn profile_agent.web:get_app --factory``."""
    global app
    if app is None:
        _configure_logging()
        app = create_app()
    return app
