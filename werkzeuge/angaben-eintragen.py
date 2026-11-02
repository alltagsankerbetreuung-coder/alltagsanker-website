#!/usr/bin/env python3
"""Trägt Angaben, die es noch nicht gibt, auf allen Seiten auf einmal ein.

Beispiele (im Hauptordner der Website ausführen):

  python3 werkzeuge/angaben-eintragen.py --telefon "02041 123456"
  python3 werkzeuge/angaben-eintragen.py --email kontakt@alltagsfels.de
  python3 werkzeuge/angaben-eintragen.py --formular https://script.google.com/macros/s/ABC…/exec
  python3 werkzeuge/angaben-eintragen.py --google-freigeben   (erst zum Start!)

Mit --probe wird nichts gespeichert, es wird nur angezeigt, was sich ändern würde.
Danach immer: python3 werkzeuge/pruefen.py

Telefon: In den Seiten stehen fertige Stellen als HTML-Kommentar
  <!--TELEFON … TELEFON_LINK … TELEFON_ANZEIGE … TELEFON-->
Das Skript macht daraus sichtbaren Inhalt und ergänzt die Nummer im
Google-Datenblock der Startseite.
"""
import argparse
import glob
import html
import json
import os
import re
import sys

HAUPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALTE_EMAIL = "alltagsankerbetreuung@gmail.com"
FORMULAR_PLATZHALTER = "https://script.google.com/macros/s/FORMULAR-NOCH-NICHT-EINGERICHTET/exec"
TELEFON_BLOCK = re.compile(r"<!--TELEFON(.*?)TELEFON-->", re.S)


def seiten():
    return sorted(glob.glob(os.path.join(HAUPT, "*.html")))


def telefon_pruefen(eingabe):
    anzeige = re.sub(r"\s+", " ", eingabe.strip())
    ziffern = re.sub(r"[^\d+]", "", anzeige)
    if ziffern.startswith("00"):
        ziffern = "+" + ziffern[2:]
    elif ziffern.startswith("0"):
        ziffern = "+49" + ziffern[1:]
    if not re.fullmatch(r"\+\d{7,15}", ziffern):
        sys.exit(f"Telefonnummer sieht falsch aus: {eingabe!r}")
    if not re.fullmatch(r"[\d +()/\-]+", anzeige):
        sys.exit(f"Bitte nur Ziffern, Leerzeichen, + / - ( ) verwenden: {eingabe!r}")
    return anzeige, ziffern


def telefon_eintragen(text, anzeige, link, datei):
    neu = TELEFON_BLOCK.sub(
        lambda m: m.group(1).replace("TELEFON_LINK", html.escape(link)).replace("TELEFON_ANZEIGE", html.escape(anzeige)),
        text,
    )
    if os.path.basename(datei) == "index.html" and '"telephone"' not in neu:
        zeile = re.search(r'\n(\s*)"email": "[^"]+",\n', neu)
        if not zeile:
            sys.exit("Google-Datenblock in index.html nicht gefunden.")
        einzug = zeile.group(1)
        neu = neu[: zeile.end()] + f'{einzug}"telephone": "{link}",\n' + neu[zeile.end():]
    return neu


def email_pruefen(adresse):
    if not re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", adresse):
        sys.exit(f"E-Mail-Adresse sieht falsch aus: {adresse!r}")
    return adresse


def email_eintragen(text, neu):
    lokal_alt, domain_alt = ALTE_EMAIL.split("@")
    lokal_neu, domain_neu = neu.split("@")
    text = text.replace(f"{lokal_alt}<wbr />@{domain_alt}", f"{lokal_neu}<wbr />@{domain_neu}")
    return text.replace(ALTE_EMAIL, neu)


def formular_pruefen(adresse):
    if not re.fullmatch(r"https://script\.google\.com/(a/macros/[A-Za-z0-9.-]+|macros)/s/[A-Za-z0-9_-]{20,}/exec", adresse):
        sys.exit("Das ist keine Web-App-Adresse von Google Apps Script (…/macros/s/…/exec).")
    return adresse


def google_freigeben(probe):
    """Hebt die Google-Sperre auf: robots.txt und vercel.json."""
    dateien = {}
    dateien["robots.txt"] = "User-agent: *\nAllow: /\n\nSitemap: https://alltagsfels.de/sitemap.xml\n"

    pfad = os.path.join(HAUPT, "vercel.json")
    with open(pfad, encoding="utf-8") as d:
        text = d.read()
    neu = re.sub(r',\s*\{\s*"source": "/\(\.\*\)",\s*"headers": \[\s*\{ "key": "X-Robots-Tag", "value": "[^"]*" \}\s*\]\s*\}', "", text)
    cfg = json.loads(neu)
    if any(k["key"] == "X-Robots-Tag" for r in cfg.get("headers", []) for k in r["headers"]):
        sys.exit("vercel.json: Google-Sperre nicht gefunden oder anders aufgebaut, bitte von Hand ändern.")
    dateien["vercel.json"] = neu

    for name, inhalt in dateien.items():
        with open(os.path.join(HAUPT, name), encoding="utf-8") as d:
            if d.read() == inhalt:
                continue
        print(("würde ändern: " if probe else "geändert: ") + name)
        if not probe:
            with open(os.path.join(HAUPT, name), "w", encoding="utf-8") as d:
                d.write(inhalt)


def main():
    teile = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    teile.add_argument("--telefon", help='z. B. "02041 123456"')
    teile.add_argument("--email", help="neue E-Mail-Adresse, z. B. kontakt@alltagsfels.de")
    teile.add_argument("--formular", help="Web-App-Adresse des Website-Formulars (…/exec)")
    teile.add_argument("--google-freigeben", action="store_true", help="Google-Sperre aufheben (erst zum Start)")
    teile.add_argument("--probe", action="store_true", help="nichts speichern, nur anzeigen")
    a = teile.parse_args()
    if not (a.telefon or a.email or a.formular or a.google_freigeben):
        teile.print_help()
        return
    if a.google_freigeben:
        google_freigeben(a.probe)
        if not (a.telefon or a.email or a.formular):
            return

    tel = telefon_pruefen(a.telefon) if a.telefon else None
    mail = email_pruefen(a.email) if a.email else None
    formular = formular_pruefen(a.formular) if a.formular else None

    geaendert = 0
    for datei in seiten():
        with open(datei, encoding="utf-8") as d:
            alt = d.read()
        neu = alt
        if tel:
            neu = telefon_eintragen(neu, tel[0], tel[1], datei)
        if mail:
            neu = email_eintragen(neu, mail)
        if formular:
            neu = neu.replace(FORMULAR_PLATZHALTER, formular)
        if neu != alt:
            geaendert += 1
            print(("würde ändern: " if a.probe else "geändert: ") + os.path.basename(datei))
            if not a.probe:
                with open(datei, "w", encoding="utf-8") as d:
                    d.write(neu)

    if formular and not a.probe:
        # Sicherheitsregel: Formular-Adresse muss erlaubt sein (steht schon für script.google.com drin)
        with open(os.path.join(HAUPT, "vercel.json"), encoding="utf-8") as d:
            if "https://script.google.com" not in d.read():
                print("Achtung: script.google.com fehlt in den Sicherheitsregeln (vercel.json).")
    print(f"{geaendert} Seiten {'würden geändert' if a.probe else 'geändert'}. Jetzt prüfen: python3 werkzeuge/pruefen.py")


if __name__ == "__main__":
    main()
