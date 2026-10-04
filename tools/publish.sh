#!/bin/bash
# Regenera live/ y sube la foto del día. Lo lanza el temporizador diario.
cd "$(dirname "$0")/.." || exit 1
python3 tools/update_live.py || exit 1
git add live
git diff --cached --quiet && exit 0
git commit -q -m "Paper trading: foto del $(date -u +%Y-%m-%d)"
git push -q
