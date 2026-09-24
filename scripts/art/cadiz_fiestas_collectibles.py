#!/usr/bin/env python3
"""
Coleccionables de la ruta de Carnaval de Cádiz (medallón 120×124).
Aro: oro = comunes, mar = camino de La Viña, arcilla = camino de las plazas.

Uso: python3 scripts/art/cadiz_fiestas_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import (INK, CLAY, CLAYD, SEA, SEAD, SEAT, PEACH, GOLD, GOLDD, PAPER, SAND, WHITE,
                                WOOD, WOODL, sparkle, waves, write)
VIOLET = "#6E2C5E"; VIOLETD = "#521E46"; MINT = "#4F8B5A"; WIN_DARK = "#3E3024"

# El antifaz, con plumas y cintas
antifaz = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F1E2EC"/>'
    f'<path d="M58 40Q52 16 40 12Q50 26 52 42Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>'
    f'<path d="M62 40Q70 14 84 12Q72 28 66 42Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>'
    f'<path d="M24 56Q42 44 60 54Q78 44 96 56Q96 78 78 80Q66 80 60 70Q54 80 42 80Q24 78 24 56Z" fill="{VIOLET}" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M34 60Q42 54 50 62Q42 68 34 60ZM70 62Q78 54 86 60Q78 68 70 62Z" fill="#F1E2EC" stroke="{INK}" stroke-width="1.6"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{GOLD}"/>' for x, y in [(30, 54), (44, 50), (60, 58), (76, 50), (90, 54), (60, 72)])
    + f'<path d="M24 58Q14 70 20 90M96 58Q106 70 100 90" fill="none" stroke="{GOLD}" stroke-width="2.4"/>'
    + "".join(f'<rect x="{(i * 29) % 90 + 15}" y="{(i * 47) % 30 + 86}" width="4" height="4" transform="rotate({i * 33} {(i * 29) % 90 + 15} {(i * 47) % 30 + 86})" fill="{[CLAY, GOLD, SEA][i % 3]}"/>' for i in range(9))
    + sparkle(96, 30, 5, GOLD)
)

# La hierbabuena de María: ramita de hierbabuena ante un azulejo de calle
hierbabuena = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F4EEE2"/>'
    f'<rect x="26" y="20" width="68" height="40" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
    f'<rect x="31" y="25" width="58" height="30" rx="2" fill="none" stroke="{SEA}" stroke-width="1.8"/>'
    + "".join(f'<path d="M38 {32 + k * 8}H{82 - k * 10}" stroke="{SEAD}" stroke-width="2"/>' for k in range(3))
    + f'<path d="M60 98Q58 80 62 62" fill="none" stroke="#3F6A3A" stroke-width="2.4"/>'
    + "".join(f'<path d="M{61 + s * 1} {y}Q{61 + s * 16} {y - 8} {61 + s * 20} {y + 2}Q{61 + s * 12} {y + 6} {61 + s * 1} {y}Z" fill="{MINT}" stroke="{INK}" stroke-width="1.4"/>'
              for s, y in [(-1, 86), (1, 80), (-1, 72), (1, 66)])
    + f'<path d="M50 74Q54 78 58 76M70 70Q66 74 64 72" stroke="#6FA878" stroke-width="1"/>'
    + sparkle(94, 88, 5, GOLD) + sparkle(24, 90, 3.5)
)

# Las claves del cuarteto (y un pito)
claves = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    f'<path d="M30 96L70 30" stroke="{INK}" stroke-width="12"/><path d="M30 96L70 30" stroke="#C9885A" stroke-width="8"/>'
    f'<path d="M50 30L90 96" stroke="{INK}" stroke-width="12"/><path d="M50 30L90 96" stroke="#B8763F" stroke-width="8"/>'
    f'<path d="M34 90L66 36M54 36L86 90" stroke="#E6B58A" stroke-width="2"/>'
    f'<path d="M78 58L100 44" stroke="{INK}" stroke-width="7"/><path d="M78 58L100 44" stroke="{GOLD}" stroke-width="4"/>'
    f'<path d="M34 24Q30 18 36 16M84 24Q90 18 84 16" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    + sparkle(26, 60, 5, GOLD)
)

# La batea del coro
batea = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    f'<path d="M22 84H98V70H22Z" fill="{SEA}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M22 70L30 60H90L98 70" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} 70V64" stroke="{INK}" stroke-width="1.2"/>' for x in range(30, 92, 8))
    + f'<circle cx="34" cy="90" r="7" fill="{INK}"/><circle cx="86" cy="90" r="7" fill="{INK}"/>'
    f'<circle cx="34" cy="90" r="3" fill="#9AA3AA"/><circle cx="86" cy="90" r="3" fill="#9AA3AA"/>'
    + "".join(f'<circle cx="{x}" cy="50" r="6" fill="#D9A27A" stroke="{INK}" stroke-width="1.2"/><path d="M{x - 7} 60Q{x} 52 {x + 7} 60Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/><path d="M{x - 8} 45H{x + 8}L{x + 5} 40H{x - 5}Z" fill="#E9CF8A" stroke="{INK}" stroke-width="1"/>'
              for x, c in [(42, PAPER), (60, CLAY), (78, PAPER)])
    + f'<path d="M16 38Q60 20 104 38" fill="none" stroke="{INK}" stroke-width="1"/>'
    + "".join(f'<path d="M{x} {34 - abs(60 - x) * .0:.0f}l3 6l3 -6Z" fill="{[CLAY, GOLD, SEA, VIOLET][i % 4]}"/>' for i, x in enumerate(range(24, 100, 10)))
    + sparkle(100, 60, 4.5, GOLD)
)

# El pregón: atril con micrófono y papeles
pregon = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<path d="M40 104H80L74 60H46Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M34 60H86L80 50H40Z" fill="{WOODL}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M44 50L48 34L74 30L76 50Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<path d="M50 {38 + k * 4}L72 {35 + k * 4}" stroke="#9AA3AA" stroke-width="1"/>' for k in range(3))
    + f'<path d="M80 50Q86 36 82 26" fill="none" stroke="{INK}" stroke-width="2"/>'
    f'<ellipse cx="81" cy="22" rx="5" ry="7" fill="#4A4A55" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M50 80H70" stroke="{GOLD}" stroke-width="3"/>'
    f'<path d="M92 30Q98 26 96 20M96 38Q104 34 104 26" fill="none" stroke="{CLAY}" stroke-width="2"/>'
    + sparkle(28, 34, 5, GOLD)
)

# La bandurria
bandurria = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<g transform="rotate(-35 60 64)">'
    f'<path d="M60 70Q40 70 40 88Q40 108 60 108Q80 108 80 88Q80 70 60 70Z" fill="#C9885A" stroke="{INK}" stroke-width="2.2"/>'
    f'<circle cx="60" cy="86" r="6" fill="#3A2418" stroke="{INK}" stroke-width="1.4"/>'
    f'<path d="M56 72V24H64V72" fill="#6E4C33" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M54 24H66L64 12H56Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.6"/>'
    + "".join(f'<path d="M{57 + k * 2} 24V100" stroke="#F4E4CC" stroke-width=".7"/>' for k in range(4))
    + f'<path d="M50 98H70" stroke="{INK}" stroke-width="2"/></g>'
    + sparkle(94, 34, 5, GOLD) + sparkle(26, 92, 3.5)
)

# El cartelón completo, con sus cuatro viñetas y el puntero
cartelon = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<path d="M58 96V110M62 96V110" stroke="{WOOD}" stroke-width="3"/>'
    f'<path d="M26 28L94 24L96 96L28 100Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M61 26L62 98M27 64L95 60" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M34 58V42L44 34L54 42V58Z" fill="#C4623F" stroke="{INK}" stroke-width="1.2"/>'
    f'<path d="M68 52Q76 34 88 40M68 44Q78 30 90 32" fill="none" stroke="{SEA}" stroke-width="2.4"/>'
    f'<circle cx="40" cy="76" r="5" fill="{GOLD}" stroke="{INK}" stroke-width="1"/><circle cx="50" cy="78" r="5" fill="{CLAY}" stroke="{INK}" stroke-width="1"/><path d="M32 92H56L52 84H36Z" fill="{SEA}" stroke="{INK}" stroke-width="1"/>'
    f'<path d="M78 70L70 92H86Z" fill="{VIOLET}" stroke="{INK}" stroke-width="1.2"/><circle cx="78" cy="68" r="4" fill="#9BB58A" stroke="{INK}" stroke-width="1"/>'
    f'<path d="M96 104L70 50" stroke="{INK}" stroke-width="5"/><path d="M96 104L70 50" stroke="#C9A77E" stroke-width="2.6"/>'
    + sparkle(100, 30, 5, GOLD)
)

ART = {
    "carnaval_antifaz": (GOLD, antifaz, "El antifaz"),
    "carnaval_hierbabuena": (GOLD, hierbabuena, "La hierbabuena de María"),
    "carnaval_claves": (SEA, claves, "Las claves del cuarteto"),
    "carnaval_batea": (SEA, batea, "La batea del coro"),
    "carnaval_pregon": (CLAY, pregon, "El pregón"),
    "carnaval_bandurria": (CLAY, bandurria, "La bandurria"),
    "carnaval_cartelon": (GOLD, cartelon, "El cartelón completo"),
}

# ---------------------------------------------------------------------------
# Semana Santa (sin imágenes sagradas: solo objetos de la cofradía y de la calle)
# ---------------------------------------------------------------------------
PURPLE = "#4A2A5A"; NIGHT = "#2B3F5C"; WAX = "#F4E8CC"


def flame(x, y, s=1.0):
    return (f'<path d="M{x} {y - 10 * s}Q{x + 5 * s} {y - 3 * s} {x} {y}Q{x - 5 * s} {y - 3 * s} {x} {y - 10 * s}Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
            f'<path d="M{x} {y - 6 * s}Q{x + 2 * s} {y - 2 * s} {x} {y - 1 * s}Q{x - 2 * s} {y - 2 * s} {x} {y - 6 * s}Z" fill="{WHITE}"/>')


cirio = (
    f'<rect x="0" y="0" width="120" height="124" fill="#EFE6F2"/>'
    f'<circle cx="60" cy="40" r="22" fill="{GOLD}" opacity=".3"/>'
    f'<rect x="52" y="44" width="16" height="62" rx="2" fill="{WAX}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M52 50Q56 58 54 66M66 48Q64 54 67 60" fill="none" stroke="#E0D2AE" stroke-width="2"/>'
    f'<path d="M60 44V36" stroke="{INK}" stroke-width="1.6"/>' + flame(60, 36, 1.6)
    + f'<path d="M44 106H76" stroke="{PURPLE}" stroke-width="5"/>'
    + sparkle(92, 30, 4.5, GOLD)
)
horquilla = (
    f'<rect x="0" y="0" width="120" height="124" fill="#EFE6F2"/>'
    f'<path d="M60 40V108" stroke="{INK}" stroke-width="8"/><path d="M60 40V108" stroke="#8A6243" stroke-width="4.4"/>'
    f'<path d="M44 22Q44 42 60 42Q76 42 76 22" fill="none" stroke="{INK}" stroke-width="7"/><path d="M44 22Q44 42 60 42Q76 42 76 22" fill="none" stroke="#C9A77E" stroke-width="3.6"/>'
    f'<path d="M50 108H70" stroke="{INK}" stroke-width="3"/>'
    + "".join(f'<path d="M{x} 104q-6 -4 -10 0" fill="none" stroke="{INK}" stroke-width="1.4" opacity=".6"/>' for x in (44, 88))
    + sparkle(92, 60, 4.5, GOLD)
)
cruz = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    f'<path d="M56 18H64V108H56Z" fill="#8A6243" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M36 40H84V48H36Z" fill="#8A6243" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>' for x, y in [(60, 16), (34, 44), (86, 44)])
    + f'<path d="M50 44Q60 34 70 44Q60 54 50 44Z" fill="none" stroke="{GOLD}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} 70Q{x + 3} 64 {x + 6} 70" fill="none" stroke="{GOLD}" stroke-width="1.4"/>' for x in (52, 62))
    + sparkle(92, 86, 4.5, GOLD)
)
saeta = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    f'<path d="M26 60H94V100H26Z" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M34 66H86V94H34Z" fill="{WIN_DARK}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M22 60H98" stroke="{INK}" stroke-width="3"/>'
    + "".join(f'<path d="M{x} 48V60" stroke="{INK}" stroke-width="1.6"/>' for x in range(28, 96, 8))
    + f'<path d="M24 48H96" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M84 48Q76 40 80 32" fill="none" stroke="#4F8B5A" stroke-width="2"/><circle cx="80" cy="30" r="4" fill="{CLAY}"/><circle cx="86" cy="36" r="3" fill="#E0766A"/>'
    + "".join(f'<path d="M{x} {y}v-10l8 -3v10" fill="none" stroke="{INK}" stroke-width="1.6"/><circle cx="{x - 2}" cy="{y}" r="2.4" fill="{INK}"/><circle cx="{x + 6}" cy="{y - 3}" r="2.4" fill="{INK}"/>' for x, y in [(44, 34), (60, 26)])
    + sparkle(30, 30, 4, GOLD)
)
estandarte = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<path d="M58 14V110" stroke="{INK}" stroke-width="6"/><path d="M58 14V110" stroke="{GOLD}" stroke-width="3"/>'
    f'<path d="M40 30H76" stroke="{INK}" stroke-width="4"/><path d="M40 30H76" stroke="{GOLD}" stroke-width="2"/>'
    f'<path d="M42 32H74V80L58 90L42 80Z" fill="{SEA}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M48 38H68V74L58 81L48 74Z" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
    f'<path d="M58 70Q52 60 58 46Q64 60 58 70Z" fill="#4F8B5A" stroke="{INK}" stroke-width="1.2"/>'
    f'<path d="M58 70V50" stroke="#2F5A3C" stroke-width="1"/>'
    f'<path d="M14 104Q34 96 54 104T100 104L100 112L14 112Z" fill="{SEAT}" stroke="{INK}" stroke-width="1.6"/>'
    + sparkle(92, 40, 4.5, GOLD)
)
silencio = (
    f'<rect x="0" y="0" width="120" height="124" fill="{NIGHT}"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="1" fill="{WHITE}" opacity=".7"/>' for x, y in [(30, 30), (84, 24), (96, 50), (24, 60)])
    + "".join(f'<rect x="{x}" y="{58 + (i % 2) * 6}" width="10" height="{40 - (i % 2) * 6}" rx="1.5" fill="{WAX}" stroke="{INK}" stroke-width="1.6"/>' + flame(x + 5, 58 + (i % 2) * 6, 1.1)
              for i, x in enumerate((34, 55, 76)))
    + f'<circle cx="60" cy="60" r="28" fill="{GOLD}" opacity=".12"/>'
    + sparkle(92, 92, 3.5, GOLD)
)
torrija = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    f'<ellipse cx="60" cy="88" rx="38" ry="10" fill="{INK}"/><ellipse cx="60" cy="85" rx="38" ry="10" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<g transform="rotate({r} {x} 70)"><rect x="{x - 16}" y="60" width="32" height="20" rx="5" fill="#D9A24E" stroke="{INK}" stroke-width="1.8"/><rect x="{x - 14}" y="62" width="28" height="6" rx="3" fill="#EFC27A"/></g>'
              for x, r in [(46, -8), (74, 6)])
    + "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#8A5A2A"/>' for x, y in [(40, 64), (50, 70), (70, 64), (80, 70), (60, 66)])
    + f'<path d="M36 58Q60 50 84 58" fill="none" stroke="#F4E4CC" stroke-width="2"/>'
    + sparkle(92, 32, 5, GOLD)
)
palio = (
    f'<rect x="0" y="0" width="120" height="124" fill="{NIGHT}"/>'
    f'<path d="M24 36H96V46H24Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} 46q4 6 8 0" fill="{PURPLE}" stroke="{INK}" stroke-width="1"/>' for x in range(24, 96, 8))
    + "".join(f'<path d="M{x} 46V96" stroke="{GOLD}" stroke-width="2.6"/>' for x in (28, 44, 76, 92))
    + "".join(f'<rect x="{x}" y="{y}" width="5" height="{96 - y}" fill="{WAX}" stroke="{INK}" stroke-width=".8"/>' + flame(x + 2.5, y, .8)
              for x, y in [(48, 70), (56, 64), (64, 64), (72, 70), (52, 76), (68, 76)])
    + f'<path d="M22 96H98V108H22Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M26 100H94" stroke="{GOLD}" stroke-width="1.6"/>'
    + sparkle(100, 24, 4, GOLD) + sparkle(20, 60, 3, GOLD)
)

ART_SSANTA = {
    "ssanta_cirio": (GOLD, cirio, "El cirio"),
    "ssanta_horquilla": (GOLD, horquilla, "La horquilla"),
    "ssanta_cruz": (SEA, cruz, "La cruz de guía"),
    "ssanta_saeta": (SEA, saeta, "La saeta"),
    "ssanta_estandarte": (CLAY, estandarte, "El estandarte de la Palma"),
    "ssanta_silencio": (CLAY, silencio, "La vela del silencio"),
    "ssanta_torrija": (GOLD, torrija, "La torrija"),
    "ssanta_palio": (GOLD, palio, "Sobre los hombros de Cádiz"),
}


if __name__ == "__main__":
    write(ART)
    write(ART_SSANTA)
    print("coleccionables del Carnaval y de Semana Santa generados")
