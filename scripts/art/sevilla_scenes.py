#!/usr/bin/env python3
"""
Fondos de Sevilla (390×560, un grupo por capa como los de Cádiz y Málaga).

Uso: python3 scripts/art/sevilla_scenes.py && python3 scripts/art/render_layers.py sevilla_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, SHUT, W, H, WHITE, YELLOW, PINK, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)

# Paleta sevillana: albero, almagra, ladrillo de la Giralda y piedra de la catedral
ALBERO = ("#EDC56A", "#D3A84C", "#F6DC98")
ALMAGRA = ("#B5553A", "#96432C", "#CF7458")
BRICK = ("#DDA57C", "#C28862", "#EDC2A0")
GOTHIC = ("#E6D3AE", "#CDB68C", "#F4E7CC")


def orange_tree(x, base, r=22):
    s = tree(x, base, r, "#3F7A4E", "#2F6440")
    for dx, dy in [(-.5, -1.7), (.3, -1.9), (.6, -1.4), (-.7, -1.25), (0, -1.5), (.2, -2.3), (-.2, -1.1)]:
        s += f'<circle cx="{f(x + dx * r)}" cy="{f(base + dy * r)}" r="{f(r * .12)}" fill="#F29A2E" stroke="#B8651C" stroke-width=".6"/>'
    return s + f'<path d="M{f(x - r * .9)} {f(base)}L{f(x + r * .9)} {f(base)}" stroke="#8A6A4A" stroke-width="3"/>'


def sebka(x, y, w, h, c):
    """Paño de rombos (sebka) de la Giralda."""
    s = ""
    step = w / 3
    for i in range(3):
        cx = x + step * (i + .5)
        s += f'<path d="M{f(cx)} {f(y)}L{f(cx + step / 2)} {f(y + h / 2)}L{f(cx)} {f(y + h)}L{f(cx - step / 2)} {f(y + h / 2)}Z" fill="none" stroke="{c}" stroke-width="1.2"/>'
    return s


def giralda(x, base, w=70, top=24, stroke=1.8, soft=False):
    """La Giralda: caña almohade de ladrillo con paños de rombos, campanario renacentista y el Giraldillo."""
    ink = "none" if soft else INK
    sw = 0 if soft else stroke
    b, bd, bl = BRICK
    wh, whd, whl = WHITE
    h = base - top
    shaft_top = top + h * .34
    s = f'<path d="M{f(x)} {f(base)}L{f(x)} {f(shaft_top)}L{f(x + w)} {f(shaft_top)}L{f(x + w)} {f(base)}Z" fill="{b}" stroke="{ink}" stroke-width="{sw}"/>'
    s += f'<path d="M{f(x + w * .74)} {f(shaft_top)}L{f(x + w)} {f(shaft_top)}L{f(x + w)} {f(base)}L{f(x + w * .74)} {f(base)}Z" fill="{bd}" opacity=".7"/>'
    if not soft:
        for k in range(3):
            y = shaft_top + 16 + k * (base - shaft_top - 30) / 3
            s += sebka(x + 6, y, w * .26, 34, bd) + sebka(x + w * .66 - 6, y, w * .26, 34, bd)
            s += f'<path d="M{f(x + w * .42)} {f(y + 30)}L{f(x + w * .42)} {f(y + 12)}Q{f(x + w / 2)} {f(y + 4)} {f(x + w * .58)} {f(y + 12)}L{f(x + w * .58)} {f(y + 30)}Z" fill="{WIN}" stroke="{INK}" stroke-width="1.1"/>'
    # cuerpo de campanas
    bw = w * .86
    bx = x + (w - bw) / 2
    bell_top = top + h * .17
    s += f'<path d="M{f(bx)} {f(shaft_top)}L{f(bx)} {f(bell_top)}L{f(bx + bw)} {f(bell_top)}L{f(bx + bw)} {f(shaft_top)}Z" fill="{wh}" stroke="{ink}" stroke-width="{sw}"/>'
    s += f'<path d="M{f(x - 3)} {f(shaft_top)}L{f(x + w + 3)} {f(shaft_top)}L{f(x + w + 3)} {f(shaft_top - 5)}L{f(x - 3)} {f(shaft_top - 5)}Z" fill="{whl}" stroke="{ink}" stroke-width="{sw * .8:.2f}"/>'
    for i in range(3):
        ax = bx + bw * (i + .5) / 3
        s += f'<path d="M{f(ax - bw * .1)} {f(shaft_top - 8)}L{f(ax - bw * .1)} {f(bell_top + 14)}Q{f(ax)} {f(bell_top + 4)} {f(ax + bw * .1)} {f(bell_top + 14)}L{f(ax + bw * .1)} {f(shaft_top - 8)}Z" fill="{WIN if not soft else whd}" stroke="{ink}" stroke-width="{sw * .6:.2f}"/>'
        if not soft:
            s += f'<path d="M{f(ax - 5)} {f(bell_top + 30)}Q{f(ax)} {f(bell_top + 16)} {f(ax + 5)} {f(bell_top + 30)}Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
    # cuerpos superiores y remate
    t1w, t2w = bw * .72, bw * .46
    t1x, t2x = x + (w - t1w) / 2, x + (w - t2w) / 2
    t1top = top + h * .08
    s += f'<path d="M{f(t1x)} {f(bell_top)}L{f(t1x)} {f(t1top)}L{f(t1x + t1w)} {f(t1top)}L{f(t1x + t1w)} {f(bell_top)}Z" fill="{whl}" stroke="{ink}" stroke-width="{sw}"/>'
    s += f'<path d="M{f(t1x + t1w * .35)} {f(bell_top - 4)}L{f(t1x + t1w * .35)} {f(t1top + 10)}Q{f(x + w / 2)} {f(t1top + 4)} {f(t1x + t1w * .65)} {f(t1top + 10)}L{f(t1x + t1w * .65)} {f(bell_top - 4)}Z" fill="{WIN if not soft else whd}"/>'
    t2top = top + h * .03
    s += f'<path d="M{f(t2x)} {f(t1top)}L{f(t2x)} {f(t2top)}L{f(t2x + t2w)} {f(t2top)}L{f(t2x + t2w)} {f(t1top)}Z" fill="{wh}" stroke="{ink}" stroke-width="{sw}"/>'
    s += f'<path d="M{f(t2x)} {f(t2top)}Q{f(x + w / 2)} {f(top - 4)} {f(t2x + t2w)} {f(t2top)}Z" fill="{ALBERO[0] if not soft else whd}" stroke="{ink}" stroke-width="{sw}"/>'
    # Giraldillo
    gx = x + w / 2
    gy = top - 4
    s += f'<path d="M{f(gx)} {f(gy)}L{f(gx)} {f(gy - 10)}" stroke="{"#8E6640" if not soft else whd}" stroke-width="2"/>'
    s += f'<path d="M{f(gx - 3)} {f(gy - 10)}L{f(gx + 3)} {f(gy - 10)}L{f(gx + 2)} {f(gy - 20)}L{f(gx - 2)} {f(gy - 20)}Z" fill="{"#8E6640" if not soft else whd}"/>'
    s += f'<circle cx="{f(gx)}" cy="{f(gy - 22)}" r="2.4" fill="{"#8E6640" if not soft else whd}"/>'
    s += f'<path d="M{f(gx + 3)} {f(gy - 18)}L{f(gx + 12)} {f(gy - 19)}L{f(gx + 12)} {f(gy - 13)}L{f(gx + 3)} {f(gy - 14)}Z" fill="{"#B8895A" if not soft else whd}"/>'
    return s


def pinnacles(x0, x1, y, n, c=GOTHIC, h=22, stroke=1.3):
    s = ""
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        s += f'<path d="M{f(x - 4)} {f(y)}L{f(x - 4)} {f(y - h * .5)}L{f(x)} {f(y - h)}L{f(x + 4)} {f(y - h * .5)}L{f(x + 4)} {f(y)}Z" fill="{c[2]}" stroke="{INK}" stroke-width="{stroke}"/>'
    return s


def gothic_wall(x, y, w, h, stroke=1.8):
    c, cd, cl = GOTHIC
    s = f'<path d="M{f(x)} {f(y)}L{f(x + w)} {f(y)}L{f(x + w)} {f(y + h)}L{f(x)} {f(y + h)}Z" fill="{c}" stroke="{INK}" stroke-width="{stroke}"/>'
    for i in range(int(w // 46) + 1):
        bx = x + 10 + i * 46
        s += f'<path d="M{f(bx)} {f(y)}L{f(bx + 10)} {f(y)}L{f(bx + 10)} {f(y + h)}L{f(bx)} {f(y + h)}Z" fill="{cd}" stroke="{INK}" stroke-width="{stroke * .6:.2f}"/>'
        s += f'<path d="M{f(bx + 20)} {f(y + h * .7)}L{f(bx + 20)} {f(y + 30)}Q{f(bx + 28)} {f(y + 14)} {f(bx + 36)} {f(y + 30)}L{f(bx + 36)} {f(y + h * .7)}Z" fill="{WIN}" stroke="{INK}" stroke-width="{stroke * .6:.2f}"/>'
    return s + pinnacles(x + 15, x + w - 15, y, int(w // 46) + 1)


def river(p, y0, y1, bank="#8FB9B4"):
    s = f'<rect x="-10" y="{y0}" width="{W + 20}" height="{y1 - y0}" fill="url(#{p}sea)"/>'
    for x, y, ln in [(20, y0 + 14, 30), (130, y0 + 30, 24), (270, y0 + 18, 34), (60, y0 + 50, 22), (300, y0 + 48, 28), (190, y0 + 70, 26)]:
        if y < y1 - 4:
            s += f'<path d="M{x} {y}L{x + ln} {y}" stroke="#E6F2EF" stroke-width="1.6" opacity=".7"/>'
    return s


def horse_carriage(x, y):
    return (f'<ellipse cx="{x + 30}" cy="{y + 2}" rx="44" ry="4" fill="#5B3524" opacity=".18"/>'
            f'<path d="M{x} {y - 30}L{x + 34} {y - 30}L{x + 38} {y - 12}L{x - 4} {y - 12}Z" fill="#2E3A48"/>'
            f'<path d="M{x + 2} {y - 30}Q{x + 16} {y - 44} {x + 30} {y - 30}" fill="#2E3A48"/>'
            f'<circle cx="{x + 4}" cy="{y - 6}" r="7" fill="none" stroke="#6E4C33" stroke-width="2.4"/><circle cx="{x + 32}" cy="{y - 6}" r="9" fill="none" stroke="#6E4C33" stroke-width="2.4"/>'
            f'<path d="M{x + 40} {y - 14}L{x + 50} {y - 16}" stroke="#2E3A48" stroke-width="2"/>'
            f'<path d="M{x + 50} {y - 24}Q{x + 58} {y - 30} {x + 72} {y - 26}L{x + 76} {y - 38}L{x + 82} {y - 34}L{x + 78} {y - 22}L{x + 76} {y - 14}L{x + 76} {y}M{x + 54} {y - 16}L{x + 52} {y}M{x + 70} {y - 18}L{x + 70} {y}" fill="#8A5A3A" stroke="#6E4630" stroke-width="3"/>')


# ---------------------------------------------------------------------------
def s_giralda():
    p = "sgi"; sun = (90, 120)
    far = f'<g id="far">{far_city(290, 31)}</g>'
    mid = (f'<g id="mid">{gothic_wall(-20, 250, 200, 150)}{giralda(200, 400, 74, 30)}'
           + house(300, 270, 110, 130, ALBERO, floors=2, cols=2, lit={(0, 0)})
           + f'<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>')
    near = (f'<g id="near">{floor(p, 420)}'
            + orange_tree(40, 470, 26) + orange_tree(352, 474, 26)
            + horse_carriage(210, 470)
            + person(120, 440, .9, CLAY, dress=True) + person(150, 446, 1, "#34495E", hat=True)
            + lamp(92, 540, 170) + "</g>")
    return doc(p, "La Giralda", [sky(p, sun, [(300, 70, .9)], [(140, 60), (160, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_catedral():
    p = "sca"; sun = (320, 110)
    far = f'<g id="far">{far_city(270, 33)}{giralda(28, 300, 44, 70, soft=True)}</g>'
    c, cd, cl = GOTHIC
    portal = (gothic_wall(-20, 190, 430, 210)
              + f'<path d="M120 400L120 150L270 150L270 400Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M110 150L195 70L280 150Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              + pinnacles(110, 280, 150, 2, h=40) + pinnacles(195, 195, 72, 1, h=26)
              + "".join(f'<path d="M{195 - k * 9} 400L{195 - k * 9} {290 - k * 6}Q195 {200 - k * 10} {195 + k * 9} {290 - k * 6}L{195 + k * 9} 400" fill="none" stroke="{cd if k % 2 else INK}" stroke-width="{1.6 if k % 2 == 0 else 3}"/>' for k in range(2, 7))
              + f'<path d="M165 400L165 300Q195 250 225 300L225 400Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M195 272L195 400" stroke="#3A2418" stroke-width="1.4"/>'
              f'<circle cx="195" cy="128" r="17" fill="{c}" stroke="{INK}" stroke-width="1.6"/><circle cx="195" cy="128" r="10" fill="{LIT}" stroke="{INK}" stroke-width="1.3"/>'
              + "".join(f'<path d="M195 128L{f(195 + math.cos(math.radians(a)) * 10)} {f(128 + math.sin(math.radians(a)) * 10)}" stroke="{INK}" stroke-width="1"/>' for a in range(0, 360, 45)))
    mid = f'<g id="mid">{portal}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            # réplica del Giraldillo sobre su pedestal
            + f'<path d="M318 470L318 400L348 400L348 470Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/><path d="M312 400L354 400L354 392L312 392Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M324 392L326 350Q333 340 340 350L342 392Z" fill="#8E6640" stroke="{INK}" stroke-width="1.6"/><circle cx="333" cy="342" r="6" fill="#8E6640" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M342 360L352 330L352 316" stroke="{INK}" stroke-width="2"/><path d="M352 318L368 322L352 328Z" fill="#B8895A" stroke="{INK}" stroke-width="1.2"/>'
            + person(90, 440, .9, SEA) + person(240, 436, .85, "#6E2C5E", dress=True)
            + lamp(40, 540, 170) + orange_tree(262, 560, 30) + "</g>")
    return doc(p, "Catedral de Sevilla", [sky(p, sun, [(80, 60, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def s_torreoro():
    p = "sto"; sun = (290, 130)
    far = f'<g id="far">{far_city(292, 35, "#E8BC98", "#EDC9A8", towers=3)}<rect x="-10" y="290" width="{W + 20}" height="20" fill="#E3B48E"/></g>'
    # torre dodecagonal de tres cuerpos, sobre el río
    tx, tw = 60, 110
    t = (f'<path d="M{tx} 390L{tx} 220L{tx + tw} 220L{tx + tw} 390Z" fill="#E7C47E" stroke="{INK}" stroke-width="1.8"/>'
         + "".join(f'<path d="M{tx + tw * k / 6} 222L{tx + tw * k / 6} 390" stroke="#D2A85E" stroke-width="1.4"/>' for k in range(1, 6))
         + f'<path d="M{tx + tw * .7} 222L{tx + tw} 222L{tx + tw} 390L{tx + tw * .7} 390Z" fill="#D2A85E" opacity=".7"/>'
         + f'<path d="M{tx - 5} 220L{tx + tw + 5} 220L{tx + tw + 5} 210L{tx - 5} 210Z" fill="#F2D48F" stroke="{INK}" stroke-width="1.6"/>'
         + "".join(f'<path d="M{tx - 3 + i * 12} 210L{tx - 3 + i * 12} 200L{tx + 5 + i * 12} 200L{tx + 5 + i * 12} 210" fill="#F2D48F" stroke="{INK}" stroke-width="1.2"/>' for i in range(10))
         + window(tx + 44, 260, 22, 36, shutters=False, arch=True, sw=1.3)
         + window(tx + 46, 320, 18, 28, shutters=False, arch=True, sw=1.2, lit=True)
         + f'<path d="M{tx + 25} 200L{tx + 25} 140L{tx + 85} 140L{tx + 85} 200Z" fill="#E7C47E" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M{tx + 68} 142L{tx + 85} 142L{tx + 85} 200L{tx + 68} 200Z" fill="#D2A85E" opacity=".7"/>'
         + window(tx + 47, 156, 16, 26, shutters=False, arch=True, sw=1.2)
         + f'<path d="M{tx + 38} 140L{tx + 38} 110L{tx + 72} 110L{tx + 72} 140Z" fill="#F2D48F" stroke="{INK}" stroke-width="1.5"/>'
         f'<path d="M{tx + 36} 110Q{tx + 55} 78 {tx + 74} 110Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M{tx + 55} 88L{tx + 55} 74" stroke="{INK}" stroke-width="1.6"/>')
    sea = (f'<g id="sea">{river(p, 300, 420)}'
           + f'<path d="M-10 300L400 300L400 306L-10 306Z" fill="#D9C3A0"/>'
           + t
           + f'<path d="M{tx - 10} 390L{tx + tw + 10} 390L{tx + tw + 14} 400L{tx - 14} 400Z" fill="#D9C3A0" stroke="{INK}" stroke-width="1.4"/>'
           # barco turístico
           + f'<path d="M230 360L330 360L322 374L238 374Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><path d="M246 360L246 346L312 346L312 360" fill="{SEA}" stroke="{INK}" stroke-width="1.4"/>'
           + "".join(f'<rect x="{x}" y="349" width="8" height="6" fill="{PAPER}"/>' for x in range(252, 306, 12))
           + f'<path d="M-10 408Q80 402 180 408T400 406L400 422L-10 422Z" fill="#DCC3A0"/></g>')
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + palm(300, 470, 250, -10, 1.0) + palm(360, 480, 210, -6, .85)
            + person(140, 440, .9, SEA) + person(170, 446, 1, CLAY, dress=True)
            + lamp(40, 540, 170) + bench(200, 490) + "</g>")
    return doc(p, "Torre del Oro", [sky(p, sun, [(80, 60, .9), (330, 70, .6)], [(200, 60), (220, 50, .8)]), far, sea, near, fx(p, sun, 420, .25)])


def s_triana():
    p = "str"; sun = (110, 120)
    far = (f'<g id="far">{far_city(270, 37, "#E8BC98", "#EDC9A8", towers=2)}'
           + "".join(house(x, 200, 60, 90, c, floors=2, cols=2, stroke=0.01, roof_rail=False) for x, c in [(150, ALBERO), (210, PINK), (270, WHITE), (330, ALBERO)]).replace(f'stroke="{INK}" stroke-width="0.01"', 'stroke="none"')
           + f'<rect x="-10" y="286" width="{W + 20}" height="22" fill="#E3B48E"/></g>')
    # puente de hierro con los aros, y la Capillita del Carmen al final
    bridge = f'<path d="M-20 270L400 270L400 282L-20 282Z" fill="#6E8A8E" stroke="{INK}" stroke-width="1.6"/>'
    for i in range(4):
        x0 = -20 + i * 110
        bridge += f'<path d="M{x0} 282Q{x0 + 55} 350 {x0 + 110} 282" fill="none" stroke="#5A7478" stroke-width="7"/><path d="M{x0} 282Q{x0 + 55} 350 {x0 + 110} 282" fill="none" stroke="{INK}" stroke-width="1.4"/>'
        for k in range(1, 6):
            cx = x0 + k * 110 / 6
            dy = 282 + 68 * (1 - ((k - 3) / 3) ** 2) * .5
            r = max(3.5, (dy - 282) / 2 - 1)
            bridge += f'<circle cx="{f(cx)}" cy="{f(282 + (dy - 282) / 2)}" r="{f(r)}" fill="none" stroke="#5A7478" stroke-width="2"/>'
        bridge += f'<path d="M{x0 + 110} 282L{x0 + 104} 420L{x0 + 116} 420Z" fill="#D9C3A0" stroke="{INK}" stroke-width="1.2"/>'
    bridge += "".join(f'<path d="M{x} 270L{x} 256" stroke="{INK}" stroke-width="1.2"/>' for x in range(-20, 400, 10)) + f'<path d="M-20 256L400 256" stroke="{INK}" stroke-width="1.8"/>'
    cap = (f'<path d="M318 270L318 196L366 196L366 270Z" fill="{ALMAGRA[0]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M322 200L362 200L362 266L322 266Z" fill="none" stroke="{WHITE[0]}" stroke-width="2"/>'
           f'<path d="M334 266L334 230Q342 220 350 230L350 266Z" fill="{WIN}" stroke="{INK}" stroke-width="1.2"/>'
           f'<path d="M314 196L370 196L370 188L314 188Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M322 188Q342 156 362 188Z" fill="{ALBERO[0]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{342 + d} 164Q{342 + d * 1.6} 176 {342 + d * 1.8} 188" fill="none" stroke="{SEA}" stroke-width="1.6"/>' for d in (-6, 0, 6))
           + f'<path d="M342 160L342 146M337 152L347 152" stroke="{INK}" stroke-width="1.6"/>')
    sea = f'<g id="sea">{river(p, 300, 422)}{bridge}{cap}<path d="M-10 410Q90 404 190 410T400 408L400 424L-10 424Z" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + f'<path d="M-10 420L400 420L400 432L-10 432Z" fill="#CDB38E"/>'
            + "".join(f'<path d="M{x} 432L{x} 414" stroke="#2E3A48" stroke-width="2"/>' for x in range(0, 390, 14)) + f'<path d="M-10 414L400 414" stroke="#2E3A48" stroke-width="2.4"/>'
            + person(150, 452, .95, CLAY, dress=True) + person(250, 456, 1, "#34495E", hat=True)
            + lamp(60, 540, 160) + lamp(330, 540, 160) + "</g>")
    return doc(p, "Puente de Triana", [sky(p, sun, [(300, 70, .9)], [(210, 60), (230, 50, .8)]), far, sea, near, fx(p, sun, 420, .25)])


def s_archivo():
    p = "sar"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 39)}{giralda(300, 260, 40, 60, soft=True)}</g>'
    c, cd, cl = PINK[0], PINK[1], PINK[2]
    bx, bw = 20, 350
    b = (f'<path d="M{bx} 170L{bx + bw} 170L{bx + bw} 400L{bx} 400Z" fill="#EBC3A6" stroke="{INK}" stroke-width="1.8"/>'
         f'<path d="M{bx + bw - 30} 172L{bx + bw} 172L{bx + bw} 400L{bx + bw - 30} 400Z" fill="#D9A888" opacity=".7"/>'
         # pilastras de piedra gris y cornisas
         + "".join(f'<path d="M{x} 170L{x + 10} 170L{x + 10} 400L{x} 400Z" fill="#CFC6B8" stroke="{INK}" stroke-width="1"/>' for x in range(bx + 4, bx + bw, 58))
         + f'<path d="M{bx - 4} 280L{bx + bw + 4} 280L{bx + bw + 4} 288L{bx - 4} 288Z" fill="#DCD3C6" stroke="{INK}" stroke-width="1.4"/>'
         f'<path d="M{bx - 6} 170L{bx + bw + 6} 170L{bx + bw + 6} 160L{bx - 6} 160Z" fill="#DCD3C6" stroke="{INK}" stroke-width="1.6"/>'
         # balaustrada con remates de bola y pirámide
         + f'<path d="M{bx} 160L{bx} 146L{bx + bw} 146L{bx + bw} 160" fill="#DCD3C6" stroke="{INK}" stroke-width="1.3"/>'
         + "".join(f'<path d="M{x} 146L{x} 140M{x - 3} 140L{x + 3} 140L{x} 128Z" fill="#DCD3C6" stroke="{INK}" stroke-width="1.2"/><circle cx="{x}" cy="126" r="2.4" fill="#DCD3C6" stroke="{INK}" stroke-width="1"/>' for x in range(bx + 9, bx + bw, 58))
         + "".join(window(x, y, 18, 40, shutters=False, balcony=False, lit=(x, y) == (bx + 78, 200), sw=1.2) for x in range(bx + 20, bx + bw - 20, 58) for y in (200, 310))
         + "".join(f'<path d="M{x - 3} {y - 4}L{x + 21} {y - 4}L{x + 9} {y - 12}Z" fill="#DCD3C6" stroke="{INK}" stroke-width="1"/>' for x in range(bx + 20, bx + bw - 20, 58) for y in (200, 310)))
    mid = f'<g id="mid">{b}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + orange_tree(30, 480, 28) + orange_tree(360, 484, 28)
            + person(160, 440, .9, "#34495E", hat=True) + person(230, 444, .9, SEA)
            + lamp(100, 540, 160) + bench(260, 490) + "</g>")
    return doc(p, "Archivo de Indias", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_alcazar():
    p = "sal"; sun = (90, 110)
    far = (f'<g id="far">{far_city(250, 41)}{giralda(40, 250, 40, 40, soft=True)}</g>')
    c, cd, cl = ALMAGRA
    wall = (f'<path d="M-20 200L410 200L410 400L-20 400Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 200L{x} 186L{x + 14} 186L{x + 14} 200" fill="{c}" stroke="{INK}" stroke-width="1.4"/>' for x in range(-16, 400, 24))
            + "".join(f'<path d="M{x} {y}L{x + 30} {y}" stroke="{cd}" stroke-width="1.2"/>' for x in range(-10, 400, 50) for y in (240, 290, 340))
            # torres a los lados
            + f'<path d="M20 400L20 170L80 170L80 400Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 170L{x} 158L{x + 10} 158L{x + 10} 170" fill="{cl}" stroke="{INK}" stroke-width="1.3"/>' for x in (22, 38, 54, 68))
            + f'<path d="M310 400L310 170L370 170L370 400Z" fill="{cl}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<path d="M{x} 170L{x} 158L{x + 10} 158L{x + 10} 170" fill="{cl}" stroke="{INK}" stroke-width="1.3"/>' for x in (312, 328, 344, 358))
            # la puerta y el panel de azulejos con el león
            + f'<path d="M160 400L160 320Q195 284 230 320L230 400Z" fill="#3A2A20" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M150 400L150 318Q195 272 240 318L240 400" fill="none" stroke="{WHITE[0]}" stroke-width="5"/>'
            f'<path d="M160 216L230 216L230 272L160 272Z" fill="#F6EBD2" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M164 220L226 220L226 268L164 268Z" fill="none" stroke="{SEA}" stroke-width="1.6"/>'
            f'<path d="M176 262L178 248Q176 240 182 236Q190 232 198 236L206 234Q212 236 210 242L204 246L206 262H200L198 252H186L184 262Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.3"/>'
            f'<path d="M182 236Q178 228 186 226Q192 222 198 228Q202 234 198 238Q190 242 182 236Z" fill="#C9962A" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M214 226V248M209 232H219" stroke="{CLAY}" stroke-width="2"/>')
    mid = f'<g id="mid">{palm(120, 200, 110, 6, .7)}{palm(270, 200, 120, -4, .75)}{wall}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + person(120, 442, .9, SEA) + person(280, 440, .9, "#6E2C5E", dress=True) + person(300, 446, 1, "#34495E")
            + orange_tree(30, 500, 30) + lamp(360, 540, 160) + "</g>")
    return doc(p, "Real Alcázar, Puerta del León", [sky(p, sun, [(300, 70, .9)], [(220, 60), (240, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def s_triunfo():
    p = "stu"; sun = (320, 120)
    far = f'<g id="far">{far_city(290, 43)}{giralda(70, 300, 60, 30, soft=False, stroke=1.2)}</g>'
    # columna del Triunfo con la Virgen en lo alto, catedral y archivo a los lados
    col = (f'<path d="M180 400L180 368L210 368L210 400Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M172 368L218 368L218 360L172 360Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M186 360L188 170L202 170L204 360Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M187 {y}Q195 {y - 6} 203 {y}" fill="none" stroke="{STONE[1]}" stroke-width="1.4"/>' for y in range(190, 360, 22))
           + f'<path d="M182 170L208 170L208 162L182 162Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M188 162L190 132Q195 124 200 132L202 162Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.4"/><circle cx="195" cy="126" r="5" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.2"/>'
           f'<path d="M188 118Q195 112 202 118" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    mid = (f'<g id="mid">{gothic_wall(-20, 240, 150, 160)}'
           + f'<path d="M270 240L410 240L410 400L270 400Z" fill="#EBC3A6" stroke="{INK}" stroke-width="1.8"/>'
           + "".join(window(x, 270, 16, 36, shutters=False, sw=1.2) + window(x, 340, 16, 36, shutters=False, sw=1.2) for x in (290, 340, 386))
           + f'<path d="M266 240L414 240L414 230L266 230Z" fill="#DCD3C6" stroke="{INK}" stroke-width="1.4"/>'
           + col + f'<rect x="-10" y="396" width="{W + 20}" height="32" fill="#DCC3A0"/></g>')
    near = (f'<g id="near">{floor(p, 420)}'
            + orange_tree(40, 486, 30) + orange_tree(350, 490, 30)
            + horse_carriage(110, 452)
            + person(250, 440, .9, CLAY, dress=True) + person(272, 446, 1, SEA)
            + lamp(300, 540, 170) + "</g>")
    return doc(p, "Plaza del Triunfo", [sky(p, sun, [(260, 60, .8)], [(150, 50), (170, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def s_santacruz():
    p = "ssc"; sun = (220, 80)
    far = f'<g id="far">{far_city(250, 45, towers=2)}{giralda(170, 260, 36, 70, soft=True)}</g>'

    def side(left):
        s = ""
        for k in range(4):
            x0 = -30 + k * 34 if left else W + 30 - k * 34
            x1 = x0 + (44 if left else -44)
            top0, top1 = 110 + k * 30, 128 + k * 32
            bot = 470 - k * 24
            xa, xb = (x0, x1) if left else (x1, x0)
            ta, tb = (top0, top1) if left else (top1, top0)
            if left:
                c = WHITE if k % 2 == 0 else ("#F7EFD9", "#E6D8B8", "#FFF8E6")
                s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot - 10}L{xa} {bot}Z" fill="{c[0]}" stroke="{INK}" stroke-width="1.6"/>'
                s += f'<path d="M{xa} {bot - 26}L{xb} {bot - 34}L{xb} {bot - 10}L{xa} {bot}Z" fill="{ALBERO[0]}" stroke="{INK}" stroke-width="1.2"/>'
                s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {tb + 8}L{xa} {ta + 8}Z" fill="{ALBERO[0]}"/>'
                for fl in range(2):
                    y = ta + 50 + fl * 110
                    s += f'<path d="M{xa + 10} {y}L{xb - 10} {y + 4}L{xb - 10} {y + 50}L{xa + 10} {y + 46}Z" fill="{WIN}" stroke="{INK}" stroke-width="1.2"/>'
                    s += "".join(f'<path d="M{xa + 10 + i * (xb - xa - 20) / 4:.1f} {y + i:.1f}L{xa + 10 + i * (xb - xa - 20) / 4:.1f} {y + 46 + i:.1f}" stroke="{INK}" stroke-width="1.4"/>' for i in range(5))
                    # macetas de geranios
                    s += f'<path d="M{xa + 8} {y - 16}L{xa + 18} {y - 16}L{xa + 16} {y - 6}L{xa + 10} {y - 6}Z" fill="{SEA}" stroke="{INK}" stroke-width="1"/>'
                    s += f'<circle cx="{xa + 11}" cy="{y - 20}" r="3.4" fill="{CLAY}"/><circle cx="{xa + 16}" cy="{y - 21}" r="3" fill="#E0766A"/><circle cx="{xa + 13}" cy="{y - 24}" r="2.6" fill="#3F7A4E"/>'
            else:
                # muralla del Alcázar, de albero, con almenas
                s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot - 10}L{xa} {bot}Z" fill="{ALBERO[0]}" stroke="{INK}" stroke-width="1.6"/>'
                s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {tb - 12}L{xa} {ta - 12}Z" fill="{ALBERO[2]}" stroke="{INK}" stroke-width="1.2"/>'
                for i in range(4):
                    mx = xa + 4 + i * (xb - xa - 8) / 4
                    my = ta - 12 + (mx - xa) / (xb - xa) * (tb - ta)
                    s += f'<path d="M{mx:.1f} {my:.1f}L{mx:.1f} {my - 9:.1f}L{mx + 6:.1f} {my - 9:.1f}L{mx + 6:.1f} {my:.1f}Z" fill="{ALBERO[2]}" stroke="{INK}" stroke-width="1.1"/>'
                s += "".join(f'<path d="M{xa + 4} {y}L{xb - 4} {y + (tb - ta) * .8:.1f}" stroke="{ALBERO[1]}" stroke-width="1.2"/>' for y in range(ta + 60, bot - 40, 70))
        return s
    mid = f'<g id="mid">{side(False)}{side(True)}{orange_tree(200, 404, 22)}<rect x="-10" y="400" width="{W + 20}" height="28" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + person(180, 436, .8, SEA) + person(215, 432, .75, CLAY, dress=True)
            + lamp(40, 540, 170) + "</g>")
    return doc(p, "Callejón del Agua", [sky(p, sun, [(90, 60, .8)], [(280, 40), (300, 30, .8)]), far, mid, near, fx(p, sun, 420)])


def s_colon():
    p = "sco"; sun = (300, 120)
    far = f'<g id="far">{far_city(280, 47)}</g>'
    trees = tree(40, 400, 60, "#4B7C58", "#3A6446") + tree(350, 404, 62, "#4B7C58", "#3A6446") + tree(110, 400, 40, "#5A8B63", "#46714F") + tree(290, 400, 40, "#5A8B63", "#46714F")
    # monumento: dos columnas unidas, carabela arriba, león delante
    mon = (f'<path d="M150 400L150 350L240 350L240 400Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M144 350L246 350L246 340L144 340Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M170 340L172 120L188 120L190 340Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M200 340L202 120L218 120L220 340Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M184 122L186 340M214 122L216 340" stroke="{STONE[1]}" stroke-width="3"/>'
           + "".join(f'<path d="M168 {y}L222 {y}" stroke="{STONE[1]}" stroke-width="1.4"/>' for y in (180, 250))
           + f'<circle cx="195" cy="300" r="12" fill="#6E8A7A" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M164 120L226 120L226 110L164 110Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           # carabela
           + f'<path d="M168 96L222 96L216 108L174 108Z" fill="#6E5A3E" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M195 96L195 54M181 96L181 70M209 96L209 68" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M187 62Q195 60 203 62Q204 74 203 86Q195 84 187 86Q186 74 187 62Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.3"/>'
           f'<path d="M195 66V82M190 73H200" stroke="{CLAY}" stroke-width="1.8"/>'
           f'<path d="M209 70L218 88H209Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.2"/>'
           # león de bronce sentado, delante del pedestal
           f'<path d="M150 340Q148 322 158 316L176 316Q184 322 184 340Z" fill="#6B5A40" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M150 340Q146 330 142 332" fill="none" stroke="{INK}" stroke-width="1.6"/>'
           f'<circle cx="176" cy="308" r="11" fill="#54462F" stroke="{INK}" stroke-width="1.4"/>'
           f'<circle cx="178" cy="309" r="6.5" fill="#7A6848" stroke="{INK}" stroke-width="1.2"/>'
           f'<circle cx="180" cy="307" r="1" fill="{INK}"/><path d="M181 312L184 312" stroke="{INK}" stroke-width="1"/>'
           f'<path d="M172 340L172 326M180 340L180 326" stroke="{INK}" stroke-width="1.2"/>')
    mid = f'<g id="mid">{trees}{mon}<rect x="-10" y="396" width="{W + 20}" height="32" fill="#D8C09A"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + palm(40, 470, 240, 10, 1.0)
            + person(260, 440, .9, CLAY, dress=True) + person(282, 446, 1, "#34495E", hat=True) + person(120, 438, .8, SEA)
            + bench(250, 490) + lamp(350, 540, 160) + "</g>")
    return doc(p, "Monumento a Colón, Jardines de Murillo", [sky(p, sun, [(80, 60, .9)], [(220, 60), (240, 50, .8)]), far, mid, near, fx(p, sun, 420)])


SCENES = {"giralda": s_giralda, "catedral": s_catedral, "torreoro": s_torreoro, "triana": s_triana, "archivo": s_archivo,
          "alcazar": s_alcazar, "triunfo": s_triunfo, "santacruz": s_santacruz, "colon": s_colon}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_sevilla_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos de Sevilla generados:", ", ".join(SCENES))
