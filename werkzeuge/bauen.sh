#!/bin/sh
# Baut die Website für Cloudflare Pages in den Ordner dist/.
# In dist/ kommt nur, was auf die Website gehört: keine Werkzeuge,
# keine Druckvorlagen, keine Zeichnungs-Quelltexte.
#
# Einstellungen bei Cloudflare Pages:
#   Build command:          sh werkzeuge/bauen.sh
#   Build output directory: dist
#
# Vorher läuft die Prüfung. Findet sie einen Fehler, bricht der Bau ab
# und die alte Fassung der Website bleibt online.
set -eu
cd "$(dirname "$0")/.."

PY=$(command -v python3 || command -v python || true)
if [ -n "$PY" ]; then
  "$PY" werkzeuge/pruefen.py
else
  echo "Achtung: Python fehlt, die Prüfung wurde übersprungen."
fi

rm -rf dist
mkdir dist
cp ./*.html kopf.js script.js style.css robots.txt sitemap.xml site.webmanifest \
   favicon.ico apple-touch-icon.png _headers dist/
cp -R fonts images dist/

echo "Fertig: dist/ mit $(find dist -type f | wc -l | tr -d ' ') Dateien."
