# Design

A light, professional CV page: portrait, name and certifications first, then a question box whose answers come only from the documents, and a source map whose tiles light up for each answer. Built with the impeccable, ui-ux-pro-max and design-taste-frontend skills; house rules from design-taste-frontend apply (no hairline rules, no eyebrows, no index numbers, no monospace outside code, no shadows at rest, one accent).

## Palette

| Token | Value | Role |
|---|---|---|
| `--ground` | `#f4f6f5` | Page |
| `--raised` | `#ffffff` | Cards, rows, ask bar |
| `--step` | `#e9eeec` | Chips, tiles, quiet buttons (tone step instead of borders) |
| `--ink` | `#0e1714` | Text, ask button, numbers band |
| `--ink-2` / `--ink-3` | `#39443f` / `#5b6762` | Secondary text |
| `--green` | `#0d6b55` | The one accent: CV button, cited tiles, focus |
| `--read` | `#d9eee6` | Read tiles, citation pills |

## Type

Lexend (600) for headings and the name; Source Sans 3 for text at 17–18px. Monospace only inside real code (MCP endpoint and snippets).

## Layout

- Hero: portrait (220px) · name, statement and certifications · contact card with CV button and visible email, LinkedIn and location. At ≤1100px the contact card spans below; at ≤760px it moves after the answer so the question comes first.
- Ask: visible label, pill input with dark submit, suggestion chips, answer card with reserved height, citations as pills, sources grouped by document.
- Source map: one row per area (and one per case study), tiles with short titles; read tiles pale green, cited tiles green with their number.
- MCP band right after the answer, on the pale green field: heading and one sentence left; URL with "Copy URL" and a "How to connect it" disclosure (client tabs and the six tools) right. On phones the URL takes its own line.
- Three starter suggestions; two follow-ups per answer, shown as quiet text links. Asking never scrolls the page; the answer card keeps its height while streaming and takes focus.
- Numbers band in ink, How it works in two columns, footer with the name at full width.

## Motion

Staggered rise of the hero on load; sections reveal once on scroll; the source map does a single pale-green wave when it first enters view; per answer, read tiles fill in retrieval order and cited tiles turn green with a small pop in citation order. All motion is transform, opacity or colour, and disabled under `prefers-reduced-motion`.
