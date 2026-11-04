# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- Clients who hire freelance or contract work: SOC leads, CISOs and Splunk partner consultancies looking for a Splunk / SIEM / SOAR / detection-engineering specialist. (Inferred from the brief; not confirmed by Lean.)
- Recruiters and people teams screening candidates for contract roles. (Inferred.)
- Technical evaluators who want proof of AI/MCP work and may connect the MCP endpoint from their own assistant.

## Product Purpose
A public "chat with my profile" for Leandro Federico Juárez (Lean). Visitors ask questions and get answers only from his curated documents, each answer citing document and section; the same knowledge base is exposed as a read-only MCP server. Success: the visitor understands what Lean does, trusts the answers, and contacts him, downloads the CV or connects the MCP server. (Primary action not ranked by Lean yet.)

## Positioning
The CV answers questions itself, with sources, and doubles as a working demonstration of the AI/MCP consulting service Lean sells: grounded retrieval, citations, refusals when something is not documented, and an MCP endpoint a recruiter's own assistant can use.

## Operating Context
Visitors arrive from LinkedIn, Upwork, proposals and outreach messages, on desktop and mobile, in Spanish or English. Lean is based in Buenos Aires and works remotely for Latin America, Spain, US and EU clients.

## Capabilities and Constraints
- Bilingual ES/EN page, grounded chat with citations and follow-up chips, CV downloads (EN/ES PDF), MCP section with copyable endpoint and client instructions.
- Chat answers only from `knowledge/`; free Gemini Flash-Lite tier, rate limits and a daily cap.
- Single FastAPI process, static HTML/CSS/JS (no build step), deploy target Google Cloud Run.

## Brand Commitments
- Certifications always in this order: Splunk Core Certified Consultant, Splunk Enterprise Certified Architect, Splunk Certified Instructor (Power User Fast Start, authorized by Splunk).
- Never mention TripleTen; never name Edenor ("a leading electricity distributor in Argentina"); never claim a SOAR certification; Target Minds only in the experience record.
- Honest copy: "answers only from my documented experience, with sources"; never "zero hallucinations".
- Lean's portrait: `src/profile_agent/static/img/lean.jpg` (800×800, provided by Lean 2026-11-04).

## Evidence on Hand
- Knowledge base: 11 documents per language under `knowledge/`.
- Case studies with synthetic figures (detection coverage, multi-site platform, SOAR triage); PDFs and diagrams in `~/Freelance/muestras/pro/out/`.
- Key facts: 12+ years in IT, 6 in SIEM, 2,000+ detection rules migrated with AI agents, 20–30 h/week freelance or contract, immediate start.
- No testimonials, client logos or reviews exist; none may be fabricated.

## Product Principles
1. Every claim is traceable to a document and section.
2. Saying "not documented" is a feature, not a failure.
3. The page itself is proof of the service; show the mechanism working.
4. Spanish and English are equals.
