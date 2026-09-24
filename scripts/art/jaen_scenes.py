#!/usr/bin/env python3
"""
Fondos de Jaén (viewBox 390×560, capas sky · far · mid · near · fx). Al fondo, el cerro de Santa
Catalina con su castillo y los olivares.

Uso: python3 scripts/art/jaen_scenes.py && python3 scripts/art/render_layers.py jaen_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from granada_scenes import horseshoe, cypress
from sevilla_scenes import orange_tree
from cordoba_scenes import statue, ground, battlements, lime_wall

JSTONE = ("#E6D2A8", "#C9B284", "#F3E4C2")   # piedra dorada de Jaén


def santa_catalina(y, x=280):
    """Cerro de Santa Catalina con el castillo y la cruz, sin contorno."""
    return (f'<path d="M-10 {y}Q80 {y - 30} {x - 60} {y - 110}Q{x} {y - 150} {x + 60} {y - 100}Q{x + 110} {y - 60} 400 {y - 20}V{y + 40}H-10Z" fill="#B7A6A0"/>'
            f'<path d="M{x - 40} {y - 128}H{x + 40}V{y - 150}H{x - 40}Z" fill="#CDBBA8"/>'
            + "".join(f'<path d="M{x - 40 + k * 12} {y - 150}V{y - 156}H{x - 34 + k * 12}V{y - 150}Z" fill="#CDBBA8"/>' for k in range(7))
            + f'<path d="M{x + 10} {y - 150}V{y - 176}H{x + 30}V{y - 150}Z" fill="#CDBBA8"/>'
            f'<path d="M{x - 70} {y - 116}V{y - 136}M{x - 76} {y - 130}H{x - 64}" stroke="#A89890" stroke-width="3"/>')


def olive_hills(y):
    s = f'<path d="M-10 {y}Q100 {y - 24} 200 {y - 10}T400 {y - 16}V{y + 60}H-10Z" fill="#C9B07A"/>'
    for r, (yy, rad, step) in enumerate([(y - 4, 2.6, 14), (y + 12, 3.4, 18), (y + 30, 4.2, 22)]):
        for x in range(-4 + r * 5, 400, step):
            s += f'<circle cx="{x}" cy="{yy + (x % 3)}" r="{rad}" fill="#7C8A4A"/>'
    return s


def far_jaen(y=290, x=280):
    return f'<g id="far">{olive_hills(y + 10)}{santa_catalina(y, x)}{far_city(y + 10, 161, "#E3C9A4", "#EAD5B6", towers=2)}</g>'


def gothic_portal(x, base, w, h, col=JSTONE):
    c, cd, cl = col
    s = f'<path d="M{x} {base}V{base - h}H{x + w}V{base}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    for k in range(4):
        ins = k * 7
        s += f'<path d="M{x + w * .3 + ins} {base}V{base - h * .4}Q{x + w / 2} {base - h * .75 + ins} {x + w * .7 - ins} {base - h * .4}V{base}" fill="{cl if k % 2 else c}" stroke="{INK}" stroke-width="1.2"/>'
    s += f'<path d="M{x + w * .3 + 28} {base}V{base - h * .4}Q{x + w / 2} {base - h * .75 + 28} {x + w * .7 - 28} {base - h * .4}V{base}Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>'
    s += f'<circle cx="{x + w / 2}" cy="{base - h * .85}" r="{w * .1}" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
    return s


def lizard_statue(x, base, s=1.0):
    """El lagarto de la Malena en bronce, sobre una roca con agua."""
    c = "#5E7A4E"
    return (f'<path d="M{x - 60 * s} {base}Q{x - 50 * s} {base - 50 * s} {x} {base - 56 * s}Q{x + 54 * s} {base - 50 * s} {x + 64 * s} {base}Z" fill="#A89F92" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M{x - 58 * s} {base - 50 * s}Q{x - 20 * s} {base - 80 * s} {x + 10 * s} {base - 70 * s}Q{x + 40 * s} {base - 66 * s} {x + 56 * s} {base - 84 * s}L{x + 72 * s} {base - 80 * s}Q{x + 62 * s} {base - 60 * s} {x + 30 * s} {base - 54 * s}Q{x - 10 * s} {base - 50 * s} {x - 58 * s} {base - 50 * s}Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x + dx * s} {base - 58 * s}l{lx * s} {12 * s}" stroke="{INK}" stroke-width="{4 * s}"/>' for dx, lx in [(-24, -6), (-6, 4), (18, -4), (34, 6)])
            + f'<circle cx="{x + 62 * s}" cy="{base - 80 * s}" r="{2.4 * s}" fill="{GOLD}"/>'
            + "".join(f'<circle cx="{x + dx * s}" cy="{base - 62 * s}" r="{2.4 * s}" fill="#40573A"/>' for dx in (-30, -14, 2, 20))
            + f'<path d="M{x + 70 * s} {base - 76 * s}Q{x + 90 * s} {base - 60 * s} {x + 84 * s} {base - 20 * s}" fill="none" stroke="#DDEFF0" stroke-width="3"/>')


def ochre_house(x, y, w, h, **kw):
    return house(x, y, w, h, ("#E8C98E", "#CDAE72", "#F3DCAE"), **kw)


# ---------------------------------------------------------------------------
def catedral():
    p = "jca"; sun = (80, 110)
    far = far_jaen(280, 300)
    c, cd, cl = JSTONE
    fac = (f'<path d="M70 390V150H320V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M60 150H330V136H60Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 136V124H{x + 6}V136" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in range(64, 326, 12))
           + columns(96, 190, 198, 190, 6, JSTONE, 1.4)
           + f'<path d="M70 260H320" stroke="{cd}" stroke-width="4"/>'
           + "".join(f'<path d="M{x} 390V320Q{x + 16} 300 {x + 32} 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>' for x in (120, 179, 238))
           + "".join(window(x, 208, 16, 30, shutters=False, arch=True, sw=1.1) for x in (128, 187, 246)))
    towers = "".join(f'<path d="M{x} 390V90H{x + 56}V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
                     f'<path d="M{x + 40} 92H{x + 56}V390H{x + 40}Z" fill="{cd}" opacity=".6"/>'
                     f'<path d="M{x - 4} 90H{x + 60}V80H{x - 4}Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
                     f'<path d="M{x + 8} 80Q{x + 28} 50 {x + 48} 80Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
                     f'<path d="M{x + 28} 56V44M{x + 23} 50H{x + 33}" stroke="{INK}" stroke-width="1.4"/>'
                     + window(x + 20, 110, 16, 32, shutters=False, arch=True, sw=1.1) + window(x + 20, 180, 16, 32, shutters=False, arch=True, sw=1.1)
                     for x in (20, 314))
    mid = f'<g id="mid">{fac}{towers}{ground(386, "#E0CDA8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E2CFAA", line="#CFB98E")}'
            + person(150, 450, 1, SEA) + person(176, 454, .95, CLAY, dress=True) + person(250, 448, .9, "#34495E")
            + lamp(40, 540, 170) + lamp(350, 540, 170) + "</g>")
    return doc(p, "Catedral de Jaén", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sanlorenzo():
    p = "jsl"; sun = (195, 80)
    far = far_jaen(280, 110)
    left = lime_wall(-30, 180, 150, 230) + window(20, 230, 20, 34) + window(70, 300, 20, 34, balcony=True)
    right = ochre_house(270, 170, 160, 240, floors=3, cols=2, lit={(1, 0)})
    c, cd, cl = JSTONE
    arch = (f'<path d="M120 400V210H270V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M150 400V300Q195 250 240 300V400Z" fill="#8FB9B4" opacity=".35" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M150 300Q195 250 240 300" fill="none" stroke="{cd}" stroke-width="6"/>'
            f'<path d="M150 240H240V270H150Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
            + window(186, 244, 18, 20, shutters=False, sw=1)
            + f'<path d="M116 210H274V200H116Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{arch}{left}{right}{ground(400, "#D9C6A2")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D8C6A4", line="#C4AF88")}'
            + person(180, 452, .95, SEA) + person(210, 456, 1, CLAY, dress=True) + lamp(360, 540, 160) + "</g>")
    return doc(p, "Arco de San Lorenzo", [sky(p, sun, [(80, 60, .7), (320, 80, .6)], []), far, mid, near, fx(p, sun, 420, .25)])


def sanildefonso():
    p = "jsi"; sun = (310, 100)
    far = far_jaen(290, 80)
    c, cd, cl = JSTONE
    church = (gothic_portal(120, 390, 150, 210)
              + f'<path d="M110 180L195 130L280 180Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M280 390V120H330V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(280, 330, 120, c, 12)
              + window(296, 150, 18, 34, shutters=False, arch=True, sw=1.1)
              + "".join(f'<path d="M{x} 390V200L{x + 10} 190V390Z" fill="{cd}" stroke="{INK}" stroke-width="1.2"/>' for x in (110, 270)))
    side = ochre_house(-30, 210, 140, 180, floors=3, cols=2) + house(330, 230, 90, 160, WHITE, floors=2, cols=1)
    mid = f'<g id="mid">{side}{church}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + orange_tree(40, 480, 32) + orange_tree(350, 480, 32)
            + bench(150, 474) + person(230, 452, 1, SEA) + person(256, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Basílica de San Ildefonso", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def constitucion():
    p = "jco"; sun = (80, 110)
    far = far_jaen(280, 300)
    houses = (house(-30, 180, 140, 210, YELLOW, floors=3, cols=2, cierro=True) + house(110, 160, 170, 230, WHITE, floors=4, cols=3, lit={(2, 1)})
              + ochre_house(280, 190, 140, 200, floors=3, cols=2))
    mid = f'<g id="mid">{houses}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#DDD3C3", line="#C9BEAC")}'
            + statue(195, 480, 1.1, c="#6E7A72")
            + tree(40, 490, 40) + tree(350, 490, 40) + person(110, 452, 1, SEA) + person(290, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza de la Constitución", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def banos():
    """Sala de los baños árabes: bóveda con lucernas en estrella y arcos de herradura."""
    p = "jba"; sun = (195, 40)
    skyg = (f'<g id="sky"><rect x="0" y="0" width="{W}" height="{H}" fill="#8A6A4E"/>'
            f'<path d="M-10 0H400V200Q195 110 -10 200Z" fill="#9E7C5C"/></g>')
    vault = f'<path d="M-10 60Q195 -40 400 60V240H-10Z" fill="#B58E68" stroke="{INK}" stroke-width="1.8"/>'
    stars = ""
    for i, (x, y) in enumerate([(80, 80), (150, 50), (240, 50), (310, 80), (195, 110), (110, 140), (280, 140)]):
        pts = " ".join(f"{x + (9 if k % 2 == 0 else 4) * math.cos(math.radians(k * 45 - 90)):.1f},{y + (9 if k % 2 == 0 else 4) * math.sin(math.radians(k * 45 - 90)):.1f}" for k in range(8))
        stars += f'<polygon points="{pts}" fill="#FFF3C4" stroke="{INK}" stroke-width="1.2"/>'
    far = f'<g id="far">{vault}{stars}</g>'
    arches = (f'<path d="M-10 400V230H400V400Z" fill="#C49C74" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(horseshoe(x, 290, 70, 110, "#5E4232", 1.6) for x in (-20, 90, 230, 340))
              + "".join(f'<path d="M{x} 400V250H{x + 14}V400Z" fill="#A88460" stroke="{INK}" stroke-width="1.4"/>' for x in (60, 190, 320)))
    mid = f'<g id="mid">{arches}{ground(396, "#B99A76")}</g>'
    beams = "".join(f'<path d="M{x - 6} 0L{x + 6} 0L{x + 30} 560L{x - 20} 560Z" fill="#FFF3C4" opacity=".12"/>' for x in (150, 240, 110, 280))
    near = (f'<g id="near">{floor(p, 420, color="#B99A76", line="#A5845F")}{beams}'
            + person(170, 460, 1.05, SEA) + person(220, 464, 1, CLAY, dress=True) + "</g>")
    fxg = (f'<g id="fx"><defs><radialGradient id="{p}v" cx=".5" cy=".4" r=".7"><stop offset=".45" stop-color="#2A1A10" stop-opacity="0"/>'
           f'<stop offset="1" stop-color="#2A1A10" stop-opacity=".5"/></radialGradient></defs><rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}v)"/></g>')
    return doc(p, "Baños árabes de Jaén", [skyg, far, mid, near, fxg])


def sanjuan():
    p = "jsj"; sun = (300, 100)
    far = far_jaen(280, 90)
    c, cd, cl = JSTONE
    church = (f'<path d="M110 390V230H250V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M104 230L180 196L256 230Z" fill="#B5553A" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M160 390V330Q180 310 200 330V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{156 - k * 6} 330Q180 {302 - k * 6} {204 + k * 6} 330" fill="none" stroke="{cd}" stroke-width="2"/>' for k in range(1, 3))
              + f'<path d="M250 390V130H310V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              + f'<path d="M244 130H316V120H244Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/><path d="M256 120L280 94L304 120Z" fill="#B5553A" stroke="{INK}" stroke-width="1.4"/>'
              + f'<circle cx="280" cy="170" r="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/><path d="M280 170V160M280 170L288 174" stroke="{INK}" stroke-width="1.6"/>'
              + window(272, 220, 16, 30, shutters=False, arch=True, sw=1.1))
    side = lime_wall(-30, 220, 140, 170) + window(20, 260, 20, 34) + ochre_house(310, 210, 110, 180, floors=3, cols=2)
    mid = f'<g id="mid">{side}{church}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D8C6A4", line="#C4AF88")}' + orange_tree(50, 480, 30)
            + person(170, 452, 1, SEA) + person(230, 456, .95, CLAY, dress=True) + lamp(360, 540, 160) + "</g>")
    return doc(p, "Plaza de San Juan", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def magdalena():
    p = "jma"; sun = (90, 110)
    far = far_jaen(280, 300)
    c, cd, cl = JSTONE
    wall = (f'<path d="M-20 390V200H300V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 390V270Q{x + 25} 236 {x + 50} 270V390Z" fill="#6E5140" stroke="{INK}" stroke-width="1.4"/>' for x in (0, 70, 140, 210))
            + f'<path d="M300 390V140H350V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(300, 350, 140, cl, 12)
            + horseshoe(314, 170, 22, 40, WIN, 1.1) + horseshoe(314, 240, 22, 40, WIN, 1.1))
    mid = f'<g id="mid">{wall}{ground(386, "#D9C6A2")}</g>'
    pool = (f'<path d="M80 470H310V520H80Z" fill="#8FB9B4" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x} 494q6 -3 12 0" fill="none" stroke="#E6F2EF" stroke-width="1.6"/>' for x in (110, 170, 240)))
    near = (f'<g id="near">{floor(p, 420, color="#DAC7A2", line="#C6B08A")}{pool}'
            + orange_tree(40, 470, 32) + orange_tree(350, 470, 32) + orange_tree(195, 450, 24)
            + person(120, 456, .95, SEA) + person(280, 458, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Iglesia de la Magdalena", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def raudal():
    p = "jra"; sun = (300, 110)
    far = far_jaen(280, 100)
    houses = (lime_wall(-30, 220, 130, 170) + window(10, 260, 18, 30) + window(60, 260, 18, 30, lit=True)
              + ochre_house(100, 200, 110, 190, floors=3, cols=2) + lime_wall(210, 230, 200, 160) + window(250, 270, 18, 30) + window(330, 270, 18, 30))
    mid = f'<g id="mid">{houses}{ground(386, "#D9C6A2")}</g>'
    basin = (f'<path d="M40 520H350L336 480H54Z" fill="{JSTONE[0]}" stroke="{INK}" stroke-width="2"/>'
             f'<path d="M58 486H332V496H58Z" fill="#8FB9B4"/>')
    near = (f'<g id="near">{floor(p, 420)}{basin}' + lizard_statue(195, 486, 1.25)
            + person(60, 452, 1, SEA) + person(340, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Fuente del Lagarto", [sky(p, sun, [(80, 70, .8)], [(180, 50), (200, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def mercado():
    p = "jme"; sun = (80, 110)
    far = far_jaen(280, 300)
    hall = (f'<path d="M10 390V210H380V390Z" fill="{JSTONE[2]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M0 210H390V194H0Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 390V250H{x + 44}V390Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.4"/>' for x in range(30, 360, 66))
            + f'<path d="M110 222H280V238H110Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<path d="M{120 + k * 16} 230h8" stroke="{SEA}" stroke-width="3"/>' for k in range(10)))
    mid = f'<g id="mid">{hall}{ground(386)}</g>'
    stall = lambda x, c: (f'<path d="M{x} 480V446H{x + 90}V480" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
                          f'<path d="M{x - 6} 446L{x + 45} 424L{x + 96} 446Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
                          + "".join(f'<circle cx="{x + 14 + k * 16}" cy="440" r="6" fill="{fc}" stroke="{INK}" stroke-width=".8"/>' for k, fc in enumerate(["#6E7A3E", "#3E4A2A", "#D8412F", "#6E7A3E", "#E8B83A"])))
    near = (f'<g id="near">{floor(p, 420, color="#E0D3BC", line="#CDBE9E")}{stall(10, "#6E7A3E")}{stall(290, CLAY)}'
            + person(170, 452, 1, SEA) + person(196, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Mercado de San Francisco", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"catedral": catedral, "sanlorenzo": sanlorenzo, "sanildefonso": sanildefonso, "constitucion": constitucion,
          "banos": banos, "sanjuan": sanjuan, "magdalena": magdalena, "raudal": raudal, "mercado": mercado}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_jaen_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de Jaén generados:", ", ".join(keys))
