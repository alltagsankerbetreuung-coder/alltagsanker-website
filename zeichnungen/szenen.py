"""Die einzelnen Szenen. Jede Funktion gibt einen SVG-String zurück."""
from figuren import *
from teile import *

W, H = 640, 462
BODEN = 452  # Bodenlinie aller Kopfbilder


def rahmen_bogen(inhalt, cid='b', x0=72, x1=568, yt=10, wand=SAND, boden=SAND_D, boden_y=392, sonne=None):
    """Szene in einem Bogenfenster. sonne=(x,y,r) zeichnet eine Sonne hinter dem Bogen."""
    d = bogen_pfad(x0, x1, BODEN, yt)
    o = ''
    if sonne:
        o += circle(*sonne, fill=SONNE)
    o += f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    o += f'<g clip-path="url(#{cid})">'
    o += rect(0, 0, W, H, fill=wand)
    o += rect(0, boden_y, W, H - boden_y, fill=boden)
    o += inhalt
    o += '</g>'
    o += rect(x0 - 26, BODEN - 1.5, x1 - x0 + 52, 3, fill=NAVY, rx=1.5)
    return o


def hero():
    s = 1.1
    Y = 436
    T = Y - 140 * s
    sen = dict(SENIORIN, haarfarbe='grau')
    inhalt = ''
    inhalt += fenster(236, 70, 168, 128, huegel_aussicht(236, 70, 168, 128))
    inhalt += pflanze(374, 205, s=0.85)
    inhalt += kalender(436, 108, w=54, h=62)
    inhalt += path('M320 0 L320 34', stroke=NAVY, w=2)
    inhalt += path('M298 54 Q320 26 342 54 Z', fill=NAVY)
    inhalt += ellipse(320, 55, 8, 3.5, fill=SONNE)
    inhalt += ellipse(320, Y + 2, 210, 12, fill=SALBEI_M)
    a = sitzend(sen, 172, Y, facing=1, s=s, expr='lachen', arme=('tisch', 'tasse_v'), lean=6)
    b = sitzend(HELFERIN, 468, Y, facing=-1, s=s, expr='laecheln', arme=('tisch', 'tisch_v'), lean=6, tilt=-4)
    inhalt += stuhl_seite(172, Y, facing=1, s=s, lehne=96)
    inhalt += stuhl_seite(468, Y, facing=-1, s=s, lehne=96)
    inhalt += zeichne(a, ohne=('arm_v',)) + zeichne(b, ohne=('arm_v',))
    # Tisch
    inhalt += rect(206, T, 228, 12, fill=HALDE_D, rx=4)
    inhalt += rect(216, T + 12, 208, 10, fill=HALDE)
    inhalt += rect(240, T + 22, 10, Y - T - 22, fill=HALDE_D)
    inhalt += rect(390, T + 22, 10, Y - T - 22, fill=HALDE_D)
    inhalt += kanne(322, T, s=0.95)
    inhalt += teller_kekse(282, T + 1, s=0.8)
    inhalt += tasse(256, T, s=1.05, inhalt=True, henkel=-1)
    inhalt += tasse(372, T, s=1.05, inhalt=True)
    inhalt += a['arm_v'] + b['arm_v']
    return svg(W, H, rahmen_bogen(inhalt, 'hero'))



# ---------- Leistungs-Bilder (gleiches Format und gleicher Bogen wie die Kopfbilder) ----------
B2 = dict(x0=56, x1=584, yt=10)


