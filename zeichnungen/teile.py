"""Gegenstände und Rahmen für die Szenen."""
from kit import *
import math


def bogen_pfad(x0, x1, yb, yt):
    """Bogenfenster: unten gerade bei yb, oben Halbkreis, höchster Punkt yt."""
    r = (x1 - x0) / 2
    cx = x0 + r
    ys = yt + r
    return f"M{P((x0, yb))} L{P((x0, ys))} A{n(r)} {n(r)} 0 0 1 {P((x1, ys))} L{P((x1, yb))} Z"


def tetraeder(x, y, h, color=NAVY, w=1.6):
    """Bottroper Tetraeder auf der Halde, Spitze bei (x, y-h), Fuß bei y."""
    b = h * 0.62
    pts = [(x - b, y), (x, y - h), (x + b, y)]
    o = path(f"M{P(*pts)} Z M{P((x, y - h))} L{P((x - b * 0.25, y))} M{P((x, y - h))} L{P((x + b * 0.35, y))}", stroke=color, w=w)
    o += path(f"M{P((x - b * 0.62, y - h * 0.38))} L{P((x + b * 0.62, y - h * 0.38))} M{P((x - b * 0.3, y - h * 0.7))} L{P((x + b * 0.3, y - h * 0.7))}", stroke=color, w=w * 0.8)
    return o


def tasse(x, y, s=1.0, color=WEISS, inhalt=None, henkel=1):
    """Tasse, Boden bei y, Mitte x."""
    w, h = 18 * s, 16 * s
    o = path(f"M{P((x + henkel * w / 2 - 1, y - h * 0.75))} c{n(henkel * 7 * s)} 0 {n(henkel * 7 * s)} {n(9 * s)} 0 {n(9 * s)}", stroke=color if color != WEISS else HALDE_D, w=3 * s)
    o += path(f"M{P((x - w / 2, y - h))} L{P((x + w / 2, y - h))} L{P((x + w / 2 - 2 * s, y - 3 * s))} Q{P((x + w / 2 - 3 * s, y), (x + w / 2 - 6 * s, y))} L{P((x - w / 2 + 6 * s, y))} Q{P((x - w / 2 + 3 * s, y), (x - w / 2 + 2 * s, y - 3 * s))} Z", fill=color)
    o += path(f"M{P((x - w / 2 + 2 * s, y - h + 5 * s))} L{P((x + w / 2 - 2 * s, y - h + 5 * s))}", stroke=SONNE if color == WEISS else shade(color), w=2.2 * s)
    if inhalt:
        o += path(f"M{P((x - 3 * s, y - h - 5 * s))} q{n(3 * s)} {n(-4 * s)} 0 {n(-8 * s)} M{P((x + 4 * s, y - h - 5 * s))} q{n(3 * s)} {n(-4 * s)} 0 {n(-8 * s)}", stroke=HALDE_D, w=1.8 * s)
    return o


def kanne(x, y, s=1.0, color=BLUE):
    o = path(f"M{P((x - 14 * s, y))} L{P((x - 12 * s, y - 30 * s))} Q{P((x, y - 36 * s), (x + 12 * s, y - 30 * s))} L{P((x + 14 * s, y))} Z", fill=color)
    o += path(f"M{P((x + 12 * s, y - 24 * s))} q{n(12 * s)} {n(-2 * s)} {n(12 * s)} {n(10 * s)} q0 {n(8 * s)} {n(-10 * s)} {n(10 * s)}", stroke=color, w=3.5 * s)
    o += path(f"M{P((x - 12 * s, y - 24 * s))} l{n(-10 * s)} {n(-8 * s)}", stroke=color, w=4 * s)
    o += ellipse(x, y - 34 * s, 7 * s, 3 * s, fill=shade(color))
    o += circle(x, y - 39 * s, 2.6 * s, fill=shade(color))
    o += path(f"M{P((x - 12 * s, y - 14 * s))} L{P((x + 13 * s, y - 14 * s))}", stroke=WEISS, w=2 * s, extra='opacity=".5"')
    return o


