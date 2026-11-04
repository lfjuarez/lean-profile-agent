"""The projects page: one project at a time, picked from a menu, rendered from the same documents
the chat answers from. Each text is cut into short labelled parts so it reads in a minute."""

from __future__ import annotations

import html
import re
from pathlib import Path
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
        "gallery": "Capturas",
        "docs": "Documentos",
        "links": "Enlaces",
        "view_pdf": "Ver PDF",
        "download": "Descargar",
        "pages": "páginas",
        "page": "página",
        "close": "Cerrar",
        "open_tab": "Abrir en otra pestaña",
        "video": "Video",
        "zoom": "Ampliar imagen",
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
        "gallery": "Screenshots",
        "docs": "Documents",
        "links": "Links",
        "view_pdf": "View PDF",
        "download": "Download",
        "pages": "pages",
        "page": "page",
        "close": "Close",
        "open_tab": "Open in a new tab",
        "video": "Video",
        "zoom": "Enlarge image",
    },
}

STATIC = Path(__file__).parent / "static"

# Section id prefix (either language) → one key for both languages.
KEYS = (
    ("ia-agentica", "ia-agentica"), ("agentic-ai", "ia-agentica"),
    ("mitre-coverage-kit", "mitre-coverage-kit"),
    ("splunk-mcp-readonly", "splunk-mcp-readonly"),
    ("arquitectura", "arquitectura"), ("multi-site", "arquitectura"),
    ("presupuestar", "presupuestar"),
    ("este-sitio", "este-sitio"), ("this-site", "este-sitio"),
)

