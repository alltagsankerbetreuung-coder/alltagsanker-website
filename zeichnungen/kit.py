"""Zeichen-Baukasten für die Alltagsfels-Illustrationen.
Flächiger Stil ohne Umrisslinien (wie das Logo), Navy nur als Farbe und für feine Details."""

NAVY = '#2b3328'   # Dunkelgrün aus dem Logo
NAVY_D = '#1f2a1e'
BLUE = '#5a6152'   # Stein
BLUE_D = '#474d40'
ROST = '#9c5b3b'   # Ziegel, gedeckt
ROST_D = '#7f4a30'
SONNE = '#d6ac7a'  # Sonne im Logo
SONNE_D = '#b98547'  # Ocker
CREME = '#fbf6ee'
SAND = '#f3e7d6'
SAND_D = '#e9d8c1'
HALDE = '#d9c6ab'
HALDE_D = '#c3ac8b'
SALBEI = '#e3e8d6'
SALBEI_M = '#c9d4b8'
SALBEI_D = '#a7b78f'
SALBEI_DD = '#8a9c72'
WEISS = '#ffffff'
TINTE = '#1f2a1e'  # Augen, Brauen

SKIN = {'hell': ('#f6d8c2', '#e7bfa3'), 'mittel': ('#d9a37f', '#c38c68'), 'dunkel': ('#9a6748', '#845539')}
HAIR = {'weiss': ('#f5f2ec', '#dcd6cc'), 'grau': ('#cdc8bf', '#b4aea4'), 'braun': ('#6e4b36', '#583a29'),
        'dunkel': ('#33251f', '#251a15'), 'blond': ('#d9b571', '#c49c55')}
SHADE = {SONNE_D: '#9a6c35', NAVY: NAVY_D, BLUE: BLUE_D, ROST: ROST_D, SONNE: SONNE_D, SAND_D: HALDE, HALDE: HALDE_D,
         SALBEI_M: SALBEI_D, SALBEI_D: SALBEI_DD, CREME: SAND_D, SAND: SAND_D, WEISS: SAND}


def shade(c):
    return SHADE.get(c, c)


def n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith('.0') else s


def P(*pts):
    return ' '.join(f"{n(x)} {n(y)}" for x, y in pts)


def path(d, fill='none', stroke=None, w=2, extra=''):
    s = f'<path d="{d}"'
    if fill != 'none':
        s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{n(w)}"'
    return s + (f' {extra}' if extra else '') + '/>'


def circle(x, y, r, fill='none', stroke=None, w=2, extra=''):
    s = f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}"'
    if fill != 'none':
        s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{n(w)}"'
    return s + (f' {extra}' if extra else '') + '/>'


def ellipse(x, y, rx, ry, fill='none', stroke=None, w=2, extra=''):
    s = f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}"'
    if fill != 'none':
        s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{n(w)}"'
    return s + (f' {extra}' if extra else '') + '/>'


def rect(x, y, w_, h_, fill='none', stroke=None, w=2, rx=0):
    s = f'<rect x="{n(x)}" y="{n(y)}" width="{n(w_)}" height="{n(h_)}"'
    if rx:
        s += f' rx="{n(rx)}"'
    if fill != 'none':
        s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{n(w)}"'
    return s + '/>'


def line(*pts, w=2, stroke=NAVY):
    return path('M' + P(*pts), stroke=stroke, w=w)


def g(content, x=0, y=0, s=1, flip=False, extra=''):
    t = []
    if x or y:
        t.append(f'translate({n(x)} {n(y)})')
    if flip:
        t.append('scale(-1 1)')
    if s != 1:
        t.append(f'scale({n(s) if s * 10 % 1 == 0 else s})')
    tr = f' transform="{" ".join(t)}"' if t else ''
    return f'<g{tr}{(" " + extra) if extra else ""}>' + ''.join(content if isinstance(content, list) else [content]) + '</g>'


def limb(pts, wd, color, edge=None, curve=True):
    """Gliedmaße als dicker runder Strich. edge: schmale dunklere Kante (für vordere Arme vor gleichfarbigem Rumpf)."""
    if curve and len(pts) == 3:
        (x0, y0), (x1, y1), (x2, y2) = pts
        cx, cy = 2 * x1 - (x0 + x2) / 2, 2 * y1 - (y0 + y2) / 2
        d = f"M{P((x0, y0))} Q{P((cx, cy), (x2, y2))}"
    else:
        d = 'M' + ' L'.join(P(p) for p in pts)
    o = ''
    if edge:
        o += f'<path d="{d}" stroke="{edge}" stroke-width="{n(wd + 3)}"/>'
    o += f'<path d="{d}" stroke="{color}" stroke-width="{n(wd)}"/>'
    return o


