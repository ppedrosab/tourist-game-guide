#!/usr/bin/env python3
"""
Fondos nuevos de las rutas de leyendas. El resto de paradas reutiliza fondos existentes.
Sevilla (Alfalfa, calle Candilejo de noche, Casa de Pilatos, calle Cabeza del Rey Don Pedro de noche) ·
Granada (Casa de Castril, Dar al-Horra) · Córdoba (plaza de Colón, torre de la Malmuerta de noche) ·
Cádiz (yacimiento Gadir, Parque Genovés con el drago) · Jaén (Palacio de los Vélez, plaza de San Bartolomé de noche).

Uso: python3 scripts/art/leyendas_andalucia_scenes.py && python3 scripts/art/render_layers.py <prefijo> && npm run gen:assets
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from cadiz_ssanta_scenes import night_sky, night_fx, glow, night_floor, crowd, WHITE_N, YELLOW_N, PINK_N, STONE_N, FLOOR_N, FLOORL_N
from granada_scenes import horseshoe, sierra, alhambra_hill, cypress, albaicin_houses
from sevilla_scenes import giralda, orange_tree, ALBERO, ALMAGRA, BRICK, GOTHIC
from cordoba_scenes import statue, ground, battlements, merlons, lime_wall
from jaen_scenes import JSTONE, far_jaen, ochre_house, gothic_portal

RED = "#D8412F"; LEAF = "#4F8B5A"
GRANITE = ("#E6D3AE", "#CDB68C", "#F4E7CC")


def night_house(x, y, w, h, col, floors=3, cols=2, lit=()):
    return house(x, y, w, h, col, floors=floors, cols=cols, lit=lit)


def street_lantern(p, key, x, y, s=1.0):
    """Farol de pared encendido, con su halo."""
    return (glow(p, key, x, y + 14 * s, 60 * s, .55)
            + f'<path d="M{f(x - 22 * s)} {f(y - 6 * s)}H{f(x)}V{f(y)}" fill="none" stroke="{INK}" stroke-width="{f(2.4 * s)}"/>'
            f'<path d="M{f(x - 8 * s)} {f(y)}H{f(x + 8 * s)}L{f(x + 6 * s)} {f(y + 24 * s)}H{f(x - 6 * s)}Z" fill="#FFE7A8" stroke="{INK}" stroke-width="{f(1.6 * s)}"/>'
            f'<path d="M{f(x - 10 * s)} {f(y)}L{f(x)} {f(y - 8 * s)}L{f(x + 10 * s)} {f(y)}Z" fill="{INK}"/>')


# ---------------------------------------------------------------------------
# Sevilla
# ---------------------------------------------------------------------------
def sevilla_alfalfa():
    p = "sal"; sun = (300, 120)
    far = f'<g id="far">{far_city(250, 131, towers=2)}{giralda(70, 260, 32, 20, soft=True)}</g>'
    houses = (house(-30, 180, 130, 210, ALMAGRA, floors=3, cols=2, cierro=True) + house(100, 170, 120, 220, YELLOW, floors=4, cols=2)
              + house(220, 185, 100, 205, WHITE, floors=3, cols=2) + house(320, 175, 110, 215, PINK, floors=3, cols=2))
    mid = f'<g id="mid">{houses}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}' + tree(40, 490, 40) + tree(350, 490, 40)
            + bench(160, 470) + person(120, 452, 1, SEA) + person(250, 456, .95, CLAY, dress=True) + person(280, 452, 1, "#34495E") + "</g>")
    return doc(p, "Plaza de la Alfalfa", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sevilla_candilejo():
    p = "scn"
    far = f'<g id="far"><path d="M-10 300H400V330H-10Z" fill="#2B3350"/></g>'
    c, cd, cl = WHITE_N
    lane = (f'<path d="M-20 120L150 230L150 420L-20 560Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M410 120L240 230L240 420L410 560Z" fill="{YELLOW_N[1]}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M150 230H240V420H150Z" fill="{PINK_N[0]}" stroke="{INK}" stroke-width="1.4"/>'
            + window(170, 260, 18, 34, lit=True) + window(204, 260, 18, 34) + f'<path d="M180 420V360Q195 346 210 360V420Z" fill="#2E2230" stroke="{INK}" stroke-width="1.4"/>'
            + "".join(window(x, y, 20, 36, lit=(x == 40)) for x, y in [(20, 250), (80, 280)])
            + "".join(window(x, y, 20, 36, lit=(x == 330)) for x, y in [(330, 250), (280, 280)]))
    # la vieja se asoma con su candil
    old = (f'<path d="M84 282H104V318H84Z" fill="#FFE7A8" stroke="{INK}" stroke-width="1.4"/><circle cx="94" cy="294" r="6" fill="#D9A07A"/>'
           f'<path d="M86 302Q94 296 102 302V318H86Z" fill="#2B2A33"/>' + glow(p, "vie", 94, 300, 50, .5))
    mid = f'<g id="mid">{lane}{old}{street_lantern(p, "fa", 262, 240, 1.1)}<path d="M150 420H240V428H150Z" fill="{FLOOR_N}"/></g>'
    near = f'<g id="near">{night_floor(p, 420)}{person(190, 470, 1, "#2B2A33", hat=True)}</g>'
    return doc(p, "Calle Candilejo", [night_sky(p, (200, 70), 17), far, mid, near, night_fx(p)])


def sevilla_pilatos():
    p = "spl"; sun = (90, 110)
    far = f'<g id="far">{far_city(250, 137, towers=2)}</g>'
    c, cd, cl = ("#F1E4C8", "#D8C6A2", "#FBF3E2")
    front = (f'<path d="M20 390V180H370V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M14 180H376V168H14Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 168V160H{x + 8}V168" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in range(20, 370, 22))
             + f'<path d="M140 390V250H250V390Z" fill="#F4F1EA" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 390V256" stroke="#E0C9A0" stroke-width="7"/>' for x in (150, 240))
             + f'<path d="M165 390V300Q195 270 225 300V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
             + f'<path d="M140 250H250V240H140Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>' + "".join(f'<circle cx="{x}" cy="232" r="5" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in (150, 195, 240))
             + "".join(window(x, 210, 18, 30, shutters=False, balcony=True, sw=1.1) for x in (50, 100, 280, 330)))
    mid = f'<g id="mid">{palm(40, 300, 140, 6, .7)}{front}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + orange_tree(40, 490, 30) + orange_tree(350, 490, 30)
            + person(130, 452, 1, SEA) + person(270, 456, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Casa de Pilatos", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sevilla_cabezarey():
    p = "scr"
    far = f'<g id="far"><path d="M-10 290H400V330H-10Z" fill="#2B3350"/>{giralda(320, 300, 30, 18, soft=True).replace("#E", "#6")}</g>'
    corner = (f'<path d="M-20 170H200V420H-20Z" fill="{YELLOW_N[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M200 190H410V420H200Z" fill="{WHITE_N[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M190 170H210V420H190Z" fill="{YELLOW_N[1]}" stroke="{INK}" stroke-width="1.4"/>'
              + "".join(window(x, 220, 20, 36, lit=(x == 40)) for x in (40, 120)) + "".join(window(x, 240, 20, 36, lit=(x == 330)) for x in (260, 330))
              # la hornacina con el busto del rey
              + f'<path d="M160 260V330H236V260Q198 226 160 260Z" fill="#3E3450" stroke="{INK}" stroke-width="2"/>'
              f'<path d="M168 330V270Q198 244 228 270V330Z" fill="#2A2238"/>'
              f'<path d="M180 330Q180 300 198 298Q216 300 216 330Z" fill="#BDB6A8" stroke="{INK}" stroke-width="1.6"/>'
              f'<circle cx="198" cy="286" r="14" fill="#BDB6A8" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M186 276L190 266L196 274L198 264L202 274L208 266L212 276Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
              f'<path d="M154 330H242V338H154Z" fill="#8C8579" stroke="{INK}" stroke-width="1.4"/>'
              + glow(p, "bus", 198, 300, 70, .35)
              + f'<path d="M60 150H140V166H60Z" fill="#E9DCC0" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{corner}{street_lantern(p, "fl", 110, 300, 1)}<rect x="-10" y="416" width="{W + 20}" height="12" fill="{FLOOR_N}"/></g>'
    near = f'<g id="near">{night_floor(p, 420)}{person(120, 470, 1, "#2B2A33", hat=True)}{person(290, 474, .95, "#3A3552", dress=True)}</g>'
    return doc(p, "Calle Cabeza del Rey Don Pedro", [night_sky(p, (80, 80), 23), far, mid, near, night_fx(p)])


# ---------------------------------------------------------------------------
# Granada
# ---------------------------------------------------------------------------
def granada_castril():
    p = "gcs"; sun = (300, 100)
    far = f'<g id="far">{sierra(230)}{alhambra_hill(260, soft=True, scale=.8)}</g>'
    c, cd, cl = GRANITE
    front = (f'<path d="M60 390V150H330V390Z" fill="#F1E8D8" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M140 390V190H250V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M140 {y}H250" stroke="{cd}" stroke-width="1.2"/>' for y in range(210, 390, 22))
             + f'<path d="M170 390V310Q195 286 220 310V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
             # ventana tapiada con la inscripción y el fénix
             + f'<path d="M270 200H316V260H270Z" fill="{cd}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M270 {y}H316" stroke="#B8A27A" stroke-width="1"/>' for y in range(210, 260, 10))
             + f'<path d="M264 266H322V276H264Z" fill="{cl}" stroke="{INK}" stroke-width="1.2"/><path d="M270 271H316" stroke="{INK}" stroke-width="1" stroke-dasharray="3 2"/>'
             + f'<path d="M293 196Q282 186 286 176Q292 184 293 180Q294 184 300 176Q304 186 293 196Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
             + "".join(f'<path d="M{x} 200L{x + 6} 190L{x + 12} 200" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in (150, 170, 190, 210, 230))
             + window(80, 200, 22, 40, shutters=False, balcony=True, sw=1.2) + window(80, 290, 22, 40, shutters=False, sw=1.2))
    mid = f'<g id="mid">{house(-40, 200, 100, 190, PINK, floors=3, cols=1)}{front}{house(330, 210, 100, 180, WHITE, floors=3, cols=1)}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}<path d="M-10 424Q195 440 400 424V440H-10Z" fill="#8FB9B4"/>'
            + tree(30, 500, 34) + person(150, 462, 1, SEA) + person(250, 466, .95, "#6E2C5E", dress=True) + lamp(350, 540, 150) + "</g>")
    return doc(p, "Casa de Castril", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_darhorra():
    p = "gdh"; sun = (90, 110)
    far = f'<g id="far">{sierra(240)}{albaicin_houses(300, 3, 7, soft=True)}</g>'
    c, cd, cl = ("#F4EEE2", "#DCD2BF", "#FFFDF6")
    palace = (f'<path d="M70 390V210H320V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M230 390V150H300V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(horseshoe(x, 260, 30, 50, "#6E5140", 1.3) for x in (95, 150))
              + horseshoe(248, 190, 34, 56, "#6E5140", 1.3)
              + f'<path d="M226 150H304V142H226Z" fill="#B5553A" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M110 390V330H160V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{lime_wall(-30, 250, 110, 140)}{palace}{cypress(345, 390, 180, 14)}{ground(386, "#E6D6B8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E6D6B8", line="#D2C09E")}'
            + person(140, 452, 1, SEA) + person(250, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Palacio de Dar al-Horra", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


# ---------------------------------------------------------------------------
# Córdoba
# ---------------------------------------------------------------------------
def cordoba_colon():
    p = "kcl"; sun = (300, 110)
    far = f'<g id="far">{far_city(260, 141, towers=2)}</g>'
    merced = (f'<path d="M40 390V190H350V390Z" fill="#B5553A" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{x} 390V190" stroke="{PAPER}" stroke-width="7"/>' for x in (50, 130, 260, 340))
              + f'<path d="M150 390V160H240V390Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
              + f'<path d="M144 160Q195 110 246 160Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M175 390V320Q195 300 215 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(window(x, 220, 18, 34, shutters=False, balcony=True, sw=1.1) for x in (80, 180, 290))
              + f'<path d="M34 190H356V180H34Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{merced}{ground(386, "#DDBE98")}</g>'
    garden = "".join(tree(x, 470, r) for x, r in [(30, 44), (130, 32), (260, 34), (365, 44)])
    near = (f'<g id="near">{floor(p, 420, color="#D8CBAE", line="#C4B592")}{garden}'
            + f'<ellipse cx="195" cy="486" rx="50" ry="12" fill="#8FB9B4" stroke="{INK}" stroke-width="1.6"/>'
            + person(90, 470, 1, SEA) + person(300, 474, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Plaza de Colón", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def cordoba_malmuerta():
    p = "kmm"
    far = f'<g id="far"><path d="M-10 300H400V330H-10Z" fill="#2B3350"/></g>'
    c, cd, cl = ("#B89A6A", "#9A7E52", "#CDB180")
    tower = (f'<path d="M150 400V150H250V400Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
             f'<path d="M150 150H175V400H150Z" fill="{cl}" opacity=".5"/><path d="M225 150H250V400H225Z" fill="{cd}" opacity=".6"/>'
             f'<path d="M142 150H258V136H142Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>' + merlons(142, 258, 136, cl, 14)
             + "".join(f'<path d="M150 {y}H250" stroke="{cd}" stroke-width="1"/>' for y in range(170, 400, 18))
             + f'<path d="M190 230H210V260H190Z" fill="#2A2238" stroke="{INK}" stroke-width="1.2"/>'
             # el arco que la une a la muralla
             + f'<path d="M250 300H410V400H390V340Q330 300 270 340V400H250Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
             + merlons(250, 410, 300, c, 14)
             + f'<path d="M270 340Q330 300 390 340" fill="none" stroke="{cd}" stroke-width="2"/>'
             + f'<path d="M-20 330H150V400H-20Z" fill="{cd}" stroke="{INK}" stroke-width="1.6"/>' + merlons(-20, 150, 330, cd, 14)
             + glow(p, "tor", 200, 260, 120, .25))
    mid = f'<g id="mid">{tower}<rect x="-10" y="396" width="{W + 20}" height="32" fill="{FLOOR_N}"/></g>'
    near = (f'<g id="near">{night_floor(p, 420)}' + lamp(60, 540, 160) + lamp(340, 540, 160)
            + person(170, 470, 1, "#2B2A33", hat=True) + person(230, 474, .95, "#3A3552", dress=True) + "</g>")
    return doc(p, "Torre de la Malmuerta", [night_sky(p, (310, 90), 29), far, mid, near, night_fx(p)])


# ---------------------------------------------------------------------------
# Cádiz
# ---------------------------------------------------------------------------
def cadiz_gadir():
    p = "kgd"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 149, towers=4)}</g>'
    theatre = (house(-30, 170, 150, 220, YELLOW, floors=3, cols=2) + house(270, 180, 150, 210, PINK, floors=3, cols=2)
               + f'<path d="M110 390V190H280V390Z" fill="#F1E4C8" stroke="{INK}" stroke-width="1.8"/>'
               + f'<path d="M104 190H286V178H104Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
               + f'<path d="M140 210H250V240H140Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
               + "".join(f'<path d="M{150 + k * 10} 225h6" stroke="{CLAY}" stroke-width="3"/>' for k in range(9))
               + f'<path d="M160 390V300Q195 276 230 300V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>')
    mid = f'<g id="mid">{theatre}{ground(386, "#E3CFAA")}</g>'
    # cristal en el suelo con los muros fenicios debajo
    pit = (f'<path d="M60 450H330L350 530H40Z" fill="#6E5A44" stroke="{INK}" stroke-width="2"/>'
           + "".join(f'<path d="M{x} {y}h{w}v{h}h-{w}Z" fill="#C9A77E" stroke="{INK}" stroke-width="1"/>' for x, y, w, h in [(80, 470, 60, 14), (160, 470, 40, 14), (220, 470, 70, 14), (90, 500, 90, 14), (210, 500, 100, 14)])
           + f'<path d="M60 450H330L350 530H40Z" fill="#DCEBE6" opacity=".25"/>')
    near = f'<g id="near">{floor(p, 420)}{pit}' + person(60, 448, 1, SEA) + person(340, 452, .95, CLAY, dress=True) + "</g>"
    return doc(p, "Yacimiento Gadir", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def dragon_tree(x, base, s=1.0):
    out = f'<path d="M{f(x - 16 * s)} {f(base)}Q{f(x - 10 * s)} {f(base - 90 * s)} {f(x - 8 * s)} {f(base - 150 * s)}H{f(x + 8 * s)}Q{f(x + 10 * s)} {f(base - 90 * s)} {f(x + 16 * s)} {f(base)}Z" fill="#9A8A6E" stroke="{INK}" stroke-width="2"/>'
    tips = []
    for a in (-70, -40, -12, 12, 40, 70):
        ex = x + math.sin(math.radians(a)) * 90 * s; ey = base - 150 * s - math.cos(math.radians(a)) * 50 * s
        out += f'<path d="M{f(x)} {f(base - 146 * s)}Q{f((x + ex) / 2)} {f(ey + 30 * s)} {f(ex)} {f(ey)}" fill="none" stroke="#9A8A6E" stroke-width="{f(12 * s)}"/>'
        tips.append((ex, ey))
    for ex, ey in tips:
        out += "".join(f'<path d="M{f(ex)} {f(ey)}L{f(ex + 26 * s * math.cos(math.radians(t)))} {f(ey - 26 * s * math.sin(math.radians(t)))}" stroke="#4F7F5A" stroke-width="{f(5 * s)}"/>' for t in range(20, 170, 22))
    out += f'<path d="M{f(x + 4 * s)} {f(base - 60 * s)}q2 10 0 18" stroke="{RED}" stroke-width="3"/><circle cx="{f(x + 4 * s)}" cy="{f(base - 38 * s)}" r="3" fill="{RED}"/>'
    return out


def cadiz_genoves():
    p = "kgn"; sun = (330, 140)
    far = f'<g id="far">{far_city(270, 151, towers=3)}</g>'
    sea = f'<g id="sea"><rect x="-10" y="280" width="{W + 20}" height="60" fill="url(#{p}sea)"/></g>'
    hedges = "".join(f'<path d="M{x} 390V340Q{x + 30} 300 {x + 60} 340V390Z" fill="#4F7F5A" stroke="{INK}" stroke-width="1.4"/>' for x in (-20, 60, 270, 340))
    mid = f'<g id="mid">{hedges}{ground(386, "#DDC9A6")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#DDC9A6", line="#C8B38E")}{dragon_tree(195, 500, 1.3)}'
            + palm(30, 520, 240, 8, 1) + palm(360, 520, 230, -8, 1) + person(90, 470, 1, SEA) + person(300, 474, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Parque Genovés", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, sea, mid, near, fx(p, sun, 420, .25)])


# ---------------------------------------------------------------------------
# Jaén
# ---------------------------------------------------------------------------
def jaen_velez():
    p = "jvl"; sun = (300, 110)
    far = far_jaen(280, 90)
    c, cd, cl = JSTONE
    palace = (f'<path d="M40 390V190H280V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M34 190H286V178H34Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M280 390V130H350V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/><path d="M276 130H354V120H276Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
              + window(304, 160, 20, 36, shutters=False, sw=1.1) + window(304, 240, 20, 36, shutters=False, balcony=True, sw=1.1)
              + "".join(window(x, 220, 18, 32, shutters=False, balcony=True, sw=1.1) for x in (70, 140, 210))
              + gothic_portal(130, 390, 70, 110))
    mid = f'<g id="mid">{palace}{ochre_house(350, 200, 80, 190, floors=3, cols=1)}{ground(386, "#D8C6A4")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#D8C6A4", line="#C4AF88")}' + lamp(30, 540, 150)
            + person(160, 452, 1, SEA) + person(250, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Palacio de los Vélez", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), [f'<g id="far">{far}</g>' if not far.startswith("<g") else far][0], mid, near, fx(p, sun, 420)])


def jaen_sanbartolome():
    p = "jsb"
    far = f'<g id="far"><path d="M-10 300Q120 250 240 262T400 250V330H-10Z" fill="#2B3350"/></g>'
    c, cd, cl = STONE_N
    church = (f'<path d="M-20 390V210H140V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M20 210V140H80V210Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/><path d="M16 140L50 110L84 140Z" fill="#6E4A44" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M40 390V330Q60 312 80 330V390Z" fill="#2E2230" stroke="{INK}" stroke-width="1.4"/>')
    casa = (house(150, 170, 250, 220, YELLOW_N, floors=3, cols=3, lit={(0, 2)})
            + f'<path d="M150 170H400V160H150Z" fill="{YELLOW_N[2]}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{church}{casa}<rect x="-10" y="386" width="{W + 20}" height="42" fill="{FLOOR_N}"/></g>'
    ghost = (glow(p, "gh", 200, 440, 60, .35)
             + f'<path d="M176 488Q172 430 200 410Q228 430 224 488L216 480L208 488L200 480L192 488L184 480Z" fill="#F4F1EA" stroke="{INK}" stroke-width="1.8"/>'
             f'<circle cx="192" cy="436" r="3.4" fill="{INK}"/><circle cx="208" cy="436" r="3.4" fill="{INK}"/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2.6" fill="none" stroke="#8C8579" stroke-width="2"/>' for x, y in [(176, 470), (170, 478), (164, 486)]))
    near = f'<g id="near">{night_floor(p, 420)}{lamp(340, 540, 160)}{ghost}{person(80, 476, 1, "#2B2A33", hat=True)}</g>'
    return doc(p, "Plaza de San Bartolomé", [night_sky(p, (310, 80), 31), far, mid, near, night_fx(p)])


SCENES = {"sevilla_alfalfa": sevilla_alfalfa, "sevilla_candilejo": sevilla_candilejo, "sevilla_pilatos": sevilla_pilatos, "sevilla_cabezarey": sevilla_cabezarey,
          "granada_castril": granada_castril, "granada_darhorra": granada_darhorra,
          "cordoba_colon": cordoba_colon, "cordoba_malmuerta": cordoba_malmuerta,
          "cadiz_gadir": cadiz_gadir, "cadiz_genoves": cadiz_genoves,
          "jaen_velez": jaen_velez, "jaen_sanbartolome": jaen_sanbartolome}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de leyendas generados:", ", ".join(keys))