def teller_kekse(x, y, s=1.0):
    o = ellipse(x, y - 2 * s, 24 * s, 5 * s, fill=WEISS)
    o += ellipse(x, y - 1 * s, 24 * s, 4 * s, fill=SAND_D)
    o += ellipse(x, y - 4 * s, 24 * s, 4.5 * s, fill=WEISS)
    for dx, dy in ((-9, -8), (2, -9), (11, -7), (-3, -12)):
        o += ellipse(x + dx * s, y + dy * s, 6.5 * s, 3.5 * s, fill=SONNE if dx % 2 else HALDE_D)
    return o


def pflanze(x, y, s=1.0, topf=ROST):
    o = ''
    for ang, ln in ((-35, 26), (-12, 32), (10, 30), (32, 24), (-2, 20)):
        a = math.radians(ang - 90)
        tx, ty = x + math.cos(a) * ln * s, y - 16 * s + math.sin(a) * ln * s
        o += path(f"M{P((x, y - 14 * s))} Q{P((x + (tx - x) * 0.3, ty + 8 * s), (tx, ty))}", stroke=SALBEI_DD, w=2 * s)
        o += ellipse(tx, ty, 6 * s, 3.4 * s, fill=SALBEI_D, extra=f'transform="rotate({n(ang - 90)} {n(tx)} {n(ty)})"')
    o += path(f"M{P((x - 11 * s, y - 16 * s))} L{P((x + 11 * s, y - 16 * s), (x + 8 * s, y), (x - 8 * s, y))} Z", fill=topf)
    o += rect(x - 12 * s, y - 19 * s, 24 * s, 5 * s, fill=shade(topf), rx=1.5 * s)
    return o


def kalender(x, y, w=64, h=74, markiert=(2, 1), seite=WEISS):
    """Wandkalender, oben links bei (x,y)."""
    o = rect(x, y, w, h, fill=seite, rx=4)
    o += rect(x, y, w, h * 0.24, fill=ROST, rx=4)
    o += rect(x, y + h * 0.16, w, h * 0.08, fill=ROST)
    o += circle(x + w * 0.3, y, 2.4, fill=NAVY) + circle(x + w * 0.7, y, 2.4, fill=NAVY)
    cols, rows = 5, 4
    gx = w / (cols + 1)
    gy = (h * 0.7) / (rows + 0.5)
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + gx * (c + 1), y + h * 0.33 + gy * (r + 0.5)
            if (c, r) == markiert:
                o += circle(cx, cy, 5.5, fill=SONNE)
            else:
                o += rect(cx - 3, cy - 1.5, 6, 3, fill=HALDE_D, rx=1)
    return o


def stuhl_lehne(x, yb, h, color=HALDE_D, breite=46):
    """Stuhllehne hinter einer Figur (sichtbar über dem Tisch)."""
    o = rect(x - breite / 2, yb - h, 7, h, fill=color, rx=3)
    o += rect(x + breite / 2 - 7, yb - h, 7, h, fill=color, rx=3)
    o += rect(x - breite / 2 - 2, yb - h - 4, breite + 4, 10, fill=color, rx=5)
    o += rect(x - breite / 2, yb - h * 0.55, breite, 6, fill=color, rx=3)
    return o


def stuhl_seite(x, Y, sh=86, facing=1, color=HALDE_D, lehne=90, s=1.0):
    """Stuhl in Seitenansicht; x = Mitte der Sitzfläche, Y = Boden."""
    f = facing
    sw = 52 * s
    S = Y - sh * s
    o = rect(x - sw / 2, S - 6 * s, sw, 9 * s, fill=color, rx=3 * s)
    o += path(f"M{P((x - sw / 2 + 5 * s, S))} L{P((x - sw / 2 + 5 * s, Y))} M{P((x + sw / 2 - 5 * s, S))} L{P((x + sw / 2 - 5 * s, Y))}", stroke=color, w=5 * s)
    bx = x - f * (sw / 2 - 3 * s)
    o += path(f"M{P((bx, S))} L{P((bx - f * 6 * s, S - lehne * s))}", stroke=color, w=6 * s)
    o += path(f"M{P((bx - f * 2 * s, S - lehne * 0.45 * s))} L{P((bx - f * 5 * s, S - lehne * 0.9 * s))}", stroke=color, w=12 * s)
    return o


