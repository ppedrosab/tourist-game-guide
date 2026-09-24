#!/usr/bin/env python3
"""
Fondos de Córdoba (viewBox 390×560, capas sky · far · mid|sea · near · fx).

Uso: python3 scripts/art/cordoba_scenes.py && python3 scripts/art/render_layers.py cordoba_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from granada_scenes import horseshoe, cypress
from sevilla_scenes import orange_tree, river

BRICK = "#B5553A"
OCHRE = ("#E3B96F", "#C99B50", "#F0CF92")
LIME = ("#F4EEE2", "#DCD2BF", "#FFFDF6")       # cal de la Judería
POTBLUE = "#2F6F9E"


# ---------------------------------------------------------------------------
# Piezas
# ---------------------------------------------------------------------------
def merlons(x0, x1, y, c=STONE[0], step=18, sw=1.2):
    """Almenas escalonadas, como las de la Mezquita."""
    return "".join(f'<path d="M{x} {y}V{y - 6}H{x + 3}V{y - 11}H{x + 9}V{y - 6}H{x + 12}V{y}Z" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>'
                   for x in range(int(x0), int(x1) - 11, step))


def battlements(x0, x1, y, c=STONE[0], step=16, sw=1.2):
    return "".join(f'<path d="M{x} {y}V{y - 10}H{x + 9}V{y}" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>' for x in range(int(x0), int(x1) - 8, step))


def voussoirs(cx, cy, ro, ri, n=11, sw=1):
    out = ""
    for k in range(n):
        a0, a1 = math.pi + k * math.pi / n, math.pi + (k + 1) * math.pi / n
        pts = [(cx + ro * math.cos(a0), cy + ro * math.sin(a0)), (cx + ro * math.cos(a1), cy + ro * math.sin(a1)),
               (cx + ri * math.cos(a1), cy + ri * math.sin(a1)), (cx + ri * math.cos(a0), cy + ri * math.sin(a0))]
        out += f'<path d="M{"L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}Z" fill="{BRICK if k % 2 == 0 else STONE[2]}" stroke="{INK}" stroke-width="{sw}"/>'
    return out


def bell_tower(x, base, s=1.0, soft=False):
    """Torre campanario de la Mezquita-Catedral: cuerpo de piedra, campanas y remate."""
    sw = 0 if soft else 1.6
    w = 44 * s
    c, cd, cl = STONE
    out = (f'<path d="M{f(x - w / 2)} {f(base)}V{f(base - 150 * s)}H{f(x + w / 2)}V{f(base)}Z" fill="{c}" stroke="{INK}" stroke-width="{sw}"/>'
           f'<path d="M{f(x + w * .2)} {f(base - 148 * s)}H{f(x + w / 2)}V{f(base)}H{f(x + w * .2)}Z" fill="{cd}" opacity=".6"/>')
    for k, (yy, ww) in enumerate([(150, 1.0), (190, .8), (222, .62)]):
        top = base - yy * s
        hh = (40 if k < 2 else 28) * s
        out += f'<path d="M{f(x - w * ww / 2)} {f(top)}V{f(top - hh)}H{f(x + w * ww / 2)}V{f(top)}Z" fill="{cl}" stroke="{INK}" stroke-width="{sw}"/>'
        out += f'<path d="M{f(x - w * ww / 2 - 3)} {f(top)}H{f(x + w * ww / 2 + 3)}" stroke="{INK if not soft else cd}" stroke-width="{f(2.4 * s)}"/>'
        if not soft:
            out += window(x - 5 * s, top - hh + 8 * s, 10 * s, hh - 14 * s, shutters=False, arch=True, sw=1)
    top = base - 250 * s
    out += f'<path d="M{f(x - 8 * s)} {f(top)}Q{f(x)} {f(top - 22 * s)} {f(x + 8 * s)} {f(top)}Z" fill="#B9822A" stroke="{INK}" stroke-width="{sw}"/>'
    out += f'<path d="M{f(x)} {f(top - 18 * s)}V{f(top - 30 * s)}" stroke="{INK}" stroke-width="{f(1.6 * s)}"/>'
    for yy in (80, 120):
        if not soft:
            out += window(x - 6 * s, base - yy * s, 12 * s, 18 * s, shutters=False, arch=True, sw=1)
    return out


def mezquita_far(y, x0=-10, x1=400, soft=True):
    """Silueta lejana de la Mezquita-Catedral: muros almenados, cubierta del crucero y torre."""
    c = "#E6C9A0"
    s = f'<path d="M{x0} {y}V{y - 40}H{x1}V{y}Z" fill="{c}"/>' + merlons(x0, x1, y - 40, c, 16, 0)
    s += f'<path d="M150 {y - 40}L170 {y - 90}H250L270 {y - 40}Z" fill="#DDBE94"/>'
    s += bell_tower(90, y - 30, .55, soft=True).replace(STONE[0], "#E0C398").replace(STONE[2], "#EBD3AC").replace(STONE[1], "#D2B284")
    return s


def flowerpots(x0, x1, y0, rows=3, cols_step=22, seed=0):
    """Macetas azules colgadas en la pared encalada, con geranios."""
    s = ""
    for r in range(rows):
        for i, x in enumerate(range(int(x0), int(x1), cols_step)):
            if (i + r + seed) % 3 == 2:
                continue
            y = y0 + r * 34
            s += (f'<path d="M{x - 6} {y}H{x + 6}L{x + 4} {y + 10}H{x - 4}Z" fill="{POTBLUE}" stroke="{INK}" stroke-width="1"/>'
                  f'<circle cx="{x - 3}" cy="{y - 3}" r="4" fill="#4F8B5A"/><circle cx="{x + 3}" cy="{y - 4}" r="4" fill="#3D6647"/>'
                  f'<circle cx="{x}" cy="{y - 7}" r="3.2" fill="{[CLAY, "#D8412F", "#E86A92"][(i + r) % 3]}"/>')
    return s


def lime_wall(x, y, w, h, stroke=1.8):
    c, cd, cl = LIME
    return (f'<path d="M{x} {y}H{x + w}V{y + h}H{x}Z" fill="{c}" stroke="{INK}" stroke-width="{stroke}"/>'
            f'<path d="M{x} {y + h - 18}H{x + w}V{y + h}H{x}Z" fill="#E8C872" opacity=".7"/>')


def noria(cx, cy, r):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="9"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8A6243" stroke-width="5"/>'
    for k in range(12):
        a = math.radians(k * 30)
        s += f'<path d="M{cx} {cy}L{f(cx + r * math.cos(a))} {f(cy + r * math.sin(a))}" stroke="#6E4C33" stroke-width="3"/>'
        s += f'<path d="M{f(cx + r * math.cos(a) - 5)} {f(cy + r * math.sin(a) - 4)}h10v8h-10Z" fill="#C9763F" stroke="{INK}" stroke-width="1"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="8" fill="#6E4C33" stroke="{INK}" stroke-width="2"/>'


def statue(x, base, s=1.0, c="#8C938A", horse=False, seated=False):
    """Estatua en silueta sobre pedestal (personajes civiles, sin rasgos)."""
    out = (f'<path d="M{f(x - 16 * s)} {f(base)}V{f(base - 50 * s)}H{f(x + 16 * s)}V{f(base)}Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.5"/>'
           f'<path d="M{f(x - 20 * s)} {f(base - 50 * s)}H{f(x + 20 * s)}V{f(base - 58 * s)}H{f(x - 20 * s)}Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>')
    top = base - 58 * s
    if horse:
        out += (f'<path d="M{f(x - 22 * s)} {f(top)}L{f(x - 18 * s)} {f(top - 24 * s)}Q{f(x)} {f(top - 30 * s)} {f(x + 16 * s)} {f(top - 26 * s)}L{f(x + 26 * s)} {f(top - 44 * s)}L{f(x + 30 * s)} {f(top - 38 * s)}L{f(x + 22 * s)} {f(top - 20 * s)}L{f(x + 20 * s)} {f(top)}H{f(x + 14 * s)}V{f(top - 14 * s)}H{f(x - 12 * s)}V{f(top)}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M{f(x - 4 * s)} {f(top - 26 * s)}V{f(top - 50 * s)}H{f(x + 6 * s)}V{f(top - 26 * s)}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                f'<circle cx="{f(x + s)}" cy="{f(top - 55 * s)}" r="{f(6 * s)}" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    elif seated:
        out += (f'<path d="M{f(x - 12 * s)} {f(top)}V{f(top - 16 * s)}H{f(x + 12 * s)}L{f(x + 14 * s)} {f(top)}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M{f(x - 10 * s)} {f(top - 16 * s)}L{f(x - 8 * s)} {f(top - 40 * s)}H{f(x + 8 * s)}L{f(x + 10 * s)} {f(top - 16 * s)}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                f'<circle cx="{x}" cy="{f(top - 47 * s)}" r="{f(7 * s)}" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    else:
        out += (f'<path d="M{f(x - 9 * s)} {f(top)}L{f(x - 8 * s)} {f(top - 44 * s)}H{f(x + 8 * s)}L{f(x + 9 * s)} {f(top)}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                f'<circle cx="{x}" cy="{f(top - 51 * s)}" r="{f(7 * s)}" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    return out


def ground(y, c="#DDBE98"):
    return f'<rect x="-10" y="{y}" width="{W + 20}" height="{428 - y}" fill="{c}"/>'


# ---------------------------------------------------------------------------
# Historia
# ---------------------------------------------------------------------------
def puente():
    p = "kpu"; sun = (310, 110)
    far = f'<g id="far">{far_city(270, 111, towers=2)}{mezquita_far(300)}</g>'
    c, cd, cl = STONE
    gate = (f'<path d="M110 390V180H280V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M250 182H280V390H250Z" fill="{cd}" opacity=".6"/>'
            f'<path d="M100 180H290V166H100Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M110 166L195 124L280 166Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M136 166L195 138L254 166Z" fill="none" stroke="{cd}" stroke-width="2"/>'
            + columns(126, 200, 138, 190, 4, STONE, 1.3)
            + f'<path d="M160 390V270Q195 222 230 270V390Z" fill="#5E4A3A" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M176 390V282Q195 258 214 282V390Z" fill="#8FB9B4" opacity=".6"/>'
            f'<path d="M150 214H240V226H150Z" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>')
    walls = (f'<path d="M-20 390V260H110V390Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>' + battlements(-20, 110, 260, STONE[1])
             + f'<path d="M280 390V250H410V390Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>' + battlements(280, 410, 250, STONE[1]))
    mid = f'<g id="mid">{walls}{gate}{ground(386, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D7C3A0", line="#C4AC86")}'
            + f'<path d="M0 440H80V470H0Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/><path d="M310 440H390V470H310Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
            + person(150, 448, 1, SEA) + person(176, 452, .95, CLAY, dress=True) + person(250, 446, .9, "#34495E")
            + lamp(40, 440, 150) + lamp(350, 440, 150) + "</g>")
    return doc(p, "Puerta del Puente", [sky(p, sun, [(80, 70, .8)], [(230, 60), (250, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def mezquita():
    p = "kmz"; sun = (320, 90)
    far = f'<g id="far">{far_city(250, 113, towers=1)}</g>'
    c, cd, cl = STONE
    wall = (f'<path d="M-20 400V190H410V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + merlons(-20, 410, 190, c, 18)
            + "".join(f'<path d="M{x} 400V300" stroke="{INK}" stroke-width="10"/><path d="M{x} 400V300" stroke="#9A8A76" stroke-width="7"/>' for x in range(20, 400, 64))
            + "".join(voussoirs(x + 32, 300, 30, 20, 11) + f'<path d="M{x + 4} 400V300Q{x + 32} 276 {x + 60} 300V400Z" fill="#6E5140" opacity=".85"/>' for x in range(20, 360, 64))
            + "".join(f'<path d="M{x} 240H{x + 30}V270H{x}Z" fill="none" stroke="{cd}" stroke-width="2"/>' for x in range(36, 380, 64)))
    tower = bell_tower(330, 330, 1.1)
    mid = f'<g id="mid">{wall}{tower}{ground(396, "#E4CBA4")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E1C49A", line="#CDAF84")}'
            + orange_tree(40, 470, 34) + orange_tree(150, 450, 26) + orange_tree(250, 452, 26) + orange_tree(350, 470, 34)
            + "".join(f'<path d="M{x} 470L{x + 20} 560" stroke="#8FB9B4" stroke-width="4" opacity=".7"/>' for x in (90, 290))
            + person(196, 452, .95, SEA) + person(214, 456, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Patio de los Naranjos", [sky(p, sun, [(80, 60, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sinagoga():
    p = "ksi"; sun = (200, 80)
    far = f'<g id="far">{far_city(240, 115, towers=2)}</g>'
    left = lime_wall(-20, 160, 150, 250) + flowerpots(0, 120, 190, 3) + window(40, 300, 22, 40, shutters=False, balcony=False)
    right = lime_wall(260, 150, 150, 260) + flowerpots(270, 390, 180, 3, seed=1)
    # fachada de la sinagoga al fondo de la calle
    syn = (lime_wall(130, 210, 130, 190)
           + f'<path d="M180 400V330Q195 314 210 330V400Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.8"/>'
           + f'<path d="M168 262H222V300H168Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
           + "".join(f'<path d="M172 {270 + k * 8}H218" stroke="#8A7A62" stroke-width="1.2"/>' for k in range(4))
           + f'<path d="M126 210H264V200H126Z" fill="{LIME[2]}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{syn}{left}{right}{ground(400, "#D8C6A6")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D5C29E", line="#C1AB85")}'
            + f'<path d="M0 420L120 420L60 560L0 560Z" fill="#CDB896" opacity=".6"/>'
            + person(170, 446, .9, "#6E2C5E", dress=True) + person(226, 450, .95, SEA)
            + "".join(f'<path d="M{x - 10} 470h20l-3 16h-14Z" fill="{POTBLUE}" stroke="{INK}" stroke-width="1.2"/><circle cx="{x}" cy="462" r="7" fill="#4F8B5A"/><circle cx="{x + 3}" cy="456" r="4" fill="{CLAY}"/>' for x in (40, 350))
            + "</g>")
    return doc(p, "Calle Judíos", [sky(p, sun, [(300, 70, .8)], [(90, 60), (110, 50, .8)]), far, mid, near, fx(p, sun, 420, .25)])


def almodovar():
    p = "kal"; sun = (90, 110)
    far = f'<g id="far">{far_city(260, 117, towers=3)}</g>'
    c, cd, cl = OCHRE
    wall = (f'<path d="M-20 390V240H410V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(-20, 410, 240, c)
            + "".join(f'<path d="M-20 {y}H410" stroke="{cd}" stroke-width="1" opacity=".6"/>' for y in range(256, 390, 14))
            + f'<path d="M140 390V170H250V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(140, 250, 170, cl)
            + f'<path d="M226 172H250V390H226Z" fill="{cd}" opacity=".6"/>'
            + horseshoe(165, 290, 60, 100, "#5E4232", 1.8)
            + f'<path d="M150 230H240V240H150Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{wall}<rect x="-10" y="384" width="{W + 20}" height="44" fill="#8FB9B4"/>{ground(404, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + cypress(30, 470, 180, 16) + cypress(360, 470, 170, 15)
            + statue(300, 470, 1.1, seated=True)
            + person(110, 446, .95, SEA) + person(134, 450, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Puerta de Almodóvar", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def albolafia():
    p = "kab"; sun = (300, 120)
    far = f'<g id="far">{mezquita_far(290)}</g>'
    sea = f'<g id="sea">{river(p, 300, 430)}</g>'
    c, cd, cl = OCHRE
    mill = (f'<path d="M10 400V280H150V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(10, 150, 280, c)
            + horseshoe(40, 330, 28, 70, "#4A3A2E", 1.4) + horseshoe(90, 330, 28, 70, "#4A3A2E", 1.4)
            + noria(230, 300, 90)
            + f'<path d="M150 300H230" stroke="{INK}" stroke-width="6"/><path d="M150 300H230" stroke="{cl}" stroke-width="3"/>')
    mid = f'<g id="mid">{mill}</g>'
    near = (f'<g id="near"><path d="M-10 440Q200 420 400 450V570H-10Z" fill="#8FAF6E"/><path d="M-10 460Q200 444 400 470V570H-10Z" fill="#7C9C5E"/>'
            + "".join(f'<path d="M{x} 450q-4 -18 2 -30M{x + 4} 450q2 -20 8 -26" fill="none" stroke="#4E7A4A" stroke-width="2"/>' for x in (40, 90, 300, 350))
            + person(180, 480, 1.1, SEA) + person(206, 484, 1.05, CLAY, dress=True) + bench(260, 480) + "</g>")
    return doc(p, "Molino de la Albolafia", [sky(p, sun, [(80, 80, .8)], [(150, 60), (170, 50, .8)]), far, sea, mid, near, fx(p, sun, 430, .25)])


def alcazar():
    p = "kaz"; sun = (80, 100)
    far = f'<g id="far">{far_city(260, 119, towers=2)}</g>'
    c, cd, cl = OCHRE
    fort = (f'<path d="M20 380V220H370V380Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(20, 370, 220, c)
            + f'<path d="M40 380V150H110V380Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(40, 110, 150, cl, 14)
            + f'<path d="M90 152H110V380H90Z" fill="{cd}" opacity=".6"/>'
            + f'<path d="M290 380V160Q325 144 360 160V380Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(290, 360, 160, cl, 14)
            + window(66, 190, 16, 26, shutters=False, arch=True, sw=1.2) + window(318, 200, 16, 26, shutters=False, arch=True, sw=1.2)
            + f'<path d="M180 380V300Q200 280 220 300V380Z" fill="#5E4232" stroke="{INK}" stroke-width="1.6"/>')
    mid = f'<g id="mid">{fort}{ground(376, "#CFB48A")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C8A2", line="#C4AE88")}'
            + f'<path d="M110 440H280V520H110Z" fill="#8FB9B4" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x} 470q6 -3 12 0" fill="none" stroke="#E6F2EF" stroke-width="1.6"/>' for x in (140, 190, 240))
            + "".join(f'<path d="M{x} 440V420" stroke="#E6F2EF" stroke-width="2.4" opacity=".8"/>' for x in (150, 195, 240))
            + cypress(70, 470, 150, 13) + cypress(320, 470, 150, 13) + cypress(20, 500, 190, 16) + cypress(372, 500, 190, 16)
            + person(196, 434, .9, SEA) + "</g>")
    return doc(p, "Alcázar de los Reyes Cristianos", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def camposanto():
    p = "kcs"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 121, towers=3)}</g>'
    c, cd, cl = OCHRE
    left = (f'<path d="M-20 390V220H140V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(-20, 140, 220, c)
            + f'<path d="M60 390V170H120V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(60, 120, 170, cl, 14))
    right = house(250, 200, 160, 190, WHITE, floors=3, cols=3, lit={(1, 2)})
    column = (f'<path d="M186 390V360H214V390Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M194 360V230H206V360Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M188 230H212V220H188Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{left}{right}{column}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + tree(40, 470, 44) + tree(350, 470, 46)
            + bench(110, 470) + bench(230, 470) + person(180, 446, .95, SEA) + person(160, 450, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Campo Santo de los Mártires", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def calahorra():
    p = "kcl"; sun = (90, 120)
    far = f'<g id="far">{mezquita_far(300)}</g>'
    sea = f'<g id="sea">{river(p, 300, 420)}</g>'
    c, cd, cl = OCHRE
    tower = (f'<path d="M110 400V170H170V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(110, 170, 170, c, 12)
             + f'<path d="M220 400V170H280V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(220, 280, 170, c, 12)
             + f'<path d="M170 400V220H220V400Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(170, 220, 220, cl, 12)
             + f'<path d="M180 400V330Q195 312 210 330V400Z" fill="#5E4232" stroke="{INK}" stroke-width="1.6"/>'
             + f'<path d="M154 172H170V400H154Z" fill="{cd}" opacity=".6"/><path d="M264 172H280V400H264Z" fill="{cd}" opacity=".6"/>'
             + window(132, 230, 14, 24, shutters=False, arch=True, sw=1.1) + window(242, 230, 14, 24, shutters=False, arch=True, sw=1.1))
    mid = f'<g id="mid">{tower}{ground(396, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D7C3A0", line="#C4AC86")}'
            + palm(30, 480, 220, 14, .95) + palm(360, 480, 210, -12, .95)
            + person(140, 448, .95, SEA) + person(250, 450, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Torre de la Calahorra", [sky(p, sun, [(300, 70, .8)], [(250, 60), (270, 50, .8)]), far, sea, mid, near, fx(p, sun, 420)])


# ---------------------------------------------------------------------------
# Gastronomía
# ---------------------------------------------------------------------------
def arcade_facade(y, h, col, floors=3, arch_w=44):
    c, cd, cl = col
    s = f'<path d="M-20 {y}H410V{y + h}H-20Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    fh = (h - 70) / floors
    for fl in range(floors):
        for x in range(-10, 400, arch_w):
            s += window(x + 12, y + 14 + fl * fh, 16, fh * .6, shutters=False, balcony=True, sw=1.1, lit=(x + fl) % 5 == 0)
    s += f'<path d="M-20 {y + h - 70}H410" stroke="{cd}" stroke-width="3"/>'
    for x in range(-10, 400, arch_w):
        s += f'<path d="M{x + 4} {y + h}V{y + h - 44}Q{x + arch_w / 2} {y + h - 70} {x + arch_w - 4} {y + h - 44}V{y + h}Z" fill="#6E5140" stroke="{INK}" stroke-width="1.4"/>'
    return s


def corredera():
    p = "kco"; sun = (80, 100)
    far = f'<g id="far">{far_city(230, 123, towers=2)}</g>'
    mid = f'<g id="mid">{arcade_facade(150, 240, ("#D9A56A", "#BF8A50", "#E8BE88"))}{ground(386)}</g>'
    stalls = "".join(f'<path d="M{x} 470V440H{x + 70}V470" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
                     f'<path d="M{x - 6} 440L{x + 35} 420L{x + 76} 440Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
                     + "".join(f'<circle cx="{x + 12 + k * 12}" cy="436" r="5" fill="{fc}" stroke="{INK}" stroke-width=".8"/>' for k, fc in enumerate(["#D8412F", "#E8B83A", "#4F8B5A", "#D8412F", "#7A2E5E"]))
                     for x, c in [(20, CLAY), (300, SEA)])
    near = (f'<g id="near">{floor(p, 420, color="#E0C7A0", line="#CCAF86")}{stalls}'
            + person(150, 450, 1, SEA) + person(176, 454, .95, CLAY, dress=True) + person(230, 448, .9, "#6E2C5E", dress=True)
            + lamp(372, 540, 160) + "</g>")
    return doc(p, "Plaza de la Corredera", [sky(p, sun, [(300, 60, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def templo():
    p = "kte"; sun = (300, 100)
    far = f'<g id="far">{far_city(240, 125, towers=3)}</g>'
    back = house(-20, 170, 230, 220, YELLOW, floors=3, cols=4) + house(210, 180, 200, 210, WHITE, floors=3, cols=3, lit={(0, 1)})
    podium = (f'<path d="M60 390V340H330V390Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{60 + k * 10} {340 + k * 10}H{330 - k * 10}" stroke="{STONE[1]}" stroke-width="2"/>' for k in range(1, 5))
              + columns(90, 160, 210, 180, 6, STONE, 1.4)
              + f'<path d="M80 160H310V172H80Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x - 6} 172Q{x} 164 {x + 6} 172" fill="{STONE[0]}" stroke="{INK}" stroke-width="1"/>' for x in range(90, 310, 42)))
    mid = f'<g id="mid">{back}{ground(386)}{podium}</g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + tree(20, 480, 40) + tree(370, 480, 40) + person(180, 446, .95, SEA) + person(206, 450, 1, CLAY) + "</g>")
    return doc(p, "Templo romano", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def viana():
    p = "kvi"; sun = (200, 60)
    far = f'<g id="far"><rect x="-10" y="120" width="{W + 20}" height="300" fill="#EAD9BD"/></g>'
    walls = (lime_wall(-20, 130, 410, 270)
             + "".join(horseshoe(x, 300, 40, 90, "#6E5140", 1.4) for x in (30, 320))
             + columns(100, 290, 190, 110, 4, WHITE, 1.3)
             + f'<path d="M90 290H300V280H90Z" fill="{LIME[2]}" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(f'<path d="M{x} 280Q{x + 31} 240 {x + 62} 280" fill="none" stroke="{INK}" stroke-width="1.4"/>' for x in range(100, 290, 63))
             + flowerpots(0, 390, 160, 3, 26) + window(160, 160, 18, 34, shutters=True, balcony=True))
    mid = f'<g id="mid">{walls}{ground(396, "#D6C3A0")}</g>'
    fountain = (f'<ellipse cx="195" cy="500" rx="80" ry="22" fill="#8FB9B4" stroke="{INK}" stroke-width="2"/>'
                f'<ellipse cx="195" cy="496" rx="70" ry="16" fill="#A9CDC8"/>'
                f'<path d="M188 496V460H202V496Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<ellipse cx="195" cy="460" rx="20" ry="6" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M195 454Q180 440 170 470M195 454Q210 440 220 470" fill="none" stroke="#E6F2EF" stroke-width="2"/>')
    pebbles = "".join(f'<circle cx="{(i * 37) % 390}" cy="{430 + (i * 53) % 130}" r="1.6" fill="#B9A488"/>' for i in range(70))
    near = (f'<g id="near">{floor(p, 420, color="#E0CFAE", line="#CDB892")}{pebbles}{fountain}'
            + orange_tree(40, 520, 36) + orange_tree(350, 520, 36) + "</g>")
    return doc(p, "Palacio de Viana", [sky(p, sun, [(90, 60, .7)], []), far, mid, near, fx(p, sun, 420, .2)])


def marina():
    p = "kma"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 127, towers=3)}</g>'
    c, cd, cl = OCHRE
    church = (f'<path d="M110 390V180H290V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M104 180L200 130L296 180Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 390V200L{x + 14} 214V390Z" fill="{cd}" stroke="{INK}" stroke-width="1.2"/>' for x in (100, 286))
              + f'<circle cx="200" cy="220" r="22" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M200 220L{f(200 + 20 * math.cos(math.radians(a)))} {f(220 + 20 * math.sin(math.radians(a)))}" stroke="{INK}" stroke-width="1"/>' for a in range(0, 360, 45))
              + f'<path d="M176 390V300Q200 270 224 300V390Z" fill="#5E4232" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{176 - k * 6} 300Q200 {264 - k * 6} {224 + k * 6} 300" fill="none" stroke="{cd}" stroke-width="2"/>' for k in range(1, 3)))
    side = house(-30, 220, 130, 170, WHITE, floors=2, cols=2) + house(300, 210, 120, 180, LIME, floors=2, cols=2, lit={(0, 0)})
    mid = f'<g id="mid">{side}{church}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + statue(90, 480, 1.1)
            + tree(350, 480, 42) + person(200, 450, .95, SEA) + person(226, 454, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza de Santa Marina", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def flores():
    p = "kfl"; sun = (195, 70)
    far = f'<g id="far">{bell_tower(195, 424, 1.2)}</g>'
    # calleja en perspectiva: paredes encaladas que convergen hacia la torre
    left = (f'<path d="M-20 110L150 250L150 420L-20 560Z" fill="{LIME[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M-20 500L150 400L150 420L-20 560Z" fill="#E8C872" opacity=".7"/>')
    right = (f'<path d="M410 110L240 250L240 420L410 560Z" fill="{LIME[1]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M410 500L240 400L240 420L410 560Z" fill="#D8B862" opacity=".7"/>')
    pots = ""
    for side in (-1, 1):
        for r in range(3):
            for k in range(6):
                t = (k + .5) / 6
                x = (-20 + t * 170) if side < 0 else (410 - t * 170)
                top = 110 + t * 140
                bot = 480 - t * 60
                y = top + (bot - top) * (.2 + r * .22)
                sz = 1.4 - t * .8
                pots += (f'<path d="M{f(x - 6 * sz)} {f(y)}H{f(x + 6 * sz)}L{f(x + 4 * sz)} {f(y + 10 * sz)}H{f(x - 4 * sz)}Z" fill="{POTBLUE}" stroke="{INK}" stroke-width=".9"/>'
                         f'<circle cx="{f(x)}" cy="{f(y - 5 * sz)}" r="{f(5 * sz)}" fill="#4F8B5A"/><circle cx="{f(x + 2 * sz)}" cy="{f(y - 8 * sz)}" r="{f(3 * sz)}" fill="{[CLAY, "#D8412F", "#E86A92"][(k + r) % 3]}"/>')
    mid = f'<g id="mid">{left}{right}{pots}<path d="M150 420H240V428H150Z" fill="#D5C29E"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#D5C29E", line="#C1AB85")}'
            + person(180, 450, .8, SEA) + person(208, 454, .85, CLAY, dress=True) + "</g>")
    return doc(p, "Calleja de las Flores", [sky(p, sun, [(80, 60, .7), (320, 80, .6)], []), far, mid, near, fx(p, sun, 420, .2)])


def tendillas():
    p = "ktd"; sun = (300, 110)
    far = f'<g id="far">{far_city(240, 129, towers=4)}</g>'
    clock = (house(110, 150, 170, 240, WHITE, floors=3, cols=3, lit={(1, 1)})
             + f'<path d="M160 150V110H230V150Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.6"/>'
             + f'<circle cx="195" cy="128" r="14" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/><path d="M195 128V118M195 128L203 132" stroke="{INK}" stroke-width="1.6"/>')
    side = house(-30, 190, 140, 200, YELLOW, floors=3, cols=2) + house(280, 180, 140, 210, PINK, floors=3, cols=2, lit={(0, 1)})
    mid = f'<g id="mid">{side}{clock}{ground(386)}</g>'
    jets = "".join(f'<path d="M{x} 470V{450 - (x % 3) * 6}" stroke="#DDEFF0" stroke-width="3" opacity=".8"/>' for x in range(80, 320, 24))
    near = (f'<g id="near">{floor(p, 420, color="#DCD3C4", line="#C8BEAD")}{jets}'
            + f'<path d="M60 470H330V476H60Z" fill="#8FB9B4"/>'
            + statue(195, 450, 1.2, horse=True, c="#5E6B64")
            + person(60, 452, .95, SEA) + person(330, 456, 1, CLAY, dress=True) + lamp(20, 540, 170) + lamp(370, 540, 170) + "</g>")
    return doc(p, "Plaza de las Tendillas", [sky(p, sun, [(80, 70, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def potro():
    p = "kpo"; sun = (90, 110)
    far = f'<g id="far">{far_city(250, 131, towers=2)}</g>'
    posada = (lime_wall(-20, 220, 200, 170)
              + f'<path d="M50 390V310H110V390Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{x} 390V310" stroke="#5B3A26" stroke-width="1.2"/>' for x in (70, 90))
              + window(20, 250, 22, 30, shutters=True) + window(130, 250, 22, 30, shutters=True)
              + f'<path d="M-20 220H180V210H-20Z" fill="#B5553A" stroke="{INK}" stroke-width="1.4"/>')
    museum = (f'<path d="M200 390V190H410V390Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
              + f'<path d="M270 390V300Q300 270 330 300V390Z" fill="#5E4232" stroke="{INK}" stroke-width="1.6"/>'
              + columns(256, 280, 88, 110, 2, STONE, 1.2) + window(230, 220, 18, 30, shutters=False, arch=True) + window(360, 220, 18, 30, shutters=False, arch=True))
    mid = f'<g id="mid">{posada}{museum}{ground(386)}</g>'
    # fuente del Potro: pilón, fuste y el potrillo encabritado
    fountain = (f'<path d="M140 500H250L244 470H146Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M188 470V380H202V470Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<ellipse cx="195" cy="380" rx="18" ry="5" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M182 378L184 350Q194 344 204 350L214 330L220 336L212 356L210 378H204V364H190V378Z" fill="#8C938A" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M150 470Q170 440 188 430M240 470Q220 440 202 430" fill="none" stroke="#DDEFF0" stroke-width="2"/>')
    near = (f'<g id="near">{floor(p, 420)}{fountain}'
            + person(80, 450, 1, SEA) + person(310, 452, .95, CLAY, dress=True) + tree(370, 490, 34) + "</g>")
    return doc(p, "Plaza del Potro", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"puente": puente, "mezquita": mezquita, "sinagoga": sinagoga, "almodovar": almodovar, "albolafia": albolafia,
          "alcazar": alcazar, "camposanto": camposanto, "calahorra": calahorra,
          "corredera": corredera, "templo": templo, "viana": viana, "marina": marina, "flores": flores,
          "tendillas": tendillas, "potro": potro}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_cordoba_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de Córdoba generados:", ", ".join(keys))
