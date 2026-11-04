"""HTTP surface: page, chat SSE, suggestions, CV download, rate limits and the MCP mount."""

from __future__ import annotations

import json
import socket
import threading
import time
from collections.abc import Iterator

import pytest
import uvicorn
from fastapi.testclient import TestClient

from profile_agent.web import create_app
from tests.test_chat import FakeBackend


def parse_sse(body: str) -> list[tuple[str, object]]:
    events: list[tuple[str, object]] = []
    for block in body.strip().split("\n\n"):
        kind, data = None, None
        for line in block.splitlines():
            if line.startswith("event: "):
                kind = line[7:]
            elif line.startswith("data: "):
                data = json.loads(line[6:])
        if kind:
            events.append((kind, data))
    return events


@pytest.fixture
def backend() -> FakeBackend:
    return FakeBackend(answer="Nine certifications [1]. Instructor since 2025 [2].")


@pytest.fixture
def cv_dir(tmp_path):
    """CV PDFs are git-ignored, so tests serve a stand-in file."""
    (tmp_path / "Leandro_Juarez_CV_EN.pdf").write_bytes(b"%PDF-1.4 test")
    return tmp_path


@pytest.fixture
def client(backend: FakeBackend, cv_dir) -> Iterator[TestClient]:
    app = create_app(backend=backend, cv_dir=cv_dir)
    with TestClient(app) as c:
        yield c


def test_home_page_is_bilingual_and_honest(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    assert "Leandro" in html
    assert "documented experience" in html
    assert "zero hallucinations" not in html.lower()
    js = client.get("/static/app.js").text
    assert "experiencia documentada" in js and "documented experience" in js
    assert "zero hallucinations" not in js.lower()
    assert 'data-lang="es"' in html and 'data-lang="en"' in html
    assert "/cv/Leandro_Juarez_CV_EN.pdf" in html and "/cv/Leandro_Juarez_CV_ES.pdf" in html
    assert "/mcp" in html


def test_healthz(client: TestClient) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/health").json() == {"status": "ok"}


def test_cv_download_and_404(client: TestClient) -> None:
    r = client.get("/cv/Leandro_Juarez_CV_EN.pdf")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert client.get("/cv/other.pdf").status_code == 404
    assert client.get("/cv/../pyproject.toml").status_code in (404, 400)


def test_suggestions_per_language(client: TestClient) -> None:
    es = client.get("/api/suggestions", params={"lang": "es"}).json()
    en = client.get("/api/suggestions", params={"lang": "en"}).json()
    assert 3 <= len(es["questions"]) <= 6 and 3 <= len(en["questions"]) <= 6
    assert es["questions"] != en["questions"]
    assert any("¿" in q for q in es["questions"])


def test_chat_streams_sse_with_sources_and_followups(
    client: TestClient, backend: FakeBackend
) -> None:
    r = client.post(
        "/api/chat",
        json={
            "messages": [{"role": "user", "content": "Which Splunk certifications do you hold?"}],
            "lang": "en",
        },
    )
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/event-stream")
    events = parse_sse(r.text)
    kinds = [k for k, _ in events]
    assert kinds[:2] == ["retrieved", "text"] and kinds[-1] == "done"
    assert "sources" in kinds and "followups" in kinds
    sources = dict(events)["sources"]
    assert sources[0]["doc_id"] == "certifications"
    assert len(backend.calls) == 1


def test_chat_rejects_bad_payloads(client: TestClient) -> None:
    assert client.post("/api/chat", json={"messages": []}).status_code in (400, 422)
    assert (
        client.post(
            "/api/chat", json={"messages": [{"role": "user", "content": "x" * 2000}]}
        ).status_code
        == 400
    )
    assert client.post("/api/chat", json={"nope": 1}).status_code in (400, 422)


def test_chat_rate_limit_returns_429(backend: FakeBackend) -> None:
    app = create_app(backend=backend, chat_limit=(2, 60), daily_limit=100)
    with TestClient(app) as c:
        payload = {"messages": [{"role": "user", "content": "What are your rates?"}], "lang": "en"}
        assert c.post("/api/chat", json=payload).status_code == 200
        assert c.post("/api/chat", json=payload).status_code == 200
        r = c.post("/api/chat", json=payload)
        assert r.status_code == 429
        assert "retry-after" in r.headers


def test_daily_cap_returns_503(backend: FakeBackend) -> None:
    app = create_app(backend=backend, chat_limit=(100, 60), daily_limit=1)
    with TestClient(app) as c:
        payload = {"messages": [{"role": "user", "content": "What are your rates?"}], "lang": "en"}
        assert c.post("/api/chat", json=payload).status_code == 200
        assert c.post("/api/chat", json=payload).status_code == 503


def test_decline_path_never_calls_backend(client: TestClient, backend: FakeBackend) -> None:
    r = client.post(
        "/api/chat",
        json={"messages": [{"role": "user", "content": "best pizza in Rome?"}], "lang": "en"},
    )
    events = dict(parse_sse(r.text))
    assert events["done"]["grounded"] is False
    assert backend.calls == []


@pytest.fixture(scope="module")
def live_url() -> Iterator[str]:
    """A real uvicorn server, so the MCP session manager lifespan runs."""
    app = create_app(backend=FakeBackend())
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    assert server.started
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)


async def test_mcp_round_trip_over_streamable_http(live_url: str) -> None:
    from mcp.client.session import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    async with streamable_http_client(f"{live_url}/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            assert init.server_info.name == "lean-profile"
            tools = await session.list_tools()
            assert "search_experience" in {t.name for t in tools.tools}
            result = await session.call_tool("contact")
            assert not result.is_error
            assert result.structured_content["email"] == "l.federico.juarez@gmail.com"


def test_mcp_rate_limit(live_url: str) -> None:
    import httpx

    app_limited = create_app(backend=FakeBackend(), mcp_limit=(1, 60))
    with TestClient(app_limited) as c:
        body = {"jsonrpc": "2.0", "id": 1, "method": "ping"}
        headers = {
            "accept": "application/json, text/event-stream",
            "content-type": "application/json",
        }
        first = c.post("/mcp", json=body, headers=headers)
        assert first.status_code != 429
        second = c.post("/mcp", json=body, headers=headers)
        assert second.status_code == 429
    assert httpx  # keep import used (TestClient is httpx based)


def test_matrix_lists_every_section_once(client: TestClient) -> None:
    for lang in ("es", "en"):
        data = client.get("/api/matrix", params={"lang": lang}).json()
        assert data["lang"] == lang
        assert len(data["columns"]) == 8
        cells = [c for col in data["columns"] for c in col["cells"]]
        ids = [c["id"] for c in cells]
        assert len(ids) == len(set(ids))
        kb = client.app.state.kbs[lang]
        assert set(ids) == {c.id for c in kb.chunks}
        assert all(c["code"].startswith("LJ-") for c in cells)
        assert all(col["label"] and col["cells"] for col in data["columns"])


def test_chat_emits_retrieved_before_text(client: TestClient) -> None:
    r = client.post(
        "/api/chat",
        json={"messages": [{"role": "user", "content": "What are your rates?"}], "lang": "en"},
    )
    kinds = [k for k, _ in parse_sse(r.text)]
    assert kinds[0] == "retrieved"
    retrieved = dict(parse_sse(r.text))["retrieved"]
    assert retrieved and all("#" in i for i in retrieved)
