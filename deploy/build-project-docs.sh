#!/usr/bin/env bash
# Print every project's fact sheet (ES and EN) and render the pages of every PDF the projects page
# offers as pictures, so phones can scroll them. Needs the app running locally (default
# http://localhost:8765), Google Chrome and poppler (pdftoppm). Run after deploy/build-cv-pdfs.sh
# and before deploy/cloud-run.sh.
set -euo pipefail
BASE="${BASE:-http://localhost:8765}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
cd "$(dirname "$0")/.."
DOCS=src/profile_agent/static/docs

pages() {  # pages <pdf> <folder>: one JPEG per page, p-1.jpg… (p-01.jpg… past nine pages)
  rm -rf "$2"; mkdir -p "$2"
  pdftoppm -jpeg -jpegopt quality=72 -scale-to 1100 "$1" "$2/p"
}

for lang in es en; do
  mkdir -p "$DOCS/sheets/$lang"
  for key in ia-agentica mitre-coverage-kit splunk-mcp-readonly arquitectura presupuestar este-sitio; do
    pdf="$DOCS/sheets/$lang/$key.pdf"
    "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=6000 \
      --print-to-pdf="$PWD/$pdf" "$BASE/projects/$key/sheet?lang=$lang" >/dev/null 2>&1
    pages "$pdf" "${pdf%.pdf}"
    echo "$pdf"
  done
done
for f in "$DOCS"/*.pdf; do pages "$f" "${f%.pdf}"; done
pages cv/Leandro_Juarez_CV_ES.pdf "$DOCS/cv-es"
pages cv/Leandro_Juarez_CV_EN.pdf "$DOCS/cv-en"
echo "pages rendered under $DOCS"
