# Design

A dark, professional CV page in navy blue, taken from the LinkedIn banner. Navigation: a sticky bar with the seven sections (Perfil, Preguntar, Experiencia, Formación, Competencias, Proyectos, MCP) and scroll-spy marking the one in view; on phones the links become a horizontally scrollable row under the name; a floating "Preguntar" button appears once the question box is scrolled past and returns to it with the input focused. Reading order: portrait, name, role line ("Ingeniero de ciberseguridad y arquitecto de SIEM"), the first-person statement and the credentials; a strip that says who the site is for and that an AI assistant answers on Leandro's behalf from his documents; the question box, whose answers come only from the documents; the CV itself (professional experience with measurable results, education, skills by area); six project cards; the MCP band; numbers; how it works. Spanish by default, English one click away. Built with the impeccable, ui-ux-pro-max and design-taste-frontend skills; house rules from design-taste-frontend apply (no hairline rules, no eyebrows, no index numbers, no monospace outside code, no shadows at rest, one accent).

## Palette

| Token | Value | Role |
|---|---|---|
| `--ground` | `#0e1829` | Page and the sticky bar |
| `--raised` | `#152440` | Cards, panels, ask bar, audience strip, numbers band, read CV blocks |
| `--step` / `--step-2` | `#1d3156` / `#26406e` | Chips, tiles, topic buttons, MCP band (tone step instead of borders) |
| `--ink` | `#eef3fb` | Text and the name |
| `--ink-2` / `--ink-3` | `#c3cfe0` / `#8a9bb5` | Secondary text, dates |
| `--blue` | `#2f6bc0` | The one accent (AA on white): CV button, ask button, selected audience tab |
| `--blue-hi` | `#7fb0ec` | Links, cited tiles, focus ring, big numbers, bullets |
| `--read` | `#2b4a7a` | Read tiles, read topic badges, cited CV blocks, citation pills |
| `--cited` | `#7fb0ec` on `#0b1a30` | Cited tiles and badges with their number |

## Type

Lexend (500–600) for headings, the name, the role line, dates and topic buttons; Source Sans 3 for text at 16–18px. Monospace only inside real code (MCP endpoint, snippets, tool names).

## Layout, top to bottom

- Hero: portrait (220px) · name, role line and sub-line, LinkedIn statement, credentials as an inline list (the three Splunk certifications in the agreed order, the Master's in Data Science, cloud experience on AWS, Azure and Google Cloud) · contact card with a compact CV button (44px, not full width), the other CV, email with copy, LinkedIn, GitHub and location. A quiet heat map of cells pulses behind the right side (the detection-coverage motif), masked so it never sits under text. At ≤1100px the contact card spans below; at ≤760px it moves after the answer so the question comes first.
- Audience strip: three tabs (technical, sales, People) that swap one sentence on what to ask, plus the standing disclosure about the AI assistant. The selected tab also changes the three starter chips and travels with every question as `audience`, so the answer takes the matching shape (engineering detail, interview answer, or business outcome and next step) without changing facts or citations.
- Ask: visible label, pill input with blue submit, three starter chips, answer card with reserved height, citations as pills, sources grouped by document, two quiet follow-ups.
- Professional experience: a dated list (150px date column, Lexend) with role · organisation and two or three result bullets per role, taken from LinkedIn; "Ask about this role" under each. Each block carries `data-keys` (document#fragment) and lights up when an answer reads it (`--raised`) or cites it (`--read` plus the citation number).
- Education and skills side by side (5fr / 6fr): dated education list with grade and thesis notes and the languages line; skills as a definition list of eight areas (SIEM platforms, data, detection, AI, cloud, data science, compliance, leadership and training), each row lighting up with its sections.
- Projects: six cards with real pictures (Elastic detection rules from the lab for the agentic-AI work, the mitre-coverage-kit terminal report, a rendered view of splunk-mcp-readonly's tools and guard, the multi-site Splunk architecture diagram, the PresupuestAR showreel frame, a screenshot of the topics block). Title, one paragraph, link; no tags above titles.
- Topics live under the question box: a quiet "Más temas" toggle opens one row of topic links (areas and case studies); picking one swaps the three suggestion chips for that topic's questions without moving the page. The old source-map section is gone; what an answer read and cited shows in the answer's source list and in the CV blocks that light up.
- MCP band on `--step`: heading and one sentence left; URL with "Copy URL" and a "How to connect it" disclosure (client tabs and the six tools) right.
- Numbers band (12+ years in IT, 15 SIEM clients, 2,000+ rules, 200+ sources), How it works in two columns, footer with the name at full width.

## Motion

Entrances only play on a visible page (`.motion` is added by JS unless the tab is hidden or reduced motion is set): staggered rise of the hero, sections revealing once on scroll, hero heat-map cells brightening and dimming on their own clocks (CSS only). Per answer, read blocks and tiles fill in retrieval order and cited ones turn light blue with a small pop in citation order; the audience sentence and topic panels rise when they change. All motion is transform, opacity or colour, and disabled under `prefers-reduced-motion`.
