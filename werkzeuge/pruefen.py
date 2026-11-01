#!/usr/bin/env python3
"""Prüft die Website, bevor eine Änderung übernommen wird.

  python3 werkzeuge/pruefen.py          normale Prüfung (vor jedem Änderungsvorschlag)
  python3 werkzeuge/pruefen.py --start  zusätzlich: ist alles bereit zum Live-Schalten?

Geprüft wird: Links und Dateien, Sicherheitsregeln (keine fremden Skripte,
keine eingebetteten Skripte oder Styles), gleicher Kopf und Fuß auf allen
Seiten, Pflichtangaben je Seite, Google-Datenblöcke, Seitenliste, und die
Werberegeln (keine Preise, keine Anerkennung, keine Wochentage oder Uhrzeiten …).
Braucht nur Python 3, keine Zusatzpakete.
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

HAUPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://alltagsfels.de"
OHNE_BESCHREIBUNG = {"404.html", "danke.html"}
ERLAUBT_EXTERN = (
    DOMAIN + "/",
    DOMAIN,
    "https://www.ldi.nrw.de",
    "https://script.google.com/macros/s/",
    "https://script.google.com/a/macros/",
)
FORMULAR_PLATZHALTER = "FORMULAR-NOCH-NICHT-EINGERICHTET"
ALTE_EMAIL = "alltagsankerbetreuung@gmail.com"

# Werberegeln: Was nirgends im sichtbaren Text stehen darf
VERBOTEN = [
    (r"€|\bEuro\b|\bEUR\b", "Preis oder Betrag"),
    (r"\bUSt\b|Umsatzsteuer|Mehrwertsteuer|MwSt", "Hinweis zur Umsatzsteuer"),
    (r"§\s*45|anerkannt|Anerkennung", "Hinweis auf die Anerkennung"),
    (r"\b(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)s?\b", "Wochentag"),
    (r"\b\d{1,2}([.:]\d{2})?\s*Uhr\b", "Uhrzeit"),
    (r"\b\d+\s*(Stunden|Std\.)\b|Mindestdauer|Absage(frist|regel)", "Bedingung (Dauer, Absagen)"),
    (r"innerhalb von \d+|binnen \d+|\d+\s*Werktag", "Rückmeldezeit"),
    (r"\b\d+\s*Jahren?\b[^.]{0,40}Erfahrung|Erfahrung[^.]{0,40}\b\d+\s*Jahren?\b", "Jahreszahl zur Erfahrung"),
    (r"Vertretung", "Vertretungsregel"),
    (r"\bIBAN\b|\bBIC\b|DE\d{2}\s?\d{4}\s?\d{4}", "Bankverbindung"),
    (r"Kurs (bezahlen|zahlen|stellen)|übernehmen die Kosten|kostenlose(n)? (Kurs|Schulung)", "Zusage zum Grundkurs"),
]

fehler = []
hinweise = []


def melde(datei, text):
    fehler.append(f"{datei}: {text}")


class Leser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.ids = []
        self.skripte = []
        self.titel = ""
        self.h1 = 0
        self.text = []
        self._im = []
        self._skript = None
        self._titel = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a, self.getpos()[0]))
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "script":
            self._skript = {"a": a, "inhalt": "", "zeile": self.getpos()[0]}
        if tag == "title":
            self._titel = True
        if tag == "h1":
            self.h1 += 1
        if tag in ("script", "style"):
            self._im.append(tag)

    def handle_endtag(self, tag):
        if tag == "script" and self._skript is not None:
            self.skripte.append(self._skript)
            self._skript = None
        if tag == "title":
            self._titel = False
        if tag in ("script", "style") and self._im:
            self._im.pop()

    def handle_data(self, data):
        if self._skript is not None:
            self._skript["inhalt"] += data
        elif self._titel:
            self.titel += data
        elif not self._im:
            self.text.append(data)


def lies(datei):
    with open(os.path.join(HAUPT, datei), encoding="utf-8") as d:
        return d.read()


def ziel_datei(pfad):
    """Interner Link -> Datei im Ordner (oder None, wenn extern/kein Ziel)."""
    pfad = pfad.split("#")[0].split("?")[0]
    if pfad in ("", "/"):
        return "index.html"
    pfad = pfad.lstrip("/")
    if os.path.isfile(os.path.join(HAUPT, pfad)):
        return pfad
    if os.path.isfile(os.path.join(HAUPT, pfad + ".html")):
        return pfad + ".html"
    return False


def bloecke(html, tag):
    m = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S)
    if not m:
        return ""
    b = m.group(0)
    b = b.replace(' aria-current="page"', "")
    b = re.sub(r'(href|src)="/', r'\1="', b)
    return b


def pruefe_seiten(start):
    seiten = sorted(os.path.basename(p) for p in glob.glob(os.path.join(HAUPT, "*.html")))
    ids_je_seite = {}
    leser_je_seite = {}
    for s in seiten:
        html = lies(s)
        lp = Leser()
        lp.feed(html)
        leser_je_seite[s] = (lp, html)
        ids_je_seite[s] = set(lp.ids)

    kopf_vorlage = bloecke(leser_je_seite["index.html"][1], "header")
    fuss_vorlage = bloecke(leser_je_seite["index.html"][1], "footer")

    for s in seiten:
        lp, html = leser_je_seite[s]
        if '<html lang="de">' not in html:
            melde(s, 'fehlt <html lang="de">')
        if not lp.titel.strip():
            melde(s, "Seitentitel fehlt")
        if lp.h1 != 1:
            melde(s, f"{lp.h1} Hauptüberschriften (h1), erwartet genau 1")
        doppelt = {i for i in lp.ids if lp.ids.count(i) > 1}
        if doppelt:
            melde(s, "doppelte id: " + ", ".join(sorted(doppelt)))
        if re.search(r"\sstyle\s*=", html) or re.search(r"<style\b", html):
            melde(s, "eingebettetes style – verboten durch die Sicherheitsregeln (CSP)")
        if s not in OHNE_BESCHREIBUNG:
            if not re.search(r'<meta name="description" content="[^"]{50,}"', html):
                melde(s, "Beschreibung (meta description) fehlt oder ist zu kurz")
            kanon = DOMAIN + "/" + ("" if s == "index.html" else s[:-5])
            if f'<link rel="canonical" href="{kanon}" />' not in html:
                melde(s, f"canonical fehlt oder falsch (erwartet {kanon})")
        else:
            if '<meta name="robots" content="noindex" />' not in html:
                melde(s, "soll nicht bei Google erscheinen: robots noindex fehlt")
        for pflicht in ("kopf.js", "script.js", "style.css"):
            if not re.search(rf'(src|href)="/?{re.escape(pflicht)}"', html):
                melde(s, f"{pflicht} wird nicht geladen")
        if bloecke(html, "header") != kopf_vorlage and s != "danke.html":
            melde(s, "Kopfbereich weicht von der Startseite ab")
        if bloecke(html, "footer") != fuss_vorlage:
            melde(s, "Fußbereich weicht von der Startseite ab")

        for sk in lp.skripte:
            typ = sk["a"].get("type", "")
            if "src" in sk["a"]:
                if not ziel_datei(sk["a"]["src"]) or sk["a"]["src"].startswith("http"):
                    melde(s, f"Skript nicht gefunden oder extern: {sk['a']['src']}")
            elif typ == "application/ld+json":
                try:
                    json.loads(sk["inhalt"])
                except ValueError as e:
                    melde(s, f"Google-Datenblock (Zeile {sk['zeile']}) ist kein gültiges JSON: {e}")
            else:
                melde(s, f"eingebettetes Skript in Zeile {sk['zeile']} – verboten durch die Sicherheitsregeln (CSP)")

        for tag, a, zeile in lp.tags:
            if tag == "img" and "alt" not in a:
                melde(s, f"Bild ohne alt-Text (Zeile {zeile})")
            if tag == "a" and a.get("target") == "_blank":
                melde(s, f"Link öffnet neues Fenster (Zeile {zeile}), bitte vermeiden")
            for attr in ("href", "src", "action", "content"):
                wert = a.get(attr)
                if not wert:
                    continue
                if attr == "content" and not wert.startswith("http"):
                    continue
                if wert.startswith(("mailto:", "tel:", "data:")):
                    continue
                if wert.startswith("#"):
                    if wert != "#" and wert[1:] not in ids_je_seite[s]:
                        melde(s, f"Sprungziel {wert} fehlt (Zeile {zeile})")
                    continue
                if wert.startswith(("http://", "https://", "//")):
                    if not wert.startswith(ERLAUBT_EXTERN):
                        melde(s, f"fremde Adresse {wert} (Zeile {zeile})")
                    elif tag in ("script", "img", "iframe") or (tag == "link" and a.get("rel") in ("stylesheet", "preload", "icon")):
                        melde(s, f"lädt etwas von außen: {wert} (Zeile {zeile})")
                    continue
                ziel = ziel_datei(wert)
                if not ziel:
                    melde(s, f"Link/Datei nicht gefunden: {wert} (Zeile {zeile})")
                    continue
                if "#" in wert and ziel.endswith(".html"):
                    anker = wert.split("#", 1)[1]
                    if anker and "/" not in anker and ziel in ids_je_seite and anker not in ids_je_seite[ziel]:
                        melde(s, f"Sprungziel {wert} fehlt (Zeile {zeile})")
                if "#" in wert and ".svg#" in wert:
                    symbol = wert.split("#", 1)[1]
                    if f'id="{symbol}"' not in lies(ziel):
                        melde(s, f"Symbol {symbol} fehlt in {ziel}")

        # Werberegeln im sichtbaren Text (Kommentare zählen nicht)
        text = re.sub(r"\s+", " ", " ".join(lp.text))
        for muster, was in VERBOTEN:
            for m in re.finditer(muster, text):
                umfeld = text[max(0, m.start() - 40): m.end() + 40]
                melde(s, f"Werberegel ({was}): „…{umfeld.strip()}…“")
        if s == "mitarbeiten.html" and re.search(r"\b20\d\d\b", text.replace("©", "")):
            if re.search(r"(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+20\d\d|\b20\d\d\b(?!\s*Alltagsfels)", text):
                melde(s, "Jobs-Seite nennt ein Datum (Bewerbern kein festes Startdatum)")
        if "Alltagsanker" in text.replace(ALTE_EMAIL, "").replace("alltagsankerbetreuung", ""):
            if s not in ("impressum.html", "datenschutz.html"):
                melde(s, "alter Name „Alltagsanker“ im Text")

        # Offene Angaben
        if FORMULAR_PLATZHALTER in html:
            hinweise.append(f"{s}: Formular noch nicht mit dem Google-Konto verbunden")
        if "<!--TELEFON" in html:
            hinweise.append(f"{s}: Telefonnummer noch nicht eingetragen")
        if ALTE_EMAIL in html:
            hinweise.append(f"{s}: noch die Gmail-Adresse statt der Firmen-Adresse")
        if "derzeit noch unter dem bisherigen Namen" in html or "derzeit noch als Alltagsanker" in html:
            hinweise.append(f"{s}: Hinweis auf den alten Namen im Handelsregister (nach der Eintragung entfernen)")
    return seiten


def headers_regeln(text):
    """Liest eine Cloudflare-Datei _headers: {Pfad: {Name: Wert}}."""
    regeln, pfad = {}, None
    for zeile in text.splitlines():
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        if not zeile[0].isspace():
            pfad = zeile.strip()
            regeln.setdefault(pfad, {})
        elif pfad is not None:
            name, _, wert = zeile.strip().partition(":")
            regeln[pfad][name.strip()] = wert.strip()
    return regeln


def pruefe_dateien(seiten, start):
    # vercel.json und _headers: gleiche Sicherheitsregeln
    try:
        cfg = json.loads(lies("vercel.json"))
    except ValueError as e:
        melde("vercel.json", f"kein gültiges JSON: {e}")
        cfg = {}
    kopf = {}
    sperre = False
    for regel in cfg.get("headers", []):
        for k in regel["headers"]:
            if regel["source"] == "/(.*)":
                kopf[k["key"]] = k["value"]
            if k["key"] == "X-Robots-Tag":
                sperre = True
    for pflicht in ("Content-Security-Policy", "X-Content-Type-Options", "Referrer-Policy", "X-Frame-Options", "Permissions-Policy"):
        if pflicht not in kopf:
            melde("vercel.json", f"Sicherheitsregel {pflicht} fehlt")
    csp = kopf.get("Content-Security-Policy", "")
    if "'unsafe-inline'" in csp or "'unsafe-eval'" in csp:
        melde("vercel.json", "CSP erlaubt eingebettete Skripte (unsafe-inline/unsafe-eval)")
    if os.path.isfile(os.path.join(HAUPT, "_headers")):
        # Cloudflare: gleiche Regeln je Pfad wie in vercel.json ("/(.*)" = "/*")
        text = lies("_headers")
        cf = headers_regeln(text)
        vc = {}
        for regel in cfg.get("headers", []):
            pfad = regel["source"].replace("(.*)", "*")
            for k in regel["headers"]:
                vc.setdefault(pfad, {})[k["key"]] = k["value"]
        eigene = {p: r for p, r in cf.items() if p.startswith("/")}
        for pfad in sorted(set(vc) | set(eigene)):
            a, b = vc.get(pfad, {}), eigene.get(pfad, {})
            for k in sorted(set(a) | set(b)):
                if a.get(k) != b.get(k):
                    wo = "nur in vercel.json" if k not in b else "nur in _headers" if k not in a else "unterschiedlich"
                    melde("_headers", f"Regel {k} für {pfad} {wo}")
        if len(cf) > 100:
            melde("_headers", "mehr als 100 Regeln (Cloudflare erlaubt 100)")
        if any(len(z) > 2000 for z in text.splitlines()):
            melde("_headers", "Zeile länger als 2000 Zeichen (Cloudflare erlaubt 2000)")
        for pfad, r in cf.items():
            if not pfad.startswith("/") and r.get("X-Robots-Tag", "").lower() != "noindex":
                melde("_headers", f"{pfad}: Ersatzadresse muss für Google gesperrt bleiben")

    robots = lies("robots.txt")
    gesperrt = bool(re.search(r"Disallow:\s*/\s*$", robots, re.M))
    if sperre or gesperrt:
        hinweise.append("Google-Sperre ist noch an (robots.txt / X-Robots-Tag) – wird zum Start aufgehoben")

    # Seitenliste
    sm = lies("sitemap.xml")
    orte = re.findall(r"<loc>([^<]+)</loc>", sm)
    erwartet = {DOMAIN + "/" + ("" if s == "index.html" else s[:-5]) for s in seiten if s not in OHNE_BESCHREIBUNG}
    if set(orte) != erwartet:
        melde("sitemap.xml", f"Seitenliste passt nicht: fehlt {sorted(erwartet - set(orte))}, zu viel {sorted(set(orte) - erwartet)}")

    # Manifest
    try:
        mf = json.loads(lies("site.webmanifest"))
        for icon in mf.get("icons", []):
            if not ziel_datei(icon["src"]):
                melde("site.webmanifest", f"Symbol fehlt: {icon['src']}")
    except ValueError as e:
        melde("site.webmanifest", f"kein gültiges JSON: {e}")

    # CSS: alle url(...) vorhanden
    css = lies("style.css")
    for u in re.findall(r'url\("?([^")]+)"?\)', css):
        if not u.startswith("data:") and not ziel_datei(u):
            melde("style.css", f"Datei nicht gefunden: {u}")

    # Nichts davon darf auf die Website: Quelltexte, Druckvorlagen, Werkzeuge
    vi = lies(".vercelignore")
    for ordner in ("druckvorlagen/", "zeichnungen/", "werkzeuge/", "README.md"):
        if ordner not in vi:
            melde(".vercelignore", f"{ordner} fehlt (sonst landet es auf der Website)")

    if start:
        for h in hinweise:
            if "Telefonnummer" in h:
                continue  # ohne Telefon darf es losgehen (Rückruf über das Formular)
            fehler.append("Zum Start offen – " + h)


def main():
    start = "--start" in sys.argv
    seiten = pruefe_seiten(start)
    pruefe_dateien(seiten, start)
    if hinweise and not start:
        print("Noch offen (kein Fehler):")
        gruppen = {}
        for h in hinweise:
            seite, _, text = h.partition(".html: ")
            if text:
                gruppen.setdefault(text, set()).add(seite + ".html")
            else:
                gruppen.setdefault(h, set())
        for text, s in sorted(gruppen.items()):
            wo = f" (alle {len(s)} Seiten)" if len(s) >= 8 else f" ({', '.join(sorted(s))})" if s else ""
            print("  · " + text + wo)
        print()
    if fehler:
        print(f"{len(fehler)} Fehler:")
        for f in fehler:
            print("  ✗ " + f)
        sys.exit(1)
    print(f"Alles in Ordnung ({len(seiten)} Seiten geprüft{', bereit zum Start' if start else ''}).")


if __name__ == "__main__":
    main()
