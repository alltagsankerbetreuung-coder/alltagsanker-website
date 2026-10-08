# Alltagsfels Website

Statische Website für Alltagsfels – Alltagsbetreuung für Senioren in Bottrop, Gladbeck, Essen und Gelsenkirchen.

## Struktur

- `index.html` – Startseite (mit Abschnitt „Unser Einsatzgebiet“)
- `leistungen.html` – Leistungen
- `ueber-uns.html` – Über uns
- `kosten.html` – Kosten und Pflegekasse (Stand der Rechtslage regelmäßig prüfen)
- `fragen.html` – Häufige Fragen (vor allem für Angehörige)
- `kontakt.html` – Kontakt (inkl. Kontaktformular)
- `danke.html` – Bestätigungsseite nach Formularversand
- `impressum.html`, `datenschutz.html` – Pflichtseiten
- `404.html` – Seite für nicht gefundene Adressen
- `style.css` – Gemeinsame Gestaltung (Farben, Schriften, Abstände)
- `script.js` – Handy-Menü, sanftes Einblenden beim Scrollen, Jahreszahl
- `fonts/` – Schriften Fraunces (Überschriften) und Atkinson Hyperlegible (Text), liegen auf der eigenen Website, keine Verbindung zu Google
- `images/` – Logo (`logo.svg`, `logo-hell.svg` für dunklen Hintergrund), `favicon.svg` und Zeichnungen
- `robots.txt` und `vercel.json` – sperren die Seite vorerst für Suchmaschinen (Disallow + Header „noindex“). Zum Start beides entfernen und Sitemap ergänzen.
- `.vercelignore` – Dateien, die nicht auf der Website erscheinen sollen (z. B. `druckvorlagen/`)

## Kontaktformular

Das Formular auf `kontakt.html` nutzt [formsubmit.co](https://formsubmit.co) – ein kostenloser Dienst, der Formulardaten ohne eigenes Backend per E-Mail an `alltagsankerbetreuung@gmail.com` weiterleitet.

**Wichtig:** Beim allerersten Absenden schickt formsubmit.co eine Bestätigungs-E-Mail an `alltagsankerbetreuung@gmail.com`. Diese muss einmalig bestätigt werden, danach funktionieren alle weiteren Einsendungen automatisch.

## Lokal ansehen

Einfach `index.html` im Browser öffnen, oder mit einem lokalen Server:

```bash
python3 -m http.server 8000
```

Danach im Browser: `http://localhost:8000`

## Deployment auf GitHub + Vercel

Siehe die Schritt-für-Schritt-Anleitung im Chat bzw. unten.

### 1. GitHub

```bash
git init
git add .
git commit -m "Initial commit: Alltagsfels Website"
git branch -M main
git remote add origin https://github.com/<dein-username>/alltagsanker-website.git
git push -u origin main
```

### 2. Vercel

1. Auf [vercel.com](https://vercel.com) einloggen (mit GitHub-Konto).
2. "Add New… → Project" wählen.
3. Das Repo `alltagsanker-website` importieren.
4. Framework Preset: **Other** (statisches HTML), keine Build-Konfiguration nötig.
5. "Deploy" klicken – nach ca. 30 Sekunden ist die Seite live.

Jeder weitere `git push` auf `main` löst automatisch ein neues Deployment aus.
