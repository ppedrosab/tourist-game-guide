#!/usr/bin/env python3
"""
Fondos de Almería (viewBox 390×560, capas sky · far · sea · mid · near · fx). Cerros secos, la
Alcazaba sobre la ciudad y mucha luz.

Uso: python3 scripts/art/almeria_scenes.py && python3 scripts/art/render_layers.py almeria_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from granada_scenes import horseshoe
from sevilla_scenes import river
from cordoba_scenes import statue, ground, battlements, lime_wall
from huelva_scenes import boat, lattice

OCHRE = ("#D9B06A", "#B8904E", "#E8C88A")
HILL = "#C9A77E"; HILLD = "#B08F66"


def alcazaba_hill(y, x0=0, soft=False, s=1.0):
    """El cerro de la Alcazaba con sus murallas escalonadas y torres."""
    sw = 0 if soft else 1.4
    c, cd, cl = OCHRE if not soft else ("#E2C89A", "#D3B888", "#EAD4AC")
    out = f'<path d="M{x0 - 20} {y}Q{x0 + 60 * s} {y - 110 * s} {x0 + 170 * s} {y - 130 * s}Q{x0 + 260 * s} {y - 120 * s} {x0 + 330 * s} {y - 60 * s}L{x0 + 420 * s} {y}Z" fill="{HILL if not soft else "#DCC39E"}"/>'
    pts = [(x0 + 20 * s, y - 40 * s), (x0 + 80 * s, y - 96 * s), (x0 + 170 * s, y - 118 * s), (x0 + 250 * s, y - 108 * s), (x0 + 320 * s, y - 60 * s)]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        out += f'<path d="M{f(xa)} {f(ya)}L{f(xb)} {f(yb)}L{f(xb)} {f(yb + 18 * s)}L{f(xa)} {f(ya + 18 * s)}Z" fill="{c}" stroke="{INK if not soft else c}" stroke-width="{sw}"/>'
    for i, (xa, ya) in enumerate(pts):
        th = (40 if i == 2 else 26) * s
        out += f'<path d="M{f(xa - 10 * s)} {f(ya + 18 * s)}V{f(ya - th)}H{f(xa + 10 * s)}V{f(ya + 18 * s)}Z" fill="{cl}" stroke="{INK if not soft else cl}" stroke-width="{sw}"/>'
        out += "".join(f'<path d="M{f(xa - 10 * s + k * 7 * s)} {f(ya - th)}V{f(ya - th - 5 * s)}H{f(xa - 6 * s + k * 7 * s)}V{f(ya - th)}" fill="{cl}" stroke="{INK if not soft else cl}" stroke-width="{sw * .7}"/>' for k in range(3))
    return out


def dry_hills(y):
    return (f'<path d="M-10 {y}Q60 {y - 50} 140 {y - 30}T300 {y - 40}T400 {y - 20}V{y + 40}H-10Z" fill="#DCC39E"/>'
            + "".join(f'<circle cx="{x}" cy="{y - 10 - (x % 5) * 3}" r="3" fill="#A8A06A" opacity=".7"/>' for x in range(10, 390, 37)))


def far_alm(y=290, x0=0, s=1.0):
    return f'<g id="far">{dry_hills(y)}{alcazaba_hill(y + 10, x0, soft=True, s=s)}{far_city(y + 10, 171, "#EAD2B0", "#F0DDC0", towers=1)}</g>'


def cube_houses(y, seed=0, n=8):
    cols = ["#F4EEE2", "#E8744A", "#2F9EB0", "#F2C14E", "#E86A92", "#8FB9B4", "#F4EEE2", "#A8D08D"]
    s = ""
    for i in range(n):
        x = -10 + i * 52 + (seed * 11 + i * 7) % 12
        yy = y - (i * 13 + seed * 7) % 40
        w = 44 + (i * 5) % 12
        h = 34 + (i * 11) % 20
        c = cols[(i + seed) % len(cols)]
        s += (f'<path d="M{x} {yy}V{yy - h}H{x + w}V{yy}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M{x + 8} {yy}V{yy - 16}H{x + 18}V{yy}Z" fill="#5B3A26" stroke="{INK}" stroke-width="1"/>'
              f'<path d="M{x + w - 16} {yy - h + 8}H{x + w - 6}V{yy - h + 18}H{x + w - 16}Z" fill="{WIN}"/>')
    return s


# ---------------------------------------------------------------------------
def puerto():
    p = "apu"; sun = (300, 110)
    far = far_alm(290, -20, .95)
    sea = f'<g id="sea">{river(p, 300, 420)}{boat(260, 350, 1.2, SEA)}{boat(110, 330, .8, CLAY)}</g>'
    quay = f'<path d="M-10 410H400V430H-10Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>'
    mid = f'<g id="mid">{quay}</g>'
    near = (f'<g id="near">{floor(p, 430, color="#E3CFAA", line="#CFB78E")}'
            + palm(30, 520, 280, 12, 1.1) + palm(360, 520, 270, -10, 1.1) + palm(120, 480, 220, 6, .9)
            + bench(200, 480) + person(170, 460, 1.05, SEA) + person(290, 464, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Parque de Nicolás Salmerón", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, sea, mid, near, fx(p, sun, 430, .3)])


def catedral():
    p = "aca"; sun = (80, 100)
    far = far_alm(280, 120, .9)
    c, cd, cl = OCHRE
    cat = (f'<path d="M40 390V170H350V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(40, 350, 170, c, 18)
           + f'<path d="M40 390V120H100V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(40, 100, 120, cl, 14)
           + f'<path d="M290 390V130H350V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(290, 350, 130, cl, 14)
           + f'<path d="M150 390V230H240V390Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           + columns(160, 250, 70, 140, 2, STONE, 1.2)
           + f'<path d="M176 390V310Q195 290 214 310V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
           + f'<path d="M146 230L195 204L244 230Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
           # el sol de Portocarrero en el muro de la cabecera
           + f'<circle cx="320" cy="250" r="14" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{320 + 16 * math.cos(math.radians(a)):.1f} {250 + 16 * math.sin(math.radians(a)):.1f}L{320 + 24 * math.cos(math.radians(a)):.1f} {250 + 24 * math.sin(math.radians(a)):.1f}" stroke="{GOLD}" stroke-width="3"/>' for a in range(0, 360, 30))
           + window(62, 160, 16, 30, shutters=False, arch=True, sw=1.1) + window(312, 170, 16, 30, shutters=False, arch=True, sw=1.1))
    mid = f'<g id="mid">{cat}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + palm(20, 500, 250, 10, 1) + palm(372, 500, 240, -10, 1)
            + person(150, 452, 1, SEA) + person(250, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Catedral de Almería", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def alcazaba():
    p = "aal"; sun = (310, 110)
    far = f'<g id="far">{dry_hills(290)}</g>'
    mid = f'<g id="mid">{alcazaba_hill(400, -10, s=1.25)}{ground(392, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C6A2", line="#C5AF88")}'
            + f'<path d="M110 470V430H280V470Z" fill="{OCHRE[0]}" stroke="{INK}" stroke-width="1.8"/>' + horseshoe(170, 440, 50, 60, "#5E4232", 1.6).replace("M", "M", 1)
            + palm(30, 520, 260, 10, 1.05) + palm(360, 520, 250, -10, 1.05)
            + person(120, 486, 1.05, SEA) + person(280, 490, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Alcazaba de Almería", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def muralla():
    p = "amu"; sun = (90, 110)
    far = f'<g id="far">{dry_hills(270)}</g>'
    c, cd, cl = OCHRE
    wall = (f'<path d="M-20 380Q60 300 150 330Q250 360 410 180V420H-20Z" fill="{HILL}"/>'
            f'<path d="M-20 360L60 300L150 320L250 290L330 220L410 170" fill="none" stroke="{INK}" stroke-width="16"/>'
            f'<path d="M-20 360L60 300L150 320L250 290L330 220L410 170" fill="none" stroke="{c}" stroke-width="12"/>'
            + "".join(f'<path d="M{x - 14} {y}V{y - 40}H{x + 14}V{y}Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>' + battlements(x - 14, x + 14, y - 40, cl, 8)
                      for x, y in [(60, 304), (150, 324), (250, 294), (330, 226)]))
    mid = f'<g id="mid">{wall}{ground(400, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C6A2", line="#C5AF88")}'
            + "".join(f'<path d="M{x} 470q-8 -20 0 -40q8 20 0 40Z" fill="#8FA66A" stroke="{INK}" stroke-width="1"/>' for x in (40, 70, 330, 360))
            + person(180, 456, 1, SEA) + person(210, 460, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Muralla de Jayrán", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def plazavieja():
    p = "apv"; sun = (300, 110)
    far = far_alm(270, 40, .8)
    arc = (f'<path d="M-20 390V210H410V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
           + "".join(window(x, 230, 16, 30, shutters=True, balcony=True, sw=1.1) for x in range(0, 390, 52))
           + "".join(f'<path d="M{x} 390V320Q{x + 22} 298 {x + 44} 320V390Z" fill="#6E5140" stroke="{INK}" stroke-width="1.4"/>' for x in range(-10, 400, 52)))
    ayto = (f'<path d="M110 390V150H280V390Z" fill="#C0564A" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 390V150" stroke="{PAPER}" stroke-width="6"/>' for x in (120, 270))
            + f'<path d="M104 150H286V136H104Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
            + f'<path d="M170 136V104H220V136Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><circle cx="195" cy="120" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><path d="M195 120V112M195 120L201 123" stroke="{INK}" stroke-width="1.4"/>'
            + "".join(window(x, 180, 16, 34, shutters=False, balcony=True, sw=1.1) for x in (140, 187, 234))
            + "".join(f'<path d="M{x} 390V320Q{x + 16} 300 {x + 32} 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>' for x in (130, 179, 228)))
    mid = f'<g id="mid">{arc}{ayto}{ground(386, "#E3CFAA")}</g>'
    column = (f'<path d="M180 480V450H210V480Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M189 450V380H201V450Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M183 380H207V372H183Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.2"/>')
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}{column}'
            + palm(40, 500, 240, 10, 1) + palm(350, 500, 240, -10, 1)
            + person(120, 452, 1, SEA) + person(280, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza Vieja", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def aljibes():
    p = "aaj"
    skyg = f'<g id="sky"><rect x="0" y="0" width="{W}" height="{H}" fill="#7E5E44"/></g>'
    vault = (f'<path d="M-10 0H400V240H-10Z" fill="#9E7654"/>'
             + "".join(f'<rect x="{x}" y="{y}" width="24" height="10" fill="#B58E68" stroke="#7E5E44" stroke-width="1.2"/>' for x in range(-10 + 0, 400, 26) for y in range(10, 230, 14)))
    far = f'<g id="far">{vault}</g>'
    arches = (f'<path d="M-10 400V200H400V400Z" fill="#A88460" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{x} 400V270Q{x + 50} 190 {x + 100} 270V400Z" fill="#5E4232" stroke="{INK}" stroke-width="1.8"/>' for x in (-40, 90, 220, 350))
              + "".join(f'<rect x="{x}" y="{y}" width="20" height="8" fill="#B58E68" stroke="#7E5E44" stroke-width="1"/>' for x in range(-10, 400, 22) for y in (206, 216)))
    mid = f'<g id="mid">{arches}</g>'
    water = (f'<path d="M-10 400H400V470H-10Z" fill="#6E9FA0"/>'
             + "".join(f'<path d="M{x} {y}q10 -4 20 0" fill="none" stroke="#DDEFF0" stroke-width="1.6"/>' for x, y in [(30, 420), (120, 440), (220, 425), (300, 450)]))
    near = (f'<g id="near">{water}<path d="M-10 470H400V570H-10Z" fill="#B99A76"/><path d="M-10 470H400" stroke="{INK}" stroke-width="2.4"/>'
            + person(170, 510, 1.1, SEA) + person(220, 514, 1.05, CLAY, dress=True) + lamp(40, 560, 110) + lamp(350, 560, 110) + "</g>")
    fxg = (f'<g id="fx"><defs><radialGradient id="{p}v" cx=".5" cy=".5" r=".7"><stop offset=".4" stop-color="#2A1A10" stop-opacity="0"/>'
           f'<stop offset="1" stop-color="#2A1A10" stop-opacity=".55"/></radialGradient></defs><rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}v)"/></g>')
    return doc(p, "Aljibes de Jayrán", [skyg, far, mid, near, fxg])


def purchena():
    p = "apc"; sun = (300, 100)
    far = far_alm(260, -40, .8)
    c, cd, cl = ("#F2D9B8", "#D9BE98", "#FBEBD4")
    mariposas = (f'<path d="M100 390V140H290V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
                 f'<path d="M100 140Q195 100 290 140Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
                 + "".join(window(x, y, 18, 34, shutters=False, balcony=True, sw=1.1, lit=(x + y) % 3 == 0) for x in (122, 186, 250) for y in (170, 240, 310))
                 + "".join(f'<path d="M{x} 124Q{x - 12} {110} {x - 14} 122Q{x - 12} 132 {x} 126Q{x + 12} 132 {x + 14} 122Q{x + 12} 110 {x} 124Z" fill="#2F9EB0" stroke="{INK}" stroke-width="1.2"/>' for x in (150, 195, 240)))
    side = house(-30, 180, 130, 210, YELLOW, floors=3, cols=2, cierro=True) + house(290, 190, 130, 200, PINK, floors=3, cols=2)
    mid = f'<g id="mid">{side}{mariposas}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#DDD3C3", line="#C9BEAC")}'
            + person(80, 452, 1, SEA) + person(140, 456, .95, CLAY, dress=True) + person(260, 450, .9, "#6E2C5E", dress=True) + person(320, 454, 1, "#34495E")
            + lamp(195, 540, 170) + "</g>")
    return doc(p, "Puerta de Purchena", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def refugios():
    p = "are"; sun = (90, 110)
    far = far_alm(260, 60, .8)
    houses = (house(-30, 170, 150, 220, WHITE, floors=4, cols=2, lit={(1, 0)}) + house(120, 190, 150, 200, YELLOW, floors=3, cols=3)
              + house(270, 180, 150, 210, MINT, floors=3, cols=2, cierro=True))
    mid = f'<g id="mid">{houses}{ground(386)}</g>'
    entrance = (f'<path d="M140 490V440H250V490Z" fill="#DDEFF0" fill-opacity=".7" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M136 440H254V432H136Z" fill="#5E6B78" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M170 490V456H220V490Z" fill="#3A3A48" stroke="{INK}" stroke-width="1.4"/>'
                + "".join(f'<path d="M{176 + k * 8} {460 + k * 6}H{214 - k * 8}" stroke="#6E6E78" stroke-width="2"/>' for k in range(4)))
    near = (f'<g id="near">{floor(p, 420, color="#DDD3C3", line="#C9BEAC")}{entrance}'
            + tree(40, 490, 40) + tree(350, 490, 40) + person(100, 456, 1, SEA) + person(300, 460, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Refugios de la Guerra Civil", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def mercado():
    p = "ame"; sun = (80, 110)
    far = far_alm(270, 100, .8)
    m = (f'<path d="M20 390V200H370V390Z" fill="#C8704E" stroke="{INK}" stroke-width="1.8"/>'
         + "".join(f'<path d="M20 {y}H370" stroke="#A85A3C" stroke-width=".8" opacity=".6"/>' for y in range(210, 390, 12))
         + f'<path d="M110 390V250Q195 170 280 250V390Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.8"/>'
         + "".join(f'<path d="M{x} 390V{250 - (1 - ((x - 195) / 85) ** 2) * 60:.0f}" stroke="#5E6B78" stroke-width="2"/>' for x in range(124, 280, 18))
         + f'<path d="M110 250Q195 170 280 250" fill="none" stroke="#5E6B78" stroke-width="4"/>'
         + f'<path d="M14 200H376V186H14Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
         + window(40, 250, 20, 50, shutters=False, arch=True) + window(330, 250, 20, 50, shutters=False, arch=True))
    mid = f'<g id="mid">{m}{ground(386)}</g>'
    stall = lambda x, c: (f'<path d="M{x} 480V446H{x + 90}V480" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
                          f'<path d="M{x - 6} 446L{x + 45} 424L{x + 96} 446Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
                          + "".join(f'<circle cx="{x + 14 + k * 16}" cy="440" r="6" fill="{fc}" stroke="{INK}" stroke-width=".8"/>' for k, fc in enumerate(["#D8412F", "#4F8B5A", "#E8B83A", "#D8412F", "#4F8B5A"])))
    near = (f'<g id="near">{floor(p, 420, color="#E0D3BC", line="#CDBE9E")}{stall(10, "#4F8B5A")}{stall(290, CLAY)}'
            + person(170, 452, 1, SEA) + person(196, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Mercado Central", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def cable():
    p = "acb"; sun = (120, 120)
    far = f'<g id="far">{dry_hills(300)}</g>'
    sea = f'<g id="sea">{river(p, 300, 430)}</g>'
    iron = "#8C4A2E"
    pier = (f'<path d="M-10 250H400V262H-10Z" fill="{iron}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 262V430" stroke="{INK}" stroke-width="8"/><path d="M{x} 262V430" stroke="{iron}" stroke-width="5"/>' for x in range(10, 400, 60))
            + "".join(f'<path d="M{x} 262L{x + 60} 360M{x + 60} 262L{x} 360" stroke="{iron}" stroke-width="2.4"/>' for x in range(10, 340, 60))
            + f'<path d="M-10 360H400" stroke="{iron}" stroke-width="4"/>'
            + f'<path d="M-10 250V200H120V250" fill="{iron}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 200V250" stroke="{INK}" stroke-width="1.4"/>' for x in range(0, 120, 16)))
    mid = f'<g id="mid">{pier}</g>'
    near = (f'<g id="near"><path d="M-10 440H400V570H-10Z" fill="#E3CFAA"/><path d="M-10 440H400" stroke="{INK}" stroke-width="2"/>'
            + palm(40, 530, 250, 10, 1) + palm(350, 530, 240, -10, 1)
            + person(170, 480, 1.1, SEA) + person(200, 484, 1.05, CLAY, dress=True) + "</g>")
    return doc(p, "Cable Inglés", [sky(p, sun, [(300, 70, .8)], [(250, 60), (270, 50, .8)]), far, sea, mid, near, fx(p, sun, 440, .25)])


def chanca():
    p = "ach"; sun = (300, 110)
    far = f'<g id="far">{dry_hills(270)}{alcazaba_hill(290, -60, soft=True, s=.9)}</g>'
    hill = f'<path d="M-10 400Q100 260 250 250Q340 250 400 300V420H-10Z" fill="{HILL}"/>'
    caves = "".join(f'<path d="M{x} {y}Q{x + 10} {y - 16} {x + 20} {y}Z" fill="#5B3A26" stroke="{INK}" stroke-width="1"/>' for x, y in [(290, 290), (330, 300), (250, 280)])
    mid = f'<g id="mid">{hill}{caves}{cube_houses(330, 1, 6)}{cube_houses(390, 3, 8)}{ground(392, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C6A2", line="#C5AF88")}'
            + f'<path d="M280 440V470M340 440V470M280 444H340" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 446q4 10 0 18q-4 -8 0 -18Z" fill="#C7B39A" stroke="{INK}" stroke-width=".8"/>' for x in (292, 306, 320))
            + person(120, 456, 1, SEA) + person(160, 460, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Barrio de la Chanca", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"puerto": puerto, "catedral": catedral, "alcazaba": alcazaba, "muralla": muralla, "plazavieja": plazavieja,
          "aljibes": aljibes, "purchena": purchena, "refugios": refugios, "mercado": mercado, "cable": cable, "chanca": chanca}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_almeria_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de Almería generados:", ", ".join(keys))
