# Alltagsanker Website

Statische Website für Alltagsanker – Alltagsbetreuung für Senioren in Bottrop, Gladbeck, Essen und Gelsenkirchen.

## Struktur

- `index.html` – Startseite
- `ueber-uns.html` – Über uns
- `leistungen.html` – Leistungen
- `kontakt.html` – Kontakt (inkl. Kontaktformular)
- `danke.html` – Bestätigungsseite nach Formularversand
- `impressum.html` – Impressum (**Platzhalter müssen ausgefüllt werden**)
- `datenschutz.html` – Datenschutzerklärung (**Platzhalter müssen ausgefüllt werden**)
- `style.css` – Gemeinsames Stylesheet
- `script.js` – Mobiles Menü, Einblend-Effekte, Jahreszahl im Footer
- `images/` – Logo und Illustrationen (SVG)
- `vercel.json` – Vercel-Konfiguration für sauberes Static Hosting

## Design

Modernes, ruhiges Layout mit großer Schrift und hohem Kontrast – bewusst gut
lesbar für ältere Besucher:innen. Es werden **keine externen Schriftarten oder
Dienste** geladen (systemeigene Schriften), das ist schnell und DSGVO-freundlich.

Weitere Details: mobiles Menü, sanfte Einblendungen beim Scrollen (nur mit
aktivem JavaScript), Rücksicht auf `prefers-reduced-motion`, Sprungmarke zum
Inhalt und sichtbare Fokus-Rahmen für die Tastaturbedienung.

## ⚠️ Vor dem Livegang erledigen

`impressum.html` und `datenschutz.html` enthalten **orange markierte Platzhalter**
(vollständiger Name, Anschrift, Telefonnummer, ggf. USt-IdNr. und Aktenzeichen der
Anerkennung nach § 45a SGB XI). Diese müssen durch die echten Angaben ersetzt
werden – ein unvollständiges Impressum ist abmahnfähig. Die Texte sind Vorlagen
und ersetzen keine Rechtsberatung.

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
git commit -m "Initial commit: Alltagsanker Website"
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
