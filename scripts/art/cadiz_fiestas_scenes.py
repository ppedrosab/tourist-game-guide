#!/usr/bin/env python3
"""
Fondos de la ruta de Carnaval de Cádiz. Reutiliza La Viña, San Antonio, Mina y la Catedral;
aquí van el Gran Teatro Falla, la calle de María la Hierbabuena, el carrusel de coros y
Puertas de Tierra.

Uso: python3 scripts/art/cadiz_fiestas_scenes.py && python3 scripts/art/render_layers.py cadiz_falla (etc.)
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, SHUT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from cadiz_gastro_scenes import garlands
from granada_scenes import horseshoe

BRICK = ("#B5553A", "#96432C", "#CF7458")
VIOLET = "#6E2C5E"


def confetti(n=40, seed=1):
    return "".join(f'<rect x="{(i * 53 + seed * 17) % 390}" y="{(i * 97 + seed * 31) % 380 + 20}" width="4" height="4" '
                   f'transform="rotate({i * 37} {(i * 53 + seed * 17) % 390} {(i * 97 + seed * 31) % 380 + 20})" '
                   f'fill="{[CLAY, GOLD, SEA, VIOLET][i % 4]}" opacity=".8"/>' for i in range(n))


def costumed(x, y, s=1.0, hat=GOLD, body=VIOLET):
    """Figurante disfrazado, con sombrero de color."""
    return (person(x, y, s, body)
            + f'<path d="M{f(x - 6 * s)} {f(y - 20 * s)}L{f(x + 6 * s)} {f(y - 20 * s)}L{f(x)} {f(y - 30 * s)}Z" fill="{hat}" stroke="{INK}" stroke-width=".8"/>')


def falla():
    p = "cfa"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 81)}</g>'
    c, cd, cl = BRICK
    x0, w = 30, 330
    fac = (f'<path d="M{x0} 150L{x0 + w} 150L{x0 + w} 400L{x0} 400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M{x0 + w - 36} 152L{x0 + w} 152L{x0 + w} 400L{x0 + w - 36} 400Z" fill="{cd}" opacity=".6"/>'
           # hiladas de ladrillo
           + "".join(f'<path d="M{x0} {y}H{x0 + w}" stroke="{cd}" stroke-width=".8" opacity=".6"/>' for y in range(160, 400, 12))
           # cuerpo central más alto con frontón y remate
           + f'<path d="M120 400L120 110L270 110L270 400Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M112 110L278 110L278 98L112 98Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 98L{x} 86L{x + 10} 86L{x + 10} 98" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.1"/>' for x in range(116, 272, 18))
           # tres grandes arcos de herradura en la planta baja
           + "".join(horseshoe(x, 300, 44, 100, "#4A2A20", 1.6) + f'<path d="M{x - 4} 300Q{x + 22} 262 {x + 48} 300" fill="none" stroke="{STONE[2]}" stroke-width="4"/>' for x in (132, 173, 214))
           # ventanas geminadas arriba
           + "".join(horseshoe(x, 170, 18, 50, WIN if x != 170 else LIT, 1.2) + horseshoe(x + 20, 170, 18, 50, WIN, 1.2) for x in (138, 186, 234 - 10))
           + "".join(horseshoe(x, 200, 26, 80, WIN, 1.3) for x in (50, 90, 294, 326))
           # rosetón
           + f'<circle cx="195" cy="136" r="14" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/><circle cx="195" cy="136" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
           # cenefa de azulejo
           + f'<path d="M{x0} 250H{x0 + w}V258H{x0}Z" fill="{SEA}" opacity=".85"/>'
           + "".join(f'<path d="M{x} 254l4 -4l4 4l-4 4Z" fill="{PAPER}"/>' for x in range(x0 + 4, x0 + w - 6, 14)))
    mid = f'<g id="mid">{fac}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + palm(20, 480, 250, 14, 1.0) + palm(372, 480, 240, -12, 1.0)
            + costumed(110, 444, 1, GOLD, VIOLET) + costumed(130, 448, .95, CLAY, SEA) + costumed(270, 444, 1, SEA, CLAY) + costumed(292, 450, 1.05, VIOLET, GOLD)
            + lamp(340, 540, 160) + "</g>")
    fxg = fx(p, sun, 420).replace('<g id="fx">', f'<g id="fx">{garlands(60, 90, seed=1)}{confetti(30, 2)}')
    return doc(p, "Gran Teatro Falla", [sky(p, sun, [(80, 60, .8)], []), far, mid, near, fxg])


def sacramento():
    p = "csa"; sun = (200, 80)
    far = f'<g id="far">{far_city(240, 83, towers=4)}</g>'
    c, cd, cl = BRICK
    # a la izquierda, el muro lateral del Falla; a la derecha, casas
    left = (f'<path d="M-30 90L150 150L150 440L-30 480Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M-30 {y}L150 {y + 60 - (y - 90) * .12:.0f}" stroke="{cd}" stroke-width=".8" opacity=".5"/>' for y in range(110, 470, 16))
            + "".join(horseshoe(x, y, 22, 60, WIN, 1.2) for x, y in [(6, 180), (60, 196), (110, 210)])
            # puerta de artistas por donde entran las agrupaciones
            + horseshoe(40, 330, 60, 130, "#4A2A20", 1.6)
            # placa de azulejo con el nombre de la calle
            + f'<path d="M86 290L140 296L140 330L86 326Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M90 296L136 301L136 325L90 321Z" fill="none" stroke="{SEA}" stroke-width="1.4"/>'
            + "".join(f'<path d="M94 {303 + k * 7}L{128 - k * 6} {307 + k * 7}" stroke="{SEA}" stroke-width="1.6"/>' for k in range(3))
            # ramita de hierbabuena en una maceta bajo la placa
            + f'<path d="M104 350H122L120 362H106Z" fill="#C9763F" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="2.6" transform="rotate({r} {x} {y})" fill="#4F8B5A" stroke="{INK}" stroke-width=".8"/>' for x, y, r in [(108, 344, -30), (118, 342, 30), (112, 336, -20), (116, 334, 25)]))
    right = ""
    cols = [WHITE, YELLOW, PINK]
    for k in range(3):
        xa, xb = W + 30 - k * 50 - 60, W + 30 - k * 50
        ta, tb = 130 + k * 36, 110 + k * 36
        bot = 460 - k * 26
        right += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot}L{xa} {bot - 10}Z" fill="{cols[k][0]}" stroke="{INK}" stroke-width="1.6"/>'
        for fl in range(2):
            y = ta + 40 + fl * 100
            right += f'<path d="M{xa + 10} {y}L{xb - 10} {y - 4}L{xb - 10} {y + 44}L{xa + 10} {y + 48}Z" fill="{SHUT}" stroke="{INK}" stroke-width="1.2"/>'
    mid = f'<g id="mid">{left}{right}<rect x="-10" y="436" width="{W + 20}" height="0" fill="none"/></g>'
    near = (f'<g id="near">{floor(p, 430, color="#E0C7A4")}'
            # una agrupación haciendo cola para entrar
            + "".join(costumed(x, 452 + (x % 3) * 2, .9, VIOLET, GOLD) for x in (170, 186, 202, 218, 234))
            + lamp(350, 550, 170) + "</g>")
    return doc(p, "Calle María la Hierbabuena", [sky(p, sun, [(300, 50, .8)], [(240, 40), (260, 30, .8)]), far, mid, near, fx(p, sun, 430)])


def coros():
    p = "cco"; sun = (310, 100)
    far = f'<g id="far">{far_city(230, 85, towers=8)}<rect x="0" y="230" width="{W}" height="100" fill="#E3B48E"/></g>'
    arc = (f'<path d="M-10 190L400 190L400 340L-10 340Z" fill="{YELLOW[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M-14 190L404 190L404 178L-14 178Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 340L{x} 226Q{x + 20} 206 {x + 40} 226L{x + 40} 340Z" fill="#5E4232" stroke="{INK}" stroke-width="1.4"/>' for x in range(0, 390, 56))
           + columns(-4, 204, 392, 136, 8, WHITE, 1.3))
    mid = f'<g id="mid">{arc}<rect x="-10" y="336" width="{W + 20}" height="92" fill="#DCC3A0"/></g>'
    # la batea con el coro, en primer plano pero a un lado
    b = (f'<path d="M180 470L380 470L380 430L180 430Z" fill="{SEA}" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M176 430L384 430L376 416H184Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>'
         + "".join(f'<path d="M{x} 416V408" stroke="{INK}" stroke-width="1.2"/>' for x in range(190, 380, 12))
         + f'<circle cx="210" cy="476" r="12" fill="{INK}"/><circle cx="350" cy="476" r="12" fill="{INK}"/>'
         f'<circle cx="210" cy="476" r="5" fill="#9AA3AA"/><circle cx="350" cy="476" r="5" fill="#9AA3AA"/>'
         + "".join(costumed(x, 414, 1.1, "#E9CF8A", c) for x, c in [(200, PAPER), (226, CLAY), (252, PAPER), (278, CLAY), (304, PAPER), (330, CLAY), (356, PAPER)])
         + f'<path d="M150 470L180 450" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M110 470H160V440H130L110 454Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/><circle cx="124" cy="476" r="9" fill="{INK}"/><circle cx="152" cy="476" r="7" fill="{INK}"/>')
    near = (f'<g id="near">{floor(p, 420, color="#E3CBAA")}{b}'
            + person(40, 452, 1, SEA) + person(64, 456, .95, "#6E2C5E", dress=True) + "</g>")
    fxg = fx(p, sun, 420, .25).replace('<g id="fx">', f'<g id="fx">{garlands(150, 170, seed=2)}{confetti(24, 5)}')
    return doc(p, "Carrusel de coros", [sky(p, sun, [(80, 60, .8)], []), far, mid, near, fxg])


def puertas():
    p = "cpt"; sun = (90, 110)
    far = f'<g id="far">{far_city(280, 87, "#E8BC98", "#EDC9A8", towers=3)}</g>'
    sc, scd, scl = ("#E7C98E", "#CFAE70", "#F3DEAE")
    wall = (f'<path d="M-20 240L410 240L410 400L-20 400Z" fill="{sc}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 240V230H{x + 14}V240" fill="{sc}" stroke="{INK}" stroke-width="1.2"/>' for x in range(-16, 400, 26))
            + "".join(f'<path d="M-20 {y}H410" stroke="{scd}" stroke-width="1" opacity=".6"/>' for y in range(256, 400, 16))
            # torreón a la izquierda
            + f'<path d="M40 400V110H110V400Z" fill="{scl}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M92 112H110V400H92Z" fill="{scd}" opacity=".6"/>'
            f'<path d="M34 110H116V100H34Z" fill="{sc}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 100V90H{x + 10}V100" fill="{sc}" stroke="{INK}" stroke-width="1.1"/>' for x in range(36, 114, 16))
            + window(66, 140, 18, 30, shutters=False, arch=True, sw=1.2) + window(66, 210, 18, 30, shutters=False, arch=True, sw=1.2, lit=True)
            + f'<path d="M75 90V60M68 66H82" stroke="{INK}" stroke-width="2"/>'
            # la última viñeta, enganchada en el torreón
            + f'<g transform="rotate(12 96 124)"><rect x="86" y="112" width="22" height="18" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/><path d="M90 126L96 118L102 126Z" fill="{VIOLET}"/></g>'
            # la puerta barroca en el centro
            + f'<path d="M180 400V270H300V400Z" fill="{scl}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M172 270L240 236L308 270Z" fill="{sc}" stroke="{INK}" stroke-width="1.6"/>'
            + columns(192, 290, 96, 110, 2, STONE, 1.3)
            + f'<path d="M212 400V330Q240 300 268 330V400Z" fill="#4A342A" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M226 282H254V300H226Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{wall}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#D8C09A"/></g>'
    # la Bruja Piti, esperando su quema, sobre una pila de leña
    bruja = (f'<path d="M300 520L380 520L370 500L310 500Z" fill="#8A6243" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 500L{x + 16} 486" stroke="#6E4C33" stroke-width="4"/>' for x in (312, 330, 348))
             + f'<path d="M340 500L326 430L354 430Z" fill="{VIOLET}" stroke="{INK}" stroke-width="1.8"/>'
             f'<circle cx="340" cy="420" r="11" fill="#9BB58A" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M322 414L358 414L340 380Z" fill="#2B2A33" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M318 414H362" stroke="#2B2A33" stroke-width="4"/>'
             f'<path d="M354 440L372 470" stroke="#8A6243" stroke-width="3"/><path d="M366 462L380 474L374 478Z" fill="#C9A77E" stroke="{INK}" stroke-width="1"/>'
             f'<circle cx="336" cy="418" r="1.4" fill="{INK}"/><circle cx="344" cy="418" r="1.4" fill="{INK}"/><path d="M336 424Q340 427 344 424" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    near = (f'<g id="near">{floor(p, 420)}{bruja}'
            + person(140, 446, .95, SEA) + costumed(166, 450, 1, GOLD, CLAY) + person(250, 444, .9, "#6E2C5E", dress=True)
            + palm(20, 480, 230, 12, .95) + "</g>")
    # el levante: rachas de viento que cruzan la escena de este a oeste
    wind = "".join(f'<path d="M{x} {y}q-30 -8 -60 0t-60 0" fill="none" stroke="#FFFFFF" stroke-width="2.4" opacity=".55"/>' for x, y in [(400, 160), (360, 210), (420, 300), (330, 350)])
    fxg = fx(p, sun, 420).replace('<g id="fx">', f'<g id="fx">{wind}')
    return doc(p, "Puertas de Tierra", [sky(p, sun, [(300, 70, .9), (200, 40, .6)], [(250, 50), (270, 40, .8)]), far, mid, near, fxg])


SCENES = {"falla": falla, "sacramento": sacramento, "coros": coros, "puertas": puertas}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_cadiz_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos del Carnaval generados:", ", ".join(SCENES))
