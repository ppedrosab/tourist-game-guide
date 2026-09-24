#!/usr/bin/env python3
"""
Fondos de la ruta de Semana Santa de Cádiz («Sobre los hombros de Cádiz»). Reutiliza San Juan de
Dios y la Catedral; aquí van Santa María, la Merced, La Palma, San Agustín, la Candelaria y el
Palillero. Con respeto: se ven pasos de palio, cirios y nazarenos, nunca imágenes sagradas.

Uso: python3 scripts/art/cadiz_ssanta_scenes.py && python3 scripts/art/render_layers.py cadiz_santamaria (etc.)
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, tree, columns, far_city, fx, doc)
from cadiz_gastro_scenes import church

VIOLET = "#6E2C5E"
BURGUNDY = "#6B1F2A"
VELVET = "#3D1E3A"
NAVY = "#1E2A4A"
# Fachadas de noche (color, sombra, luz)
WHITE_N = ("#8C92AC", "#707792", "#A6ABC2")
YELLOW_N = ("#9C8E7C", "#7F7364", "#B3A48F")
PINK_N = ("#977C88", "#7A6370", "#AD93A0")
STONE_N = ("#958C8A", "#77706F", "#ADA4A0")
FLOOR_N = "#5C5566"; FLOORL_N = "#4D4757"


# ---------------------------------------------------------------------------
# Piezas
# ---------------------------------------------------------------------------
def night_sky(p, moon=(300, 90), seed=3):
    """Cielo de noche con la luna llena de Pascua (la Semana Santa se fija por ella)."""
    mx, my = moon
    rnd = random.Random(seed)
    stars = "".join(f'<circle cx="{rnd.randint(4, W - 4)}" cy="{rnd.randint(6, 300)}" r="{rnd.choice((.8, 1, 1.3))}" fill="#FFF6E0" opacity="{rnd.choice((.5, .7, .9))}"/>' for _ in range(46))
    return (f'<g id="sky"><defs><linearGradient id="{p}night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141C36"/>'
            f'<stop offset=".5" stop-color="{NAVY}"/><stop offset=".8" stop-color="#3B3F66"/><stop offset="1" stop-color="#5B4E6E"/></linearGradient>'
            f'<radialGradient id="{p}moon"><stop offset="0" stop-color="#FFF4D6" stop-opacity=".55"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></radialGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}night)"/>{stars}'
            f'<circle cx="{mx}" cy="{my}" r="70" fill="url(#{p}moon)"/><circle cx="{mx}" cy="{my}" r="24" fill="#FFF3D2"/>'
            f'<circle cx="{mx - 7}" cy="{my - 4}" r="5" fill="#EDDDB6" opacity=".7"/><circle cx="{mx + 8}" cy="{my + 7}" r="3.5" fill="#EDDDB6" opacity=".7"/></g>')


def night_fx(p, ground_y=420):
    """Viñeta de noche: sin rayos de sol, bordes oscuros."""
    return (f'<g id="fx"><defs><radialGradient id="{p}fxn" cx=".5" cy=".45" r=".72"><stop offset=".45" stop-color="#0E1224" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#0E1224" stop-opacity=".5"/></radialGradient></defs>'
            f'<rect x="0" y="{ground_y - 8}" width="{W}" height="16" fill="#0E1224" opacity=".08"/>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}fxn)"/></g>')


def glow(p, key, x, y, r, op=.6):
    return (f'<defs><radialGradient id="{p}{key}"><stop offset="0" stop-color="#FFD98A" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="url(#{p}{key})"/>')


def cirio(x, top, h, s=1.0):
    """Vela encendida (cirio)."""
    return (f'<path d="M{f(x - 1.6 * s)} {f(top + h)}V{f(top)}H{f(x + 1.6 * s)}V{f(top + h)}Z" fill="#FFF6E2" stroke="{INK}" stroke-width="{f(.5 * s)}"/>'
            f'<path d="M{f(x)} {f(top - 1)}Q{f(x - 2 * s)} {f(top - 4 * s)} {f(x)} {f(top - 7 * s)}Q{f(x + 2 * s)} {f(top - 4 * s)} {f(x)} {f(top - 1)}Z" fill="{GOLD}"/>')


def nazareno(x, y, s=1.0, robe=VIOLET, hood=None, candle=True, lit_candle=True, cincture=PAPER):
    """Nazareno con túnica y capirote; lleva un cirio. Anónimo: solo se ven los ojos."""
    hood = hood or robe
    out = f'<ellipse cx="{f(x)}" cy="{f(y + 1)}" rx="{f(8 * s)}" ry="{f(2 * s)}" fill="#1A1420" opacity=".25"/>'
    # túnica
    out += f'<path d="M{f(x - 7 * s)} {f(y)}L{f(x - 4.5 * s)} {f(y - 26 * s)}L{f(x + 4.5 * s)} {f(y - 26 * s)}L{f(x + 7 * s)} {f(y)}Z" fill="{robe}" stroke="{INK}" stroke-width="{f(.8 * s)}"/>'
    out += f'<path d="M{f(x - 5 * s)} {f(y - 16 * s)}H{f(x + 5 * s)}" stroke="{cincture}" stroke-width="{f(1.4 * s)}"/>'
    # capirote (antifaz sobre el cono)
    out += f'<path d="M{f(x - 5.5 * s)} {f(y - 24 * s)}L{f(x)} {f(y - 50 * s)}L{f(x + 5.5 * s)} {f(y - 24 * s)}Z" fill="{hood}" stroke="{INK}" stroke-width="{f(.8 * s)}"/>'
    out += f'<circle cx="{f(x - 1.7 * s)}" cy="{f(y - 29 * s)}" r="{f(.9 * s)}" fill="{INK}"/><circle cx="{f(x + 1.7 * s)}" cy="{f(y - 29 * s)}" r="{f(.9 * s)}" fill="{INK}"/>'
    if candle:
        cx = x + 6 * s
        if lit_candle:
            out += cirio(cx, y - 34 * s, 22 * s, s)
        else:
            out += f'<path d="M{f(cx - 1.6 * s)} {f(y - 12 * s)}V{f(y - 34 * s)}H{f(cx + 1.6 * s)}V{f(y - 12 * s)}Z" fill="#FFF6E2" stroke="{INK}" stroke-width="{f(.5 * s)}"/>'
        out += f'<circle cx="{f(cx)}" cy="{f(y - 18 * s)}" r="{f(1.8 * s)}" fill="{robe}" stroke="{INK}" stroke-width="{f(.5 * s)}"/>'
    return out


def colgadura(x, y, w, h, c=BURGUNDY):
    """Colgadura de damasco que se cuelga del balcón en Semana Santa."""
    return (f'<path d="M{f(x)} {f(y)}H{f(x + w)}V{f(y + h)}L{f(x + w / 2)} {f(y + h + 8)}L{f(x)} {f(y + h)}Z" fill="{c}" stroke="{INK}" stroke-width="1.1"/>'
            f'<path d="M{f(x + 3)} {f(y + 3)}H{f(x + w - 3)}V{f(y + h - 1)}L{f(x + w / 2)} {f(y + h + 5)}L{f(x + 3)} {f(y + h - 1)}Z" fill="none" stroke="{GOLD}" stroke-width=".9"/>'
            f'<path d="M{f(x + w / 2)} {f(y + h * .3)}V{f(y + h * .75)}M{f(x + w / 2 - 4)} {f(y + h * .45)}H{f(x + w / 2 + 4)}" stroke="{GOLD}" stroke-width="1.1"/>')


def palio(p, x, base, w=96, h=230, night=True):
    """Paso de palio visto de frente: faldón, candelería, varales y techo con bambalinas.
    Bajo el techo solo se ve la luz de las velas: no se dibuja la imagen."""
    x0, x1 = x - w / 2, x + w / 2
    plat = base - 58
    top = base - h
    s = glow(p, "pg", x, plat - 60, w * 1.1, .55 if night else .3)
    # faldón con los pies de los cargadores asomando
    s += "".join(f'<path d="M{f(x0 + 8 + i * (w - 16) / 5)} {f(base)}h7v-5h-5Z" fill="#20202A"/>' for i in range(6))
    s += f'<path d="M{f(x0)} {f(base - 4)}V{f(plat)}H{f(x1)}V{f(base - 4)}Z" fill="{VELVET}" stroke="{INK}" stroke-width="1.8"/>'
    s += f'<path d="M{f(x0 + 5)} {f(base - 8)}V{f(plat + 6)}H{f(x1 - 5)}V{f(base - 8)}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
    s += "".join(f'<path d="M{f(x0 + 12 + i * (w - 24) / 4)} {f(plat + 16)}q6 8 0 16q-6 8 0 16" fill="none" stroke="{GOLD}" stroke-width="1.1"/>' for i in range(5))
    s += f'<path d="M{f(x0 - 4)} {f(plat)}H{f(x1 + 4)}V{f(plat - 8)}H{f(x0 - 4)}Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.5"/>'
    # varales
    for vx in (x0 + 2, x0 + w * .3, x1 - w * .3, x1 - 2):
        s += f'<path d="M{f(vx)} {f(plat - 8)}V{f(top + 24)}" stroke="{GOLD}" stroke-width="2.6"/><path d="M{f(vx)} {f(plat - 8)}V{f(top + 24)}" stroke="#B9822A" stroke-width="1" opacity=".7"/>'
    # candelería en gradas (más altas atrás)
    for row, (n, hh, yy) in enumerate([(9, 30, plat - 36), (7, 40, plat - 48), (5, 50, plat - 60)]):
        span = w * (.8 - row * .14)
        s += "".join(cirio(x - span / 2 + i * span / (n - 1), yy - hh + 30, hh, 1.05) for i in range(n))
    # jarras de flores blancas en las esquinas
    for jx in (x0 + 10, x1 - 10):
        s += f'<path d="M{f(jx - 5)} {f(plat - 8)}L{f(jx - 7)} {f(plat - 20)}H{f(jx + 7)}L{f(jx + 5)} {f(plat - 8)}Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
        s += "".join(f'<circle cx="{f(jx + dx)}" cy="{f(plat - 24 + dy)}" r="3.4" fill="#FFFDF6" stroke="{INK}" stroke-width=".6"/>' for dx, dy in [(-5, 0), (5, 0), (0, -5), (-3, -9), (3, -9), (0, 2)])
    # techo de palio con bambalinas y flecos
    s += f'<path d="M{f(x0 - 8)} {f(top + 24)}H{f(x1 + 8)}V{f(top)}H{f(x0 - 8)}Z" fill="{BURGUNDY}" stroke="{INK}" stroke-width="1.8"/>'
    s += "".join(f'<path d="M{f(x0 - 8 + i * (w + 16) / 8)} {f(top + 24)}q{f((w + 16) / 16)} 12 {f((w + 16) / 8)} 0" fill="{BURGUNDY}" stroke="{INK}" stroke-width="1.2"/>' for i in range(8))
    s += "".join(f'<path d="M{f(x0 - 8 + i * (w + 16) / 8 + (w + 16) / 16)} {f(top + 30)}v8" stroke="{GOLD}" stroke-width="1.4"/>' for i in range(8))
    s += f'<path d="M{f(x0 - 4)} {f(top + 6)}H{f(x1 + 4)}M{f(x0 - 4)} {f(top + 18)}H{f(x1 + 4)}" stroke="{GOLD}" stroke-width="1.2"/>'
    s += "".join(f'<circle cx="{f(x0 + i * w / 6)}" cy="{f(top + 12)}" r="2" fill="{GOLD}"/>' for i in range(7))
    s += f'<path d="M{f(x0 - 10)} {f(top)}H{f(x1 + 10)}V{f(top - 5)}H{f(x0 - 10)}Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.3"/>'
    # capataz delante, con traje oscuro
    s += person(x - w * .62, base + 4, 1.4, "#26262E")
    return s


def crowd(xs, y, s=.9, night=False, seed=0):
    rnd = random.Random(seed)
    cols = ["#3A3548", "#433B52", "#2E3345", "#4A3A48"] if night else ["#34495E", VIOLET, CLAY, SEA, "#5B4A3A"]
    return "".join(person(x, y + rnd.randint(-3, 3), s * rnd.uniform(.9, 1.1), rnd.choice(cols), dress=rnd.random() < .45) for x in xs)


def dark_lamp(x, base, h=150):
    """Farola apagada (como en el Silencio)."""
    return lamp(x, base, h).replace("#FFE7A8", "#4A5068")


def night_floor(p, y0):
    return floor(p, y0, color=FLOOR_N, line=FLOORL_N).replace(f'fill="url(#{p}dots)"', 'fill="none"')


# ---------------------------------------------------------------------------
# Escenas
# ---------------------------------------------------------------------------
def santamaria():
    """Iglesia de Santa María, con su chapitel de azulejos, en el barrio de Santa María."""
    p = "csm"; sun = (310, 120)
    far = f'<g id="far">{far_city(270, 91, towers=4)}</g>'
    c, cd, cl = WHITE
    tx = 214
    # torre con chapitel de azulejo azul y blanco
    tower = (f'<path d="M{tx} 110H{tx + 50}V380H{tx}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M{tx + 36} 112H{tx + 50}V380H{tx + 36}Z" fill="{cd}" opacity=".6"/>'
             f'<path d="M{tx - 4} 110H{tx + 54}V102H{tx - 4}Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.5"/>'
             + window(tx + 17, 124, 16, 30, shutters=False, arch=True, sw=1.2)
             + f'<path d="M{tx + 2} 102L{tx + 25} 34L{tx + 48} 102Z" fill="#3E6FA0" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{f(tx + 25 - (102 - y) * .0 - (y - 34) * .34)} {y}H{f(tx + 25 + (y - 34) * .34)}" stroke="{PAPER}" stroke-width="1.4"/>' for y in range(46, 102, 10))
             + "".join(f'<path d="M{tx + 25} 34L{f(tx + 2 + k * 11.5)} 102" stroke="{PAPER}" stroke-width=".9" opacity=".8"/>' for k in range(1, 4))
             + f'<path d="M{tx + 25} 34V18M{tx + 20} 24H{tx + 30}" stroke="{INK}" stroke-width="1.6"/>')
    nave = (f'<path d="M96 180H{tx}V380H96Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M90 180L{(96 + tx) / 2} 156L{tx + 6} 180Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
            + columns(120, 250, 70, 130, 2, STONE, 1.3)
            + f'<path d="M136 380V300Q155 276 174 300V380Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.8"/>'
            f'<circle cx="155" cy="214" r="12" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.5"/><circle cx="155" cy="214" r="6" fill="{LIT}" stroke="{INK}" stroke-width="1.1"/>')
    houses = (house(-30, 220, 120, 160, PINK, floors=3, cols=2, lit={(1, 0)})
              + colgadura(10, 280, 22, 30) + house(270, 200, 150, 180, YELLOW, floors=3, cols=3)
              + colgadura(300, 256, 22, 30, VIOLET) + colgadura(348, 256, 22, 30))
    mid = f'<g id="mid">{nave}{tower}{houses}<rect x="-10" y="376" width="{W + 20}" height="50" fill="#DDBE98"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + crowd((60, 84, 300, 322, 346), 440, .95, seed=4)
            + nazareno(150, 452, 1.1, VIOLET, cincture=GOLD) + nazareno(196, 446, 1.0, VIOLET, cincture=GOLD) + nazareno(240, 452, 1.1, VIOLET, cincture=GOLD)
            + lamp(24, 540, 170) + "</g>")
    return doc(p, "Iglesia de Santa María", [sky(p, sun, [(80, 80, .8)], [(120, 60), (140, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def merced():
    """Plaza de la Merced: el antiguo convento, hoy centro de flamenco, y un balcón para la saeta."""
    p = "cme"; sun = (70, 150)
    far = f'<g id="far">{far_city(260, 93, towers=5)}</g>'
    conv = (church(150, 110, w=140, h=270, towers=1, col=STONE)
            + f'<path d="M186 250H254V262H186Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<path d="M{x} 256h8" stroke="{CLAY}" stroke-width="1.6"/>' for x in range(192, 248, 12)))
    # casa con el balcón de la saeta, con colgadura y macetas de geranios
    bal = (house(290, 170, 130, 210, WHITE, floors=3, cols=2, lit={(0, 0), (1, 0)})
           + f'<path d="M298 260H352V266H298Z" fill="{INK}"/>' + colgadura(306, 266, 36, 34)
           + "".join(f'<path d="M{x} 256h8l-1 6h-6Z" fill="#C9763F" stroke="{INK}" stroke-width=".8"/><circle cx="{x + 4}" cy="253" r="3.4" fill="{CLAY}"/><circle cx="{x + 1}" cy="255" r="2.2" fill="#4F8B5A"/>' for x in (300, 334)))
    left = house(-40, 200, 150, 180, MINT, floors=3, cols=2, lit={(1, 1)}) + colgadura(52, 262, 22, 28, VIOLET)
    mid = f'<g id="mid">{conv}{left}{bal}<rect x="-10" y="376" width="{W + 20}" height="50" fill="#DDBE98"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + crowd((40, 64, 90, 250, 274), 444, 1, seed=7)
            + "".join(f'<path d="M{x - 10} 470h20l-3 16h-14Z" fill="#C9763F" stroke="{INK}" stroke-width="1.2"/>'
                      f'<circle cx="{x - 4}" cy="464" r="6" fill="#4F8B5A" stroke="{INK}" stroke-width=".8"/><circle cx="{x + 5}" cy="462" r="7" fill="#4F8B5A" stroke="{INK}" stroke-width=".8"/>'
                      f'<circle cx="{x}" cy="456" r="4" fill="{CLAY}"/>' for x in (130, 350))
            + lamp(372, 540, 170) + palm(-6, 490, 240, 14, .95) + "</g>")
    return doc(p, "Plaza de la Merced", [sky(p, sun, [(280, 60, .8)], [(230, 40), (250, 30, .8)]), far, mid, near, fx(p, sun, 420, .35)])


def palma():
    """Calle de la Palma, en La Viña, con su iglesia al fondo."""
    p = "cpa"; sun = (200, 90)
    far = f'<g id="far">{far_city(270, 95, towers=2)}</g>'
    # iglesia de la Palma en el fondo de la calle, con espadaña
    c, cd, cl = YELLOW
    ch = (f'<rect x="-10" y="356" width="{W + 20}" height="70" fill="#DDBE98"/>'
          f'<path d="M150 190H240V360H150Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M222 192H240V360H222Z" fill="{cd}" opacity=".6"/>'
          f'<path d="M146 190Q195 150 244 190Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M178 160H212V130Q195 116 178 130Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.5"/>'
          f'<path d="M188 158V138Q195 131 202 138V158Z" fill="{WIN}"/><circle cx="195" cy="148" r="4" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>'
          f'<path d="M195 118V104M190 110H200" stroke="{INK}" stroke-width="1.5"/>'
          + columns(166, 250, 58, 110, 2, WHITE, 1.2)
          + f'<path d="M180 360V296Q195 280 210 296V360Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M184 222H206V240H184Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/><path d="M188 231q7 -6 14 0" fill="none" stroke="{SEA}" stroke-width="1.4"/>')
    # la calle, con casas en perspectiva a los lados
    sides = (house(-60, 150, 190, 250, PINK, floors=3, cols=2, lit={(1, 0)}) + colgadura(40, 222, 24, 32)
             + house(262, 150, 190, 250, MINT, floors=3, cols=2) + colgadura(290, 222, 24, 32, VIOLET)
             + "".join(f'<path d="M{x0} {y}H{x1}" stroke="{INK}" stroke-width="1.4"/><path d="M{x0} {y}L{x0} {y + 6}M{x1} {y}L{x1} {y + 6}" stroke="{INK}" stroke-width="1"/>' for x0, x1, y in [(130, 150, 176), (240, 262, 176)]))
    # banderitas de papel verdes y blancas cruzando la calle (La Viña se viste para su cofradía)
    flags = "".join(f'<path d="M{130 + i * 11} {182 + abs(i - 6) * -1.5 + 9}l5 10l5 -10Z" fill="{["#4F8B5A", PAPER][i % 2]}" stroke="{INK}" stroke-width=".6"/>' for i in range(12))
    mid = f'<g id="mid">{ch}{sides}<path d="M130 190Q195 205 262 190" fill="none" stroke="{INK}" stroke-width=".8"/>{flags}</g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + crowd((40, 66, 92, 290, 316, 346), 446, 1, seed=11)
            + nazareno(160, 460, 1.05, "#F4EEE2", hood="#4F8B5A", cincture="#4F8B5A") + nazareno(228, 460, 1.05, "#F4EEE2", hood="#4F8B5A", cincture="#4F8B5A")
            + "</g>")
    return doc(p, "Calle de la Palma", [sky(p, sun, [(90, 70, .8), (320, 110, .6)], [(300, 50), (320, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sanagustin():
    """San Agustín en la noche del Viernes Santo: farolas apagadas, solo cirios y silencio."""
    p = "csg"
    far = f'<g id="far">{far_city(250, 97, "#2E3552", "#363E5E", towers=4)}</g>'
    c, cd, cl = STONE_N
    fac = (f'<path d="M100 130H290V390H100Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M262 132H290V390H262Z" fill="{cd}" opacity=".6"/>'
           f'<path d="M92 130L195 92L298 130Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M195 104V86M189 92H201" stroke="{INK}" stroke-width="1.6"/>'
           + columns(130, 230, 130, 160, 4, STONE_N, 1.3)
           + f'<path d="M166 390V300Q195 270 224 300V390Z" fill="#2A1E1A" stroke="{INK}" stroke-width="1.8"/>'
           + glow(p, "dg", 195, 350, 50, .45)
           + f'<circle cx="195" cy="180" r="14" fill="{cl}" stroke="{INK}" stroke-width="1.5"/><circle cx="195" cy="180" r="7" fill="#6A5A3A" stroke="{INK}" stroke-width="1.1"/>')
    houses = (house(-40, 190, 140, 200, WHITE_N, floors=3, cols=2, lit={(0, 1)})
              + house(290, 170, 140, 220, YELLOW_N, floors=3, cols=2, lit={(1, 0)}))
    mid = f'<g id="mid">{fac}{houses}<rect x="-10" y="386" width="{W + 20}" height="40" fill="#4E4858"/></g>'
    # fila de nazarenos de negro, cada uno con su cirio encendido; la gente mira callada
    row = "".join(glow(p, f"n{i}", x + 6 * s, y - 36 * s, 22 * s, .5) + nazareno(x, y, s, "#1D1A22", cincture=PAPER)
                  for i, (x, y, s) in enumerate([(150, 432, .8), (190, 436, .85), (236, 442, .95), (170, 470, 1.15), (240, 486, 1.25)]))
    near = (f'<g id="near">{night_floor(p, 420)}'
            + crowd((30, 54, 78, 316, 340, 364), 448, 1, night=True, seed=13) + row
            + dark_lamp(22, 540, 170) + dark_lamp(368, 540, 170) + "</g>")
    return doc(p, "San Agustín, el Silencio", [night_sky(p, (80, 70), 5), far, mid, near, night_fx(p)])


def candelaria():
    """Plaza de la Candelaria en la Carrera Oficial: sillas en fila y los grandes árboles."""
    p = "cca"; sun = (320, 140)
    far = f'<g id="far">{far_city(250, 99, towers=6)}</g>'
    houses = (house(-30, 160, 130, 220, YELLOW, floors=3, cols=2, lit={(1, 1)}) + colgadura(22, 226, 22, 28)
              + house(100, 180, 110, 200, WHITE, floors=3, cols=2) + colgadura(140, 240, 22, 28, VIOLET)
              + house(210, 170, 120, 210, PINK, floors=3, cols=2, lit={(0, 0)})
              + house(330, 190, 100, 190, MINT, floors=3, cols=2))
    # monumento en el centro de la plaza (pedestal y figura en silueta)
    mon = (f'<path d="M180 380V330H210V380Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.5"/>'
           f'<path d="M176 330H214V322H176Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.3"/>'
           f'<path d="M188 322L190 296L200 296L202 322Z" fill="#6E7A72" stroke="{INK}" stroke-width="1.2"/><circle cx="195" cy="291" r="5" fill="#6E7A72" stroke="{INK}" stroke-width="1.2"/>')
    trees = tree(60, 390, 64) + tree(330, 390, 60)
    mid = f'<g id="mid">{houses}<rect x="-10" y="376" width="{W + 20}" height="50" fill="#DDBE98"/>{mon}{trees}</g>'
    # palcos y filas de sillas de la Carrera Oficial, con gente esperando
    chairs = "".join(f'<path d="M{x} 470v-16h10v16M{x} 462h10" fill="none" stroke="{CLAY}" stroke-width="2"/>' for x in range(20, 380, 20))
    rail = f'<path d="M0 450H{W}" stroke="{INK}" stroke-width="2.4"/>' + "".join(f'<path d="M{x} 450V474" stroke="{INK}" stroke-width="1.6"/>' for x in range(10, 390, 40))
    near = (f'<g id="near">{floor(p, 420)}{chairs}'
            + crowd(range(28, 380, 34), 452, 1, seed=17) + rail
            + lamp(372, 540, 170) + "</g>")
    return doc(p, "Plaza de la Candelaria", [sky(p, sun, [(90, 80, .8)], [(150, 60), (170, 50, .8)]), far, mid, near, fx(p, sun, 420, .35)])


def palillero():
    """Plaza del Palillero, final de la Carrera Oficial, de noche: pasa un palio entre cirios."""
    p = "cpl"
    far = f'<g id="far">{far_city(250, 101, "#2E3552", "#363E5E", towers=5)}</g>'
    houses = (house(-40, 170, 150, 230, YELLOW_N, floors=3, cols=2, lit={(0, 0), (1, 1)}) + colgadura(40, 238, 24, 30)
              + house(110, 190, 90, 210, WHITE_N, floors=3, cols=2, lit={(0, 1)})
              + house(200, 180, 90, 220, PINK_N, floors=3, cols=2, lit={(1, 0)}) + colgadura(222, 244, 22, 28, VIOLET)
              + house(290, 160, 140, 240, WHITE_N, floors=3, cols=2, lit={(0, 1), (1, 0)}))
    mid = (f'<g id="mid">{houses}<rect x="-10" y="396" width="{W + 20}" height="30" fill="#4E4858"/>'
           + palio(p, 195, 420, 104, 250) + "</g>")
    near = (f'<g id="near">{night_floor(p, 420)}'
            + crowd((20, 44, 346, 370), 450, 1.05, night=True, seed=19)
            + "".join(glow(p, f"q{i}", x + 6 * s, y - 36 * s, 22 * s, .5) + nazareno(x, y, s, VIOLET, cincture=GOLD)
                      for i, (x, y, s) in enumerate([(84, 466, 1.1), (300, 466, 1.1), (60, 510, 1.3), (324, 510, 1.3)]))
            + "</g>")
    return doc(p, "Plaza del Palillero", [night_sky(p, (310, 80), 9), far, mid, near, night_fx(p)])


SCENES = {"santamaria": santamaria, "merced": merced, "palma": palma, "sanagustin": sanagustin,
          "candelaria": candelaria, "palillero": palillero}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_cadiz_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos de Semana Santa generados:", ", ".join(SCENES))
