#!/usr/bin/env python3
"""
Coleccionables de las rutas gastronómicas de Málaga (espeto), Sevilla (azahar) y Granada (pionono).
Medallón 120×124. Aro: oro = comunes; mar = primer camino (dinero), arcilla = segundo (poder).

Uso: python3 scripts/art/gastro_andalucia_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, PURPLE, frame, sparkle, waves, write

BG = '<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
SKY = f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
ORANGE = "#F29A2E"; ORANGED = "#C9741C"; LEAF = "#4F8B5A"; SARD = "#8FA3AE"; RED = "#D8412F"


def sardine(x, y, s=1.0, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x - 22 * s} {y}Q{x - 4 * s} {y - 9 * s} {x + 16 * s} {y}Q{x - 4 * s} {y + 9 * s} {x - 22 * s} {y}Z" fill="{SARD}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x + 14 * s} {y}L{x + 24 * s} {y - 7 * s}V{y + 7 * s}Z" fill="{SARD}" stroke="{INK}" stroke-width="1.4"/>'
            f'<path d="M{x - 18 * s} {y - 1 * s}Q{x - 2 * s} {y - 6 * s} {x + 12 * s} {y - 1 * s}" fill="none" stroke="#5E7A8A" stroke-width="1.2"/>'
            f'<circle cx="{x - 16 * s}" cy="{y - 1.5 * s}" r="{1.4 * s}" fill="{INK}"/></g>')


def orange(x, y, r=12, leaf=True):
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{ORANGE}" stroke="{INK}" stroke-width="2"/><circle cx="{x - r * .35}" cy="{y - r * .35}" r="{r * .22}" fill="#FFF" opacity=".35"/>'
    if leaf:
        out += f'<path d="M{x} {y - r}Q{x + r * .8} {y - r * 1.8} {x + r * 1.3} {y - r * 1.1}Q{x + r * .6} {y - r * .6} {x} {y - r}Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.2"/>'
    return out


def blossom(x, y, s=1.0):
    petals = "".join(f'<ellipse cx="{x + 7 * s * math.cos(math.radians(a)):.1f}" cy="{y + 7 * s * math.sin(math.radians(a)):.1f}" rx="{5 * s}" ry="{3.4 * s}" transform="rotate({a} {x + 7 * s * math.cos(math.radians(a)):.1f} {y + 7 * s * math.sin(math.radians(a)):.1f})" fill="{WHITE}" stroke="{INK}" stroke-width="1"/>' for a in range(-90, 270, 72))
    return petals + f'<circle cx="{x}" cy="{y}" r="{3 * s}" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>'


def plate(y=76, rx=46, ry=14):
    return f'<ellipse cx="60" cy="{y}" rx="{rx}" ry="{ry}" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'


# --- Málaga -----------------------------------------------------------------
m_sardina = (SKY + waves(92) + sardine(58, 56, 1.8, -10))

m_pasa = (BG + f'<path d="M14 88H106" stroke="{WOOD}" stroke-width="5"/>'
          + "".join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="5" fill="#6E3A52" stroke="{INK}" stroke-width="1.2"/><path d="M{x - 2} {y - 2}q2 -2 4 0" stroke="#A56A82" stroke-width="1.2" fill="none"/>'
                    for x, y in [(34, 78), (46, 80), (58, 78), (70, 80), (82, 78), (40, 70), (52, 70), (64, 70), (76, 70), (46, 62), (58, 62), (70, 62), (58, 54)])
          + f'<path d="M58 50V36M58 40Q70 30 80 38Q70 44 58 40Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.4"/>' + sparkle(92, 32, 6, GOLD))

m_jabega = (SKY + waves(84)
            + f'<path d="M14 72Q60 88 106 72L98 86Q60 96 22 86Z" fill="{SEA}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M16 72Q60 86 104 72" fill="none" stroke="{PAPER}" stroke-width="2"/>'
            f'<path d="M100 72L110 50L104 74Z" fill="{SEA}" stroke="{INK}" stroke-width="1.6"/>'
            f'<ellipse cx="92" cy="78" rx="5" ry="3.4" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/><circle cx="92" cy="78" r="1.8" fill="{INK}"/>'
            f'<path d="M40 72L30 40M60 76L64 38" stroke="#B07A45" stroke-width="3"/>')

m_espeto = ('<rect x="0" y="0" width="120" height="124" fill="#F3D9A8"/>'
            + f'<path d="M0 88H120V124H0Z" fill="#E6C98E"/>'
            + f'<path d="M20 96Q60 110 100 96L94 108Q60 116 26 108Z" fill="#7A5236" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>' for x, y, c in [(40, 98, "#E8744A"), (54, 100, GOLD), (68, 100, "#E8744A"), (82, 98, GOLD)])
            + f'<path d="M36 100L78 18" stroke="{INK}" stroke-width="5"/><path d="M36 100L78 18" stroke="#C9A96A" stroke-width="3"/>'
            + "".join(sardine(52 + k * 7, 70 - k * 14, .8, -63) for k in range(4))
            + "".join(f'<path d="M{x} 86Q{x - 4} 76 {x + 2} 68" fill="none" stroke="#CCC" stroke-width="2.4" opacity=".7"/>' for x in (86, 96)))

m_vino = (BG + f'<path d="M50 20H70V36Q84 44 84 62V100H36V62Q36 44 50 36Z" fill="#5A2A2E" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M48 16H72V24H48Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M42 62H78V84H42Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
          f'<text x="60" y="77" font-family="Georgia, serif" font-size="7.5" font-weight="700" text-anchor="middle" fill="{CLAY}">MÁLAGA</text>'
          f'<path d="M44 44Q48 40 54 40" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')

m_garum = (BG + f'<path d="M48 22H72V30Q88 42 86 64Q84 86 60 102Q36 86 34 64Q32 42 48 30Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
           f'<path d="M48 30Q36 28 36 42M72 30Q84 28 84 42" fill="none" stroke="{INK}" stroke-width="3"/>'
           + sardine(60, 62, .9, 0) + f'<path d="M40 50Q60 56 80 50" fill="none" stroke="#9A5A2E" stroke-width="2"/>')

m_cafe = (BG + f'<ellipse cx="60" cy="96" rx="36" ry="8" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M34 44H86V70Q86 92 60 92Q34 92 34 70Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M86 52Q102 52 100 66Q98 78 84 76" fill="none" stroke="{INK}" stroke-width="3"/>'
          f'<ellipse cx="60" cy="44" rx="26" ry="6" fill="#8A5A3A" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M36 44Q60 56 84 44" fill="#E9DCC0" opacity=".7"/>'
          + "".join(f'<path d="M{x} 34Q{x - 4} 26 {x + 2} 18" fill="none" stroke="#BBB" stroke-width="2.4" opacity=".7"/>' for x in (50, 62, 74)))

m_insignia = (f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>' + waves(90, SEA, "#2F6F73")
              + f'<path d="M26 90L84 22" stroke="{INK}" stroke-width="6"/><path d="M26 90L84 22" stroke="#C9A96A" stroke-width="3.4"/>'
              + "".join(sardine(44 + k * 9, 66 - k * 11, .85, -50) for k in range(4))
              + f'<circle cx="92" cy="30" r="10" fill="#FFF3C4"/>' + sparkle(24, 32, 6, GOLD))

# --- Sevilla ----------------------------------------------------------------
s_naranja = (BG + orange(60, 64, 30) + blossom(28, 34, 1.1))

s_aceitunas = (BG + f'<path d="M18 56H102Q100 94 60 96Q20 94 18 56Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
               f'<ellipse cx="60" cy="56" rx="42" ry="11" fill="#9A5A2E" stroke="{INK}" stroke-width="2"/>'
               + "".join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="7.5" fill="#7C8A4A" stroke="{INK}" stroke-width="1.2"/><circle cx="{x - 2}" cy="{y - 3}" r="1.4" fill="#FFF" opacity=".5"/>' for x, y in [(34, 52), (46, 48), (58, 50), (70, 47), (82, 52), (40, 58), (64, 58), (76, 58)])
               + f'<path d="M86 30L94 18M92 34L104 26" stroke="{LEAF}" stroke-width="2.4"/><circle cx="30" cy="30" r="5" fill="{ORANGE}" stroke="{INK}" stroke-width="1"/>')

s_mermelada = (BG + f'<path d="M36 40H84V96Q60 104 36 96Z" fill="#E8812E" stroke="{INK}" stroke-width="2.4"/>'
               f'<path d="M32 28H88V40H32Z" fill="#C0476A" stroke="{INK}" stroke-width="2"/>'
               + "".join(f'<path d="M{32 + k * 8} 28V40" stroke="{PAPER}" stroke-width="1.6"/>' for k in range(8))
               + f'<path d="M44 56H76V80H44Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
               + orange(60, 68, 7, False) + f'<path d="M40 48Q44 44 50 44" fill="none" stroke="#FFF" stroke-width="2" opacity=".4"/>')

s_naranjo = (f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
             + f'<path d="M0 96H120V124H0Z" fill="#D9C39E"/>'
             + f'<path d="M56 100V70H64V100Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.6"/>'
             + f'<circle cx="60" cy="50" r="28" fill="{LEAF}" stroke="{INK}" stroke-width="2"/><circle cx="40" cy="60" r="14" fill="#3D6647"/><circle cx="80" cy="60" r="14" fill="#3D6647"/>'
             + "".join(orange(x, y, 4.5, False) for x, y in [(48, 40), (66, 36), (74, 52), (54, 58), (40, 60), (80, 62)])
             + f'<path d="M50 30L54 14L60 24L66 14L70 30Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>')

s_aguazahar = (BG + f'<path d="M50 30H70V42Q86 50 86 70Q86 96 60 98Q34 96 34 70Q34 50 50 42Z" fill="#DDEFF0" fill-opacity=".85" stroke="{INK}" stroke-width="2.4"/>'
               f'<path d="M48 22H72V30H48Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>'
               f'<path d="M36 72Q60 80 84 72V74Q84 96 60 96Q36 96 36 74Z" fill="#BFE0E4" opacity=".8"/>'
               + blossom(60, 68, 1.2) + blossom(92, 32, .8))

s_patio = ('<rect x="0" y="0" width="120" height="124" fill="#F3D9A8"/>'
           + "".join(f'<path d="M{x} 66V40Q{x + 13} 26 {x + 26} 40V66" fill="#E6C9A0" stroke="{INK}" stroke-width="1.6"/>' for x in (6, 34, 62, 90))
           + f'<path d="M0 66H120V124H0Z" fill="#DCC3A0"/>'
           + "".join(f'<path d="M{x} 104V84" stroke="#6E4C33" stroke-width="3"/><circle cx="{x}" cy="78" r="12" fill="{LEAF}" stroke="{INK}" stroke-width="1.4"/>'
                     + orange(x - 4, 76, 3, False) + orange(x + 5, 80, 3, False) for x in (26, 60, 94))
           + f'<path d="M20 108Q60 100 100 108" fill="none" stroke="#8FB9B4" stroke-width="4"/>')

s_tapa = (BG + plate(80, 44, 14)
          + f'<ellipse cx="46" cy="74" rx="16" ry="6" fill="#E8C872" stroke="{INK}" stroke-width="1.4"/>'
          + "".join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="5" fill="#7C8A4A" stroke="{INK}" stroke-width=".8"/>' for x, y in [(70, 72), (78, 76), (74, 80)])
          + f'<path d="M58 52H86V60H58Z" fill="#A8432F" stroke="{INK}" stroke-width="1.4"/>'
          f'<path d="M26 44L42 68" stroke="#C9A96A" stroke-width="2"/>' + sparkle(94, 30, 6, GOLD))

s_insignia = (f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>'
              + "".join(blossom(x, y, s) for x, y, s in [(34, 40, 1.1), (84, 34, .9), (60, 70, 1.4), (30, 86, .8), (90, 84, 1)])
              + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{PAPER}" opacity=".7"/>' for x, y in [(20, 20), (100, 56), (50, 100), (70, 22)]))

# --- Granada ----------------------------------------------------------------
g_especias = (BG + "".join(f'<path d="M{x - 16} 96Q{x - 20} 60 {x - 10} 54H{x + 10}Q{x + 20} 60 {x + 16} 96Z" fill="#E9DCC0" stroke="{INK}" stroke-width="2"/>'
                           f'<ellipse cx="{x}" cy="56" rx="12" ry="5" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                           f'<path d="M{x - 12} {56}Q{x} {44} {x + 12} {56}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
                           for x, c in [(32, "#D98A2E"), (60, "#B8412A"), (88, "#C9B23A")])
              + f'<path d="M50 30L54 24L58 30M66 28L70 22L74 28" fill="none" stroke="{RED}" stroke-width="2"/>')

g_churros = (BG + f'<path d="M22 76Q60 90 98 76L92 98Q60 106 28 98Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{x} 78Q{x + 8} 44 {x + 30} 30" fill="none" stroke="{INK}" stroke-width="9"/><path d="M{x} 78Q{x + 8} 44 {x + 30} 30" fill="none" stroke="#E0A04A" stroke-width="6"/>' for x in (30, 44))
             + f'<path d="M72 60H98V86Q98 94 85 94Q72 94 72 86Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><ellipse cx="85" cy="60" rx="13" ry="4" fill="#4A2A1A" stroke="{INK}" stroke-width="1.4"/>'
             + f'<path d="M98 66Q108 68 104 78Q100 84 96 82" fill="none" stroke="{INK}" stroke-width="2.4"/>')

g_seda = (BG + "".join(f'<path d="M{x} 20V100" stroke="{WOOD}" stroke-width="4"/>' for x in (22, 98))
          + f'<path d="M18 22H102" stroke="{WOOD}" stroke-width="5"/>'
          + "".join(f'<path d="M{x} 24Q{x + 4} 60 {x - 2} 100H{x + 16}Q{x + 20} 60 {x + 16} 24Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
                    for x, c in [(28, "#C0476A"), (46, GOLD), (64, SEA), (80, PURPLE)])
          + "".join(f'<path d="M{x + 4} {y}l4 4l4 -4" fill="none" stroke="{PAPER}" stroke-width="1.2"/>' for x in (28, 46, 64, 80) for y in (44, 70)))

g_alhondiga = ('<rect x="0" y="0" width="120" height="124" fill="#E9D3AE"/>'
               + f'<path d="M20 108V34H100V108Z" fill="#D9B98A" stroke="{INK}" stroke-width="2.4"/>'
               + f'<path d="M36 108V60Q60 30 84 60V108Z" fill="#5E4232" stroke="{INK}" stroke-width="2"/>'
               + f'<path d="M36 60Q60 30 84 60" fill="none" stroke="#C9A77E" stroke-width="5"/>'
               + "".join(f'<path d="M{44 + k * 8} {54 - (3 - abs(k - 2)) * 3}l3 5l3 -5" fill="none" stroke="#F2E3C4" stroke-width="1.4"/>' for k in range(5))
               + f'<path d="M26 44H94" stroke="#B8986A" stroke-width="3"/>')

g_torno = ('<rect x="0" y="0" width="120" height="124" fill="#E9DCC0"/>'
           + f'<path d="M0 0H120V124H0Z" fill="#DCCFB6"/>'
           + f'<circle cx="60" cy="64" r="34" fill="#8A6243" stroke="{INK}" stroke-width="2.6"/>'
           + f'<path d="M26 64H94" stroke="{INK}" stroke-width="2"/><path d="M60 30V98" stroke="{INK}" stroke-width="2" opacity=".4"/>'
           + f'<path d="M34 64Q34 38 60 36Q86 38 86 64Z" fill="#A87A52" stroke="{INK}" stroke-width="1.6"/>'
           + f'<path d="M44 58H76V64H44Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
           + "".join(f'<circle cx="{x}" cy="54" r="4" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for x in (50, 60, 70)))

g_yemas = (BG + plate(80, 44, 14)
           + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#F2B233" stroke="{INK}" stroke-width="1.6"/><circle cx="{x - 3}" cy="{y - 3}" r="2" fill="#FFF3C4"/>'
                     for x, y in [(40, 74), (60, 72), (80, 74), (50, 62), (70, 62), (60, 52)])
           + sparkle(96, 32, 6, GOLD))

g_remojon = (BG + plate(78, 46, 16)
             + "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="{ORANGE}" stroke="{INK}" stroke-width="1.2"/>'
                       + "".join(f'<path d="M{x} {y}L{x + 7 * math.cos(math.radians(a)):.1f} {y + 7 * math.sin(math.radians(a)):.1f}" stroke="#FCE0B0" stroke-width="1"/>' for a in range(0, 360, 60))
                       for x, y in [(40, 74), (60, 70), (80, 76)])
             + "".join(f'<path d="M{x} {y}h10v4h-10Z" fill="{PAPER}" stroke="{INK}" stroke-width=".8"/>' for x, y in [(46, 82), (66, 80)])
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="4" fill="#3E3A2A"/>' for x, y in [(52, 66), (72, 68), (34, 82), (88, 70)]))

g_pionono = ('<rect x="0" y="0" width="120" height="124" fill="#F3E3C8"/>'
             + f'<path d="M34 58H86L82 100H38Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
             + "".join(f'<path d="M{x} 60L{x + 2} 98" stroke="#E6D8BE" stroke-width="1.4"/>' for x in range(40, 84, 6))
             + f'<path d="M40 60V36H80V60Z" fill="#E6B26A" stroke="{INK}" stroke-width="2.2"/>'
             + "".join(f'<path d="M40 {y}Q60 {y + 5} 80 {y}" fill="none" stroke="#C98E3E" stroke-width="1.6"/>' for y in (44, 52))
             + f'<ellipse cx="60" cy="34" rx="22" ry="8" fill="#B8742E" stroke="{INK}" stroke-width="2"/>'
             + f'<ellipse cx="56" cy="31" rx="8" ry="2.6" fill="#E8A860" opacity=".8"/>' + sparkle(96, 26, 6, GOLD))

ART = {
    "malaga_sardina": (GOLD, m_sardina, "La sardina"),
    "malaga_pasa": (GOLD, m_pasa, "La pasa moscatel"),
    "malaga_jabega": (SEA, m_jabega, "La jábega"),
    "malaga_espeto": (SEA, m_espeto, "El espeto"),
    "malaga_vino": (CLAY, m_vino, "El vino de Málaga"),
    "malaga_garum": (CLAY, m_garum, "El ánfora de garum"),
    "malaga_cafe": (GOLD, m_cafe, "El café de nueve nombres"),
    "malaga_espeto_insignia": (GOLD, m_insignia, "¿Quién inventó el espeto?"),
    "sevilla_naranja": (GOLD, s_naranja, "La naranja amarga"),
    "sevilla_aceitunas": (GOLD, s_aceitunas, "Las aceitunas aliñadas"),
    "sevilla_mermelada": (SEA, s_mermelada, "La mermelada"),
    "sevilla_naranjo": (SEA, s_naranjo, "El naranjo del rey"),
    "sevilla_aguazahar": (CLAY, s_aguazahar, "El agua de azahar"),
    "sevilla_patio": (CLAY, s_patio, "El Patio de los Naranjos"),
    "sevilla_tapa": (GOLD, s_tapa, "La tapa"),
    "sevilla_azahar": (GOLD, s_insignia, "¿Por qué Sevilla huele a azahar?"),
    "granada_especias": (GOLD, g_especias, "Las especias"),
    "granada_churros": (GOLD, g_churros, "Churros con chocolate"),
    "granada_seda": (SEA, g_seda, "La seda de la Alcaicería"),
    "granada_alhondiga": (SEA, g_alhondiga, "La alhóndiga"),
    "granada_torno": (CLAY, g_torno, "El torno"),
    "granada_yemas": (CLAY, g_yemas, "Las yemas"),
    "granada_remojon": (GOLD, g_remojon, "El remojón"),
    "granada_pionono": (GOLD, g_pionono, "¿Quién inventó el pionono?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables gastronómicos de Málaga, Sevilla y Granada generados")
