# Zeichnungen der Website

Alle Zeichnungen auf der Website (Alltagsszenen, Karte, Wegweiser) entstehen aus den Python-Dateien in diesem Ordner. Es gibt keine Fotos und keine fremden Bilder.

## Stil

- Flache Flächen ohne Umrisslinien, wie beim Logo.
- Jede Szene steht in einem Bogenfenster mit einer dunkelblauen Bodenlinie.
- Nur die Farben der Website, dazu Haut- und Haartöne.
- Kein Text in den Bildern. Was ein Bild zeigt, steht im `alt`-Text in der HTML-Datei.
- Menschen tun das, was im Text daneben steht. Keine Gehstöcke oder Rollatoren als Kennzeichen für „alt“.

## Dateien

- `kit.py`: Farben, Köpfe, Kleidung und Grundformen
- `figuren.py`: Haltungen (sitzend, stehend, Oberkörper)
- `teile.py`: Möbel und Gegenstände (Tisch, Sessel, Fenster, Tetraeder, Förderturm …)
- `szenen.py`: die einzelnen Bilder; die Liste `ALLE` ordnet jedem Dateinamen eine Szene zu
- `karte.py`: Karte des Einsatzgebiets. Die Orte liegen nach echten Koordinaten um Bottrop, 20 km = 230 Pixel. Die Ortsnamen stehen nicht im Bild, sondern als Text darüber (`.karte-orte` in `style.css`).

## Neu erzeugen

Python 3 genügt, es braucht keine Zusatzpakete.

```
cd zeichnungen
python3 szenen.py ../images
python3 karte.py ../images/karte.svg
```

`karte.py` gibt danach die Lage jedes Ortes in Prozent aus. Danach richten sich die Ortsnamen in `style.css` (`.karte-orte .ort-…`).

Der Ordner wird nicht mit auf die Website geladen (`.vercelignore`).
