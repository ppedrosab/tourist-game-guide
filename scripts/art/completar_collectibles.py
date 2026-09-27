#!/usr/bin/env python3
"""
Coleccionables de las rutas que completan las ciudades (ver docs/CIUDADES_QUE_FALTAN.md).
Medallón 120×124. Aro: oro = comunes; mar = primer camino (dinero), arcilla = segundo (poder).

Uso: python3 scripts/art/completar_collectibles.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, sparkle, write
from fiestas_andalucia_collectibles import BG, SKY, RED, LEAF

BLUE = "#3A6EA5"; YELLOWP = "#F2C14E"


def pigeon(x, y, s=1.0, c="#E9E4DA"):
    return (f'<path d="M{x - 26 * s} {y}Q{x - 6 * s} {y - 22 * s} {x + 18 * s} {y - 8 * s}L{x + 30 * s} {y - 14 * s}L{x + 24 * s} {y - 2 * s}Q{x + 6 * s} {y + 18 * s} {x - 26 * s} {y}Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x - 8 * s} {y - 6 * s}Q{x + 4 * s} {y - 30 * s} {x + 14 * s} {y - 10 * s}" fill="#CFC8BA" stroke="{INK}" stroke-width="1.6"/>'
            f'<circle cx="{x + 20 * s}" cy="{y - 10 * s}" r="{1.6 * s}" fill="{INK}"/>'
            f'<path d="M{x - 4 * s} {y + 8 * s}V{y + 16 * s}M{x + 4 * s} {y + 8 * s}V{y + 16 * s}" stroke="{RED}" stroke-width="{2 * s}"/>')


def palette(x, y):
    return (f'<path d="M{x - 34} {y}Q{x - 30} {y - 30} {x} {y - 30}Q{x + 34} {y - 28} {x + 32} {y}Q{x + 28} {y + 22} {x + 4} {y + 18}Q{x - 8} {y + 14} {x - 12} {y + 22}Q{x - 34} {y + 24} {x - 34} {y}Z" fill="{WOODL}" stroke="{INK}" stroke-width="2.2"/>'
            f'<circle cx="{x - 16}" cy="{y + 4}" r="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
            + "".join(f'<circle cx="{x + dx}" cy="{y + dy}" r="5" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'
                      for dx, dy, c in [(-14, -16, RED), (0, -20, YELLOWP), (14, -16, BLUE), (22, -2, LEAF), (12, 10, INK)]))


mal = {
    "lapiz": BG + (f'<path d="M26 92L82 36L94 48L38 104Z" fill="{YELLOWP}" stroke="{INK}" stroke-width="2.2"/>'
                   f'<path d="M26 92L38 104L20 110Z" fill="#E9C9A0" stroke="{INK}" stroke-width="2"/><path d="M20 110L24 104L26 108Z" fill="{INK}"/>'
                   f'<path d="M82 36L94 48L100 42L88 30Z" fill="#E9A0A0" stroke="{INK}" stroke-width="2"/>'
                   f'<text x="72" y="92" font-family="Georgia, serif" font-style="italic" font-weight="700" font-size="15" fill="{INK}">piz!</text>'),
    "nombre": BG + (f'<path d="M24 26H96V96Q60 104 24 96Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
                    + "".join(f'<text x="30" y="{40 + k * 11}" font-family="Georgia, serif" font-size="8.5" fill="{INK}">{w}</text>'
                              for k, w in enumerate(["Pablo, Diego, José,", "Francisco de Paula,", "Juan Nepomuceno,", "María de los Remedios,", "Cipriano de la…"]))
                    + f'<text x="60" y="94" font-family="Georgia, serif" font-weight="700" font-size="13" text-anchor="middle" fill="{CLAY}">Picasso</text>'),
    "paloma": SKY + pigeon(58, 66, 1.3) + sparkle(94, 30, 5, GOLD),
    "picador": BG + (f'<path d="M20 28H100V100H20Z" fill="{YELLOWP}" stroke="{INK}" stroke-width="2.4"/>'
                     f'<path d="M34 90Q40 66 62 64Q84 62 88 84L84 92M44 90V78" fill="none" stroke="{INK}" stroke-width="3"/>'
                     f'<circle cx="60" cy="46" r="8" fill="#D9A07A" stroke="{INK}" stroke-width="1.8"/><path d="M50 40Q60 30 70 40Z" fill="{INK}"/>'
                     f'<path d="M58 54L60 70M74 50L40 36" stroke="{INK}" stroke-width="2.4"/>'),
    "paleta": BG + palette(60, 66) + f'<path d="M78 34L100 12" stroke="{INK}" stroke-width="5"/><path d="M78 34L100 12" stroke="{WOOD}" stroke-width="3"/>',
    "insignia": SKY + pigeon(60, 70, 1.1, PAPER) + f'<path d="M34 94Q60 104 86 94" fill="none" stroke="{GOLD}" stroke-width="4"/>' + sparkle(28, 30, 6, GOLD) + sparkle(94, 36, 4, GOLD),
}

ORDER = {
    "malaga_picasso": (mal, [("lapiz", "El lápiz del «piz, piz»"), ("nombre", "El nombre larguísimo"), ("paloma", "La paloma de papá"),
                             ("picador", "El pequeño picador amarillo"), ("paleta", "La paleta de Picasso"), ("insignia", "¿Por qué Picasso no volvió a Málaga?")]),
}
ART = {}
for prefix, (arts, items) in ORDER.items():
    for (key, title), ring in zip(items, (GOLD, GOLD, SEA, CLAY, GOLD, GOLD)):
        ART[f"{prefix}_{key}"] = (ring, arts[key], title)

if __name__ == "__main__":
    write(ART)
    print("coleccionables:", len(ART))
