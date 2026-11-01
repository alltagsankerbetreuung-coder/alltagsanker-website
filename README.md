# Alltagsfels Website

Statische Website für Alltagsfels: Alltagsbetreuung für Senioren in Bottrop und Umgebung (z. B. Gladbeck, Gelsenkirchen, Essen). Reines HTML, CSS und etwas JavaScript, keine Fremddienste, keine Cookies.

Die Anleitung für den Inhaber (ohne Technik) liegt in den Projektunterlagen: „Anleitung Website live schalten 2026-11-01.md“.

## Regeln für Änderungen

- Nichts in `main` übernehmen ohne ausdrückliches „übernehmen“ von Julian. Jede Änderung als eigener Zweig mit Änderungsvorschlag.
- Vor jedem Änderungsvorschlag: `python3 werkzeuge/pruefen.py` (muss „Alles in Ordnung“ melden).
- Werberegeln (prüft `pruefen.py` zum Teil automatisch): keine Preise oder Kassenbeträge, keine Umsatzsteuer, kein Wort zur Anerkennung (§ 45a), keine Wochentage, Uhrzeiten, Mindestdauern oder Absageregeln, keine Rückmeldezeiten, keine Vertretungsregel, Erfahrung nur als „viele Jahre“, keine Fotos (Zeichnungen ja), keine erfundenen Bewertungen, Zahlen oder Siegel, kein Fahrdienst, keine Zusagen zum Grundkurs, keine Stadtseiten, „Januar 2027“ nur für Kunden (Jobs-Seite ohne Startdatum), Pflegegrad 2+ und Selbstzahler, „Ihre Angehörigen“.
- Nie eine Bankverbindung (IBAN) in dieses öffentliche Repo.
- Nichts von fremden Servern laden (Schriften, Bilder, Skripte liegen hier). Keine eingebetteten Skripte oder Styles in den Seiten: Die Sicherheitsregeln (CSP) verbieten das.

## Zum Start

Der Ablauf ist in der Anleitung für den Inhaber beschrieben. Technisch:

1. **Hosting:** Empfohlen Cloudflare Pages (kostenlos, gewerblich erlaubt, Datenschutzvertrag in den Bedingungen). Der kostenlose Vercel-Tarif ist nur für nicht gewerbliche Seiten erlaubt und hat keinen Datenschutzvertrag. Cloudflare-Einstellungen: Production branch `main`, Framework preset `None`, Build command `sh werkzeuge/bauen.sh`, Build output directory `dist`. In der Zone „Email Address Obfuscation“ aus, „Bot Fight Mode“ aus, keine Web Analytics, „Always Use HTTPS“ an. Bleibt es bei Vercel (dann Pro), Abschnitt 2 in `datenschutz.html` auf Vercel umschreiben.
2. **Formular:** Google-Apps-Script im Firmenkonto bereitstellen, siehe `werkzeuge/website-formular/LIESMICH.md`. Dann `python3 werkzeuge/angaben-eintragen.py --formular https://script.google.com/macros/s/…/exec`.
3. **Angaben:** `python3 werkzeuge/angaben-eintragen.py --telefon "02041 …" --email kontakt@alltagsfels.de`. Das trägt Telefon und E-Mail auf allen Seiten ein (auch im Google-Datenblock der Startseite).
4. **Handelsregister:** Sobald Alltagsfels eingetragen ist, den Satz zum alten Namen aus `impressum.html` und `datenschutz.html` entfernen.
5. **Google-Sperre aufheben:** `python3 werkzeuge/angaben-eintragen.py --google-freigeben` (ändert `robots.txt`, `vercel.json`, `_headers`; die Ersatzadressen `….pages.dev` bleiben gesperrt).
6. `python3 werkzeuge/pruefen.py --start` muss „bereit zum Start“ melden. Ohne Telefonnummer darf es losgehen.
7. Nach dem Start prüfen: alle Seiten unter https://alltagsfels.de, `www.` leitet auf die Adresse ohne www weiter, Formular mit Testdaten (Anfrage und Bewerbung), Sicherheitsregeln (z. B. securityheaders.com), Vorschaubild in WhatsApp.
8. Danach: Google Search Console (Sitemap `https://alltagsfels.de/sitemap.xml` einreichen), Google-Unternehmensprofil, Vercel-Projekt löschen.

Später:

- Ab Februar 2027 die Hinweise auf den Start anpassen: Leiste oben auf allen Seiten („Neu in Bottrop: Wir starten im Januar 2027 …“), „Ab Januar 2027 …“ in `index.html` (Ablauf, Schritt 3), `kontakt.html` („So geht es weiter“) und `fragen.html` (Frage „Ab wann kann die Betreuung beginnen?“, sichtbar und im Google-Datenblock).
- `kosten.html` nach dem Bundesrat am 18.12.2026 (Pflegereform) prüfen, „Stand“ anpassen.
- Wirtschafts-Identifikationsnummer ins Impressum, falls vergeben. Nach der Anerkennung von einer Fachperson klären lassen, ob die Behörde ins Impressum muss. Impressum und Datenschutz von einer Fachperson prüfen lassen.
- Stellenangebot: Wenn alle Stellen besetzt sind, „Jobs“ aus Menü und Fußbereich und die Zeile „Wir suchen Verstärkung“ auf „Über uns“ nehmen.

## Struktur

- `index.html`: Startseite (mit Einsatzgebiet und Google-Datenblock)
- `leistungen.html`, `ueber-uns.html`, `kosten.html` (Rechtsstand regelmäßig prüfen), `fragen.html` (mit Google-Datenblock der Fragen)
- `kontakt.html`: Kontaktformular; `mitarbeiten.html`: Stellenangebot mit Bewerbungsformular (als „Jobs“ verlinkt)
- `danke.html`: nach dem Absenden (`danke.html?bewerbung` zeigt die Schritte für Bewerber)
- `impressum.html`, `datenschutz.html`, `404.html`
- `style.css`: Gestaltung (Farben, Schriften, Abstände, Druckansicht)
- `kopf.js`: im Kopf jeder Seite, setzt die gespeicherte Schriftgröße vor dem Anzeigen (keine Sprünge)
- `script.js`: Menü, „Schrift größer“, Drucken, Formulare (Prüfung „Telefon oder E-Mail“, Senden, Fehlerkasten), Jahreszahl
- `fonts/`: Fraunces und Atkinson Hyperlegible Next, lokal
- `images/`: Logo (`logo-kurz.svg` im Kopf, `logo-kurz-hell.svg` im Fuß, `fels-sonne.svg` Bildzeichen, `logo.svg` für Druckvorlagen), Zeichnungen (Quelltext in `zeichnungen/`), `icons.svg`, `vorschau.png` (1200 × 630 für WhatsApp und E-Mail), App-Symbole
- `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.ico`, `apple-touch-icon.png`
- `vercel.json` (Vercel) und `_headers` (Cloudflare): gleiche Sicherheitsregeln und bis zum Start die Google-Sperre. `pruefen.py` meldet, wenn die beiden voneinander abweichen.
- `.vercelignore`: was Vercel nicht ausliefern soll (Druckvorlagen, Zeichnungen, Werkzeuge, README, `_headers`)
- `druckvorlagen/`, `zeichnungen/`: Quelltexte für Druck und Bilder, nicht Teil der Website

## Werkzeuge (`werkzeuge/`)

- `pruefen.py`: prüft alle Seiten (Links, Dateien, Pflichtangaben, gleicher Kopf und Fuß, Sicherheitsregeln, Werberegeln, Seitenliste) und listet, was zum Start noch offen ist. Nur Python 3, keine Zusatzpakete.
- `angaben-eintragen.py`: Telefon, E-Mail, Formular-Adresse eintragen und die Google-Sperre aufheben. Mit `--probe` wird nur angezeigt, was sich ändern würde.
- `bauen.sh`: baut für Cloudflare den Ordner `dist/` (nur Website-Dateien) und bricht ab, wenn `pruefen.py` einen Fehler findet.
- `website-formular/`: das Programm für die Formulare (Google Apps Script) mit Anleitung und Tests (`node werkzeuge/website-formular/test.js`).

## Formulare

Beide Formulare schicken per `fetch` an die eigene Web-App (Google Apps Script im Firmenkonto). Die Web-App prüft die Angaben und schickt sie als E-Mail ins eigene Postfach. Kein Fremddienst, nichts wird gespeichert. Bis die Adresse eingetragen ist, zeigt das Formular beim Absenden einen Hinweis mit der E-Mail-Adresse, und es verlässt nichts die Seite. Ohne JavaScript wird das Formular normal abgeschickt; dann zeigt Google eine einfache Bestätigungsseite.

## Lokal ansehen

```bash
python3 -m http.server 8000
```

Danach im Browser `http://localhost:8000` öffnen. Saubere Adressen ohne `.html` gibt es nur bei Vercel und Cloudflare.