# Key → extra pictures, documents and links. Captions are (es, en); "{lang}" picks the language.
# Documents are (href, (es, en), pages, page-image base or None for "<href without .pdf>/p-").
G = "/static/img/gallery/"
D = "/static/docs/"
MEDIA: dict[str, dict] = {
    "ia-agentica": {
        "gallery": [
            (G + "diagram-ai-{lang}.jpg", ("Cómo un agente migra una regla, paso a paso", "How an agent migrates a rule, step by step")),
            (G + "elastic-rule-mitre.jpg", ("Una regla de Elastic con su mapeo a MITRE ATT&CK, en mi laboratorio", "An Elastic rule with its MITRE ATT&CK mapping, in my lab")),
        ],
    },
    "mitre-coverage-kit": {
        "gallery": [
            (G + "coverage-overview.jpg", ("Resumen: cifras clave y su variación", "Overview: key figures and their change")),
            (G + "coverage-matrix.jpg", ("Matriz ATT&CK con el semáforo de cobertura", "ATT&CK matrix with the coverage levels")),
            (G + "coverage-technique.jpg", ("Panel por técnica: reglas, datos faltantes y tests", "Technique panel: rules, missing data and tests")),
            (G + "coverage-catalog.jpg", ("Catálogo: reglas públicas que cubrirían cada hueco", "Catalog: public rules that would close each gap")),
            (G + "coverage-heatmap.jpg", ("Mapa de calor unificado de varios SIEM", "Unified heat map across several SIEMs")),
            (G + "coverage-terminal.jpg", ("Importación desde Splunk, Elastic y Wazuh en el laboratorio", "Import from Splunk, Elastic and Wazuh in the lab")),
        ],
        "docs": [
            (D + "mitre-coverage-kit-informe-ejemplo.pdf", ("Informe de cobertura de ejemplo", "Sample coverage report"), 25, None),
        ],
    },
    "splunk-mcp-readonly": {
        "gallery": [
            (G + "diagram-mcp-{lang}.jpg", ("Solo lectura dos veces: en el servidor y en el rol de Splunk", "Read-only twice: in the server and in the Splunk role")),
        ],
    },
    "presupuestar": {
        "gallery": [
            (G + "presupuestar-landing.jpg", ("El sitio en beta", "The beta site")),
            (G + "presupuestar-showreel.jpg", ("Fotograma del video de presentación", "Frame of the presentation video")),
        ],
        "docs": [
            (D + "presupuestar-ejemplo-moderno.pdf", ("Presupuesto de ejemplo, diseño Moderno", "Sample quote, Modern design"), 1, None),
            (D + "presupuestar-ejemplo-membrete.pdf", ("Presupuesto de ejemplo, diseño Membrete", "Sample quote, Letterhead design"), 1, None),
        ],
        "links": [("video", "https://www.youtube.com/watch?v=HcGEmoTAqLw", "youtube.com/watch?v=HcGEmoTAqLw")],
    },
    "este-sitio": {
        "gallery": [
            (G + "diagram-site-{lang}.jpg", ("Cómo responde el asistente", "How the assistant answers")),
            (G + "site-cv.jpg", ("El CV generado desde los mismos documentos", "The CV built from the same documents")),
            (G + "site-projects.jpg", ("Esta página de proyectos", "This projects page")),
        ],
        "docs": [
            ("/cv/Leandro_Juarez_CV_ES.pdf", ("Mi CV en español, generado por el sitio", "My CV in Spanish, generated by the site"), 2, D + "cv-es/p-"),
            ("/cv/Leandro_Juarez_CV_EN.pdf", ("Mi CV en inglés, generado por el sitio", "My CV in English, generated by the site"), 2, D + "cv-en/p-"),
        ],
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


def _key(section_id: str) -> str:
    for prefix, key in KEYS:
        if section_id.startswith(prefix):
            return key
    return section_id


def _media(section_id: str) -> dict:
    return MEDIA.get(_key(section_id), {})


def _sheet(section_id: str, lang: str) -> tuple | None:
    """The project's fact sheet, when deploy/build-project-docs.sh has printed it."""
    key = _key(section_id)
    folder = STATIC / "docs" / "sheets" / lang / key
    pages = len(list(folder.glob("p-*.jpg"))) if folder.is_dir() else 0
    if not pages:
        return None
    return (f"/static/docs/sheets/{lang}/{key}.pdf", ("Ficha del proyecto", "Project sheet"), pages, None)


def _links_html(urls: list[str], extra: list[tuple[str, str, str]], L: dict) -> str:
    rows = []
    for u in urls:
        kind = L["code"] if u.startswith("github") else L["site"]
        rows.append((kind, f"https://{u}", u))
    rows += [(L[k], href, text) for k, href, text in extra]
    if not rows:
        return ""
    items = "".join(
        f'<li><span>{_esc(k)}</span><a href="{_esc(h)}" target="_blank" rel="noopener">{_esc(x)}<i aria-hidden="true">↗</i></a></li>'
        for k, h, x in rows
    )
    return f'<ul class="links" aria-label="{_esc(L["links"])}">{items}</ul>'


def _gallery_html(items: list, lang: str, L: dict) -> str:
    if not items:
        return ""
    i = 0 if lang == "es" else 1
    items = [(src.format(lang=lang), cap) for src, cap in items]
    figs = "".join(
        f'<li><button type="button" class="shot" data-src="{src}" data-caption="{_esc(cap[i])}" aria-label="{_esc(L["zoom"])}: {_esc(cap[i])}">'
        f'<img src="{src}" loading="lazy" alt="{_esc(cap[i])}" /></button><span>{_esc(cap[i])}</span></li>'
        for src, cap in items
    )
    return f'<section class="extra"><h3>{_esc(L["gallery"])}</h3><ul class="gallery">{figs}</ul></section>'


def _docs_html(items: list, lang: str, L: dict) -> str:
    if not items:
        return ""
    i = 0 if lang == "es" else 1
    cards = []
    for href, title, pages, base in items:
        base = base or href.removesuffix(".pdf") + "/p-"
        thumb = base + ("1" if pages < 10 else "01") + ".jpg"
        count = f'{pages} {L["page"] if pages == 1 else L["pages"]}'
        cards.append(
            f'<li class="doc"><a class="doc-thumb pdf" href="{href}" target="_blank" rel="noopener" data-title="{_esc(title[i])}" data-pages="{pages}" data-base="{base}">'
            f'<img src="{thumb}" loading="lazy" alt="" /></a><div><p class="doc-title">{_esc(title[i])}</p>'
            f'<p class="doc-meta">PDF · {count}</p><p class="doc-actions">'
            f'<a class="btn btn-small pdf" href="{href}" target="_blank" rel="noopener" data-title="{_esc(title[i])}" data-pages="{pages}" data-base="{base}">{_esc(L["view_pdf"])}</a>'
            f'<a class="btn btn-small btn-quiet" href="{href}" download>{_esc(L["download"])}</a></p></div></li>'
        )
    return f'<section class="extra"><h3>{_esc(L["docs"])}</h3><ul class="docs">{"".join(cards)}</ul></section>'


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
        media = _media(sec.id)
        links = list(dict.fromkeys(PROJECT_LINK.findall(sec.text)))
        link_html = _links_html(links, media.get("links", []), L)
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
        {link_html}
        <p class="actions">
          <a class="btn" href="/?lang={lang}&amp;q={ask}">{_esc(L["ask"])}</a>
        </p>
      </div>
      {f'<figure><button type="button" class="shot" data-src="{img}" data-caption="{_esc(title)}" aria-label="{_esc(L["zoom"])}"><img src="{img}" width="1200" height="675" alt="" /></button></figure>' if img else ""}
    </header>
    {_gallery_html(media.get("gallery", []), lang, L)}
    {_docs_html([d for d in [_sheet(sec.id, lang)] if d] + media.get("docs", []), lang, L)}
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
<link rel="stylesheet" href="/static/projects.css?v=7" />
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
<dialog class="viewer" id="viewer" aria-labelledby="viewer-caption">
  <div class="viewer-bar">
    <button type="button" class="viewer-close" id="viewer-close" aria-label="{_esc(L["close"])}"><span aria-hidden="true">×</span></button>
    <p class="viewer-caption" id="viewer-caption"></p>
    <a class="viewer-open" id="viewer-open" href="#" download>{_esc(L["download"])}</a>
  </div>
  <div class="viewer-body" id="viewer-body"></div>
</dialog>
<script>
(() => {{
  // Full-screen viewer for pictures and PDFs. The X, Escape and the phone's back button all
  // close it and leave the reader exactly where they were.
  const viewer = document.getElementById("viewer");
  const body = document.getElementById("viewer-body");
  const caption = document.getElementById("viewer-caption");
  const download = document.getElementById("viewer-open");
  let scrollY = 0;
  const shut = () => {{
    if (!viewer.open) return;
    viewer.close(); body.replaceChildren();
    document.documentElement.classList.remove("viewing");
    window.scrollTo(0, scrollY);
  }};
  const close = () => {{ if (history.state && history.state.viewer) history.back(); else shut(); }};
  window.addEventListener("popstate", shut);
  document.getElementById("viewer-close").addEventListener("click", close);
  viewer.addEventListener("cancel", (e) => {{ e.preventDefault(); close(); }});
  const open = (nodes, text, href, kind) => {{
    scrollY = window.scrollY;
    body.replaceChildren(...nodes); body.scrollTop = 0;
    caption.textContent = text; download.href = href;
    download.hidden = kind !== "pdf";
    viewer.dataset.kind = kind;
    document.documentElement.classList.add("viewing");
    viewer.showModal();
    history.pushState({{ viewer: true }}, "");
  }};
  document.querySelectorAll(".shot").forEach((b) => b.addEventListener("click", () => {{
    const img = new Image(); img.src = b.dataset.src; img.alt = b.dataset.caption;
    open([img], b.dataset.caption, b.dataset.src, "image");
  }}));
  // Desktop browsers show the PDF itself; phones get its pages as pictures, which every phone can scroll.
  const wide = window.matchMedia("(min-width: 761px)");
  document.querySelectorAll("a.pdf").forEach((a) => a.addEventListener("click", (e) => {{
    e.preventDefault();
    const href = a.getAttribute("href");
    let nodes;
    if (wide.matches) {{
      const frame = document.createElement("iframe"); frame.src = href; frame.title = a.dataset.title;
      nodes = [frame];
    }} else {{
      const n = Number(a.dataset.pages) || 1, pad = String(n).length;
      const base = a.dataset.base;
      nodes = Array.from({{ length: n }}, (_, i) => {{
        const img = new Image(); img.loading = i < 2 ? "eager" : "lazy";
        img.src = base + String(i + 1).padStart(pad, "0") + ".jpg"; img.alt = `${{a.dataset.title}} · ${{i + 1}}/${{n}}`;
        img.className = "page"; return img;
      }});
    }}
    open(nodes, a.dataset.title, href, "pdf");
  }}));
}})();
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


SHEET_LABELS = {
    "es": {"kicker": "Proyecto", "links": "Enlaces", "more": "Capturas, documentos y preguntas en"},
    "en": {"kicker": "Project", "links": "Links", "more": "Screenshots, documents and questions at"},
}


def render_sheet(kb: KnowledgeBase, lang: str, key: str) -> str | None:
    """One printable A4 page (or two) per project, from the same text as the projects page."""
    lang = lang if lang in LABELS else "es"
    L, S = LABELS[lang], SHEET_LABELS[lang]
    sec = next((s for s in kb.get("projects").sections if _key(s.id) == key), None)
    if sec is None:
        return None
    title = re.sub(r"\s*\([^)]*\)\s*$", "", sec.title)
    lead, parts = _parts(sec.text, L["detail"])
    media = _media(sec.id)
    gallery = [(src.format(lang=lang), cap[0 if lang == "es" else 1]) for src, cap in media.get("gallery", [])]
    hero = next((g for g in gallery if "diagram-" in g[0]), None) or (_image(sec.id), title)
    shots = [g for g in gallery if g is not hero][:4]
    links = [f"https://{u}" for u in dict.fromkeys(PROJECT_LINK.findall(sec.text))]
    links += [h for _, h, _ in media.get("links", [])]
    page = f"https://leandrojuarez.info/projects?lang={lang}#{sec.id}"
    links_html = "".join(f'<li><a href="{_esc(u)}">{_esc(u.removeprefix("https://"))}</a></li>' for u in links)
    shots_html = "".join(
        f'<figure><img src="{_esc(src)}" alt="" /><figcaption>{_esc(cap)}</figcaption></figure>' for src, cap in shots
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8" />
<title>{_esc(title)} · Leandro F. Juárez</title>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/static/sheet.css?v=2" />
</head>
<body>
<header class="band">
  <p class="who">Leandro F. Juárez · {_esc(S["kicker"])}</p>
  <h1>{_esc(title)}</h1>
  <p class="lead">{_inline(lead)}</p>
</header>
<figure class="hero"><img src="{_esc(hero[0])}" alt="" /></figure>
{f'<section class="links"><h2>{_esc(S["links"])}</h2><ul>{links_html}</ul></section>' if links else ""}
<div class="parts">{"".join(_part_html(*p) for p in parts)}</div>
{f'<div class="shots">{shots_html}</div>' if shots else ""}
<footer>{_esc(S["more"])} <a href="{_esc(page)}">{_esc(page.removeprefix("https://"))}</a></footer>
</body>
</html>
"""
