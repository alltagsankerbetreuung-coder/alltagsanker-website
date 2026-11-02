# Website-Formular (Google Apps Script)

Die beiden Formulare der Website (Anfrage auf `kontakt.html`, Bewerbung auf
`mitarbeiten.html`) schicken ihre Angaben an ein kleines Programm im
Google-Konto der Firma. Das Programm prüft die Angaben und schickt sie als
E-Mail in das Postfach. Es speichert nichts, schickt keine Mails an Fremde und
schreibt keine Inhalte in Protokolle.

- `Code.gs`: das Programm (öffentlich, also nie Passwörter hineinschreiben)
- `test.js`: Prüfungen ohne Google (`node werkzeuge/website-formular/test.js`)

## Einrichten (einmal, ca. 10 Minuten)

**Wichtig:** Im **Firmenkonto** (Google Workspace, Adresse @alltagsfels.de)
einrichten, nicht im alten Gmail-Konto. Nur für das Firmenkonto gibt es den
Datenschutzvertrag mit Google, und die Datenschutzerklärung beschreibt genau das.

1. Im Firmenkonto angemeldet `https://script.google.com` öffnen.
2. **Neues Projekt**. Oben links auf „Unbenanntes Projekt“ klicken und
   `Website-Formular Alltagsfels` eintragen.
3. Im Editor den ganzen vorhandenen Text löschen und den Inhalt von `Code.gs`
   einfügen. Speichern (Disketten-Symbol oder Strg+S).
4. Oben rechts **Bereitstellen → Neue Bereitstellung**.
   - Beim Zahnrad „Typ auswählen“ **Web-App** wählen.
   - Beschreibung: `Website`
   - Ausführen als: **Ich (…@alltagsfels.de)**
   - Wer hat Zugriff: **Jeder** (nicht „Jeder mit Google-Konto“)
5. **Bereitstellen**. Google fragt nach der Erlaubnis („Zugriff autorisieren“):
   Konto wählen, bei „Google hat diese App nicht überprüft“ auf **Erweitert →
   Website-Formular Alltagsfels öffnen (unsicher)** und **Zulassen**. Das ist
   normal bei eigenen Programmen. Erbeten werden nur zwei Rechte: E-Mails in
   deinem Namen senden und deine E-Mail-Adresse sehen.
6. Die **Web-App-URL** kopieren (endet auf `/exec`) und an Claude schicken.

## Testen

- Die Web-App-URL im Browser öffnen. Richtig ist eine Zeile wie
  `{"ok":true,"dienst":"Website-Formular Alltagsfels","version":"2026-11-01"}`.
- Dann trägt Claude die Adresse ein:
  `python3 werkzeuge/angaben-eintragen.py --formular https://script.google.com/macros/s/…/exec`
  und `python3 werkzeuge/pruefen.py`.
- Nach dem Übernehmen auf der Vorschau einmal eine Anfrage und eine Bewerbung
  mit Testdaten abschicken. Beide Mails müssen im Postfach ankommen
  (Betreff „Neue Anfrage über die Website: …“ bzw. „Neue Bewerbung …“).
  „Antworten“ geht direkt an die angegebene E-Mail-Adresse.

## Ändern

Neue Fassung von `Code.gs` einfügen, speichern, dann **Bereitstellen →
Bereitstellungen verwalten → Stift (Bearbeiten) → Version: „Neue Version“ →
Bereitstellen**. So bleibt die Adresse gleich. „Neue Bereitstellung“ würde eine
neue Adresse erzeugen, die dann auf der Website neu eingetragen werden muss.

## Wie es funktioniert

- Die Website schickt die Angaben per `fetch` (POST, `antwort=json`) und zeigt
  bei Erfolg die Danke-Seite. Ohne JavaScript schickt der Browser das Formular
  normal ab und bekommt eine einfache Bestätigungsseite von Google.
- Schutz: unsichtbares Fallen-Feld `_honey` (wird es ausgefüllt, wird nichts
  gesendet), Längengrenzen je Feld, Pflichtfelder, höchstens 30 Nachrichten pro
  Stunde, Mails nur an das eigene Postfach.
- Die Sicherheitsregeln der Website (`vercel.json`) erlauben
  `script.google.com` und `script.googleusercontent.com` (Google leitet die
  Antwort dorthin weiter).

## Wenn etwas nicht klappt

- **„Zugriff: Jeder“ fehlt in der Auswahl:** In der Google-Admin-Konsole ist das
  Teilen außerhalb der Firma gesperrt. Unter Apps → Google Workspace → Drive und
  Docs → Freigabeeinstellungen das Teilen nach außen erlauben.
- **Die Website meldet „Ihre Nachricht ist leider noch nicht bei uns
  angekommen“:** Web-App-URL im Browser öffnen. Kommt eine Google-Anmeldung
  statt der Zeile mit `"ok":true`, steht „Wer hat Zugriff“ nicht auf „Jeder“.
- **Keine Mail im Postfach:** In script.google.com links auf „Ausführungen“
  schauen. Dort steht, ob das Programm lief und ob es einen Fehler gab.
