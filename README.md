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
mit Anschrift und Einsatzgebiet sowie `FAQPage` mit den häufigen Fragen) auf
der Startseite, Open-Graph-Angaben für Vorschauen in Messengern sowie feste
Bildmaße, damit beim Laden nichts verspringt. Titel und Beschreibungen sind
auf Länge und Suchbegriffe (Ort + Leistung) geprüft.

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

## 🔎 SEO: Sobald die Domain feststeht

Ein paar Dinge lassen sich erst mit der echten, endgültigen Adresse der
Website sinnvoll ergänzen (z. B. `https://www.alltagsanker.de`) – vorher
absichtlich weggelassen, damit keine falsche Platzhalter-Domain unbemerkt
live geht. Sobald die Domain feststeht, folgende Schritte:

**1. `sitemap.xml` im Hauptordner anlegen** (Domain ersetzen):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.DOMAIN.de/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
  <url><loc>https://www.DOMAIN.de/ueber-uns.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.DOMAIN.de/leistungen.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.DOMAIN.de/kontakt.html</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://www.DOMAIN.de/impressum.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>https://www.DOMAIN.de/datenschutz.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
</urlset>
```

**2. In `robots.txt` ergänzen:**

```
Sitemap: https://www.DOMAIN.de/sitemap.xml
```

**3. In jeder Seite `<head>` eine kanonische URL ergänzen** (Beispiel für
`index.html`, auf jeder Seite die eigene Adresse eintragen):

```html
<link rel="canonical" href="https://www.DOMAIN.de/" />
<meta property="og:url" content="https://www.DOMAIN.de/" />
```

**4. Bei Google Search Console anmelden**, die Domain verifizieren und die
Sitemap dort einreichen – das ist der schnellste Weg, damit Google die Seite
findet und indexiert.

Ohne diese vier Schritte funktioniert die Website und wird auch gefunden,
aber Google braucht dafür länger und Suchergebnis-Vorschauen sind seltener
perfekt (z. B. bei doppelt aufrufbaren Adressen mit und ohne `www.`).

## Kontaktformular

Das Formular auf `kontakt.html` nutzt [formsubmit.co](https://formsubmit.co) – ein kostenloser Dienst, der Formulardaten ohne eigenes Backend per E-Mail an `Alltagsankerbetreuung@gmail.com` weiterleitet.

**Wichtig:** Beim allerersten Absenden schickt formsubmit.co eine Bestätigungs-E-Mail an `Alltagsankerbetreuung@gmail.com`. Diese muss einmalig bestätigt werden, danach funktionieren alle weiteren Einsendungen automatisch.

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
