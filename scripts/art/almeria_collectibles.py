#!/usr/bin/env python3
"""
Coleccionables de Almería (medallón 120×124). Aro: oro = comunes; historia: mar = la Alcazaba,
arcilla = la medina; gastronomía: mar = el puerto, arcilla = la Chanca.

Uso: python3 scripts/art/almeria_collectibles.py && npm run gen:assets
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, frame, sparkle, waves, write

BG = '<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
SKY = f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
OCHRE = "#D9B06A"; OCHRED = "#B8904E"; SILK = "#C0476A"; RED = "#D8412F"; LEAF = "#4F8B5A"


def merlons(x0, x1, y, c=OCHRE, step=10):
    return "".join(f'<path d="M{x} {y}V{y - 7}H{x + 6}V{y}" fill="{c}" stroke="{INK}" stroke-width="1.2"/>' for x in range(int(x0), int(x1) - 5, step))


cuerno = (SKY + waves(90)
          + f'<path d="M26 78Q40 40 84 28L92 44Q54 50 38 84Z" fill="#E9DCC0" stroke="{INK}" stroke-width="2.4"/>'
          f'<ellipse cx="88" cy="36" rx="6" ry="10" transform="rotate(-20 88 36)" fill="#C9B48A" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M{x} {y}l6 8" stroke="#8A6243" stroke-width="2.4"/>' for x, y in [(44, 52), (56, 42), (68, 36)])
          + "".join(f'<path d="M{96 + k * 4} {26 - k * 6}q6 -2 8 -8" fill="none" stroke="{INK}" stroke-width="1.6"/>' for k in range(2)))

seda = (BG + f'<path d="M20 44H82V78H20Z" fill="{SILK}" stroke="{INK}" stroke-width="2.4"/>'
        f'<ellipse cx="82" cy="61" rx="9" ry="17" fill="#D96A8C" stroke="{INK}" stroke-width="2"/><ellipse cx="82" cy="61" rx="3" ry="6" fill="{SILK}"/>'
        f'<path d="M20 78Q14 98 34 104Q60 108 86 100" fill="none" stroke="{SILK}" stroke-width="10"/>'
        + "".join(f'<path d="M26 {52 + k * 8}H76" stroke="{GOLD}" stroke-width="1.6"/>' for k in range(3))
        + "".join(f'<path d="M{30 + k * 12} 52l4 4l4 -4" fill="none" stroke="{PAPER}" stroke-width="1.2"/>' for k in range(4)) + sparkle(96, 30, 6))

alcazaba = (SKY + f'<path d="M0 100Q40 70 60 72Q86 74 120 96V124H0Z" fill="#B8904E"/>'
            + f'<path d="M14 84V58H106V84Z" fill="{OCHRE}" stroke="{INK}" stroke-width="2.2"/>' + merlons(14, 106, 58)
            + f'<path d="M66 60V28H92V60Z" fill="{OCHRE}" stroke="{INK}" stroke-width="2.2"/>' + merlons(66, 92, 28, OCHRE, 9)
            + f'<path d="M22 64V40H40V64Z" fill="{OCHRE}" stroke="{INK}" stroke-width="2"/>' + merlons(22, 40, 40, OCHRE, 8)
            + f'<path d="M76 42H82V52H76Z" fill="{INK}"/><path d="M50 84V72Q54 66 58 72V84Z" fill="#5E4232"/>')

muralla = (SKY + f'<path d="M-10 110Q30 40 70 60Q100 76 130 30V124H-10Z" fill="#C9A77E"/>'
           + f'<path d="M-4 100L30 66L70 76L110 40" fill="none" stroke="{INK}" stroke-width="12"/><path d="M-4 100L30 66L70 76L110 40" fill="none" stroke="{OCHRE}" stroke-width="8"/>'
           + "".join(f'<path d="M{x - 7} {y}V{y - 22}H{x + 7}V{y}Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.8"/>' + merlons(x - 7, x + 7, y - 22, OCHRE, 5) for x, y in [(30, 66), (70, 76), (100, 48)])
           + f'<path d="M106 18V32M102 22H110" stroke="{INK}" stroke-width="2"/>')

telar = (BG + f'<path d="M20 30V104M100 30V104" stroke="{INK}" stroke-width="7"/><path d="M20 30V104M100 30V104" stroke="{WOODL}" stroke-width="4"/>'
         f'<path d="M16 34H104M16 92H104" stroke="{INK}" stroke-width="6"/><path d="M16 34H104M16 92H104" stroke="{WOOD}" stroke-width="3"/>'
         + "".join(f'<path d="M{x} 36V90" stroke="#E9DCC0" stroke-width="1.2"/>' for x in range(26, 98, 5))
         + f'<path d="M24 52H96V76H24Z" fill="{SILK}" stroke="{INK}" stroke-width="1.6"/>'
         + "".join(f'<path d="M{30 + k * 13} 58l6 6l6 -6l-6 12Z" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for k in range(5))
         + f'<path d="M34 82L86 82" stroke="{WOOD}" stroke-width="5"/>')

aljibe = ('<rect x="0" y="0" width="120" height="124" fill="#8A6A4E"/>'
          + "".join(f'<path d="M{x} 110V56Q{x + 17} 30 {x + 34} 56V110" fill="#B58E68" stroke="{INK}" stroke-width="2"/>' for x in (8, 43, 78))
          + f'<path d="M0 92H120V124H0Z" fill="#6E9FA0"/>'
          + "".join(f'<path d="M{x} 100q6 -3 12 0" fill="none" stroke="#DDEFF0" stroke-width="1.6"/>' for x in (20, 54, 86))
          + "".join(f'<rect x="{x}" y="{y}" width="8" height="4" fill="#9E7654" stroke="{INK}" stroke-width=".5"/>' for x in range(10, 110, 12) for y in (22, 30)))

moneda = (BG + f'<circle cx="60" cy="62" r="36" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>'
          f'<circle cx="60" cy="62" r="29" fill="none" stroke="{GOLDD}" stroke-width="2"/>'
          + "".join(f'<circle cx="{60 + 32 * math.cos(math.radians(a)):.1f}" cy="{62 + 32 * math.sin(math.radians(a)):.1f}" r="1.4" fill="{GOLDD}"/>' for a in range(0, 360, 20))
          + f'<path d="M42 52Q50 44 58 52T74 52" fill="none" stroke="{INK}" stroke-width="2.4"/>'
          f'<path d="M44 64H76M48 74Q60 80 72 74" fill="none" stroke="{INK}" stroke-width="2.4"/><circle cx="60" cy="44" r="2" fill="{INK}"/>'
          + sparkle(94, 30, 6))

atalaya = (f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>' + waves(96, SEA, "#2F6F73")
           + f'<path d="M0 96Q30 70 58 70Q80 72 92 96Z" fill="#8A6A4E"/>'
           + f'<path d="M40 76V36H66V76Z" fill="{OCHRE}" stroke="{INK}" stroke-width="2.2"/>' + merlons(40, 66, 36, OCHRE, 7)
           + f'<path d="M50 50H56V60H50Z" fill="#FFE7A8"/>'
           + "".join(f'<path d="M58 54L{58 + 60 * math.cos(math.radians(a)):.0f} {54 + 60 * math.sin(math.radians(a)):.0f}" stroke="#FFE7A8" stroke-width="2" opacity=".5"/>' for a in (-20, -8, 4))
           + "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{PAPER}"/>' for x, y in [(20, 24), (96, 20), (84, 40), (30, 44)]))

# --- gastronomía ---
tomate = (BG + f'<path d="M24 64Q24 36 60 34Q96 36 96 64Q96 96 60 98Q24 96 24 64Z" fill="{RED}" stroke="{INK}" stroke-width="2.6"/>'
          f'<path d="M36 48Q44 40 54 42" fill="none" stroke="#FFF" stroke-width="3" opacity=".4"/>'
          f'<path d="M44 36L52 42L60 32L68 42L76 36L70 46H50Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.8"/><path d="M60 32V22" stroke="{LEAF}" stroke-width="4"/>'
          + "".join(f'<path d="M{x} 60Q{x + 2} 80 {x} 94" fill="none" stroke="#B8322A" stroke-width="1.6" opacity=".6"/>' for x in (44, 60, 76)))

uva = (BG + f'<path d="M60 26V38" stroke="#6E4C33" stroke-width="4"/><path d="M62 30Q80 18 92 30Q80 38 64 34Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.6"/>'
       + "".join(f'<circle cx="{60 + dx}" cy="{44 + dy}" r="8" fill="#C9D97A" stroke="{INK}" stroke-width="1.6"/><circle cx="{58 + dx}" cy="{41 + dy}" r="2" fill="#FFF" opacity=".6"/>'
                 for dx, dy in [(-16, 4), (0, 2), (16, 4), (-8, 16), (8, 16), (-16, 28), (0, 30), (16, 28), (-8, 42), (8, 42), (0, 54)]))

barril = (SKY + waves(96)
          + f'<path d="M34 28Q24 62 34 96H86Q96 62 86 28Z" fill="#B07A45" stroke="{INK}" stroke-width="2.6"/>'
          + "".join(f'<path d="M{x} 30Q{x - 4 if x < 60 else x + 4} 62 {x} 94" fill="none" stroke="#8A5A30" stroke-width="1.6"/>' for x in (46, 60, 74))
          + f'<path d="M29 46H91M29 78H91" stroke="#4A4A55" stroke-width="4"/>'
          f'<ellipse cx="60" cy="28" rx="26" ry="6" fill="#C9935A" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#C9D97A" stroke="{INK}" stroke-width="1"/>' for x, y in [(52, 24), (60, 22), (68, 25)]))

cable = (SKY + waves(94)
         + f'<path d="M-10 60L60 48H120V58H60L-10 72Z" fill="#7A5236" stroke="{INK}" stroke-width="2"/>'
         + "".join(f'<path d="M{x} {54 if x > 60 else 60 - (60 - x) * .12}V108" stroke="{INK}" stroke-width="5"/><path d="M{x} {54 if x > 60 else 60 - (60 - x) * .12}V108" stroke="#8C4A2E" stroke-width="2.6"/>' for x in (10, 34, 58, 82, 106))
         + "".join(f'<path d="M{x} 58L{x + 24} 108M{x + 24} 58L{x} 108" stroke="#8C4A2E" stroke-width="1.4"/>' for x in (10, 34, 58, 82))
         + f'<path d="M70 48V28H100V48" fill="#8C4A2E" stroke="{INK}" stroke-width="1.8"/>')

gurullos = (BG + f'<path d="M16 56H104Q102 98 60 100Q18 98 16 56Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
            f'<ellipse cx="60" cy="56" rx="44" ry="12" fill="#D98A4A" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3.2" ry="1.8" fill="#F2E3C4" stroke="{INK}" stroke-width=".6"/>' for x, y in [(30, 54), (38, 58), (46, 52), (54, 58), (62, 54), (70, 58), (78, 53), (86, 57), (42, 62), (66, 62), (50, 48), (74, 49)])
            + f'<path d="M82 22Q90 32 84 44" fill="none" stroke="#CCC" stroke-width="3" opacity=".7"/>')

gamba = (SKY + f'<ellipse cx="60" cy="92" rx="44" ry="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M26 80Q20 44 58 36Q88 30 96 54Q84 50 72 56Q88 70 68 80Q52 68 44 74Q40 84 26 80Z" fill="#D8412F" stroke="{INK}" stroke-width="2.4"/>'
         + "".join(f'<path d="M{x} {y}q4 6 0 12" fill="none" stroke="#A82E22" stroke-width="1.6"/>' for x, y in [(46, 42), (56, 38), (66, 38)])
         + f'<path d="M90 50L112 22M92 54L114 36" stroke="{INK}" stroke-width="1.4"/><circle cx="88" cy="48" r="2" fill="{INK}"/>'
         f'<path d="M26 80L14 88L20 76Z" fill="#D8412F" stroke="{INK}" stroke-width="1.6"/>')

invernadero = ('<rect x="0" y="0" width="120" height="124" fill="#F3D9A8"/>'
               + f'<path d="M0 90H120V124H0Z" fill="#D9B97A"/>'
               + "".join(f'<path d="M{x} 90V62Q{x + 20} 48 {x + 40} 62V90Z" fill="#EEF2F2" fill-opacity=".85" stroke="{INK}" stroke-width="1.6"/>' for x in (6, 42, 78))
               + "".join(f'<path d="M{x} 90V58" stroke="{SILVERD}" stroke-width="1"/>' for x in range(14, 118, 9))
               + "".join(f'<circle cx="{x}" cy="{84 - (x % 3) * 4}" r="3" fill="{RED}"/><path d="M{x} 88V{80 - (x % 3) * 4}" stroke="{LEAF}" stroke-width="2"/>' for x in range(16, 112, 12))
               + f'<circle cx="92" cy="30" r="12" fill="#FFF3C4"/>')

huerta = (f'<rect x="0" y="0" width="120" height="124" fill="#F3D9A8"/>'
          + f'<path d="M0 70Q40 58 80 66T120 62V124H0Z" fill="#EEF2F2"/>'
          + "".join(f'<path d="M{x} 70Q{x + 8} 62 {x + 16} 70" fill="none" stroke="{SILVERD}" stroke-width="1.2"/>' for x in range(0, 120, 16))
          + f'<path d="M0 88Q40 78 80 86T120 82V124H0Z" fill="#E4EAEA"/>'
          + f'<path d="M22 70Q22 44 60 42Q98 44 98 70Q98 100 60 102Q22 100 22 70Z" fill="{RED}" stroke="{INK}" stroke-width="2.6" transform="translate(12 6) scale(.8)"/>'
          + f'<path d="M50 44L56 48L62 40L68 48L74 44L70 52H54Z" fill="{LEAF}" stroke="{INK}" stroke-width="1.6"/>'
          + f'<circle cx="94" cy="26" r="11" fill="#FFF3C4"/>' + sparkle(24, 30, 6, GOLD))

ART = {
    "almeria_cuerno": (GOLD, cuerno, "El cuerno del vigía"),
    "almeria_seda": (GOLD, seda, "La seda de Almería"),
    "almeria_alcazaba": (SEA, alcazaba, "La Alcazaba"),
    "almeria_muralla": (SEA, muralla, "La muralla de Jayrán"),
    "almeria_telar": (CLAY, telar, "El telar"),
    "almeria_aljibe": (CLAY, aljibe, "El aljibe"),
    "almeria_moneda": (GOLD, moneda, "La moneda de al-Mariyya"),
    "almeria_atalaya": (GOLD, atalaya, "¿Qué significa Almería?"),
    "almeria_tomate": (GOLD, tomate, "El tomate"),
    "almeria_uva": (GOLD, uva, "La uva de barco"),
    "almeria_barril": (SEA, barril, "El barril de uva"),
    "almeria_cable": (SEA, cable, "El Cable Inglés"),
    "almeria_gurullos": (CLAY, gurullos, "Los gurullos"),
    "almeria_gamba": (CLAY, gamba, "La gamba roja"),
    "almeria_invernadero": (GOLD, invernadero, "El invernadero"),
    "almeria_huerta": (GOLD, huerta, "¿Quién convirtió el desierto en huerta?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Almería generados")
