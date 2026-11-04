# lean-profile-agent — design

Date: 2026-11-03. Status: implemented from this spec; Lean reviews the local demo before anything is deployed.

## Goal

A public "chat with my profile" page for Leandro F. Juárez that doubles as proof of his AI/MCP
consulting work: a grounded, cited Q&A over a curated knowledge base, plus the same knowledge
base exposed as a read-only MCP server a recruiter can add to Claude Desktop or ChatGPT.

Honest framing everywhere: "answers only from my documented experience, with sources". Never
"zero hallucinations".

## Decisions

- **Stack: Python, FastAPI + one static page.** Matches the sibling repos (`mitre-coverage-kit`,
  `splunk-mcp-server`: Python 3.11+, hatchling, src layout, pytest + ruff, MIT, English README).
  One process serves the page, the chat API and the MCP endpoint, so Cloud Run runs one container.
- **Knowledge base = curated markdown, bilingual.** `knowledge/en/*.md` and `knowledge/es/*.md`
  with identical document ids and section structure. Each file has YAML front matter
  (`id`, `title`, `questions`). Chunks are `##` sections. A parity test keeps both languages in
  sync. The KB is the only thing the model may answer from.
- **Retrieval = BM25 over sections, no embeddings.** The KB is ~40 chunks per language; lexical
  retrieval with accent folding and ES/EN stopwords is deterministic, free, and testable. The
  query language (UI toggle, or detected) selects the KB language. A score floor decides whether
  the question is answerable at all; below it the server declines without calling the model.
- **Model: `claude-sonnet-5-5`**, streaming, adaptive thinking at `effort: low`, stable cached
  system prompt, server-side refusal fallback (`fallbacks: "default"`), `max_tokens` 1500.
  The retrieved sections go in the user turn as numbered sources; the model cites `[n]`; the
  server maps `[n]` back to document + section and streams the answer plus a final `sources`
  event. Answers with no citation to a real source are flagged as ungrounded in the UI copy.
- **Follow-up chips are KB-driven, not model-generated.** Each document declares suggested
  questions; after an answer the server picks up to three from the documents that were retrieved
  (minus the one just asked) and from documents not yet visited. Deterministic, bilingual, never
  invented.
- **MCP server: `mcp` 2.x `MCPServer`, Streamable HTTP, stateless, JSON responses**, mounted at
  `/mcp` in the same FastAPI app. Tools: `profile_summary`, `search_experience`,
  `list_case_studies`, `get_case_study`, `availability_and_rates`, `contact`. All read-only,
  all served from the KB, no secrets touched (the Anthropic key is used only by the chat route).
- **Rate limiting** in-memory per client IP (`X-Forwarded-For` first hop on Cloud Run):
  chat 10 requests / 5 min, MCP 60 / min, plus a global daily cap on chat calls
  (`CHAT_DAILY_LIMIT`, default 300) so a public demo cannot run up a bill.
- **Hard rules are tests.** `tests/test_hard_rules.py` scans the KB, the static page and the
  system prompt: no "TripleTen", no "Edenor", no SOAR certification claim, "Target Minds" only
  inside the experience document (as in the CV), certifications always in the order Consultant →
  Architect → Instructor.
- **CV PDFs are deploy-time assets.** `cv/*.pdf` is git-ignored, copied into the Docker image,
  served at `/cv/<file>`. The page links to the EN and ES CV.

## Components

| Unit | Responsibility | Depends on |
|---|---|---|
| `kb.py` | Load `knowledge/<lang>`, parse front matter, split into `Chunk(doc_id, section_id, title, text)` | pyyaml |
| `retrieval.py` | Tokenizer (lowercase, accent fold, stopwords), BM25 index per language, `search(query, lang, k)` with score floor | kb |
| `chat.py` | Build prompt, call Claude (stream), parse `[n]` citations, choose follow-ups, decline path | retrieval, anthropic |
| `mcp_server.py` | `MCPServer` with the six tools | kb, retrieval |
| `ratelimit.py` | Token bucket + daily counter | — |
| `web.py` | FastAPI app: `/`, `/api/chat` (SSE), `/api/suggestions`, `/cv/*`, `/healthz`, mount `/mcp` | all |
| `static/` | `index.html`, `app.js`, `styles.css`; ES/EN toggle, chips, sources, CV download, MCP instructions | — |

## Data flow (chat)

1. Browser POSTs `{messages, lang}` to `/api/chat`.
2. Server validates (≤ 6 turns, ≤ 1,000 chars each), rate-limits, detects language if missing.
3. `retrieval.search(last_user_message, lang, k=6)`. If best score < floor → stream the decline
   text and the contact follow-up; no model call.
4. Otherwise build the user turn: numbered `<source n doc="…" section="…">` blocks + the question;
   stream Claude's answer as `text` events; on completion emit `sources` (only the `[n]` actually
   cited) and `followups`; `done`.
5. Errors (no API key, API error, refusal) become a `error` event with a short bilingual message.

## Error handling

- Missing `ANTHROPIC_API_KEY`: page loads, MCP works, chat returns a clear error event.
- Anthropic errors: typed chain (RateLimitError → APIStatusError → APIConnectionError) → `error` event; logged with request id.
- `stop_reason == "refusal"` after fallback → polite decline event.
- Rate limit → HTTP 429 with `Retry-After`.

## Testing

- `test_kb.py`: parsing, front matter, chunk ids, ES/EN parity.
- `test_retrieval.py`: known questions hit the expected document (both languages); nonsense is below the floor.
- `test_chat.py`: with a fake Anthropic client — prompt contains only KB text, citations map to real sources, decline path never calls the model, follow-ups come from the KB.
- `test_mcp.py`: each tool via `MCPServer.call_tool`, plus one Streamable HTTP round trip through the ASGI app.
- `test_web.py`: routes, SSE framing, 429.
- `test_hard_rules.py`: the forbidden/ordered strings.

## Deploy (recipe only; not run without Lean's go-ahead)

Dockerfile (python:3.12-slim, uvicorn, `PORT`), `deploy/cloud-run.sh` with the `gcloud` commands:
secret `ANTHROPIC_API_KEY` in Secret Manager, `gcloud run deploy --source .`, region
`southamerica-east1`, min instances 0, concurrency 20, 512 MiB.
