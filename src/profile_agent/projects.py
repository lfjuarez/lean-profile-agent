"""The projects page: one project at a time, picked from a menu, rendered from the same documents
the chat answers from. Each text is cut into short labelled parts so it reads in a minute."""

from __future__ import annotations

import html
import re
from urllib.parse import quote

from .cv import _SENTENCE_END, PROJECT_LINK
from .kb import KnowledgeBase

LABELS = {
    "es": {
        "title": "Proyectos · Leandro F. Juárez",
        "h1": "Proyectos",
        "menu": "Proyecto",
        "ask": "Preguntar por este proyecto",
        "code": "Código",
        "site": "Sitio",
        "back": "Volver al sitio",
        "other": "EN",
        "other_name": "English version",
        "prev": "Anterior",
        "next": "Siguiente",
        "detail": "En detalle",
        "of": "de",
        "ask_q": "Contame sobre {t}.",
    },
    "en": {
        "title": "Projects · Leandro F. Juárez",
        "h1": "Projects",
        "menu": "Project",
        "ask": "Ask about this project",
        "code": "Code",
        "site": "Site",
        "back": "Back to the site",
        "other": "ES",
        "other_name": "Versión en español",
        "prev": "Previous",
        "next": "Next",
        "detail": "In detail",
        "of": "of",
        "ask_q": "Tell me about {t}.",
    },
}

# Labels that open a part of a project text. "Stack" is shown as chips; the link labels are
# dropped because the links are buttons.
PART_LABELS = {
    "El problema": "problem", "The problem": "problem",
    "Lo que construí": "built", "What I built": "built",
    "Cómo funciona": "how", "How it works": "how",
    "Funciones": "features", "Features": "features",
    "Stack": "stack",
    "Código": "link", "Code": "link", "Sitio en beta": "link", "Beta site": "link",
}
_LABEL = re.compile(r"^(?P<label>[^.:]{2,40}?)(?:, [^.:]{2,30})?:\s+(?P<rest>.+)$", re.S)

# Section id prefix → picture (both languages).
IMAGES = (
    ("ia-agentica", "proj-ai.jpg"),
    ("agentic-ai", "proj-ai.jpg"),
    ("mitre-coverage-kit", "proj-coverage.jpg"),
    ("splunk-mcp-readonly", "proj-mcp.jpg"),
    ("arquitectura", "proj-arch.jpg"),
    ("multi-site", "proj-arch.jpg"),
    ("presupuestar", "proj-presupuestar.jpg"),
    ("este-sitio", "proj-site.jpg"),
    ("this-site", "proj-site.jpg"),
)


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _image(section_id: str) -> str:
    for prefix, name in IMAGES:
        if section_id.startswith(prefix):
            return f"/static/img/{name}"
    return ""


def _split_sentences(text: str) -> list[str]:
    text = " ".join(text.split())
    out, start = [], 0
    for m in _SENTENCE_END.finditer(text):
        out.append(text[start : m.start() + 1])
        start = m.end()
    out.append(text[start:])
    return [s.strip() for s in out if s.strip()]