def fenster(x, y, w, h, aussen, rahmen=WEISS, sprosse=True):
    """Fenster mit Inhalt 'aussen' (SVG-String, wird auf das Fenster zugeschnitten). id muss eindeutig sein."""
    cid = f"f{int(x)}{int(y)}"
    o = f'<clipPath id="{cid}"><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"/></clipPath>'
    o += f'<g clip-path="url(#{cid})">' + rect(x, y, w, h, fill=CREME) + aussen + '</g>'
    fw = 7
    o += path(f"M{P((x - fw / 2, y - fw / 2))} h{n(w + fw)} v{n(h + fw)} h{n(-w - fw)} Z M{P((x + fw / 2, y + fw / 2))} v{n(h - fw)} h{n(w - fw)} v{n(-h + fw)} Z", fill=rahmen, extra='fill-rule="evenodd"')
    if sprosse:
        o += rect(x + w / 2 - 2.5, y, 5, h, fill=rahmen)
    o += rect(x - 10, y + h + 2, w + 20, 7, fill=rahmen, rx=2)
    return o


def huegel_aussicht(x, y, w, h, tetra=True, sonne=True):
    """Blick nach draußen: Himmel, Sonne, Halde mit Tetraeder, Bäume."""
    o = ''
    if sonne:
        o += circle(x + w * 0.74, y + h * 0.34, h * 0.2, fill=SONNE)
    o += path(f"M{P((x - 5, y + h * 0.78))} C{P((x + w * 0.25, y + h * 0.5), (x + w * 0.55, y + h * 0.48), (x + w + 5, y + h * 0.66))} L{P((x + w + 5, y + h + 5), (x - 5, y + h + 5))} Z", fill=SALBEI_M)
    if tetra:
        o += tetraeder(x + w * 0.42, y + h * 0.53, h * 0.26, color=NAVY, w=1.5)
    o += path(f"M{P((x - 5, y + h * 0.9))} C{P((x + w * 0.3, y + h * 0.78), (x + w * 0.7, y + h * 0.82), (x + w + 5, y + h * 0.76))} L{P((x + w + 5, y + h + 5), (x - 5, y + h + 5))} Z", fill=SALBEI_D)
    return o


def baum(x, y, h=60, s=1.0, krone=SALBEI_D):
    o = rect(x - 3 * s, y - h * 0.45 * s, 6 * s, h * 0.45 * s, fill=HALDE_D, rx=2)
    o += ellipse(x, y - h * 0.62 * s, h * 0.3 * s, h * 0.36 * s, fill=krone)
    o += ellipse(x + h * 0.08 * s, y - h * 0.7 * s, h * 0.16 * s, h * 0.2 * s, fill=shade(krone) if shade(krone) != krone else SALBEI_DD, extra='opacity=".35"')
    return o


def brief(x, y, w=34, h=24, color=WEISS, ang=0, siegel=False):
    o = rect(x - w / 2, y - h / 2, w, h, fill=color, rx=2)
    o += path(f"M{P((x - w / 2 + 2, y - h / 2 + 2))} L{P((x, y + 1), (x + w / 2 - 2, y - h / 2 + 2))}", stroke=HALDE_D, w=1.8)
    if siegel:
        o += circle(x, y + 1, 3, fill=ROST)
    if ang:
        o = f'<g transform="rotate({n(ang)} {n(x)} {n(y)})">{o}</g>'
    return o


def papier(x, y, w=40, h=52, zeilen=4, ang=0, color=WEISS):
    o = rect(x - w / 2, y - h / 2, w, h, fill=color, rx=2)
    for k in range(zeilen):
        yy = y - h / 2 + 10 + k * (h - 16) / max(zeilen - 1, 1)
        o += path(f"M{P((x - w / 2 + 6, yy))} L{P((x + w / 2 - 6 - (8 if k == zeilen - 1 else 0), yy))}", stroke=HALDE_D, w=2)
    if ang:
        o = f'<g transform="rotate({n(ang)} {n(x)} {n(y)})">{o}</g>'
    return o


def sprechblase(x, y, w, h, inhalt='', color=WEISS, schwanz=-1):
    """Sprechblase, Mitte (x,y). schwanz: -1 links unten, 1 rechts unten."""
    o = rect(x - w / 2, y - h / 2, w, h, fill=color, rx=h / 2.4)
    sx = x + schwanz * w * 0.22
    o += path(f"M{P((sx - 7, y + h / 2 - 2))} L{P((sx + schwanz * 4, y + h / 2 + 14), (sx + 9, y + h / 2 - 2))} Z", fill=color)
    return o + inhalt


