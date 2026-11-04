#!/usr/bin/env bash
# Renders the project diagrams (deploy/project-docs/*.html) to static/img/gallery/diagram-<name>-<lang>.jpg.
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
OUT=../../src/profile_agent/static/img/gallery
TMP=$(mktemp -d)
for d in ai mcp site; do
  for l in es en; do
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1600,900 \
      --virtual-time-budget=5000 --screenshot="$TMP/$d-$l.png" "file://$PWD/$d.html?lang=$l" 2>/dev/null
    sips -s format jpeg -s formatOptions 85 "$TMP/$d-$l.png" --out "$OUT/diagram-$d-$l.jpg" >/dev/null
  done
done
rm -rf "$TMP"
echo "diagrams in $OUT"
