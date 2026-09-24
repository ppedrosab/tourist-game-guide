#!/usr/bin/env python3
"""
Coleccionables de Córdoba (medallón 120×124). Aro: oro = comunes; en la ruta de historia,
mar = camino del río y arcilla = Judería; en la gastronómica, mar = Santa Marina y arcilla = Judería.

Uso: python3 scripts/art/cordoba_collectibles.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, SAND, WOOD, WOODL, NAVY, PURPLE, frame, sparkle, waves, write

BG = f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
BRICK = "#B5553A"; STONE = "#EFDCB8"; LEAF = "#4F8B5A"; LEAFD = "#3D6647"


def book(x, y, w, h, c, spine=GOLD):
    return (f'<path d="M{x} {y}H{x + w}V{y + h}H{x}Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x + 3} {y + 4}H{x + w - 3}M{x + 3} {y + h - 4}H{x + w - 3}" stroke="{spine}" stroke-width="1.6"/>')


calamo = (BG + f'<path d="M26 92H94V100H26Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M32 {76 + k * 6}H{88 - k * 10}" stroke="#8A7A62" stroke-width="1.6"/>' for k in range(3))
          + f'<path d="M36 70L84 22L90 28L42 76Z" fill="#D9B77A" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M36 70L30 82L42 76Z" fill="{INK}"/><path d="M58 48L74 32" stroke="#B08A4E" stroke-width="1.6"/>'
          f'<path d="M78 70Q84 60 92 66Q88 76 78 70Z" fill="{NAVY}" stroke="{INK}" stroke-width="1.6"/>' + sparkle(90, 44, 5))

def voussoirs(cx, cy, ro, ri, n=9):
    """Arco de medio punto con dovelas alternas de ladrillo y piedra, como los de la Mezquita."""
    import math
    out = ""
    for k in range(n):
        a0, a1 = math.pi + k * math.pi / n, math.pi + (k + 1) * math.pi / n
        pts = [(cx + ro * math.cos(a0), cy + ro * math.sin(a0)), (cx + ro * math.cos(a1), cy + ro * math.sin(a1)),
               (cx + ri * math.cos(a1), cy + ri * math.sin(a1)), (cx + ri * math.cos(a0), cy + ri * math.sin(a0))]
        d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
        out += f'<path d="{d}" fill="{BRICK if k % 2 == 0 else STONE}" stroke="{INK}" stroke-width="1.2"/>'
    return out


arcos = ('<rect x="0" y="0" width="120" height="124" fill="#5B3A26"/>'
         + "".join(f'<path d="M{x - 4} 112V{y}H{x + 4}V112Z" fill="#8C7A66" stroke="{INK}" stroke-width="1.6"/>' for x, y in [(22, 62), (60, 62), (98, 62)])
         + voussoirs(41, 62, 22, 14) + voussoirs(79, 62, 22, 14)
         + "".join(f'<path d="M{x - 3} 62V{y}H{x + 3}V62" fill="#8C7A66" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(41, 34), (79, 34)])
         + voussoirs(60, 34, 22, 15, 7) + voussoirs(22, 34, 22, 15, 7) + voussoirs(98, 34, 22, 15, 7))

candil = (BG + '<g transform="translate(9 2)">' + f'<circle cx="38" cy="46" r="20" fill="{GOLD}" opacity=".25"/>'
          f'<path d="M34 74Q44 96 68 94Q90 92 92 76Q90 64 70 62L46 64Q38 64 34 70Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>'
          f'<path d="M46 64Q66 56 86 66" fill="none" stroke="#9A5A2E" stroke-width="2"/><ellipse cx="66" cy="64" rx="7" ry="3" fill="#5B3524"/>'
          f'<path d="M34 70L26 64L30 60L40 64Z" fill="#C9763F" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M92 72Q104 70 100 84Q96 90 90 86" fill="none" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M28 60Q20 46 28 32Q36 46 30 60Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M28 56Q25 48 28 42Q31 48 29 56Z" fill="#FFF3C4"/></g>' + sparkle(82, 32, 6))

averroes = (BG + book(26, 34, 68, 56, "#2F6F73")
            + f'<path d="M60 34V90" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M30 40H56V84H30Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><path d="M64 40H90V84H64Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
            + "".join(f'<path d="M34 {48 + k * 8}H52M68 {48 + k * 8}H86" stroke="#8A7A62" stroke-width="1.4"/>' for k in range(4))
            + f'<circle cx="43" cy="28" r="0" fill="none"/>'
            f'<path d="M72 44Q78 38 84 44Q78 50 72 44Z" fill="none" stroke="{CLAY}" stroke-width="1.8"/>' + sparkle(94, 26, 6))

noria = (f'<rect x="0" y="0" width="120" height="124" fill="#F4E4C8"/>' + waves(84)
         + f'<circle cx="60" cy="56" r="34" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="60" cy="56" r="34" fill="none" stroke="{WOODL}" stroke-width="4"/>'
         + "".join(f'<path d="M60 56L{60 + 34 * c:.1f} {56 + 34 * s:.1f}" stroke="{WOOD}" stroke-width="3"/>' for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.71, .71), (-.71, .71), (.71, -.71), (-.71, -.71)])
         + f'<circle cx="60" cy="56" r="6" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>'
         + "".join(f'<path d="M{60 + 34 * c - 4:.1f} {56 + 34 * s - 3:.1f}h8v7h-8Z" fill="#C9763F" stroke="{INK}" stroke-width="1.2"/>' for c, s in [(1, 0), (-1, 0), (0, -1), (.71, .71), (-.71, .71), (.71, -.71), (-.71, -.71)]))

jardin = ('<rect x="0" y="0" width="120" height="124" fill="#F4E4C8"/>'
          f'<path d="M10 70H110V110H10Z" fill="#8FB9B4" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M{x} 80Q{x + 3} 64 {x + 6} 80" fill="none" stroke="{WHITE}" stroke-width="2"/>' for x in (30, 52, 74))
          + "".join(f'<path d="M{x} 70Q{x - 10} 40 {x} 18Q{x + 10} 40 {x} 70Z" fill="{LEAFD}" stroke="{INK}" stroke-width="2"/>' for x in (18, 102))
          + f'<path d="M40 70V40H80V70" fill="{STONE}" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M{x} 40V32H{x + 6}V40" fill="{STONE}" stroke="{INK}" stroke-width="1.4"/>' for x in (40, 52, 64, 74))
          + f'<path d="M54 70V56Q60 50 66 56V70Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>')

catalogo = (BG + "".join(book(20 + k * 12, 34 + (k % 3) * 4, 11, 62 - (k % 3) * 4, [CLAY, SEA, NAVY, PURPLE, "#6E7A3E", GOLDD, CLAY][k]) for k in range(7))
            + f'<path d="M16 98H104" stroke="{WOOD}" stroke-width="6"/>'
            f'<circle cx="84" cy="72" r="15" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<text x="84" y="77" font-family="Georgia, serif" font-size="14" font-weight="700" text-anchor="middle" fill="{INK}">44</text>')

insignia = (f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{PAPER}" opacity=".7"/>' for x, y in [(20, 30), (98, 24), (90, 46), (28, 52), (60, 16)])
            + f'<path d="M34 100V58Q60 20 86 58V100Z" fill="{STONE}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M42 100V62Q60 36 78 62V100Z" fill="#E9D3AE" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(book(45 + k * 8, 72 - (k % 2) * 4, 7, 26 + (k % 2) * 4, [CLAY, SEA, GOLDD, PURPLE][k]) for k in range(4))
            + f'<path d="M40 70H80" stroke="{WOOD}" stroke-width="3"/>' + sparkle(60, 46, 6, GOLD))

# --- gastronomía ---
def bowl(x, y, w, fill, inner):
    return (f'<path d="M{x - w} {y}H{x + w}Q{x + w - 4} {y + w * .9} {x} {y + w * .9}Q{x - w + 4} {y + w * .9} {x - w} {y}Z" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w * .24}" fill="{inner}" stroke="{INK}" stroke-width="2"/>')


dornillo = (BG + bowl(60, 66, 36, "#9A6B45", "#F2E3C4")
            + f'<path d="M66 64L90 24" stroke="{INK}" stroke-width="10"/><path d="M66 64L90 24" stroke="#C9A77E" stroke-width="6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#F7F0E4" stroke="{INK}" stroke-width="1"/>' for x, y in [(34, 64), (46, 62), (52, 67)])
            + f'<path d="M20 100H100" stroke="{WOOD}" stroke-width="5"/>')

anfora = (BG + f'<path d="M50 24H70V32Q86 44 84 66Q82 88 60 104Q38 88 36 66Q34 44 50 32Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M50 32Q38 30 38 44M70 32Q82 30 82 44" fill="none" stroke="{INK}" stroke-width="3"/>'
          f'<path d="M42 58Q60 64 78 58" fill="none" stroke="#9A5A2E" stroke-width="2"/><path d="M52 40Q46 60 52 86" fill="none" stroke="#E0A06A" stroke-width="3"/>'
          f'<path d="M86 34Q98 48 90 60Q82 48 86 34Z" fill="#B7A23A" stroke="{INK}" stroke-width="1.6"/>')

maceta = ('<rect x="0" y="0" width="120" height="124" fill="#F7F0E4"/>'
          f'<path d="M0 0H120V124H0Z" fill="#FFFFFF"/>'
          + "".join(f'<path d="M{x} 0V124" stroke="#EDE3D1" stroke-width="1"/>' for x in range(10, 120, 20))
          + f'<path d="M38 72H82L76 104H44Z" fill="#2F6F9E" stroke="{INK}" stroke-width="2.2"/><path d="M34 66H86V74H34Z" fill="#2F6F9E" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="4.4" transform="rotate({r} {x} {y})" fill="{LEAF}" stroke="{INK}" stroke-width="1.2"/>' for x, y, r in [(46, 58, -30), (74, 58, 30), (60, 52, 0), (40, 46, -50), (80, 46, 50)])
          + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#D8412F" stroke="{INK}" stroke-width="1.6"/><circle cx="{x}" cy="{y}" r="3" fill="{GOLD}"/>' for x, y in [(48, 36), (70, 32), (60, 42), (84, 38), (36, 34)]))

flamenquin = (BG + '<g transform="translate(-7 0)">' + f'<ellipse cx="60" cy="86" rx="46" ry="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
              f'<path d="M22 70Q20 56 34 52L92 42Q104 44 104 58Q102 70 90 72L32 80Q22 80 22 70Z" fill="#D99A48" stroke="{INK}" stroke-width="2.4"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#A8743C"/>' for x, y in [(40, 60), (52, 56), (66, 54), (80, 52), (48, 70), (72, 64), (88, 60)])
              + f'<circle cx="98" cy="57" r="10" fill="#F2E3C4" stroke="{INK}" stroke-width="2"/><path d="M98 57m-6 0a6 6 0 1 0 6 -6" fill="none" stroke="#C0564A" stroke-width="2.4"/>'
              f'<path d="M30 94Q34 88 40 92Q36 98 30 94Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/></g>')

berenjenas = (BG + f'<ellipse cx="60" cy="84" rx="46" ry="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
              + "".join(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="6" transform="rotate({r} {x} {y})" fill="#E3B05A" stroke="{INK}" stroke-width="1.8"/>' for x, y, r in [(40, 80, -10), (60, 76, 8), (80, 82, -6), (52, 88, 4), (72, 90, -4)])
              + f'<path d="M58 30Q54 44 60 58Q66 70 60 76" fill="none" stroke="#7A3E14" stroke-width="5" opacity=".8"/>'
              f'<path d="M50 20H70V28H50Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/><path d="M52 28Q60 34 68 28" fill="#7A3E14" stroke="{INK}" stroke-width="1.4"/>'
              f'<path d="M92 40Q100 30 96 22Q88 32 92 40Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.4"/><path d="M84 46Q96 40 102 52Q94 62 84 56Z" fill="{PURPLE}" stroke="{INK}" stroke-width="1.6"/>')

laud = (BG + f'<path d="M72 50L100 18" stroke="{INK}" stroke-width="10"/><path d="M72 50L100 18" stroke="#6E4C33" stroke-width="6"/>'
        f'<path d="M96 20L108 14L104 28Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.6"/>'
        f'<ellipse cx="52" cy="72" rx="30" ry="36" transform="rotate(40 52 72)" fill="#C98F4E" stroke="{INK}" stroke-width="2.4"/>'
        + "".join(f'<path d="M{36 + k * 5} {92 - k * 4}Q{58 + k * 3} {62 - k * 3} {80 + k * 2} {40 + k}" fill="none" stroke="#A8743C" stroke-width="1"/>' for k in range(3))
        + f'<circle cx="56" cy="66" r="8" fill="#5B3A26" stroke="{INK}" stroke-width="1.4"/>'
        + "".join(f'<path d="M{44 + k * 3} {82}L{98 + k} {20}" stroke="{PAPER}" stroke-width=".8"/>' for k in range(3))
        + f'<path d="M20 30q4 -8 8 0t8 0" fill="none" stroke="{INK}" stroke-width="1.6"/>' + sparkle(26, 48, 4, GOLD))

pastel = (BG + f'<ellipse cx="60" cy="90" rx="46" ry="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M18 80Q18 50 60 46Q102 50 102 80Q80 90 60 90Q40 90 18 80Z" fill="#E6B05E" stroke="{INK}" stroke-width="2.4"/>'
          + "".join(f'<path d="M{24 + k * 9} {70 - (k % 2) * 4}l6 -4" stroke="#B8812E" stroke-width="2"/>' for k in range(9))
          + "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{PAPER}" stroke="{INK}" stroke-width=".8"/>' for x, y in [(40, 58), (60, 54), (80, 58), (50, 66), (70, 66)])
          + f'<path d="M60 90L96 84L90 96Q60 104 30 96Z" fill="#F2A33A" opacity=".5"/>')

salmorejo = (f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
             + bowl(60, 58, 38, "#F7F0E4", "#E8744A")
             + "".join(f'<rect x="{x}" y="{y}" width="5" height="5" fill="{c}" stroke="{INK}" stroke-width=".8"/>' for x, y, c in [(44, 54, "#FFF3C4"), (56, 56, "#C0564A"), (66, 53, "#FFF3C4"), (50, 60, "#C0564A"), (72, 58, "#FFF3C4")])
             + f'<path d="M84 50L104 30" stroke="{INK}" stroke-width="6"/><path d="M84 50L104 30" stroke="#C9CED6" stroke-width="3"/>'
             f'<circle cx="38" cy="36" r="9" fill="#D8412F" stroke="{INK}" stroke-width="2"/><path d="M33 28L38 31L43 28M38 31V24" stroke="{LEAF}" stroke-width="2.4"/>'
             + sparkle(96, 92, 6, GOLD))

ART = {
    "cordoba_calamo": (GOLD, calamo, "El cálamo de Lubna"),
    "cordoba_arcos": (GOLD, arcos, "Los arcos de la Mezquita"),
    "cordoba_candil": (CLAY, candil, "El candil de la Judería"),
    "cordoba_averroes": (CLAY, averroes, "El libro de Averroes"),
    "cordoba_noria": (SEA, noria, "La noria de la Albolafia"),
    "cordoba_jardin": (SEA, jardin, "Los jardines del Alcázar"),
    "cordoba_catalogo": (GOLD, catalogo, "Los 44 catálogos"),
    "cordoba_insignia": (GOLD, insignia, "La biblioteca del califa"),
    "cordoba_dornillo": (GOLD, dornillo, "El dornillo"),
    "cordoba_anfora": (GOLD, anfora, "El ánfora de la Bética"),
    "cordoba_maceta": (SEA, maceta, "La maceta del patio"),
    "cordoba_flamenquin": (SEA, flamenquin, "El flamenquín"),
    "cordoba_berenjenas": (CLAY, berenjenas, "Berenjenas con miel"),
    "cordoba_laud": (CLAY, laud, "El laúd de Ziryab"),
    "cordoba_pastel": (GOLD, pastel, "El pastel cordobés"),
    "cordoba_salmorejo": (GOLD, salmorejo, "¿Quién le puso tomate al salmorejo?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Córdoba generados")