def taper(a, b, wa, wb, color):
    """Konische Form zwischen zwei Punkten (für Oberschenkel, Unterarme), runde Enden."""
    import math
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    p1 = (x0 + nx * wa / 2, y0 + ny * wa / 2)
    p2 = (x1 + nx * wb / 2, y1 + ny * wb / 2)
    p3 = (x1 - nx * wb / 2, y1 - ny * wb / 2)
    p4 = (x0 - nx * wa / 2, y0 - ny * wa / 2)
    d = (f"M{P(p1)} L{P(p2)} A{n(wb / 2)} {n(wb / 2)} 0 0 1 {P(p3)} L{P(p4)} A{n(wa / 2)} {n(wa / 2)} 0 0 1 {P(p1)} Z")
    return path(d, fill=color)


def hand(x, y, skin, r=5.4):
    return ellipse(x, y, r * 1.1, r * 0.92, fill=skin)


def shoe(x, y, color=NAVY_D, facing=1, s=1.0):
    f = facing
    d = (f"M{P((x - 6 * s * f, y))} L{P((x + 15 * s * f, y))} C{P((x + 17 * s * f, y - 7 * s), (x + 9 * s * f, y - 10 * s), (x + 2 * s * f, y - 10 * s))}"
         f" L{P((x - 6 * s * f, y - 10 * s))} C{P((x - 8 * s * f, y - 8 * s), (x - 8 * s * f, y - 2 * s), (x - 6 * s * f, y))} Z")
    return path(d, fill=color)


# ---------- Köpfe (Blick nach rechts, 3/4-Ansicht) ----------

FACE = 'M0 -21 C10 -21 17 -13 17 -1 C17 10 12 19 3 20 C-6 21 -16 12 -16 0 C-16 -12 -10 -21 0 -21 Z'


