#!/usr/bin/env python3
"""
Fondos nuevos de las rutas gastronómicas de Málaga (Muelle Uno, la Malagueta), Sevilla (Mercado de
Triana, plaza del Salvador) y Granada (Mercado de San Agustín, Bib-Rambla, Alcaicería). El resto de
paradas reutiliza los fondos de las rutas de historia.

Uso: python3 scripts/art/gastro_andalucia_scenes.py && python3 scripts/art/render_layers.py malaga_ (etc.) && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import (INK, CLAY, SEA, GOLD, PAPER, WIN, LIT, W, H, WHITE, YELLOW, PINK, MINT, STONE, OUT,
                          f, sky, window, house, palm, lamp, person, floor, bench, tree, columns, far_city, fx, doc)
from granada_scenes import horseshoe, sierra, alhambra_hill, cypress
from sevilla_scenes import giralda, river, orange_tree
from cordoba_scenes import statue, ground, battlements, lime_wall
from huelva_scenes import boat

SAND = "#E9D2A6"


def lighthouse(x, base, s=1.0, soft=False):
    """La Farola de Málaga: faro blanco con linterna."""
    sw = 0 if soft else 1.4
    return (f'<path d="M{f(x - 12 * s)} {f(base)}L{f(x - 8 * s)} {f(base - 90 * s)}H{f(x + 8 * s)}L{f(x + 12 * s)} {f(base)}Z" fill="{WHITE[2]}" stroke="{INK if not soft else WHITE[1]}" stroke-width="{sw}"/>'
            f'<path d="M{f(x - 11 * s)} {f(base - 90 * s)}H{f(x + 11 * s)}V{f(base - 96 * s)}H{f(x - 11 * s)}Z" fill="{WHITE[1]}"/>'
            f'<path d="M{f(x - 6 * s)} {f(base - 96 * s)}V{f(base - 110 * s)}H{f(x + 6 * s)}V{f(base - 96 * s)}Z" fill="#FFE7A8" stroke="{INK if not soft else WHITE[1]}" stroke-width="{sw}"/>'
            f'<path d="M{f(x - 8 * s)} {f(base - 110 * s)}L{f(x)} {f(base - 118 * s)}L{f(x + 8 * s)} {f(base - 110 * s)}Z" fill="#2E3A48"/>')


def espeto_boat(x, y, s=1.0):
    """Barca varada en la arena, llena de brasas, con espetos clavados."""
    out = (f'<path d="M{f(x - 60 * s)} {f(y - 16 * s)}Q{x} {f(y + 10 * s)} {f(x + 60 * s)} {f(y - 16 * s)}L{f(x + 48 * s)} {f(y + 4 * s)}Q{x} {f(y + 22 * s)} {f(x - 48 * s)} {f(y + 4 * s)}Z" fill="#2F6F9E" stroke="{INK}" stroke-width="2"/>'
           f'<path d="M{f(x - 56 * s)} {f(y - 14 * s)}Q{x} {f(y + 8 * s)} {f(x + 56 * s)} {f(y - 14 * s)}" fill="none" stroke="{PAPER}" stroke-width="2"/>')
    out += "".join(f'<circle cx="{f(x + dx * s)}" cy="{f(y - 8 * s)}" r="{f(4 * s)}" fill="{c}"/>' for dx, c in [(-36, "#E8744A"), (-20, GOLD), (-4, "#E8744A"), (12, GOLD), (28, "#E8744A")])
    for k in range(5):
        bx = x - 44 * s + k * 20 * s
        out += f'<path d="M{f(bx)} {f(y - 6 * s)}L{f(bx + 12 * s)} {f(y - 56 * s)}" stroke="#C9A96A" stroke-width="{f(2.4 * s)}"/>'
        out += "".join(f'<ellipse cx="{f(bx + (4 + j * 3) * s)}" cy="{f(y - (22 + j * 12) * s)}" rx="{f(7 * s)}" ry="{f(2.6 * s)}" transform="rotate(-76 {f(bx + (4 + j * 3) * s)} {f(y - (22 + j * 12) * s)})" fill="#8FA3AE" stroke="{INK}" stroke-width=".8"/>' for j in range(3))
    out += "".join(f'<path d="M{f(x + dx * s)} {f(y - 30 * s)}q-6 -14 2 -26" fill="none" stroke="#DDD" stroke-width="3" opacity=".6"/>' for dx in (-30, 10, 40))
    return out


def market_hall(x0, x1, top, base, wall, roof, sign_c=CLAY):
    s = (f'<path d="M{x0} {base}V{top}H{x1}V{base}Z" fill="{wall}" stroke="{INK}" stroke-width="1.8"/>'
         f'<path d="M{x0 - 10} {top}L{(x0 + x1) / 2} {top - 40}L{x1 + 10} {top}Z" fill="{roof}" stroke="{INK}" stroke-width="1.8"/>'
         + "".join(f'<path d="M{x} {base}V{top + 50}H{x + 40}V{base}Z" fill="#9BBFC0" stroke="{INK}" stroke-width="1.4"/>' for x in range(int(x0) + 20, int(x1) - 40, 62))
         + f'<path d="M{(x0 + x1) / 2 - 80} {top + 14}H{(x0 + x1) / 2 + 80}V{top + 30}H{(x0 + x1) / 2 - 80}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
         + "".join(f'<path d="M{(x0 + x1) / 2 - 70 + k * 16} {top + 22}h8" stroke="{sign_c}" stroke-width="3"/>' for k in range(9)))
    return s


def stalls(colors, fruits):
    out = ""
    for x, c in zip((10, 290), colors):
        out += (f'<path d="M{x} 480V446H{x + 90}V480" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{x - 6} 446L{x + 45} 424L{x + 96} 446Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
                + "".join(f'<circle cx="{x + 14 + k * 16}" cy="440" r="6" fill="{fc}" stroke="{INK}" stroke-width=".8"/>' for k, fc in enumerate(fruits)))
    return out


# ---------------------------------------------------------------------------
def malaga_muelle():
    p = "mmu"; sun = (300, 110)
    far = (f'<g id="far">{far_city(290, 181, "#EBD0B4", "#F0DAC4", towers=2)}{lighthouse(330, 300, .9, soft=True)}'
           f'<path d="M-10 300Q60 240 130 250T260 260L260 300Z" fill="#C9B79A"/></g>')
    sea = f'<g id="sea">{river(p, 300, 400)}{boat(120, 340, .9, SEA)}{boat(260, 350, 1.1, CLAY)}</g>'
    # pérgola ondulada del paseo y un cubo de colores al fondo
    perg = (f'<path d="M-10 390H400V400H-10Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.4"/>'
            + f'<path d="M-10 250Q50 230 100 250T200 250T300 250T410 250V262Q350 244 300 262T200 262T100 262T-10 262Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x} 262V400" stroke="{INK}" stroke-width="4"/><path d="M{x} 262V400" stroke="{WHITE[1]}" stroke-width="2"/>' for x in range(20, 400, 60))
            + f'<path d="M150 390V330H210V390Z" fill="#E8B83A" fill-opacity=".85" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{150 + k * 15} 330V390" stroke="{c}" stroke-width="6" opacity=".7"/>' for k, c in enumerate(["#D8412F", "#2F9EB0", "#4F8B5A", "#6E2C5E"])))
    mid = f'<g id="mid">{perg}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E3D5BE", line="#CFBFA2")}'
            + palm(40, 520, 260, 10, 1.05) + palm(350, 520, 250, -10, 1.05)
            + person(170, 458, 1.05, SEA) + person(200, 462, 1, CLAY, dress=True) + person(260, 454, .95, "#6E2C5E", dress=True) + "</g>")
    return doc(p, "Muelle Uno", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, sea, mid, near, fx(p, sun, 420, .3)])


def malaga_malagueta():
    p = "mml"; sun = (310, 120)
    far = f'<g id="far">{far_city(270, 183, "#EBD0B4", "#F0DAC4", towers=1)}{lighthouse(60, 290, .8, soft=True)}</g>'
    sea = f'<g id="sea">{river(p, 280, 390)}{boat(250, 320, .7, "#E8B83A")}</g>'
    beach = (f'<path d="M-10 380Q200 366 400 384V428H-10Z" fill="{SAND}"/>'
             + "".join(f'<path d="M{x} 386q12 -6 24 0" fill="none" stroke="#FFF" stroke-width="2" opacity=".7"/>' for x in (20, 120, 240, 330)))
    mid = f'<g id="mid">{beach}</g>'
    parasols = "".join(f'<path d="M{x} 470V420" stroke="{INK}" stroke-width="2"/><path d="M{x - 30} 424Q{x} 396 {x + 30} 424Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>' for x, c in [(40, CLAY), (350, SEA)])
    near = (f'<g id="near"><path d="M-10 420H400V570H-10Z" fill="{SAND}"/>'
            + "".join(f'<circle cx="{(i * 41) % 390}" cy="{430 + (i * 67) % 130}" r="1.4" fill="#C9AE7E"/>' for i in range(60))
            + espeto_boat(195, 500, 1.3) + parasols
            + person(90, 470, 1.05, SEA) + person(300, 474, 1, CLAY, dress=True) + "</g>")
    return doc(p, "Playa de la Malagueta", [sky(p, sun, [(80, 70, .8)], [(180, 60), (200, 50, .8)]), far, sea, mid, near, fx(p, sun, 420, .3)])


def sevilla_mercado():
    p = "smt"; sun = (90, 110)
    far = f'<g id="far">{far_city(260, 185, towers=2)}{giralda(330, 300, 40, 24, soft=True)}</g>'
    hall = market_hall(30, 360, 200, 390, "#EFDCB8", "#B5553A")
    ruins = "".join(f'<path d="M{x} 390V{y}H{x + 20}V390Z" fill="#C9A77E" stroke="{INK}" stroke-width="1.2"/>' for x, y in [(0, 330), (360, 320)])
    mid = f'<g id="mid">{hall}{ruins}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E0D3BC", line="#CDBE9E")}{stalls((CLAY, SEA), ["#F29A2E", "#7C8A4A", "#D8412F", "#F29A2E", "#7C8A4A"])}'
            + person(170, 452, 1, SEA) + person(196, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Mercado de Triana", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def sevilla_salvador():
    p = "ssv"; sun = (300, 100)
    far = f'<g id="far">{far_city(250, 187, towers=3)}</g>'
    c, cd, cl = ("#E8B7A0", "#CF9A82", "#F4D0BF")
    church = (f'<path d="M70 390V170H320V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M60 170H330V156H60Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.6"/>'
              + f'<path d="M150 156Q195 90 240 156Z" fill="{cl}" stroke="{INK}" stroke-width="1.6"/><path d="M195 102V84M189 90H201" stroke="{INK}" stroke-width="1.6"/>'
              + "".join(f'<path d="M{x} 390V220H{x + 16}V390Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.2"/>' for x in (100, 150, 224, 274))
              + "".join(f'<path d="M{x} 390V300Q{x + 17} 280 {x + 34} 300V390Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>' for x in (116, 178, 240))
              + "".join(window(x, 200, 16, 30, shutters=False, arch=True, sw=1.1) for x in (124, 187, 250))
              + f'<path d="M300 390V110H340V390Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/><path d="M296 110H344V100H296Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.4"/>'
              + f'<path d="M304 100Q320 70 336 100Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>' + window(312, 130, 16, 30, shutters=False, arch=True, sw=1.1))
    side = house(-30, 210, 110, 180, YELLOW, floors=3, cols=2, cierro=True) + house(340, 220, 80, 170, WHITE, floors=3, cols=1)
    mid = f'<g id="mid">{side}{church}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + orange_tree(40, 480, 30) + orange_tree(350, 480, 30)
            + "".join(person(x, 452 + (x % 3) * 3, .95, c, dress=d) for x, c, d in [(120, SEA, False), (140, CLAY, True), (200, "#6E2C5E", True), (220, "#34495E", False), (270, SEA, True)])
            + "</g>")
    return doc(p, "Plaza del Salvador", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_sanagustin():
    p = "gsa"; sun = (80, 110)
    far = f'<g id="far">{sierra(260)}{far_city(270, 189, "#EBCFB4", "#F0DAC4", towers=2)}</g>'
    hall = market_hall(30, 360, 200, 390, "#E9D8B4", SEA, sign_c=SEA)
    mid = f'<g id="mid">{hall}{ground(386)}</g>'
    near = (f'<g id="near">{floor(p, 420, color="#E0D3BC", line="#CDBE9E")}{stalls(("#6E2C5E", CLAY), ["#D98A2E", "#B8412A", "#C9B23A", "#4F8B5A", "#D98A2E"])}'
            + person(170, 452, 1, SEA) + person(196, 456, .95, CLAY, dress=True) + "</g>")
    return doc(p, "Mercado de San Agustín", [sky(p, sun, [(300, 70, .8)], [(240, 50), (260, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_bibrambla():
    p = "gbr"; sun = (300, 110)
    far = f'<g id="far">{sierra(250)}{far_city(270, 191, "#EBCFB4", "#F0DAC4", towers=3)}</g>'
    houses = (house(-30, 180, 140, 210, PINK, floors=3, cols=2, cierro=True) + house(110, 170, 170, 220, YELLOW, floors=4, cols=3, lit={(1, 1)})
              + house(280, 190, 140, 200, MINT, floors=3, cols=2))
    mid = f'<g id="mid">{houses}{ground(386)}</g>'
    # fuente de los Gigantones y puestos de flores
    fountain = (f'<ellipse cx="195" cy="500" rx="70" ry="16" fill="#8FB9B4" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M180 500V440H210V500Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
                + "".join(f'<path d="M{x - 7} 470L{x - 5} 444H{x + 5}L{x + 7} 470Z" fill="#9A9488" stroke="{INK}" stroke-width="1.2"/><circle cx="{x}" cy="438" r="6" fill="#9A9488" stroke="{INK}" stroke-width="1.2"/>' for x in (172, 218))
                + f'<ellipse cx="195" cy="430" rx="34" ry="8" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M195 424Q176 412 166 440M195 424Q214 412 224 440" fill="none" stroke="#E6F2EF" stroke-width="2"/>')
    kiosks = "".join(f'<path d="M{x} 480V450H{x + 60}V480" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 6} 450L{x + 30} 432L{x + 66} 450Z" fill="#4F8B5A" stroke="{INK}" stroke-width="1.4"/>'
                     + "".join(f'<circle cx="{x + 8 + k * 11}" cy="446" r="5" fill="{fc}"/>' for k, fc in enumerate([CLAY, "#E86A92", GOLD, "#D8412F", "#E86A92"])) for x in (10, 320))
    near = f'<g id="near">{floor(p, 420, color="#E3D5BE", line="#CFBFA2")}{kiosks}{fountain}' + person(110, 458, 1, SEA) + person(290, 460, .95, CLAY, dress=True) + "</g>"
    return doc(p, "Plaza de Bib-Rambla", [sky(p, sun, [(80, 70, .8)], [(200, 50), (220, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def granada_alcaiceria():
    p = "gal"; sun = (195, 70)
    far = f'<g id="far">{sierra(240)}</g>'
    c, cd, cl = ("#F4EEE2", "#DCD2BF", "#FFFDF6")
    lane = (f'<path d="M-20 120L150 240L150 420L-20 560Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M410 120L240 240L240 420L410 560Z" fill="{cd}" stroke="{INK}" stroke-width="1.8"/>'
            + f'<path d="M150 240H240V250H150Z" fill="{cl}" stroke="{INK}" stroke-width="1.2"/>'
            + horseshoe(165, 260, 60, 120, "#6E5140", 1.6))
    shops = ""
    for side in (-1, 1):
        for k in range(3):
            t = (k + .5) / 3.4
            x = -20 + t * 170 if side < 0 else 410 - t * 170
            top = 150 + t * 100
            h = 170 - t * 60
            w = 60 - t * 26
            x0 = x if side < 0 else x - w
            shops += (f'<path d="M{f(x0)} {f(top + h)}V{f(top + 30)}Q{f(x0 + w / 2)} {f(top)} {f(x0 + w)} {f(top + 30)}V{f(top + h)}Z" fill="#6E5140" stroke="{INK}" stroke-width="1.2"/>'
                      + "".join(f'<path d="M{f(x0 + 4 + j * (w - 8) / 3)} {f(top + 34)}V{f(top + h - 10)}" stroke="{col}" stroke-width="{f(5 - t * 3)}"/>' for j, col in enumerate(["#C0476A", GOLD, SEA, "#6E2C5E"])))
    lanterns = "".join(f'<path d="M{x} {y}V{y + 10}" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 6} {y + 10}H{x + 6}L{x + 4} {y + 24}H{x - 4}Z" fill="#E8B83A" stroke="{INK}" stroke-width="1.2"/>' for x, y in [(120, 190), (270, 190), (80, 150), (310, 150)])
    mid = f'<g id="mid">{lane}{shops}{lanterns}<path d="M150 420H240V428H150Z" fill="#D5C29E"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#D5C29E", line="#C1AB85")}'
            + person(180, 452, .85, SEA) + person(210, 456, .9, CLAY, dress=True) + "</g>")
    return doc(p, "Alcaicería", [sky(p, sun, [(80, 60, .7), (320, 80, .6)], []), far, mid, near, fx(p, sun, 420, .2)])


SCENES = {"malaga_muelle": malaga_muelle, "malaga_malagueta": malaga_malagueta,
          "sevilla_mercado": sevilla_mercado, "sevilla_salvador": sevilla_salvador,
          "granada_sanagustin": granada_sanagustin, "granada_bibrambla": granada_bibrambla, "granada_alcaiceria": granada_alcaiceria}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or list(SCENES)
    for key in keys:
        with open(os.path.join(OUT, f"fondo_{key}.svg"), "w") as fh:
            fh.write(SCENES[key]())
    print("fondos gastronómicos generados:", ", ".join(keys))