def spot_gesellschaft():
    Y, s = 436, 1.1
    o = path('M40 330 C200 290 380 296 600 318 L600 470 L40 470 Z', fill=SALBEI_M)
    o += circle(446, 118, 34, fill=SONNE)
    o += baum(138, 360, h=230) + baum(520, 352, h=180)
    o += bank(468, 372, w=110, s=0.7, color=HALDE_D)
    o += path('M40 452 C180 400 420 392 600 410 L600 470 L40 470 Z', fill=SAND_D)
    b = stehend(HELFERIN, 372, Y, facing=1, s=s, gehen=0.5, arme=('schwingen', 'haengen_v'), kopf_f=-1, expr='lachen')
    a = stehend(SENIOR, 262, Y, facing=1, s=s, gehen=0.55, arme=('schwingen', 'erzaehlen_v'), expr='reden')
    o += zeichne(b) + zeichne(a)
    return svg(W, H, rahmen_bogen(o, 'sg', wand=SAND, boden=SALBEI_M, boden_y=470, **B2))


def spot_begleitung():
    Y, s = 436, 1.1
    o = uhr(320, 96, r=22)
    o += rect(452, 196, 84, 196, fill=HALDE, rx=3) + rect(464, 212, 60, 58, fill=SALBEI, rx=2) + circle(522, 300, 4.5, fill=NAVY)
    o += rect(458, 168, 72, 18, fill=NAVY, rx=4) + path('M470 177 h22 M498 177 h22', stroke=CREME, w=2.6)
    o += rect(112, 150, 74, 54, fill=WEISS, rx=2) + path('M119 198 L140 174 L154 186 L166 170 L180 198 Z', fill=SALBEI_D) + circle(166, 162, 6, fill=SONNE)
    o += pflanze(110, 400, s=1.5)
    o += stuhl_seite(226, Y, facing=1, s=s, lehne=92) + stuhl_seite(410, Y, facing=-1, s=s, lehne=92)
    a = sitzend(SENIORIN, 226, Y, facing=1, s=s, arme=('schoss', 'tasche_v'), expr='laecheln', tilt=3)
    b = sitzend(HELFER, 410, Y, facing=-1, s=s, arme=('schoss', 'reden_v'), expr='reden', tilt=-3)
    o += zeichne(a, ohne=('arm_v',)) + handtasche(270, Y - 101, s=1.1) + a['arm_v']
    o += zeichne(b)
    return svg(W, H, rahmen_bogen(o, 'sb', **B2))


def spot_haushalt():
    Y, s = 436, 1.1
    T = Y - 130
    o = rect(0, T - 52, W, 52, fill=SALBEI)
    o += path(''.join(f'M{x} {T - 52} V{T} ' for x in range(30, 640, 26)) + f'M0 {T - 26} H640', stroke=SALBEI_M, w=1.6)
    o += rect(0, T, W, H - T, fill=HALDE) + rect(0, T, W, 11, fill=HALDE_D)
    o += ''.join(rect(x, T + 24, 88, 104, fill=SAND_D, rx=3) + rect(x + 36, T + 34, 16, 4.5, fill=NAVY, rx=2) for x in (60, 158, 256, 354, 452))
    o += rect(330, 118, 196, 108, fill=HALDE_D, rx=4) + rect(337, 125, 88, 94, fill=HALDE, rx=2)
    o += rect(431, 125, 88, 94, fill=CREME, rx=2) + rect(431, 170, 88, 5, fill=HALDE_D)
    o += glas(452, 169, s=0.95, inhalt=SONNE) + glas(492, 169, s=0.95, inhalt=SALBEI_D) + glas(452, 218, s=0.95, inhalt=ROST)
    o += rect(398, 166, 18, 5, fill=NAVY, rx=2)
    o += einkaufstuete(306, T + 2, s=1.15)
    a = stehend(SENIOR_B, 186, Y, facing=1, s=s, arme=('haengen', 'zettel_v'), expr='laecheln', tilt=6)
    o += zeichne(a, ohne=('arm_v',)) + papier(232, Y - 216, w=26, h=34, zeilen=3, ang=-8) + a['arm_v']
    b = stehend(HELFERIN, 414, Y, facing=1, s=s, arme=('haengen', 'regal_v'), kopf_f=-1, expr='lachen')
    o += zeichne(b, ohne=('arm_v',)) + glas(474, Y - 258, s=1.0, inhalt=SONNE) + b['arm_v']
    return svg(W, H, rahmen_bogen(o, 'sh', boden=HALDE, **B2))