def head(char, expr='laecheln', look=0.0):
    sk, skd = SKIN[char['haut']]
    hr, hrd = HAIR[char['haarfarbe']]
    style = char['frisur']
    o = []
    # hinter dem Kopf
    if style == 'dutt':
        o.append(circle(-12, -19, 8.5, fill=hrd))
    if style == 'schulter':
        o.append(path('M-12 -14 C-25 -4 -26 16 -22 28 C-15 31 -6 30 -2 25 L2 8 Z', fill=hrd))
    if style == 'zopf':
        o.append(path('M-15 -8 C-25 0 -27 15 -23 26 C-19 29 -14 27 -13 22 C-15 13 -13 3 -9 -3 Z', fill=hrd))
    # Hals-Schatten unter dem Kinn wird im Körper gezeichnet
    o.append(path(FACE, fill=sk))
    # Nase (Profilnase)
    o.append(path(f'M{P((15.5 + look, -3))} C{P((18.5 + look, 2), (21.5 + look, 5.5), (19.5 + look, 7.5))} C{P((18.5 + look, 8.5), (16.5 + look, 8.5), (15 + look, 8))} Z', fill=sk))
    # Haare
    if style == 'bob':
        o.append(path('M17 -9 C16 -24 -6 -29 -17 -19 C-24 -12 -25 6 -21 16 C-18 21 -11 20 -8 15 C-10 8 -10 1 -7 -5 C-2 -12 8 -13 17 -9 Z', fill=hr))
        o.append(path('M-16 -11 C-12 -6 -13 1 -16 6 M-5 -19 C1 -16 8 -15 13 -16', stroke=hrd, w=1.8))
    elif style in ('dutt', 'zopf'):
        o.append(path('M17 -6 C16 -23 -6 -27 -17 -17 C-22 -12 -22 -2 -19 6 C-16 8 -11 6 -9 1 C-8 -4 -4 -9 2 -10 C9 -11 14 -10 17 -6 Z', fill=hr))
        o.append(path('M-5 -20 C2 -17 8 -15 13 -15', stroke=hrd, w=1.6))
    elif style == 'kurz':
        o.append(path('M17 -8 C16 -22 -5 -26 -16 -17 C-20 -12 -20 -3 -17 4 C-13 4 -11 0 -10 -4 C-6 -9 6 -12 17 -8 Z', fill=hr))
    elif style == 'schulter':
        o.append(path('M17 -7 C15 -23 -6 -28 -18 -17 C-22 -11 -22 0 -18 9 C-13 7 -10 1 -8 -3 C-3 -9 8 -11 17 -7 Z', fill=hr))
        o.append(path('M-7 -21 C0 -17 7 -15 13 -16', stroke=hrd, w=1.6))
    elif style == 'glatze':
        o.append(path('M-16 -6 C-19 3 -17 12 -11 14 C-9 9 -8 3 -8 -1 C-11 -3 -14 -5 -16 -6 Z', fill=hr))
    elif style == 'muetze':
        o.append(path('M-16 -6 C-19 3 -17 12 -11 14 C-9 9 -8 3 -8 -1 C-11 -3 -14 -5 -16 -6 Z', fill=hr))
        cap = char.get('muetze', BLUE)
        o.append(path('M-18 -5 C-20 -17 -6 -24 8 -22 C17 -21 24 -17 27 -12 C28 -9 23 -8 17 -9 C6 -11 -7 -9 -18 -5 Z', fill=cap))
        o.append(path('M14 -10 C19 -8 26 -8 27 -12 C24 -14 19 -14 14 -13 Z', fill=shade(cap)))
        o.append(path('M-12 -17 C-4 -20 6 -20 14 -17', stroke=shade(cap), w=1.4))
    # Ohr
    o.append(ellipse(-6.5, 3, 3.8, 5.4, fill=sk))
    o.append(path('M-7.5 0.5 C-5 1 -5 5 -7.5 5.5', stroke=skd, w=1.5))
    # Augen und Brauen
    lx = look
    if expr == 'zu':
        o.append(path(f"M{P((1.5 + lx, 1))} Q{P((4 + lx, -1.5), (6.5 + lx, 1))} M{P((10.5 + lx, 1))} Q{P((13 + lx, -1.5), (15.5 + lx, 1))}", stroke=TINTE, w=1.8))
    else:
        o.append(ellipse(4 + lx, 0.5, 1.9, 2.4, fill=TINTE))
        o.append(ellipse(13.2 + lx, 0.5, 1.7, 2.3, fill=TINTE))
    o.append(path(f"M{P((0.5 + lx, -5.5))} Q{P((4 + lx, -8), (7 + lx, -6.5))} M{P((10.5 + lx, -6.5))} Q{P((13.5 + lx, -8), (16 + lx, -5.5))}", stroke=char.get('braue', hrd if style not in ('glatze', 'muetze') else '#9a948a'), w=1.8))
    # Mund
    if expr in ('lachen', 'zu'):
        o.append(path(f"M{P((5 + lx, 11))} Q{P((10 + lx, 17.5), (14.5 + lx, 10.5))} Z", fill=TINTE))
        o.append(path(f"M{P((7 + lx, 13.3))} Q{P((10 + lx, 16), (12.8 + lx, 13))}", stroke='#c96b5c', w=1.6))
    elif expr == 'reden':
        o.append(ellipse(10.5 + lx, 12.5, 2.8, 2.2, fill=TINTE))
    else:
        o.append(path(f"M{P((6 + lx, 11.5))} Q{P((10 + lx, 14.5), (14 + lx, 11))}", stroke=TINTE, w=1.8))
    # Wange
    o.append(ellipse(2 + lx, 8, 3.6, 2.6, fill='#e98b6d', extra='opacity=".28"'))
    if char.get('falten'):
        o.append(path(f"M{P((16.5 + lx, -2.5))} l2 -1 M{P((16.5 + lx, 1.5))} l2.2 0.6", stroke=skd, w=1.2))
    if char.get('brille'):
        bc = char.get('brillenfarbe', NAVY)
        o.append(circle(4 + lx, 0.5, 5.2, stroke=bc, w=1.7))
        o.append(circle(14 + lx, 0.5, 4.5, stroke=bc, w=1.7))
        o.append(path(f"M{P((9.2 + lx, 0))} L{P((9.6 + lx, 0))} M{P((-1.2 + lx, -0.5))} L{P((-5.5, 0.5))}", stroke=bc, w=1.7))
    if char.get('bart'):
        o.append(path('M-8 5 C-7 15 0 21 7 20 C12 19 16.5 15 16.5 9 C13 12.5 9 14 6 13.5 C1 13 -4 10 -8 5 Z', fill=hrd))
        o.append(path(f"M{P((7 + lx, 12.5))} Q{P((10 + lx, 14.5), (13 + lx, 12))}", stroke=sk, w=1.6))
    return ''.join(o)


