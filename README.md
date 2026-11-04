# lean-profile-agent

Chat with my professional profile, grounded in my own documents and cited on every answer, plus
the same knowledge base exposed as a read-only [MCP](https://modelcontextprotocol.io) server so
a recruiter or client can ask from Claude, ChatGPT or any MCP client.

I am Leandro F. Juárez: Splunk Core Certified Consultant, Splunk Enterprise Certified Architect
and Splunk Certified Instructor (Power User Fast Start, authorized by Splunk), working on SIEM,
SOAR, detection engineering and AI engineering for security teams. This repository is both my
"living CV" and a small, honest example of the AI/MCP work I do for clients.

**Answers come only from my documented experience, with sources.** When something is not in the
documents, the assistant says so and points you to me. This is not a promise of perfection: the
retrieval is deterministic and the model is instructed and tested to cite, but every answer
still shows its sources and the CV is one click away.

## What is inside

| Piece | Where | What it does |
|---|---|---|
| Knowledge base | `knowledge/en`, `knowledge/es` | Ten curated markdown documents per language (profile, certifications, experience, skills, services, rates, contact, three case studies). Same ids and sections in both languages, enforced by tests. |
| Retrieval | `src/profile_agent/retrieval.py` | BM25 over sections with accent folding, ES/EN stopwords and light stemming. No embeddings: a few dozen sections do not need them, and lexical retrieval is deterministic and testable. A score floor declines questions before the model is called. |
| Chat | `src/profile_agent/chat.py` | Claude Sonnet 5.5 (`claude-sonnet-5-5`) through the official SDK, streaming, adaptive thinking at low effort, cached system prompt, server-side refusal fallback. The retrieved sections go in the user turn as numbered sources; `[n]` citations are mapped back to document and section. Follow-up chips come from the knowledge base, not from the model. |
| MCP server | `src/profile_agent/mcp_server.py` | `MCPServer` (mcp 2.x), Streamable HTTP, stateless, JSON responses, mounted at `/mcp`. Six read-only tools, no secrets. |
| Web app | `src/profile_agent/web.py`, `static/` | FastAPI: the page, `/api/chat` (SSE), `/api/suggestions`, `/cv/*`, `/healthz`, `/mcp`. Per-client rate limits and a global daily cap on model calls. |
| Tests | `tests/` | Retrieval grounding, chat grounding with a fake backend, every MCP tool plus a Streamable HTTP round trip, the web routes, and Lean's editorial hard rules. |

## Run it locally

Requires Python 3.11+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp /path/to/Leandro_Juarez_CV_EN.pdf cv/   # optional, see cv/README.md
export ANTHROPIC_API_KEY=sk-ant-...        # only the chat needs it; MCP and the page work without
profile-agent                              # http://localhost:8080
```

Tests and lint:

```bash
pytest -q
ruff check src tests
```

Chat backend: `PROFILE_PROVIDER=anthropic` (default, `ANTHROPIC_API_KEY`, `PROFILE_MODEL`),
`gemini` (`GEMINI_API_KEY`, `GEMINI_MODEL`, default `gemini-flash-lite-latest`) or `openrouter`
(`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`). `eval/compare_models.py` runs the same twelve
questions through any of them and writes a side-by-side report with automatic checks.

Other environment variables: `ANTHROPIC_API_KEY` (chat), `PROFILE_MODEL` (default `claude-sonnet-5-5`),
`CHAT_DAILY_LIMIT` (default 300 model calls per day), `PROFILE_KB_DIR`, `PROFILE_CV_DIR`, `PORT`.

## Use the MCP server

Endpoint: `https://<your-service>/mcp` (locally `http://localhost:8080/mcp`). See
[examples/clients.md](examples/clients.md) for Claude Code, Claude Desktop, ChatGPT and a Python
client, and [examples/claude_desktop_config.json](examples/claude_desktop_config.json).

```bash
claude mcp add --transport http lean-profile https://<your-service>/mcp
```

Tools: `profile_summary(lang)`, `search_experience(query, lang, k)`, `list_case_studies(lang)`,
`get_case_study(id, lang)`, `availability_and_rates(lang)`, `contact()`.

## How the chat stays grounded

1. The last user message is tokenized and matched against the sections of the knowledge base in
   the requested language (`lang`, or detected from the question).
2. If the best match is weak or covers too few of the question's terms, the server answers with
   a fixed "not in my documented experience" message and never calls the model.
3. Otherwise the top sections are sent as `<source n="…" doc="…" section="…">` blocks with the
   question. The system prompt allows only those sources, requires `[n]` citations, and treats
   the question text as data, not instructions.
4. The server streams the text, then emits the sources that were actually cited and three
   follow-up questions taken from the documents just used.

`tests/test_hard_rules.py` keeps the public copy honest: certifications always in the agreed
order, no certification claims that do not exist, and a few names that must never appear.

## Deploy to Cloud Run

`deploy/cloud-run.sh` holds the recipe (Secret Manager for the API key, `gcloud run deploy
--source .`, region `us-east1` (Cloud Run domain mappings are not available in southamerica-east1), scale to zero). It does not run by itself; read it,
set `PROJECT` (and `PROVIDER=gemini` or `anthropic`, default `gemini`), and run it when you are ready. The Dockerfile copies `knowledge/` and `cv/` into
the image; the CV PDFs are git-ignored on purpose.

## Design notes

The full design is in `docs/superpowers/specs/2026-11-03-profile-agent-design.md`. In short:
Python to match my other public repositories, one process for page + API + MCP so one small
container serves everything, lexical retrieval because the corpus is tiny and must be auditable,
and knowledge-base-driven follow-ups because suggestions should never be invented.

## License

MIT. Case study figures are synthetic; the method, design decisions and deliverables are the
real ones, as every case study states.