def uhr(x, y, r=18, rand=NAVY):
    o = circle(x, y, r, fill=WEISS)
    o += circle(x, y, r, stroke=rand, w=3.5)
    o += path(f"M{P((x, y))} L{P((x, y - r * 0.6))} M{P((x, y))} L{P((x + r * 0.45, y + r * 0.2))}", stroke=NAVY, w=2.6)
    return o


def fragezeichen(x, y, s=1.0, color=NAVY, w=4):
    return path(f"M{P((x - 7 * s, y - 8 * s))} C{P((x - 7 * s, y - 16 * s), (x + 8 * s, y - 16 * s), (x + 8 * s, y - 8 * s))} C{P((x + 8 * s, y - 2 * s), (x, y - 1 * s), (x, y + 5 * s))}", stroke=color, w=w * s) + circle(x, y + 12 * s, 2.6 * s, fill=color)


def haken(x, y, s=1.0, color=NAVY, w=4):
    return path(f"M{P((x - 9 * s, y))} L{P((x - 2 * s, y + 7 * s), (x + 10 * s, y - 8 * s))}", stroke=color, w=w * s)


def handy(x, y, s=1.0, ang=0, color=NAVY):
    o = rect(x - 6 * s, y - 11 * s, 12 * s, 22 * s, fill=color, rx=3 * s)
    o += rect(x - 4.2 * s, y - 8.5 * s, 8.4 * s, 15 * s, fill=SALBEI, rx=1 * s)
    if ang:
        o = f'<g transform="rotate({n(ang)} {n(x)} {n(y)})">{o}</g>'
    return o


def handtasche(x, y, s=1.0, color=ROST):
    o = path(f"M{P((x - 10 * s, y - 16 * s))} C{P((x - 10 * s, y - 28 * s), (x + 10 * s, y - 28 * s), (x + 10 * s, y - 16 * s))}", stroke=shade(color), w=3 * s)
    o += path(f"M{P((x - 16 * s, y - 17 * s))} L{P((x + 16 * s, y - 17 * s), (x + 14 * s, y), (x - 14 * s, y))} Z", fill=color)
    o += rect(x - 3 * s, y - 14 * s, 6 * s, 4 * s, fill=SONNE, rx=1)
    return o


def einkaufstuete(x, y, s=1.0):
    """Papiertüte mit Lauch, Brot und Apfel; Boden bei y."""
    o = ''
    o += path(f"M{P((x - 6 * s, y - 40 * s))} L{P((x - 14 * s, y - 72 * s))}", stroke=SALBEI_DD, w=7 * s)
    o += path(f"M{P((x - 14 * s, y - 72 * s))} l{n(-4 * s)} {n(-12 * s)} M{P((x - 14 * s, y - 72 * s))} l{n(5 * s)} {n(-11 * s)}", stroke=SALBEI_D, w=5 * s)
    o += path(f"M{P((x + 2 * s, y - 40 * s))} L{P((x + 14 * s, y - 70 * s))}", stroke=SONNE, w=11 * s)
    o += circle(x + 10 * s, y - 44 * s, 8 * s, fill=ROST)
    o += path(f"M{P((x - 20 * s, y - 44 * s))} L{P((x + 20 * s, y - 44 * s), (x + 18 * s, y), (x - 18 * s, y))} Z", fill=HALDE)
    o += path(f"M{P((x - 20 * s, y - 44 * s))} L{P((x + 20 * s, y - 44 * s))} l{n(-3 * s)} {n(6 * s)} h{n(-34 * s)} Z", fill=HALDE_D)
    return o


def glas(x, y, s=1.0, inhalt=SONNE):
    o = rect(x - 8 * s, y - 20 * s, 16 * s, 20 * s, fill=WEISS, rx=3 * s)
    o += rect(x - 6 * s, y - 13 * s, 12 * s, 11 * s, fill=inhalt, rx=2 * s)
    o += rect(x - 9 * s, y - 25 * s, 18 * s, 6 * s, fill=ROST, rx=2 * s)
    return o


