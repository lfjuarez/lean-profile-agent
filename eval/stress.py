"""Stress test: many question types about Lean, each with an expected behaviour.

    .venv/bin/python eval/stress.py [backend-spec] > eval/stress-report.md

Expectations (eval/questions.yaml): `answer` must cite sources and mention the `must` terms;
`decline` must say it is not documented and cite nothing; `decline_or_no` may answer "no" with
a citation; `any` only checks `never` terms. Results are grouped by category.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "eval"))

from compare_models import load_env, make_backend  # noqa: E402

from profile_agent.chat import ProfileChat  # noqa: E402
from profile_agent.kb import LANGS, load_kb  # noqa: E402
from profile_agent.retrieval import Index  # noqa: E402

DECLINE_MARKERS = re.compile(
    r"(not (in|contain|mention|include|specif|document)|no (information|details|mention|data)|"
    r"don't have|do not have|cannot (answer|find)|isn't (in|documented)|not documented|"
    r"no (contiene|menciona|incluye|especifica|está|tengo|hay|se menciona|figura|aparece|cuento)|"
    r"no (se )?(encuentra|detalla|indica)|sin información|solo puedo responder|only answer|"
    r"cannot help|can't help|no puedo ayudar|not part of (his|the)|no forma parte|"
    r"out of scope|fuera de|no es parte|no forman? parte|cannot share|can't share|"
    r"is not part of|are not part of|no es posible)",
    re.I,
)
CITE = re.compile(r"\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\]")


def judge(item: dict, text: str, sources: list, error: str | None) -> list[str]:
    problems: list[str] = []
    if error:
        return [f"error {error}"]
    low = text.lower()
    cited = bool(CITE.search(text))
    declined = bool(DECLINE_MARKERS.search(text))
    expect = item["expect"]
    if expect == "answer":
        if declined and not cited:
            problems.append("declined but should answer")
        elif not cited:
            problems.append("no citation")
        for term in item.get("must", []):
            if not any(alt.lower() in low for alt in term.split("|")):
                problems.append(f"missing '{term}'")
    elif expect == "decline":
        if not declined:
            problems.append("answered but should decline")

    elif expect == "decline_or_no":
        for term in item.get("must", []):
            if not any(re.search(rf"\b{re.escape(alt)}\b", low) for alt in term.split("|")):
                problems.append(f"missing '{term}'")
    for bad in item.get("never", []):
        if bad.lower() in low:
            problems.append(f"contains forbidden '{bad}'")
    return problems


def main() -> None:
    load_env()
    spec = sys.argv[1] if len(sys.argv) > 1 else "gemini:gemini-flash-lite-latest"
    qfile = os.environ.get("QUESTIONS", "questions.yaml")
    items = yaml.safe_load((ROOT / "eval" / qfile).read_text())
    indexes = {lang: Index(load_kb(lang)) for lang in LANGS}
    chat = ProfileChat(indexes, backend=make_backend(spec))
    pause = float(os.environ.get("PAUSE", "2"))
    rows = []
    for item in items:
        text, sources, error = "", [], None
        for ev in chat.stream([{"role": "user", "content": item["q"]}], lang=item["lang"]):
            if ev.type == "text":
                text += ev.data
            elif ev.type == "sources":
                sources = ev.data
            elif ev.type == "error":
                error = ev.data["code"]
        rows.append((item, text.strip(), sources, error, judge(item, text, sources, error)))
        time.sleep(pause)

    ok = sum(not r[4] for r in rows)
    print(f"# Stress test · {spec}\n\n**{ok}/{len(rows)} passed**\n")
    cats: dict[str, list] = {}
    for r in rows:
        cats.setdefault(r[0]["cat"], []).append(r)
    print("| Category | Passed |\n|---|---|")
    for cat, rs in cats.items():
        print(f"| {cat} | {sum(not r[4] for r in rs)}/{len(rs)} |")
    for cat, rs in cats.items():
        print(f"\n## {cat}\n")
        for item, text, sources, _error, problems in rs:
            mark = "OK" if not problems else "FAIL: " + "; ".join(problems)
            print(f"### {item['q']} · expect {item['expect']} · {mark}\n")
            print(text or "_(no text)_")
            if sources:
                print(
                    "\nSources: "
                    + "; ".join(f"{s['doc_title']} › {s['section_title']}" for s in sources)
                )
            print()


if __name__ == "__main__":
    main()