# ---------- Rumpf ----------

def torso(char, hals, becken, breite, facing=1, lang=None):
    """Rumpf von der Halsbasis bis zum Becken (vor dem Becken gerundet)."""
    sk, skd = SKIN[char['haut']]
    top = char['oben']
    hx, hy = hals
    bx, by = becken
    f = facing
    br = breite
    o = []
    # Hals
    o.append(path(f"M{P((hx - 5.5, hy - 14))} L{P((hx - 5.5, hy + 2), (hx + 5.5, hy + 2), (hx + 5.5, hy - 14))} Z", fill=skd))
    sx, sy = hx - f * 2, hy
    d = (f"M{P((sx - br / 2, sy + 12))} C{P((sx - br / 2, sy + 1), (sx - br / 4, sy - 1), (sx, sy - 1))}"
         f" C{P((sx + br / 4, sy - 1), (sx + br / 2, sy + 1), (sx + br / 2, sy + 12))}"
         f" L{P((bx + br * 0.44, by))} C{P((bx + br * 0.3, by + 7), (bx - br * 0.3, by + 7), (bx - br * 0.44, by))} Z")
    o.append(path(d, fill=top))
    stil = char.get('stil')
    cx_ = sx + f * br * 0.17
    if stil == 'strickjacke':
        inner = char.get('innen', CREME)
        bx2 = bx + f * br * 0.17
        o.append(path(f"M{P((cx_ - 6, sy - 1))} L{P((cx_ + 6, sy - 1), (bx2 + 2, by + 3), (bx2 - 2, by + 3))} Z", fill=inner))
        o.append(path(f"M{P((cx_ - 6, sy - 1))} L{P((bx2 - 2, by + 3))} M{P((cx_ + 6, sy - 1))} L{P((bx2 + 2, by + 3))}", stroke=shade(top), w=1.6))
        for k in range(3):
            t = 0.28 + k * 0.22
            xx = cx_ + (bx2 - cx_) * t + f * 4.5
            yy = sy + (by - sy) * t
            o.append(circle(xx, yy, 1.7, fill=shade(top)))
    elif stil == 'weste':
        inner = char.get('innen', BLUE)
        o.append(path(f"M{P((cx_ - 7, sy - 1))} L{P((cx_ + 7, sy - 1), (cx_ + 1, sy + 18))} Z", fill=inner))
        o.append(path(f"M{P((cx_ - 3, sy - 1))} L{P((cx_ + 1, sy + 7), (cx_ + 4, sy - 1))} Z", fill=WEISS))
    elif stil == 'kragen':
        o.append(path(f"M{P((cx_ - 8, sy - 1))} L{P((cx_, sy + 8), (cx_ + 8, sy - 1))} Z", fill=char.get('innen', WEISS)))
    elif stil == 'rund':
        o.append(path(f"M{P((cx_ - 7, sy - 1))} Q{P((cx_, sy + 6), (cx_ + 7, sy - 1))}", stroke=shade(top), w=2))
    return ''.join(o)


# ---------- Besetzung ----------

SENIORIN = dict(haut='hell', frisur='bob', haarfarbe='weiss', brille=True, falten=True, oben=SALBEI_D, stil='strickjacke', innen=CREME, hose=BLUE, rock=BLUE, schuh=NAVY_D)
SENIOR = dict(haut='hell', frisur='muetze', haarfarbe='weiss', falten=True, muetze=BLUE, oben=SONNE_D, stil='weste', innen=CREME, hose=NAVY, schuh=NAVY_D)
SENIOR_B = dict(haut='hell', frisur='glatze', haarfarbe='weiss', brille=True, falten=True, oben=BLUE, stil='kragen', innen=WEISS, hose=NAVY, schuh=NAVY_D)
HELFERIN = dict(haut='mittel', frisur='dutt', haarfarbe='dunkel', oben=NAVY, stil='kragen', innen=SAND, hose=HALDE, schuh=NAVY_D)
HELFER = dict(haut='hell', frisur='kurz', haarfarbe='braun', bart=True, oben=NAVY, stil='kragen', innen=SAND, hose=HALDE, schuh=NAVY_D)
TOCHTER = dict(haut='hell', frisur='schulter', haarfarbe='braun', oben=ROST, stil='rund', hose=NAVY, schuh=NAVY_D)


def svg(w, h, body, title=None):
    t = f'<title>{title}</title>' if title else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            + t + body + '</svg>')