def bank(x, Y, w=150, s=1.0, color=HALDE_D, lehne=True):
    """Parkbank in Seitenansicht von vorn, x = Mitte, Y = Boden. Sitzfläche bei Y-48*s."""
    o = ''
    S = Y - 48 * s
    if lehne:
        o += rect(x - w / 2, S - 50 * s, w, 9 * s, fill=color, rx=3)
        o += rect(x - w / 2, S - 32 * s, w, 9 * s, fill=color, rx=3)
        o += rect(x - w / 2 + 12 * s, S - 50 * s, 6 * s, 50 * s, fill=shade(color))
        o += rect(x + w / 2 - 18 * s, S - 50 * s, 6 * s, 50 * s, fill=shade(color))
    o += rect(x - w / 2 - 4, S, w + 8, 9 * s, fill=color, rx=3)
    o += rect(x - w / 2 + 10 * s, S + 9 * s, 7 * s, 39 * s, fill=NAVY)
    o += rect(x + w / 2 - 17 * s, S + 9 * s, 7 * s, 39 * s, fill=NAVY)
    return o


def laterne(x, Y, h=170, s=1.0):
    o = rect(x - 3 * s, Y - h * s, 6 * s, h * s, fill=NAVY)
    o += path(f"M{P((x - 12 * s, Y - h * s))} L{P((x + 12 * s, Y - h * s), (x + 8 * s, Y - (h + 22) * s), (x - 8 * s, Y - (h + 22) * s))} Z", fill=SONNE)
    o += path(f"M{P((x - 14 * s, Y - (h + 22) * s))} L{P((x + 14 * s, Y - (h + 22) * s), (x, Y - (h + 32) * s))} Z", fill=NAVY)
    return o


def sessel(x, Y, facing=1, color=BLUE, s=1.0):
    """Sessel in Seitenansicht (hinterer Teil); x = Mitte der Sitzfläche; Sitzhöhe 86*s."""
    f = facing
    S = Y - 86 * s
    X = lambda dx: x + f * dx * s
    o = path(f"M{P((X(-38), S + 20 * s))} L{P((X(-40), Y))} M{P((X(34), S + 20 * s))} L{P((X(36), Y))}", stroke=NAVY, w=6 * s)
    cx, cy = X(-44), S + 18 * s
    lehne = rect(X(-44) - 16 * s, S - 104 * s, 32 * s, 126 * s, fill=shade(color), rx=15 * s)
    o += f'<g transform="rotate({n(-9 * f)} {n(cx)} {n(cy)})">{lehne}</g>'
    o += rect(x - 52 * s, S - 6 * s, 104 * s, 30 * s, fill=color, rx=12 * s)
    return o


def sessel_lehne_vorn(x, Y, facing=1, color=BLUE, s=1.0):
    """Seitenteil mit Armlehne, liegt vor der sitzenden Figur."""
    f = facing
    S = Y - 86 * s
    X = lambda dx: x + f * dx * s
    x0, x1 = sorted((X(-56), X(42)))
    o = rect(x0, S - 36 * s, x1 - x0, 62 * s, fill=color, rx=13 * s)
    o += rect(x0, S - 36 * s, x1 - x0, 20 * s, fill=shade(color), rx=10 * s, extra='') if False else ''
    o += path(f"M{P((x0 + 10 * s, S - 14 * s))} H{n(x1 - 10 * s)}", stroke=shade(color), w=3 * s)
    return o


def schatten(x, y, rx, ry=None):
    return ellipse(x, y, rx, ry or rx * 0.09, fill=NAVY, extra='opacity=".1"')


def sofa(x0, x1, Y, color=SALBEI_D, s=1.0):
    """Sofa von vorn: Rückenlehne, Sitzpolster, Armlehnen. Sitzhöhe 86*s."""
    S = Y - 86 * s
    o = rect(x0 + 10 * s, S - 92 * s, x1 - x0 - 20 * s, 100 * s, fill=shade(color), rx=18 * s)
    o += rect(x0, S - 8 * s, x1 - x0, 36 * s, fill=color, rx=12 * s)
    o += rect(x0 - 10 * s, S - 44 * s, 34 * s, 74 * s, fill=color, rx=14 * s)
    o += rect(x1 - 24 * s, S - 44 * s, 34 * s, 74 * s, fill=color, rx=14 * s)
    o += path(f"M{P((x0 + 14 * s, S + 28 * s))} L{P((x0 + 12 * s, Y))} M{P((x1 - 14 * s, S + 28 * s))} L{P((x1 - 12 * s, Y))}", stroke=NAVY, w=6 * s)
    return o


