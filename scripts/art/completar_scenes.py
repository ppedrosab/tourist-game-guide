#!/usr/bin/env python3
"""
Fondos de las rutas que completan las ciudades (ver docs/CIUDADES_QUE_FALTAN.md).
Málaga: iglesia de Santiago, plaza de toros de La Malagueta, Palacio de Buenavista (Museo Picasso).
Cádiz: arco del Pópulo, teatro romano, Casa del Almirante, Casa de las Cuatro Torres, castillo de Santa Catalina.
Córdoba: plaza de Tiberíades (Maimónides), muralla de la calle Cairuán (Averroes), Museo Arqueológico.
Sevilla: palacio de Mañara, plaza de los Refinadores (Don Juan), la Maestranza, Hospital de la Caridad.
Granada: Carrera del Darro, San Juan de los Reyes (alminar), cuevas y abadía del Sacromonte.
Jaén: Museo de Jaén, monasterio de Santa Clara, San Andrés (Judería), castillo de Santa Catalina.

Uso: python3 scripts/art/completar_scenes.py [escena ...] && python3 scripts/art/render_layers.py <prefijo> && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WHITE, YELLOW, PINK, MINT, STONE, OUT, W,
                          f, sky, window, house, mirador, palm, lamp, person, floor, bench, tree, far_city, fx, doc)
from sevilla_scenes import ALMAGRA, BRICK, ALBERO, giralda, river
from cordoba_scenes import ground, lime_wall, flowerpots, statue, battlements, LIME, OCHRE, POTBLUE
from granada_scenes import horseshoe, cypress, alhambra_hill, sierra, albaicin_houses, CAL, ROJA, TEJA
from jaen_scenes import far_jaen, olive_hills, JSTONE, ochre_house
from sevilla_scenes import orange_tree

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



def cadiz_populo():
    p = "cpo"; sun = (300, 110)
    far = f'<g id="far">{far_city(250, 71, towers=3)}</g>'
    c, dk, lt = STONE
    wall = (f'<path d="M-10 390V200H400V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 200V186H{x + 16}V200" fill="{lt}" stroke="{INK}" stroke-width="1.4"/>' for x in range(-6, 400, 30))
            + f'<path d="M140 390V280Q195 220 250 280V390Z" fill="#6E5A48" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M150 390V284Q195 234 240 284V390Z" fill="#3A2E28"/>'
            f'<path d="M128 280Q195 206 262 280" fill="none" stroke="{dk}" stroke-width="8"/>'
            # capillita sobre el arco
            f'<path d="M176 236H214V210H176Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><path d="M172 210L195 196L218 210Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>'
            + house(-20, 120, 120, 80, YELLOW, floors=1, cols=2, door=False) + house(300, 110, 110, 90, PINK, floors=1, cols=2, door=False))
    mid = f'<g id="mid">{wall}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + lamp(60, 480) + lamp(330, 480)
            + person(195, 440, .9, SEA) + person(120, 456, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Arco del Pópulo", [sky(p, sun, [(80, 70, .8)], [(220, 60)]), far, mid, near, fx(p, sun, 420)])


def cadiz_teatro():
    p = "cte"; sun = (90, 120)
    far = f'<g id="far">{far_city(240, 131, towers=4)}</g>'
    c, dk, lt = STONE
    # gradas del teatro en semicírculo, con las casas del Pópulo detrás
    back = house(-20, 170, 130, 150, WHITE, floors=2, cols=2) + house(110, 160, 150, 160, YELLOW, floors=2, cols=3) + house(260, 175, 150, 145, PINK, floors=2, cols=2)
    cavea = ""
    for k in range(6):
        y = 300 + k * 16
        cavea += f'<path d="M{-10 + k * 18} {y}Q195 {y + 60 - k * 6} {400 - k * 18} {y}" fill="none" stroke="{INK}" stroke-width="{f(9 - k * .6)}"/>'
        cavea += f'<path d="M{-10 + k * 18} {y}Q195 {y + 60 - k * 6} {400 - k * 18} {y}" fill="none" stroke="{lt if k % 2 else c}" stroke-width="{f(6 - k * .5)}"/>'
    orchestra = f'<path d="M100 400Q195 360 290 400Z" fill="{dk}" stroke="{INK}" stroke-width="1.6"/>'
    mid = f'<g id="mid">{back}<path d="M-10 290H400V410H-10Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>{cavea}{orchestra}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}'
            + "".join(f'<path d="M{x} 460V420H{x + 16}V460Z" fill="{lt}" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 4} 420H{x + 20}V412H{x - 4}Z" fill="{dk}" stroke="{INK}" stroke-width="1.2"/>' for x in (40, 334))
            + person(170, 450, 1, SEA) + person(230, 454, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Teatro romano de Cádiz", [sky(p, sun, [(260, 70, .8)], [(150, 70)]), far, mid, near, fx(p, sun, 420)])


def cadiz_almirante():
    p = "cal"; sun = (310, 100)
    far = f'<g id="far">{far_city(250, 43, towers=2)}</g>'
    front = (f'<path d="M40 390V170H350V390Z" fill="#F4EFE6" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M34 170H356V156H34Z" fill="#E3D5BE" stroke="{INK}" stroke-width="1.6"/>'
             # portada de mármol rojo y blanco en dos cuerpos
             f'<path d="M140 390V200H250V390Z" fill="#C0584A" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M156 390V310Q195 280 234 310V390Z" fill="#4A2E24" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 390V226" stroke="#F4EFE6" stroke-width="7"/><path d="M{x} 390V226" stroke="{INK}" stroke-width=".8" opacity=".5"/>' for x in (148, 242))
             + f'<path d="M136 270H254V260H136Z" fill="#F4EFE6" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M170 250V214H220V250Z" fill="#F4EFE6" stroke="{INK}" stroke-width="1.2"/><circle cx="195" cy="232" r="10" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
             + "".join(window(x, 210, 20, 36, shutters=False, balcony=True, sw=1.1) for x in (60, 100, 280, 320))
             + mirador(290, 110, 40, 60, WHITE))
    mid = f'<g id="mid">{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + tree(20, 500, 34) + tree(370, 500, 34)
            + person(110, 454, 1, "#34495E") + person(290, 458, .95, SEA, dress=True) + "</g>")
    return doc(p, "Casa del Almirante", [sky(p, sun, [(90, 80, .8)], [(200, 60)]), far, mid, near, fx(p, sun, 420)])


def cadiz_cuatrotorres():
    p = "c4t"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 211, towers=3)}</g>'
    front = house(30, 190, 330, 200, WHITE, floors=3, cols=5)
    towers = "".join(mirador(x, 130, 34, 60, WHITE) for x in (40, 130, 226, 316))
    mid = f'<g id="mid">{towers}{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + palm(30, 520, 160, -6) + bench(250, 470)
            + person(140, 452, 1, CLAY) + person(200, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "Casa de las Cuatro Torres", [sky(p, sun, [(280, 70, .8)], [(160, 60), (178, 52, .8)]), far, mid, near, fx(p, sun, 420)])


def cadiz_santacatalina():
    p = "csc"; sun = (220, 150)
    far = f'<g id="far"><rect x="-10" y="290" width="{W + 20}" height="20" fill="#E1B28C"/></g>'
    sea = (f'<g id="sea"><rect x="-10" y="300" width="{W + 20}" height="120" fill="url(#{p}sea)"/>'
           + "".join(f'<path d="M{x} {y}L{x + ln} {y}" stroke="#E6F2EF" stroke-width="1.6" opacity=".7"/>' for x, y, ln in [(40, 330, 30), (220, 318, 24), (300, 350, 34), (120, 372, 22)])
           + "</g>")
    c, dk, lt = STONE
    # baluarte en punta de estrella con garita
    castle = (f'<path d="M-10 420V300L120 262L200 300L200 420Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M120 262L200 300L200 420L120 420Z" fill="{dk}" opacity=".4"/>'
              f'<path d="M-10 300L120 262L200 300" fill="none" stroke="{lt}" stroke-width="5"/>'
              f'<path d="M108 262V232Q120 220 132 232V262Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/><path d="M104 232L120 218L136 232Z" fill="{dk}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M40 420V360Q60 340 80 360V420Z" fill="#4A3A30" stroke="{INK}" stroke-width="1.6"/>')
    mid = f'<g id="mid">{castle}</g>'
    near = (f'<g id="near"><rect x="-10" y="412" width="{W + 20}" height="150" fill="#EBD3AC"/>'
            + person(260, 446, 1, CLAY, dress=True) + person(300, 452, .9, SEA) + palm(370, 460, 200, -8) + "</g>")
    return doc(p, "Castillo de Santa Catalina", [sky(p, sun, [(80, 90, .9)], [(160, 90), (300, 110, .8)]), far, sea, mid, near, fx(p, sun, 412, .25)])


def cordoba_tiberiades():
    p = "ktb"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 97, towers=2)}</g>'
    back = (lime_wall(-20, 180, 150, 220) + flowerpots(0, 120, 210, 3)
            + lime_wall(250, 170, 160, 230) + flowerpots(262, 392, 200, 3, seed=2)
            + lime_wall(120, 220, 140, 180)
            + f'<path d="M176 400V336Q190 320 204 336V400Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.6"/>'
            + window(140, 260, 18, 34, shutters=False, arch=True) + window(226, 260, 18, 34, shutters=False, arch=True))
    mid = f'<g id="mid">{back}{ground(398, "#D8C6A6")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D5C29E", line="#C1AB85")}'
            + statue(195, 470, 1.15, seated=True) + orange_tree(40, 486, 30) + orange_tree(352, 486, 28)
            + person(120, 452, .95, "#5A3E6E") + person(270, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "Plaza de Tiberíades", [sky(p, sun, [(90, 70, .8)], [(220, 56)]), far, mid, near, fx(p, sun, 420, .25)])


def cordoba_averroes():
    p = "kav"; sun = (100, 110)
    far = f'<g id="far">{far_city(250, 53, towers=3)}</g>'
    c, cd, cl = OCHRE
    wall = (f'<path d="M150 380V200H410V380Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(150, 410, 200, c)
            + "".join(f'<path d="M150 {y}H410" stroke="{cd}" stroke-width="1" opacity=".6"/>' for y in range(216, 380, 14))
            + f'<path d="M250 380V160H320V380Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(250, 320, 160, cl)
            + horseshoe(262, 300, 46, 80, "#5E4232", 1.6)
            + f'<path d="M-20 380V250L150 230V380Z" fill="{cd}" stroke="{INK}" stroke-width="1.6"/>' + battlements(-20, 150, 250, cd))
    water = (f'<rect x="-10" y="380" width="{W + 20}" height="22" fill="#8FB9B4" stroke="{INK}" stroke-width="1.2"/>'
             + "".join(f'<path d="M{x} 390h22" stroke="#E6F2EF" stroke-width="1.4" opacity=".8"/>' for x in (30, 150, 280)))
    mid = f'<g id="mid">{wall}{water}{ground(402, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + cypress(360, 480, 190, 16)
            + statue(90, 476, 1.2, seated=True) + person(200, 450, .95, SEA) + person(246, 454, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Monumento a Averroes", [sky(p, sun, [(290, 70, .8)], [(200, 50), (218, 42, .8)]), far, mid, near, fx(p, sun, 420)])


def cordoba_arqueologico():
    p = "kaq"; sun = (310, 110)
    far = f'<g id="far">{far_city(250, 211, towers=3)}</g>'
    c, dk, lt = STONE
    # palacio renacentista de los Páez de Castillejo: portada con columnas y frontón
    front = (f'<path d="M20 390V180H370V390Z" fill="{LIME[0]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M14 180H376V166H14Z" fill="{LIME[1]}" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M130 390V190H260V390Z" fill="{lt}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} 390V214" stroke="{c}" stroke-width="10"/><path d="M{x - 5} 390V214M{x + 5} 390V214" stroke="{INK}" stroke-width="1"/>' for x in (146, 244))
             + f'<path d="M166 390V300Q195 270 224 300V390Z" fill="#4A3A30" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M126 214H264V202H126Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
             f'<path d="M150 250H240V282H150Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M160 202L195 176L230 202Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(window(x, 220, 20, 36, shutters=False, balcony=True, sw=1.1) for x in (44, 84, 290, 330))
             + "".join(window(x, 300, 20, 36, shutters=False, sw=1.1) for x in (44, 84, 290, 330)))
    mid = f'<g id="mid">{front}{ground(386, "#E3CFAA")}</g>'
    # vitrina en el suelo con restos del teatro romano
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}'
            + f'<path d="M120 476H270L284 500H106Z" fill="#9FC3C4" stroke="{INK}" stroke-width="1.6" opacity=".9"/>'
            + "".join(f'<path d="M{130 + k * 10} {482 + k * 5}Q195 {476 + k * 5} {260 - k * 10} {482 + k * 5}" fill="none" stroke="{dk}" stroke-width="2"/>' for k in range(3))
            + orange_tree(40, 490, 28) + orange_tree(350, 490, 30)
            + person(90, 452, .95, CLAY) + person(300, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "Museo Arqueológico de Córdoba", [sky(p, sun, [(90, 80, .8)], [(180, 60)]), far, mid, near, fx(p, sun, 420)])


def azulejo_panel(x, y, w, h):
    """Paño de azulejo azul y blanco, sin figuras."""
    s = f'<path d="M{x} {y}H{x + w}V{y + h}H{x}Z" fill="#F4F1E8" stroke="{INK}" stroke-width="1.4"/>'
    s += f'<path d="M{x + 4} {y + 4}H{x + w - 4}V{y + h - 4}H{x + 4}Z" fill="none" stroke="#2F5F9E" stroke-width="2"/>'
    s += f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 4}" ry="{h / 3.4}" fill="#8FB1D9" stroke="#2F5F9E" stroke-width="1.4"/>'
    return s


def sevilla_manara():
    p = "smn"; sun = (90, 110)
    far = f'<g id="far">{far_city(250, 91, towers=3)}</g>'
    c, dk, lt = ALMAGRA
    front = (f'<path d="M10 390V170H380V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M4 170H386V156H4Z" fill="{lt}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 390V170" stroke="{c}" stroke-width="10"/><path d="M{x - 5} 390V170M{x + 5} 390V170" stroke="{INK}" stroke-width=".8"/>' for x in (14, 376))
             # portada de mármol con columnas pareadas y escudo
             + f'<path d="M140 390V206H250V390Z" fill="#EDE6DA" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} 390V222" stroke="#D8CFC0" stroke-width="8"/><path d="M{x - 4} 390V222M{x + 4} 390V222" stroke="{INK}" stroke-width=".9"/>' for x in (152, 166, 224, 238))
             + f'<path d="M176 390V298Q195 276 214 298V390Z" fill="#4A2E24" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M136 222H254V210H136Z" fill="#D8CFC0" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M180 262Q195 238 210 262V282H180Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/><path d="M184 258H206M183 266H207M184 274H206" stroke="{c}" stroke-width="3"/>'
             + "".join(window(x, 210, 22, 40, shutters=False, balcony=True, sw=1.1) for x in (40, 90, 280, 330))
             + "".join(window(x, 300, 22, 40, shutters=True, sw=1.1) for x in (40, 90, 280, 330)))
    mid = f'<g id="mid">{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + lamp(60, 480) + lamp(330, 480)
            + person(120, 452, 1, "#22222A") + person(260, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Palacio de Mañara", [sky(p, sun, [(290, 70, .8)], [(200, 56)]), far, mid, near, fx(p, sun, 420)])


def sevilla_refinadores():
    p = "srf"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 97, towers=2)}{giralda(60, 250, 40, 20, 1.4, soft=True)}</g>'
    back = (house(-20, 200, 140, 190, WHITE, floors=2, cols=2) + house(120, 220, 130, 170, YELLOW, floors=2, cols=2)
            + house(250, 190, 160, 200, PINK, floors=2, cols=3))
    mid = f'<g id="mid">{back}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}'
            + orange_tree(40, 486, 30) + orange_tree(350, 490, 30) + palm(300, 470, 150, 4)
            + statue(195, 480, 1.2) + person(110, 452, .95, SEA) + person(260, 456, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Plaza de los Refinadores", [sky(p, sun, [(90, 70, .8)], [(180, 56), (198, 48, .8)]), far, mid, near, fx(p, sun, 420, .25)])


def sevilla_maestranza():
    p = "smz"; sun = (300, 110)
    far = f'<g id="far">{far_city(250, 211, towers=2)}{giralda(340, 250, 40, 20, 1.4, soft=True)}</g>'
    c, dk, lt = ALBERO
    ring = (f'<path d="M-10 390V220Q195 196 400 220V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M-10 220Q195 196 400 220V210Q195 186 -10 210Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 300V262Q{x + 11} 250 {x + 22} 262V300Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for x in range(-4, 400, 34))
            + f'<path d="M-10 316Q195 300 400 316" fill="none" stroke="{c}" stroke-width="10"/>'
            # Puerta del Príncipe
            + f'<path d="M140 390V230H250V390Z" fill="{lt}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M166 390V310Q195 282 224 310V390Z" fill="#3A2E28" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 390V246" stroke="{c}" stroke-width="8"/><path d="M{x - 4} 390V246M{x + 4} 390V246" stroke="{INK}" stroke-width=".8"/>' for x in (152, 238))
            + f'<path d="M136 246H254V234H136Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/><path d="M170 234Q195 206 220 234Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{ring}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + tree(30, 500, 34) + tree(360, 500, 32)
            + person(110, 452, 1, "#22222A") + person(280, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Real Maestranza", [sky(p, sun, [(90, 70, .8)], [(200, 60)]), far, mid, near, fx(p, sun, 420)])


def sevilla_caridad():
    p = "scd"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 53, towers=3)}</g>'
    c, dk, lt = ALMAGRA
    front = (f'<path d="M100 390V170H290V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} 390V170" stroke="{c}" stroke-width="10"/><path d="M{x - 5} 390V170M{x + 5} 390V170" stroke="{INK}" stroke-width=".8"/>' for x in (104, 286))
             # espadaña
             + f'<path d="M150 170V110H240V170Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/><path d="M146 110Q195 80 244 110Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M184 150V124Q195 112 206 124V150Z" fill="#3A2E28" stroke="{INK}" stroke-width="1.4"/><circle cx="195" cy="136" r="5" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
             + azulejo_panel(170, 176, 50, 60) + azulejo_panel(118, 196, 36, 46) + azulejo_panel(236, 196, 36, 46)
             + azulejo_panel(118, 260, 36, 46) + azulejo_panel(236, 260, 36, 46)
             + f'<path d="M172 390V300Q195 278 218 300V390Z" fill="#4A2E24" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M160 256H230V246H160Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>')
    # naves de las atarazanas a los lados, de ladrillo
    b, bd, bl = BRICK
    sides = "".join(f'<path d="M{x} 390V250H{x + 100}V390Z" fill="{b}" stroke="{INK}" stroke-width="1.6"/>'
                    + "".join(f'<path d="M{x + 10 + k * 30} 390V320Q{x + 22 + k * 30} 300 {x + 34 + k * 30} 320V390Z" fill="{bd}" stroke="{INK}" stroke-width="1.2"/>' for k in range(3))
                    for x in (-10, 300))
    mid = f'<g id="mid">{sides}{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}'
            + statue(60, 480, 1.1) + person(250, 452, 1, SEA) + person(300, 456, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Hospital de la Caridad", [sky(p, sun, [(300, 70, .8)], [(230, 56)]), far, mid, near, fx(p, sun, 420)])


def chumbera(x, base, s=1.0):
    """Chumbera de las cuestas del Sacromonte."""
    out = ""
    for dx, dy, r in [(0, -18, 14), (-14, -38, 11), (12, -42, 12), (-2, -60, 10), (22, -64, 9)]:
        out += f'<ellipse cx="{f(x + dx * s)}" cy="{f(base + dy * s)}" rx="{f(r * .8 * s)}" ry="{f(r * s)}" fill="#6E9F5A" stroke="{INK}" stroke-width="1.2"/>'
    return out + "".join(f'<circle cx="{f(x + dx * s)}" cy="{f(base + dy * s)}" r="{f(2.6 * s)}" fill="{CLAY}"/>' for dx, dy in [(-6, -72), (18, -76), (-20, -48)])


def granada_darro():
    p = "gdr"; sun = (100, 110)
    far = f'<g id="far">{sierra(170)}{alhambra_hill(190)}</g>'
    houses = (house(-30, 200, 120, 150, CAL, floors=2, cols=2) + house(90, 220, 90, 130, YELLOW, floors=2, cols=1)
              + f'<path d="M-10 350H200V360H-10Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.2"/>')
    sea = (f'<g id="sea">{river(p, 360, 410)}'
           # puente de Cabrera, de piedra, de un ojo
           + f'<path d="M200 410V376Q246 336 292 376V410H312V350H180V410Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.6"/>'
           + f'<path d="M176 350H316V342H176Z" fill="#DCC7A0" stroke="{INK}" stroke-width="1.4"/>'
           + tree(360, 350, 30, "#4F7F5A", "#3D6647") + "</g>")
    mid = f'<g id="mid">{houses}</g>'
    near = (f'<g id="near"><rect x="-10" y="406" width="{W + 20}" height="170" fill="#D9C7A8"/>'
            f'<path d="M-10 406L400 406L400 418L-10 418Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#BFAE8E"/>' for x in range(10, 390, 24) for y in (450, 490, 530))
            + person(120, 452, .95, "#2E5E3E") + person(270, 456, .9, CLAY, dress=True) + lamp(40, 540, 170) + "</g>")
    return doc(p, "Carrera del Darro", [sky(p, sun, [(290, 60, .8)], [(220, 50)]), far, mid, sea, near, fx(p, sun, 406, .25)])


def granada_sanjuan():
    p = "gsj"; sun = (300, 100)
    far = f'<g id="far">{albaicin_houses(250, seed=3, soft=True)}</g>'
    minaret = brick_tower(210, 150, 64, 190, ("#D7A27A", "#B98260", "#E8C3A2"))
    church = (f'<path d="M20 390V240H214V390Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M14 242L117 206L220 242Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M92 390V310Q117 286 142 310V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              + window(46, 268, 16, 30, shutters=False, arch=True) + window(172, 268, 16, 30, shutters=False, arch=True)
              + house(274, 230, 130, 160, CAL, floors=2, cols=2))
    mid = f'<g id="mid">{church}{minaret}{ground(386, "#DCCBAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C7A8", line="#C1AB85")}' + cypress(360, 480, 170, 14)
            + person(110, 450, .95, "#22222A") + person(160, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "San Juan de los Reyes", [sky(p, sun, [(80, 70, .8)], [(150, 60)]), far, mid, near, fx(p, sun, 420)])


def granada_cuevas():
    p = "gcv"; sun = (90, 110)
    far = f'<g id="far">{sierra(180)}{alhambra_hill(230, soft=True)}</g>'
    # ladera con cuevas encaladas: fachadas blancas con chimeneas asomando del monte
    hill = f'<path d="M-10 200Q120 170 250 210Q330 230 400 220V400H-10Z" fill="#C9A77A" stroke="{INK}" stroke-width="1.6"/>'
    caves = ""
    for x, y in [(20, 250), (130, 236), (250, 256), (60, 320), (190, 320), (310, 314)]:
        caves += (f'<path d="M{x} {y + 60}V{y + 10}Q{x + 40} {y - 6} {x + 80} {y + 10}V{y + 60}Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.6"/>'
                  f'<path d="M{x + 28} {y + 60}V{y + 32}Q{x + 40} {y + 22} {x + 52} {y + 32}V{y + 60}Z" fill="#2F6F9E" stroke="{INK}" stroke-width="1.4"/>'
                  f'<path d="M{x + 60} {y + 2}V{y - 14}H{x + 68}V{y + 4}" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.2"/>'
                  + "".join(f'<path d="M{x + dx - 5} {y + 30}h10l-2 8h-6Z" fill="{CLAY}" stroke="{INK}" stroke-width=".8"/><circle cx="{x + dx}" cy="{y + 27}" r="3.4" fill="#4F8B5A"/>' for dx in (12, 70)))
    mid = f'<g id="mid">{hill}{caves}{ground(390, "#D9C3A0")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C3A0", line="#C1AB85")}' + chumbera(40, 500, 1.4) + chumbera(350, 496, 1.2)
            + person(170, 450, .95, "#3A3A48") + person(220, 454, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Cuevas del Sacromonte", [sky(p, sun, [(300, 70, .8)], [(220, 60)]), far, mid, near, fx(p, sun, 420)])


def granada_abadia():
    p = "gab"; sun = (300, 110)
    far = f'<g id="far">{sierra(190)}</g>'
    c, dk, lt = STONE
    abbey = (f'<path d="M-10 260Q200 230 400 250V400H-10Z" fill="#8FA86E"/>'
             + f'<path d="M20 390V220H370V390Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M14 222L195 190L376 222Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.8"/>'
             # patio de arcos de ladrillo y portada de piedra sin imágenes
             + "".join(f'<path d="M{x} 390V330Q{x + 16} 312 {x + 32} 330V390Z" fill="#B98260" stroke="{INK}" stroke-width="1.2"/>' for x in (34, 78, 280, 324))
             + f'<path d="M150 390V250H240V390Z" fill="{lt}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M172 390V316Q195 294 218 316V390Z" fill="#4A3A30" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M146 266H244V256H146Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
             + "".join(window(x, 250, 18, 30, shutters=False, sw=1.1) for x in (44, 96, 286, 332))
             + f'<path d="M270 220V150H320V220Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.8"/><path d="M264 152L295 128L326 152Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M286 196V170Q295 160 304 170V196Z" fill="#3A2E28" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{abbey}{ground(386, "#D9C3A0")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C3A0", line="#C1AB85")}' + cypress(30, 480, 190, 16) + cypress(366, 476, 180, 15)
            + chumbera(90, 500, 1.1) + person(200, 450, .95, "#5A2E4E") + person(260, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "Abadía del Sacromonte", [sky(p, sun, [(90, 70, .8)], [(200, 60), (218, 52, .8)]), far, mid, near, fx(p, sun, 420)])


def jaen_museo():
    p = "jmu"; sun = (90, 110)
    far = far_jaen(290, 300)
    c, cd, cl = JSTONE
    # edificio regionalista con la portada renacentista del antiguo Pósito
    front = (f'<path d="M10 390V200H380V390Z" fill="#F1E6D0" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M4 200H386V186H4Z" fill="{cd}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 200V178H{x + 12}V200" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for x in range(20, 380, 40))
             + f'<path d="M140 390V224H250V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} 390V240" stroke="{cl}" stroke-width="9"/><path d="M{x - 4} 390V240M{x + 4} 390V240" stroke="{INK}" stroke-width=".9"/>' for x in (152, 238))
             + f'<path d="M136 240H254V228H136Z" fill="{cd}" stroke="{INK}" stroke-width="1.2"/><path d="M160 228L195 206L230 228Z" fill="{cd}" stroke="{INK}" stroke-width="1.4"/>'
             f'<path d="M170 390V306Q195 280 220 306V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(window(x, 230, 20, 36, shutters=False, balcony=True, sw=1.1) for x in (40, 90, 280, 330))
             + "".join(window(x, 310, 20, 36, shutters=False, sw=1.1) for x in (40, 90, 280, 330)))
    mid = f'<g id="mid">{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + tree(30, 500, 34) + tree(360, 500, 32)
            + person(110, 452, 1, "#9C2A22") + person(280, 456, .95, SEA, dress=True) + "</g>")
    return doc(p, "Museo de Jaén", [sky(p, sun, [(300, 70, .8)], [(220, 56)]), far, mid, near, fx(p, sun, 420)])


def jaen_santaclara():
    p = "jsc"; sun = (300, 110)
    far = far_jaen(290, 110)
    wall = (lime_wall(-20, 220, 250, 180)
            + f'<path d="M110 220V150H170V220Z" fill="{LIME[0]}" stroke="{INK}" stroke-width="1.8"/><path d="M104 152L140 128L176 152Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 206V180Q{x + 8} 170 {x + 16} 180V206Z" fill="#3A2E28" stroke="{INK}" stroke-width="1.2"/>' for x in (118, 144))
            + f'<path d="M40 400V320Q64 300 88 320V400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 260H{x + 14}V280H{x}Z" fill="#3A2E28" stroke="{INK}" stroke-width="1"/>' for x in (150, 190))
            + ochre_house(230, 210, 170, 190, floors=2, cols=2))
    mid = f'<g id="mid">{wall}{ground(398, "#D9C7A8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C7A8", line="#C1AB85")}' + orange_tree(340, 490, 30)
            + person(150, 452, 1, "#B03A2E") + person(200, 456, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Monasterio de Santa Clara", [sky(p, sun, [(80, 70, .8)], [(200, 56)]), far, mid, near, fx(p, sun, 420, .25)])


def jaen_sanandres():
    p = "jsa"; sun = (200, 90)
    far = far_jaen(280, 200)
    left = lime_wall(-20, 170, 150, 230) + flowerpots(0, 120, 200, 2) + window(40, 300, 22, 40, shutters=False)
    right = lime_wall(260, 160, 150, 240) + flowerpots(270, 390, 190, 2, seed=1)
    c, cd, cl = JSTONE
    # portada plateresca de la Santa Capilla al fondo de la calleja, sin imágenes
    chapel = (f'<path d="M130 400V230H260V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M126 230H264V220H126Z" fill="{cd}" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M176 400V330Q195 312 214 330V400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 400V300" stroke="{cl}" stroke-width="7"/><path d="M{x - 3} 400V300M{x + 3} 400V300" stroke="{INK}" stroke-width=".8"/>' for x in (164, 226))
              + f'<path d="M160 300H230V292H160Z" fill="{cd}" stroke="{INK}" stroke-width="1.2"/><circle cx="195" cy="266" r="12" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{chapel}{left}{right}{ground(400, "#D8C6A6")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D5C29E", line="#C1AB85")}'
            + person(170, 446, .9, "#2F6F73") + person(226, 450, .95, "#9C2A22") + "</g>")
    return doc(p, "San Andrés", [sky(p, sun, [(300, 70, .8)], [(90, 60)]), far, mid, near, fx(p, sun, 420, .25)])


def jaen_castillo():
    p = "jca"; sun = (320, 120)
    far = f'<g id="far">{sierra(220, snow=False)}{olive_hills(330)}</g>'
    c, cd, cl = JSTONE
    castle = (f'<path d="M-10 400V300Q120 280 260 300L400 310V400Z" fill="#A89880" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M20 330V200H300V330Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(20, 300, 200, c)
              + "".join(f'<path d="M20 {y}H300" stroke="{cd}" stroke-width="1" opacity=".6"/>' for y in range(216, 330, 14))
              + f'<path d="M120 330V120H200V330Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(120, 200, 120, cl)
              + f'<path d="M176 122H200V330H176Z" fill="{cd}" opacity=".55"/>'
              + f'<path d="M150 180H170V210H150Z" fill="#3A2E28" stroke="{INK}" stroke-width="1.2"/>'
              + "".join(f'<path d="M{x} 330V160H{x + 40}V330Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>' + battlements(x, x + 40, 160, c) for x in (10, 270))
              + horseshoe(226, 270, 40, 60, "#5E4232", 1.6))
    mid = f'<g id="mid">{castle}</g>'
    near = (f'<g id="near"><rect x="-10" y="400" width="{W + 20}" height="170" fill="#C9B89A"/>'
            f'<path d="M-10 400L400 400L400 412L-10 412Z" fill="#B3A283" stroke="{INK}" stroke-width="1.4"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#A89878"/>' for x in range(10, 390, 26) for y in (450, 500))
            + cypress(360, 480, 150, 14) + person(90, 452, .95, "#9C2A22") + person(140, 456, .9, SEA, dress=True) + "</g>")
    return doc(p, "Castillo de Santa Catalina", [sky(p, sun, [(90, 70, .8)], [(200, 50), (218, 42, .8)]), far, mid, near, fx(p, sun, 400, .25)])


SCENES = {"malaga_santiago": malaga_santiago, "malaga_toros": malaga_toros, "malaga_buenavista": malaga_buenavista,
          "cadiz_populo": cadiz_populo, "cadiz_teatro": cadiz_teatro, "cadiz_almirante": cadiz_almirante,
          "cadiz_cuatrotorres": cadiz_cuatrotorres, "cadiz_santacatalina": cadiz_santacatalina,
          "cordoba_tiberiades": cordoba_tiberiades, "cordoba_averroes": cordoba_averroes, "cordoba_arqueologico": cordoba_arqueologico,
          "sevilla_manara": sevilla_manara, "sevilla_refinadores": sevilla_refinadores, "sevilla_maestranza": sevilla_maestranza,
          "sevilla_caridad": sevilla_caridad, "granada_darro": granada_darro, "granada_sanjuan": granada_sanjuan,
          "granada_cuevas": granada_cuevas, "granada_abadia": granada_abadia, "jaen_museo": jaen_museo,
          "jaen_santaclara": jaen_santaclara, "jaen_sanandres": jaen_sanandres, "jaen_castillo": jaen_castillo}

if __name__ == "__main__":
    for key in sys.argv[1:] or SCENES:
        open(os.path.join(OUT, f"fondo_{key}.svg"), "w").write(SCENES[key]())
    print("fondos:", ", ".join(sys.argv[1:] or SCENES))
