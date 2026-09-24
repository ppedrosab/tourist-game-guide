#!/usr/bin/env python3
"""
Sprites de Granada: Washington Irving, el León de la fuente y Boabdil.

Uso: python3 scripts/art/granada_sprites.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import (INK, CLAY, CLAYD, SEA, SEAD, GOLD, GOLDD, PAPER, SHADOW, face_of, g, limb, svg, write)

# ---------------------------------------------------------------------------
# Washington Irving (1829): levita oscura, chaleco, pañuelo al cuello, chistera y cuaderno
# ---------------------------------------------------------------------------
SK = "#EDC19C"; SKD = "#CF9D78"; COAT = "#2F3E5C"; COATD = "#22304A"; HAIR = "#4A3222"


def irving():
    legs = g("legs",
             f'<path d="M84 200L116 200L116 240L104 240L100 214L96 240L84 240Z" fill="#8A7A62" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M100 202L116 202L116 240L105 240Z" fill="#6E614D"/>',
             f'<path d="M78 248Q80 240 92 240Q98 241 98 248Z" fill="#1E1D25" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M102 248Q102 241 108 240Q120 240 122 248Z" fill="#1E1D25" stroke="{INK}" stroke-width="2.4"/>')
    coat = g("coat",
             # faldones de la levita por detrás
             f'<path d="M70 150L64 222L84 218L86 160Z" fill="{COAT}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M130 150L136 222L116 218L114 160Z" fill="{COATD}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M74 118Q100 106 126 118L130 204L70 204Z" fill="{COAT}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q118 112 126 118L130 204L110 204Z" fill="{COATD}"/>',
             # chaleco y camisa
             f'<path d="M88 116L112 116L110 178L100 186L90 178Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
             *[f'<circle cx="100" cy="{y}" r="1.8" fill="{INK}"/>' for y in (140, 152, 164)],
             f'<path d="M88 112L100 136L112 112Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>',
             # pañuelo al cuello
             f'<path d="M86 112Q100 122 114 112L112 120Q100 128 88 120Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M96 120L100 132L104 120Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>',
             # solapas
             f'<path d="M84 116L92 150L80 140Z" fill="{COATD}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M116 116L108 150L120 140Z" fill="#1A2640" stroke="{INK}" stroke-width="1.8"/>')
    arms = g("arms",
             limb("M76 124Q60 132 52 148", COAT, 12),
             limb("M124 124Q140 132 150 146", COAT, 12),
             # cuaderno abierto en la mano izquierda
             f'<path d="M30 146L54 140L58 166L34 172Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M54 140L74 146L72 172L58 166Z" fill="#F1E6D0" stroke="{INK}" stroke-width="2"/>',
             *[f'<path d="M36 {150 + k * 5}L52 {146 + k * 5}M60 {150 + k * 5}L70 {153 + k * 5}" stroke="#9AA3AA" stroke-width="1"/>' for k in range(3)],
             f'<circle cx="52" cy="150" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="150" cy="148" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M150 144L166 108Q172 102 170 114Q162 134 152 146Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>')
    head = g("head",
             f'<path d="M90 96L90 112L110 112L110 96Z" fill="{SK}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{SK}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{SKD}" opacity=".5"/>',
             # pelo ondulado y patillas
             f'<path d="M60 76Q56 40 100 36Q144 40 140 76L134 76Q132 58 124 52Q112 60 96 56Q80 58 68 66L66 76Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M62 70L64 94M138 70L136 94" stroke="{HAIR}" stroke-width="6"/>',
             f'<path d="M78 48Q88 42 98 44" fill="none" stroke="#6B5343" stroke-width="2.2"/>',
             # chistera
             f'<path d="M66 44Q100 36 134 44L134 50Q100 42 66 50Z" fill="#1E1D25" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M76 44L78 6L122 6L124 44Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M106 7L122 7L124 44L110 44Z" fill="#1E1D25"/>',
             f'<path d="M77 34L123 34L123 40L77 40Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M84 12Q86 22 84 30" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    rim = g("rim", f'<path d="M72 126L68 200" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')
    return lambda e: svg(e, [SHADOW, legs, coat, arms, head, face_of(e).replace("#5A3A22", "#4A3A2A"), rim])


# ---------------------------------------------------------------------------
# El León: de mármol, sentado de frente, melena en rizos y un chorrito de agua
# ---------------------------------------------------------------------------
MB = "#EEE6D6"; MBD = "#CFC3AC"; MBL = "#FBF7EE"; MANE = "#DCCFB6"; MANED = "#B9AA8E"


def leon():
    body = g("body",
             # lomo y patas traseras
             f'<path d="M58 238Q44 186 66 130Q100 112 134 130Q156 186 142 238Z" fill="{MB}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M112 126Q142 140 148 196Q146 224 142 238L118 238Q130 190 112 126Z" fill="{MBD}" opacity=".7"/>',
             # cola
             f'<path d="M142 214Q170 208 166 184Q164 172 172 168" fill="none" stroke="{INK}" stroke-width="6"/>',
             f'<path d="M142 214Q170 208 166 184Q164 172 172 168" fill="none" stroke="{MB}" stroke-width="3"/>',
             f'<circle cx="173" cy="166" r="6" fill="{MANE}" stroke="{INK}" stroke-width="2"/>',
             # patas delanteras
             f'<path d="M78 150L76 238L94 238L96 156Z" fill="{MBL}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M122 150L124 238L106 238L104 156Z" fill="{MB}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M72 248Q72 236 86 236Q98 236 98 248Z" fill="{MBL}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M102 248Q102 236 114 236Q128 236 128 248Z" fill="{MB}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M80 242V248M86 242V248M92 242V248M108 242V248M114 242V248M120 242V248" stroke="{INK}" stroke-width="1.4"/>',
             # vetas del mármol
             f'<path d="M66 196Q74 190 70 180M132 204Q126 196 130 188" fill="none" stroke="{MBD}" stroke-width="1.4"/>')
    mane = g("mane",
             *[f'<circle cx="{100 + math.cos(math.radians(a)) * 48:.1f}" cy="{80 + math.sin(math.radians(a)) * 46:.1f}" r="15" fill="{MANE if a % 60 else MANED}" stroke="{INK}" stroke-width="2.4"/>'
               for a in range(0, 360, 30)],
             f'<circle cx="100" cy="80" r="50" fill="{MANE}"/>',
             *[f'<path d="M{100 + math.cos(math.radians(a)) * 44:.1f} {80 + math.sin(math.radians(a)) * 42:.1f}q4 -4 8 0" fill="none" stroke="{MANED}" stroke-width="2"/>' for a in range(15, 360, 30)])
    head = g("head",
             f'<path d="M64 60Q60 30 76 30Q84 30 86 42Z" fill="{MB}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M136 60Q140 30 124 30Q116 30 114 42Z" fill="{MB}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M62 76Q60 40 100 38Q140 40 138 76Q140 110 100 114Q60 110 62 76Z" fill="{MB}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M120 44Q140 54 138 76Q138 106 112 112Q128 94 126 70Q124 52 120 44Z" fill="{MBD}" opacity=".55"/>',
             # hocico
             f'<path d="M86 86Q100 80 114 86Q114 96 100 98Q86 96 86 86Z" fill="{MBL}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M95 84L105 84L100 90Z" fill="#8A6A5A" stroke="{INK}" stroke-width="1.4"/>',
             *[f'<circle cx="{x}" cy="{y}" r="1" fill="{MANED}"/>' for x, y in [(90, 90), (92, 94), (108, 90), (110, 94)]],
             f'<ellipse cx="80" cy="60" rx="8" ry="3.5" fill="#FFF" opacity=".5"/>')
    # la cara del Cenachero, un poco más arriba y con la boca bajo el hocico
    face = lambda e: face_of(e).replace('<g id="face">', '<g id="face" transform="translate(0 -4)">').replace("#5A3A22", "#8A6A3A")
    water = g("water",
              f'<path d="M114 100Q146 94 160 122" fill="none" stroke="#8FB9B4" stroke-width="4" opacity=".85"/>',
              f'<circle cx="162" cy="130" r="3" fill="#8FB9B4" stroke="{INK}" stroke-width="1"/><circle cx="166" cy="140" r="2" fill="#8FB9B4" stroke="{INK}" stroke-width="1"/>')
    rim = g("rim",
            f'<path d="M66 176Q60 200 64 230" fill="none" stroke="#FFF" stroke-width="2.4" opacity=".7"/>',
            f'<path d="M70 58Q76 46 90 42" fill="none" stroke="#FFF" stroke-width="2.2" opacity=".6"/>')
    return lambda e: svg(e, [SHADOW, body, mane, head, face(e), water, rim])


# ---------------------------------------------------------------------------
# Boabdil: turbante blanco y oro, túnica roja nazarí, capa blanca y la gran llave de la ciudad
# ---------------------------------------------------------------------------
BS = "#D9A27A"; BSD = "#B98260"; RED = "#9E2F2A"; REDD = "#7E2420"; BEARD = "#2A1E1A"


def boabdil():
    legs = g("legs",
             limb("M90 214L89 240", "#5A4632", 9), limb("M110 214L111 240", "#5A4632", 9),
             f'<path d="M76 248Q78 238 92 240Q100 242 96 248Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 248Q100 242 108 240Q122 238 124 248Z" fill="{GOLDD}" stroke="{INK}" stroke-width="2.4"/>')
    cape = g("cape",
             f'<path d="M66 122Q100 104 134 122L146 228L54 228Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M110 110Q128 114 134 122L146 228L124 228Z" fill="#E6DCC6"/>')
    robe = g("robe",
             f'<path d="M78 118Q100 108 122 118L128 220L72 220Z" fill="{RED}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q116 112 122 118L128 220L110 220Z" fill="{REDD}"/>',
             f'<path d="M100 116L100 220" stroke="{GOLD}" stroke-width="3"/>',
             *[f'<path d="M{97} {y}l3 -3l3 3l-3 3Z" fill="{GOLDD}"/>' for y in range(132, 214, 14)],
             f'<path d="M74 164L126 164L127 174L73 174Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
             # espada envainada
             f'<path d="M122 172Q136 196 132 220" fill="none" stroke="{INK}" stroke-width="7"/><path d="M122 172Q136 196 132 220" fill="none" stroke="{GOLDD}" stroke-width="3.6"/>',
             f'<path d="M116 170L128 170" stroke="{INK}" stroke-width="4"/>')
    arms = g("arms",
             limb("M78 124Q60 132 54 148", RED, 12),
             limb("M122 124Q140 130 150 144", RED, 12),
             # la llave de Granada
             f'<path d="M152 150L176 96" stroke="{INK}" stroke-width="8"/><path d="M152 150L176 96" stroke="{GOLD}" stroke-width="4.4"/>',
             f'<circle cx="179" cy="88" r="9" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="179" cy="88" r="9" fill="none" stroke="{GOLD}" stroke-width="3.6"/>',
             f'<path d="M158 138L168 142L166 148L156 144Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>',
             f'<circle cx="54" cy="150" r="6" fill="{BS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="152" cy="148" r="6" fill="{BS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{BS}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{BS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{BS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{BS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{BSD}" opacity=".5"/>',
             # barba corta y cuidada, bajo la boca
             f'<path d="M64 82Q62 112 100 120Q138 112 136 82Q132 98 122 104Q112 110 100 110Q88 110 78 104Q68 98 64 82Z" fill="{BEARD}" stroke="{INK}" stroke-width="2.2"/>',
             # turbante
             f'<path d="M58 62Q54 20 100 16Q146 20 142 62Q126 52 100 52Q74 52 58 62Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M100 16Q140 22 142 62Q130 54 116 52Q118 30 100 16Z" fill="#E6DCC6"/>',
             *[f'<path d="M{62 + k * 3} {56 - k * 8}Q100 {44 - k * 9} {138 - k * 3} {56 - k * 8}" fill="none" stroke="#D8CBB3" stroke-width="1.8"/>' for k in range(1, 4)],
             f'<path d="M58 62Q100 50 142 62L142 68Q100 56 58 68Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
             f'<circle cx="100" cy="44" r="6" fill="{RED}" stroke="{GOLD}" stroke-width="2.4"/>',
             f'<path d="M100 38L102 24Q106 20 104 30Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>',
             f'<ellipse cx="78" cy="70" rx="7" ry="3.2" fill="#FFF" opacity=".2"/>')
    rim = g("rim", f'<path d="M58 130L56 222" fill="none" stroke="#FFF" stroke-width="2" opacity=".5"/>')
    return lambda e: svg(e, [SHADOW, legs, cape, robe, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


if __name__ == "__main__":
    for key, build in [("irving", irving()), ("leon", leon()), ("boabdil", boabdil())]:
        write(key, build)
    print("sprites de Granada generados")