def spot_ordnen():
    Y, s = 436, 1.1
    T = Y - 154
    o = kalender(446, 132, w=84, h=96, markiert=(3, 2))
    o += uhr(170, 150, r=20)
    o += stuhl_seite(178, Y, facing=1, s=s, lehne=92)
    a = sitzend(SENIORIN, 178, Y, facing=1, s=s, arme=('tisch', 'brief_v'), expr='laecheln', tilt=5)
    o += zeichne(a, ohne=('arm_v',))
    o += rect(232, T, 150, 11, fill=HALDE_D, rx=3) + rect(246, T + 11, 9, Y - T - 11, fill=HALDE_D) + rect(360, T + 11, 9, Y - T - 11, fill=HALDE_D)
    o += brief(300, T - 4, w=34, h=8) + tasse(344, T, s=1.0)
    o += papier(244, Y - 214, w=36, h=46, zeilen=4, ang=-6) + a['arm_v']
    b = stehend(HELFERIN, 404, Y, facing=1, s=s, arme=('haengen', 'kalender_v'), kopf_f=-1, expr='laecheln')
    o += zeichne(b, ohne=('arm_v',)) + path('M466 190 L476 176', stroke=ROST, w=4.5) + b['arm_v']
    return svg(W, H, rahmen_bogen(o, 'so', **B2))


def spot_angehoerige():
    Y, s = 436, 1.1
    o = path('M40 340 C160 290 300 300 360 326 C430 290 540 296 600 330 L600 470 L40 470 Z', fill=SALBEI_M)
    o += circle(452, 128, 36, fill=SONNE)
    o += path('M196 120 q7 -7 14 0 q7 -7 14 0 M240 96 q6 -6 12 0 q6 -6 12 0', stroke=NAVY, w=2.4)
    o += pflanze(536, 420, s=1.6, topf=ROST)
    o += stuhl_seite(240, Y, facing=1, color=NAVY, s=s, lehne=90)
    a = sitzend(TOCHTER, 240, Y, facing=1, s=s, arme=('schoss', 'tasse_v'), expr='zu', tilt=-8, lean=0)
    o += zeichne(a, ohne=('arm_v',))
    o += bistrotisch(356, Y, r=56, h=150, s=1.0)
    o += buch(372, Y - 154, s=1.0, color=ROST) + tasse(338, Y - 151, s=0.95)
    o += tasse(301, Y - 165, s=0.9, inhalt=True) + a['arm_v']
    return svg(W, H, rahmen_bogen(o, 'sa', wand=SAND, boden=SAND_D, boden_y=430, **B2))


# ---------- Kopfbilder der Unterseiten ----------

def kontakt():
    Y, s = 436, 1.15
    o = fenster(162, 108, 116, 136, huegel_aussicht(162, 108, 116, 136, tetra=False, sonne=True) + baum(198, 252, h=100))
    o += rect(430, 120, 74, 92, fill=WEISS, rx=2) + rect(437, 127, 60, 78, fill=SALBEI_M) + circle(467, 158, 14, fill=SONNE) + path('M437 205 L462 176 L478 192 L497 170 L497 205 Z', fill=SALBEI_D)
    # Stehlampe
    o += rect(518, 196, 5, 200, fill=NAVY) + path('M496 200 L546 200 L536 160 L506 160 Z', fill=SONNE) + path('M506 396 L536 396', stroke=NAVY, w=5)
    o += ellipse(330, Y + 2, 190, 12, fill=SALBEI_M)
    o += sessel(300, Y, facing=1, color=BLUE, s=s)
    a = sitzend(SENIORIN, 300, Y, facing=1, s=s, arme=('schoss', 'telefon_v'), expr='reden', tilt=-4, lean=2)
    o += zeichne(a, ohne=('arm_v',))
    o += sessel_lehne_vorn(300, Y, facing=1, color=BLUE, s=s)
    o += a['arm_v'] + handy(330, Y - 99 - 124, s=1.15, ang=12)
    o += sprechblase(430, 214, 64, 40) + ''.join(circle(414 + k * 16, 214, 3.6, fill=NAVY) for k in range(3))
    o += rect(392, 330, 64, 8, fill=HALDE_D, rx=3) + rect(420, 338, 8, 98, fill=HALDE_D) + pflanze(424, 330, s=1.0)
    return svg(W, H, rahmen_bogen(o, 'kt'))


