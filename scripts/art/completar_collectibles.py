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

def mask(x, y, s=1.0, c=PAPER):
    return (f'<path d="M{x - 24 * s} {y - 22 * s}Q{x} {y - 34 * s} {x + 24 * s} {y - 22 * s}Q{x + 26 * s} {y + 10 * s} {x} {y + 30 * s}Q{x - 26 * s} {y + 10 * s} {x - 24 * s} {y - 22 * s}Z" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            f'<ellipse cx="{x - 10 * s}" cy="{y - 6 * s}" rx="{6 * s}" ry="{4 * s}" fill="{INK}"/><ellipse cx="{x + 10 * s}" cy="{y - 6 * s}" rx="{6 * s}" ry="{4 * s}" fill="{INK}"/>'
            f'<path d="M{x - 12 * s} {y + 10 * s}Q{x} {y + 22 * s} {x + 12 * s} {y + 10 * s}Q{x} {y + 16 * s} {x - 12 * s} {y + 10 * s}Z" fill="{INK}"/>')


def castanet(x, y, r=16, c=WOOD):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x - r * 0.6} {y - r * 0.3}Q{x - r * 0.2} {y - r * 0.8} {x + r * 0.3} {y - r * 0.6}" fill="none" stroke="{WOODL}" stroke-width="2"/>'
            f'<path d="M{x} {y - r}Q{x + 4} {y - r - 12} {x + 12} {y - r - 14}" fill="none" stroke="{RED}" stroke-width="2.4"/>')


cad = {
    "mascara": BG + mask(60, 64, 1.15) + sparkle(96, 30, 5, GOLD),
    "crotalos": BG + castanet(44, 70) + castanet(76, 64, 16, WOODL) + sparkle(28, 32, 5, GOLD),
    "anillo": BG + (f'<ellipse cx="60" cy="72" rx="28" ry="24" fill="none" stroke="{INK}" stroke-width="10"/>'
                    f'<ellipse cx="60" cy="72" rx="28" ry="24" fill="none" stroke="{GOLD}" stroke-width="6"/>'
                    f'<ellipse cx="60" cy="44" rx="14" ry="10" fill="{RED}" stroke="{INK}" stroke-width="2.2"/>'
                    f'<path d="M54 42Q60 36 66 42" fill="none" stroke="{WHITE}" stroke-width="1.6"/>'),
    "versos": BG + (f'<path d="M36 32H84Q90 32 90 38V90Q90 96 84 96H36Q30 96 30 90V38Q30 32 36 32Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
                    + "".join(f'<text x="60" y="{47 + k * 10}" font-family="Georgia, serif" font-style="italic" font-size="7.5" text-anchor="middle" fill="{INK}">{w}</text>'
                              for k, w in enumerate(["Nec de Gadibus", "improbis puellae", "vibrabunt", "sine fine…"]))
                    + f'<text x="60" y="88" font-family="Georgia, serif" font-weight="700" font-size="8.5" text-anchor="middle" fill="{CLAY}">MARTIALIS</text>'),
    "atun": SKY + (f'<path d="M18 68Q40 42 76 56L98 42L94 68L98 94L76 80Q40 94 18 68Z" fill="{SILVER}" stroke="{INK}" stroke-width="2.4"/>'
                   f'<path d="M30 68Q52 58 76 66" fill="none" stroke="{NAVY}" stroke-width="3"/>'
                   f'<circle cx="32" cy="64" r="3" fill="{INK}"/><path d="M52 50L60 40L64 52Z" fill="{NAVY}" stroke="{INK}" stroke-width="1.6"/>'),
    "insignia": BG + (f'<path d="M20 92Q60 30 100 92" fill="none" stroke="{INK}" stroke-width="3"/>'
                      + "".join(f'<path d="M{20 + k * 7} 92Q60 {40 + k * 8} {100 - k * 7} 92" fill="none" stroke="{INK}" stroke-width="1.6"/>' for k in range(1, 5))
                      + f'<path d="M44 96H76" stroke="{INK}" stroke-width="3"/>' + mask(60, 58, 0.55, GOLD) + sparkle(96, 30, 5, GOLD)),
}

def book(x, y, c, w=44, h=54):
    return (f'<path d="M{x - w / 2} {y - h / 2}H{x + w / 2}V{y + h / 2}H{x - w / 2}Z" fill="{c}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x - w / 2 + 6} {y - h / 2}V{y + h / 2}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{x - w / 2 + 12} {y - h / 2 + 10}H{x + w / 2 - 6}M{x - w / 2 + 12} {y - h / 2 + 16}H{x + w / 2 - 10}" stroke="{GOLD}" stroke-width="2"/>')


