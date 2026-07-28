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
- `robots.txt` – Hinweise für Suchmaschinen
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

Für Suchmaschinen und geteilte Links: strukturierte Daten (`LocalBusiness`
mit Anschrift und Einsatzgebiet) auf der Startseite, Open-Graph-Angaben für
Vorschauen in Messengern sowie feste Bildmaße, damit beim Laden nichts
verspringt.

## ⚠️ Vor dem Livegang erledigen

`impressum.html` und `datenschutz.html` enthalten noch **orange markierte
Platzhalter**. Die Anschrift (Batenbrockstraße 66, 46238 Bottrop) ist bereits
eingetragen; es fehlen noch:

- vollständiger Name der Inhaberin / des Inhabers
- Telefonnummer
- USt-IdNr. – oder Hinweis auf die Kleinunternehmerregelung
- Behörde und Aktenzeichen der Anerkennung nach § 45a SGB XI

Ein unvollständiges Impressum ist abmahnfähig. Die Texte sind Vorlagen und
ersetzen keine Rechtsberatung.

Sobald die endgültige Domain feststeht, lohnt es sich außerdem, sie in den
`og:image`-Angaben der Seiten als vollständige Adresse zu hinterlegen – dann
zeigen WhatsApp und Facebook beim Teilen auch das Logo an. Eine `sitemap.xml`
lässt sich dann ebenfalls ergänzen.

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