def kosten():
    Y, s = 436, 1.1
    o = rect(120, 118, 66, 84, fill=WEISS, rx=2) + rect(126, 124, 54, 72, fill=SALBEI_M) + path('M126 196 L150 160 L180 196 Z', fill=SALBEI_D)
    o += rect(204, 136, 52, 52, fill=WEISS, rx=2) + rect(210, 142, 40, 40, fill=SONNE)
    o += pflanze(520, 392, s=1.6)
    o += sofa(150, 476, Y, color=SALBEI_D, s=s)
    a = sitzend(SENIOR_B, 214, Y, facing=1, s=s, arme=('schoss', 'schoss_v'), expr='laecheln', tilt=4)
    b = sitzend(HELFERIN, 412, Y, facing=-1, s=s, arme=('schoss', 'buch_v'), expr='reden', tilt=-3)
    o += zeichne(a) + zeichne(b, ohne=('arm_v',)) + mappe(352, Y - 160, s=1.1, color=BLUE, ang=10) + b['arm_v']
    o += couchtisch(318, Y + 6, w=150, h=44) + tasse(286, Y - 41, s=0.9) + tasse(336, Y - 41, s=0.9, henkel=-1)
    return svg(W, H, rahmen_bogen(o, 'ko'))


def fragen():
    Y, s = 436, 1.1
    o = path('M40 300 C180 260 400 270 600 296 L600 470 L40 470 Z', fill=SALBEI_M)
    o += baum(134, 330, h=210) + baum(512, 326, h=170)
    o += bank(320, Y, w=260, s=1.1, color=HALDE_D)
    a = sitzend(SENIORIN, 232, Y, facing=1, s=s, sh=53, arme=('schoss', 'reden_v'), expr='reden', tilt=-2, lean=4)
    b = sitzend(HELFER, 408, Y, facing=-1, s=s, sh=53, arme=('schoss', 'reden_v'), expr='laecheln', tilt=-3)
    o += zeichne(a) + zeichne(b)
    o += sprechblase(222, 118, 74, 66, schwanz=1) + fragezeichen(222, 112, s=1.5, color=ROST)
    o += sprechblase(420, 112, 74, 66, schwanz=-1) + haken(420, 112, s=1.6, color=NAVY)
    return svg(W, H, rahmen_bogen(o, 'fr', wand=SAND, boden=SAND_D, boden_y=440))


