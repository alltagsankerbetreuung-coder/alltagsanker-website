import math
import sys
from kit import *
# Ortsmitten (Breite, Länge), gerundet
ORTE = {
    'bottrop': (51.5236, 6.9285), 'kirchhellen': (51.6050, 6.9210), 'gladbeck': (51.5703, 6.9856),
    'gelsenkirchen': (51.5177, 7.0857), 'essen': (51.4556, 7.0116), 'oberhausen': (51.4696, 6.8514),
    'dinslaken': (51.5623, 6.7434), 'dorsten': (51.6604, 6.9646)}
CX, CY, R = 270, 270, 230   # 20 km = 230 px
KM = R / 20.0
lat0, lon0 = ORTE['bottrop']
def pos(lat, lon):
    dy = (lat - lat0) * 111.2
    dx = (lon - lon0) * 111.32 * math.cos(math.radians(lat0))
    return CX + dx * KM, CY - dy * KM, math.hypot(dx, dy)
P_ = {k: pos(*v) for k, v in ORTE.items()}
o = circle(CX, CY, R, fill=SALBEI)
o += circle(CX, CY, R, stroke=NAVY, w=2, extra='stroke-dasharray="9 8"')
# Radius nach Süden
o += path(f'M{CX} {CY + 16} V{CY + R}', stroke=NAVY, w=1.6)
o += path(f'M{CX - 7} {CY + R - 9} L{CX} {CY + R} L{CX + 7} {CY + R - 9}', stroke=NAVY, w=1.6)
for k, (x, y, d) in P_.items():
    if k == 'bottrop':
        continue
    o += circle(x, y, 6, fill=WEISS, stroke=NAVY, w=3)
x, y, _ = P_['bottrop']
o += circle(x, y, 13, fill=NAVY) + circle(x, y, 5, fill=SONNE)
ziel = sys.argv[1] if len(sys.argv) > 1 else 'karte.svg'
open(ziel, 'w').write(svg(600, 540, o))
for k, (x, y, d) in P_.items():
    print(f'{k:14s} x={x:6.1f} y={y:6.1f}  {x/600*100:5.1f}% {y/540*100:5.1f}%  {d:4.1f} km')
