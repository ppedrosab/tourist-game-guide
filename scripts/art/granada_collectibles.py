#!/usr/bin/env python3
"""
Coleccionables de Granada (medallón 120×124). Aro: oro = comunes, mar = Albaicín,
arcilla = Alhambra.

Uso: python3 scripts/art/granada_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import (INK, CLAY, CLAYD, SEA, SEAD, SEAT, PEACH, GOLD, GOLDD, PAPER, SAND, WHITE,
                                WOOD, WOODL, sparkle, waves, write)

# La pluma de Irving: tintero, pluma y libro de cuentos
pluma = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    f'<path d="M24 84L60 76L96 84L96 96L60 90L24 96Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M60 76V90" stroke="{INK}" stroke-width="1.6"/>'
    + "".join(f'<path d="M30 {86 + k * 3}L54 {81 + k * 3}M66 {81 + k * 3}L90 {86 + k * 3}" stroke="#9AA3AA" stroke-width="1"/>' for k in range(2))
    + f'<path d="M34 66Q34 54 44 54Q54 54 54 66L52 76H36Z" fill="{SEA}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M38 56H50" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M46 60L80 24Q90 18 86 30Q74 50 48 64Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M46 62L84 24" stroke="{INK}" stroke-width="1.4"/>'
    + "".join(f'<path d="M{60 + k * 6} {50 - k * 7}L{66 + k * 6} {48 - k * 7}" stroke="#D8CBB3" stroke-width="1.2"/>' for k in range(4))
    + sparkle(92, 50, 5, GOLD) + sparkle(26, 40, 3.5)
)

# Atardecer en San Nicolás: la Alhambra roja y la nieve de Sierra Nevada
atardecer = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F6C8A0"/>'
    f'<circle cx="84" cy="40" r="10" fill="#FFF3DC"/>'
    f'<path d="M14 64L40 40L58 56L78 34L106 62Z" fill="#B9C8D0" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M34 46L40 40L46 46L42 48ZM72 40L78 34L86 42L80 44Z" fill="{WHITE}"/>'
    f'<path d="M14 92Q40 70 106 80L106 110L14 110Z" fill="#6E9F7A" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M26 82H94V70H26Z" fill="#C4623F" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<path d="M{x} 70V{y}H{x + 10}V70" fill="#C4623F" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(30, 58), (52, 62), (72, 54), (84, 62)])
    + "".join(f'<path d="M{x} {y}l1.6 -3l1.6 3Z" fill="{INK}" opacity=".6"/>' for x, y in [(33, 66), (55, 68), (75, 62), (87, 68)])
    + f'<path d="M36 98Q36 92 40 92M60 102Q60 94 66 94" fill="none" stroke="#2F6440" stroke-width="3"/>'
    + sparkle(30, 30, 5, GOLD)
)

# Las pesas del arco: arco de herradura con pesas colgadas
pesas = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F4EEE2"/>'
    f'<path d="M20 108V30H100V108Z" fill="{WHITE}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M40 108V70Q40 48 60 48Q80 48 80 70V108Z" fill="#5E4232" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M36 72Q36 42 60 42Q84 42 84 72" fill="none" stroke="{GOLDD}" stroke-width="3"/>'
    + "".join(f'<path d="M{x} 30V{y}" stroke="{INK}" stroke-width="1.2"/><path d="M{x - 5} {y}H{x + 5}L{x + 4} {y + 8}H{x - 4}Z" fill="#6E6E78" stroke="{INK}" stroke-width="1.4"/>' for x, y in [(34, 20 + 16), (48, 34), (72, 34), (86, 36)])
    + f'<path d="M20 30H100" stroke="{INK}" stroke-width="2.4"/>'
    + sparkle(96, 96, 4.5, GOLD)
)

# La mano y la llave de la Puerta de la Justicia
llave = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F4D9C8"/>'
    f'<path d="M24 108V52Q24 24 60 24Q96 24 96 52V108" fill="none" stroke="#C4623F" stroke-width="10"/>'
    f'<path d="M24 108V52Q24 24 60 24Q96 24 96 52V108" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    # mano abierta
    f'<path transform="translate(0 -10)" d="M44 74V52Q44 48 47 48Q50 48 50 52V64V44Q50 40 53 40Q56 40 56 44V64V42Q56 38 59 38Q62 38 62 42V64V46Q62 42 65 42Q68 42 68 46V70Q70 64 74 64Q77 66 74 72L66 86Q62 90 54 90Q44 90 44 80Z" fill="{SAND}" stroke="{INK}" stroke-width="1.8"/>'
    # llave
    f'<path d="M58 90H90" stroke="{INK}" stroke-width="6"/><path d="M58 90H90" stroke="{GOLD}" stroke-width="3"/>'
    f'<circle cx="52" cy="90" r="7" fill="none" stroke="{INK}" stroke-width="5.6"/><circle cx="52" cy="90" r="7" fill="none" stroke="{GOLD}" stroke-width="2.8"/>'
    f'<path d="M80 90V98M86 90V96" stroke="{INK}" stroke-width="3"/>'
    + sparkle(86, 44, 5, GOLD)
)

# La granada, símbolo de la ciudad
granada = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<path d="M60 38Q86 38 90 64Q92 92 60 98Q28 92 30 64Q34 38 60 38Z" fill="#B8323A" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M60 40Q84 42 88 64Q90 88 64 96Q82 80 78 60Q74 46 60 40Z" fill="#8E2430"/>'
    f'<path d="M52 40L50 28L56 34L60 26L64 34L70 28L68 40Z" fill="#B8323A" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M40 56Q46 48 54 48" fill="none" stroke="#F09A9A" stroke-width="2.6"/>'
    f'<path d="M62 26Q70 14 84 18Q76 28 62 26Z" fill="#4F8B5A" stroke="{INK}" stroke-width="1.6"/>'
    + "".join(f'<ellipse cx="{x}" cy="{y}" rx="2.4" ry="3" fill="#E0566A" stroke="{INK}" stroke-width=".8"/>' for x, y in [(52, 72), (58, 78), (64, 72), (70, 78), (58, 86), (64, 86)])
    + f'<path d="M46 66Q60 60 76 68L72 92Q60 96 48 90Z" fill="none" stroke="{INK}" stroke-width="1.2" opacity=".5"/>'
    + sparkle(92, 36, 5, GOLD) + sparkle(28, 92, 3.5)
)

# El león de la fuente
leon = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + "".join(f'<circle cx="{58 + math.cos(math.radians(a)) * 24:.1f}" cy="{56 + math.sin(math.radians(a)) * 22:.1f}" r="9" fill="#DCCFB6" stroke="{INK}" stroke-width="1.6"/>' for a in range(0, 360, 36))
    + f'<circle cx="58" cy="56" r="24" fill="#DCCFB6"/>'
    f'<circle cx="58" cy="56" r="17" fill="#EEE6D6" stroke="{INK}" stroke-width="2"/>'
    f'<circle cx="52" cy="52" r="2" fill="{INK}"/><circle cx="64" cy="52" r="2" fill="{INK}"/>'
    f'<path d="M54 60H62L58 64Z" fill="#8A6A5A"/><path d="M52 66Q58 70 64 66" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M64 66Q86 64 94 84" fill="none" stroke="#8FB9B4" stroke-width="3.4"/>'
    f'<path d="M24 98Q60 84 96 98L92 108H28Z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M28 98Q60 88 92 98" fill="none" stroke="#8FB9B4" stroke-width="3"/>'
    + sparkle(92, 32, 5, GOLD)
)

# Insignia: la taza de la fuente con las manchas y una lupa
insignia = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="60" cy="56" r="30" fill="{GOLD}" opacity=".3"/>'
    f'<path d="M26 66Q60 56 94 66L88 82Q60 92 32 82Z" fill="{WHITE}" stroke="{INK}" stroke-width="2.2"/>'
    f'<ellipse cx="60" cy="66" rx="34" ry="8" fill="#DCEBE6" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="1.6" fill="#B85A3A" opacity=".75"/>' for x, y, rx in [(46, 80, 5), (58, 84, 3), (70, 80, 4)])
    + f'<path d="M54 86L52 100H68L66 86" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M44 102H76" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M60 58V40" stroke="#8FB9B4" stroke-width="3"/><path d="M60 40Q52 46 50 56M60 40Q68 46 70 56" fill="none" stroke="#8FB9B4" stroke-width="2"/>'
    f'<path d="M82 90L94 102" stroke="{INK}" stroke-width="6"/><path d="M82 90L94 102" stroke="{WOODL}" stroke-width="3"/>'
    f'<circle cx="74" cy="82" r="10" fill="{SEAT}" fill-opacity=".55" stroke="{INK}" stroke-width="2.6"/>'
    + sparkle(30, 36, 5, GOLD)
)

ART = {
    "granada_pluma": (GOLD, pluma, "La pluma de Irving"),
    "granada_atardecer": (SEA, atardecer, "Atardecer en San Nicolás"),
    "granada_pesas": (SEA, pesas, "Las pesas del arco"),
    "granada_llave": (CLAY, llave, "La mano y la llave"),
    "granada_granada": (CLAY, granada, "La granada"),
    "granada_leon": (GOLD, leon, "El león de la fuente"),
    "granada_insignia": (GOLD, insignia, "¿Quién mató a los Abencerrajes?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Granada generados")
