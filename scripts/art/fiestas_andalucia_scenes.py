#!/usr/bin/env python3
"""
Fondos nuevos de las rutas de fiestas. El resto de paradas reutiliza los fondos de historia y gastronomía.
Málaga (Alcazaba) · Sevilla (Prado, Plaza de España, Fábrica de Tabacos, portada de la Feria) ·
Granada (Plaza del Carmen, catedral, Plaza Nueva) · Córdoba (cruz de mayo en San Andrés, Puerta de
Sevilla, El Arenal) · Huelva (Paseo de la Ría) · Jaén (lumbre de San Antón, de noche) ·
Almería (santuario de la Virgen del Mar, solo la fachada: nunca se dibuja la imagen).

Uso: python3 scripts/art/fiestas_andalucia_scenes.py && python3 scripts/art/render_layers.py <prefijo> && npm run gen:assets
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from cadiz_ssanta_scenes import night_sky, night_fx, glow, FLOOR_N, FLOORL_N, STONE_N, WHITE_N
from granada_scenes import horseshoe, sierra, alhambra_hill, cypress
from sevilla_scenes import giralda, river, orange_tree, ALBERO, ALMAGRA, BRICK, GOTHIC
from cordoba_scenes import statue, ground, battlements, merlons, lime_wall, flowerpots
from huelva_scenes import boat, marsh
from jaen_scenes import JSTONE, far_jaen, ochre_house
from almeria_scenes import far_alm, OCHRE as AOCHRE

RED = "#D8412F"; ROSE = "#C0476A"; LEAF = "#4F8B5A"; BLUE = "#2F6F9E"


def lantern_string(y, x0=-10, x1=400, sag=18, step=34, colors=(PAPER, "#F7E6CF"), dots=(RED, LEAF)):
    """Guirnalda de farolillos de feria."""
    out = f'<path d="M{x0} {y}Q{(x0 + x1) / 2} {y + sag * 2} {x1} {y}" fill="none" stroke="{INK}" stroke-width="1"/>'
    k = 0
    for x in range(x0 + step // 2, x1, step):
        t = (x - x0) / (x1 - x0)
        yy = y + sag * 4 * t * (1 - t)
        c = colors[k % len(colors)]; d = dots[k % len(dots)]
        out += (f'<path d="M{x - 7} {f(yy + 2)}H{x + 7}Q{x + 13} {f(yy + 13)} {x + 7} {f(yy + 24)}H{x - 7}Q{x - 13} {f(yy + 13)} {x - 7} {f(yy + 2)}Z" fill="{c}" stroke="{INK}" stroke-width="1"/>'
                f'<circle cx="{x - 2}" cy="{f(yy + 10)}" r="2" fill="{d}"/><circle cx="{x + 3}" cy="{f(yy + 17)}" r="2" fill="{d}"/>')
        k += 1
    return out


def caseta(x, base, w=90, stripe=CLAY):
    """Caseta de feria de lona a rayas."""
    out = f'<path d="M{x} {base}V{base - 60}H{x + w}V{base}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
    out += "".join(f'<path d="M{x + k} {base - 60}H{x + k + 8}V{base}H{x + k}Z" fill="{stripe}"/>' for k in range(4, w - 4, 18))
    out += f'<path d="M{x} {base}V{base - 60}H{x + w}V{base}Z" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    out += f'<path d="M{x - 6} {base - 60}L{x + w / 2} {base - 84}L{x + w + 6} {base - 60}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
    out += "".join(f'<path d="M{x + w / 2} {base - 84}L{x + k} {base - 60}L{x + k + 10} {base - 60}Z" fill="{stripe}"/>' for k in range(0, int(w), 22))
    out += "".join(f'<path d="M{x + k} {base - 60}Q{x + k + 9} {base - 50} {x + k + 18} {base - 60}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>' for k in range(0, int(w) - 8, 18))
    return out


def albero_floor(p, y0):
    return floor(p, y0, color=ALBERO[2], line=ALBERO[0])


# ---------------------------------------------------------------------------
# Málaga
# ---------------------------------------------------------------------------
def malaga_alcazaba():
    p = "mal"; sun = (300, 100)
    brick = ("#C98A5E", "#A86E48", "#DDA67E")
    far = f'<g id="far"><path d="M-10 250Q100 200 200 210T400 190V300H-10Z" fill="#9DB38A"/>{far_city(300, 61, "#EBD0B4", "#F0DAC4", towers=1)}</g>'
    c, cd, cl = brick
    hill = f'<path d="M-20 400L-20 250Q80 200 190 190Q300 180 410 230L410 400Z" fill="#7FA06A" stroke="{INK}" stroke-width="1.6"/>'
    walls = (f'<path d="M10 300L40 230L180 200L330 210L380 260L380 290L330 238L180 228L52 256L28 312Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} {y}V{y - 8}H{x + 8}V{y}" fill="{c}" stroke="{INK}" stroke-width="1.1"/>' for x, y in [(44, 229), (60, 225), (76, 222), (92, 218), (108, 215), (124, 212), (140, 208), (156, 205), (190, 201), (206, 202), (222, 203), (238, 204), (254, 205), (270, 206), (286, 207), (302, 208)])
             + f'<path d="M150 236V150H220V236Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + merlons(150, 220, 150, cl, 14)
             + f'<path d="M260 240V160H310V240Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + merlons(260, 310, 160, c, 12)
             + horseshoe(170, 180, 30, 50, "#5E4232", 1.4)
             + f'<path d="M40 244L180 214L330 224" fill="none" stroke="{cd}" stroke-width="1.2"/>')
    trees = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4F7F5A" stroke="{INK}" stroke-width="1.2"/>' for x, y, r in [(30, 330, 26), (100, 340, 22), (330, 330, 26), (380, 320, 22), (240, 350, 20)])
    mid = f'<g id="mid">{hill}{walls}{trees}{ground(386, "#D8C6A4")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3D5BE", line="#CFBFA2")}'
            + palm(40, 520, 240, 10, 1) + palm(350, 520, 250, -8, 1)
            + person(150, 452, 1, SEA) + person(230, 456, .95, CLAY, dress=True) + lamp(300, 540, 150) + "</g>")
    return doc(p, "Alcazaba de Málaga", [sky(p, sun, [(80, 70, .8)], [(220, 60), (240, 50, .8)]), far, mid, near, fx(p, sun, 420)])


# ---------------------------------------------------------------------------
# Sevilla
# ---------------------------------------------------------------------------
def sevilla_prado():
    p = "spr"; sun = (90, 100)
    far = f'<g id="far">{far_city(260, 71, towers=2)}{giralda(320, 290, 36, 26, soft=True)}</g>'
    c, cd, cl = ALBERO
    court = (f'<path d="M60 390V220H330V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M52 220H338V206H52Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(window(x, 240, 18, 34, shutters=False, balcony=True, sw=1.1) for x in range(80, 320, 44))
             + "".join(f'<path d="M{x} 390V330H{x + 30}V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>' for x in (120, 180, 240)))
    trees = "".join(tree(x, 400, r) for x, r in [(20, 50), (370, 54), (110, 34), (290, 36)])
    mid = f'<g id="mid">{court}{trees}{ground(386, c)}</g>'
    near = (f'<g id="near">{albero_floor(p, 420)}'
            + "".join(person(x, 456 + (x % 5), .95, col, dress=d) for x, col, d in [(90, SEA, False), (130, RED, True), (250, "#6E2C5E", True), (300, "#34495E", False)])
            + f'<path d="M160 470L150 440Q170 430 196 436L204 424L210 428L206 444L210 470M170 452L168 470M196 452L196 470" fill="#8A5A3A" stroke="#6E4630" stroke-width="3"/>'
            + lamp(40, 540, 150) + lamp(350, 540, 150) + "</g>")
    return doc(p, "Prado de San Sebastián", [sky(p, sun, [(300, 70, .8)], [(230, 50), (250, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sevilla_plazaespana():
    p = "spe"; sun = (195, 90)
    far = f'<g id="far">{far_city(260, 73, towers=1)}</g>'
    c, cd, cl = BRICK

    def tower(x, top):
        return (f'<path d="M{x - 16} 360V{top}H{x + 16}V360Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M{x - 12} {top}V{top - 26}H{x + 12}V{top}Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M{x - 8} {top - 26}L{x} {top - 48}L{x + 8} {top - 26}Z" fill="{GOTHIC[0]}" stroke="{INK}" stroke-width="1.4"/>'
                + "".join(window(x - 5, y, 10, 20, shutters=False, arch=True, sw=1) for y in range(top + 20, 330, 50)))
    arc = (f'<path d="M-20 360V250Q195 200 410 250V360Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
           + "".join(f'<path d="M{x} 360V{f(318 - 30 * math.sin(math.pi * (x + 20) / 430))}Q{x + 12} {f(304 - 30 * math.sin(math.pi * (x + 20) / 430))} {x + 24} {f(318 - 30 * math.sin(math.pi * (x + 20) / 430))}V360Z" fill="{cd}" stroke="{INK}" stroke-width="1.1"/>' for x in range(-10, 400, 32))
           + "".join(window(x, round(262 - 30 * math.sin(math.pi * (x + 20) / 430), 1), 12, 22, shutters=False, arch=True, sw=1) for x in range(0, 390, 32))
           + tower(40, 150) + tower(350, 150)
           + f'<path d="M160 250V200H230V250Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/><path d="M160 200Q195 176 230 200Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>')
    canal = (f'<rect x="-10" y="360" width="{W + 20}" height="26" fill="url(#{p}sea)" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M150 386V372Q195 350 240 372V386Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(f'<path d="M{x} 368V358" stroke="{BLUE}" stroke-width="3"/>' for x in range(154, 240, 8)))
    mid = f'<g id="mid">{arc}{canal}{ground(386, "#E3CFAA")}</g>'
    benches = "".join(f'<path d="M{x} 470V440H{x + 80}V470Z" fill="#F6EBD2" stroke="{INK}" stroke-width="1.4"/>'
                      f'<path d="M{x + 6} 446H{x + 74}V464H{x + 6}Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1"/>'
                      + "".join(f'<path d="M{x + 8 + k * 11} 448l4 6 -4 6 -4 -6Z" fill="{GOLD}" stroke="{INK}" stroke-width=".6"/>' for k in range(6)) for x in (10, 300))
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}{benches}'
            + person(150, 456, 1, SEA) + person(180, 458, .95, RED, dress=True) + person(240, 454, .95, "#34495E") + "</g>")
    return doc(p, "Plaza de España", [sky(p, sun, [(60, 70, .8), (330, 60, .7)], [(260, 50)]), far, mid, near, fx(p, sun, 420, .25)])


def sevilla_tabacos():
    p = "sft"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 79, towers=2)}{giralda(60, 260, 34, 22, soft=True)}</g>'
    c, cd, cl = GOTHIC
    facade = (f'<path d="M-20 390V210H410V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M-20 210H410V196H-20Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 196V186H{x + 8}V196" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in range(-10, 400, 30))
              + "".join(window(x, y, 18, 32, shutters=False, balcony=(y == 230), sw=1.1) for x in list(range(0, 130, 40)) + list(range(270, 400, 40)) for y in (230, 300))
              + f'<path d="M140 390V150H250V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
              + "".join(f'<path d="M{x} 390V160" stroke="{cd}" stroke-width="5"/>' for x in (150, 240))
              + f'<path d="M132 150H258V138H132Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M150 138L195 104L240 138Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M190 104V80H200V104Z" fill="#8C938A" stroke="{INK}" stroke-width="1.2"/><circle cx="195" cy="74" r="6" fill="#8C938A" stroke="{INK}" stroke-width="1.2"/>'
              f'<path d="M199 78L214 60" stroke="#8C938A" stroke-width="3"/>'
              + f'<path d="M170 390V320Q195 296 220 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              + window(180, 200, 30, 50, shutters=False, balcony=True, sw=1.2))
    moat = f'<rect x="-10" y="386" width="{W + 20}" height="10" fill="#9BBFC0"/>'
    mid = f'<g id="mid">{facade}{moat}{ground(396, "#DCC6A0")}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + orange_tree(40, 490, 30) + orange_tree(350, 490, 30)
            + person(150, 452, .95, SEA) + person(176, 456, .9, "#6E2C5E", dress=True) + person(250, 454, 1, "#34495E") + "</g>")
    return doc(p, "Antigua Fábrica de Tabacos", [sky(p, sun, [(80, 70, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sevilla_portada():
    p = "spo"; sun = (320, 110)
    far = f'<g id="far">{far_city(270, 83, towers=1)}{giralda(60, 280, 30, 18, soft=True)}</g>'
    # portada efímera de la feria: arcos, pináculos y miles de bombillas
    c, cd = PAPER, "#E9DCC0"
    gate = (f'<path d="M20 400V190Q20 170 40 170H350Q370 170 370 190V400H290V270Q290 220 245 216H145Q100 220 100 270V400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + f'<path d="M150 400V300Q195 260 240 300V400Z" fill="none" stroke="{INK}" stroke-width="1.6"/>'
            + f'<path d="M150 170L195 100L240 170Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/><path d="M190 100V76H200V100Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<path d="M{x - 10} 170L{x} 136L{x + 10} 170Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>' for x in (40, 90, 300, 350))
            + "".join(f'<path d="M{x} 190H{x + 40}V240H{x}Z" fill="{cd}" stroke="{INK}" stroke-width="1"/><circle cx="{x + 20}" cy="215" r="14" fill="{BLUE}" stroke="{INK}" stroke-width="1"/>' for x in (36, 314))
            + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{GOLD}"/>' for x in range(28, 366, 12) for y in (178,))
            + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{GOLD}"/>' for y in range(200, 400, 14) for x in (28, 92, 298, 362))
            + "".join(f'<circle cx="{f(195 + 96 * math.cos(math.radians(a)))}" cy="{f(270 - 60 * math.sin(math.radians(a)))}" r="2.6" fill="{GOLD}"/>' for a in range(10, 171, 10)))
    mid = f'<g id="mid">{caseta(-30, 390, 60)}{caseta(360, 390, 60, SEA)}{gate}{ground(386, ALBERO[0])}</g>'
    near = (f'<g id="near">{albero_floor(p, 420)}{lantern_string(430, -10, 400, 20, 36)}'
            + person(140, 470, 1.05, RED, dress=True) + person(170, 474, 1, "#34495E") + person(250, 470, 1, "#E8744A", dress=True) + "</g>")
    return doc(p, "Portada de la Feria de Abril", [sky(p, sun, [(80, 70, .8)], [(220, 50)]), far, mid, near, fx(p, sun, 420, .25)])


# ---------------------------------------------------------------------------
# Granada
# ---------------------------------------------------------------------------
def granada_carmen():
    p = "gca"; sun = (300, 100)
    far = f'<g id="far">{sierra(250)}{far_city(270, 97, "#EBCFB4", "#F0DAC4", towers=2)}</g>'
    c, cd, cl = ("#F0DDB8", "#D6BE94", "#FBEFD4")
    ayto = (f'<path d="M40 390V170H350V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M34 170H356V156H34Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(window(x, 196, 18, 34, shutters=False, balcony=True, sw=1.1) for x in range(64, 340, 44))
            + "".join(f'<path d="M{x} 390V310Q{x + 18} 290 {x + 36} 310V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>' for x in range(56, 340, 50))
            + "".join(f'<path d="M{x} 300V260" stroke="{cd}" stroke-width="4"/>' for x in range(52, 350, 50))
            + f'<path d="M170 156V130H220V156Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/><circle cx="195" cy="143" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
            + f'<path d="M195 130V100" stroke="{INK}" stroke-width="1.6"/><path d="M195 100L215 106L195 112Z" fill="{RED}"/>')
    side = house(-40, 200, 80, 190, PINK, floors=3, cols=1) + house(350, 190, 80, 200, YELLOW, floors=3, cols=1)
    mid = f'<g id="mid">{side}{ayto}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + tree(30, 490, 34) + tree(360, 490, 34)
            + person(150, 454, 1, SEA) + person(176, 456, .95, "#6E2C5E", dress=True) + person(260, 452, 1, CLAY) + lamp(320, 540, 150) + "</g>")
    return doc(p, "Plaza del Carmen", [sky(p, sun, [(80, 70, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_catedral():
    p = "gct"; sun = (80, 100)
    far = f'<g id="far">{sierra(240)}</g>'
    c, cd, cl = ("#EADBC0", "#CDB894", "#F7EDD8")
    front = (f'<path d="M50 390V120H340V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             + "".join(f'<path d="M{x} 390V120H{x + 70}V390Z" fill="{cd}" opacity=".35"/>' for x in (50,))
             # tres grandes arcos de medio punto (fachada de Alonso Cano)
             + "".join(f'<path d="M{x} 390V200Q{x + w / 2} {200 - w * .55} {x + w} 200V390Z" fill="{cd}" stroke="{INK}" stroke-width="1.6"/>' for x, w in [(64, 70), (150, 90), (256, 70)])
             + "".join(f'<path d="M{x + 10} 390V330Q{x + w / 2} {316} {x + w - 10} 330V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>' for x, w in [(64, 70), (150, 90), (256, 70)])
             + f'<circle cx="195" cy="230" r="22" fill="{cl}" stroke="{INK}" stroke-width="1.6"/><circle cx="195" cy="230" r="12" fill="#9BBFC0" stroke="{INK}" stroke-width="1.2"/>'
             + f'<path d="M44 120H346V106H44Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<circle cx="{x}" cy="98" r="6" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>' for x in (60, 130, 195, 260, 330))
             + f'<path d="M-20 390V150H50V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(window(x, 180, 14, 28, shutters=False, arch=True, sw=1) for x in (8,)))
    mid = f'<g id="mid">{front}{ground(386, "#DCCBA8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3D5BE", line="#CFBFA2")}'
            + person(120, 452, 1, SEA) + person(150, 456, .95, CLAY, dress=True) + person(270, 452, 1, "#34495E") + lamp(40, 540, 150) + lamp(350, 540, 150) + "</g>")
    return doc(p, "Plaza de las Pasiegas", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_plazanueva():
    p = "gpn"; sun = (300, 90)
    far = f'<g id="far">{sierra(220)}{alhambra_hill(250, soft=True)}</g>'
    c, cd, cl = ("#E6D3AE", "#CDB68C", "#F4E7CC")
    chanc = (f'<path d="M-20 390V210H240V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M-24 210H244V198H-24Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<path d="M{x} 390V210" stroke="{cd}" stroke-width="4"/>' for x in range(10, 240, 46))
             + "".join(window(x, y, 18, 30, shutters=False, balcony=(y == 230), sw=1.1) for x in range(20, 230, 46) for y in (230, 296))
             + f'<path d="M90 390V340Q106 324 122 340V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>')
    church = (f'<path d="M270 390V220H350V390Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M340 390V150H380V390Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.8"/><path d="M336 150L360 124L384 150Z" fill="#B5553A" stroke="{INK}" stroke-width="1.4"/>'
              + window(352, 176, 16, 28, shutters=False, arch=True, sw=1) + f'<path d="M296 390V330Q310 314 324 330V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{chanc}{church}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + f'<path d="M160 480V440H230V480Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/><ellipse cx="195" cy="440" rx="38" ry="8" fill="#8FB9B4" stroke="{INK}" stroke-width="1.4"/>'
            + person(100, 452, 1, SEA) + person(280, 456, .95, "#6E2C5E", dress=True) + lamp(40, 540, 150) + "</g>")
    return doc(p, "Plaza Nueva", [sky(p, sun, [(80, 60, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


# ---------------------------------------------------------------------------
# Córdoba
# ---------------------------------------------------------------------------
def may_cross(x, base, h=220, w=130):
    """Cruz de mayo cubierta de claveles, con macetas al pie (cruz de flores, sin imágenes)."""
    arm = base - h * .7
    out = (f'<path d="M{x - 14} {base}V{base - h}H{x + 14}V{arm - 14}H{x + w / 2}V{arm + 14}H{x + 14}V{base}Z" fill="{RED}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M{x - 14} {arm - 14}H{x - w / 2}V{arm + 14}H{x - 14}Z" fill="{RED}" stroke="{INK}" stroke-width="1.8"/>')
    rnd = random.Random(5)
    for _ in range(70):
        if rnd.random() < .5:
            cx, cy = x + rnd.uniform(-10, 10), rnd.uniform(base - h + 4, base - 4)
        else:
            cx, cy = x + rnd.uniform(-w / 2 + 4, w / 2 - 4), arm + rnd.uniform(-10, 10)
        out += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="3.6" fill="{rnd.choice([RED, ROSE, "#E8744A", PAPER])}" stroke="{INK}" stroke-width=".5"/>'
    out += "".join(f'<path d="M{x + dx - 12} {base}L{x + dx - 9} {base - 18}H{x + dx + 9}L{x + dx + 12} {base}Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"/>'
                   f'<circle cx="{x + dx - 4}" cy="{base - 22}" r="6" fill="{LEAF}"/><circle cx="{x + dx + 4}" cy="{base - 24}" r="4" fill="{rnd.choice([RED, ROSE])}"/>' for dx in (-60, -30, 30, 60))
    return out


def cordoba_cruz():
    p = "kcr"; sun = (300, 100)
    far = f'<g id="far">{far_city(260, 101, towers=2)}</g>'
    church = (f'<path d="M230 390V200H400V390Z" fill="#E3B96F" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M300 390V110H350V390Z" fill="#F0CF92" stroke="{INK}" stroke-width="1.8"/><path d="M296 110L325 80L354 110Z" fill="#B5553A" stroke="{INK}" stroke-width="1.4"/>'
              + window(318, 130, 14, 26, shutters=False, arch=True, sw=1) + f'<path d="M250 390V320Q270 300 290 320V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>')
    houses = lime_wall(-30, 220, 250, 170) + "".join(window(x, 260, 20, 34) for x in (20, 80, 150)) + flowerpots(0, 220, 250, rows=1)
    mid = f'<g id="mid">{houses}{church}{ground(386, "#E6D6B8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E6D6B8", line="#D2C09E")}{may_cross(195, 500, 200, 130)}'
            + person(80, 458, 1, SEA) + person(320, 460, .95, RED, dress=True) + "</g>")
    return doc(p, "Cruz de mayo en San Andrés", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def cordoba_puertasevilla():
    p = "kps"; sun = (90, 100)
    far = f'<g id="far">{far_city(260, 103, towers=2)}</g>'
    c, cd, cl = ("#E3B96F", "#C99B50", "#F0CF92")
    wall = (f'<path d="M-20 390V250H410V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>' + battlements(-20, 410, 250, c)
            + "".join(f'<path d="M-20 {y}H410" stroke="{cd}" stroke-width="1" opacity=".6"/>' for y in range(266, 390, 14))
            + f'<path d="M120 390V200H270V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>' + battlements(120, 270, 200, cl)
            + horseshoe(160, 280, 70, 110, "#5E4232", 1.8)
            + horseshoe(128, 230, 20, 30, "#7E5E48", 1.2) + horseshoe(242, 230, 20, 30, "#7E5E48", 1.2))
    garden = "".join(f'<circle cx="{x}" cy="390" r="{r}" fill="#4F7F5A" stroke="{INK}" stroke-width="1.2"/>' for x, r in [(20, 30), (70, 22), (320, 26), (380, 30)])
    mid = f'<g id="mid">{wall}{garden}{ground(386, "#D9C39E")}</g>'
    near = (f'<g id="near">{floor(p, 420)}' + cypress(30, 480, 170, 15) + cypress(360, 480, 170, 15)
            + person(140, 452, 1, SEA) + person(250, 456, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Puerta de Sevilla", [sky(p, sun, [(300, 70, .8)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def cordoba_arenal():
    p = "kar"; sun = (300, 110)
    far = f'<g id="far">{far_city(250, 107, towers=1)}<path d="M-10 250Q200 220 400 240V300H-10Z" fill="#B7C7A4"/></g>'
    sea = f'<g id="sea">{river(p, 300, 340)}</g>'
    gate = (f'<path d="M100 390V220Q100 200 120 200H270Q290 200 290 220V390H250V280Q250 250 195 248Q140 250 140 280V390Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M170 200L195 160L220 200Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<circle cx="{x}" cy="206" r="2.4" fill="{GOLD}"/>' for x in range(108, 286, 10))
            + "".join(f'<circle cx="{f(195 + 55 * math.cos(math.radians(a)))}" cy="{f(284 - 36 * math.sin(math.radians(a)))}" r="2.4" fill="{GOLD}"/>' for a in range(10, 171, 16))
            + f'<path d="M110 220H150V250H110ZM240 220H280V250H240Z" fill="{RED}" stroke="{INK}" stroke-width="1"/>')
    mid = f'<g id="mid">{caseta(-30, 390, 100, "#4F8B5A")}{caseta(310, 390, 100, RED)}{gate}{ground(386, ALBERO[0])}</g>'
    near = (f'<g id="near">{albero_floor(p, 420)}{lantern_string(430, -10, 400, 18, 36, dots=(RED, "#4F8B5A"))}'
            + f'<path d="M80 480L70 450Q90 440 116 446L124 434L130 438L126 454L130 480M90 462L88 480M116 462L116 480" fill="#5B3A26" stroke="#3E281A" stroke-width="3"/>'
            f'<path d="M92 444V424H104V444" fill="#2B2A33"/><circle cx="98" cy="418" r="5" fill="#D9A07A"/><path d="M90 414H106" stroke="#2B2A33" stroke-width="3"/>'
            + person(220, 474, 1, RED, dress=True) + person(250, 470, 1, "#34495E") + "</g>")
    return doc(p, "Recinto ferial de El Arenal", [sky(p, sun, [(80, 70, .8)], [(220, 50)]), far, sea, mid, near, fx(p, sun, 420, .25)])


# ---------------------------------------------------------------------------
# Huelva
# ---------------------------------------------------------------------------
def huelva_paseoria():
    p = "hpr"; sun = (300, 110)
    far = f'<g id="far">{marsh(270)}</g>'
    sea = f'<g id="sea">{river(p, 280, 370)}{boat(80, 320, .8, SEA)}{boat(300, 340, 1, CLAY)}</g>'
    # noria de la feria y casetas a la orilla
    cx, cy, r = 280, 220, 90
    wheel = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="{r - 8}" fill="none" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(f'<path d="M{cx} {cy}L{f(cx + r * math.cos(math.radians(a)))} {f(cy + r * math.sin(math.radians(a)))}" stroke="{INK}" stroke-width="1.4"/>' for a in range(0, 360, 30))
             + "".join(f'<path d="M{f(cx + r * math.cos(math.radians(a)) - 9)} {f(cy + r * math.sin(math.radians(a)))}h18v14h-18Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
                       for a, c in zip(range(0, 360, 30), [RED, GOLD, SEA, CLAY] * 3))
             + f'<path d="M{cx} {cy}L{cx - 50} 390M{cx} {cy}L{cx + 50} 390" stroke="{INK}" stroke-width="4"/><circle cx="{cx}" cy="{cy}" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>')
    mid = f'<g id="mid">{wheel}{caseta(-20, 390, 90, SEA)}{caseta(80, 390, 90, CLAY)}<path d="M-10 386H400V396H-10Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.2"/>{ground(396, "#DCCBA8")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3D5BE", line="#CFBFA2")}{lantern_string(430, -10, 400, 18, 36, dots=(SEA, RED))}'
            + palm(40, 530, 240, 8, 1) + palm(360, 530, 230, -8, 1)
            + person(160, 474, 1, SEA) + person(190, 476, .95, RED, dress=True) + person(250, 472, 1, "#34495E") + "</g>")
    return doc(p, "Paseo de la Ría", [sky(p, sun, [(80, 70, .8)], [(160, 50), (180, 40, .8)]), far, sea, mid, near, fx(p, sun, 420, .25)])


# ---------------------------------------------------------------------------
# Jaén (de noche)
# ---------------------------------------------------------------------------
def bonfire(p, x, base, s=1.0):
    out = glow(p, "fire", x, base - 60 * s, 170 * s, .7)
    out += "".join(f'<path d="M{f(x + a * s)} {f(base)}L{f(x + b * s)} {f(base - 40 * s)}" stroke="#3E2A1C" stroke-width="{f(10 * s)}"/>' for a, b in [(-50, 20), (50, -20), (-30, 30), (30, -30)])
    out += (f'<path d="M{f(x)} {f(base - 150 * s)}Q{f(x + 30 * s)} {f(base - 100 * s)} {f(x + 50 * s)} {f(base - 20 * s)}Q{f(x)} {f(base)} {f(x - 50 * s)} {f(base - 20 * s)}Q{f(x - 36 * s)} {f(base - 90 * s)} {f(x)} {f(base - 150 * s)}Z" fill="#F29A2E"/>'
            f'<path d="M{f(x - 4 * s)} {f(base - 100 * s)}Q{f(x + 20 * s)} {f(base - 60 * s)} {f(x + 26 * s)} {f(base - 20 * s)}Q{f(x)} {f(base - 6 * s)} {f(x - 26 * s)} {f(base - 20 * s)}Q{f(x - 20 * s)} {f(base - 60 * s)} {f(x - 4 * s)} {f(base - 100 * s)}Z" fill="{GOLD}"/>'
            f'<path d="M{f(x)} {f(base - 56 * s)}Q{f(x + 10 * s)} {f(base - 36 * s)} {f(x + 10 * s)} {f(base - 20 * s)}Q{f(x)} {f(base - 12 * s)} {f(x - 10 * s)} {f(base - 20 * s)}Q{f(x - 10 * s)} {f(base - 36 * s)} {f(x)} {f(base - 56 * s)}Z" fill="#FFF3C4"/>')
    out += "".join(f'<circle cx="{f(x + dx * s)}" cy="{f(base - dy * s)}" r="1.6" fill="{GOLD}"/>' for dx, dy in [(-30, 170), (20, 190), (40, 160), (-10, 210), (30, 230)])
    return out


def ring_dancers(x, y, n=7, rx=150, ry=18):
    out = ""
    for k in range(n):
        a = math.pi * (k + .5) / n
        px, py = x - rx * math.cos(a), y + ry * math.sin(a)
        out += person(px, py, 1.05, ["#3A3552", "#5B3A4E", "#34495E", "#4A3A5E"][k % 4], dress=k % 2 == 0)
    return out


def jaen_lumbre():
    p = "jlu"
    far = f'<g id="far"><path d="M-10 300Q120 250 240 262T400 250V330H-10Z" fill="#2B3350"/><path d="M230 262L250 236H300L316 258Z" fill="#2B3350"/></g>'
    c, cd, cl = STONE_N
    church = (f'<path d="M110 390V230H250V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M104 230L180 196L256 230Z" fill="#6E4A44" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M160 390V330Q180 310 200 330V390Z" fill="#2E2230" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M250 390V130H310V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              + f'<path d="M244 130H316V120H244Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/><path d="M256 120L280 94L304 120Z" fill="#6E4A44" stroke="{INK}" stroke-width="1.4"/>'
              + f'<circle cx="280" cy="170" r="16" fill="#C9C2B0" stroke="{INK}" stroke-width="1.8"/><path d="M280 170V160M280 170L288 174" stroke="{INK}" stroke-width="1.6"/>')
    side = (f'<path d="M-30 390V220H110V390Z" fill="{WHITE_N[0]}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(window(x, 260, 20, 34, lit=True) for x in (0, 60))
            + f'<path d="M310 390V210H420V390Z" fill="#A08A6A" stroke="{INK}" stroke-width="1.8"/>' + "".join(window(x, 250, 20, 34, lit=(x == 330)) for x in (330, 380)))
    mid = f'<g id="mid">{side}{church}<rect x="-10" y="386" width="{W + 20}" height="42" fill="{FLOOR_N}"/></g>'
    near = (f'<g id="near">{floor(p, 420, color=FLOOR_N, line=FLOORL_N)}{bonfire(p, 195, 500, 1.1)}{ring_dancers(195, 470)}</g>')
    return doc(p, "Lumbre de San Antón en la Plaza de San Juan", [night_sky(p, (80, 90), 11), far, mid, near, night_fx(p)])


# ---------------------------------------------------------------------------
# Almería
# ---------------------------------------------------------------------------
def almeria_santuario():
    p = "asv"; sun = (300, 100)
    far = f'<g id="far">{far_alm(270, 40, .8)}</g>'
    c, cd, cl = ("#F1E4C8", "#D8C6A2", "#FBF3E2")
    # iglesia del antiguo convento de Santo Domingo: portada clásica y espadaña; puertas cerradas
    church = (f'<path d="M90 390V180H300V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M84 180H306V166H84Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M150 390V230H240V390Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 390V240" stroke="{cd}" stroke-width="5"/>' for x in (158, 232))
              + f'<path d="M146 240H244V230H146Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/><path d="M160 230L195 204L230 230Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M172 390V310Q195 290 218 310V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/><path d="M195 300V390" stroke="{INK}" stroke-width="1.2"/>'
              + f'<path d="M180 270H210V290H180Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.2"/>'
              + f'<path d="M160 166V120H230V166Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/><path d="M160 120Q195 96 230 120Z" fill="{cl}" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M176 160V134Q186 124 196 134V160ZM196 160V134Q206 124 214 134V160Z" fill="#6E5140" stroke="{INK}" stroke-width="1.1"/>'
              + f'<path d="M195 96V84M190 89H200" stroke="{INK}" stroke-width="1.6"/>')
    side = (f'<path d="M-30 390V210H90V390Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>' + "".join(window(x, 250, 18, 30) for x in (0, 50))
            + f'<path d="M300 390V200H420V390Z" fill="{AOCHRE[0]}" stroke="{INK}" stroke-width="1.8"/>' + "".join(window(x, 240, 18, 30, balcony=True) for x in (320, 370)))
    mid = f'<g id="mid">{side}{church}{ground(386, "#E3CFAA")}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3CFAA", line="#CFB78E")}'
            + palm(40, 520, 240, 8, 1) + palm(350, 520, 230, -8, 1)
            + person(140, 452, .95, SEA) + person(260, 456, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Santuario de la Virgen del Mar", [sky(p, sun, [(80, 70, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"malaga_alcazaba": malaga_alcazaba,
          "sevilla_prado": sevilla_prado, "sevilla_plazaespana": sevilla_plazaespana, "sevilla_tabacos": sevilla_tabacos, "sevilla_portada": sevilla_portada,
          "granada_carmen": granada_carmen, "granada_catedral": granada_catedral, "granada_plazanueva": granada_plazanueva,
          "cordoba_cruz": cordoba_cruz, "cordoba_puertasevilla": cordoba_puertasevilla, "cordoba_arenal": cordoba_arenal,
          "huelva_paseoria": huelva_paseoria, "jaen_lumbre": jaen_lumbre, "almeria_santuario": almeria_santuario}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos de fiestas generados:", ", ".join(keys))