def mitarbeiten():
    Y, s = 436, 1.1
    T = Y - 140 * s
    o = fenster(240, 84, 160, 120, huegel_aussicht(240, 84, 160, 120))
    o += uhr(478, 140, r=20)
    o += stuhl_seite(176, Y, facing=1, s=s, lehne=96) + stuhl_seite(464, Y, facing=-1, s=s, lehne=96)
    a = sitzend(SENIOR, 176, Y, facing=1, s=s, arme=('tisch', 'spiel_v'), expr='lachen', lean=6)
    b = sitzend(HELFER, 464, Y, facing=-1, s=s, arme=('tisch', 'tisch_v'), expr='lachen', lean=6)
    o += zeichne(a, ohne=('arm_v',)) + zeichne(b, ohne=('arm_v',))
    o += rect(206, T, 228, 12, fill=HALDE_D, rx=4) + rect(216, T + 12, 208, 10, fill=HALDE)
    o += rect(240, T + 22, 10, Y - T - 22, fill=HALDE_D) + rect(390, T + 22, 10, Y - T - 22, fill=HALDE_D)
    # Spielbrett „Mensch ärgere Dich nicht“, leicht schräg von vorn
    y0, y1 = T - 1, T - 26
    o += path(f'M256 {y0} L384 {y0} L370 {y1} L270 {y1} Z', fill=CREME)
    o += path(f'M256 {y0} L384 {y0} L384 {y0 + 3} L256 {y0 + 3} Z', fill=HALDE_D)
    for (xa, xb, ya, yb, c) in ((262, 286, y0 - 2, y0 - 9, ROST), (354, 378, y0 - 2, y0 - 9, BLUE), (273, 293, y1 + 8, y1 + 2, SALBEI_DD), (347, 367, y1 + 8, y1 + 2, SONNE)):
        o += path(f'M{xa} {ya} L{xb} {ya} L{xb - 2} {yb} L{xa + 2} {yb} Z', fill=c)
    o += path(f'M296 {y0 - 13} H344 M320 {y0 - 3} V{y1 + 3}', stroke=HALDE_D, w=5)
    o += path(f'M298 {y0 - 13} H342', stroke=CREME, w=1.4, extra='stroke-dasharray="1 5"')
    # Spielfiguren und Würfel
    for (x, c) in ((300, ROST), (334, BLUE)):
        o += path(f'M{x - 6} {y0 - 12} Q{x} {y0 - 30} {x + 6} {y0 - 12} Z', fill=c) + circle(x, y0 - 30, 5, fill=c)
    o += rect(392, T - 15, 15, 15, fill=WEISS, rx=3) + circle(396.5, T - 10.5, 1.4, fill=NAVY) + circle(402.5, T - 4.5, 1.4, fill=NAVY) + circle(399.5, T - 7.5, 1.4, fill=NAVY)
    o += a['arm_v'] + b['arm_v']
    return svg(W, H, rahmen_bogen(o, 'mi'))


def ueber():
    o = circle(452, 118, 40, fill=SONNE)
    o += path('M40 300 C150 300 210 210 300 190 C360 178 420 236 480 268 C530 292 570 300 600 300 L600 470 L40 470 Z', fill=SALBEI_D)
    o += tetraeder(304, 192, 88, color=NAVY, w=2.6)
    o += foerderturm(470, 330, h=120, color=NAVY, w=2.6)
    o += path('M40 334 C200 312 420 316 600 330 L600 470 L40 470 Z', fill=SALBEI_M)
    o += zechenhaus(150, 412, w=96, h=72) + zechenhaus(256, 414, w=96, h=72, dach=BLUE) + zechenhaus(362, 412, w=96, h=72)
    o += baum(456, 412, h=110) + baum(530, 414, h=90)
    o += rect(40, 412, 560, 60, fill=SAND_D)
    return svg(W, H, rahmen_bogen(o, 'ue', wand=SAND, boden=SAND_D, boden_y=470))


def danke():
    Y, s = 436, 1.15
    T = Y - 140 * s
    o = fenster(120, 100, 120, 130, huegel_aussicht(120, 100, 120, 130))
    o += pflanze(180, 236, s=0.8)
    o += stuhl_seite(452, Y, facing=-1, s=s, lehne=96)
    a = sitzend(HELFERIN, 452, Y, facing=-1, s=s, arme=('tisch', 'tisch_v'), expr='lachen', lean=6, tilt=-4)
    o += zeichne(a, ohne=('arm_v',))
    o += rect(222, T, 200, 12, fill=HALDE_D, rx=4) + rect(236, T + 12, 10, Y - T - 12, fill=HALDE_D) + rect(398, T + 12, 10, Y - T - 12, fill=HALDE_D)
    o += laptop(346, T, s=1.2, facing=1) + tasse(258, T, s=1.0, inhalt=True)
    o += a['arm_v']
    # ankommender Brief
    o += path('M260 150 C300 110 340 120 360 170', stroke=SONNE, w=2.4, extra='stroke-dasharray="2 9"')
    o += brief(380, 186, w=48, h=34, color=WEISS, ang=-10, siegel=True)
    return svg(W, H, rahmen_bogen(o, 'da'))


