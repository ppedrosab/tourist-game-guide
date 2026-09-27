#!/usr/bin/env python3
"""
Fondos de las rutas que completan las ciudades (ver docs/CIUDADES_QUE_FALTAN.md).
Málaga: iglesia de Santiago, plaza de toros de La Malagueta, Palacio de Buenavista (Museo Picasso).

Uso: python3 scripts/art/completar_scenes.py [escena ...] && python3 scripts/art/render_layers.py <prefijo> && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WHITE, YELLOW, PINK, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, far_city, fx, doc)
from sevilla_scenes import ALMAGRA, BRICK
from cordoba_scenes import ground

RED = "#D8412F"


def brick_tower(x, y, w, h, c=BRICK):
    """Torre mudéjar de ladrillo con paños de sebka y campanario."""
    col, dk, lt = c
    s = (f'<path d="M{x} {y + h}V{y}H{x + w}V{y + h}Z" fill="{col}" stroke="{INK}" stroke-width="1.8"/>'
         f'<path d="M{x + w * .62} {y}H{x + w}V{y + h}H{x + w * .62}Z" fill="{dk}" opacity=".45"/>')
    # paños de rombos (sebka)
    for k in range(3):
        yy = y + 40 + k * 46
        s += "".join(f'<path d="M{f(x + 8 + j * 14)} {yy + 14}L{f(x + 15 + j * 14)} {yy}L{f(x + 22 + j * 14)} {yy + 14}L{f(x + 15 + j * 14)} {yy + 28}Z" fill="none" stroke="{dk}" stroke-width="1.6"/>'
                     for j in range(int((w - 16) // 14)))
    # campanario
    s += (f'<path d="M{x - 4} {y}H{x + w + 4}V{y - 8}H{x - 4}Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M{x + 6} {y - 8}V{y - 50}H{x + w - 6}V{y - 8}Z" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M{x + w / 2 - 9} {y - 12}V{y - 36}Q{x + w / 2} {y - 46} {x + w / 2 + 9} {y - 36}V{y - 12}Z" fill="#3A2A26" stroke="{INK}" stroke-width="1.4"/>'
          f'<circle cx="{x + w / 2}" cy="{y - 24}" r="5" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
          f'<path d="M{x + 2} {y - 50}L{x + w / 2} {y - 70}L{x + w - 2} {y - 50}Z" fill="#9C4A2E" stroke="{INK}" stroke-width="1.6"/>')
    return s


def malaga_santiago():
    p = "msg"; sun = (310, 110)
    far = f'<g id="far">{far_city(260, 211, towers=3)}</g>'
    tower = brick_tower(150, 150, 70, 180)
    nave = (f'<path d="M210 390V230H372V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M204 232L290 196L378 232Z" fill="#B5553A" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M262 390V300Q290 272 318 300V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M254 300Q290 262 326 300" fill="none" stroke="{BRICK[1]}" stroke-width="6"/>'
            + window(230, 250, 16, 30, shutters=False, arch=True) + window(338, 250, 16, 30, shutters=False, arch=True))
    street = house(-30, 200, 120, 190, YELLOW, floors=3, cols=2) + house(90, 250, 70, 140, WHITE, floors=2, cols=1)
    mid = f'<g id="mid">{street}{tower}{nave}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + lamp(60, 480) + lamp(340, 480)
            + person(120, 452, 1, SEA) + person(230, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Iglesia de Santiago", [sky(p, sun, [(80, 80, .8)], [(240, 60), (260, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def malaga_toros():
    p = "mto"; sun = (80, 120)
    far = f'<g id="far">{far_city(250, 311, towers=2)}<path d="M260 250Q320 180 400 200V260H260Z" fill="#8FB39A" stroke="{INK}" stroke-width="1.4"/></g>'
    # fachada curva de la plaza: dos pisos de arcos
    ring = (f'<path d="M-10 390V230Q195 190 400 230V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M-10 230Q195 190 400 230V222Q195 180 -10 222Z" fill="{ALMAGRA[0]}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M-10 310Q195 276 400 310" fill="none" stroke="{ALMAGRA[0]}" stroke-width="6"/>')
    for k in range(9):
        x = 6 + k * 44
        yy = 236 - (1 - ((x - 195) / 205) ** 2) * 36
        ring += (f'<path d="M{f(x)} {f(yy + 64)}V{f(yy + 30)}Q{f(x + 14)} {f(yy + 14)} {f(x + 28)} {f(yy + 30)}V{f(yy + 64)}Z" fill="#B97A4E" stroke="{INK}" stroke-width="1.2"/>'
                 f'<path d="M{f(x)} {f(yy + 150)}V{f(yy + 106)}Q{f(x + 14)} {f(yy + 90)} {f(x + 28)} {f(yy + 106)}V{f(yy + 150)}Z" fill="#7A4A30" stroke="{INK}" stroke-width="1.2"/>')
    gate = (f'<path d="M160 390V300Q195 268 230 300V390Z" fill="#3A2A26" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M150 300Q195 256 240 300" fill="none" stroke="{GOLD}" stroke-width="5"/>'
            f'<path d="M170 262H220V250H170Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{ring}{gate}{ground(386, "#E8D3A6")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E8D3A6", line="#D2BA88")}' + palm(40, 520, 150, -6) + palm(360, 520, 140, 8)
            + person(130, 456, 1, "#2B2A33", hat=True) + person(270, 452, .95, RED, dress=True) + "</g>")
    return doc(p, "Plaza de toros de La Malagueta", [sky(p, sun, [(260, 70, .9)], [(120, 60)]), far, mid, near, fx(p, sun, 420)])


def malaga_buenavista():
    p = "mbv"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 97, towers=2)}</g>'
    c, dk, lt = STONE
    palace = (f'<path d="M30 390V210H300V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M24 210H306V198H24Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/>'
              # torre mirador
              f'<path d="M230 210V120H300V210Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M224 120H306V110H224Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 200V150Q{x + 9} 138 {x + 18} 150V200Z" fill="#3A2A26" stroke="{INK}" stroke-width="1.2"/>' for x in (240, 266))
              # portada renacentista
              + f'<path d="M120 390V290H200V390Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M136 390V320Q160 298 184 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M116 290H204V280H116Z" fill="{dk}" stroke="{INK}" stroke-width="1.4"/>'
              f'<circle cx="160" cy="262" r="12" fill="{dk}" stroke="{INK}" stroke-width="1.4"/>'
              + "".join(window(x, 236, 18, 32, shutters=False, balcony=True, sw=1.1) for x in (50, 90, 210))
              + f'<path d="M60 344H104V360H60Z" fill="{RED}" stroke="{INK}" stroke-width="1.2"/>'  # banderola del museo
              f'<path d="M66 350H98" stroke="{PAPER}" stroke-width="2"/>')
    street = house(300, 190, 110, 200, PINK, floors=3, cols=2)
    mid = f'<g id="mid">{palace}{street}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + tree(20, 500, 36)
            + person(240, 456, 1, SEA) + person(280, 452, .9, CLAY, dress=True) + person(110, 460, 1, "#34495E") + "</g>")
    return doc(p, "Museo Picasso Málaga", [sky(p, sun, [(90, 70, .8)], [(200, 50), (218, 44, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"malaga_santiago": malaga_santiago, "malaga_toros": malaga_toros, "malaga_buenavista": malaga_buenavista}

if __name__ == "__main__":
    for key in sys.argv[1:] or SCENES:
        open(os.path.join(OUT, f"fondo_{key}.svg"), "w").write(SCENES[key]())
    print("fondos:", ", ".join(sys.argv[1:] or SCENES))
