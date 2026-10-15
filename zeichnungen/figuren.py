"""Posen für die Figuren. Eine Pose liefert Ebenen, damit Tische, Stühle usw. dazwischen liegen können.
Maßstab 1: Kopfhöhe etwa 42 px, Sitzhöhe 86, Tischhöhe 140."""
from kit import *

KOPF = 1.12
ORDNUNG = ('bein_h', 'arm_h', 'rumpf', 'kopf', 'bein_v', 'arm_v')


def zeichne(l, ohne=()):
    return ''.join(l[k] for k in ORDNUNG if k not in ohne and k in l)


def _hand_arm(pts, color, sk, wd, hand_r, kante=False):
    o = limb(pts, wd, color, edge=(shade(color) if kante else None))
    x, y = pts[-1]
    return o + hand(x, y, sk, r=hand_r)


def _schoss(X, Ys, color):
    d = (f"M{P((X(-18), Ys(0)))} L{P((X(50), Ys(0)))} C{P((X(59), Ys(0)), (X(63), Ys(-6)), (X(63), Ys(-12)))}"
         f" C{P((X(63), Ys(-19)), (X(58), Ys(-24)), (X(50), Ys(-24)))} L{P((X(8), Ys(-28)))}"
         f" C{P((X(-6), Ys(-30)), (X(-18), Ys(-26)), (X(-20), Ys(-16)))} C{P((X(-21), Ys(-8)), (X(-20), Ys(-2)), (X(-18), Ys(0)))} Z")
    return path(d, fill=color)


def _sitzbein(X, Ys, Y, color, schuh, f, s, back=False, dx=0):
    c = shade(color) if back else color
    sc = shade(schuh) if back else schuh
    Xd = lambda v: X(v + dx)
    o = _schoss(Xd, Ys, c)
    o += limb([(Xd(52), Ys(-12)), (Xd(50), Y - 14 * s)], 16 * s, c, curve=False)
    o += shoe(Xd(48), Y - 4.5 * s, sc, f, s=s)
    return o


def _stehbein(pts, color, schuh, f, s, back=False, schuh_winkel=0):
    c = shade(color) if back else color
    sc = shade(schuh) if back else schuh
    o = limb(pts, 17 * s, c, curve=False)
    ax, ay = pts[-1]
    sh_ = shoe(ax - f * 2 * s, ay + 10 * s, sc, f, s=s)
    if schuh_winkel:
        sh_ = f'<g transform="rotate({n(schuh_winkel * f)} {n(ax)} {n(ay + 8 * s)})">{sh_}</g>'
    return o + sh_


def _kopf(char, pos, s, f, expr, look, tilt, drehpunkt):
    k = g(head(char, expr, look), pos[0], pos[1], s=round(s * KOPF, 3), flip=f < 0)
    if tilt:
        k = f'<g transform="rotate({n(tilt * f)} {n(drehpunkt[0])} {n(drehpunkt[1])})">{k}</g>'
    return k


ARME_SITZ = {
    # Schulter, Ellbogen, Hand relativ zur Sitzfläche (dx, dy)
    'schoss': [(-8, -84), (-4, -46), (26, -26)],
    'schoss_v': [(16, -84), (22, -46), (44, -24)],
    'tisch': [(-8, -84), (6, -56), (40, -58)],
    'tisch_v': [(16, -84), (30, -56), (60, -60)],
    'tasse_v': [(16, -84), (28, -54), (52, -66)],
    'reden_v': [(16, -84), (30, -56), (54, -76)],
    'zeigen_v': [(16, -84), (36, -66), (66, -74)],
    'telefon_v': [(16, -84), (32, -60), (24, -108)],
    'buch_v': [(16, -84), (26, -50), (48, -50)],
    'lehne': [(-8, -84), (-16, -52), (-8, -28)],
    'arm_um_v': [(16, -84), (36, -82), (58, -86)],
    'brief_v': [(16, -84), (30, -56), (50, -84)],
    'tasche_v': [(16, -84), (24, -48), (40, -34)],
    'spiel_v': [(16, -84), (30, -56), (62, -64)],
    'hoch_v': [(16, -84), (34, -76), (40, -118)],
}


def sitzend(char, x, Y, facing=1, s=1.0, sh=86, expr='laecheln', look=0.0, arme=('schoss', 'schoss_v'), beine='normal', tilt=0, lean=4, kopf_f=None):
    f = facing
    X = lambda dx: x + f * dx * s
    S = Y - sh * s
    Ys = lambda dy: S + dy * s
    sk, skd = SKIN[char['haut']]
    top = char['oben']
    hose = char.get('hose', NAVY)
    schuh = char.get('schuh', NAVY_D)
    L = {}
    L['bein_h'] = _sitzbein(X, Ys, Y, hose, schuh, f, s, back=True, dx=-8)
    ah = arme[0] if not isinstance(arme[0], str) else ARME_SITZ[arme[0]]
    L['arm_h'] = _hand_arm([(X(a), Ys(b)) for a, b in ah], shade(top), sk, 13 * s, 5.6 * s)
    hals = (X(6 + lean), Ys(-92))
    L['rumpf'] = torso(char, hals, (X(0), Ys(-6)), 46 * s, f)
    L['kopf'] = _kopf(char, (X(10 + lean * 1.2), Ys(-120)), s, kopf_f or f, expr, look, tilt, (X(8 + lean), Ys(-94)))
    if beine == 'gekreuzt':
        bv = taper((X(4), Ys(-10)), (X(50), Ys(-24)), 26 * s, 18 * s, hose)
        bv += limb([(X(50), Ys(-24)), (X(70), Ys(30)), (X(66), Y - 34 * s)], 16 * s, hose, curve=False)
        bv += shoe(X(64), Y - 24 * s, schuh, f, s=s)
        L['bein_v'] = bv
    else:
        L['bein_v'] = _sitzbein(X, Ys, Y, hose, schuh, f, s)
    av = arme[1] if not isinstance(arme[1], str) else ARME_SITZ[arme[1]]
    L['arm_v'] = _hand_arm([(X(a), Ys(b)) for a, b in av], top, sk, 13 * s, 5.6 * s, kante=True)
    return L


