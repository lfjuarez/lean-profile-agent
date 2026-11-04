#!/usr/bin/env bash
# Print the CV pages to the PDFs the site serves. Needs the app running locally (default
# http://localhost:8765) and Google Chrome. Run before deploy/cloud-run.sh so the image ships
# fresh PDFs that match the knowledge base.
set -euo pipefail
BASE="${BASE:-http://localhost:8765}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
cd "$(dirname "$0")/.."
for lang in es en; do
  upper="$(printf '%s' "$lang" | tr '[:lower:]' '[:upper:]')"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=6000 \
    --print-to-pdf="$PWD/cv/Leandro_Juarez_CV_$upper.pdf" "$BASE/cv?lang=$lang" >/dev/null 2>&1
  echo "cv/Leandro_Juarez_CV_$upper.pdf"
done
