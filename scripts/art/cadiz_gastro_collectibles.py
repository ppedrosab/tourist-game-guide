#!/usr/bin/env python3
"""
Coleccionables de la ruta gastronómica de Cádiz (medallón 120×124).
Aro: oro = comunes, mar = recetas del mar, arcilla = recetas de la tierra.

Uso: python3 scripts/art/cadiz_gastro_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import (INK, CLAY, CLAYD, SEA, SEAD, SEAT, PEACH, GOLD, GOLDD, PAPER, SAND, WHITE,
                                WOOD, WOODL, sparkle, waves, write)

FRY = "#E0A64E"; FRYD = "#B97F2E"; FRYL = "#F2CC80"


def plate(cx=60, cy=84, rx=36, ry=10):
    return (f'<ellipse cx="{cx}" cy="{cy + 3}" rx="{rx}" ry="{ry}" fill="{INK}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{cy - 1}" rx="{rx - 8}" ry="{ry - 4}" fill="none" stroke="{SEA}" stroke-width="1.4"/>')


# Cartucho de pescaíto: cono de papel con boquerones fritos
cartucho = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    + "".join(f'<g transform="rotate({r} {x} {y})"><path d="M{x - 18} {y}Q{x} {y - 10} {x + 14} {y}Q{x} {y + 10} {x - 18} {y}Z" fill="{FRY}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M{x + 14} {y}L{x + 22} {y - 7}L{x + 22} {y + 7}Z" fill="{FRYD}" stroke="{INK}" stroke-width="1.4"/><circle cx="{x - 11}" cy="{y - 2}" r="1.4" fill="{INK}"/>'
              f'<path d="M{x - 4} {y - 5}Q{x} {y} {x - 4} {y + 5}" fill="none" stroke="{FRYD}" stroke-width="1.2"/></g>'
              for x, y, r in [(38, 56, -20), (50, 46, -55), (70, 46, -125), (82, 56, -160), (60, 50, -90)])
    + f'<path d="M28 62L92 62L60 110Z" fill="#E8D8B8" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M60 62L92 62L60 110Z" fill="#D4BF96"/>'
    f'<path d="M28 62L92 62" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M42 74L78 74M50 86L70 86" stroke="#BFA77A" stroke-width="1.4"/>'
    f'<path d="M88 44Q96 40 98 50" fill="none" stroke="{GOLD}" stroke-width="2"/>'
    + sparkle(94, 28, 5, GOLD) + sparkle(24, 86, 3.5)
)

# Erizo de mar abierto, con su cucharilla
erizo = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + "".join(f'<path d="M{60 + math.cos(math.radians(a)) * 26:.1f} {66 + math.sin(math.radians(a)) * 20:.1f}L{60 + math.cos(math.radians(a)) * 38:.1f} {66 + math.sin(math.radians(a)) * 30:.1f}" stroke="#3A2A48" stroke-width="3"/>' for a in range(0, 360, 15))
    + f'<ellipse cx="60" cy="66" rx="28" ry="22" fill="#4A3A5A" stroke="{INK}" stroke-width="2.2"/>'
    f'<ellipse cx="60" cy="62" rx="18" ry="12" fill="#F29A2E" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<path d="M60 62L{60 + math.cos(math.radians(a)) * 14:.1f} {62 + math.sin(math.radians(a)) * 9:.1f}" stroke="#E07A2E" stroke-width="3"/>' for a in range(0, 360, 72))
    + f'<path d="M78 40L96 22" stroke="{INK}" stroke-width="5"/><path d="M78 40L96 22" stroke="#C9C6CF" stroke-width="2.4"/>'
    f'<ellipse cx="75" cy="44" rx="5" ry="3.4" transform="rotate(-45 75 44)" fill="#C9C6CF" stroke="{INK}" stroke-width="1.6"/>'
    + sparkle(28, 32, 5, GOLD)
)

# Tortillita de camarones: fina, dorada y con camarones asomando
tortillita = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + plate(60, 78, 40, 12)
    + f'<path d="M26 66Q30 44 58 42Q90 40 94 62Q96 78 60 80Q24 80 26 66Z" fill="{FRYL}" stroke="{INK}" stroke-width="2.2"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{FRYD}" stroke-width="1.2"/>' for x, y, r in [(40, 56, 5), (70, 50, 4), (82, 66, 5), (48, 70, 3), (62, 62, 3)])
    + "".join(f'<path d="M{x} {y}q4 -6 9 -2q-2 5 -9 2Z" fill="#F08A74" stroke="{INK}" stroke-width="1"/>' for x, y in [(36, 60), (58, 52), (76, 60), (50, 72), (66, 70)])
    + f'<path d="M44 48Q52 44 60 46" fill="none" stroke="#FFF" stroke-width="2" opacity=".7"/>'
    + sparkle(94, 32, 5, GOLD)
)

# Chicharrón en lonchas con medio limón
chicharron = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    + plate(60, 80, 40, 12)
    + "".join(f'<g transform="rotate({r} {x} 66)"><rect x="{x - 14}" y="58" width="28" height="18" rx="3" fill="#C9885A" stroke="{INK}" stroke-width="1.8"/>'
              f'<rect x="{x - 14}" y="58" width="28" height="5" fill="#F4E4CC"/><rect x="{x - 14}" y="66" width="28" height="3" fill="#F4E4CC"/></g>'
              for x, r in [(40, -12), (58, -4), (76, 8)])
    + f'<path d="M84 50A12 12 0 0 1 100 62L84 62Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M86 60L92 52M88 61L97 57" stroke="{GOLDD}" stroke-width="1.2"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{WHITE}" stroke="{INK}" stroke-width=".5"/>' for x, y in [(44, 50), (60, 46), (72, 52)])
    + sparkle(28, 36, 5, GOLD)
)

# Papas aliñás: patatas, cebolleta y perejil en su plato
papas = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    + plate(60, 80, 40, 12)
    + "".join(f'<path d="M{x - 9} {y}Q{x - 9} {y - 9} {x} {y - 10}Q{x + 10} {y - 9} {x + 9} {y}Q{x} {y + 6} {x - 9} {y}Z" fill="#F2D48F" stroke="{INK}" stroke-width="1.6"/>'
              for x, y in [(42, 76), (60, 72), (78, 76), (50, 64), (70, 64), (60, 56)])
    + "".join(f'<path d="M{x} {y}q3 -2 6 0" fill="none" stroke="#F4F0E6" stroke-width="2"/>' for x, y in [(44, 70), (64, 62), (74, 72)])
    + "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#4F8B5A"/>' for x, y in [(48, 66), (56, 60), (66, 68), (72, 58), (52, 74), (80, 70), (40, 72)])
    + f'<path d="M86 30L96 58" stroke="{INK}" stroke-width="5"/><path d="M86 30L96 58" stroke="#C9C6CF" stroke-width="2.4"/>'
    + sparkle(26, 36, 5, GOLD)
)

# Pan de Cádiz: dulce de mazapán tostado, con su loncha cortada
pan = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    + plate(60, 84, 40, 11)
    + f'<path d="M26 78L26 58Q26 50 34 50L78 50L78 78Z" fill="#F2DCA8" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M26 58Q26 50 34 50L78 50L78 58Z" fill="#C98E4A"/>'
    + "".join(f'<path d="M{x} 50L{x + 6} 58" stroke="#A86F32" stroke-width="1.4"/>' for x in range(32, 76, 8))
    + f'<path d="M34 64H72" stroke="#E07A2E" stroke-width="3"/><path d="M34 70H72" stroke="#F29A2E" stroke-width="2"/>'
    + "".join(f'<rect x="{x}" y="{y}" width="4" height="3" fill="{c}"/>' for x, y, c in [(40, 66, "#B8323A"), (56, 67, "#4F8B5A"), (66, 65, "#B8323A")])
    + f'<path d="M82 78L82 60L96 56L96 74Z" fill="#F2DCA8" stroke="{INK}" stroke-width="1.8"/><path d="M82 60L96 56L96 60L82 64Z" fill="#C98E4A"/>'
    f'<path d="M84 68L94 65" stroke="#E07A2E" stroke-width="2.4"/>'
    + sparkle(92, 32, 5, GOLD) + sparkle(28, 34, 3.5)
)

# El recetario de la Tía Norica, asomando del delantal
recetario = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="60" cy="56" r="30" fill="{GOLD}" opacity=".3"/>'
    f'<path d="M30 60H90V110H30Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M30 60Q60 70 90 60" fill="none" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M36 66H84V100H36Z" fill="none" stroke="#EADFCB" stroke-width="2"/>'
    # libreta asomando del bolsillo
    f'<path d="M44 28L76 24L80 70L48 74Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M52 36L72 33M53 44L73 41M54 52L68 50" stroke="#F4D3A6" stroke-width="1.6"/>'
    f'<path d="M40 70H80V86Q60 92 40 86Z" fill="#E6DCC6" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<circle cx="{x}" cy="78" r="1.6" fill="{CLAY}"/>' for x in (48, 60, 72))
    + f'<path d="M86 30Q90 22 98 24" fill="none" stroke="{INK}" stroke-width="1.4"/>'
    + sparkle(94, 42, 5, GOLD) + sparkle(24, 40, 3.5)
)

ART = {
    "cadiz_g_cartucho": (GOLD, cartucho, "El cartucho de pescaíto"),
    "cadiz_g_erizo": (SEA, erizo, "El erizo de La Viña"),
    "cadiz_g_tortillita": (SEA, tortillita, "La tortillita de camarones"),
    "cadiz_g_chicharron": (CLAY, chicharron, "El chicharrón con limón"),
    "cadiz_g_papas": (CLAY, papas, "Las papas aliñás"),
    "cadiz_g_pan": (GOLD, pan, "El pan de Cádiz"),
    "cadiz_g_recetario": (GOLD, recetario, "El recetario de la Tía Norica"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables gastronómicos de Cádiz generados")
