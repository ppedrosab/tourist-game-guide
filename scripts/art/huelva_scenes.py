#!/usr/bin/env python3
"""
Fondos de Huelva (viewBox 390×560, capas sky · far · sea · mid · near · fx).

Uso: python3 scripts/art/huelva_scenes.py && python3 scripts/art/render_layers.py huelva_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from granada_scenes import horseshoe
from sevilla_scenes import river
from cordoba_scenes import statue, ground, noria

IRON = "#5E6B78"; IROND = "#46525E"
BRICKS = ("#B8563C", "#9A4430", "#CC7156")


def marsh(y):
    """Marismas y la otra orilla de la ría, sin contorno."""
    return (f'<path d="M-10 {y}Q100 {y - 10} 200 {y - 4}T400 {y - 8}V{y + 20}H-10Z" fill="#9DB88A"/>'
            f'<path d="M-10 {y + 6}Q120 {y} 240 {y + 4}T400 {y + 2}V{y + 20}H-10Z" fill="#88A676"/>')


def lattice(x0, x1, y0, y1, step=18):
    s = f'<path d="M{x0} {y0}H{x1}M{x0} {y1}H{x1}" stroke="{INK}" stroke-width="3"/>'
    for x in range(int(x0), int(x1), step):
        s += f'<path d="M{x} {y0}L{x + step} {y1}M{x + step} {y0}L{x} {y1}" stroke="{IRON}" stroke-width="1.6"/>'
        s += f'<path d="M{x} {y0}V{y1}" stroke="{IROND}" stroke-width="2"/>'
    return s


def boat(x, y, s=1.0, c=SEA):
    return (f'<path d="M{f(x - 34 * s)} {f(y)}H{f(x + 34 * s)}L{f(x + 24 * s)} {f(y + 14 * s)}H{f(x - 26 * s)}Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{f(x - 30 * s)} {f(y + 4 * s)}H{f(x + 30 * s)}" stroke="{PAPER}" stroke-width="{f(2 * s)}"/>'
            f'<path d="M{f(x - 6 * s)} {f(y)}V{f(y - 34 * s)}" stroke="{INK}" stroke-width="{f(2 * s)}"/>'
            f'<path d="M{f(x - 4 * s)} {f(y - 32 * s)}L{f(x + 20 * s)} {f(y - 6 * s)}H{f(x - 4 * s)}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M{f(x + 10 * s)} {f(y)}V{f(y - 10 * s)}H{f(x + 24 * s)}V{f(y)}" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.2"/>')


def cottage(x, base, w, roof, wall="#F4EEE2"):
    """Casita del Barrio Obrero: fachada clara, tejado a dos aguas de color y jardín."""
    h = w * .8
    return (f'<path d="M{x} {base}V{base - h}H{x + w}V{base}Z" fill="{wall}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x - 6} {base - h + 2}L{x + w / 2} {base - h - w * .45}L{x + w + 6} {base - h + 2}Z" fill="{roof}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x + w * .7} {base - h - w * .2}V{base - h - w * .42}H{x + w * .8}V{base - h - w * .12}" fill="{roof}" stroke="{INK}" stroke-width="1.2"/>'
            + window(x + w * .14, base - h * .78, w * .22, h * .3, shutters=False, sw=1.1)
            + window(x + w * .64, base - h * .78, w * .22, h * .3, shutters=False, sw=1.1, lit=True)
            + f'<path d="M{x + w * .4} {base}V{base - h * .42}H{x + w * .6}V{base}Z" fill="{SEA}" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<circle cx="{x + k * w / 4}" cy="{base + 2}" r="{w * .07}" fill="#4F8B5A"/>' for k in range(5)))


def church_front(x, base, w, h, col=WHITE, towers=2, tint="#E8B7A0"):
    """Iglesia de fachada barroca colonial con una o dos torres."""
    c, cd, cl = col
    s = (f'<path d="M{x} {base}V{base - h}H{x + w}V{base}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
         f'<path d="M{x + w * .25} {base - h}Q{x + w / 2} {base - h - 40} {x + w * .75} {base - h}Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M{x + w * .38} {base}V{base - 70}Q{x + w / 2} {base - 96} {x + w * .62} {base - 70}V{base}Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
         + window(x + w * .44, base - h + 30, w * .12, 30, shutters=False, arch=True, sw=1.1)
         + f'<path d="M{x + w * .3} {base - 110}H{x + w * .7}" stroke="{tint}" stroke-width="5"/>')
    tws = [x - 34] if towers == 1 else [x - 34, x + w]
    for tx in tws:
        s += (f'<path d="M{tx} {base}V{base - h - 60}H{tx + 34}V{base}Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M{tx + 24} {base - h - 58}H{tx + 34}V{base}H{tx + 24}Z" fill="{cd}" opacity=".6"/>'
              + window(tx + 11, base - h - 44, 12, 24, shutters=False, arch=True, sw=1.1)
              + f'<path d="M{tx - 3} {base - h - 60}H{tx + 37}V{base - h - 66}H{tx - 3}Z" fill="{cl}" stroke="{INK}" stroke-width="1.3"/>'
              f'<path d="M{tx + 4} {base - h - 66}Q{tx + 17} {base - h - 96} {tx + 30} {base - h - 66}Z" fill="{tint}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M{tx + 17} {base - h - 90}V{base - h - 102}M{tx + 13} {base - h - 97}H{tx + 21}" stroke="{INK}" stroke-width="1.3"/>')
    return s


# ---------------------------------------------------------------------------
def muelle():
    p = "hmu"; sun = (90, 120)
    far = f'<g id="far">{marsh(300)}</g>'
    sea = f'<g id="sea">{river(p, 310, 430)}</g>'
    pier = (lattice(-10, 400, 300, 360, 22)
            + f'<path d="M-10 290H400V300H-10Z" fill="#7A5236" stroke="{INK}" stroke-width="1.6"/>'
            + lattice(-10, 400, 360, 390, 22)
            + "".join(f'<path d="M{x} 390V440" stroke="{INK}" stroke-width="7"/><path d="M{x} 390V440" stroke="{IRON}" stroke-width="4"/>' for x in range(0, 400, 44))
            + f'<path d="M-10 282H400" stroke="{INK}" stroke-width="2"/>' + "".join(f'<path d="M{x} 282V290" stroke="{INK}" stroke-width="1.4"/>' for x in range(0, 400, 16)))
    mid = f'<g id="mid">{pier}</g>'
    planks = (f'<path d="M-10 440H400V570H-10Z" fill="#9A6B45"/>'
              + "".join(f'<path d="M-10 {y}H400" stroke="#7A5236" stroke-width="2"/>' for y in range(452, 570, 14))
              + f'<path d="M-10 440H400" stroke="{INK}" stroke-width="2.4"/>')
    near = (f'<g id="near">{planks}'
            + f'<path d="M0 440V410H400V440" fill="none" stroke="{INK}" stroke-width="3"/>' + "".join(f'<path d="M{x} 440V410" stroke="{INK}" stroke-width="2"/>' for x in range(10, 400, 30))
            + person(150, 470, 1.1, SEA) + person(176, 474, 1.05, CLAY, dress=True) + person(260, 468, 1, "#34495E") + "</g>")
    return doc(p, "Muelle del Tinto", [sky(p, sun, [(300, 70, .8)], [(240, 60), (260, 50, .8)]), far, sea, mid, near, fx(p, sun, 440, .25)])


def estacion():
    p = "hes"; sun = (300, 110)
    far = f'<g id="far">{far_city(250, 141, towers=2)}</g>'
    c, cd, cl = BRICKS
    st = (f'<path d="M20 390V220H370V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
          + "".join(f'<path d="M20 {y}H370" stroke="{cd}" stroke-width=".8" opacity=".6"/>' for y in range(230, 390, 10))
          + f'<path d="M140 390V170H250V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
          + "".join(f'<path d="M{x} 170V160H{x + 10}V170" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>' for x in range(142, 244, 16))
          + f'<circle cx="195" cy="200" r="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/><path d="M195 200V190M195 200L204 204" stroke="{INK}" stroke-width="1.6"/>'
          + horseshoe(165, 290, 60, 100, "#4A342A", 1.8)
          + "".join(horseshoe(x, 280, 34, 70, "#5E4232", 1.4) for x in (36, 90, 266, 320))
          + f'<path d="M20 250H370V256H20Z" fill="{PAPER}" opacity=".7"/>')
    mid = f'<g id="mid">{st}{ground(386, "#D9C8A8")}</g>'
    tracks = (f'<path d="M-10 500H400M-10 520H400" stroke="{IRON}" stroke-width="4"/>'
              + "".join(f'<path d="M{x} 494V526" stroke="#7A5236" stroke-width="6"/>' for x in range(0, 400, 26)))
    near = (f'<g id="near">{floor(p, 420, color="#D8C8AA", line="#C4B08E")}{tracks}'
            + palm(30, 480, 240, 12, 1) + palm(360, 480, 230, -10, 1)
            + person(170, 452, 1, SEA) + person(220, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Antigua Estación de Sevilla", [sky(p, sun, [(80, 60, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def carmen():
    p = "hca"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 143, towers=3)}</g>'
    hall = (f'<path d="M10 390V220H380V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M0 220L195 170L390 220Z" fill="{SEA}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 390V260H{x + 40}V390Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.4"/>' for x in range(30, 360, 60))
            + f'<path d="M100 240H290V256H100Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
            + "".join(f'<path d="M{110 + k * 18} 248h10" stroke="{CLAY}" stroke-width="3"/>' for k in range(10)))
    mid = f'<g id="mid">{hall}{ground(386)}</g>'
    stall = lambda x, c: (f'<path d="M{x} 480V446H{x + 90}V480" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
                          f'<path d="M{x - 6} 446L{x + 45} 424L{x + 96} 446Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
                          f'<path d="M{x + 4} 446H{x + 86}V454H{x + 4}Z" fill="#DDEFF0" stroke="{INK}" stroke-width="1"/>'
                          + "".join(f'<ellipse cx="{x + 14 + k * 16}" cy="449" rx="6" ry="3" fill="{fc}" stroke="{INK}" stroke-width=".6"/>' for k, fc in enumerate(["#C7B39A", "#F2A58A", "#9FB6BF", "#C7B39A", "#F2A58A"])))
    near = (f'<g id="near">{floor(p, 420, color="#E0D3BC", line="#CDBE9E")}{stall(10, CLAY)}{stall(290, SEA)}'
            + person(170, 452, 1, SEA) + person(196, 456, .95, CLAY, dress=True) + person(240, 450, .9, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Mercado del Carmen", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def monjas():
    p = "hmo"; sun = (310, 100)
    far = f'<g id="far">{far_city(250, 145, towers=3)}</g>'
    conv = (f'<path d="M-20 390V210H160V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M60 210V170H100V210" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.6"/><path d="M68 200V180Q80 170 92 180V200Z" fill="{WIN}"/>'
            f'<path d="M58 170H102L80 150Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.4"/>'
            + window(20, 240, 18, 30, shutters=True) + window(110, 240, 18, 30, shutters=True)
            + f'<path d="M60 390V320Q80 300 100 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>')
    right = house(250, 180, 160, 210, YELLOW, floors=3, cols=3, lit={(1, 0)}) + house(150, 200, 100, 190, PINK, floors=3, cols=2)
    mid = f'<g id="mid">{right}{conv}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E2D2B6", line="#CFBC98")}'
            + palm(40, 490, 250, 10, 1.05) + palm(350, 490, 240, -10, 1.05) + palm(250, 460, 200, 6, .85)
            + statue(160, 470, 1.25)
            + bench(270, 480) + person(100, 452, 1, SEA) + person(220, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza de las Monjas", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def museo():
    p = "hmu2"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 147, towers=2)}</g>'
    mus = (f'<path d="M20 390V200H370V390Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M10 200H380V186H10Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 380V220H{x + 30}V380Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.2"/>' for x in range(40, 170, 44))
           + "".join(f'<path d="M{x} 380V220H{x + 30}V380Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.2"/>' for x in range(240, 360, 44))
           + noria(205, 290, 62)
           + f'<path d="M110 210H300V224H110Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{mus}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + palm(20, 480, 240, 10, 1) + palm(370, 480, 240, -10, 1)
            + person(150, 452, 1, SEA) + person(250, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Museo de Huelva", [sky(p, sun, [(300, 60, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def obrero():
    p = "hob"; sun = (300, 110)
    far = f'<g id="far">{far_city(240, 149, "#E8C9A8", "#EDD3B6", towers=1)}</g>'
    row1 = "".join(cottage(x, 300, 60, r) for x, r in [(10, CLAY), (90, SEA), (170, "#6E2C5E"), (250, CLAY), (330, "#4F8B5A")])
    row2 = "".join(cottage(x, 390, 80, r, w) for x, r, w in [(-20, SEA, "#F4EEE2"), (90, CLAY, "#F2D48F"), (200, "#4F8B5A", "#F4EEE2"), (310, "#6E2C5E", "#EFB7A0")])
    mid = f'<g id="mid">{row1}<rect x="-10" y="302" width="{W + 20}" height="8" fill="#8FAF6E"/>{row2}{ground(392, "#D9C8A8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D8CBB0", line="#C5B592")}'
            + tree(30, 490, 40, "#5E8F5E") + tree(360, 490, 40, "#5E8F5E")
            + person(160, 456, 1, SEA) + person(186, 460, .7, CLAY) + f'<circle cx="210" cy="468" r="6" fill="#B9793E" stroke="{INK}" stroke-width="1.4"/>'
            + person(240, 452, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Barrio Obrero", [sky(p, sun, [(80, 70, .8)], [(180, 50), (200, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def colon():
    p = "hco"; sun = (90, 100)
    far = f'<g id="far">{far_city(240, 151, towers=2)}</g>'
    c, cd, cl = WHITE
    hotel = (f'<path d="M-10 390V190H400V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M-14 190H404V178H-14Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 178V168H{x + 8}V178" fill="{cl}" stroke="{INK}" stroke-width="1.1"/>' for x in range(-6, 400, 20))
             + "".join(window(x, 214, 18, 40, shutters=True, balcony=True, sw=1.1, lit=x == 150) for x in range(20, 390, 64))
             + f'<path d="M-10 300H400" stroke="{cd}" stroke-width="3"/>'
             + "".join(f'<path d="M{x} 390V330Q{x + 24} 304 {x + 48} 330V390Z" fill="#6E5140" stroke="{INK}" stroke-width="1.4"/>' for x in range(0, 390, 64))
             + f'<path d="M150 170V130H240V170Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/><path d="M144 130L195 104L246 130Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M170 150H220V158H170Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>')
    mid = f'<g id="mid">{hotel}{ground(386, "#D9C8A8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C8A8", line="#C5B08C")}'
            + palm(40, 500, 260, 10, 1.05) + palm(350, 500, 250, -8, 1.05) + palm(130, 470, 210, -6, .9)
            + f'<path d="M200 470Q240 440 290 470" fill="#6E9A4E" stroke="{INK}" stroke-width="1.4"/>'
            + person(220, 452, 1, SEA) + person(246, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Casa Colón", [sky(p, sun, [(300, 60, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def merced():
    p = "hme"; sun = (310, 110)
    far = f'<g id="far">{far_city(240, 153, towers=2)}</g>'
    ch = church_front(125, 390, 140, 180, WHITE, 2, "#E8A87C")
    side = house(-40, 220, 130, 170, YELLOW, floors=2, cols=2) + house(300, 230, 130, 160, PINK, floors=2, cols=2, lit={(0, 1)})
    mid = f'<g id="mid">{side}{ch}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + tree(40, 480, 44, "#4B7C58", "#3A6446") + tree(350, 480, 44, "#4B7C58", "#3A6446")
            + bench(160, 474) + person(120, 452, 1, SEA) + person(280, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza de la Merced", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def levante():
    p = "hle"; sun = (120, 130)
    far = f'<g id="far">{marsh(300)}</g>'
    sea = f'<g id="sea">{river(p, 310, 430)}{boat(90, 350, 1.1, SEA)}{boat(270, 360, 1.2, CLAY)}{boat(190, 330, .7, "#E8B83A")}</g>'
    quay = (f'<path d="M-10 420H400V440H-10Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 420V410H{x + 12}V420" fill="{IRON}" stroke="{INK}" stroke-width="1.2"/>' for x in (60, 200, 330)))
    mid = f'<g id="mid">{quay}</g>'
    crates = "".join(f'<path d="M{x} 500V476H{x + 40}V500Z" fill="#C9A05E" stroke="{INK}" stroke-width="1.6"/><path d="M{x} 484H{x + 40}" stroke="#A07C3C" stroke-width="1.4"/>'
                     + "".join(f'<ellipse cx="{x + 8 + k * 12}" cy="474" rx="6" ry="3" fill="#C7B39A" stroke="{INK}" stroke-width=".6"/>' for k in range(3)) for x in (30, 76))
    near = (f'<g id="near">{floor(p, 440, color="#CDB896", line="#B9A27C")}{crates}'
            + lamp(360, 540, 170) + person(200, 470, 1.1, SEA) + person(230, 474, 1.05, CLAY, dress=True)
            + f'<path d="M280 500Q300 480 330 496" fill="none" stroke="#C9B48A" stroke-width="3"/>' + "</g>")
    return doc(p, "Muelle de Levante", [sky(p, sun, [(300, 70, .8)], [(250, 60), (270, 50, .8), (320, 90, .7)]), far, sea, mid, near, fx(p, sun, 440, .25)])


def sanpedro():
    p = "hsp"; sun = (80, 100)
    far = f'<g id="far">{far_city(250, 155, towers=2)}</g>'
    hill = f'<path d="M-10 390Q80 300 195 290Q310 300 400 390Z" fill="#B9A06A"/><path d="M-10 390Q80 320 195 312Q310 320 400 390Z" fill="#A58C58"/>'
    ch = church_front(160, 300, 100, 130, WHITE, 1, "#D98A5E")
    steps = "".join(f'<path d="M{150 - k * 8} {310 + k * 12}H{270 + k * 8}" stroke="{STONE[1]}" stroke-width="6"/>' for k in range(7))
    mid = f'<g id="mid">{hill}{ch}{steps}{ground(392, "#D9C8A8")}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + palm(40, 490, 230, 10, 1) + tree(350, 480, 40)
            + person(170, 452, 1, SEA) + person(230, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Iglesia de San Pedro", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def punto():
    p = "hpt"; sun = (300, 110)
    far = f'<g id="far">{far_city(240, 157, towers=3)}</g>'
    houses = (house(-30, 190, 140, 200, WHITE, floors=3, cols=2, cierro=True) + house(110, 210, 90, 180, YELLOW, floors=3, cols=2)
              + house(200, 200, 100, 190, MINT, floors=3, cols=2, lit={(1, 1)}) + house(300, 180, 120, 210, PINK, floors=3, cols=2))
    mid = f'<g id="mid">{houses}{ground(386)}</g>'
    fountain = (f'<ellipse cx="195" cy="486" rx="60" ry="14" fill="#8FB9B4" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M188 486V452H202V486Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<ellipse cx="195" cy="452" rx="16" ry="5" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M195 446Q182 434 174 460M195 446Q208 434 216 460" fill="none" stroke="#E6F2EF" stroke-width="2"/>')
    near = (f'<g id="near">{floor(p, 420)}{fountain}' + tree(40, 490, 42) + tree(350, 490, 42)
            + bench(60, 500) + person(120, 452, 1, SEA) + person(280, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza del Punto", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"muelle": muelle, "estacion": estacion, "carmen": carmen, "monjas": monjas, "museo": museo, "obrero": obrero,
          "colon": colon, "merced": merced, "levante": levante, "sanpedro": sanpedro, "punto": punto}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_huelva_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de Huelva generados:", ", ".join(keys))
