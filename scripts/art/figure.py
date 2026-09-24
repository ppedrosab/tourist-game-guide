#!/usr/bin/env python3
"""
Personajes paramétricos (viewBox 200×260), con la misma cabeza y las mismas 8 caras que el resto.
Se describen con un diccionario: piel, pelo, barba, tocado, ropa, colores y objetos en las manos.
Lo usan los personajes de Córdoba, Huelva, Jaén, Almería y las rutas gastronómicas.

    figure(skin="#E3AE88", hair=("short", "#3A2A1E"), hat=("cordobes", "#2B2A33"),
           outfit="jacket", main="#2F3E5C", accent=GOLD, left="book", right="staff")
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import INK, CLAY, SEA, GOLD, PAPER, SHADOW, face_of, g, limb, svg

SKINS = {"clara": ("#F1C9A5", "#D4A882"), "media": ("#E3AE88", "#C58E68"), "morena": ("#C98F66", "#A8714C"),
         "oscura": ("#8E5E3E", "#6E452C"), "piedra": ("#E4DCCB", "#C4B9A2"), "bronce": ("#C9A15A", "#A07C3C")}


def shade(c, k=.78):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    r, gg, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02X%02X%02X" % (int(r * k), int(gg * k), int(b * k))


# ---------------------------------------------------------------------------
# Pelo, barba y tocados
# ---------------------------------------------------------------------------
def hair_back(style, c):
    if style == "long":
        return f'<path d="M58 80Q52 34 100 30Q148 34 142 80L148 132Q132 140 124 122L76 122Q68 140 52 132Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
    if style == "braid":
        return (f'<path d="M136 70Q150 100 142 130" fill="none" stroke="{INK}" stroke-width="13"/><path d="M136 70Q150 100 142 130" fill="none" stroke="{c}" stroke-width="9"/>'
                + "".join(f'<path d="M{137 + k} {86 + k * 12}l8 4" stroke="{INK}" stroke-width="1.2"/>' for k in range(4)))
    return ""


def hair_front(style, c):
    top = f'<path d="M60 76Q56 38 100 34Q144 38 140 76L134 76Q132 58 124 52Q112 60 96 56Q80 58 68 66L66 76Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
    if style in ("short", "long", "braid"):
        return top + f'<path d="M62 70L64 90M138 70L136 90" stroke="{c}" stroke-width="5"/>'
    if style == "bun":
        return top + f'<circle cx="100" cy="30" r="13" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
    if style == "curly":
        return top + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                             for x, y in [(66, 60), (76, 44), (92, 36), (108, 36), (124, 44), (134, 60)])
    if style == "bald":
        return (f'<path d="M60 78Q58 60 66 54L70 80Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M140 78Q142 60 134 54L130 80Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M84 44Q94 40 104 42" fill="none" stroke="#FFF" stroke-width="2.4" opacity=".4"/>')
    if style == "slick":
        return f'<path d="M60 74Q56 36 100 34Q144 36 140 74Q134 50 100 48Q70 48 60 74Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
    return ""


def beard(kind, c):
    if kind == "full":
        return (f'<path d="M62 80Q62 124 100 128Q138 124 138 80Q130 104 112 102Q100 98 88 102Q70 104 62 80Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M86 94Q100 88 114 94Q106 98 100 96Q94 98 86 94Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>')
    if kind == "short":
        return (f'<path d="M64 86Q68 116 100 118Q132 116 136 86Q126 106 100 108Q74 106 64 86Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M86 94Q100 88 114 94Q106 98 100 96Q94 98 86 94Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "moustache":
        return f'<path d="M84 95Q100 86 116 95Q108 100 100 96Q92 100 84 95Z" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
    return ""


def hat(kind, c, c2=GOLD):
    d = shade(c)
    if kind == "cordobes":   # sombrero cordobés de ala plana
        return (f'<path d="M44 50Q100 40 156 50L156 57Q100 47 44 57Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M72 50L74 22L126 22L128 50Z" fill="{c}" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M110 23L126 23L128 50L114 50Z" fill="{d}"/>'
                f'<path d="M73 42L127 42L127 48L73 48Z" fill="{c2}" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "turban":
        return (f'<path d="M58 66Q52 22 100 18Q148 22 142 66Q122 54 100 56Q78 54 58 66Z" fill="{c}" stroke="{INK}" stroke-width="2.6"/>'
                + "".join(f'<path d="M{64 + k * 4} {60 - k * 8}Q100 {44 - k * 8} {136 - k * 4} {60 - k * 8}" fill="none" stroke="{d}" stroke-width="2"/>' for k in range(4))
                + f'<circle cx="100" cy="40" r="5" fill="{c2}" stroke="{INK}" stroke-width="1.6"/>')
    if kind == "cap":       # gorra plana
        return (f'<path d="M60 60Q62 34 100 32Q138 34 140 60Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M60 60Q46 60 42 68Q70 62 104 60Z" fill="{d}" stroke="{INK}" stroke-width="2"/>')
    if kind == "kerchief":  # pañuelo a la cabeza, anudado a un lado
        return (f'<path d="M56 80Q52 30 100 28Q148 30 144 80Q138 58 124 50Q100 44 76 50Q62 58 56 80Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M140 76L154 88L146 96Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{c2}"/>' for x, y in [(80, 40), (100, 36), (120, 40), (70, 56), (130, 56)]))
    if kind == "veil":      # toca que enmarca la cara (la caída va en hat_back)
        return (f'<path d="M54 86Q48 26 100 24Q152 26 146 86L136 86Q138 42 100 40Q62 42 64 86Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M64 86Q62 42 100 40Q138 42 136 86" fill="none" stroke="{d}" stroke-width="2"/>')
    if kind == "roman":     # casco romano con cresta
        return (f'<path d="M58 72Q56 26 100 24Q144 26 142 72L132 72Q130 48 100 44Q70 48 68 72Z" fill="#B9A06A" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M58 70L56 96L66 94L68 70Z" fill="#B9A06A" stroke="{INK}" stroke-width="2"/><path d="M142 70L144 96L134 94L132 70Z" fill="#B9A06A" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M70 24Q100 -6 130 24Q100 12 70 24Z" fill="{c}" stroke="{INK}" stroke-width="2.2"/>')
    if kind == "straw":     # sombrero de paja
        return (f'<path d="M36 54Q100 38 164 54Q100 64 36 54Z" fill="#E6C77A" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M70 50Q70 20 100 20Q130 20 130 50Z" fill="#E6C77A" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M70 44Q100 38 130 44L130 50Q100 44 70 50Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "toque":     # gorro de cocinero
        return (f'<path d="M66 54L66 40Q54 26 70 16Q80 2 100 10Q120 2 130 16Q146 26 134 40L134 54Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M66 44H134" stroke="#D9CFBE" stroke-width="2"/>')
    if kind == "crown":
        return (f'<path d="M68 48L66 20L80 34L90 14L100 30L110 14L120 34L134 20L132 48Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/>'
                f'<circle cx="100" cy="40" r="4" fill="{c}" stroke="{INK}" stroke-width="1.2"/>')
    if kind == "miner":     # casco de minero con lámpara
        return (f'<path d="M58 64Q58 26 100 24Q142 26 142 64Z" fill="{c}" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M52 64H148V70H52Z" fill="{d}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M100 24V64" stroke="{d}" stroke-width="3"/>'
                f'<circle cx="100" cy="46" r="9" fill="#FFE7A8" stroke="{INK}" stroke-width="2"/>')
    if kind == "beret":     # gorra blanda de los marinos del XV
        return (f'<path d="M56 60Q52 26 100 24Q156 22 150 50Q120 44 100 48Q74 50 56 60Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M58 60Q100 46 146 52" fill="none" stroke="{d}" stroke-width="3"/>')
    if kind == "tricorn":
        return (f'<path d="M44 52Q100 20 156 52Q128 40 100 42Q72 40 44 52Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M66 44Q100 6 134 44Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>')
    if kind == "hood":      # capucha de monje (la caída va en hat_back)
        return (f'<path d="M54 86Q48 26 100 24Q152 26 146 86L136 86Q138 42 100 40Q62 42 64 86Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M64 86Q62 42 100 40Q138 42 136 86" fill="none" stroke="{d}" stroke-width="2"/>')
    if kind == "bowler":    # bombín
        return (f'<path d="M50 54Q100 44 150 54Q146 60 100 56Q54 60 50 54Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M68 52Q66 16 100 16Q134 16 132 52Z" fill="{c}" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M68 46Q100 40 132 46V52Q100 46 68 52Z" fill="{c2}" stroke="{INK}" stroke-width="1.2"/>'
                f'<path d="M82 24Q88 20 94 22" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')
    if kind == "sailor":    # gorra de marinero
        return (f'<path d="M60 54Q60 34 100 32Q140 34 140 54Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M58 54H142V62H58Z" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M58 60L48 74L56 76L64 62Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "laurel":
        return "".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3.4" transform="rotate({r} {x} {y})" fill="#6E9A4E" stroke="{INK}" stroke-width="1.2"/>'
                       for x, y, r in [(66, 58, -60), (72, 46, -40), (82, 38, -20), (118, 38, 20), (128, 46, 40), (134, 58, 60)])
    if kind == "flower":    # flor en el pelo
        return (f'<circle cx="132" cy="46" r="9" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
                f'<circle cx="132" cy="46" r="3.4" fill="{c2}"/>')
    return ""


def hat_back(kind, c, c2=GOLD):
    """Parte de la toca o la capucha que cae por detrás de la cabeza hasta los hombros."""
    if kind in ("veil", "hood"):
        return f'<path d="M54 84Q48 26 100 24Q152 26 146 84L154 128Q126 118 100 118Q74 118 46 128Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>'
    return ""


# ---------------------------------------------------------------------------
# Objetos en las manos (x, y = centro de la mano)
# ---------------------------------------------------------------------------
def prop(kind, x, y, side):
    s = -1 if side == "left" else 1
    if kind == "book":
        return (f'<path d="M{x - 22} {y - 6}L{x} {y - 12}L{x + 4} {y + 12}L{x - 18} {y + 18}Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 16} {y - 2}L{x - 4} {y - 5}" stroke="{GOLD}" stroke-width="1.6"/>')
    if kind == "scroll":
        return (f'<path d="M{x - 14} {y - 20}H{x + 10}V{y + 20}H{x - 14}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 17} {y - 22}H{x + 13}M{x - 17} {y + 22}H{x + 13}" stroke="#8A6243" stroke-width="4"/>'
                + "".join(f'<path d="M{x - 10} {y - 12 + k * 7}H{x + 6}" stroke="#8A7A62" stroke-width="1.2"/>' for k in range(5)))
    if kind == "staff":
        return f'<path d="M{x} {y - 110}V{y + 96}" stroke="{INK}" stroke-width="7"/><path d="M{x} {y - 110}V{y + 96}" stroke="#8A6243" stroke-width="4"/>'
    if kind == "basket":
        return (f'<path d="M{x - 22} {y + 4}Q{x} {y - 30} {x + 22} {y + 4}" fill="none" stroke="#8A6243" stroke-width="3.4"/>'
                f'<path d="M{x - 24} {y + 4}H{x + 24}L{x + 18} {y + 28}H{x - 18}Z" fill="#C9A05E" stroke="{INK}" stroke-width="2"/>'
                + "".join(f'<path d="M{x - 20 + k * 8} {y + 6}V{y + 26}" stroke="#A07C3C" stroke-width="1.2"/>' for k in range(6)))
    if kind == "jug":       # jarra/cántaro
        return (f'<path d="M{x - 10} {y - 18}H{x + 10}L{x + 8} {y - 12}Q{x + 20} {y} {x + 12} {y + 22}H{x - 12}Q{x - 20} {y} {x - 8} {y - 12}Z" fill="#C9763F" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 12} {y + 4}H{x + 12}" stroke="{PAPER}" stroke-width="2"/>')
    if kind == "bottle":
        return (f'<path d="M{x - 4} {y - 32}H{x + 4}V{y - 20}Q{x + 10} {y - 14} {x + 10} {y - 6}V{y + 22}H{x - 10}V{y - 6}Q{x - 10} {y - 14} {x - 4} {y - 20}Z" fill="#4F6B3A" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 8} {y}H{x + 8}V{y + 10}H{x - 8}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    if kind == "glass":     # catavinos
        return (f'<path d="M{x - 7} {y - 26}Q{x - 9} {y - 10} {x} {y - 8}Q{x + 9} {y - 10} {x + 7} {y - 26}Z" fill="#E9C46A" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M{x} {y - 8}V{y + 4}M{x - 6} {y + 4}H{x + 6}" stroke="{INK}" stroke-width="1.8"/>')
    if kind == "ladle":
        return (f'<path d="M{x} {y}L{x + s * 6} {y - 44}" stroke="#8A6243" stroke-width="4"/>'
                f'<ellipse cx="{x + s * 8}" cy="{y - 50}" rx="9" ry="6" fill="#8A6243" stroke="{INK}" stroke-width="1.8"/>')
    if kind == "pan":       # sartén/perol
        return (f'<path d="M{x} {y}L{x + s * 14} {y - 4}" stroke="{INK}" stroke-width="5"/>'
                f'<ellipse cx="{x + s * 30}" cy="{y - 6}" rx="16" ry="7" fill="#3A3A42" stroke="{INK}" stroke-width="2"/>'
                f'<ellipse cx="{x + s * 30}" cy="{y - 8}" rx="11" ry="3.4" fill="#E0A04A"/>')
    if kind == "plate":
        return (f'<ellipse cx="{x}" cy="{y - 4}" rx="24" ry="7" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                f'<ellipse cx="{x}" cy="{y - 7}" rx="14" ry="4" fill="#D9824A"/>')
    if kind == "bowl":
        return (f'<path d="M{x - 20} {y - 8}H{x + 20}Q{x + 18} {y + 12} {x} {y + 12}Q{x - 18} {y + 12} {x - 20} {y - 8}Z" fill="#C9763F" stroke="{INK}" stroke-width="2"/>'
                f'<ellipse cx="{x}" cy="{y - 8}" rx="20" ry="4" fill="#E8744A" stroke="{INK}" stroke-width="1.6"/>')
    if kind == "fan":
        return (f'<path d="M{x} {y}L{x + s * 30} {y - 30}Q{x + s * 40} {y - 8} {x + s * 34} {y + 10}Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/>'
                + "".join(f'<path d="M{x} {y}L{x + s * (30 + k * 2)} {y - 30 + k * 12}" stroke="{PAPER}" stroke-width="1"/>' for k in range(4)))
    if kind == "sword":
        return (f'<path d="M{x} {y}L{x + s * 4} {y - 70}" stroke="{INK}" stroke-width="6"/><path d="M{x} {y}L{x + s * 4} {y - 70}" stroke="#C9CED6" stroke-width="3.4"/>'
                f'<path d="M{x - 10} {y - 4}H{x + 10}" stroke="{GOLD}" stroke-width="4"/>')
    if kind == "lantern":
        return (f'<path d="M{x} {y}V{y + 10}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 10} {y + 10}H{x + 10}L{x + 8} {y + 34}H{x - 8}Z" fill="#FFE7A8" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 12} {y + 10}L{x} {y + 2}L{x + 12} {y + 10}Z" fill="#2E3A48"/>')
    if kind == "olive":     # rama de olivo
        return (f'<path d="M{x} {y}Q{x + s * 12} {y - 30} {x + s * 6} {y - 56}" fill="none" stroke="#6E4C33" stroke-width="2.6"/>'
                + "".join(f'<ellipse cx="{x + s * (6 + (k % 2) * 8 - 4)}" cy="{y - 10 - k * 9}" rx="7" ry="2.8" transform="rotate({s * (30 if k % 2 else -30)} {x + s * (6 + (k % 2) * 8 - 4)} {y - 10 - k * 9})" fill="#6E8A4E" stroke="{INK}" stroke-width=".9"/>' for k in range(5))
                + "".join(f'<circle cx="{x + s * (2 + k * 5)}" cy="{y - 20 - k * 12}" r="3" fill="#3E4A2A"/>' for k in range(3)))
    if kind == "fish":
        return (f'<path d="M{x - 26} {y}Q{x - 6} {y - 14} {x + 18} {y}Q{x - 6} {y + 14} {x - 26} {y}Z" fill="#9FB6BF" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x + 16} {y}L{x + 28} {y - 10}V{y + 10}Z" fill="#9FB6BF" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="{x - 18}" cy="{y - 2}" r="1.8" fill="{INK}"/>')
    if kind == "shrimp":    # gamba
        return (f'<path d="M{x - 18} {y - 4}Q{x} {y - 26} {x + 18} {y - 6}Q{x + 8} {y + 6} {x - 4} {y}Q{x - 14} {y + 8} {x - 18} {y - 4}Z" fill="#E8744A" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x + 14} {y - 10}L{x + 30} {y - 26}M{x + 16} {y - 8}L{x + 34} {y - 18}" stroke="{INK}" stroke-width="1.2"/>')
    if kind == "compass":   # astrolabio/brújula
        return (f'<circle cx="{x}" cy="{y - 6}" r="16" fill="{GOLD}" stroke="{INK}" stroke-width="2.2"/>'
                f'<circle cx="{x}" cy="{y - 6}" r="10" fill="none" stroke="{INK}" stroke-width="1.2"/>'
                f'<path d="M{x - 12} {y - 6}H{x + 12}M{x} {y - 18}V{y + 6}" stroke="{INK}" stroke-width="1.4"/>'
                f'<path d="M{x - 6} {y - 12}L{x + 6} {y}" stroke="{CLAY}" stroke-width="2.4"/>')
    if kind == "pick":      # pico de minero
        return (f'<path d="M{x} {y + 30}L{x + s * 4} {y - 40}" stroke="#8A6243" stroke-width="5"/>'
                f'<path d="M{x - 26} {y - 34}Q{x + s * 4} {y - 54} {x + 30} {y - 34}Q{x + s * 4} {y - 44} {x - 26} {y - 34}Z" fill="#8C939C" stroke="{INK}" stroke-width="2"/>')
    if kind == "hammer":
        return (f'<path d="M{x} {y + 10}L{x + s * 4} {y - 34}" stroke="#8A6243" stroke-width="5"/>'
                f'<path d="M{x - 10} {y - 44}H{x + 16}V{y - 32}H{x - 10}Z" fill="#8C939C" stroke="{INK}" stroke-width="2"/>')
    if kind == "trowel":    # paleta de albañil
        return (f'<path d="M{x} {y}L{x + s * 10} {y - 16}" stroke="#8A6243" stroke-width="4"/>'
                f'<path d="M{x + s * 8} {y - 14}L{x + s * 32} {y - 34}L{x + s * 22} {y - 10}Z" fill="#8C939C" stroke="{INK}" stroke-width="1.8"/>')
    if kind == "flower":
        return (f'<path d="M{x} {y}L{x + s * 4} {y - 34}" stroke="#4F8B5A" stroke-width="2.4"/>'
                f'<circle cx="{x + s * 4}" cy="{y - 38}" r="8" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/><circle cx="{x + s * 4}" cy="{y - 38}" r="3" fill="{GOLD}"/>')
    if kind == "tomato":
        return (f'<circle cx="{x}" cy="{y - 8}" r="12" fill="#D8412F" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 6} {y - 20}L{x} {y - 16}L{x + 6} {y - 20}M{x} {y - 16}V{y - 24}" stroke="#4F8B5A" stroke-width="2.4"/>')
    if kind == "ham":       # jamón (pata)
        return (f'<path d="M{x - 8} {y + 8}Q{x - 26} {y - 30} {x + 2} {y - 46}Q{x + 26} {y - 34} {x + 10} {y + 4}Z" fill="#A8432F" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 8} {y + 8}L{x - 12} {y + 26}" stroke="#E9DCC0" stroke-width="5"/><path d="M{x - 8} {y + 8}L{x - 12} {y + 26}" stroke="{INK}" stroke-width="1" opacity=".4"/>')
    if kind == "oil":       # aceitera
        return (f'<path d="M{x - 12} {y + 16}H{x + 12}L{x + 8} {y - 12}H{x - 8}Z" fill="#C9CED6" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x + 8} {y - 8}L{x + 24} {y - 22}" stroke="{INK}" stroke-width="3"/>'
                f'<path d="M{x - 8} {y}H{x + 9}V{y + 10}H{x - 10}Z" fill="#B7A23A"/>')
    if kind == "net":
        return (f'<path d="M{x - 26} {y - 30}Q{x} {y - 40} {x + 26} {y - 30}L{x + 16} {y + 20}H{x - 16}Z" fill="#C9B48A" fill-opacity=".35" stroke="{INK}" stroke-width="1.8"/>'
                + "".join(f'<path d="M{x - 22 + k * 9} {y - 32}L{x - 14 + k * 6} {y + 20}" stroke="#8A7A62" stroke-width="1"/>' for k in range(6))
                + "".join(f'<path d="M{x - 24} {y - 22 + k * 10}H{x + 24}" stroke="#8A7A62" stroke-width="1"/>' for k in range(4)))
    if kind == "quill":
        return f'<path d="M{x} {y}L{x + s * 16} {y - 36}Q{x + s * 22} {y - 42} {x + s * 20} {y - 30}Q{x + s * 12} {y - 10} {x + s * 2} {y - 2}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
    if kind == "bread":
        return (f'<ellipse cx="{x}" cy="{y - 6}" rx="22" ry="11" fill="#D9A45E" stroke="{INK}" stroke-width="2"/>'
                + "".join(f'<path d="M{x - 12 + k * 10} {y - 14}l6 8" stroke="#A8743C" stroke-width="2"/>' for k in range(3)))
    if kind == "pomegranate":
        return (f'<circle cx="{x}" cy="{y - 8}" r="12" fill="#B8323A" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 4} {y - 22}L{x} {y - 18}L{x + 4} {y - 22}V{y - 16}H{x - 4}Z" fill="#B8323A" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "ball":      # balón de cuero de 1889
        return (f'<circle cx="{x}" cy="{y - 10}" r="15" fill="#B9793E" stroke="{INK}" stroke-width="2.2"/>'
                f'<path d="M{x - 14} {y - 14}Q{x} {y - 4} {x + 14} {y - 14}M{x - 12} {y - 2}Q{x} {y - 10} {x + 12} {y - 2}M{x} {y - 25}V{y + 5}" fill="none" stroke="#7A4A22" stroke-width="1.6"/>'
                f'<path d="M{x - 3} {y - 20}h6M{x - 3} {y - 16}h6" stroke="{PAPER}" stroke-width="1.4"/>')
    if kind == "cuttlefish":  # choco (en la mano derecha se da la vuelta para no salirse del marco)
        body = (f'<path d="M{x - 20} {y - 8}Q{x - 4} {y - 24} {x + 16} {y - 12}Q{x + 20} {y - 8} {x + 16} {y - 2}Q{x - 4} {y + 8} {x - 20} {y - 4}Z" fill="#C7B39A" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 18} {y - 10}Q{x} {y - 20} {x + 14} {y - 10}" fill="none" stroke="#A89274" stroke-width="1.4"/>'
                + "".join(f'<path d="M{x + 14} {y - 8 + k * 3}q10 {k - 2} 16 {k * 2 - 3}" fill="none" stroke="#C7B39A" stroke-width="3"/>' for k in range(4))
                + f'<circle cx="{x + 8}" cy="{y - 10}" r="2" fill="{INK}"/>')
        return body if side == "left" else f'<g transform="translate({2 * x} 0) scale(-1 1)">{body}</g>'
    if kind == "strawberries":
        return (f'<path d="M{x - 24} {y + 4}H{x + 24}L{x + 18} {y + 26}H{x - 18}Z" fill="#E9DCC0" stroke="{INK}" stroke-width="2"/>'
                + "".join(f'<path d="M{x + dx - 5} {y + dy}Q{x + dx} {y + dy + 12} {x + dx + 5} {y + dy}Z" fill="#D8412F" stroke="{INK}" stroke-width="1"/><path d="M{x + dx - 4} {y + dy}L{x + dx} {y + dy - 3}L{x + dx + 4} {y + dy}" stroke="#4F8B5A" stroke-width="1.6"/>'
                          for dx, dy in [(-14, 2), (-4, 0), (6, 2), (15, 1), (-9, -4), (1, -5), (11, -4)]))
    if kind == "knife":     # cuchillo jamonero
        return (f'<path d="M{x} {y}L{x + s * 4} {y - 16}" stroke="#2B2A33" stroke-width="5"/>'
                f'<path d="M{x + s * 3} {y - 14}L{x + s * 10} {y - 56}L{x + s * 12} {y - 54}L{x + s * 7} {y - 12}Z" fill="#D9DEE4" stroke="{INK}" stroke-width="1.4"/>')
    if kind == "bag":       # maletín de médico
        return (f'<path d="M{x - 20} {y + 2}H{x + 20}L{x + 18} {y + 26}H{x - 18}Z" fill="#4A2E22" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{x - 8} {y + 2}Q{x} {y - 8} {x + 8} {y + 2}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M{x - 20} {y + 10}H{x + 20}" stroke="{GOLD}" stroke-width="1.6"/>')
    if kind == "lute":      # laúd
        return (f'<path d="M{x - 6} {y + 4}L{x + s * 30} {y - 40}" stroke="#6E4C33" stroke-width="5"/>'
                f'<path d="M{x + s * 26} {y - 36}L{x + s * 36} {y - 50}" stroke="#6E4C33" stroke-width="6"/>'
                f'<ellipse cx="{x - s * 6}" cy="{y + 10}" rx="17" ry="21" transform="rotate({s * 40} {x - s * 6} {y + 10})" fill="#C98F4E" stroke="{INK}" stroke-width="2.2"/>'
                f'<circle cx="{x - s * 4}" cy="{y + 6}" r="4" fill="#5B3A26"/>')
    if kind == "dornillo":  # cuenco de madera con su mano de mortero
        return (f'<path d="M{x - 22} {y - 8}H{x + 22}Q{x + 20} {y + 14} {x} {y + 14}Q{x - 20} {y + 14} {x - 22} {y - 8}Z" fill="#9A6B45" stroke="{INK}" stroke-width="2"/>'
                f'<ellipse cx="{x}" cy="{y - 8}" rx="22" ry="5" fill="#E8744A" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{x + 6} {y - 8}L{x + 18} {y - 34}" stroke="{INK}" stroke-width="7"/><path d="M{x + 6} {y - 8}L{x + 18} {y - 34}" stroke="#C9A77E" stroke-width="4"/>')
    return ""


# ---------------------------------------------------------------------------
# Ropa
# ---------------------------------------------------------------------------
def clothes(outfit, main, accent, second):
    d = shade(main)
    if outfit in ("tunic", "toga", "habit"):
        s = (f'<path d="M72 116Q100 104 128 116L138 244L62 244Z" fill="{main}" stroke="{INK}" stroke-width="2.8"/>'
             f'<path d="M104 110Q120 110 128 116L138 244L112 244Z" fill="{d}"/>'
             f'<path d="M84 124Q82 180 76 240M116 124Q118 180 124 240" fill="none" stroke="{d}" stroke-width="1.8"/>'
             f'<path d="M70 168Q100 176 130 168" fill="none" stroke="{accent}" stroke-width="5"/>')
        if outfit == "toga":
            s += (f'<path d="M72 118Q96 150 132 206L124 214Q92 170 70 130Z" fill="{second}" stroke="{INK}" stroke-width="2"/>'
                  f'<path d="M78 122L126 124" stroke="{accent}" stroke-width="3"/>')
        return s
    if outfit == "dress":
        return (f'<path d="M74 118Q100 106 126 118L142 244L58 244Z" fill="{main}" stroke="{INK}" stroke-width="2.8"/>'
                f'<path d="M104 112Q120 112 126 118L142 244L114 244Z" fill="{d}"/>'
                f'<path d="M62 214Q100 226 138 214L142 244L58 244Z" fill="{second}" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M84 118L100 138L116 118" fill="none" stroke="{accent}" stroke-width="3"/>')
    if outfit in ("jacket", "shirt", "armor", "vest"):
        legs = (f'<path d="M82 200L118 200L117 238L104 238L100 218L96 238L83 238Z" fill="{second}" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M78 248Q80 240 92 240Q98 241 98 248Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M102 248Q102 241 108 240Q120 240 122 248Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>')
        torso = (f'<path d="M72 118Q100 106 128 118L132 204L68 204Z" fill="{main}" stroke="{INK}" stroke-width="2.8"/>'
                 f'<path d="M104 112Q120 112 128 118L132 204L112 204Z" fill="{d}"/>')
        if outfit == "jacket":
            torso += (f'<path d="M88 116L112 116L110 190L100 196L90 190Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M84 116L94 150L80 140Z" fill="{d}" stroke="{INK}" stroke-width="1.8"/><path d="M116 116L106 150L120 140Z" fill="{d}" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M92 118L100 128L108 118L100 122Z" fill="{accent}" stroke="{INK}" stroke-width="1.4"/>')
        if outfit == "shirt":
            torso += (f'<path d="M92 112L100 128L108 112" fill="none" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M68 172L132 172L133 188L67 188Z" fill="{accent}" stroke="{INK}" stroke-width="2"/>')
        if outfit == "vest":
            torso += (f'<path d="M92 112L100 128L108 112" fill="none" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M74 120L94 118L96 200L70 200Z" fill="{accent}" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M126 120L106 118L104 200L130 200Z" fill="{shade(accent)}" stroke="{INK}" stroke-width="1.8"/>')
        if outfit == "armor":   # lóriga de bandas y faldón de tiras
            torso = (f'<path d="M72 188L128 188L132 222L68 222Z" fill="{main}" stroke="{INK}" stroke-width="2.2"/>'
                     + "".join(f'<path d="M{x} 190V220" stroke="{INK}" stroke-width="1.4"/>' for x in range(78, 128, 8))
                     + f'<path d="M72 118Q100 106 128 118L130 192L70 192Z" fill="#B7BDC6" stroke="{INK}" stroke-width="2.8"/>'
                     + "".join(f'<path d="M71 {y}Q100 {y + 6} 129 {y}" fill="none" stroke="{INK}" stroke-width="1.4"/>' for y in (136, 152, 168, 182))
                     + f'<path d="M104 112Q120 112 128 118L130 192L112 192Z" fill="#8C939C" opacity=".5"/>')
        return legs + torso
    return ""


def figure(skin="media", eyes="#3A2A1E", hair=("short", "#3A2A1E"), beard_=None, hat_=None, outfit="jacket",
           main=SEA, accent=GOLD, second="#3A3A48", apron=None, sleeves=None, left=None, right=None,
           raise_right=False, extra="", extra_back="", neck=None):
    """Devuelve build(expresión) → SVG."""
    sk, skd = SKINS[skin] if skin in SKINS else (skin, shade(skin))
    sleeve = sleeves or main
    back = g("back", hair_back(*hair) if hair else "", hat_back(*hat_) if hat_ else "", extra_back)
    body = clothes(outfit, main, accent, second)
    if apron:
        body += (f'<path d="M80 150H120L124 {236 if outfit in ("dress", "tunic", "toga", "habit") else 204}H76Z" fill="{apron}" stroke="{INK}" stroke-width="2"/>'
                 f'<path d="M74 152Q100 160 126 152" fill="none" stroke="{apron}" stroke-width="3"/>')
    if neck:
        body += f'<path d="M86 112Q100 124 114 112L112 120Q100 130 88 120Z" fill="{neck}" stroke="{INK}" stroke-width="1.8"/>'
    body = g("body", body)
    lh = (58, 156)
    rh = (150, 96) if raise_right else (146, 150)
    rpath = "M124 124Q142 116 150 98" if raise_right else "M124 124Q142 132 146 148"
    arms = g("arms",
             limb("M76 124Q60 136 58 154", sleeve, 12), limb(rpath, sleeve, 12),
             prop(left, *lh, "left") if left else "", prop(right, *rh, "right") if right else "",
             f'<circle cx="{lh[0]}" cy="{lh[1]}" r="6" fill="{sk}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="{rh[0]}" cy="{rh[1]}" r="6" fill="{sk}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{sk}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{sk}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{skd}" opacity=".5"/>',
             hair_front(*hair) if hair else "", beard(*beard_) if beard_ else "", hat(*hat_) if hat_ else "", extra)
    rim = g("rim", f'<path d="M70 126L66 {236 if outfit in ("dress", "tunic", "toga", "habit") else 200}" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    return lambda e: svg(e, [SHADOW, back, body, arms, head, face_of(e).replace("#5A3A22", eyes), rim])