ARME_STEH = {
    'haengen': [(-12, -208), (-16, -168), (-13, -130)],
    'haengen_v': [(14, -208), (17, -168), (14, -130)],
    'schwingen': [(-12, -208), (-22, -170), (-30, -136)],
    'schwingen_v': [(14, -208), (22, -170), (34, -140)],
    'vorn': [(-12, -208), (-2, -172), (24, -160)],
    'vorn_v': [(14, -208), (24, -172), (48, -164)],
    'klingeln_v': [(14, -208), (30, -186), (52, -196)],
    'winken_v': [(14, -208), (36, -212), (38, -250)],
    'tuer_v': [(14, -208), (30, -180), (50, -170)],
    'einhaken_v': [(14, -208), (22, -176), (44, -170)],
    'zettel_v': [(14, -208), (24, -176), (40, -186)],
    'regal_v': [(14, -208), (34, -224), (54, -238)],
    'tasche': [(-12, -208), (-10, -170), (-4, -134)],
    'erzaehlen_v': [(14, -208), (32, -184), (52, -196)],
    'kalender_v': [(14, -208), (34, -214), (54, -230)],
    'zeigen_v': [(14, -208), (36, -200), (62, -206)],
    'mappe_v': [(14, -208), (26, -176), (44, -178)],
}


def stehend(char, x, Y, facing=1, s=1.0, expr='laecheln', look=0.0, arme=('haengen', 'haengen_v'), tilt=0, gehen=0.0, lean=0, kopf_f=None):
    f = facing
    X = lambda dx: x + f * dx * s
    Yy = lambda dy: Y + dy * s
    sk, skd = SKIN[char['haut']]
    top = char['oben']
    hose = char.get('hose', NAVY)
    schuh = char.get('schuh', NAVY_D)
    st = gehen
    L = {}
    if st:
        L['bein_h'] = _stehbein([(X(-3), Yy(-124)), (X(-6 - 8 * st), Yy(-66)), (X(-10 - 22 * st), Yy(-14 + 2 * st))], hose, schuh, f, s, back=True, schuh_winkel=-16 * st)
        L['bein_v'] = _stehbein([(X(4), Yy(-124)), (X(10 + 10 * st), Yy(-68)), (X(12 + 18 * st), Yy(-12))], hose, schuh, f, s)
    else:
        L['bein_h'] = _stehbein([(X(-6), Yy(-124)), (X(-7), Yy(-66)), (X(-8), Yy(-12))], hose, schuh, f, s, back=True)
        L['bein_v'] = _stehbein([(X(6), Yy(-124)), (X(7), Yy(-66)), (X(8), Yy(-12))], hose, schuh, f, s)
    ah = arme[0] if not isinstance(arme[0], str) else ARME_STEH[arme[0]]
    L['arm_h'] = _hand_arm([(X(a + lean * (1 if b < -150 else 0.5)), Yy(b)) for a, b in ah], shade(top), sk, 13 * s, 5.8 * s)
    L['rumpf'] = torso(char, (X(2 + lean), Yy(-220)), (X(0), Yy(-122)), 46 * s, f)
    L['kopf'] = _kopf(char, (X(5 + lean * 1.3), Yy(-248)), s, kopf_f or f, expr, look, tilt, (X(3 + lean), Yy(-222)))
    av = arme[1] if not isinstance(arme[1], str) else ARME_STEH[arme[1]]
    L['arm_v'] = _hand_arm([(X(a + lean * (1 if b < -150 else 0.5)), Yy(b)) for a, b in av], top, sk, 13 * s, 5.8 * s, kante=True)
    return L


def oberkoerper(char, x, T, facing=1, s=1.0, expr='laecheln', look=0.0, arme=('tisch', 'tisch_v'), tilt=0, lean=4, kopf_f=None):
    """Nur Oberkörper hinter einer Kante (z. B. Theke). T = Höhe der Kante; Becken unterhalb verdeckt."""
    f = facing
    X = lambda dx: x + f * dx * s
    Yt = lambda dy: T + dy * s
    sk, skd = SKIN[char['haut']]
    top = char['oben']
    L = {}
    arme_ok = {
        'tisch': [(-12, -68), (-4, -28), (22, -8)],
        'tisch_v': [(14, -68), (26, -32), (50, -8)],
        'hoch_v': [(14, -68), (34, -60), (52, -86)],
    }
    ah = arme[0] if not isinstance(arme[0], str) else arme_ok[arme[0]]
    L['arm_h'] = _hand_arm([(X(a), Yt(b)) for a, b in ah], shade(top), sk, 13 * s, 5.6 * s)
    L['rumpf'] = torso(char, (X(3 + lean), Yt(-78)), (X(0), Yt(40)), 46 * s, f)
    L['kopf'] = _kopf(char, (X(7 + lean * 1.2), Yt(-106)), s, kopf_f or f, expr, look, tilt, (X(5 + lean), Yt(-80)))
    av = arme[1] if not isinstance(arme[1], str) else arme_ok[arme[1]]
    L['arm_v'] = _hand_arm([(X(a), Yt(b)) for a, b in av], top, sk, 13 * s, 5.6 * s, kante=True)
    return L