def fehler404():
    o = path('M40 300 C190 266 410 270 600 296 L600 470 L40 470 Z', fill=SALBEI_M)
    o += circle(450, 120, 34, fill=SONNE)
    o += tetraeder(170, 300, 60, color=NAVY, w=2)
    o += path('M200 470 C260 400 300 360 330 330 C350 312 390 304 470 300', stroke=SAND, w=34)
    o += path('M200 470 C260 400 300 360 330 330 C350 312 390 304 470 300', stroke=CREME, w=22)
    o += wegweiser(330, 440, h=230, s=1.0)
    o += baum(520, 360, h=150)
    return svg(W, H, rahmen_bogen(o, 'fe', wand=SAND, boden=SALBEI_M, boden_y=470))


def besuch():
    HB = 400
    Y, s = 388, 1.1
    o = ziegelwand(0, 0, W, 470, color='#b9603f', fuge='#a14f33', reihe=18, stein=46)
    # Fenster
    o += rect(90, 110, 104, 120, fill=WEISS, rx=3) + rect(98, 118, 88, 104, fill=SALBEI) + rect(139, 118, 6, 104, fill=WEISS)
    o += rect(84, 230, 116, 10, fill=HALDE, rx=2)
    o += ''.join(circle(104 + k * 22, 226, 8, fill=(SONNE if k % 2 else ROST)) for k in range(5))
    # Tür offen
    o += rect(300, 116, 128, Y - 116, fill=NAVY_D) + rect(292, 104, 144, 14, fill=SAND, rx=2)
    o += path(f'M300 118 L272 130 L272 {Y + 6} L300 {Y}', fill=BLUE)
    o += rect(446, 210, 36, 46, fill=SAND, rx=3) + circle(464, 226, 5, fill=SONNE) + rect(452, 240, 24, 8, fill=NAVY, rx=2)
    o += rect(278, Y, 172, 10, fill=HALDE_D, rx=2)
    o += rect(306, Y - 4, 110, 6, fill=ROST, rx=2)
    a = stehend(SENIORIN, 356, Y, facing=1, s=s, arme=('haengen', 'tuer_v'), expr='lachen')
    o += zeichne(a)
    b = stehend(HELFER, 500, Y + 2, facing=-1, s=s, arme=('tasche', 'winken_v'), expr='lachen')
    o += zeichne(b, ohne=('arm_v',)) + handtasche(510, Y - 128, s=1.2, color=SALBEI_D) + b['arm_v']
    o += pflanze(244, Y, s=1.4) + pflanze(560, Y, s=1.2)
    d = bogen_pfad(56, 584, Y + 10, 10)
    body = f'<clipPath id="be"><path d="{d}"/></clipPath><g clip-path="url(#be)">' + o + '</g>'
    body += rect(30, Y + 8.5, 580, 3, fill=NAVY, rx=1.5)
    return svg(W, HB, body)


ALLE = {'hero-kueche': hero, 'spot-gesellschaft': spot_gesellschaft, 'spot-begleitung': spot_begleitung, 'spot-haushalt': spot_haushalt,
        'spot-ordnen': spot_ordnen, 'spot-angehoerige': spot_angehoerige, 'kontakt-telefon': kontakt, 'kosten-sofa': kosten,
        'fragen-bank': fragen, 'jobs-spiel': mitarbeiten, 'ueber-bottrop': ueber, 'danke-brief': danke, 'wegweiser': fehler404,
        'besuch-tuer': besuch}

if __name__ == '__main__':
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else 'out'
    os.makedirs(out, exist_ok=True)
    for name, fn in ALLE.items():
        open(os.path.join(out, name + '.svg'), 'w').write(fn())
        print(name)
