# Alltagsfels – Druckvorlagen

Alle Vorlagen nutzen das neue Logo (Fels mit Sonne), die Farben und die Schriften der Website.
Dieser Ordner erscheint **nicht** auf der Website (siehe `.vercelignore` im Hauptordner).

## Vor dem Druck: gelbe Platzhalter ersetzen

Gelb markiert sind Angaben, die es noch nicht gibt:

- **[TELEFON]** – Telefonnummer
- **[E-MAIL]** – E-Mail-Adresse
- **[IBAN]** – Bankverbindung (nur Briefpapier und E-Mail-Signatur)
- **[TEAM – noch offen]** – Kasten für Julian Wehner und Dominik Vogel (Flyer Seite 4 und Partner-Infoblatt)

Die Platzhalter stehen in den Dateien im Ordner `quellen/`. Nach dem Ersetzen müssen die PDFs neu erstellt werden (siehe unten).

## Fertige PDFs zum Drucken – Ordner `pdf/`

Alle PDFs haben **3 mm Beschnitt** an jeder Seite. Das Endformat ist in der PDF eingetragen.

| Datei | Was ist das? | Format mit Beschnitt | Endformat |
|---|---|---|---|
| `flyer-a5-einzelseiten.pdf` | Flyer, 4 Seiten einzeln (Seite 1 bis 4) | 154 × 216 mm | A5, 148 × 210 mm |
| `flyer-a4-quer-druckbogen.pdf` | Derselbe Flyer als Druckbogen zum Falzen: Blatt 1 = Außenseite (Seite 4 \| Seite 1), Blatt 2 = Innenseite (Seite 2 \| Seite 3) | 303 × 216 mm | A4 quer, einmal gefalzt auf A5 |
| `visitenkarte-julian-wehner.pdf` | Visitenkarte Julian Wehner, Seite 1 vorne, Seite 2 hinten | 91 × 61 mm | 85 × 55 mm |
| `visitenkarte-dominik-vogel.pdf` | Visitenkarte Dominik Vogel, Seite 1 vorne, Seite 2 hinten | 91 × 61 mm | 85 × 55 mm |
| `briefpapier-a4.pdf` | Briefpapier nach DIN 5008 (Form B), zum Vordrucken in der Druckerei | 216 × 303 mm | A4 |
| `partner-infoblatt-a4.pdf` | Infoblatt für Pflegedienste, Pflegeberatung, Sozialdienste und Hausarztpraxen | 216 × 303 mm | A4 |
| `aushang-a4-abreisszettel.pdf` | Aushang für Apotheken, Arztpraxen und Gemeindehäuser, mit 8 Abreißzetteln | 216 × 303 mm | A4 |

Welchen Flyer nehme ich? Die meisten Online-Druckereien wollen für „Flyer A5, 4 Seiten“ die **Einzelseiten**.
Fragt die Druckerei nach einem „Druckbogen“ oder „A4 auf A5 gefalzt“, nehmen Sie den **Druckbogen**.

## Word-Vorlage für Briefe – Ordner `word/`

- `alltagsfels-briefvorlage.docx` – Briefvorlage nach DIN 5008 (Form B) mit Logo, Absenderzeile,
  Falzmarken und Fußzeile. Öffnen, Text überschreiben, drucken. Passt in ein Fensterkuvert (DL oder C6/5).
- **Wichtig:** Damit der Brief richtig aussieht, installieren Sie einmal die Schriften aus dem Ordner
  `schriften/` (Doppelklick auf jede `.ttf`-Datei, dann „Installieren“). Danach Word neu starten.

## E-Mail-Signatur – Ordner `email-signatur/`

- `signatur-julian-wehner.html`, `signatur-dominik-vogel.html` – gestaltete Signatur mit Logo
- `signatur-julian-wehner.txt`, `signatur-dominik-vogel.txt` – dieselbe Signatur als reiner Text
- `alltagsfels-logo-email.png` – kleines Logo für die Signatur
- `anleitung-gmail.md` – Schritt für Schritt: Signatur in Gmail einfügen

## Logo – Ordner `logo/`

| Datei | Wofür? |
|---|---|
| `alltagsfels-logo.svg` / `.png` | Hauptlogo für helle Hintergründe (SVG für Druckereien und Grafiker, PNG für Word, Office usw.) |
| `alltagsfels-logo-weisser-hintergrund.png` | Hauptlogo mit weißem Hintergrund (für Programme ohne Transparenz) |
| `alltagsfels-logo-hell.svg` / `.png` | Logo für dunkle Hintergründe (weiße Schrift) |
| `alltagsfels-zeichen.svg` / `.png` | Nur das Zeichen (Fels mit Sonne), z. B. für Stempel, Profilbilder |
| `alltagsfels-zeichen-hell.svg` / `.png` | Zeichen für dunkle Hintergründe |
| `alltagsfels-logo-email.png` | Kleines Logo für E-Mails |

**Farben:** Blau `#173A66` · Rot `#A33A27` · Sonne `#E0874F` · Sand `#F3E7D6` · Creme `#FBF6EE`
**Schriften:** Fraunces (Überschriften) und Atkinson Hyperlegible (Text) – beide kostenlos (SIL Open Font License).

## Vorschau – Ordner `vorschau/`

Zwei Bilder mit allen Vorlagen auf einen Blick.

## Quelldateien – Ordner `quellen/`

Die Vorlagen sind als HTML-Dateien gebaut (`flyer.html`, `visitenkarten.html`, `briefpapier.html`,
`partner-infoblatt.html`, `aushang.html`), mit gemeinsamer Gestaltung in `druck.css`.
Bilder liegen in `quellen/bilder/`, Schriften in `quellen/schriften/`.

## PDFs neu erstellen (für Technik-Helfer)

```bash
node druckvorlagen/pdf-erstellen.js          # alle PDFs
node druckvorlagen/pdf-erstellen.js flyer    # nur der Flyer
python3 druckvorlagen/word-vorlage-erstellen.py   # Word-Vorlage
```

Benötigt: Node.js mit Playwright (Chromium), Python 3 mit `pypdf` und `python-docx`.

## Hinweise für die Druckerei

- Farbraum: RGB. Die Druckerei wandelt in CMYK um. Kleine Farbabweichungen sind normal.
- Schriften sind in den PDFs eingebettet.
- Mindestschriftgröße für Fließtext: 12 pt. Kleiner sind nur die gesetzlichen Angaben im Briefpapier
  (Absenderzeile und Fußzeile).