def couchtisch(x, Y, w=120, h=46, s=1.0, color=HALDE_D):
    o = rect(x - w / 2, Y - h * s, w, 9 * s, fill=color, rx=3)
    o += rect(x - w / 2 + 8, Y - h * s + 9 * s, 6, (h - 9) * s, fill=shade(color))
    o += rect(x + w / 2 - 14, Y - h * s + 9 * s, 6, (h - 9) * s, fill=shade(color))
    return o


def mappe(x, y, s=1.0, color=BLUE, ang=0):
    o = rect(x - 16 * s, y - 20 * s, 32 * s, 40 * s, fill=color, rx=3 * s)
    o += rect(x - 12 * s, y - 24 * s, 28 * s, 40 * s, fill=WEISS, rx=2 * s)
    for k in range(3):
        o += path(f"M{P((x - 7 * s, y - 16 * s + k * 8 * s))} h{n(18 * s)}", stroke=HALDE_D, w=2 * s)
    if ang:
        o = f'<g transform="rotate({n(ang)} {n(x)} {n(y)})">{o}</g>'
    return o


def bistrotisch(x, Y, r=46, h=120, s=1.0, color=WEISS):
    T = Y - h * s
    o = rect(x - 3 * s, T, 6 * s, h * s, fill=NAVY)
    o += path(f"M{P((x - 22 * s, Y))} Q{P((x, Y - 10 * s), (x + 22 * s, Y))} Z", fill=NAVY)
    o += ellipse(x, T, r * s, 7 * s, fill=color)
    o += path(f"M{P((x - r * s, T))} a{n(r * s)} {n(7 * s)} 0 0 0 {n(2 * r * s)} 0 v4 a{n(r * s)} {n(7 * s)} 0 0 1 {n(-2 * r * s)} 0 Z", fill=SAND_D)
    return o


def buch(x, y, s=1.0, color=BLUE, offen=False):
    if offen:
        o = path(f"M{P((x, y))} Q{P((x - 12 * s, y - 6 * s), (x - 24 * s, y - 2 * s))} L{P((x - 24 * s, y + 4 * s))} Q{P((x - 12 * s, y), (x, y + 6 * s))} Q{P((x + 12 * s, y), (x + 24 * s, y + 4 * s))} L{P((x + 24 * s, y - 2 * s))} Q{P((x + 12 * s, y - 6 * s), (x, y))} Z", fill=WEISS)
        o += path(f"M{P((x, y))} L{P((x, y + 6 * s))}", stroke=HALDE_D, w=1.5)
        return o
    o = rect(x - 20 * s, y - 6 * s, 40 * s, 8 * s, fill=color, rx=1.5 * s)
    o += rect(x - 18 * s, y - 4 * s, 37 * s, 4 * s, fill=WEISS)
    return o


def laptop(x, y, s=1.0, facing=1, color=NAVY):
    """Aufgeklappter Laptop in Seitenansicht, Boden bei y, Bildschirm zur Figur gerichtet (facing = Richtung des Bildschirms)."""
    f = facing
    o = rect(x - 26 * s, y - 4 * s, 52 * s, 4 * s, fill=color, rx=1.5 * s)
    o += path(f"M{P((x + f * 24 * s, y - 4 * s))} L{P((x + f * 14 * s, y - 44 * s), (x + f * 19 * s, y - 45 * s), (x + f * 28 * s, y - 4 * s))} Z", fill=color)
    return o


