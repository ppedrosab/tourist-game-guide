#!/usr/bin/env python3
"""
Coleccionables de Huelva (medallón 120×124). Aro: oro = comunes; historia: mar = el puerto,
arcilla = los barrios ingleses; gastronomía: mar = la ría, arcilla = el centro.

Uso: python3 scripts/art/huelva_collectibles.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import INK, CLAY, SEA, SEAT, GOLD, GOLDD, PAPER, WHITE, WOOD, WOODL, NAVY, SILVER, SILVERD, frame, sparkle, waves, write

BG = '<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
SKY = f'<rect x="0" y="0" width="120" height="124" fill="{SEAT}"/>'
IRON = "#5E6B78"; RED = "#D8412F"; LEAF = "#4F8B5A"

muelle = (SKY + waves(78)
          + f'<path d="M6 60H114V68H6Z" fill="{IRON}" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M{x} 68L{x + 8} 104M{x + 8} 68L{x} 104" stroke="{IRON}" stroke-width="2"/><path d="M{x + 4} 68V110" stroke="{INK}" stroke-width="2.4"/>' for x in range(10, 110, 22))
          + f'<path d="M20 60V44H44V60" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/><path d="M50 60V48H70V60" fill="#8A6243" stroke="{INK}" stroke-width="1.6"/>'
          + f'<path d="M84 60L84 30L100 44Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><path d="M84 30V60" stroke="{INK}" stroke-width="2"/>')

locomotora = (BG + f'<path d="M10 94H110" stroke="{INK}" stroke-width="3"/>' + "".join(f'<path d="M{x} 94V100" stroke="{WOOD}" stroke-width="4"/>' for x in range(14, 110, 12))
              + f'<path d="M26 82V56H72V82Z" fill="{SEA}" stroke="{INK}" stroke-width="2.2"/>'
              f'<path d="M72 82V40H100V82Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/><path d="M78 48H94V62H78Z" fill="{SEAT}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M68 36H104V42H68Z" fill="{INK}"/><path d="M34 56V38H46V56" fill="{INK}"/>'
              f'<path d="M20 82L14 90H26Z" fill="{INK}"/>'
              + "".join(f'<circle cx="{x}" cy="86" r="{r}" fill="{IRON}" stroke="{INK}" stroke-width="2"/><circle cx="{x}" cy="86" r="3" fill="{GOLD}"/>' for x, r in [(38, 8), (58, 8), (86, 10)])
              + f'<circle cx="40" cy="26" r="7" fill="#DDD" opacity=".8"/><circle cx="30" cy="18" r="9" fill="#DDD" opacity=".6"/>')

ancla = (SKY + waves(92)
         + f'<path d="M60 26V90" stroke="{INK}" stroke-width="9"/><path d="M60 26V90" stroke="{IRON}" stroke-width="5"/>'
         f'<circle cx="60" cy="22" r="8" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="60" cy="22" r="8" fill="none" stroke="{IRON}" stroke-width="3"/>'
         f'<path d="M42 40H78" stroke="{INK}" stroke-width="8"/><path d="M42 40H78" stroke="{IRON}" stroke-width="4"/>'
         f'<path d="M30 70Q34 92 60 92Q86 92 90 70" fill="none" stroke="{INK}" stroke-width="9"/><path d="M30 70Q34 92 60 92Q86 92 90 70" fill="none" stroke="{IRON}" stroke-width="5"/>'
         f'<path d="M24 74L30 62L36 74Z" fill="{IRON}" stroke="{INK}" stroke-width="1.6"/><path d="M84 74L90 62L96 74Z" fill="{IRON}" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M66 30Q90 40 84 60" fill="none" stroke="{WOODL}" stroke-width="3"/>')

carabela = (SKY + waves(84)
            + f'<path d="M22 72H98L88 88H32Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/><path d="M22 72L16 64H30Z" fill="{WOOD}" stroke="{INK}" stroke-width="1.6"/>'
            + f'<path d="M60 72V20M40 72V34M80 72V38" stroke="{INK}" stroke-width="2.4"/>'
            + "".join(f'<path d="M{x - w} {t}Q{x} {t - 4} {x + w} {t}L{x + w - 2} {t + h}Q{x} {t + h + 4} {x - w + 2} {t + h}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>' for x, t, w, h in [(60, 26, 16, 22), (40, 38, 11, 16), (80, 42, 11, 16)])
            + f'<path d="M56 34H64M60 30V38" stroke="{RED}" stroke-width="2.4"/><path d="M60 20L70 16L60 14Z" fill="{RED}"/>')

rueda = (BG + f'<circle cx="60" cy="60" r="36" fill="none" stroke="{INK}" stroke-width="8"/><circle cx="60" cy="60" r="36" fill="none" stroke="{WOODL}" stroke-width="4"/>'
         + "".join(f'<path d="M60 60L{60 + 36 * c:.1f} {60 + 36 * s:.1f}" stroke="{WOOD}" stroke-width="3"/>' for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.71, .71), (-.71, .71), (.71, -.71), (-.71, -.71)])
         + "".join(f'<path d="M{60 + 36 * c - 5:.1f} {60 + 36 * s - 4:.1f}h10v8h-10Z" fill="#8FB9B4" stroke="{INK}" stroke-width="1.2"/>' for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1), (.71, .71), (-.71, .71), (.71, -.71), (-.71, -.71)])
         + f'<circle cx="60" cy="60" r="8" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>')

casita = ('<rect x="0" y="0" width="120" height="124" fill="#DCEBE6"/>'
          f'<path d="M0 92H120V124H0Z" fill="#8FAF6E"/>'
          f'<path d="M30 92V56H90V92Z" fill="#F4EEE2" stroke="{INK}" stroke-width="2.2"/>'
          f'<path d="M24 58L60 30L96 58Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.2"/>'
          f'<path d="M76 42V28H84V48" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M54 92V72H66V92Z" fill="{SEA}" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M36 64H48V76H36ZM72 64H84V76H72Z" fill="{SEAT}" stroke="{INK}" stroke-width="1.6"/>'
          + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{LEAF}"/><circle cx="{x}" cy="{y - 3}" r="2" fill="{RED}"/>' for x, y in [(20, 90), (100, 90), (34, 94), (86, 94)])
          + f'<path d="M10 100H110" stroke="{PAPER}" stroke-width="2" stroke-dasharray="4 3"/>')

balon = (BG + '<g transform="translate(9 0) scale(.85)">' + f'<ellipse cx="60" cy="98" rx="30" ry="6" fill="{INK}" opacity=".15"/>'
         f'<circle cx="60" cy="58" r="34" fill="#B9793E" stroke="{INK}" stroke-width="2.6"/>'
         f'<path d="M28 48Q60 70 92 48M30 72Q60 50 90 72M60 24V92" fill="none" stroke="#7A4A22" stroke-width="2.2"/>'
         + "".join(f'<path d="M55 {36 + k * 6}h10" stroke="{PAPER}" stroke-width="2"/>' for k in range(4))
         + f'<path d="M40 36Q46 30 54 30" fill="none" stroke="#FFF" stroke-width="3" opacity=".35"/></g>'
         f'<text x="60" y="98" font-family="Georgia, serif" font-size="11" font-weight="700" text-anchor="middle" fill="{INK}">1889</text>')

insignia = ('<rect x="0" y="0" width="120" height="124" fill="#1F5A9E"/>'
            + "".join(f'<path d="M{x} 0V124" stroke="{WHITE}" stroke-width="9"/>' for x in (30, 60, 90))
            + f'<path d="M34 30H86V70Q86 94 60 104Q34 94 34 70Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
            + f'<circle cx="60" cy="62" r="18" fill="#B9793E" stroke="{INK}" stroke-width="2"/><path d="M44 56Q60 68 76 56M60 44V80" fill="none" stroke="#7A4A22" stroke-width="1.6"/>'
            + f'<path d="M40 40H80" stroke="{GOLD}" stroke-width="3"/>' + sparkle(90, 24, 6, GOLD))

# --- gastronomía ---
choco = (SKY + waves(90)
         + f'<path d="M20 58Q34 30 72 40Q86 46 84 60Q84 76 70 80Q34 88 20 58Z" fill="#C7B39A" stroke="{INK}" stroke-width="2.4"/>'
         f'<path d="M24 58Q38 38 70 46" fill="none" stroke="#A89274" stroke-width="2"/>'
         + "".join(f'<path d="M82 {54 + k * 5}q12 {k - 2} 22 {k * 3 - 4}" fill="none" stroke="{INK}" stroke-width="5"/><path d="M82 {54 + k * 5}q12 {k - 2} 22 {k * 3 - 4}" fill="none" stroke="#C7B39A" stroke-width="3"/>' for k in range(4))
         + f'<circle cx="72" cy="54" r="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><circle cx="73" cy="54" r="2" fill="{INK}"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}" opacity=".75"/>' for x, y, r in [(16, 86, 5), (26, 92, 3), (10, 96, 3)]))

fresa = (BG + f'<path d="M60 102Q24 78 26 52Q30 34 60 38Q90 34 94 52Q96 78 60 102Z" fill="{RED}" stroke="{INK}" stroke-width="2.6"/>'
         + "".join(f'<path d="M{x} {y}l1.4 3" stroke="#F7E08A" stroke-width="2"/>' for x, y in [(40, 52), (52, 48), (66, 50), (78, 54), (46, 64), (60, 62), (74, 66), (52, 76), (66, 78), (58, 88)])
         + f'<path d="M40 40Q50 26 60 36Q70 26 80 40Q70 44 60 40Q50 44 40 40Z" fill="{LEAF}" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M60 36V22" stroke="{LEAF}" stroke-width="4"/>' + sparkle(92, 28, 5))

gamba = (SKY + f'<ellipse cx="60" cy="88" rx="44" ry="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
         f'<path d="M28 76Q24 44 58 36Q86 32 92 52Q80 48 70 54Q84 66 66 74Q52 64 44 70Q40 80 28 76Z" fill="#F2A58A" stroke="{INK}" stroke-width="2.4"/>'
         + "".join(f'<path d="M{x} {y}q4 6 0 12" fill="none" stroke="#D97A5E" stroke-width="1.6"/>' for x, y in [(48, 42), (58, 40), (68, 40)])
         + f'<path d="M86 48L110 26M88 52L112 40" stroke="{INK}" stroke-width="1.4"/><circle cx="84" cy="46" r="2" fill="{INK}"/>'
         f'<path d="M28 76L16 84L22 72Z" fill="#F2A58A" stroke="{INK}" stroke-width="1.6"/>')

jamon = (BG + f'<path d="M22 96L36 84Q20 50 50 30Q84 12 98 36Q106 58 80 80L44 92Z" fill="#A8432F" stroke="{INK}" stroke-width="2.6"/>'
         f'<path d="M50 34Q84 18 96 40Q90 34 78 34Q60 36 50 44Z" fill="#E9DCC0" stroke="{INK}" stroke-width="1.6"/>'
         f'<path d="M22 96L14 108L28 104Z" fill="#E9DCC0" stroke="{INK}" stroke-width="1.8"/>'
         f'<path d="M36 84L44 92" stroke="{INK}" stroke-width="3"/><path d="M60 50Q70 60 64 72" fill="none" stroke="#C45A44" stroke-width="3"/>'
         + "".join(f'<path d="M{x} 104l-4 10M{x + 6} 104l-3 10" stroke="{LEAF}" stroke-width="2"/>' for x in (70, 90)))

mote = ('<rect x="0" y="0" width="120" height="124" fill="#F4EEE2"/>'
        f'<path d="M18 30H102V78H60L44 94V78H18Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
        f'<text x="60" y="61" font-family="Georgia, serif" font-size="13" font-weight="700" text-anchor="middle" fill="{CLAY}">¡choquero!</text>'
        + f'<path d="M74 88Q86 80 98 88Q106 96 98 104Q86 110 74 102Z" fill="#C7B39A" stroke="{INK}" stroke-width="1.8"/><circle cx="92" cy="92" r="1.8" fill="{INK}"/>'
        + sparkle(26, 104, 5, GOLD))

mojama = (BG + f'<path d="M14 92H106" stroke="{WOOD}" stroke-width="5"/>'
          + "".join(f'<path d="M{x} {y}H{x + 58}Q{x + 64} {y + 6} {x + 58} {y + 12}H{x}Q{x - 6} {y + 6} {x} {y}Z" fill="#7A2E24" stroke="{INK}" stroke-width="2"/>'
                    f'<path d="M{x + 4} {y + 4}H{x + 50}" stroke="#A8543F" stroke-width="1.6"/>' for x, y in [(30, 50), (36, 66)])
          + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for x, y in [(24, 84), (34, 86), (86, 84)])
          + f'<path d="M20 34Q34 20 48 34Q34 48 20 34Z" fill="#3E4F66" stroke="{INK}" stroke-width="1.6"/><path d="M48 34L56 26V42Z" fill="#3E4F66" stroke="{INK}" stroke-width="1.4"/>')

habas = (BG + f'<path d="M14 58H106Q104 96 60 98Q16 96 14 58Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
         f'<ellipse cx="60" cy="58" rx="46" ry="12" fill="#B8652E" stroke="{INK}" stroke-width="2"/>'
         + "".join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="3.4" fill="#7FA35A" stroke="{INK}" stroke-width="1"/>' for x, y in [(30, 56), (44, 60), (56, 54), (70, 60), (84, 55), (38, 52), (76, 52)])
         + "".join(f'<path d="M{x} {y}q6 -4 12 0" fill="none" stroke="#E6DCC8" stroke-width="3.4"/>' for x, y in [(34, 60), (60, 58), (80, 60)])
         + f'<path d="M90 24Q100 34 94 46" fill="none" stroke="#CCC" stroke-width="3" opacity=".7"/><path d="M76 20Q86 30 80 42" fill="none" stroke="#CCC" stroke-width="3" opacity=".7"/>')

choqueros = (f'<rect x="0" y="0" width="120" height="124" fill="{NAVY}"/>' + waves(92, SEA, "#2F6F73")
             + f'<path d="M28 60Q40 36 74 44Q88 50 86 62Q86 76 72 80Q40 86 28 60Z" fill="#C7B39A" stroke="{INK}" stroke-width="2.4"/>'
             + "".join(f'<path d="M84 {56 + k * 5}q10 {k - 2} 18 {k * 3 - 4}" fill="none" stroke="#C7B39A" stroke-width="3"/>' for k in range(4))
             + f'<circle cx="74" cy="56" r="3" fill="{INK}"/>'
             + f'<path d="M36 26L42 38L56 40L46 48L48 62L36 54L24 62L26 48L16 40L30 38Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8" transform="translate(4 -8) scale(.7)"/>'
             + sparkle(96, 28, 5, GOLD))

ART = {
    "huelva_muelle": (GOLD, muelle, "El Muelle del Tinto"),
    "huelva_locomotora": (GOLD, locomotora, "La locomotora de la mina"),
    "huelva_ancla": (SEA, ancla, "El ancla del vapor"),
    "huelva_carabela": (SEA, carabela, "La carabela"),
    "huelva_rueda": (CLAY, rueda, "La rueda romana"),
    "huelva_casita": (CLAY, casita, "La casita inglesa"),
    "huelva_balon": (GOLD, balon, "El balón de 1889"),
    "huelva_insignia": (GOLD, insignia, "¿Quién trajo el fútbol a España?"),
    "huelva_choco": (GOLD, choco, "El choco"),
    "huelva_fresa": (GOLD, fresa, "La fresa"),
    "huelva_gamba": (SEA, gamba, "La gamba blanca"),
    "huelva_jamon": (SEA, jamon, "El jamón de la sierra"),
    "huelva_mote": (CLAY, mote, "El mote"),
    "huelva_mojama": (CLAY, mojama, "La mojama"),
    "huelva_habas": (GOLD, habas, "Chocos con habas"),
    "huelva_choqueros": (GOLD, choqueros, "¿Por qué nos llaman choqueros?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Huelva generados")
