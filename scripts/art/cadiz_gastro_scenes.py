#!/usr/bin/env python3
"""
Fondos de la ruta gastronómica de Cádiz. Reutiliza el mercado, la Plaza de Mina y San Juan de
Dios de «La ciudad que no cayó»; aquí van las escenas nuevas, con terrazas, puestos y tapas.

Uso: python3 scripts/art/cadiz_gastro_scenes.py && python3 scripts/art/render_layers.py cadiz_ && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, SHUT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, mirador, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)

FRY = "#E0A64E"


def parasol(x, top, w=70, c=CLAY):
    s = f'<path d="M{x} {top + 30}L{x} {top + 110}" stroke="#2E3A48" stroke-width="2.4"/>'
    s += f'<path d="M{x - w / 2} {top + 30}Q{x} {top - 4} {x + w / 2} {top + 30}Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
    for k in (-1, 0, 1):
        s += f'<path d="M{x} {top + 4}L{x + k * w / 4:.1f} {top + 30}" stroke="{PAPER}" stroke-width="2" opacity=".7"/>'
    s += "".join(f'<path d="M{x - w / 2 + i * w / 6:.1f} {top + 30}q{w / 12:.1f} 6 {w / 6:.1f} 0" fill="{c}" stroke="{INK}" stroke-width="1"/>' for i in range(6))
    return s


def table(x, base, dishes=("fish", "wine")):
    """Mesa de terraza con dos sillas y tapas."""
    s = f'<ellipse cx="{x}" cy="{base + 3}" rx="40" ry="5" fill="#5B3524" opacity=".18"/>'
    for dx in (-30, 30):
        s += f'<path d="M{x + dx - 8} {base}L{x + dx - 8} {base - 30}M{x + dx + 8} {base}L{x + dx + 8} {base - 14}M{x + dx - 9} {base - 14}H{x + dx + 9}" stroke="#2E3A48" stroke-width="2.4"/>'
    s += f'<path d="M{x} {base}L{x} {base - 26}" stroke="#2E3A48" stroke-width="3"/><path d="M{x - 10} {base}H{x + 10}" stroke="#2E3A48" stroke-width="3"/>'
    s += f'<ellipse cx="{x}" cy="{base - 28}" rx="24" ry="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    for i, d in enumerate(dishes):
        px = x - 10 + i * 18
        if d == "fish":
            s += f'<ellipse cx="{px}" cy="{base - 31}" rx="8" ry="3" fill="#FFF" stroke="{INK}" stroke-width="1"/><path d="M{px - 6} {base - 33}q6 -4 12 0" fill="{FRY}" stroke="{INK}" stroke-width=".8"/>'
        elif d == "wine":
            s += f'<path d="M{px - 2} {base - 44}H{px + 2}L{px + 1.5} {base - 38}Q{px} {base - 36} {px - 1.5} {base - 38}Z" fill="#F4E4A8" stroke="{INK}" stroke-width=".9"/><path d="M{px} {base - 36}V{base - 31}" stroke="{INK}" stroke-width=".9"/>'
        elif d == "tapa":
            s += f'<ellipse cx="{px}" cy="{base - 31}" rx="8" ry="3" fill="#FFF" stroke="{INK}" stroke-width="1"/><rect x="{px - 5}" y="{base - 36}" width="10" height="4" rx="1" fill="#C9885A" stroke="{INK}" stroke-width=".8"/>'
    return s


def garlands(y0, y1, n=6, seed=0):
    """Banderines de Carnaval cruzando la calle."""
    cols = [CLAY, GOLD, SEA, "#6E2C5E", PAPER]
    s = ""
    for k in range(3):
        ya = y0 + k * 28
        yb = y1 + k * 28
        s += f'<path d="M-10 {ya}Q195 {(ya + yb) / 2 + 40} 400 {yb}" fill="none" stroke="{INK}" stroke-width="1"/>'
        for i in range(14):
            t = (i + .5) / 14
            x = -10 + 410 * t
            y = (1 - t) ** 2 * ya + 2 * (1 - t) * t * ((ya + yb) / 2 + 40) + t * t * yb
            s += f'<path d="M{x - 6:.1f} {y:.1f}L{x + 6:.1f} {y:.1f}L{x:.1f} {y + 12:.1f}Z" fill="{cols[(i + k + seed) % 5]}" stroke="{INK}" stroke-width=".8"/>'
    return s


def church(x, top, w=120, h=200, towers=1, col=WHITE):
    c, cd, cl = col
    base = top + h
    s = f'<path d="M{x} {top + 40}L{x + w} {top + 40}L{x + w} {base}L{x} {base}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    s += f'<path d="M{x + w * .75} {top + 42}L{x + w} {top + 42}L{x + w} {base}L{x + w * .75} {base}Z" fill="{cd}" opacity=".6"/>'
    s += f'<path d="M{x - 4} {top + 40}L{x + w / 2} {top + 14}L{x + w + 4} {top + 40}Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
    s += f'<path d="M{x + w * .35} {base}L{x + w * .35} {base - 60}Q{x + w / 2} {base - 80} {x + w * .65} {base - 60}L{x + w * .65} {base}Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
    s += f'<path d="M{x + w * .3} {base}L{x + w * .3} {base - 90}L{x + w * .7} {base - 90}L{x + w * .7} {base}" fill="none" stroke="{STONE[1]}" stroke-width="4"/>'
    s += window(x + w * .44, top + 60, w * .12, 30, shutters=False, arch=True, sw=1.2, lit=True)
    tws = [x - 30] if towers == 1 else [x - 30, x + w]
    for tx in tws:
        tw = 30
        s += f'<path d="M{tx} {top - 10}L{tx + tw} {top - 10}L{tx + tw} {base}L{tx} {base}Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
        s += f'<path d="M{tx + 20} {top - 8}L{tx + tw} {top - 8}L{tx + tw} {base}L{tx + 20} {base}Z" fill="{cd}" opacity=".6"/>'
        s += window(tx + 9, top + 4, 12, 22, shutters=False, arch=True, sw=1.1)
        s += f'<path d="M{tx - 3} {top - 10}H{tx + tw + 3}V{top - 16}H{tx - 3}Z" fill="{cl}" stroke="{INK}" stroke-width="1.3"/>'
        s += f'<path d="M{tx + 3} {top - 16}Q{tx + tw / 2} {top - 44} {tx + tw - 3} {top - 16}Z" fill="#E8B84A" stroke="{INK}" stroke-width="1.4"/>'
        s += f'<path d="M{tx + tw / 2} {top - 38}V{top - 50}M{tx + tw / 2 - 4} {top - 45}H{tx + tw / 2 + 4}" stroke="{INK}" stroke-width="1.4"/>'
    return s


# ---------------------------------------------------------------------------
def flores():
    p = "gfl"; sun = (300, 110)
    far = f'<g id="far">{far_city(250, 61, towers=8)}</g>'
    # edificio de Correos (neomudéjar) y casas; puestos de flores y una freiduría
    correos = (f'<path d="M110 150L300 150L300 390L110 390Z" fill="#D9936A" stroke="{INK}" stroke-width="1.8"/>'
               f'<path d="M270 152L300 152L300 390L270 390Z" fill="#BF7A54" opacity=".7"/>'
               f'<path d="M106 150L304 150L304 140L106 140Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
               + "".join(f'<path d="M{x} {y + 44}L{x} {y + 14}Q{x + 11} {y} {x + 22} {y + 14}L{x + 22} {y + 44}Z" fill="{WIN if (x + y) % 3 else LIT}" stroke="{INK}" stroke-width="1.2"/>'
                         + f'<path d="M{x - 3} {y + 14}Q{x + 11} {y - 6} {x + 25} {y + 14}" fill="none" stroke="{STONE[2]}" stroke-width="3"/>' for x in (128, 170, 212, 254) for y in (170, 240))
               + f'<path d="M180 390L180 330Q205 310 230 330L230 390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
               + "".join(f'<path d="M{x} 140V128H{x + 10}V140" fill="#D9936A" stroke="{INK}" stroke-width="1.1"/>' for x in range(112, 296, 18)))
    side = house(-30, 190, 140, 200, YELLOW, floors=3, cols=3, lit={(1, 2)}) + house(300, 180, 110, 210, MINT, floors=3, cols=2, cierro=True)
    mid = f'<g id="mid">{side}{correos}<rect x="-10" y="386" width="{W + 20}" height="42" fill="#DCC3A0"/></g>'
    # puestos de flores
    stall = ""
    for x0 in (20, 250):
        stall += f'<path d="M{x0} 470L{x0 + 110} 470L{x0 + 104} 440L{x0 + 6} 440Z" fill="{SEA}" stroke="{INK}" stroke-width="1.6"/>'
        stall += f'<path d="M{x0 - 4} 400H{x0 + 114}L{x0 + 104} 386H{x0 + 6}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
        stall += f'<path d="M{x0 + 6} 400V440M{x0 + 104} 400V440" stroke="#2E3A48" stroke-width="2"/>'
        for i in range(8):
            bx = x0 + 10 + i * 12
            c = [CLAY, GOLD, "#E0766A", "#6E2C5E", PAPER][i % 5]
            stall += f'<path d="M{bx} 440L{bx + 2} 426H{bx + 8}L{bx + 10} 440Z" fill="#8FA6B3" stroke="{INK}" stroke-width=".8"/>'
            stall += "".join(f'<circle cx="{bx + 2 + k * 3}" cy="{422 - (k % 2) * 4}" r="3" fill="{c}" stroke="{INK}" stroke-width=".6"/>' for k in range(3))
            stall += f'<path d="M{bx + 5} 426V414" stroke="#4F8B5A" stroke-width="1.4"/>'
    near = (f'<g id="near">{floor(p, 420)}{stall}'
            + person(160, 440, .95, CLAY, dress=True) + person(186, 446, 1, "#34495E", hat=True)
            # cartucho en la mano
            + f'<path d="M190 426L198 426L194 436Z" fill="#E8D8B8" stroke="{INK}" stroke-width=".8"/>'
            + lamp(220, 540, 160) + "</g>")
    return doc(p, "Plaza de las Flores", [sky(p, sun, [(80, 60, .9)], [(210, 60), (230, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def vina():
    p = "gvi"; sun = (200, 90)
    far = f'<g id="far">{far_city(260, 63, towers=4)}</g>'
    iglesia = church(160, 160, 90, 180, towers=1, col=STONE)

    def row(left):
        s = ""
        cols = [PINK, WHITE, YELLOW, MINT]
        for k in range(4):
            x0 = -20 + k * 38 if left else W + 20 - k * 38
            x1 = x0 + (46 if left else -46)
            top0, top1 = 180 + k * 22, 192 + k * 22
            bot = 440 - k * 16
            xa, xb = (x0, x1) if left else (x1, x0)
            ta, tb = (top0, top1) if left else (top1, top0)
            c = cols[(k + (0 if left else 2)) % 4]
            s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot - 8}L{xa} {bot}Z" fill="{c[0]}" stroke="{INK}" stroke-width="1.5"/>'
            for fl in range(2):
                y = ta + 30 + fl * 90
                s += f'<path d="M{xa + 10} {y}L{xb - 10} {y + 3}L{xb - 10} {y + 44}L{xa + 10} {y + 41}Z" fill="{SHUT if fl == 0 else WIN}" stroke="{INK}" stroke-width="1.1"/>'
                s += f'<path d="M{xa + 6} {y + 44}L{xb - 6} {y + 47}" stroke="{INK}" stroke-width="2"/>'
        return s
    mid = f'<g id="mid">{iglesia}{row(True)}{row(False)}<rect x="-10" y="400" width="{W + 20}" height="28" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E0C7A4")}'
            + table(80, 520, ("fish", "wine")) + table(310, 526, ("tapa", "wine"))
            + person(170, 440, .9, "#6E2C5E", dress=True) + person(220, 444, .95, CLAY)
            + "</g>")
    # los banderines y el confeti van en la capa fija, por encima de todo lo lejano
    confetti = "".join(f'<rect x="{(i * 53) % 390}" y="{(i * 97) % 380 + 20}" width="4" height="4" transform="rotate({i * 37} {(i * 53) % 390} {(i * 97) % 380 + 20})" fill="{[CLAY, GOLD, SEA, "#6E2C5E"][i % 4]}" opacity=".8"/>' for i in range(40))
    fxg = fx(p, sun, 420).replace('<g id="fx">', f'<g id="fx">{garlands(120, 150)}{confetti}')
    return doc(p, "Barrio de La Viña", [sky(p, sun, [(60, 60, .8), (330, 80, .6)], []), far, mid, near, fxg])


def plaza_terraces(p, sun, title, center, seed, trees=True):
    far = f'<g id="far">{far_city(250, seed, towers=6)}</g>'
    side = house(-30, 200, 120, 190, PINK, floors=3, cols=2, lit={(0, 1)}) + house(300, 190, 120, 200, YELLOW, floors=3, cols=2, cierro=True)
    t = (tree(60, 400, 48, "#4B7C58", "#3A6446") + tree(330, 400, 50, "#4B7C58", "#3A6446")) if trees else ""
    mid = f'<g id="mid">{side}{center}{t}<rect x="-10" y="392" width="{W + 20}" height="36" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + parasol(70, 400, 90, CLAY) + table(70, 520, ("fish", "wine"))
            + parasol(320, 404, 90, SEA) + table(320, 526, ("tapa", "wine"))
            + person(180, 442, .95, SEA) + person(210, 446, 1, CLAY, dress=True)
            + "</g>")
    return doc(p, title, [sky(p, sun, [(80, 60, .8)], [(220, 60), (240, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def mentidero():
    center = house(110, 200, 170, 190, WHITE, floors=3, cols=3, lit={(0, 1)}) + mirador(170, 172, 30, 30, WHITE)
    return plaza_terraces("gme", (300, 100), "Plaza del Mentidero", center, 65)


def sanfrancisco():
    center = church(150, 150, 120, 240, towers=1, col=WHITE)
    return plaza_terraces("gsf", (80, 100), "Plaza de San Francisco", center, 67)


def sanantonio():
    center = church(140, 150, 110, 240, towers=2, col=WHITE)
    return plaza_terraces("gsa", (320, 100), "Plaza de San Antonio", center, 69, trees=False)


def ancha():
    p = "gan"; sun = (200, 80)
    far = f'<g id="far">{far_city(240, 71, towers=6)}</g>'

    def side(left):
        s = ""
        cols = [WHITE, YELLOW, PINK]
        for k in range(3):
            x0 = -40 + k * 50 if left else W + 40 - k * 50
            x1 = x0 + (60 if left else -60)
            top0, top1 = 90 + k * 36, 110 + k * 38
            bot = 470 - k * 30
            xa, xb = (x0, x1) if left else (x1, x0)
            ta, tb = (top0, top1) if left else (top1, top0)
            c = cols[(k + (0 if left else 1)) % 3]
            s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot - 10}L{xa} {bot}Z" fill="{c[0]}" stroke="{INK}" stroke-width="1.6"/>'
            for fl in range(2):
                y = ta + 40 + fl * 100
                # cierros acristalados verdes
                s += f'<path d="M{xa + 8} {y}L{xb - 8} {y + 4}L{xb - 8} {y + 60}L{xa + 8} {y + 56}Z" fill="{SHUT}" stroke="{INK}" stroke-width="1.3"/>'
                s += f'<path d="M{xa + 13} {y + 6}L{xb - 13} {y + 9}L{xb - 13} {y + 52}L{xa + 13} {y + 49}Z" fill="#9BBFC0" stroke="{INK}" stroke-width=".8"/>'
                s += f'<path d="M{(xa + xb) / 2:.1f} {y + 7}V{y + 51}" stroke="{INK}" stroke-width=".8"/>'
        return s
    # escaparate de pastelería a la izquierda, con el pan de Cádiz
    shop = (f'<path d="M20 330L130 342L130 440L20 440Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M28 346L122 356L122 420L28 420Z" fill="#F6EBD2" stroke="{INK}" stroke-width="1.2"/>'
            f'<path d="M24 330L134 342L134 334L24 322Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"/>'
            + "".join(f'<path d="M{x} {y}h22v-8q-11 -6 -22 0Z" fill="#F2DCA8" stroke="{INK}" stroke-width="1"/><path d="M{x} {y - 8}q11 -6 22 0v2q-11 -6 -22 0Z" fill="#C98E4A"/>' for x, y in [(36, 380), (70, 384), (48, 410), (84, 412)])
            + f'<path d="M28 392L122 400M28 420L122 424" stroke="{INK}" stroke-width="1"/>')
    mid = f'<g id="mid">{side(True)}{side(False)}{shop}<rect x="-10" y="436" width="{W + 20}" height="0" fill="none"/></g>'
    near = (f'<g id="near">{floor(p, 430, color="#E4CDA8")}'
            + person(190, 452, .95, SEA) + person(230, 448, .9, CLAY, dress=True) + person(150, 458, 1, "#34495E", hat=True)
            + lamp(340, 550, 180) + "</g>")
    return doc(p, "Calle Ancha", [sky(p, sun, [(70, 50, .8)], [(260, 40), (280, 30, .8)]), far, mid, near, fx(p, sun, 430)])


SCENES = {"flores": flores, "vina": vina, "mentidero": mentidero, "sanfrancisco": sanfrancisco, "sanantonio": sanantonio, "ancha": ancha}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_cadiz_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos gastronómicos de Cádiz generados:", ", ".join(SCENES))
