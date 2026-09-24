#!/usr/bin/env python3
"""
Coleccionables de Jaén (medallón 120×124). Aro: oro = comunes; historia: mar = el preso,
arcilla = el pastor; gastronomía: mar = la plaza, arcilla = los baños.

Uso: python3 scripts/art/jaen_collectibles.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, frame, sparkle, write

BG = '<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
NIGHT = f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>'
OLIVE = "#6E7A3E"; OLIVED = "#4E5A2A"; OIL = "#C9B23A"; LIZ = "#5E8A4E"; LIZD = "#3F6A36"; STONE = "#E4D6BC"


def olive_branch(x, y, s=1.0, rot=0):
    leaves = "".join(f'<ellipse cx="{x + dx * s}" cy="{y + dy * s}" rx="{9 * s}" ry="{3.4 * s}" transform="rotate({r} {x + dx * s} {y + dy * s})" fill="{OLIVE}" stroke="{INK}" stroke-width="1"/>'
                     for dx, dy, r in [(-14, -4, -20), (-4, -10, -40), (8, -4, 20), (16, -12, -30), (22, -2, 30)])
    fruit = "".join(f'<ellipse cx="{x + dx * s}" cy="{y + dy * s}" rx="{4 * s}" ry="{5.4 * s}" fill="#3E4A2A" stroke="{INK}" stroke-width="1"/>' for dx, dy in [(-8, 4), (4, 4), (14, 6)])
    return f'<g transform="rotate({rot} {x} {y})"><path d="M{x - 24 * s} {y}Q{x} {y - 6 * s} {x + 28 * s} {y - 8 * s}" fill="none" stroke="#6E4C33" stroke-width="{2.4 * s}"/>{leaves}{fruit}</g>'


def lizard(x, y, s=1.0, c=LIZ, rot=-20):
    """Lagarto visto desde arriba: cola curva, cuerpo, cabeza y cuatro patas abiertas."""
    def leg(x0, y0, x1, y1, x2, y2):
        toes = "".join(f'<path d="M{x2} {y2}l{dx} {dy}" stroke="{INK}" stroke-width="2"/>' for dx, dy in [(-4, -3), (0, -5), (4, -3)])
        return f'<path d="M{x0} {y0}Q{x1} {y1} {x2} {y2}" fill="none" stroke="{INK}" stroke-width="8"/><path d="M{x0} {y0}Q{x1} {y1} {x2} {y2}" fill="none" stroke="{c}" stroke-width="4.6"/>' + toes
    body = (f'<path d="M0 22Q-6 44 -26 50Q-40 52 -44 40" fill="none" stroke="{INK}" stroke-width="10"/><path d="M0 22Q-6 44 -26 50Q-40 52 -44 40" fill="none" stroke="{c}" stroke-width="6.6"/>'
            + leg(-8, -10, -22, -14, -26, -26) + leg(8, -10, 22, -14, 26, -26) + leg(-8, 14, -22, 18, -26, 30) + leg(8, 14, 22, 18, 26, 30)
            + f'<ellipse cx="0" cy="2" rx="12" ry="24" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            + f'<ellipse cx="0" cy="-30" rx="9" ry="12" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            + f'<circle cx="-4" cy="-34" r="1.8" fill="{INK}"/><circle cx="4" cy="-34" r="1.8" fill="{INK}"/>'
            + "".join(f'<circle cx="{dx}" cy="{dy}" r="2.2" fill="{LIZD}"/>' for dx, dy in [(-4, -10), (4, -4), (-3, 6), (4, 14), (0, 20)]))
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{body}</g>'


farol = (NIGHT + "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="{PAPER}" opacity=".7"/>' for x, y in [(24, 30), (96, 26), (86, 50), (30, 60)])
         + f'<circle cx="60" cy="66" r="30" fill="{GOLD}" opacity=".2"/>'
         + f'<path d="M60 24V36" stroke="{INK}" stroke-width="3"/><path d="M48 36L60 28L72 36Z" fill="#2E3A48" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M46 36H74L70 88H50Z" fill="#FFE7A8" stroke="{INK}" stroke-width="2.4"/><path d="M60 36V88M48 60H72" stroke="#2E3A48" stroke-width="2"/>'
         f'<path d="M46 88H74V94H46Z" fill="#2E3A48" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M56 64Q60 54 64 64Q60 70 56 64Z" fill="{CLAY}"/>')

arco = (BG + f'<path d="M24 108V40H96V108Z" fill="{STONE}" stroke="{INK}" stroke-width="2.4"/>'
        f'<path d="M40 108V72Q60 46 80 72V108Z" fill="#5E4232" stroke="{INK}" stroke-width="2"/>'
        + "".join(f'<path d="M{24 + k * 12} 40V32H{32 + k * 12}V40" fill="{STONE}" stroke="{INK}" stroke-width="1.4"/>' for k in range(6))
        + f'<path d="M24 60H40M80 60H96" stroke="#C9B28A" stroke-width="2"/>')

panes = (BG + f'<path d="M20 86H100L94 100H26Z" fill="#8A6243" stroke="{INK}" stroke-width="2"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="11" fill="#D9A45E" stroke="{INK}" stroke-width="2"/><path d="M{x - 8} {y - 4}l6 7M{x + 2} {y - 6}l6 7" stroke="#A8743C" stroke-width="2"/>'
                   for x, y in [(40, 76), (80, 76), (60, 62)])
         + f'<path d="M78 40Q84 26 96 30" fill="none" stroke="#999" stroke-width="3" opacity=".7"/><circle cx="98" cy="30" r="5" fill="{INK}"/>'
         f'<path d="M100 26L106 20" stroke="{CLAY}" stroke-width="2"/>')

llaves = (BG + "".join(f'<g transform="rotate({r} 60 60)"><circle cx="60" cy="34" r="12" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="60" cy="34" r="12" fill="none" stroke="{c}" stroke-width="4"/>'
                       f'<path d="M60 46V94" stroke="{INK}" stroke-width="7"/><path d="M60 46V94" stroke="{c}" stroke-width="4"/>'
                       f'<path d="M60 84H72V90H66V96H60" fill="{c}" stroke="{INK}" stroke-width="1.6"/></g>' for r, c in [(-25, GOLD), (25, SILVER)])
          + sparkle(96, 34, 6))

zurron = (BG + f'<path d="M30 50H90L96 96Q60 108 24 96Z" fill="#9A6B45" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M30 50Q60 66 90 50L86 62Q60 76 34 62Z" fill="#7A5236" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M34 50Q40 22 60 20Q80 22 86 50" fill="none" stroke="#6E4C33" stroke-width="4"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#F2E3C4" stroke="{INK}" stroke-width="1"/>' for x, y in [(44, 84), (54, 88), (64, 86), (74, 84)])
          + f'<path d="M56 60Q60 48 64 60Q60 66 56 60Z" fill="{CLAY}"/><path d="M58 60Q60 54 62 60" fill="{GOLD}"/>')

espejo = ('<rect x="0" y="0" width="120" height="124" fill="#DCEBE6"/>'
          f'<circle cx="92" cy="28" r="10" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
          + "".join(f'<path d="M92 28L{92 + 20 * c:.0f} {28 + 20 * s:.0f}" stroke="{GOLD}" stroke-width="2"/>' for c, s in [(-1, 0), (-.7, .7), (0, 1), (-.9, .4)])
          + f'<path d="M36 36H74L78 90Q56 102 32 90Z" fill="{SILVER}" stroke="{INK}" stroke-width="2.4"/>'
          + "".join(f'<path d="M{x} {y}h10v10h-10Z" fill="#EAF4F8" stroke="{SILVERD}" stroke-width="1"/>' for x in (40, 52, 64) for y in (44, 58, 72))
          + f'<path d="M84 96L100 30" stroke="{INK}" stroke-width="6"/><path d="M84 96L100 30" stroke="#D9DEE4" stroke-width="3"/><path d="M78 88H92" stroke="{GOLD}" stroke-width="4"/>')

piel = (f'<rect x="0" y="0" width="120" height="124" fill="#E9D8B4"/>'
        + f'<path d="M60 14V26" stroke="{INK}" stroke-width="2"/><circle cx="60" cy="14" r="3" fill="{INK}"/>'
        + f'<path d="M50 26H70L78 44L72 70L80 96L64 108L60 118L56 108L40 96L48 70L42 44Z" fill="#6E7A4A" stroke="{INK}" stroke-width="2.2"/>'
        + "".join(f'<path d="M{50 + (k % 3) * 7} {34 + (k // 3) * 12}h6v6h-6Z" fill="#56603A" stroke="{INK}" stroke-width=".6"/>' for k in range(15))
        + f'<path d="M42 44L28 38M78 44L92 38M40 96L26 104M80 96L94 104" stroke="#6E7A4A" stroke-width="5"/>')

lagarto = (f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
           + f'<path d="M14 92H106V110H14Z" fill="#9FB6BF"/>'
           + lizard(64, 58, .74, rot=-30)
           + sparkle(94, 30, 6, GOLD))

# --- gastronomía ---
aceituna = (BG + olive_branch(58, 58, 1.6, -10)
            + f'<path d="M78 96Q70 84 78 72Q86 84 78 96Z" fill="{OIL}" stroke="{INK}" stroke-width="1.8"/>')

vara = ('<rect x="0" y="0" width="120" height="124" fill="#DCEBE6"/>'
        + f'<path d="M0 98H120V124H0Z" fill="#B9A06A"/>'
        + f'<path d="M50 100Q46 80 52 64" stroke="#6E4C33" stroke-width="6" fill="none"/>'
        + f'<circle cx="52" cy="46" r="26" fill="{OLIVE}"/><circle cx="36" cy="54" r="16" fill="{OLIVED}"/><circle cx="68" cy="54" r="16" fill="{OLIVED}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#2E3A1E"/>' for x, y in [(44, 40), (58, 36), (40, 58), (66, 48), (52, 60)])
        + f'<path d="M96 104L70 30" stroke="{INK}" stroke-width="6"/><path d="M96 104L70 30" stroke="#C9A77E" stroke-width="3"/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="4" fill="#2E3A1E"/>' for x, y in [(30, 84), (44, 90), (60, 80), (76, 92)]))

def plate(inner):
    return (BG + f'<ellipse cx="60" cy="72" rx="48" ry="26" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
            f'<ellipse cx="60" cy="70" rx="36" ry="17" fill="#F2E8D6" stroke="{INK}" stroke-width="1.4"/>' + inner)


pipirrana = plate("".join(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1.4" fill="{c}" stroke="{INK}" stroke-width=".8"/>'
                          for x, y, c in [(34, 62, "#D8412F"), (44, 70, "#4F8B5A"), (54, 60, "#D8412F"), (64, 72, "#F2E3C4"), (74, 62, "#4F8B5A"), (50, 76, "#F2C14E"), (80, 70, "#D8412F"), (40, 74, "#F2E3C4"), (62, 64, "#F2C14E")])
                  + f'<path d="M30 70Q60 84 90 70" fill="none" stroke="{OIL}" stroke-width="2" opacity=".7"/>')

andrajos = (BG + f'<path d="M16 56H104Q102 98 60 100Q18 98 16 56Z" fill="#8A5A3A" stroke="{INK}" stroke-width="2.4"/>'
            f'<ellipse cx="60" cy="56" rx="44" ry="12" fill="#C9763F" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x} {y}l10 -3l2 7l-11 2Z" fill="#F2E3C4" stroke="{INK}" stroke-width="1"/>' for x, y in [(30, 54), (48, 58), (64, 52), (80, 56), (40, 50)])
            + f'<path d="M86 22Q94 32 88 44M72 18Q80 28 74 40" fill="none" stroke="#CCC" stroke-width="3" opacity=".7"/>')

almazara = (BG + f'<path d="M20 100H100V86H20Z" fill="#B9A488" stroke="{INK}" stroke-width="2"/>'
            f'<ellipse cx="60" cy="86" rx="40" ry="10" fill="{STONE}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M60 86V24" stroke="#6E4C33" stroke-width="6"/><path d="M36 30H84" stroke="#6E4C33" stroke-width="5"/>'
            + "".join(f'<ellipse cx="{x}" cy="68" rx="10" ry="18" fill="#C9C0AE" stroke="{INK}" stroke-width="2"/>' for x in (44, 76))
            + f'<path d="M96 92Q104 100 100 108" stroke="{OIL}" stroke-width="4" fill="none"/><ellipse cx="100" cy="110" rx="8" ry="3" fill="{OIL}"/>')

ochio = (BG + f'<ellipse cx="60" cy="88" rx="44" ry="10" fill="{INK}" opacity=".12"/>'
         f'<path d="M22 76Q22 40 60 38Q98 40 98 76Q80 88 60 88Q40 88 22 76Z" fill="#E6B26A" stroke="{INK}" stroke-width="2.4"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#B8412A"/>' for x, y in [(40, 54), (52, 48), (66, 50), (78, 56), (46, 64), (60, 60), (74, 66), (56, 72), (36, 66), (84, 68)])
         + f'<path d="M30 60Q60 30 90 60" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')

alcuza = (BG + f'<path d="M36 100H84L80 50Q60 38 40 50Z" fill="#C9CED6" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M40 50Q60 38 80 50L76 40Q60 32 44 40Z" fill="#AEB5BF" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M78 58L104 32" stroke="{INK}" stroke-width="5"/><path d="M78 58L104 32" stroke="#C9CED6" stroke-width="2.6"/>'
          f'<path d="M36 64Q20 64 22 80Q24 92 38 90" fill="none" stroke="{INK}" stroke-width="4"/>'
          f'<path d="M40 76H80V96H40Z" fill="{OIL}" opacity=".6"/>' + olive_branch(60, 22, .7, 0))

olivos = ('<rect x="0" y="0" width="120" height="124" fill="#F3D9A8"/>'
          + f'<circle cx="86" cy="34" r="12" fill="#FFF3C4"/>'
          + "".join(f'<path d="M-10 {y}Q30 {y - 10} 60 {y - 2}T130 {y - 6}V124H-10Z" fill="{c}"/>' for y, c in [(62, "#C9B07A"), (78, "#B89C62"), (94, "#A58A52")])
          + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{OLIVE}"/><path d="M{x} {y + r}V{y + r + 4}" stroke="#6E4C33" stroke-width="1.6"/>'
                    for y, r, step in [(58, 3.4, 12), (74, 4.4, 15), (90, 5.6, 19), (108, 7, 24)] for x in range(6 + (int(y) % 7), 120, step))
          + sparkle(26, 30, 6, GOLD))

ART = {
    "jaen_farol": (GOLD, farol, "El farol del sereno"),
    "jaen_arco": (GOLD, arco, "El arco de San Lorenzo"),
    "jaen_panes": (SEA, panes, "Los panes del preso"),
    "jaen_llaves": (SEA, llaves, "Las llaves del Santo Reino"),
    "jaen_zurron": (CLAY, zurron, "El zurrón del pastor"),
    "jaen_espejo": (CLAY, espejo, "La armadura de espejos"),
    "jaen_piel": (GOLD, piel, "La piel del caimán"),
    "jaen_lagarto": (GOLD, lagarto, "¿Quién mató al lagarto de la Malena?"),
    "jaen_aceituna": (GOLD, aceituna, "La aceituna"),
    "jaen_vara": (GOLD, vara, "La vara del vareador"),
    "jaen_pipirrana": (SEA, pipirrana, "La pipirrana"),
    "jaen_andrajos": (SEA, andrajos, "Los andrajos"),
    "jaen_almazara": (CLAY, almazara, "La almazara"),
    "jaen_ochio": (CLAY, ochio, "El ochío"),
    "jaen_alcuza": (GOLD, alcuza, "La alcuza"),
    "jaen_olivos": (GOLD, olivos, "¿Quién plantó el mar de olivos?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Jaén generados")
