"""The CV page: one HTML document per language, rendered from the same knowledge base the chat
uses, so it never drifts from the answers. Print styles make it the PDF too."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

from .kb import KnowledgeBase

SITE = "leandrojuarez.info"
EMAIL = "l.federico.juarez@gmail.com"
LINKEDIN = "linkedin.com/in/leandrofjuarez"
GITHUB = "github.com/lfjuarez"
# Public links a project section may carry; anything else in the text is left as prose.
PROJECT_LINK = re.compile(r"github\.com/lfjuarez/[\w.-]*\w|presupuestarapp\.com")

LABELS = {
    "es": {
        "title": "CV · Leandro F. Juárez",
        "role": "Ingeniero de ciberseguridad y arquitecto de SIEM",
        "sub": "Ingeniería de detección · IA aplicada a operaciones de seguridad · Elastic y Splunk · Consultoría y formación",
        "location": "Buenos Aires, Argentina · remoto",
        "summary": "Perfil",
        "experience": "Experiencia profesional",
        "education": "Formación",
        "skills": "Competencias",
        "certs": "Certificaciones",
        "projects": "Proyectos",
        "languages": "Idiomas",
        "own_product": "Producto propio · SaaS en beta",
        "more": "Detalles",
        "download": "Descargar PDF",
        "print": "Imprimir",
        "share": "Compartir enlace",
        "copied": "Enlace copiado",
        "back": "Volver al sitio",
        "other": "English version",
        "note": "Generado desde los mismos documentos que responde el asistente de leandrojuarez.info.",
        "photo_alt": "Leandro F. Juárez",
    },
    "en": {
        "title": "CV · Leandro F. Juárez",
        "role": "Cybersecurity engineer and SIEM architect",
        "sub": "Detection engineering · AI for security operations · Elastic and Splunk · Consulting and training",
        "location": "Buenos Aires, Argentina · remote",
        "summary": "Profile",
        "experience": "Professional experience",
        "education": "Education",
        "skills": "Skills",
        "certs": "Certifications",
        "projects": "Projects",
        "languages": "Languages",
        "own_product": "Own product · SaaS in beta",
        "more": "Details",
        "download": "Download PDF",
        "print": "Print",
        "share": "Share link",
        "copied": "Link copied",
        "back": "Back to the site",
        "other": "Versión en español",
        "note": "Generated from the same documents the assistant at leandrojuarez.info answers from.",
        "photo_alt": "Leandro F. Juárez",
    },
}

_HEADING = re.compile(r"^(?P<role>[^,(]+), (?P<org>.+?) \((?P<dates>[^)]*)\)$")
_BULLETS_CURRENT = 4
_BULLETS_PAST = 2
_SKILL_CHARS = 150


@dataclass(frozen=True)
class Role:
    role: str
    org: str
    dates: str
    bullets: tuple[str, ...]
    intro: str


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


_SENTENCE_END = re.compile(r"(?<!\bRes)(?<!\bSr)(?<!\bDr)\.\s+(?=[A-ZÁÉÍÓÚÑ¿¡\"“(])")


def _first_sentence(text: str) -> str:
    """Up to the first full stop that really ends a sentence ("Res. 493/2018" does not)."""
    text = text.strip()
    m = _SENTENCE_END.search(text)
    return text[: m.start() + 1] if m else text


def _sentences(text: str, n: int) -> str:
    # the split consumes the full stop, so it is put back between the sentences kept
    parts = [s.strip().rstrip(".") for s in _SENTENCE_END.split(text.strip())[:n]]
    return ". ".join(p for p in parts if p) + "."


def _clip(text: str, limit: int) -> str:
    """Keep the leading items of a comma list so it fits one or two lines on paper."""
    if len(text) <= limit:
        return text
    cut = text.rfind(",", 0, limit)
    return (text[:cut] if cut > 40 else text[:limit].rstrip()) + "."


def _split_body(text: str) -> tuple[str, list[str]]:
    """Return (intro paragraph, bullet lines) of a section body."""
    intro: list[str] = []
    bullets: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("- "):
            bullets.append(s[2:].strip())
        elif not bullets:
            intro.append(s)
    return " ".join(intro), bullets


def _roles(kb: KnowledgeBase, lang: str) -> list[Role]:
    out: list[Role] = []
    for i, sec in enumerate(kb.get("experience").sections):
        intro, bullets = _split_body(sec.text)
        m = _HEADING.match(sec.title)
        if sec.title.lower().startswith(("producto propio", "own product")):
            continue  # PresupuestAR is listed once, under projects, with its site
        if m:
            role, org, dates = m.group("role"), m.group("org"), m.group("dates")
        else:
            role, org, dates = sec.title, "", ""
        cap = _BULLETS_CURRENT if i < 2 else _BULLETS_PAST
        if not bullets and intro:
            # a prose section: keep it short on paper
            intro = _sentences(intro, 2)
        out.append(Role(role, org, dates, tuple(bullets[:cap]), intro if not bullets else ""))
    return out


def _education(kb: KnowledgeBase, lang: str) -> list[str]:
    sec_id = "formacion" if lang == "es" else "education"
    sec = next(s for s in kb.get("profile").sections if s.id == sec_id)
    _, bullets = _split_body(sec.text)
    # one line per degree: up to the first sentence, and before any colon that opens a syllabus
    return [_first_sentence(b).split(":")[0].rstrip(".") + "." for b in bullets]


def _certs(kb: KnowledgeBase) -> list[str]:
    sec = kb.get("certifications").sections[0]
    items = []
    for line in sec.text.splitlines():
        m = re.match(r"^\d+\.\s+(.*)$", line.strip())
        # Azure Fundamentals is too basic to show next to the Splunk certifications
        if m and "Azure Fundamentals" not in m.group(1):
            items.append(_first_sentence(m.group(1)))
    return items


def _languages(kb: KnowledgeBase, lang: str) -> str:
    sec_id = "idiomas-y-ubicacion" if lang == "es" else "languages-and-location"
    sec = next(s for s in kb.get("profile").sections if s.id == sec_id)
    sentences = re.split(r"(?<=\.)\s+", sec.text.strip())
    return " ".join(sentences[:2])


def _projects(kb: KnowledgeBase) -> list[tuple[str, str, str, str]]:
    """(title, first sentence, public link or "", section id) for every project."""
    out = []
    for sec in kb.get("projects").sections:
        if sec.title.lower().startswith(("este sitio", "this site")):
            continue  # the header already links the site; keeps the CV on two pages
        first = _first_sentence(sec.text)
        link = PROJECT_LINK.search(sec.text)
        title = re.sub(r"\s*\([^)]*\)\s*$", "", sec.title)
        out.append((title, first, link.group(0) if link else "", sec.id))
    return out


def render_cv(kb: KnowledgeBase, lang: str, photo: bool) -> str:
    lang = lang if lang in LABELS else "es"
    L = LABELS[lang]
    other = "en" if lang == "es" else "es"
    summary = _sentences(kb.get("profile").sections[0].text.strip().split("\n")[0], 2)
    roles = _roles(kb, lang)
    skills = [(s.title, _clip(s.text.strip(), _SKILL_CHARS)) for s in kb.get("skills").sections]
    pdf = f"/cv/Leandro_Juarez_CV_{lang.upper()}.pdf"

    def role_html(r: Role) -> str:
        head = f'<h3><span class="role">{_esc(r.role)}</span>'
        if r.org:
            head += f' <span class="org">· {_esc(r.org)}</span>'
        head += "</h3>"
        body = ""
        if r.intro:
            body += f"<p>{_esc(r.intro)}</p>"
        if r.bullets:
            body += "<ul>" + "".join(f"<li>{_esc(b)}</li>" for b in r.bullets) + "</ul>"
        return f'<li><p class="when">{_esc(r.dates)}</p><div>{head}{body}</div></li>'

    photo_html = (
        f'<img class="photo" src="/static/img/lean.jpg" width="104" height="104" alt="{_esc(L["photo_alt"])}" />'
        if photo
        else ""
    )
    skills_html = "".join(f"<div><dt>{_esc(t)}</dt><dd>{_esc(x)}</dd></div>" for t, x in skills)
    def project_html(t: str, s: str, u: str, sid: str) -> str:
        more = f"https://{SITE}/projects?lang={lang}#{sid}"
        links = f'<a href="{_esc(more)}">{_esc(L["more"])}</a>'
        if u:
            links += f' · <a href="https://{_esc(u)}">{_esc(u)}</a>'
        return f'<li><b>{_esc(t)}.</b> {_esc(s)} <span class="links">{links}</span></li>'

    projects_html = "".join(project_html(*p) for p in _projects(kb))
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{_esc(L["title"])}</title>
<meta name="robots" content="noindex" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/static/cv.css?v=6" />
</head>
<body>
<nav class="tools" aria-label="CV">
  <a class="tool tool-main" href="{pdf}" download>{_esc(L["download"])}</a>
  <button type="button" class="tool" id="print">{_esc(L["print"])}</button>
  <button type="button" class="tool" id="share" data-copied="{_esc(L["copied"])}">{_esc(L["share"])}</button>
  <a class="tool tool-quiet" href="/cv?lang={other}">{_esc(L["other"])}</a>
  <a class="tool tool-quiet" href="/?lang={lang}">{_esc(L["back"])}</a>
</nav>
<main class="paper">
  <header class="head">
    {photo_html}
    <div class="who">
      <h1>Leandro F. Juárez</h1>
      <p class="role-line">{_esc(L["role"])}</p>
      <p class="sub">{_esc(L["sub"])}</p>
    </div>
    <address class="contact">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="https://{LINKEDIN}">{LINKEDIN}</a>
      <a href="https://{GITHUB}">{GITHUB}</a>
      <a href="https://{SITE}">{SITE}</a>
      <span>{_esc(L["location"])}</span>
    </address>
  </header>

  <section>
    <h2>{_esc(L["summary"])}</h2>
    <p class="summary">{_esc(summary)}</p>
  </section>

  <section>
    <h2>{_esc(L["experience"])}</h2>
    <ol class="roles">{"".join(role_html(r) for r in roles)}</ol>
  </section>

  <section class="two">
    <div>
      <h2>{_esc(L["education"])}</h2>
      <ul class="plain">{"".join(f"<li>{_esc(e)}</li>" for e in _education(kb, lang))}</ul>
      <h2>{_esc(L["languages"])}</h2>
      <p>{_esc(_languages(kb, lang))}</p>
    </div>
    <div>
      <h2>{_esc(L["certs"])}</h2>
      <ol class="plain">{"".join(f"<li>{_esc(c)}</li>" for c in _certs(kb))}</ol>
    </div>
  </section>

  <section>
    <h2>{_esc(L["skills"])}</h2>
    <dl class="skills">{skills_html}</dl>
  </section>

  <section>
    <h2>{_esc(L["projects"])}</h2>
    <ul class="plain projects">{projects_html}</ul>
  </section>

  <footer class="note">{_esc(L["note"])}</footer>
</main>
<script>
(() => {{
  // Phones paginate web pages poorly when printing; they print the ready-made PDF instead.
  const phone = matchMedia("(max-width: 820px), (pointer: coarse)").matches;
  document.getElementById("print").addEventListener("click", () => {{
    if (phone) location.href = "{pdf}?view=1"; else window.print();
  }});
  const share = document.getElementById("share");
  share.addEventListener("click", async () => {{
    const url = location.origin + "/cv?lang={lang}";
    try {{
      if (navigator.share) {{ await navigator.share({{ title: document.title, url }}); return; }}
      await navigator.clipboard.writeText(url);
      const label = share.textContent; share.textContent = share.dataset.copied;
      setTimeout(() => {{ share.textContent = label; }}, 1600);
    }} catch (_) {{}}
  }});
}})();
</script>
</body>
</html>
"""