def wegweiser(x, Y, h=190, s=1.0):
    o = rect(x - 4 * s, Y - h * s, 8 * s, h * s, fill=HALDE_D)
    o += circle(x, Y - h * s, 6 * s, fill=SONNE)
    y1 = Y - (h - 30) * s
    o += path(f"M{P((x - 6 * s, y1 - 15 * s))} L{P((x + 78 * s, y1 - 15 * s), (x + 96 * s, y1), (x + 78 * s, y1 + 15 * s), (x - 6 * s, y1 + 15 * s))} Z", fill=NAVY)
    o += path(f"M{P((x + 12 * s, y1))} h{n(56 * s)}", stroke=CREME, w=3 * s)
    y2 = Y - (h - 76) * s
    o += path(f"M{P((x + 6 * s, y2 - 14 * s))} L{P((x - 70 * s, y2 - 14 * s), (x - 86 * s, y2), (x - 70 * s, y2 + 14 * s), (x + 6 * s, y2 + 14 * s))} Z", fill=ROST)
    o += path(f"M{P((x - 62 * s, y2))} h{n(50 * s)}", stroke=CREME, w=3 * s)
    return o


def briefkasten(x, Y, s=1.0, color=SONNE):
    o = rect(x - 4 * s, Y - 90 * s, 8 * s, 90 * s, fill=NAVY)
    o += path(f"M{P((x - 30 * s, Y - 90 * s))} L{P((x + 30 * s, Y - 90 * s), (x + 30 * s, Y - 140 * s))} Q{P((x + 30 * s, Y - 158 * s), (x, Y - 158 * s))} Q{P((x - 30 * s, Y - 158 * s), (x - 30 * s, Y - 140 * s))} Z", fill=color)
    o += rect(x - 20 * s, Y - 136 * s, 40 * s, 6 * s, fill=shade(color), rx=3 * s)
    return o


def ziegelwand(x, y, w, h, color='#b65a3f', fuge='#9c4a33', reihe=16, stein=40):
    o = rect(x, y, w, h, fill=color)
    yy = y + reihe
    k = 0
    d = ''
    while yy < y + h:
        d += f"M{P((x, yy))} H{n(x + w)} "
        off = (stein / 2) if k % 2 else 0
        xx = x + off
        while xx < x + w:
            d += f"M{P((xx, yy - reihe))} V{n(yy)} "
            xx += stein
        yy += reihe
        k += 1
    o += path(d, stroke=fuge, w=1.6)
    return o


def foerderturm(x, Y, h=150, color=NAVY, w=2.2):
    """Fördergerüst (Zeche), Fuß bei Y."""
    b = h * 0.32
    o = path(f"M{P((x - b, Y))} L{P((x - b * 0.3, Y - h))} L{P((x + b * 0.3, Y - h))} L{P((x + b, Y))}", stroke=color, w=w)
    o += path(f"M{P((x - b * 0.3, Y - h))} L{P((x + b * 1.4, Y - h * 0.15))}", stroke=color, w=w)
    for t in (0.25, 0.5, 0.75):
        xl = x - b + (b * 0.7) * t
        xr = x + b - (b * 0.7) * t
        o += path(f"M{P((xl, Y - h * t))} L{P((xr, Y - h * t))}", stroke=color, w=w * 0.8)
    o += path(f"M{P((x - b, Y))} L{P((x + b * 0.3 * 0.5, Y - h * 0.5))} L{P((x - b * 0.65, Y - h * 0.5))} L{P((x + b * 0.3, Y - h))}", stroke=color, w=w * 0.7)
    o += circle(x - b * 0.12, Y - h - 8, 9, stroke=color, w=w)
    o += circle(x + b * 0.32, Y - h - 8, 9, stroke=color, w=w)
    return o


def zechenhaus(x, Y, w=120, h=90, dach=NAVY, wand='#b65a3f'):
    """Bergmannshaus mit Satteldach (Giebel zur Straße)."""
    o = ziegelwand(x - w / 2, Y - h, w, h, color=wand, fuge='#9c4a33', reihe=12, stein=30)
    o += path(f"M{P((x - w / 2 - 8, Y - h))} L{P((x, Y - h - w * 0.45), (x + w / 2 + 8, Y - h))} Z", fill=dach)
    o += rect(x - w * 0.3, Y - h * 0.7, w * 0.2, h * 0.3, fill=WEISS)
    o += rect(x + w * 0.1, Y - h * 0.7, w * 0.2, h * 0.3, fill=WEISS)
    o += rect(x - w * 0.08, Y - h * 0.38, w * 0.16, h * 0.38, fill=NAVY)
    o += rect(x - w * 0.06, Y - h - w * 0.26, w * 0.12, w * 0.12, fill=WEISS)
    return o