def _inline(s: str) -> str:
    """Escape, then show `code` spans as code."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _esc(s))


def _parts(text: str, detail: str) -> tuple[str, list[tuple[str, str, list[str]]]]:
    """Return (lead sentence, [(heading, kind, sentences)])."""
    sentences = _split_sentences(text)
    lead, rest = sentences[0], sentences[1:]
    parts: list[tuple[str, str, list[str]]] = []
    for s in rest:
        m = _LABEL.match(s)
        kind = PART_LABELS.get(m.group("label")) if m else None
        if kind == "link":
            continue
        if kind:
            heading = s[: s.index(":")]
            rest = m.group("rest")
            parts.append((heading, kind, [rest[:1].upper() + rest[1:]]))
        elif not parts or parts[-1][1] in ("problem", "stack"):
            # a problem is one sentence; what follows it is the project itself
            parts.append((detail, "detail", [s]))
        else:
            parts[-1][2].append(s)
    return lead, parts


def _part_html(heading: str, kind: str, sentences: list[str]) -> str:
    if kind == "stack":
        items = [i.strip().rstrip(".") for i in " ".join(sentences).split(",") if i.strip()]
        body = '<ul class="chips">' + "".join(f"<li>{_esc(i)}</li>" for i in items) + "</ul>"
    else:
        paras = [" ".join(sentences[i : i + 2]) for i in range(0, len(sentences), 2)]
        body = "".join(f"<p>{_inline(p)}</p>" for p in paras)
    return f'<section class="part part-{kind}"><h3>{_esc(heading)}</h3>{body}</section>'


def render_projects(kb: KnowledgeBase, lang: str) -> str:
    lang = lang if lang in LABELS else "es"
    L = LABELS[lang]
    other = "en" if lang == "es" else "es"
    secs = kb.get("projects").sections
    titles = [re.sub(r"\s*\([^)]*\)\s*$", "", s.title) for s in secs]
    menu = "".join(
        f'<li><a href="#{_esc(s.id)}" data-id="{_esc(s.id)}">{_esc(t)}</a></li>'
        for s, t in zip(secs, titles, strict=True)
    )
    blocks = []
    for i, (sec, title) in enumerate(zip(secs, titles, strict=True)):
        lead, parts = _parts(sec.text, L["detail"])
        links = list(dict.fromkeys(PROJECT_LINK.findall(sec.text)))
        link_html = "".join(
            f'<a class="btn btn-quiet" href="https://{_esc(u)}" target="_blank" rel="noopener">'
            f'{_esc(L["code"] if u.startswith("github") else L["site"])}: {_esc(u.split("/")[-1])}</a>'
            for u in links
        )
        img = _image(sec.id)
        ask = quote(L["ask_q"].format(t=title))
        prev_s, next_s = secs[i - 1] if i else None, secs[i + 1] if i + 1 < len(secs) else None
        pager = '<nav class="pager" aria-label="' + _esc(L["h1"]) + '">'
        if prev_s:
            pager += f'<a class="prev" href="#{_esc(prev_s.id)}"><small>{_esc(L["prev"])}</small>{_esc(titles[i - 1])}</a>'
        if next_s:
            pager += f'<a class="next" href="#{_esc(next_s.id)}"><small>{_esc(L["next"])}</small>{_esc(titles[i + 1])}</a>'
        pager += "</nav>"
        blocks.append(
            f"""
  <article class="project" id="{_esc(sec.id)}" aria-labelledby="h-{_esc(sec.id)}">
    <header class="project-head">
      <div>
        <p class="count">{i + 1} {_esc(L["of"])} {len(secs)}</p>
        <h2 id="h-{_esc(sec.id)}">{_esc(title)}</h2>
        <p class="lead">{_inline(lead)}</p>
        <p class="actions">
          <a class="btn" href="/?lang={lang}&amp;q={ask}">{_esc(L["ask"])}</a>
          {link_html}
        </p>
      </div>
      {f'<figure><img src="{img}" width="1200" height="675" alt="" /></figure>' if img else ""}
    </header>
    <div class="parts">{"".join(_part_html(*p) for p in parts)}</div>
    {pager}
  </article>"""
        )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{_esc(L["title"])}</title>
<meta name="theme-color" content="#0e1829" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/static/projects.css?v=2" />
</head>
<body>
<header class="bar" id="bar">
  <a class="bar-name" href="/?lang={lang}">Leandro F. Juárez</a>
  <div class="bar-right">
    <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="menu">
      <span class="menu-label">{_esc(L["menu"])}:</span> <span id="menu-current">{_esc(titles[0])}</span>
    </button>
    <a class="lang-link" href="/projects?lang={other}" title="{_esc(L["other_name"])}">{_esc(L["other"])}</a>
  </div>
  <nav class="menu" id="menu" aria-label="{_esc(L["h1"])}">
    <ol>{menu}</ol>
    <a class="menu-back" href="/?lang={lang}">{_esc(L["back"])}</a>
  </nav>
</header>
<main>
  <h1 class="visually-hidden">{_esc(L["h1"])}</h1>
  {"".join(blocks)}
</main>
<script>
(() => {{
  const bar = document.getElementById("bar");
  const toggle = document.getElementById("menu-toggle");
  const current = document.getElementById("menu-current");
  const projects = [...document.querySelectorAll(".project")];
  const links = [...document.querySelectorAll(".menu a[data-id]")];
  document.documentElement.classList.add("paged");
  const setOpen = (open) => {{ bar.classList.toggle("open", open); toggle.setAttribute("aria-expanded", String(open)); }};
  toggle.addEventListener("click", () => setOpen(!bar.classList.contains("open")));
  document.addEventListener("keydown", (e) => {{ if (e.key === "Escape") setOpen(false); }});
  document.addEventListener("click", (e) => {{ if (!bar.contains(e.target)) setOpen(false); }});
  const show = (id, scroll) => {{
    const target = projects.find((p) => p.id === id) || (id && projects.find((p) => p.id.startsWith(id))) || projects[0];
    projects.forEach((p) => p.classList.toggle("active", p === target));
    links.forEach((a) => a.toggleAttribute("aria-current", a.dataset.id === target.id));
    current.textContent = target.querySelector("h2").textContent;
    setOpen(false);
    if (scroll) window.scrollTo({{ top: 0 }});
  }};
  window.addEventListener("hashchange", () => show(location.hash.slice(1), true));
  show(location.hash.slice(1), false);
}})();
</script>
</body>
</html>
"""
