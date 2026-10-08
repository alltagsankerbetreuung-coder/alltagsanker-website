#!/usr/bin/env python3
"""Setzt in den PDFs das exakte Format (mit 3 mm Beschnitt) und trägt
Endformat (TrimBox) und Beschnitt (BleedBox) ein.
Aufruf: python3 pdf-zuschneiden.py DATEI.pdf BREITE_MM HOEHE_MM"""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

MM = 72 / 25.4
datei, breite, hoehe = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
w, h, b = breite * MM, hoehe * MM, 3 * MM

reader = PdfReader(datei)
writer = PdfWriter()
for seite in reader.pages:
    oben = float(seite.mediabox.top)
    unten = oben - h
    box = RectangleObject([0, unten, w, oben])
    seite.mediabox = box
    seite.cropbox = box
    seite.bleedbox = box
    seite.trimbox = RectangleObject([b, unten + b, w - b, oben - b])
    writer.add_page(seite)
writer.add_metadata({"/Title": reader.metadata.get("/Title", "Alltagsfels") if reader.metadata else "Alltagsfels",
                     "/Author": "Alltagsfels"})
with open(datei, "wb") as f:
    writer.write(f)
