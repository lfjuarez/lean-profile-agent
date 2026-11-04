# Connecting the MCP server

The endpoint is `https://<your-service>/mcp` (Streamable HTTP, stateless, no authentication,
rate-limited to 60 requests per minute per client). Locally it is `http://localhost:8080/mcp`.

## Claude Code

```bash
claude mcp add --transport http lean-profile https://<your-service>/mcp
```

Then ask, for example: "Use the lean-profile tools: what is Leandro's experience with SOAR?"

## Claude Desktop / claude.ai

Settings → Connectors → Add custom connector → paste the URL. On older desktop builds without
custom connectors, add `claude_desktop_config.json` from this folder (it bridges through
`mcp-remote`).

## ChatGPT

Settings → Connectors → Advanced → Developer mode → Create. Name: "Lean profile". MCP server
URL: the endpoint above. Authentication: none.

## Any MCP client (Python)

```python
import asyncio

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main() -> None:
    async with streamable_http_client("http://localhost:8080/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search_experience", {"query": "Splunk SOAR"})
            print(result.structured_content)


asyncio.run(main())
```

## Tools

| Tool | Arguments | Returns |
|---|---|---|
| `profile_summary` | `lang` | summary, what he does, differentiators, certifications in order, education, contact |
| `search_experience` | `query`, `lang` (auto), `k` (≤ 10) | ranked sections with document and section names |
| `list_case_studies` | `lang` | id, title and context paragraph of each case study |
| `get_case_study` | `id`, `lang` | full case study, section by section |
| `availability_and_rates` | `lang` | availability, hourly rate, package starting prices, how to start |
| `contact` | — | email, LinkedIn, location, languages, CV paths |