def quill(x, y, s=1.0):
    return (f'<path d="M{x} {y}Q{x + 10 * s} {y - 30 * s} {x + 34 * s} {y - 50 * s}Q{x + 26 * s} {y - 20 * s} {x} {y}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
            f'<path d="M{x} {y}L{x + 28 * s} {y - 42 * s}" stroke="{INK}" stroke-width="1.2"/>')


cor = {
    "tablilla": BG + (f'<path d="M26 34H94V94H26Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/><path d="M32 40H88V88H32Z" fill="#E0B84E" stroke="{INK}" stroke-width="1.6"/>'
                      + "".join(f'<path d="M38 {50 + k * 9}H{82 - (k % 2) * 12}" stroke="{WOOD}" stroke-width="1.8"/>' for k in range(4))
                      + f'<path d="M78 98L102 60" stroke="{INK}" stroke-width="4"/><path d="M78 98L102 60" stroke="{SILVER}" stroke-width="2"/>'),
    "guia": BG + book(56, 66, "#5A3E6E") + f'<text x="56" y="92" font-family="Georgia, serif" font-weight="700" font-size="9" text-anchor="middle" fill="{GOLD}">GUÍA</text>' + sparkle(92, 32, 5, GOLD),
    "comentario": BG + book(48, 70, SEA) + quill(70, 92, 1.1) + sparkle(28, 30, 5, GOLD),
    "lucerna": BG + '<g transform="translate(12 14) scale(.8)">' + (f'<path d="M28 74Q30 56 56 56Q78 56 86 66L102 62Q104 72 92 78Q80 90 56 90Q30 90 28 74Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/>'
                     f'<circle cx="54" cy="70" r="8" fill="#7A2E1A" stroke="{INK}" stroke-width="1.6"/><path d="M28 70Q20 64 24 56" fill="none" stroke="{INK}" stroke-width="3"/>'
                     f'<path d="M100 58Q94 44 100 32Q108 44 100 58Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/></g>'),
    "astrolabio": BG + (f'<circle cx="60" cy="68" r="32" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/><circle cx="60" cy="68" r="24" fill="#E8C872" stroke="{INK}" stroke-width="1.4"/>'
                        f'<path d="M60 44V92M36 68H84" stroke="{INK}" stroke-width="1.2"/><path d="M44 52L78 86" stroke="{INK}" stroke-width="2.4"/>'
                        f'<circle cx="60" cy="68" r="3" fill="{INK}"/><path d="M52 36H68V28H52Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/><circle cx="60" cy="24" r="5" fill="none" stroke="{INK}" stroke-width="2"/>'),
    "insignia": BG + quill(32, 94, .9) + quill(48, 96, 1.1) + quill(64, 94, .9) + sparkle(96, 34, 6, GOLD) + sparkle(98, 80, 4, GOLD),
}

ORDER = {
    "malaga_picasso": (mal, [("lapiz", "El lápiz del «piz, piz»"), ("nombre", "El nombre larguísimo"), ("paloma", "La paloma de papá"),
                             ("picador", "El pequeño picador amarillo"), ("paleta", "La paleta de Picasso"), ("insignia", "¿Por qué Picasso no volvió a Málaga?")]),
    "cadiz_teatro": (cad, [("mascara", "La máscara del teatro"), ("crotalos", "Los crótalos de Telethusa"), ("anillo", "El anillo de caballero"),
                           ("versos", "Los versos de Marcial"), ("atun", "El atún de Gades"), ("insignia", "¿Quién pagó el teatro romano de Gades?")]),
    "cordoba_sabios": (cor, [("tablilla", "La tablilla de Séneca"), ("guia", "La «Guía de perplejos»"), ("comentario", "El comentario de Averroes"),
                             ("lucerna", "La lucerna romana"), ("astrolabio", "El astrolabio andalusí"), ("insignia", "¿Por qué se fueron los sabios de Córdoba?")]),
}
ART = {}
for prefix, (arts, items) in ORDER.items():
    for (key, title), ring in zip(items, (GOLD, GOLD, SEA, CLAY, GOLD, GOLD)):
        ART[f"{prefix}_{key}"] = (ring, arts[key], title)

if __name__ == "__main__":
    write(ART)
    print("coleccionables:", len(ART))
