#!/usr/bin/env python3
"""
Fondos de Granada (390×560, un grupo por capa).

Uso: python3 scripts/art/granada_scenes.py && python3 scripts/art/render_layers.py granada_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, SHUT, W, H, WHITE, YELLOW, PINK, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from sevilla_scenes import gothic_wall, pinnacles, river, GOTHIC

ROJA = ("#C4623F", "#A34E31", "#D98A68")      # tapial de la Alhambra
CAL = ("#F7F3EA", "#E2DACB", "#FFFFFF")       # casas encaladas del Albaicín
TEJA = "#B5553A"
CYPRESS = "#2F5A3F"


def cypress(x, base, h, w=10):
    return f'<path d="M{f(x)} {f(base - h)}Q{f(x + w)} {f(base - h * .5)} {f(x + w * .6)} {f(base)}L{f(x - w * .6)} {f(base)}Q{f(x - w)} {f(base - h * .5)} {f(x)} {f(base - h)}Z" fill="{CYPRESS}"/>'


def sierra(y, snow=True):
    s = f'<path d="M-10 {y}L40 {y - 50}L90 {y - 20}L150 {y - 70}L210 {y - 30}L270 {y - 80}L330 {y - 35}L400 {y - 60}L400 {y + 40}L-10 {y + 40}Z" fill="#C9C6CF"/>'
    if snow:
        for px, py in [(40, y - 50), (150, y - 70), (270, y - 80), (400, y - 60)]:
            s += f'<path d="M{px - 18} {py + 16}L{px} {py}L{px + 18} {py + 14}L{px + 8} {py + 18}L{px} {py + 12}L{px - 8} {py + 19}Z" fill="#FFFFFF"/>'
    return s


def alhambra_hill(y, soft=False, scale=1.0):
    """La Alhambra sobre su colina: murallas rojas, torres y la torre de Comares."""
    c, cd, cl = ROJA
    sw = 0 if soft else 1.4
    ink = "none" if soft else INK
    s = f'<path d="M-10 {y + 40}Q80 {y - 10} 200 {y - 6}Q320 {y - 4} 400 {y + 30}L400 {y + 120}L-10 {y + 120}Z" fill="#6E9F7A"/>'
    s += "".join(f'<circle cx="{x}" cy="{y + 30 + (x % 3) * 6}" r="{12 + x % 7}" fill="#4F7F5A"/>' for x in range(0, 400, 22))
    s += f'<path d="M20 {y}L370 {y - 6}L370 {y + 16}L20 {y + 22}Z" fill="{c}" stroke="{ink}" stroke-width="{sw}"/>'
    towers = [(30, 26, 22), (90, 22, 16), (150, 30, 44), (215, 22, 20), (270, 26, 30), (330, 22, 18)]
    for tx, tw, th in towers:
        ty = y - th - (tx - 20) * 6 / 350
        s += f'<path d="M{tx} {f(ty)}L{tx + tw} {f(ty)}L{tx + tw} {y + 20}L{tx} {y + 20}Z" fill="{cl if tx == 150 else c}" stroke="{ink}" stroke-width="{sw}"/>'
        s += f'<path d="M{tx + tw * .7:.1f} {f(ty)}L{tx + tw} {f(ty)}L{tx + tw} {y + 20}L{tx + tw * .7:.1f} {y + 20}Z" fill="{cd}" opacity=".6"/>'
        if not soft:
            s += "".join(f'<path d="M{tx + 3 + i * 7} {f(ty)}V{f(ty - 4)}H{tx + 7 + i * 7}V{f(ty)}" fill="{c}" stroke="{INK}" stroke-width="1"/>' for i in range(int(tw // 7)))
            s += f'<path d="M{tx + tw / 2 - 2:.1f} {f(ty + 8)}V{f(ty + 14)}" stroke="{INK}" stroke-width="2.4"/>'
    # Palacio de Carlos V asomando
    s += f'<path d="M234 {y - 8}L262 {y - 8}L262 {y + 4}L234 {y + 4}Z" fill="#E7C98E" stroke="{ink}" stroke-width="{sw}"/>'
    s += cypress(120, y + 18, 34, 6) + cypress(200, y + 16, 30, 6) + cypress(300, y + 20, 36, 6)
    return s


def horseshoe(x, y, w, h, fill="#5E4232", stroke=1.6):
    """Arco de herradura: más ancho arriba que en la base."""
    r = w / 2
    return (f'<path d="M{f(x + w * .1)} {f(y + h)}L{f(x + w * .1)} {f(y + r)}'
            f'A{f(r)} {f(r)} 0 1 1 {f(x + w * .9)} {f(y + r)}L{f(x + w * .9)} {f(y + h)}Z" fill="{fill}" stroke="{INK}" stroke-width="{stroke}"/>')


def muqarnas(x, y, w, rows=3, c="#E9D8B4", cd="#C9B28A"):
    s = ""
    for r in range(rows):
        n = 6 + r * 2
        cw = w / n
        for i in range(n):
            cx = x + i * cw
            cy = y + r * 9
            s += f'<path d="M{f(cx)} {f(cy)}L{f(cx + cw)} {f(cy)}L{f(cx + cw)} {f(cy + 6)}Q{f(cx + cw / 2)} {f(cy + 12)} {f(cx)} {f(cy + 6)}Z" fill="{c if (i + r) % 2 else cd}" stroke="{INK}" stroke-width=".8"/>'
    return s


def albaicin_houses(y, seed=0, n=6, soft=False):
    s = ""
    for i in range(n):
        x = -20 + i * 72 + (seed * 13 + i * 17) % 20
        h = 60 + (seed * 7 + i * 29) % 50
        w = 70
        ink = "none" if soft else INK
        s += f'<path d="M{x} {y - h}L{x + w} {y - h}L{x + w} {y}L{x} {y}Z" fill="{CAL[0]}" stroke="{ink}" stroke-width="{0 if soft else 1.4}"/>'
        s += f'<path d="M{x - 4} {y - h}L{x + w / 2} {y - h - 16}L{x + w + 4} {y - h}Z" fill="{TEJA}" stroke="{ink}" stroke-width="{0 if soft else 1.2}"/>'
        if not soft:
            s += window(x + 16, y - h + 18, 12, 18, shutters=False, sw=1) + window(x + 42, y - h + 18, 12, 18, shutters=False, sw=1, lit=i % 3 == 0)
    return s


# ---------------------------------------------------------------------------
def s_plaza():
    p = "gpl"; sun = (310, 110)
    far = f'<g id="far">{far_city(260, 51)}</g>'
    # edificios de la Gran Vía y el monumento de las Capitulaciones
    bld = (house(-20, 170, 140, 230, CAL, floors=4, cols=3, lit={(1, 1)})
           + house(270, 180, 140, 220, YELLOW, floors=4, cols=3, cierro=True)
           + f'<path d="M-10 170Q50 120 110 170Z" fill="#9AA3AA" stroke="{INK}" stroke-width="1.6"/><path d="M50 134V118" stroke="{INK}" stroke-width="1.6"/>')
    mon = (f'<path d="M110 400Q195 380 280 400L276 412H114Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M116 396Q195 378 274 396" fill="none" stroke="#8FB9B4" stroke-width="3"/>'
           f'<path d="M160 396L166 290L224 290L230 396Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M154 290L236 290L236 280L154 280Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M176 320H214V356H176Z" fill="#6E8A7A" stroke="{INK}" stroke-width="1.2"/>'
           # la reina sentada y Colón de pie, en bronce
           f'<path d="M168 280L170 244Q170 234 178 232L190 232Q196 236 194 248L196 280Z" fill="#4E6B5E" stroke="{INK}" stroke-width="1.5"/>'
           f'<circle cx="182" cy="222" r="8" fill="#4E6B5E" stroke="{INK}" stroke-width="1.4"/><path d="M176 216L182 208L188 216Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
           f'<path d="M204 280L206 226Q210 216 218 218Q224 222 222 234L222 280Z" fill="#4E6B5E" stroke="{INK}" stroke-width="1.5"/>'
           f'<circle cx="214" cy="208" r="8" fill="#4E6B5E" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M206 236L192 244L194 250L208 244Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{bld}{mon}<rect x="-10" y="404" width="{W + 20}" height="24" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + person(90, 442, .9, CLAY, dress=True) + person(300, 440, .9, "#34495E", hat=True) + person(320, 446, 1, SEA)
            + lamp(40, 540, 170) + lamp(350, 540, 170) + bench(220, 492) + "</g>")
    return doc(p, "Plaza Isabel la Católica", [sky(p, sun, [(80, 70, .9)], [(210, 60), (230, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_capilla():
    p = "gca"; sun = (80, 110)
    far = f'<g id="far">{far_city(250, 53)}</g>'
    c, cd, cl = GOTHIC
    chapel = (gothic_wall(-20, 180, 230, 220)
              + "".join(f'<path d="M{x} 180L{x + 8} 168L{x + 16} 180" fill="{cl}" stroke="{INK}" stroke-width="1"/>' for x in range(-20, 210, 16))
              + f'<path d="M60 400L60 270Q100 230 140 270L140 400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M50 400L50 262Q100 214 150 262L150 400" fill="none" stroke="{cd}" stroke-width="5"/>'
              f'<path d="M72 250H128V236H72Z" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>')
    # la Madraza enfrente: fachada barroca almagra con balcón
    madraza = (f'<path d="M220 170L410 170L410 400L220 400Z" fill="#B5553A" stroke="{INK}" stroke-width="1.8"/>'
               f'<path d="M216 170L414 170L414 158L216 158Z" fill="#E6D3AE" stroke="{INK}" stroke-width="1.6"/>'
               + "".join(f'<path d="M{x} 170V400" stroke="#E6D3AE" stroke-width="6"/>' for x in (226, 404))
               + window(262, 200, 22, 46, shutters=False, balcony=True, sw=1.3, lit=True) + window(340, 200, 22, 46, shutters=False, balcony=True, sw=1.3)
               + f'<path d="M290 400V310Q312 290 334 310V400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
               f'<path d="M282 300H342V292H282Z" fill="#E6D3AE" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{chapel}{madraza}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + person(170, 440, .9, SEA) + person(200, 446, 1, CLAY, dress=True)
            + lamp(30, 540, 170) + "</g>")
    return doc(p, "Capilla Real", [sky(p, sun, [(300, 70, .9)], [(230, 60), (250, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_sannicolas():
    p = "gsn"; sun = (300, 150)
    far = f'<g id="far">{sierra(250)}</g>'
    mid = f'<g id="mid">{alhambra_hill(270)}<rect x="-10" y="384" width="{W + 20}" height="44" fill="#6E9F7A"/></g>'
    near = (f'<g id="near"><rect x="-10" y="390" width="{W + 20}" height="180" fill="#E4CDA8"/><rect x="-10" y="390" width="{W + 20}" height="180" fill="url(#{p}dots)"/>'
            f'<path d="M-10 390L400 390L400 412L-10 412Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M-10 388L400 388" stroke="{INK}" stroke-width="2"/>'
            # la iglesia de San Nicolás a un lado
            + f'<path d="M300 412V230H400V412Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.8"/><path d="M296 230L350 196L404 230Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M320 412V350Q336 334 352 350V412Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M300 180V230H330V180Z" fill="{CAL[0]}" stroke="{INK}" stroke-width="1.6"/><path d="M296 180L315 164L334 180Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.4"/>'
            + window(309, 190, 12, 22, shutters=False, arch=True, sw=1.1)
            + person(80, 450, 1, SEA) + person(110, 454, .95, CLAY, dress=True) + person(230, 450, 1, "#6E2C5E", dress=True)
            + tree(20, 540, 36, "#3F6F4C", "#2F5A3C") + "</g>")
    return doc(p, "Mirador de San Nicolás", [sky(p, sun, [(80, 70, .8)], [(180, 90), (200, 80, .8)]), far, mid, near, fx(p, sun, 390, .3)])


def s_pesas():
    p = "gpe"; sun = (310, 100)
    far = f'<g id="far">{far_city(240, 55, "#EBCFB4", "#F0DAC4", towers=1)}{albaicin_houses(250, 1, soft=True)}</g>'
    wall = (f'<path d="M60 130L330 130L330 400L60 400Z" fill="#C9A77E" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} {y}L{x + 22} {y}" stroke="#A88A63" stroke-width="1.4"/>' for x in range(64, 320, 30) for y in range(150, 400, 18))
            + horseshoe(140, 190, 110, 210, "#4A342A", 2)
            + f'<path d="M134 196Q195 128 256 196" fill="none" stroke="#E6D3AE" stroke-width="6"/>'
            + f'<path d="M120 170H270" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x} 170V{y}" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 7} {y}H{x + 7}L{x + 5} {y + 12}H{x - 5}Z" fill="#6E6E78" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(140, 186), (166, 180), (224, 180), (250, 186)])
            + f'<path d="M56 130L334 130L334 120L56 120Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.4"/>')
    side = albaicin_houses(400, 3, n=2).replace('x="-20"', 'x="-20"') + house(330, 200, 90, 200, CAL, floors=3, cols=2)
    mid = f'<g id="mid">{side}{wall}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C7A8")}'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#BFAE8E"/>' for x in range(10, 390, 26) for y in (452, 490, 530))
            + person(110, 442, .9, SEA) + person(290, 440, .9, CLAY, dress=True)
            + lamp(360, 540, 160) + "</g>")
    return doc(p, "Arco de las Pesas", [sky(p, sun, [(80, 70, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def s_justicia():
    p = "gju"; sun = (90, 100)
    far = f'<g id="far">{sierra(240)}</g>'
    c, cd, cl = ROJA
    gate = (f'<path d="M80 110L310 110L310 400L80 400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M260 112L310 112L310 400L260 400Z" fill="{cd}" opacity=".6"/>'
            + "".join(f'<path d="M{x} 110V98H{x + 12}V110" fill="{c}" stroke="{INK}" stroke-width="1.3"/>' for x in range(84, 306, 20))
            # gran arco de herradura con alfiz
            + f'<path d="M120 400V150H270V400" fill="none" stroke="{cl}" stroke-width="4"/>'
            + horseshoe(130, 170, 130, 230, "#7E3A26", 1.8)
            + horseshoe(152, 230, 86, 170, "#3A2418", 1.6)
            # la mano en la clave del arco exterior
            + f'<path transform="translate(186 172) scale(.35)" d="M0 60V20Q0 14 6 14Q10 14 10 20V36V8Q10 2 16 2Q20 2 20 8V36V4Q20 -2 26 -2Q30 -2 30 4V36V10Q30 4 36 4Q40 4 40 10V44Q44 36 50 36Q54 40 50 46L40 66Q34 72 22 72Q0 72 0 60Z" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
            # la llave en el arco interior
            + f'<path d="M186 244H206" stroke="{INK}" stroke-width="4"/><path d="M186 244H206" stroke="{GOLD}" stroke-width="2"/><circle cx="182" cy="244" r="4" fill="none" stroke="{GOLD}" stroke-width="2"/><path d="M202 244V250" stroke="{GOLD}" stroke-width="2"/>'
            + f'<path d="M160 140H230V126H160Z" fill="#E6D3AE" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<path d="M{164 + i * 11} 133H{170 + i * 11}" stroke="{SEA}" stroke-width="2"/>' for i in range(6)))
    trees = tree(20, 400, 50, "#4B7C58", "#3A6446") + tree(370, 400, 52, "#4B7C58", "#3A6446") + cypress(60, 400, 150, 14) + cypress(330, 400, 140, 14)
    mid = f'<g id="mid">{trees}{gate}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#CDB38E"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C7A8")}'
            + person(100, 442, .9, SEA) + person(300, 440, .9, "#6E2C5E", dress=True)
            + tree(10, 560, 44, "#3F6F4C", "#2F5A3C") + "</g>")
    return doc(p, "Puerta de la Justicia", [sky(p, sun, [(300, 60, .8)], [(230, 60), (250, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_carlos():
    p = "gcv"; sun = (320, 100)
    far = f'<g id="far">{sierra(250)}{alhambra_hill(290, soft=True)}</g>'
    sc, scd, scl = ("#E7C98E", "#CFAE70", "#F3DEAE")
    pal = (f'<path d="M-10 140L400 140L400 400L-10 400Z" fill="{sc}" stroke="{INK}" stroke-width="1.8"/>'
           # planta baja almohadillada
           + "".join(f'<path d="M{x + (12 if (y // 22) % 2 else 0)} {y}H{x + (12 if (y // 22) % 2 else 0) + 30}V{y + 18}H{x + (12 if (y // 22) % 2 else 0)}Z" fill="{scl}" stroke="{scd}" stroke-width="1.2"/>' for x in range(-20, 400, 34) for y in range(272, 400, 22))
           + f'<path d="M-10 268L400 268L400 260L-10 260Z" fill="{scl}" stroke="{INK}" stroke-width="1.4"/>'
           # piso alto con pilastras jónicas y ventanas con óculo
           + "".join(f'<path d="M{x} 148V260" stroke="{scd}" stroke-width="7"/>' for x in range(0, 400, 64))
           + "".join(window(x + 22, 180, 20, 44, shutters=False, sw=1.3, lit=(x == 128)) + f'<circle cx="{x + 32}" cy="164" r="8" fill="{WIN}" stroke="{INK}" stroke-width="1.2"/>' for x in range(0, 380, 64))
           + "".join(window(x + 22, 300, 20, 40, shutters=False, sw=1.2) for x in range(0, 380, 64) if x not in (128, 192))
           + f'<path d="M160 400V310Q195 280 230 310V400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M-14 140L404 140L404 130L-14 130Z" fill="{scl}" stroke="{INK}" stroke-width="1.6"/>')
    mid = f'<g id="mid">{pal}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#CDB38E"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#D9C7A8")}'
            + person(120, 440, .9, SEA) + person(260, 442, .9, CLAY, dress=True) + person(280, 446, 1, "#34495E", hat=True)
            + cypress(20, 540, 200, 18) + cypress(372, 540, 190, 18) + "</g>")
    return doc(p, "Palacio de Carlos V", [sky(p, sun, [(80, 60, .8)], [(200, 60), (220, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_tristes():
    p = "gtr"; sun = (90, 120)
    far = f'<g id="far">{sierra(170)}{alhambra_hill(200)}</g>'
    sea = (f'<g id="sea">{river(p, 330, 400)}'
           + f'<path d="M-10 318L400 318L400 334L-10 334Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.4"/>'
           + "".join(f'<path d="M{x} 318H{x + 24}" stroke="#A8966E" stroke-width="1"/>' for x in range(-10, 400, 30))
           # puentecillo de piedra sobre el Darro
           + f'<path d="M230 400V356Q262 318 294 356V400H310V330H214V400Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.6"/>'
           + f'<path d="M210 330H314V322H210Z" fill="#DCC7A0" stroke="{INK}" stroke-width="1.4"/>'
           + tree(40, 326, 26, "#4F7F5A", "#3D6647") + tree(120, 322, 20, "#5A8B63", "#46714F")
           + f'<path d="M-10 396L400 396L400 404L-10 404Z" fill="#B9A88A"/></g>')
    near = (f'<g id="near"><rect x="-10" y="400" width="{W + 20}" height="170" fill="#D9C7A8"/><rect x="-10" y="400" width="{W + 20}" height="170" fill="url(#{p}dots)"/>'
            f'<path d="M-10 400L400 400L400 414L-10 414Z" fill="#C9B28A" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#BFAE8E"/>' for x in range(10, 390, 24) for y in (450, 490, 530))
            + person(110, 452, .95, SEA) + person(290, 450, .95, CLAY, dress=True) + person(310, 456, 1, "#34495E")
            + lamp(40, 540, 170) + lamp(350, 540, 170) + "</g>")
    return doc(p, "Paseo de los Tristes", [sky(p, sun, [(300, 60, .8)], [(220, 50), (240, 40, .8)]), far, sea, near, fx(p, sun, 400, .25)])


def s_banuelo():
    p = "gba"; sun = (195, 60)
    # interior: sin cielo; el «cielo» es la bóveda de ladrillo con tragaluces en estrella
    vault = (f'<g id="sky"><rect x="0" y="0" width="{W}" height="{H}" fill="#8A5A3E"/>'
             + "".join(f'<path d="M{x} 0V{H}" stroke="#7A4E34" stroke-width="1"/>' for x in range(0, W, 14))
             + "".join(f'<path d="M0 {y}H{W}" stroke="#9A6A4A" stroke-width="1"/>' for y in range(0, H, 10))
             + "".join(f'<path d="M{x} {y - 9}L{x + 3} {y - 3}L{x + 9} {y}L{x + 3} {y + 3}L{x} {y + 9}L{x - 3} {y + 3}L{x - 9} {y}L{x - 3} {y - 3}Z" fill="#FFF3DC"/>' for x, y in [(60, 50), (130, 30), (195, 60), (260, 30), (330, 50), (95, 100), (295, 100)])
             + "</g>")
    far = (f'<g id="far"><path d="M-10 230Q195 150 400 230L400 420L-10 420Z" fill="#B98A62"/>'
           + "".join(horseshoe(x, 260, 60, 160, "#5E3A26", 0.01).replace(f'stroke="{INK}" stroke-width="0.01"', 'stroke="none"') for x in (40, 165, 290))
           + "</g>")
    arches = ""
    for x in (-40, 110, 260):
        arches += f'<path d="M{x} 400V250" stroke="none"/>'
    mid = (f'<g id="mid"><path d="M-10 140L400 140L400 170L-10 170Z" fill="#C9966A" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 170Q{x + 64} 110 {x + 128} 170" fill="none" stroke="#E6C49A" stroke-width="10"/><path d="M{x} 170Q{x + 64} 110 {x + 128} 170" fill="none" stroke="{INK}" stroke-width="1.4"/>' for x in (-60, 68, 196, 324))
           + "".join(f'<path d="M{x - 8} 170H{x + 8}V400H{x - 8}Z" fill="#EDE3CF" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 12} 170H{x + 12}L{x + 8} 180H{x - 8}Z" fill="#D9C7A8" stroke="{INK}" stroke-width="1.2"/>' for x in (68, 196, 324))
           + f'<rect x="-10" y="396" width="{W + 20}" height="32" fill="#9A6A4A"/></g>')
    near = (f'<g id="near"><rect x="-10" y="410" width="{W + 20}" height="160" fill="#C49A70"/>'
            + "".join(f'<path d="M-10 {y}H400" stroke="#A87E58" stroke-width="1.2"/>' for y in (430, 460, 500, 548))
            + "".join(f'<path d="M195 410L{195 + i * 60} 560" stroke="#A87E58" stroke-width="1"/>' for i in range(-6, 7))
            + person(120, 440, .85, SEA) + person(280, 442, .85, CLAY, dress=True) + "</g>")
    light = (f'<g id="fx"><defs><linearGradient id="{p}beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4DC" stop-opacity=".45"/><stop offset="1" stop-color="#FFF4DC" stop-opacity="0"/></linearGradient>'
             f'<radialGradient id="{p}vig" cx=".5" cy=".45" r=".7"><stop offset=".45" stop-color="#2A1A10" stop-opacity="0"/><stop offset="1" stop-color="#2A1A10" stop-opacity=".45"/></radialGradient></defs>'
             + "".join(f'<path d="M{x - 6} {y}L{x + 6} {y}L{x + 40} 520L{x + 10} 520Z" fill="url(#{p}beam)"/>' for x, y in [(60, 50), (130, 30), (195, 60), (260, 30), (330, 50)])
             + f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}vig)"/></g>')
    return doc(p, "El Bañuelo", [vault, far, mid, near, light])


def s_corral():
    p = "gco"; sun = (300, 90)
    far = f'<g id="far">{far_city(240, 57)}</g>'
    c, cd, cl = ("#D9B98A", "#BF9C6C", "#EAD3AE")
    portal = (f'<path d="M50 110L340 110L340 400L50 400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M300 112L340 112L340 400L300 400Z" fill="{cd}" opacity=".6"/>'
              f'<path d="M46 110L344 110L344 98L46 98Z" fill="{TEJA}" stroke="{INK}" stroke-width="1.4"/>'
              # alfiz, arco de herradura y cúpula de mocárabes por encima
              f'<path d="M110 400V150H280V400" fill="none" stroke="{cl}" stroke-width="5"/>'
              f'<path d="M110 150H280" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M116 158H274V210H116Z" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>'
              + muqarnas(118, 160, 154, rows=5)
              + horseshoe(128, 214, 134, 186, "#5E4232", 1.8)
              # el patio al fondo, con su galería
              + f'<path d="M150 400V300H240V400Z" fill="#E6D3AE"/>'
              + "".join(f'<path d="M{x} 300V400" stroke="#8A6A4A" stroke-width="3"/>' for x in (165, 195, 225))
              + f'<path d="M150 320H240M150 352H240" stroke="#8A6A4A" stroke-width="2"/>'
              + f'<path d="M140 236H250V226H140Z" fill="{SEA}" opacity=".0"/>'
              # ventanas altas
              + window(76, 150, 16, 28, shutters=False, arch=True, sw=1.1) + window(298, 150, 16, 28, shutters=False, arch=True, sw=1.1))
    side = house(-30, 180, 90, 220, CAL, floors=3, cols=2) + house(336, 190, 80, 210, PINK, floors=3, cols=2, lit={(0, 0)})
    mid = f'<g id="mid">{side}{portal}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + person(90, 442, .9, SEA) + person(310, 440, .9, CLAY, dress=True)
            + lamp(40, 540, 170) + "</g>")
    return doc(p, "Corral del Carbón", [sky(p, sun, [(80, 60, .8)], [(220, 50), (240, 40, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"plaza": s_plaza, "capilla": s_capilla, "sannicolas": s_sannicolas, "pesas": s_pesas, "justicia": s_justicia,
          "carlos": s_carlos, "tristes": s_tristes, "banuelo": s_banuelo, "corral": s_corral}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_granada_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos de Granada generados:", ", ".join(SCENES))
