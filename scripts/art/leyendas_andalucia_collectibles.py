#!/usr/bin/env python3
"""
Coleccionables de las rutas de leyendas de las ocho ciudades.
Medallón 120×124. Aro: oro = comunes; mar = primer camino (dinero), arcilla = segundo (poder).
Las insignias van de noche, con luna, como la seña de la categoría.

Uso: python3 scripts/art/leyendas_andalucia_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, PURPLE, sparkle, waves, write
from fiestas_andalucia_collectibles import BG, SKY, NIGHT, RED, LEAF, doc, burst, flame, castanet

STONE = "#BDB6A8"; STONED = "#8C8579"; BLUE = "#3A6EA5"


def moon(x=92, y=28, r=10):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF3C4"/>'
            f'<circle cx="{x + r * .45}" cy="{y - r * .25}" r="{r * .85}" fill="{NAVY}"/>')


def stars(pts):
    return "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="{PAPER}" opacity=".8"/>' for x, y in pts)


def night(*art):
    return NIGHT + stars([(20, 40), (34, 22), (100, 60), (70, 18), (24, 76)]) + moon() + "".join(art)


def stone_head(x, y, s=1.0, c=STONE):
    return (f'<circle cx="{x}" cy="{y}" r="{18 * s}" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x - 16 * s} {y - 4 * s}Q{x} {y - 26 * s} {x + 16 * s} {y - 4 * s}" fill="{STONED}"/>'
            f'<circle cx="{x - 6 * s}" cy="{y + 1 * s}" r="{1.8 * s}" fill="{INK}"/><circle cx="{x + 6 * s}" cy="{y + 1 * s}" r="{1.8 * s}" fill="{INK}"/>'
            f'<path d="M{x - 5 * s} {y + 9 * s}H{x + 5 * s}" stroke="{INK}" stroke-width="{1.6 * s}"/>')


def book(x, y, c=CLAY):
    return (f'<path d="M{x - 24} {y}L{x} {y + 6}L{x + 24} {y}V{y + 30}L{x} {y + 36}L{x - 24} {y + 30}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x} {y + 6}V{y + 36}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<path d="M{x - 20} {y + 8 + k * 6}L{x - 4} {y + 12 + k * 6}M{x + 4} {y + 12 + k * 6}L{x + 20} {y + 8 + k * 6}" stroke="#C9B48A" stroke-width="1.2"/>' for k in range(3))
            + f'<path d="M{x - 26} {y + 30}L{x} {y + 38}L{x + 26} {y + 30}" fill="none" stroke="{c}" stroke-width="3"/>')


def quill(x, y):
    return (f'<path d="M{x} {y}Q{x + 18} {y - 30} {x + 34} {y - 44}Q{x + 26} {y - 18} {x + 4} {y + 2}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x} {y}L{x - 6} {y + 10}" stroke="{INK}" stroke-width="2"/>')


def lamp(x, y, s=1.0):
    return (f'<path d="M{x - 16 * s} {y}Q{x} {y + 12 * s} {x + 16 * s} {y}L{x + 24 * s} {y - 4 * s}Q{x + 8 * s} {y - 8 * s} {x - 16 * s} {y - 6 * s}Z" fill="{GOLDD}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x - 18 * s} {y - 4 * s}Q{x - 28 * s} {y - 4 * s} {x - 26 * s} {y + 6 * s}" fill="none" stroke="{INK}" stroke-width="2"/>'
            + flame(x + 22 * s, y - 6 * s, .5 * s))


def sword(x1, y1, x2, y2):
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{INK}" stroke-width="6"/><path d="M{x1} {y1}L{x2} {y2}" stroke="{SILVER}" stroke-width="3.4"/>'
            f'<path d="M{x1 - 10} {y1 + 6}L{x1 + 10} {y1 - 6}" stroke="{GOLDD}" stroke-width="5"/><circle cx="{x1 - (x2 - x1) * .12}" cy="{y1 - (y2 - y1) * .12}" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')


# --- Málaga -----------------------------------------------------------------
m = {
    "farol": night(f'<path d="M60 100V56" stroke="{INK}" stroke-width="4"/><path d="M48 56H72L68 30H52Z" fill="#FFE7A8" stroke="{INK}" stroke-width="2"/>'
                   f'<path d="M46 30H74L60 20Z" fill="{INK}"/><circle cx="60" cy="44" r="18" fill="#FFE7A8" opacity=".25"/>'),
    "sombrero": BG + f'<ellipse cx="60" cy="76" rx="42" ry="12" fill="{INK}" stroke="{INK}" stroke-width="2"/><path d="M40 74Q40 40 60 40Q80 40 80 74Z" fill="#2B2A33" stroke="{INK}" stroke-width="2"/>'
                     f'<path d="M78 50Q100 30 96 60Q90 50 78 56Z" fill="{RED}" stroke="{INK}" stroke-width="1.6"/>',
    "vara": BG + f'<path d="M40 104L80 20" stroke="{INK}" stroke-width="7"/><path d="M40 104L80 20" stroke="{WOOD}" stroke-width="4"/><circle cx="80" cy="20" r="7" fill="{SILVER}" stroke="{INK}" stroke-width="2"/>'
                 f'<path d="M44 96L50 100M48 88L54 92" stroke="{SILVER}" stroke-width="2.4"/>',
    "carta": BG + f'<path d="M24 36H96V88H24Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/><path d="M24 36L60 64L96 36" fill="none" stroke="{INK}" stroke-width="2"/>'
                  f'<circle cx="60" cy="66" r="9" fill="{RED}" stroke="{INK}" stroke-width="1.8"/><path d="M56 66H64M60 62V70" stroke="{GOLD}" stroke-width="1.6"/>',
    "cabeza": BG + f'<path d="M22 30H98V100H22Z" fill="#E9DCC0" stroke="{INK}" stroke-width="2"/>' + stone_head(60, 64, 1.4) + sparkle(94, 26, 5, GOLD),
    "insignia": night("".join(stone_head(x, y, .55) for x, y in [(30, 60), (46, 52), (60, 48), (74, 52), (90, 60), (42, 78), (78, 78)])),
}
# --- Sevilla ----------------------------------------------------------------
s = {
    "pluma": BG + quill(40, 90) + f'<path d="M60 100H100" stroke="{INK}" stroke-width="2"/>' + f'<path d="M28 100Q40 94 50 100" fill="none" stroke="{INK}" stroke-width="2"/>',
    "candil": night(lamp(52, 78, 1.4)),
    "rodillas": BG + "".join(f'<path d="M{x} 30V60Q{x} 70 {x + 6} 74L{x + 2} 102" fill="none" stroke="{INK}" stroke-width="12"/><path d="M{x} 30V60Q{x} 70 {x + 6} 74L{x + 2} 102" fill="none" stroke="#7A2335" stroke-width="8"/>' for x in (44, 74))
                    + "".join(f'<path d="M{x} {y}l6 -4M{x + 2} {y + 6}l7 0" stroke="{GOLD}" stroke-width="2.4"/>' for x, y in [(54, 66), (84, 66)]),
    "espada": BG + sword(36, 94, 90, 22),
    "busto": night(f'<path d="M30 104V40H90V104" fill="#4A4A55" stroke="{INK}" stroke-width="2"/><path d="M36 104V48Q60 30 84 48V104Z" fill="#2B2A33"/>'
                   + stone_head(60, 70, 1.1) + f'<path d="M46 56L50 46L56 54L60 44L64 54L70 46L74 56Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'),
    "insignia": night(stone_head(60, 70, 1.1), f'<path d="M46 56L50 46L56 54L60 44L64 54L70 46L74 56Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>', lamp(30, 96, .7)),
}
# --- Granada ----------------------------------------------------------------
g = {
    "libro": BG + book(60, 42, SEA) + f'<text x="60" y="34" font-family="Georgia, serif" font-weight="700" font-size="11" text-anchor="middle" fill="{INK}">GRANADA</text>',
    "estrella": NIGHT + "".join(f'<path d="M{x} {y - 10}L{x + 3} {y - 3}L{x + 10} {y}L{x + 3} {y + 3}L{x} {y + 10}L{x - 3} {y + 3}L{x - 10} {y}L{x - 3} {y - 3}Z" fill="#FFE7A8" stroke="{INK}" stroke-width="1"/>'
                                for x, y in [(40, 44), (80, 44), (60, 64), (40, 84), (80, 84)]),
    "lluvia": SKY + f'<path d="M24 56Q60 16 96 56Z" fill="{INK}" stroke="{INK}" stroke-width="2"/><path d="M60 56V96Q60 104 52 102" fill="none" stroke="{INK}" stroke-width="3"/>'
                    + "".join(f'<path d="M{x} {y}l-4 10" stroke="{BLUE}" stroke-width="2.4"/>' for x, y in [(28, 64), (40, 76), (88, 66), (78, 80), (96, 84), (24, 90)]) + waves(98),
    "sello": BG + f'<circle cx="60" cy="62" r="30" fill="{RED}" stroke="{INK}" stroke-width="2.4"/><circle cx="60" cy="62" r="22" fill="none" stroke="#F2B4A8" stroke-width="2"/>'
                  f'<text x="60" y="70" font-family="Georgia, serif" font-weight="700" font-size="22" text-anchor="middle" fill="{PAPER}">Z</text>',
    "fenix": BG + f'<path d="M60 96Q40 80 30 50Q46 62 52 58Q44 40 50 24Q58 44 60 50Q62 44 70 24Q76 40 68 58Q74 62 90 50Q80 80 60 96Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
                  + flame(60, 104, .7),
    "insignia": night(f'<path d="M34 104V38H86V104" fill="#E9DCC0" stroke="{INK}" stroke-width="2"/><path d="M42 50H78V90H42Z" fill="#B5553A" stroke="{INK}" stroke-width="1.6"/>'
                      + "".join(f'<path d="M42 {y}H78" stroke="#8A3E2A" stroke-width="1.2"/>' for y in range(58, 90, 8)),
                      f'<path d="M60 44Q54 38 60 32Q66 38 60 44Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'),
}
# --- Córdoba ----------------------------------------------------------------
c = {
    "reloj": BG + f'<circle cx="60" cy="60" r="30" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>'
                  + "".join(f'<circle cx="{60 + 24 * math.cos(math.radians(a)):.1f}" cy="{60 + 24 * math.sin(math.radians(a)):.1f}" r="1.8" fill="{INK}"/>' for a in range(0, 360, 30))
                  + f'<path d="M60 60V42M60 60L72 66" stroke="{INK}" stroke-width="2.6"/><path d="M84 88Q96 70 88 60L92 58Q104 72 90 92Z" fill="{WOODL}" stroke="{INK}" stroke-width="1.6"/>',
    "romance": BG + doc("1448", 60, PURPLE),
    "comedia": BG + f'<path d="M26 40Q40 30 54 40Q56 66 40 74Q24 66 26 40Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M66 50Q80 40 94 50Q96 76 80 84Q64 76 66 50Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>'
                    f'<path d="M34 50h4M44 50h4M34 62Q40 58 46 62" fill="none" stroke="{INK}" stroke-width="2"/><path d="M74 60h4M84 60h4M74 72Q80 76 86 72" fill="none" stroke="{PAPER}" stroke-width="2"/>',
    "almena": SKY + f'<path d="M24 100V46H40V36H52V46H68V36H80V46H96V100Z" fill="#E3B96F" stroke="{INK}" stroke-width="2.2"/>'
                    + "".join(f'<path d="M24 {y}H96" stroke="#C99B50" stroke-width="1.2"/>' for y in range(56, 100, 10)),
    "torre": night(f'<path d="M44 106V44H76V106Z" fill="#E3B96F" stroke="{INK}" stroke-width="2"/><path d="M40 44H80V36H40Z" fill="#E3B96F" stroke="{INK}" stroke-width="2"/>'
                   + "".join(f'<path d="M{x} 36V30H{x + 6}V36" fill="#E3B96F" stroke="{INK}" stroke-width="1.4"/>' for x in (42, 52, 62, 72))
                   + f'<path d="M76 90Q96 90 100 106" fill="none" stroke="#E3B96F" stroke-width="8"/><path d="M58 70h4v10h-4Z" fill="{INK}"/>'),
    "insignia": night(f'<path d="M48 106V50H72V106Z" fill="#E3B96F" stroke="{INK}" stroke-width="2"/><path d="M44 50H76V42H44Z" fill="#E3B96F" stroke="{INK}" stroke-width="2"/>', quill(22, 96)),
}
# --- Cádiz ------------------------------------------------------------------
k = {
    "escudo": BG + f'<path d="M34 26H86V64Q86 94 60 104Q34 94 34 64Z" fill="{SEAT}" stroke="{INK}" stroke-width="2.4"/>'
                   f'<path d="M60 40V86M50 50H70" stroke="{INK}" stroke-width="3"/><circle cx="60" cy="38" r="6" fill="#D9A07A" stroke="{INK}" stroke-width="1.4"/>'
                   f'<path d="M40 70Q46 60 52 70Q46 76 40 70ZM68 70Q74 60 80 70Q74 76 68 70Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>',
    "bueyes": BG + "".join(f'<path d="M{x - 16} 90V70Q{x - 16} 58 {x} 58Q{x + 16} 58 {x + 16} 70V90" fill="#8A3E2A" stroke="{INK}" stroke-width="2"/>'
                           f'<path d="M{x - 18} 60Q{x - 26} 50 {x - 22} 44M{x + 18} 60Q{x + 26} 50 {x + 22} 44" fill="none" stroke="{PAPER}" stroke-width="3"/>'
                           f'<circle cx="{x - 5}" cy="68" r="1.8" fill="{INK}"/><circle cx="{x + 5}" cy="68" r="1.8" fill="{INK}"/>' for x in (40, 80)),
    "flecha": SKY + f'<path d="M22 98L94 26" stroke="{INK}" stroke-width="4"/><path d="M94 26L80 30L90 40Z" fill="{SILVER}" stroke="{INK}" stroke-width="1.6"/>'
                    f'<path d="M22 98L18 84M22 98L36 102M28 92L24 80M28 92L40 96" stroke="{RED}" stroke-width="3"/>',
    "anfora": BG + f'<path d="M52 24H68V32Q84 40 80 72Q76 96 60 106Q44 96 40 72Q36 40 52 32Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>'
                   f'<path d="M52 32Q40 30 42 44M68 32Q80 30 78 44" fill="none" stroke="{INK}" stroke-width="3"/><path d="M44 60H76" stroke="#8A4A26" stroke-width="2"/>',
    "drago": SKY + f'<path d="M52 104Q54 80 56 60H64Q66 80 68 104Z" fill="#9A8A6E" stroke="{INK}" stroke-width="2"/>'
                   + "".join(f'<path d="M60 62L{x} {y}" stroke="#9A8A6E" stroke-width="6"/>' for x, y in [(34, 40), (60, 34), (86, 40)])
                   + "".join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="8" fill="{LEAF}" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(30, 36), (60, 28), (90, 36)])
                   + f'<path d="M62 76Q64 84 62 90" stroke="{RED}" stroke-width="3"/><circle cx="62" cy="93" r="2.6" fill="{RED}"/>',
    "insignia": night(f'<path d="M50 106Q52 86 54 70H66Q68 86 70 106Z" fill="#9A8A6E" stroke="{INK}" stroke-width="2"/>'
                      + "".join(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="7" fill="{LEAF}" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(36, 58), (60, 50), (84, 58)])
                      + f'<circle cx="62" cy="96" r="3" fill="{RED}"/>'),
}
# --- Huelva -----------------------------------------------------------------
h = {
    "ceramica": BG + f'<path d="M36 44H84Q88 80 60 96Q32 80 36 44Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>'
                     + "".join(f'<path d="M38 {y}H82" stroke="{INK}" stroke-width="1.6"/>' for y in (54, 62)) + f'<path d="M44 72L52 66L60 72L68 66L76 72" fill="none" stroke="{PAPER}" stroke-width="2"/>',
    "espada": SKY + waves(90) + sword(40, 86, 84, 26),
    "caldero": BG + f'<path d="M26 50H94Q94 94 60 96Q26 94 26 50Z" fill="#C9963A" stroke="{INK}" stroke-width="2.4"/><ellipse cx="60" cy="50" rx="34" ry="8" fill="#A87A22" stroke="{INK}" stroke-width="2"/>'
                    + "".join(f'<circle cx="{x}" cy="46" r="7" fill="#C9963A" stroke="{INK}" stroke-width="1.6"/>' for x in (32, 88)),
    "arado": BG + f'<path d="M24 90H80L96 76" fill="none" stroke="{WOOD}" stroke-width="6"/><path d="M40 90L30 104H50Z" fill="{SILVER}" stroke="{INK}" stroke-width="1.6"/>'
                  f'<path d="M80 90L90 40" stroke="{WOOD}" stroke-width="5"/>' + "".join(f'<path d="M{x} 44Q{x + 4} 30 {x} 22" fill="none" stroke="{GOLDD}" stroke-width="2.4"/>' for x in (30, 40, 50)),
    "plata": BG + "".join(f'<path d="M{x - 18} {y}L{x - 12} {y - 12}H{x + 12}L{x + 18} {y}Z" fill="{SILVER}" stroke="{INK}" stroke-width="2"/>' for x, y in [(44, 90), (76, 90), (60, 74)]) + sparkle(92, 36, 6, WHITE),
    "insignia": night(f'<path d="M26 88H94" stroke="{SILVER}" stroke-width="2"/>' + "".join(f'<path d="M{x - 14} {y}L{x - 9} {y - 10}H{x + 9}L{x + 14} {y}Z" fill="{SILVER}" stroke="{INK}" stroke-width="1.6"/>' for x, y in [(46, 100), (74, 100), (60, 88)]),
                      f'<path d="M52 36L60 24L68 36L76 28L72 48H48L44 28Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>'),
}
# --- Jaén -------------------------------------------------------------------
j = {
    "mona": BG + f'<path d="M26 104V30H94V104" fill="#E6D2A8" stroke="{INK}" stroke-width="2"/>' + stone_head(60, 60, 1.2)
                 + f'<path d="M46 50L50 40L56 48L60 38L64 48L70 40L74 50Z" fill="{STONE}" stroke="{INK}" stroke-width="1.2"/><path d="M40 84Q60 100 80 84V104H40Z" fill="{STONE}" stroke="{INK}" stroke-width="1.6"/>',
    "compas": BG + f'<path d="M60 26L36 100M60 26L84 100" stroke="{INK}" stroke-width="6"/><path d="M60 26L36 100M60 26L84 100" stroke="{SILVER}" stroke-width="3"/>'
                   f'<circle cx="60" cy="28" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/><path d="M44 76Q60 68 76 76" fill="none" stroke="{INK}" stroke-width="2"/>',
    "lampara": NIGHT + f'<path d="M60 18V40" stroke="{SILVER}" stroke-width="2"/><path d="M40 48H80L74 74Q60 82 46 74Z" fill="{SILVER}" stroke="{INK}" stroke-width="2"/>'
                       f'<path d="M36 48H84" stroke="{SILVER}" stroke-width="4"/>' + flame(60, 50, .6),
    "cadenas": BG + "".join(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="6" transform="rotate({r} {x} {y})" fill="none" stroke="{SILVERD}" stroke-width="4"/>'
                            for x, y, r in [(30, 40, 40), (40, 52, -40), (50, 64, 40), (60, 76, -40), (70, 88, 40), (80, 98, -40)]),
    "sabana": night(f'<path d="M36 104Q34 60 60 40Q86 60 84 104L76 96L68 104L60 96L52 104L44 96Z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
                    f'<circle cx="52" cy="64" r="4" fill="{INK}"/><circle cx="68" cy="64" r="4" fill="{INK}"/><ellipse cx="60" cy="78" rx="4" ry="6" fill="{INK}"/>'),
    "insignia": night(f'<path d="M40 104Q38 66 60 50Q82 66 80 104L72 96L66 104L60 96L54 104L48 96Z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
                      f'<path d="M58 70Q60 60 64 70" fill="none" stroke="{INK}" stroke-width="2"/>', stone_head(26, 96, .5)),
}
# --- Almería ----------------------------------------------------------------
a = {
    "llave": BG + f'<circle cx="40" cy="44" r="14" fill="none" stroke="{GOLDD}" stroke-width="6"/><path d="M50 54L90 94M76 80L84 72M84 88L92 80" stroke="{GOLDD}" stroke-width="6"/>',
    "seda": BG + f'<path d="M24 40Q60 26 96 40V90Q60 76 24 90Z" fill="#6E2C5E" stroke="{INK}" stroke-width="2"/>'
                 + "".join(f'<path d="M30 {y}Q60 {y - 12} 90 {y}" fill="none" stroke="{GOLD}" stroke-width="2"/>' for y in (50, 62, 74)),
    "luna": NIGHT + stars([(22, 30), (96, 70), (30, 96), (80, 20)]) + f'<circle cx="60" cy="58" r="26" fill="#FFF3C4"/><circle cx="72" cy="50" r="22" fill="{NAVY}"/>'
                    + f'<path d="M20 104Q60 86 100 104Z" fill="#C9A77E"/>',
    "pico": BG + f'<path d="M60 104L60 40" stroke="{INK}" stroke-width="7"/><path d="M60 104L60 40" stroke="{WOOD}" stroke-width="4"/>'
                 f'<path d="M26 44Q60 22 94 44Q60 34 26 44Z" fill="{SILVER}" stroke="{INK}" stroke-width="2"/>',
    "cofre": BG + f'<path d="M26 60H94V100H26Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/><path d="M26 60L32 30H100L94 60" fill="{WOODL}" stroke="{INK}" stroke-width="2.2"/>'
                  f'<path d="M26 60H94" stroke="{GOLDD}" stroke-width="4"/><path d="M56 70H64V80H56Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/><path d="M32 64H88V96H32Z" fill="#3A2A20" opacity=".35"/>',
    "insignia": night(f'<path d="M14 106L30 70H44L50 60H70L76 70H90L106 106Z" fill="#C9A77E" stroke="{INK}" stroke-width="2"/>'
                      + "".join(f'<path d="M{x} 70V64H{x + 6}V70" fill="#C9A77E" stroke="{INK}" stroke-width="1.2"/>' for x in (32, 52, 62, 80)),
                      f'<path d="M50 96H70V106H50Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>'),
}

RING = {"l1": GOLD, "l2": GOLD, "la": SEA, "lb": CLAY, "l5": GOLD, "fi": GOLD}
ORDER = {  # icono → (anillo, título), en el orden de las paradas l1, l2, la, lb, l5, final
    "malaga": (m, [("farol", "El farol de la plaza"), ("sombrero", "El sombrero de don Álvaro"), ("vara", "La vara del corregidor"), ("carta", "La carta al rey"), ("cabeza", "La cabeza de piedra"), ("insignia", "¿De quién eran las siete cabezas?")]),
    "sevilla": (s, [("pluma", "La pluma de Bécquer"), ("candil", "El candil"), ("rodillas", "Las rodillas que crujen"), ("espada", "La espada del rey"), ("busto", "El busto del rey"), ("insignia", "¿Quién mató al caballero del Candilejo?")]),
    "granada": (g, [("libro", "«Granada la bella»"), ("estrella", "La estrella del Bañuelo"), ("lluvia", "La lluvia de Zafra"), ("sello", "El sello de Zafra"), ("fenix", "El fénix"), ("insignia", "¿Qué espera la ventana de la Casa de Castril?")]),
    "cordoba": (c, [("reloj", "El reloj de las Tendillas"), ("romance", "El romance"), ("comedia", "La comedia de Lope"), ("almena", "La almena"), ("torre", "La torre octogonal"), ("insignia", "¿Por qué se llama torre de la Malmuerta?")]),
    "cadiz": (k, [("escudo", "El escudo de Hércules"), ("bueyes", "Los bueyes de Gerión"), ("flecha", "La flecha"), ("anfora", "El ánfora de Gadir"), ("drago", "El drago"), ("insignia", "¿Por qué sangra el drago?")]),
    "huelva": (h, [("ceramica", "La cerámica del santuario"), ("espada", "La espada de la ría"), ("caldero", "El caldero de Samos"), ("arado", "El arado de Habis"), ("plata", "El lingote de plata"), ("insignia", "¿Dónde estaba Tartessos?")]),
    "jaen": (j, [("mona", "La Mona"), ("compas", "El compás de Vandelvira"), ("lampara", "La lámpara de plata"), ("cadenas", "Las cadenas"), ("sabana", "La sábana del fantasma"), ("insignia", "¿Quién era el fantasma de San Bartolomé?")]),
    "almeria": (a, [("llave", "La llave de la puerta"), ("seda", "La seda de la taifa"), ("luna", "La luna de San Juan"), ("pico", "El pico del buscador"), ("cofre", "El cofre vacío"), ("insignia", "¿Dónde está el tesoro de la Alcazaba?")]),
}
ART = {}
for city, (arts, items) in ORDER.items():
    for (key, title), ring in zip(items, (GOLD, GOLD, SEA, CLAY, GOLD, GOLD)):
        ART[f"{city}_leyenda_{key}"] = (ring, arts[key], title)

if __name__ == "__main__":
    write(ART)
    print("coleccionables de las rutas de leyendas generados:", len(ART))
