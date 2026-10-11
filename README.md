# Alltagsfels Website

Statische Website für Alltagsfels – Alltagsbetreuung für Senioren in Bottrop und Umgebung (z. B. Gladbeck, Gelsenkirchen, Essen).

## Zum Start im Januar

Diese Punkte kann nur der Inhaber erledigen. Die Website selbst ist fertig.

- [ ] **Domain verbinden:** In Vercel unter *Settings → Domains* `alltagsfels.de` hinzufügen und die angezeigten DNS-Einträge beim Domain-Anbieter eintragen. Erst danach erscheint das Vorschaubild in WhatsApp und E-Mails, denn es liegt unter `https://alltagsfels.de/images/vorschau.png`.
- [ ] **Suchmaschinen-Sperre entfernen (Teil 1):** Den Inhalt von `robots.txt` ersetzen durch:
  ```
  User-agent: *
  Allow: /

  Sitemap: https://alltagsfels.de/sitemap.xml
  ```
- [ ] **Suchmaschinen-Sperre entfernen (Teil 2):** In `vercel.json` den ganzen Block `"headers": [ … ]` mit `X-Robots-Tag` / `noindex, nofollow` löschen. Übrig bleibt:
  ```json
  {
    "cleanUrls": true,
    "trailingSlash": false
  }
  ```
- [ ] **Telefonnummer eintragen**, sobald es sie gibt: in `kontakt.html` (Kasten „Telefon“, Text „Unsere Telefonnummer folgt bald …“ ersetzen), im Fußbereich aller Seiten (Liste „Kontakt“), in `index.html` im Google-Datenblock (`"telephone": "+49 …"`) und im Impressum.
- [ ] **Hinweise auf den Start anpassen:** Die Leiste ganz oben auf allen Seiten („Wir starten im Januar 2027 …“) ändern oder entfernen. Außerdem „Ab Januar 2027 …“ in `index.html` (Ablauf, Schritt 3), `kontakt.html` („So geht es weiter“), `danke.html` (Schritt 3) und `fragen.html` (Frage „Ab wann kann die Betreuung beginnen?“, zweimal: sichtbar und im Google-Datenblock oben).
- [ ] **Kontaktformular testen:** Einmal selbst eine Nachricht senden. Beim ersten Mal kommt von formsubmit.co eine Bestätigungs-E-Mail an `alltagsankerbetreuung@gmail.com`, die einmal bestätigt werden muss.
- [ ] **Impressum und Datenschutz prüfen:** Stimmen alle Angaben (z. B. Handelsregister, Telefon)? Am besten rechtlich prüfen lassen.
- [ ] **Bei Google anmelden:** In der [Google Search Console](https://search.google.com/search-console) die Domain bestätigen und `https://alltagsfels.de/sitemap.xml` einreichen. Empfehlenswert: ein kostenloses Google-Unternehmensprofil für Bottrop anlegen.
- [ ] **Vorschau testen:** Den Link `https://alltagsfels.de` in WhatsApp an sich selbst schicken und prüfen, ob Bild und Text erscheinen.
- [ ] *Freiwillig:* Eine E-Mail-Adresse mit eigener Domain (z. B. `kontakt@alltagsfels.de`) wirkt professioneller als eine Gmail-Adresse. Dann überall austauschen, auch im Formular (`kontakt.html`, `action=…`).

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
- `images/` – Logo (`logo.svg`, `logo-hell.svg` für dunklen Hintergrund), `favicon.svg`, Zeichnungen, `vorschau.png` (Vorschaubild 1200 × 630 für WhatsApp, E-Mail und soziale Netzwerke) und `icon-192.png` / `icon-512.png` (Symbole für den Handy-Startbildschirm)
- `apple-touch-icon.png` und `site.webmanifest` – Symbol und Angaben für den Handy-Startbildschirm
- `sitemap.xml` – Liste aller Seiten für Suchmaschinen (für https://alltagsfels.de, wird erst zum Start bei Google eingereicht)
- `robots.txt` und `vercel.json` – sperren die Seite vorerst für Suchmaschinen (Disallow + Header „noindex“). Zum Start entfernen, siehe Checkliste unten.
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
