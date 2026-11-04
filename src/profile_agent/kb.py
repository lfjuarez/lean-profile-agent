"""Knowledge base: curated markdown documents, one folder per language, split into sections.

Each file has YAML front matter (``id``, ``title``, ``questions``) followed by ``##`` sections.
A section is the unit of retrieval and of citation: every answer points at ``doc_id#section_id``.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml

LANGS = ("en", "es")
_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
_SECTION = re.compile(r"^## +(.+?)\s*$", re.M)


def default_kb_dir() -> Path:
    """``PROFILE_KB_DIR`` if set, else ``<repo>/knowledge`` relative to this package."""
    env = os.environ.get("PROFILE_KB_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "knowledge"


def slugify(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    return slug or "section"


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    text: str


@dataclass(frozen=True)
class Doc:
    id: str
    lang: str
    title: str
    questions: tuple[str, ...]
    sections: tuple[Section, ...]
    path: Path

    @property
    def is_case_study(self) -> bool:
        return self.id.startswith("case-")

    @property
    def text(self) -> str:
        return "\n\n".join(f"## {s.title}\n\n{s.text}" for s in self.sections)


@dataclass(frozen=True)
class Chunk:
    """One section with everything needed to cite it."""

    id: str
    lang: str
    doc_id: str
    doc_title: str
    section_id: str
    section_title: str
    text: str
    questions: tuple[str, ...] = field(default=(), compare=False)


def parse_doc(path: Path, lang: str) -> Doc:
    raw = path.read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(raw)
    if not match:
        raise ValueError(f"{path}: missing front matter")
    meta = yaml.safe_load(match.group(1)) or {}
    body = raw[match.end() :]
    for key in ("id", "title"):
        if not meta.get(key):
            raise ValueError(f"{path}: front matter needs '{key}'")
    questions = tuple(str(q).strip() for q in meta.get("questions") or [])

    sections: list[Section] = []
    seen: set[str] = set()
    heads = list(_SECTION.finditer(body))
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        title = head.group(1).strip()
        sid = slugify(title)
        if sid in seen:
            raise ValueError(f"{path}: duplicate section '{title}'")
        seen.add(sid)
        text = body[head.end() : end].strip()
        sections.append(Section(id=sid, title=title, text=text))
    if not sections:
        raise ValueError(f"{path}: no '## ' sections")
    return Doc(
        id=str(meta["id"]),
        lang=lang,
        title=str(meta["title"]),
        questions=questions,
        sections=tuple(sections),
        path=path,
    )


@dataclass(frozen=True)
class KnowledgeBase:
    lang: str
    docs: tuple[Doc, ...]

    def get(self, doc_id: str) -> Doc:
        for doc in self.docs:
            if doc.id == doc_id:
                return doc
        raise KeyError(doc_id)

    @property
    def chunks(self) -> tuple[Chunk, ...]:
        out: list[Chunk] = []
        for doc in self.docs:
            for sec in doc.sections:
                out.append(
                    Chunk(
                        id=f"{doc.id}#{sec.id}",
                        lang=self.lang,
                        doc_id=doc.id,
                        doc_title=doc.title,
                        section_id=sec.id,
                        section_title=sec.title,
                        text=sec.text,
                        questions=doc.questions,
                    )
                )
        return tuple(out)

    def chunk(self, chunk_id: str) -> Chunk:
        for c in self.chunks:
            if c.id == chunk_id:
                return c
        raise KeyError(chunk_id)

    def case_studies(self) -> tuple[Doc, ...]:
        return tuple(d for d in self.docs if d.is_case_study)


# Reading order: general documents first, then the case studies. Unknown files go last.
_ORDER = [
    "profile",
    "certifications",
    "experience",
    "skills",
    "ways-of-working",
    "services",
    "rates",
    "contact",
    "case-detection-coverage",
    "case-multisite-platform",
    "case-soar-triage",
]


def load_kb(lang: str, base_dir: Path | None = None) -> KnowledgeBase:
    if lang not in LANGS:
        raise ValueError(f"unsupported language {lang!r}; expected one of {LANGS}")
    root = (base_dir or default_kb_dir()) / lang
    if not root.is_dir():
        raise FileNotFoundError(f"knowledge folder not found: {root}")
    docs = [parse_doc(p, lang) for p in sorted(root.rglob("*.md"))]
    ids = [d.id for d in docs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate document ids in {root}: {sorted(dupes)}")
    rank = {doc_id: i for i, doc_id in enumerate(_ORDER)}
    docs.sort(key=lambda d: (rank.get(d.id, len(_ORDER)), d.id))
    return KnowledgeBase(lang=lang, docs=tuple(docs))
