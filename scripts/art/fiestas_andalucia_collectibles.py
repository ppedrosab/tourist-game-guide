#!/usr/bin/env python3
"""
Coleccionables de las rutas de fiestas de Málaga, Sevilla, Granada, Córdoba, Huelva, Jaén y Almería.
Medallón 120×124. Aro: oro = comunes; mar = primer camino (dinero), arcilla = segundo (poder).

Uso: python3 scripts/art/fiestas_andalucia_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, PURPLE, sparkle, waves, write

BG = '<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
SKY = f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
NIGHT = f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>'
RED = "#D8412F"; LEAF = "#4F8B5A"; ORANGE = "#E8744A"; BLUE = "#3A6EA5"; ROSE = "#C0476A"; FLAME = "#F29A2E"


def doc(year, y=60, seal=CLAY):
    """Pergamino con un año bien grande y un sello."""
    return (f'<path d="M30 {y - 34}H90V{y + 30}Q60 {y + 38} 30 {y + 30}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            + "".join(f'<path d="M38 {y - 24 + k * 7}H82" stroke="#C9B48A" stroke-width="1.6"/>' for k in range(3))
            + f'<text x="60" y="{y + 12}" font-family="Georgia, serif" font-weight="700" font-size="17" text-anchor="middle" fill="{INK}">{year}</text>'
            + f'<circle cx="82" cy="{y + 26}" r="8" fill="{seal}" stroke="{INK}" stroke-width="1.8"/><path d="M78 {y + 32}L76 {y + 42}M86 {y + 32}L88 {y + 42}" stroke="{seal}" stroke-width="3"/>')


def poster(year, art, band=CLAY, size=14):
    return (f'<path d="M32 22H88V100H32Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
            + f'<path d="M32 80H88V100H32Z" fill="{band}" stroke="{INK}" stroke-width="2"/>'
            + art + f'<text x="60" y="95" font-family="Georgia, serif" font-weight="700" font-size="{size}" text-anchor="middle" fill="{PAPER}">{year}</text>')


def paper_lantern(x, y, s=1.0, c=PAPER, dots=RED):
    return (f'<path d="M{x} {y - 26 * s}V{y - 20 * s}" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M{x - 9 * s} {y - 20 * s}H{x + 9 * s}Q{x + 20 * s} {y} {x + 9 * s} {y + 20 * s}H{x - 9 * s}Q{x - 20 * s} {y} {x - 9 * s} {y - 20 * s}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
            + "".join(f'<circle cx="{x + dx * s}" cy="{y + dy * s}" r="{2.6 * s}" fill="{dots}"/>' for dx, dy in [(-5, -8), (5, -2), (-4, 8), (6, 12)]))


def burst(x, y, r, c):
    return ("".join(f'<path d="M{x + r * .3 * math.cos(math.radians(a)):.1f} {y + r * .3 * math.sin(math.radians(a)):.1f}L{x + r * math.cos(math.radians(a)):.1f} {y + r * math.sin(math.radians(a)):.1f}" stroke="{c}" stroke-width="2.6"/>' for a in range(0, 360, 30))
            + "".join(f'<circle cx="{x + r * math.cos(math.radians(a)):.1f}" cy="{y + r * math.sin(math.radians(a)):.1f}" r="2" fill="{c}"/>' for a in range(15, 360, 30)))


def carnation(x, y, s=1.0, c=RED):
    return (f'<path d="M{x} {y}V{y + 30 * s}" stroke="{LEAF}" stroke-width="{3 * s}"/>'
            f'<path d="M{x} {y + 18 * s}Q{x + 10 * s} {y + 12 * s} {x + 14 * s} {y + 16 * s}" fill="none" stroke="{LEAF}" stroke-width="{2.4 * s}"/>'
            + "".join(f'<circle cx="{x + dx * s}" cy="{y + dy * s}" r="{6 * s}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for dx, dy in [(-7, -2), (7, -2), (0, -8), (-4, 2), (4, 2)]))


def fan(cx, cy, r, c1, c2, a0=200, a1=340):
    ribs = range(a0, a1 + 1, 20)
    pts = " ".join(f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}" for a in ribs)
    out = f'<polygon points="{cx},{cy} {pts}" fill="{c1}" stroke="{INK}" stroke-width="2.2"/>'
    for k, a in enumerate(ribs):
        if k % 2:
            b = a - 20
            out += f'<path d="M{cx} {cy}L{cx + r * math.cos(math.radians(b)):.1f} {cy + r * math.sin(math.radians(b)):.1f}L{cx + r * math.cos(math.radians(a)):.1f} {cy + r * math.sin(math.radians(a)):.1f}Z" fill="{c2}" stroke="{INK}" stroke-width="1"/>'
    return out + f'<circle cx="{cx}" cy="{cy}" r="4" fill="{WOOD}" stroke="{INK}" stroke-width="1.4"/>'


def castanet(x, y, rot=0, c="#6E3A22"):
    return (f'<g transform="rotate({rot} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="15" ry="19" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            f'<ellipse cx="{x - 4}" cy="{y - 6}" rx="4" ry="6" fill="#FFF" opacity=".25"/>'
            f'<path d="M{x} {y - 19}Q{x - 8} {y - 30} {x + 4} {y - 32}" fill="none" stroke="{RED}" stroke-width="3"/></g>')


def flame(x, y, s=1.0):
    return (f'<path d="M{x} {y - 30 * s}Q{x + 16 * s} {y - 12 * s} {x + 12 * s} {y}Q{x} {y + 8 * s} {x - 12 * s} {y}Q{x - 16 * s} {y - 14 * s} {x} {y - 30 * s}Z" fill="{FLAME}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x} {y - 16 * s}Q{x + 8 * s} {y - 6 * s} {x + 5 * s} {y}Q{x} {y + 3 * s} {x - 5 * s} {y}Q{x - 7 * s} {y - 6 * s} {x} {y - 16 * s}Z" fill="{GOLD}"/>')


def logs(y=86):
    return "".join(f'<path d="M{x1} {y + 8}L{x2} {y - 6}" stroke="{INK}" stroke-width="9"/><path d="M{x1} {y + 8}L{x2} {y - 6}" stroke="{WOODL}" stroke-width="6"/>'
                   for x1, x2 in [(34, 80), (86, 40), (48, 72)])


def ribbon(y=34, c=RED):
    return f'<path d="M24 {y}Q60 {y + 10} 96 {y}" fill="none" stroke="{INK}" stroke-width="1.4"/>'


# --- Málaga · Feria de Agosto -------------------------------------------------
m_abanico = BG + fan(60, 84, 48, RED, PAPER) + sparkle(94, 30, 6, GOLD)

m_sombrero = (BG + f'<path d="M20 74Q60 60 100 74Q60 84 20 74Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.2"/>'
              f'<path d="M36 70Q34 34 60 32Q86 34 84 70Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.2"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for x, y, r, c in [(46, 44, 6, RED), (60, 36, 6, GOLD), (74, 44, 6, ROSE), (52, 56, 5, BLUE), (68, 56, 5, LEAF)])
              + "".join(f'<rect x="{x}" y="{y}" width="6" height="6" transform="rotate(45 {x + 3} {y + 3})" fill="#DDE8F0" stroke="{INK}" stroke-width="1"/>' for x, y in [(40, 60), (74, 62), (58, 48)])
              + "".join(f'<path d="M{x} 76Q{x + w} 90 {x} 104" fill="none" stroke="{c}" stroke-width="3.6"/>' for x, w, c in [(28, -6, RED), (36, 5, GOLD), (84, 6, BLUE), (92, -5, LEAF)]))

m_biznaga = (BG + f'<path d="M60 104V64" stroke="{WOOD}" stroke-width="4"/>'
             + "".join(f'<circle cx="{60 + 20 * math.cos(math.radians(a)):.1f}" cy="{52 + 20 * math.sin(math.radians(a)):.1f}" r="7" fill="{WHITE}" stroke="{INK}" stroke-width="1.4"/>' for a in range(0, 360, 30))
             + "".join(f'<circle cx="{60 + 10 * math.cos(math.radians(a)):.1f}" cy="{52 + 10 * math.sin(math.radians(a)):.1f}" r="6" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>' for a in range(15, 360, 45))
             + f'<circle cx="60" cy="52" r="7" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>'
             + f'<path d="M60 88Q72 80 80 86Q70 92 60 88Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.2"/>' + sparkle(96, 92, 5, GOLD))

m_fuegos = (NIGHT + waves(92, SEA, "#2F6F73") + burst(44, 44, 20, GOLD) + burst(80, 36, 14, RED) + burst(76, 70, 10, PAPER)
            + sparkle(28, 76, 5, GOLD))

m_estandarte = (BG + f'<path d="M34 20V104" stroke="{INK}" stroke-width="5"/><path d="M34 20V104" stroke="{WOODL}" stroke-width="3"/>'
                f'<circle cx="34" cy="20" r="5" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M36 26H92L84 46L92 66H36Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/>'
                f'<text x="60" y="52" font-family="Georgia, serif" font-weight="700" font-size="17" text-anchor="middle" fill="{GOLD}">1487</text>')

m_acta = BG + doc("1491")

m_farolillo = (NIGHT + f'<path d="M14 30Q60 44 106 30" fill="none" stroke="{PAPER}" stroke-width="1.4"/>'
               + paper_lantern(60, 66, 1.4, PAPER, RED) + paper_lantern(28, 50, .7, "#F7E6CF", LEAF) + paper_lantern(92, 50, .7, "#F7E6CF", LEAF))

m_insignia = (NIGHT + waves(96, SEA, "#2F6F73") + burst(60, 44, 24, GOLD) + fan(60, 100, 30, RED, PAPER, 210, 330) + sparkle(24, 30, 5, GOLD) + sparkle(96, 28, 5, PAPER))

# --- Sevilla · Feria de Abril -------------------------------------------------
s_traje = (BG + f'<path d="M50 24H70L74 50L62 56L46 50Z" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
           + "".join(f'<path d="M{50 - k * 9} {48 + k * 16}Q60 {56 + k * 16} {70 + k * 9} {48 + k * 16}L{74 + k * 10} {64 + k * 16}Q60 {72 + k * 16} {46 - k * 10} {64 + k * 16}Z" fill="{RED}" stroke="{INK}" stroke-width="2"/>' for k in range(3))
           + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{PAPER}"/>' for x, y in [(56, 34), (64, 42), (48, 62), (70, 60), (40, 80), (58, 84), (78, 78), (36, 96), (60, 100), (84, 96)]))

s_herradura = (BG + f'<path d="M36 94V56Q36 28 60 28Q84 28 84 56V94H72V56Q72 42 60 42Q48 42 48 56V94Z" fill="{SILVER}" stroke="{INK}" stroke-width="2.4"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{INK}"/>' for x, y in [(42, 84), (42, 66), (48, 44), (78, 84), (78, 66), (72, 44)]) + sparkle(94, 30, 6, GOLD))

s_cartel = BG + poster("1847", f'<path d="M40 70Q60 30 80 70Z" fill="{SEA}" stroke="{INK}" stroke-width="2"/>' + paper_lantern(60, 44, .6), SEA)

s_azulejo = (BG + f'<path d="M26 26H94V94H26Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
             + f'<path d="M60 30Q80 40 90 60Q80 80 60 90Q40 80 30 60Q40 40 60 30Z" fill="{BLUE}" stroke="{INK}" stroke-width="1.6"/>'
             + f'<circle cx="60" cy="60" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/><circle cx="60" cy="60" r="5" fill="{SEA}"/>'
             + "".join(f'<path d="M{x} {y}l6 6-6 6-6-6Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>' for x, y in [(32, 28), (88, 28), (32, 80), (88, 80)]))

s_caseta = (BG + f'<path d="M22 50L60 24L98 50Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            + "".join(f'<path d="M{60 + (x - 60) * 0} 24L{x} 50L{x + 9} 50Z" fill="{CLAY}"/>' for x in (26, 44, 62, 80))
            + f'<path d="M22 50L60 24L98 50Z" fill="none" stroke="{INK}" stroke-width="2.2"/>'
            + f'<path d="M26 50H94V100H26Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            + "".join(f'<path d="M{x} 50H{x + 8}V100H{x}Z" fill="{CLAY}"/>' for x in (30, 46, 62, 78))
            + f'<path d="M26 50H94V100H26Z" fill="none" stroke="{INK}" stroke-width="2.2"/>'
            + "".join(f'<path d="M{x} 50Q{x + 8} 60 {x + 16} 50" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>' for x in (26, 42, 58, 74)))

s_cigarrera = (BG + f'<path d="M24 56H96V94H24Z" fill="{WOODL}" stroke="{INK}" stroke-width="2.4"/>'
               f'<path d="M24 56L34 40H106L96 56Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/>'
               f'<path d="M34 64H86V86H34Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
               f'<text x="60" y="80" font-family="Georgia, serif" font-weight="700" font-size="11" text-anchor="middle" fill="{CLAY}">SEVILLA</text>'
               + carnation(92, 26, .6))

s_portada = (NIGHT + f'<path d="M20 100V52Q20 30 34 26H86Q100 30 100 52V100H80V60Q80 46 60 46Q40 46 40 60V100Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for x, y in [(24, 50), (30, 36), (44, 30), (60, 30), (76, 30), (90, 36), (96, 50), (24, 70), (96, 70), (24, 88), (96, 88)])
             + f'<path d="M50 26L60 12L70 26Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')

s_insignia = (NIGHT + "".join(f'<path d="M14 {y}Q60 {y + 12} 106 {y}" fill="none" stroke="{PAPER}" stroke-width="1.2"/>' for y in (28, 58))
              + "".join(paper_lantern(x, y, .55, c, d) for x, y, c, d in [(30, 44, PAPER, RED), (60, 48, "#F7E6CF", LEAF), (90, 44, PAPER, RED), (40, 76, "#F7E6CF", LEAF), (80, 76, PAPER, RED)])
              + sparkle(60, 94, 6, GOLD))

# --- Granada · la Tarasca -----------------------------------------------------
g_cabezudo = (BG + f'<circle cx="60" cy="58" r="34" fill="#F0C8A0" stroke="{INK}" stroke-width="2.4"/>'
              f'<path d="M26 54Q28 22 60 22Q92 22 94 54Q80 36 60 38Q40 36 26 54Z" fill="#2A1E1A" stroke="{INK}" stroke-width="2"/>'
              f'<circle cx="48" cy="58" r="4" fill="{INK}"/><circle cx="72" cy="58" r="4" fill="{INK}"/>'
              f'<circle cx="40" cy="70" r="6" fill="#E8866A" opacity=".7"/><circle cx="80" cy="70" r="6" fill="#E8866A" opacity=".7"/>'
              f'<path d="M50 76Q60 86 70 76" fill="none" stroke="{INK}" stroke-width="2.4"/><path d="M58 60Q60 70 64 68" fill="none" stroke="{INK}" stroke-width="1.6"/>')

g_tijeras = (BG + f'<circle cx="46" cy="88" r="10" fill="none" stroke="{RED}" stroke-width="5"/><circle cx="74" cy="88" r="10" fill="none" stroke="{RED}" stroke-width="5"/>'
             f'<path d="M52 80L78 24L72 22L50 72Z" fill="{SILVER}" stroke="{INK}" stroke-width="2"/><path d="M68 80L42 24L48 22L70 72Z" fill="{SILVERD}" stroke="{INK}" stroke-width="2"/>'
             f'<circle cx="60" cy="58" r="3" fill="{INK}"/>' + f'<path d="M20 40Q34 30 30 48" fill="none" stroke="{PURPLE}" stroke-width="3"/>')

g_tambor = (BG + f'<ellipse cx="60" cy="48" rx="34" ry="10" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M26 48V86Q60 100 94 86V48Q60 60 26 48Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M28 54L44 90L60 56L76 92L92 54" fill="none" stroke="{GOLD}" stroke-width="2.4"/>'
            f'<path d="M50 42L30 20M70 42L90 20" stroke="{INK}" stroke-width="4"/><circle cx="30" cy="20" r="4" fill="{WOOD}"/><circle cx="90" cy="20" r="4" fill="{WOOD}"/>')

g_gigantes = (BG + "".join(f'<path d="M{x - 14} 100L{x - 10} 50H{x + 10}L{x + 14} 100Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                           f'<circle cx="{x}" cy="38" r="12" fill="#F0C8A0" stroke="{INK}" stroke-width="2"/>'
                           f'<path d="M{x - 12} 32Q{x} 18 {x + 12} 32" fill="{h}" stroke="{INK}" stroke-width="1.6"/>'
                           f'<circle cx="{x - 4}" cy="38" r="1.6" fill="{INK}"/><circle cx="{x + 4}" cy="38" r="1.6" fill="{INK}"/>'
                           for x, c, h in [(40, SEA, GOLD), (80, CLAY, "#2A1E1A")]))

g_dulzaina = (BG + f'<path d="M36 24L78 92" stroke="{INK}" stroke-width="10"/><path d="M36 24L78 92" stroke="{WOODL}" stroke-width="7"/>'
              f'<path d="M72 84L90 104L66 98Z" fill="{WOODL}" stroke="{INK}" stroke-width="2"/>'
              + "".join(f'<circle cx="{36 + 42 * t:.1f}" cy="{24 + 68 * t:.1f}" r="2.2" fill="{INK}"/>' for t in (.3, .4, .5, .6, .7))
              + f'<path d="M32 18L38 26" stroke="{GOLDD}" stroke-width="4"/>' + sparkle(92, 36, 6, GOLD))

g_dragon = (BG + f'<path d="M22 78Q30 52 58 56Q84 60 92 44Q100 34 96 26Q104 34 102 48Q98 70 70 76Q50 80 44 94Q30 94 22 78Z" fill="{LEAF}" stroke="{INK}" stroke-width="2.2"/>'
            + "".join(f'<path d="M{x} {y}l5 -10 5 10Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>' for x, y in [(40, 60), (52, 57), (64, 59), (76, 56)])
            + f'<circle cx="94" cy="34" r="2.4" fill="{INK}"/><path d="M102 44Q110 42 112 48" fill="none" stroke="{RED}" stroke-width="2"/>'
            + f'<path d="M30 86L24 100M42 88L40 102" stroke="{INK}" stroke-width="3"/>')

g_muneca = (BG + f'<circle cx="60" cy="34" r="11" fill="#F0C8A0" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M49 30Q50 18 60 18Q70 18 71 30Q66 24 60 24Q54 24 49 30Z" fill="#8A5A3A" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M46 50Q60 44 74 50L88 100H32Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M36 90Q60 98 84 90L88 100H32Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M60 20L54 8H66Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="56" cy="34" r="1.4" fill="{INK}"/><circle cx="64" cy="34" r="1.4" fill="{INK}"/>' + sparkle(92, 40, 6, GOLD) + sparkle(26, 60, 5, GOLD))

g_insignia = (NIGHT + f'<path d="M18 86Q30 60 60 64Q88 68 96 50Q104 38 98 30Q108 40 104 56Q98 80 68 84Q50 86 42 100Q26 100 18 86Z" fill="{LEAF}" stroke="{INK}" stroke-width="2.2"/>'
              f'<circle cx="60" cy="44" r="8" fill="#F0C8A0" stroke="{INK}" stroke-width="1.6"/><path d="M52 56Q60 52 68 56L72 72H48Z" fill="{PURPLE}" stroke="{INK}" stroke-width="1.6"/>'
              + sparkle(26, 30, 5, GOLD) + sparkle(94, 20, 5, PAPER))

# --- Córdoba · mayo ----------------------------------------------------------
c_clavel = BG + carnation(60, 42, 2.0) + sparkle(94, 30, 6, GOLD)

c_pregon = (BG + f'<path d="M26 60L80 36V96L26 72Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M18 58H28V74H18Z" fill="{GOLDD}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M88 50Q96 66 88 82M96 42Q108 66 96 90" fill="none" stroke="{CLAY}" stroke-width="3"/>')

c_reja = (f'<rect x="0" y="0" width="120" height="124" fill="#F4F1EA"/>'
          + "".join(f'<path d="M{x} 24V100" stroke="{INK}" stroke-width="3"/>' for x in (36, 52, 68, 84))
          + "".join(f'<path d="M28 {y}H92" stroke="{INK}" stroke-width="3"/>' for y in (40, 70))
          + "".join(f'<path d="M{x - 8} {y}H{x + 8}Q{x + 6} {y + 12} {x} {y + 12}Q{x - 6} {y + 12} {x - 8} {y}Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>'
                    f'<circle cx="{x - 4}" cy="{y - 4}" r="4.4" fill="{RED}" stroke="{INK}" stroke-width="1"/><circle cx="{x + 4}" cy="{y - 5}" r="4.4" fill="{ROSE}" stroke="{INK}" stroke-width="1"/>'
                    for x, y in [(44, 32), (76, 32), (44, 62), (76, 62), (60, 92)]))

c_cruz = (BG + f'<path d="M52 20H68V44H92V60H68V104H52V60H28V44H52Z" fill="{RED}" stroke="{INK}" stroke-width="2.4"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}" stroke="{INK}" stroke-width=".8"/>' for x, y, c in
                    [(60, 26, ROSE), (60, 36, RED), (36, 52, ROSE), (46, 52, "#E8744A"), (74, 52, "#E8744A"), (84, 52, ROSE), (60, 52, GOLD), (60, 68, ROSE), (60, 80, "#E8744A"), (60, 94, ROSE)])
          + f'<path d="M36 104H84" stroke="{LEAF}" stroke-width="5"/>')

c_pozo = (BG + f'<path d="M30 60H90V98H30Z" fill="#F4F1EA" stroke="{INK}" stroke-width="2.4"/>'
          f'<ellipse cx="60" cy="60" rx="30" ry="8" fill="{SEA}" stroke="{INK}" stroke-width="2.2"/>'
          f'<path d="M36 60V26M84 60V26M32 26H88" stroke="{INK}" stroke-width="4"/><path d="M36 60V26M84 60V26M32 26H88" stroke="{WOODL}" stroke-width="2"/>'
          f'<path d="M60 26V46" stroke="{INK}" stroke-width="1.4"/><path d="M52 46H68L66 56H54Z" fill="{WOOD}" stroke="{INK}" stroke-width="1.6"/>'
          + carnation(28, 76, .5) + carnation(92, 76, .5, ROSE))

c_privilegio = BG + doc("1284", 60, PURPLE)

c_sombrero = (BG + f'<ellipse cx="60" cy="74" rx="44" ry="11" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>'
              f'<path d="M38 72L40 36H80L82 72Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>'
              f'<path d="M39 62H81V70H39Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>' + sparkle(94, 32, 6, GOLD))

c_insignia = (NIGHT + f'<path d="M52 20H68V44H92V60H68V104H52V60H28V44H52Z" fill="{RED}" stroke="{INK}" stroke-width="2"/>'
              + carnation(30, 78, .7) + carnation(90, 78, .7, ROSE) + sparkle(24, 28, 5, GOLD) + sparkle(96, 28, 5, PAPER))

# --- Huelva · Colombinas ----------------------------------------------------
def caravel(x=60, y=76, s=1.0):
    return (f'<path d="M{x - 38 * s} {y}H{x + 38 * s}L{x + 28 * s} {y + 14 * s}H{x - 28 * s}Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x} {y}V{y - 52 * s}M{x - 22 * s} {y}V{y - 36 * s}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M{x - 16 * s} {y - 48 * s}H{x + 16 * s}Q{x + 20 * s} {y - 30 * s} {x + 16 * s} {y - 14 * s}H{x - 16 * s}Q{x - 12 * s} {y - 30 * s} {x - 16 * s} {y - 48 * s}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x - 6 * s} {y - 38 * s}H{x + 6 * s}M{x} {y - 44 * s}V{y - 32 * s}" stroke="{RED}" stroke-width="{3 * s}"/>'
            f'<path d="M{x - 22 * s} {y - 34 * s}L{x - 36 * s} {y - 6 * s}H{x - 22 * s}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')


h_carabela = SKY + waves(88) + caravel(60, 80)

h_medalla = (BG + f'<path d="M48 20L60 44L72 20" fill="none" stroke="{RED}" stroke-width="8"/>'
             f'<circle cx="60" cy="70" r="26" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/><circle cx="60" cy="70" r="19" fill="none" stroke="{GOLDD}" stroke-width="2"/>'
             + caravel(60, 76, .38))

h_timon = (SKY + f'<circle cx="60" cy="60" r="28" fill="none" stroke="{INK}" stroke-width="9"/><circle cx="60" cy="60" r="28" fill="none" stroke="{WOODL}" stroke-width="6"/>'
           + "".join(f'<path d="M{60 + 12 * math.cos(math.radians(a)):.1f} {60 + 12 * math.sin(math.radians(a)):.1f}L{60 + 42 * math.cos(math.radians(a)):.1f} {60 + 42 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="7"/>'
                     f'<path d="M{60 + 12 * math.cos(math.radians(a)):.1f} {60 + 12 * math.sin(math.radians(a)):.1f}L{60 + 42 * math.cos(math.radians(a)):.1f} {60 + 42 * math.sin(math.radians(a)):.1f}" stroke="{WOODL}" stroke-width="4"/>' for a in range(0, 360, 45))
           + f'<circle cx="60" cy="60" r="11" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/><circle cx="60" cy="60" r="4" fill="{GOLD}"/>')

h_trofeo = (BG + f'<path d="M38 30H82Q82 70 60 72Q38 70 38 30Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M38 36Q24 36 26 50Q28 60 42 60M82 36Q96 36 94 50Q92 60 78 60" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M56 72H64V84H56Z" fill="{GOLDD}" stroke="{INK}" stroke-width="1.8"/><path d="M42 84H78V98H42Z" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="60" cy="48" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><path d="M60 39L64 46L60 52L56 46Z" fill="{INK}"/>')

h_acta = BG + doc("1880", 60, SEA)

h_cartel = BG + poster("1892", caravel(60, 70, .5), CLAY)

h_noria = (SKY + f'<circle cx="60" cy="54" r="32" fill="none" stroke="{INK}" stroke-width="3"/>'
           + "".join(f'<path d="M60 54L{60 + 32 * math.cos(math.radians(a)):.1f} {54 + 32 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="1.6"/>'
                     f'<path d="M{60 + 32 * math.cos(math.radians(a)) - 6:.1f} {54 + 32 * math.sin(math.radians(a)):.1f}h12v9h-12Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                     for a, c in zip(range(0, 360, 45), [RED, GOLD, SEA, CLAY, RED, GOLD, SEA, CLAY]))
           + f'<path d="M60 54L42 104M60 54L78 104" stroke="{INK}" stroke-width="3"/><circle cx="60" cy="54" r="5" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>')

h_insignia = (NIGHT + waves(90, SEA, "#2F6F73") + caravel(52, 80, .8) + burst(92, 34, 12, GOLD) + sparkle(24, 28, 5, GOLD))

# --- Jaén · lumbres de San Antón --------------------------------------------
j_candela = NIGHT + logs(90) + flame(60, 80, 1.8) + sparkle(26, 30, 4, GOLD) + sparkle(94, 40, 4, GOLD)

j_tijeras = (BG + f'<path d="M50 104L54 64M70 104L64 64" stroke="{INK}" stroke-width="9"/><path d="M50 104L54 64M70 104L64 64" stroke="{CLAY}" stroke-width="6"/>'
             f'<path d="M54 64Q36 40 50 18Q62 40 62 64Z" fill="{SILVER}" stroke="{INK}" stroke-width="2"/>'
             f'<path d="M62 64Q84 44 76 22Q58 40 56 64Z" fill="{SILVERD}" stroke="{INK}" stroke-width="2"/><circle cx="59" cy="62" r="3" fill="{INK}"/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3" transform="rotate({r} {x} {y})" fill="{LEAF}" stroke="{INK}" stroke-width="1"/>' for x, y, r in [(90, 70, -30), (96, 82, 20), (86, 90, -10)]))

j_cencerro = (BG + f'<path d="M60 20Q72 20 72 32" fill="none" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M44 34H76L84 92H36Z" fill="{GOLDD}" stroke="{INK}" stroke-width="2.4"/><path d="M62 34H76L84 92H66Z" fill="#A87A22"/>'
              f'<path d="M44 34H76L84 92H36Z" fill="none" stroke="{INK}" stroke-width="2.4"/>'
              f'<circle cx="60" cy="98" r="6" fill="{INK}"/><path d="M30 60L22 56M30 72L20 74M90 60L98 56M90 72L100 74" stroke="{INK}" stroke-width="2"/>')

j_dorsal = (BG + f'<path d="M24 34H96V94H24Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M24 34H96V48H24Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>'
            f'<text x="60" y="84" font-family="Georgia, serif" font-weight="700" font-size="30" text-anchor="middle" fill="{INK}">17</text>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{SILVER}" stroke="{INK}" stroke-width="1"/>' for x, y in [(30, 40), (90, 40), (30, 88), (90, 88)]))

j_brasero = (BG + f'<path d="M28 66H92Q90 94 60 96Q30 94 28 66Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.4"/>'
             f'<path d="M24 66H96" stroke="{INK}" stroke-width="4"/><path d="M40 96L36 106M80 96L84 106" stroke="{INK}" stroke-width="3"/>'
             + "".join(f'<circle cx="{x}" cy="62" r="6" fill="{c}" stroke="{INK}" stroke-width="1"/>' for x, c in [(42, RED), (54, FLAME), (66, RED), (78, FLAME)])
             + "".join(f'<path d="M{x} 50Q{x + 6} 40 {x} 30" fill="none" stroke="#C9B48A" stroke-width="2"/>' for x in (46, 60, 74)))

j_rosetas = (BG + f'<path d="M30 56H90L82 100H38Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
             + "".join(f'<path d="M{x} 56V100" stroke="{RED}" stroke-width="5"/>' for x in (44, 60, 76))
             + f'<path d="M30 56H90L82 100H38Z" fill="none" stroke="{INK}" stroke-width="2.4"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#FFF3D6" stroke="{INK}" stroke-width="1.2"/>' for x, y in [(38, 50), (50, 44), (62, 48), (74, 42), (84, 50), (56, 36), (70, 32), (44, 34)]))

j_haz = (BG + "".join(f'<path d="M{24 + k * 3} {40 + k * 6}L{96 - k * 2} {70 + k * 4}" stroke="{INK}" stroke-width="7"/><path d="M{24 + k * 3} {40 + k * 6}L{96 - k * 2} {70 + k * 4}" stroke="{WOODL}" stroke-width="4"/>' for k in range(5))
         + f'<path d="M54 50Q60 72 62 84" fill="none" stroke="{CLAY}" stroke-width="5"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3" transform="rotate({r} {x} {y})" fill="{LEAF}" stroke="{INK}" stroke-width="1"/>' for x, y, r in [(22, 34, -30), (28, 28, 10), (98, 64, 30), (100, 76, -20)]))

j_insignia = (NIGHT + logs(92) + flame(60, 84, 2.0)
              + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{PURPLE}" stroke="{INK}" stroke-width="1.4"/><path d="M{x - 6} {y + 6}L{x - 8} {y + 22}H{x + 8}L{x + 6} {y + 6}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                        for x, y, c in [(24, 70, CLAY), (96, 70, SEA)]) + sparkle(30, 28, 4, GOLD) + sparkle(92, 30, 4, GOLD))

# --- Almería · Feria de la Virgen del Mar ------------------------------------
a_castanuelas = BG + castanet(46, 62, -15) + castanet(74, 62, 15) + sparkle(94, 28, 6, GOLD)

a_cohete = (NIGHT + f'<path d="M60 104V56" stroke="{WOODL}" stroke-width="3"/>'
            f'<path d="M52 58H68V30H52Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/><path d="M52 30L60 14L68 30Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M52 44H68" stroke="{PAPER}" stroke-width="3"/>' + burst(28, 36, 10, GOLD) + burst(92, 48, 12, RED))

a_racimo = (BG + f'<path d="M60 18V32" stroke="{WOOD}" stroke-width="4"/><path d="M60 24Q78 12 90 22Q76 34 60 26Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#B9C98A" stroke="{INK}" stroke-width="1.4"/>' for x, y in
                      [(42, 40), (56, 38), (70, 40), (82, 42), (48, 54), (62, 54), (76, 54), (54, 68), (68, 68), (60, 82), (46, 70), (74, 70)])
            + f'<path d="M22 100H98" stroke="{WOOD}" stroke-width="4"/>')

a_torre = (SKY + waves(92) + f'<path d="M44 92L48 34H72L76 92Z" fill="#E6D2A8" stroke="{INK}" stroke-width="2.4"/>'
           f'<path d="M46 34H74V26H46Z" fill="#E6D2A8" stroke="{INK}" stroke-width="2"/>'
           + "".join(f'<path d="M{x} 26V20H{x + 5}V26" fill="#E6D2A8" stroke="{INK}" stroke-width="1.6"/>' for x in (47, 57, 67))
           + f'<path d="M58 60H62V70H58Z" fill="{INK}"/>' + f'<circle cx="90" cy="30" r="8" fill="#FFF3C4" stroke="{INK}" stroke-width="1.4"/>')

a_concha = (SKY + f'<path d="M60 96L26 52Q30 26 60 24Q90 26 94 52Z" fill="#F4D8C4" stroke="{INK}" stroke-width="2.4"/>'
            + "".join(f'<path d="M60 94L{x} {y}" stroke="#C9927A" stroke-width="2"/>' for x, y in [(32, 50), (42, 34), (60, 28), (78, 34), (88, 50)])
            + f'<path d="M48 96H72L66 104H54Z" fill="#F4D8C4" stroke="{INK}" stroke-width="2"/>')

a_vela = (NIGHT + f'<path d="M50 50H70V100H50Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
          f'<path d="M60 50V44" stroke="{INK}" stroke-width="2"/>' + flame(60, 44, .8)
          + f'<path d="M40 100H80V106H40Z" fill="{GOLDD}" stroke="{INK}" stroke-width="1.6"/>'
          + f'<circle cx="60" cy="34" r="24" fill="{GOLD}" opacity=".15"/>')

a_cartel = BG + poster("AGOSTO", castanet(60, 52, 0), SEA, 10)

a_insignia = (NIGHT + waves(92, SEA, "#2F6F73") + f'<path d="M86 92L88 50H100L102 92Z" fill="#E6D2A8" stroke="{INK}" stroke-width="2"/>'
              + burst(46, 40, 18, GOLD) + castanet(40, 76, -20) + sparkle(96, 30, 5, PAPER))

ART = {
    "malaga_fiesta_abanico": (GOLD, m_abanico, "El abanico"),
    "malaga_fiesta_sombrero": (GOLD, m_sombrero, "El sombrero de verdiales"),
    "malaga_fiesta_biznaga": (SEA, m_biznaga, "La biznaga"),
    "malaga_fiesta_fuegos": (SEA, m_fuegos, "Los fuegos de la Malagueta"),
    "malaga_fiesta_estandarte": (CLAY, m_estandarte, "El estandarte de 1487"),
    "malaga_fiesta_acta": (CLAY, m_acta, "El acta de 1491"),
    "malaga_fiesta_farolillo": (GOLD, m_farolillo, "El farolillo"),
    "malaga_fiesta_insignia": (GOLD, m_insignia, "¿Qué celebra la Feria de Agosto?"),
    "sevilla_fiesta_traje": (GOLD, s_traje, "El traje de flamenca"),
    "sevilla_fiesta_herradura": (GOLD, s_herradura, "La herradura"),
    "sevilla_fiesta_cartel": (SEA, s_cartel, "El cartel de 1847"),
    "sevilla_fiesta_azulejo": (SEA, s_azulejo, "El azulejo de la provincia"),
    "sevilla_fiesta_caseta": (CLAY, s_caseta, "La caseta"),
    "sevilla_fiesta_cigarrera": (CLAY, s_cigarrera, "La cigarrera"),
    "sevilla_fiesta_portada": (GOLD, s_portada, "La portada"),
    "sevilla_fiesta_insignia": (GOLD, s_insignia, "¿Quién inventó la Feria de Abril?"),
    "granada_fiesta_cabezudo": (GOLD, g_cabezudo, "El cabezudo"),
    "granada_fiesta_tijeras": (GOLD, g_tijeras, "Las tijeras de la modista"),
    "granada_fiesta_tambor": (SEA, g_tambor, "El tambor"),
    "granada_fiesta_gigantes": (SEA, g_gigantes, "Los gigantes"),
    "granada_fiesta_dulzaina": (CLAY, g_dulzaina, "La dulzaina"),
    "granada_fiesta_dragon": (CLAY, g_dragon, "El dragón de Tarascón"),
    "granada_fiesta_muneca": (GOLD, g_muneca, "La muñeca de la Tarasca"),
    "granada_fiesta_insignia": (GOLD, g_insignia, "¿De dónde viene la Tarasca?"),
    "cordoba_fiesta_clavel": (GOLD, c_clavel, "El clavel"),
    "cordoba_fiesta_pregon": (GOLD, c_pregon, "El pregón"),
    "cordoba_fiesta_reja": (SEA, c_reja, "La reja florida"),
    "cordoba_fiesta_cruz": (SEA, c_cruz, "La cruz de mayo"),
    "cordoba_fiesta_pozo": (CLAY, c_pozo, "El pozo de la Salud"),
    "cordoba_fiesta_privilegio": (CLAY, c_privilegio, "El privilegio de 1284"),
    "cordoba_fiesta_sombrero": (GOLD, c_sombrero, "El sombrero cordobés"),
    "cordoba_fiesta_insignia": (GOLD, c_insignia, "¿Cuál es la fiesta más antigua de mayo?"),
    "huelva_fiesta_carabela": (GOLD, h_carabela, "La carabela"),
    "huelva_fiesta_medalla": (GOLD, h_medalla, "La medalla colombina"),
    "huelva_fiesta_timon": (SEA, h_timon, "El timón de la Pinta"),
    "huelva_fiesta_trofeo": (SEA, h_trofeo, "El Trofeo Colombino"),
    "huelva_fiesta_acta": (CLAY, h_acta, "El acta de 1880"),
    "huelva_fiesta_cartel": (CLAY, h_cartel, "El cartel de 1892"),
    "huelva_fiesta_noria": (GOLD, h_noria, "La noria de la ría"),
    "huelva_fiesta_insignia": (GOLD, h_insignia, "¿Quién inventó las Colombinas?"),
    "jaen_fiesta_candela": (GOLD, j_candela, "La candela"),
    "jaen_fiesta_tijeras": (GOLD, j_tijeras, "Las tijeras de podar"),
    "jaen_fiesta_cencerro": (SEA, j_cencerro, "El cencerro"),
    "jaen_fiesta_dorsal": (SEA, j_dorsal, "El dorsal de la carrera"),
    "jaen_fiesta_brasero": (CLAY, j_brasero, "El brasero"),
    "jaen_fiesta_rosetas": (CLAY, j_rosetas, "Las rosetas"),
    "jaen_fiesta_haz": (GOLD, j_haz, "El haz de leña"),
    "jaen_fiesta_insignia": (GOLD, j_insignia, "¿Por qué Jaén enciende lumbres por San Antón?"),
    "almeria_fiesta_castanuelas": (GOLD, a_castanuelas, "Las castañuelas"),
    "almeria_fiesta_cohete": (GOLD, a_cohete, "El cohete"),
    "almeria_fiesta_racimo": (SEA, a_racimo, "El racimo de uva"),
    "almeria_fiesta_torre": (SEA, a_torre, "La torre de Torregarcía"),
    "almeria_fiesta_concha": (CLAY, a_concha, "La concha"),
    "almeria_fiesta_vela": (CLAY, a_vela, "La vela del santuario"),
    "almeria_fiesta_cartel": (GOLD, a_cartel, "El cartel de la feria"),
    "almeria_fiesta_insignia": (GOLD, a_insignia, "¿Por qué la feria de Almería es en agosto?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de las rutas de fiestas generados")
