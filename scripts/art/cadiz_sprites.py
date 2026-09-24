#!/usr/bin/env python3
"""
Sprites de Cádiz: Tía Norica, la Pepa y Magón (viewBox 200×260, como los de Málaga).
Grupos de primer nivel: shadow · cuerpo… · face · rim. Las 8 caras salen de las del
Cenachero (misma geometría de cabeza) cambiando el color del iris; en la Pepa van
desplazadas porque la cara está en la tapa del libro.

Uso: python3 scripts/art/cadiz_sprites.py && npm run gen:assets
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SPR = os.path.join(ROOT, "assets", "sprites")
EXPR = ["neutral", "talking", "happy", "thinking", "surprised", "nervous", "proud", "dramatic"]
INK = "#1B2A3A"; CLAY = "#A8431F"; CLAYD = "#7E3015"; SEA = "#2F6F73"; SEAD = "#22575A"
GOLD = "#F2C14E"; GOLDD = "#C9962A"; PAPER = "#FFF8EC"; PEACH = "#F0A27F"


def face_of(expr: str) -> str:
    s = open(os.path.join(SPR, "cenachero", f"cenachero_{expr}.svg")).read()
    i = s.index('<g id="face"')
    j = s.index('<g id="rim"')
    return s[i:j]


def svg(expr: str, groups: list[str]) -> str:
    return ('<svg stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" '
            f'width="200" height="260" viewBox="0 0 200 260" role="img" aria-label="{expr}">' + "".join(groups) + "</svg>\n")


def g(id_: str, *parts: str, attrs: str = "") -> str:
    return f'<g id="{id_}"{attrs}>' + "".join(parts) + "</g>"


def limb(d: str, fill: str, w: float = 11) -> str:
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 4}"/><path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}"/>'


SHADOW = g("shadow",
           f'<ellipse cx="100" cy="249" rx="69.6" ry="9" fill="{INK}" opacity="0"/>',
           f'<ellipse cx="100" cy="249" rx="50" ry="6" fill="{INK}" opacity=".2"/>',
           f'<ellipse cx="100" cy="249" rx="28" ry="3.5" fill="{INK}" opacity=".1"/>')

# ---------------------------------------------------------------------------
# Tía Norica: marioneta, abuela gaditana con moño, mantón y delantal
# ---------------------------------------------------------------------------
SK = "#EDBE98"; SKD = "#D29C74"; HAIR = "#CFC9C0"; HAIRD = "#A9A197"; DRESS = "#2E2833"; DRESSD = "#1F1B24"


def norica():
    strings = g("strings",
                # cruceta de madera y los hilos a cabeza y manos
                *[f'<path d="M100 2L{x} {y}" fill="none" stroke="{INK}" stroke-width=".9" opacity=".35"/>'
                  for x, y in [(66, 58), (134, 58), (46, 146), (154, 146)]],
                f'<path d="M72 6L128 6" fill="none" stroke="{INK}" stroke-width="7"/>',
                f'<path d="M72 6L128 6" fill="none" stroke="#9A6B45" stroke-width="4"/>',
                f'<path d="M100 0L100 12" fill="none" stroke="{INK}" stroke-width="7"/>',
                f'<path d="M100 0L100 12" fill="none" stroke="#9A6B45" stroke-width="4"/>')
    skirt = g("skirt",
              f'<path d="M72 170Q66 206 62 236L138 236Q134 206 128 170Z" fill="{DRESS}" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M104 172L128 170Q134 206 138 236L112 236Z" fill="{DRESSD}"/>',
              f'<path d="M80 176Q78 206 76 232L124 232Q122 206 120 176Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>',
              f'<path d="M104 176L120 176Q122 206 124 232L110 232Z" fill="#EADFCB"/>',
              f'<path d="M76 232Q82 226 88 232Q94 226 100 232Q106 226 112 232Q118 226 124 232" fill="none" stroke="{INK}" stroke-width="1.8"/>',
              f'<path d="M84 196L116 196" fill="none" stroke="#EADFCB" stroke-width="1.6"/>',
              f'<path d="M84 238Q84 246 92 246L98 246L98 236Z" fill="{INK}"/>',
              f'<path d="M116 238Q116 246 108 246L102 246L102 236Z" fill="{INK}"/>')
    torso = g("torso",
              f'<path d="M76 116Q100 106 124 116L130 176L70 176Z" fill="{DRESS}" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M104 110Q116 110 124 116L130 176L108 176Z" fill="{DRESSD}"/>',
              f'<path d="M92 110L100 122L108 110" fill="{SK}" stroke="{INK}" stroke-width="2"/>',
              # mantón de flecos cruzado
              f'<path d="M70 118Q100 150 130 118L134 140Q100 170 66 140Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.4"/>',
              f'<path d="M104 148Q122 140 134 140L130 118Q120 134 104 140Z" fill="{CLAYD}"/>',
              *[f'<circle cx="{x}" cy="{y}" r="2" fill="{PEACH}"/>' for x, y in [(78, 132), (90, 142), (100, 146), (110, 142), (122, 132), (84, 138), (116, 138)]],
              *[f'<path d="M{x} {150 - abs(100 - x) * .28:.1f}L{x} {158 - abs(100 - x) * .28:.1f}" fill="none" stroke="{CLAY}" stroke-width="1.6"/>' for x in range(74, 128, 6)],
              f'<path d="M96 150L100 162L104 150" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>')
    arms = g("arms",
             limb("M78 122Q60 130 48 146", DRESS, 12),
             limb("M122 122Q140 130 152 146", DRESS, 12),
             # articulaciones de madera de la marioneta
             f'<circle cx="48" cy="146" r="4" fill="#9A6B45" stroke="{INK}" stroke-width="2"/>',
             f'<circle cx="152" cy="146" r="4" fill="#9A6B45" stroke="{INK}" stroke-width="2"/>',
             f'<circle cx="44" cy="153" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="156" cy="153" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M91 98L91 114L109 114L109 98Z" fill="{SK}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<circle cx="61" cy="92" r="4" fill="none" stroke="{GOLD}" stroke-width="2.2"/>',
             f'<circle cx="139" cy="92" r="4" fill="none" stroke="{GOLD}" stroke-width="2.2"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{SK}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{SKD}" opacity=".5"/>',
             f'<ellipse cx="78" cy="92" rx="7" ry="4" fill="#E88A78" opacity=".45"/>',
             f'<ellipse cx="122" cy="92" rx="7" ry="4" fill="#E88A78" opacity=".45"/>',
             f'<path d="M70 86Q72 90 70 94M130 86Q128 90 130 94" fill="none" stroke="{SKD}" stroke-width="1.4"/>',
             # moño y pelo cano con raya en medio
             f'<circle cx="100" cy="22" r="14" fill="{HAIR}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 10Q114 14 112 28Q106 20 98 18Z" fill="{HAIRD}"/>',
             f'<path d="M86 16L116 30" fill="none" stroke="{GOLDD}" stroke-width="2.4"/>',
             f'<path d="M60 74Q54 32 100 30Q146 32 140 74Q134 54 118 48Q108 44 100 42Q92 44 82 48Q66 54 60 74Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M100 32L100 42" fill="none" stroke="{HAIRD}" stroke-width="2"/>',
             f'<path d="M112 34Q134 40 138 64Q128 50 112 46Z" fill="{HAIRD}"/>',
             f'<path d="M74 40Q86 34 96 34" fill="none" stroke="#EEEAE4" stroke-width="2.4"/>',
             # clavel en el pelo
             *[f'<circle cx="{132 + dx}" cy="{46 + dy}" r="4.2" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>' for dx, dy in [(-3, -2), (3, -2), (0, 3)]],
             f'<circle cx="132" cy="45" r="2.4" fill="#C9553A"/>',
             f'<ellipse cx="76" cy="66" rx="7" ry="3.5" fill="#FFF" opacity=".2"/>')
    rim = g("rim",
            f'<path d="M68 62Q74 44 92 40" fill="none" stroke="#FFF" stroke-width="2.2" opacity=".4"/>',
            f'<path d="M79 122L74 170" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>',
            f'<path d="M82 180L80 226" fill="none" stroke="#FFF" stroke-width="2" opacity=".6"/>')
    return lambda e: svg(e, [SHADOW, strings, skirt, torso, arms, head, face_of(e).replace("#5A3A22", "#4A5A6A"), rim])


# ---------------------------------------------------------------------------
# La Pepa: la Constitución de 1812 hecha libro, con laurel y pluma
# ---------------------------------------------------------------------------
def digit_paths(x0: float, y0: float, w: float, h: float) -> str:
    """«1812» con trazos (sin fuentes: SvgXml no garantiza tipografías)."""
    sx = w; sy = h
    def P(pts): return "M" + "L".join(f"{x0 + px * sx:.1f} {y0 + py * sy:.1f}" for px, py in pts)
    one = lambda o: P([(o + .15, .2), (o + .45, 0), (o + .45, 1)])
    eight = lambda o: (f"M{x0 + (o + .4) * sx:.1f} {y0:.1f}"
                       f"a{.3 * sx:.1f} {.25 * sy:.1f} 0 1 0 .01 0Z"
                       f"M{x0 + (o + .4) * sx:.1f} {y0 + .5 * sy:.1f}"
                       f"a{.35 * sx:.1f} {.25 * sy:.1f} 0 1 0 .01 0Z")
    two = lambda o: (f"M{x0 + (o + .1) * sx:.1f} {y0 + .25 * sy:.1f}"
                     f"Q{x0 + (o + .4) * sx:.1f} {y0 - .1 * sy:.1f} {x0 + (o + .7) * sx:.1f} {y0 + .25 * sy:.1f}"
                     f"Q{x0 + (o + .7) * sx:.1f} {y0 + .55 * sy:.1f} {x0 + (o + .1) * sx:.1f} {y0 + sy:.1f}"
                     f"L{x0 + (o + .75) * sx:.1f} {y0 + sy:.1f}")
    d = one(0) + eight(1) + one(2) + two(3)
    return f'<path d="{d}" fill="none" stroke="{CLAYD}" stroke-width="2.4"/>'


def pepa():
    legs = g("legs",
             limb("M88 228L86 242", INK, 6),
             limb("M112 228L114 242", INK, 6),
             f'<path d="M74 248Q76 240 86 240Q94 240 94 248Z" fill="{SEA}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M106 248Q106 240 114 240Q124 240 126 248Z" fill="{SEA}" stroke="{INK}" stroke-width="2.4"/>')
    book = g("book",
             # hojas (canto) y tapa
             f'<path d="M140 50L154 58L154 238L140 232Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
             *[f'<path d="M143 {y}L151 {y + 5}" fill="none" stroke="#D8CBB3" stroke-width="1.2"/>' for y in range(64, 230, 9)],
             f'<path d="M62 42L140 42Q146 42 146 48L146 228Q146 234 140 234L62 234Q54 234 54 226L54 50Q54 42 62 42Z" fill="{CLAY}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M54 50Q54 42 62 42L68 42L68 234L62 234Q54 234 54 226Z" fill="{CLAYD}"/>',
             f'<path d="M68 42L68 234" fill="none" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M122 44L140 44Q144 44 144 48L144 228Q144 232 140 232L122 232Z" fill="{CLAYD}" opacity=".45"/>',
             f'<rect x="76" y="52" width="60" height="172" rx="4" fill="none" stroke="{GOLD}" stroke-width="2.2"/>',
             *[f'<path d="M{x} {y}l4 -4l4 4l-4 4Z" fill="{GOLD}" stroke="{GOLDD}" stroke-width=".8"/>' for x, y in [(74, 52), (130, 52), (74, 224), (130, 224)]],
             f'<ellipse cx="84" cy="126" rx="7" ry="4" fill="#F08A74" opacity=".55"/>',
             f'<ellipse cx="124" cy="126" rx="7" ry="4" fill="#F08A74" opacity=".55"/>',
             # cartela con el año
             f'<path d="M82 176L130 176L130 208L82 208Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>',
             digit_paths(88, 183, 9.4, 18),
             f'<path d="M86 172L126 172" fill="none" stroke="{GOLD}" stroke-width="1.6"/>',
             # cinta de marcapáginas
             f'<path d="M126 234L126 250L131 245L136 250L136 234Z" fill="{SEA}" stroke="{INK}" stroke-width="2"/>',
             # laurel sobre el libro
             *[f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3.4" transform="rotate({r} {x} {y})" fill="#5E8B4F" stroke="{INK}" stroke-width="1.6"/>'
               for x, y, r in [(70, 38, -40), (80, 32, -25), (91, 28, -10), (130, 38, 40), (120, 32, 25), (109, 28, 10)]],
             f'<path d="M64 42Q80 24 100 24Q120 24 136 42" fill="none" stroke="#3F6A3A" stroke-width="2"/>',
             f'<circle cx="100" cy="25" r="3.4" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>')
    arms = g("arms",
             limb("M56 118Q44 132 42 150", INK, 5),
             limb("M146 118Q158 132 158 150", INK, 5),
             f'<circle cx="42" cy="152" r="6.5" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="158" cy="152" r="6.5" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>')
    quill = g("quill",
              f'<path d="M160 158L180 104Q186 98 184 110Q176 138 162 158Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>',
              f'<path d="M160 160L182 104" fill="none" stroke="{INK}" stroke-width="1.4"/>',
              *[f'<path d="M{170 + k * 3} {134 - k * 7}L{176 + k * 3} {130 - k * 7}" fill="none" stroke="#D8CBB3" stroke-width="1.2"/>' for k in range(4)],
              f'<path d="M158 160L156 166" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    face = lambda e: face_of(e).replace('<g id="face">', '<g id="face" transform="translate(4 30)">').replace("#5A3A22", "#6B3A2A")
    rim = g("rim",
            f'<path d="M58 60L58 220" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>',
            f'<path d="M72 48L118 48" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    return lambda e: svg(e, [SHADOW, legs, book, arms, quill, face(e), rim])


# ---------------------------------------------------------------------------
# Magón: mercader fenicio con barba rizada, gorro cónico, túnica púrpura y ánfora
# ---------------------------------------------------------------------------
MS = "#C68A5E"; MSD = "#A86F47"; PURPLE = "#6E2C5E"; PURPLED = "#521E46"; BEARD = "#2A1E1A"


def magon():
    legs = g("legs",
             limb("M90 214L89 242", MS, 9),
             limb("M110 214L111 242", MS, 9),
             f'<path d="M84 232L94 232M84 238L94 238M106 232L116 232M106 238L116 238" fill="none" stroke="#7A5236" stroke-width="2"/>',
             f'<path d="M78 248Q80 241 90 242Q97 243 96 248Z" fill="#7A5236" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 248Q103 243 110 242Q120 241 122 248Z" fill="#7A5236" stroke="{INK}" stroke-width="2.4"/>')
    amphora = g("amphora",
                f'<path d="M30 150Q18 170 26 196Q32 212 38 218L44 218Q50 212 56 196Q64 170 52 150L50 142L32 142Z" fill="#C9763F" stroke="{INK}" stroke-width="2.6"/>',
                f'<path d="M44 150Q58 168 52 198Q48 210 44 218L40 218Q50 196 44 150Z" fill="#A55A2C"/>',
                f'<path d="M30 140L52 140L52 146L30 146Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>',
                f'<path d="M32 150Q22 146 26 158M50 150Q60 146 56 158" fill="none" stroke="{INK}" stroke-width="2.4"/>',
                f'<path d="M26 176Q41 182 56 176" fill="none" stroke="#F0C69A" stroke-width="2"/>',
                f'<path d="M24 186Q41 192 58 186" fill="none" stroke="#8E4A22" stroke-width="1.6"/>')
    tunic = g("tunic",
              f'<path d="M74 118Q100 106 126 118L136 222L64 222Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M104 112Q118 112 126 118L136 222L110 222Z" fill="{PURPLED}"/>',
              f'<path d="M65 212L135 212L136 222L64 222Z" fill="{GOLD}" stroke="{INK}" stroke-width="2"/>',
              *[f'<path d="M{x} 214l3 3l-3 3l-3 -3Z" fill="{GOLDD}"/>' for x in range(72, 132, 10)],
              f'<path d="M88 112Q100 126 112 112" fill="none" stroke="{GOLD}" stroke-width="4"/>',
              f'<path d="M70 162L130 162L131 172L69 172Z" fill="{SEA}" stroke="{INK}" stroke-width="2.2"/>',
              f'<path d="M104 162L130 162L131 172L108 172Z" fill="{SEAD}"/>',
              f'<circle cx="100" cy="167" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>',
              f'<path d="M84 176Q82 196 80 210M116 176Q118 196 120 210" fill="none" stroke="{PURPLED}" stroke-width="1.8"/>')
    arms = g("arms",
             limb("M76 124Q58 132 46 144", MS, 11),
             limb("M124 124Q142 132 156 146", MS, 11),
             f'<path d="M80 120Q70 124 64 132L72 138Q78 130 84 128Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2.2"/>',
             f'<path d="M120 120Q130 124 136 132L128 138Q122 130 116 128Z" fill="{PURPLED}" stroke="{INK}" stroke-width="2.2"/>',
             f'<path d="M150 140L162 140" fill="none" stroke="{GOLD}" stroke-width="3"/>',
             f'<circle cx="46" cy="146" r="6" fill="{MS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="156" cy="148" r="6" fill="{MS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{MS}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{MS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{MS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<circle cx="61" cy="91" r="3.4" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{MS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{MSD}" opacity=".5"/>',
             # barba rizada: por debajo de la boca, de oreja a oreja
             f'<path d="M62 78Q58 120 100 132Q142 120 138 78Q134 96 124 102Q116 110 100 110Q84 110 76 102Q66 96 62 78Z" fill="{BEARD}" stroke="{INK}" stroke-width="2.6"/>',
             *[f'<path d="M{x - 4} {y}q4 -5 8 0" fill="none" stroke="#4A3A32" stroke-width="1.8"/>'
               for x, y in [(74, 110), (86, 118), (100, 122), (114, 118), (126, 110), (92, 128), (108, 128), (68, 98), (132, 98)]],
             # pelo rizado y gorro cónico
             *[f'<circle cx="{x}" cy="{y}" r="5" fill="{BEARD}" stroke="{INK}" stroke-width="1.8"/>' for x, y in [(64, 62), (136, 62), (66, 52), (134, 52)]],
             f'<path d="M62 54Q66 12 100 4Q134 12 138 54Z" fill="{SEA}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M100 4Q126 12 138 54L118 54Q116 22 100 4Z" fill="{SEAD}"/>',
             f'<path d="M60 48Q100 40 140 48L140 58Q100 50 60 58Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.4"/>',
             *[f'<circle cx="{x}" cy="{52 - (4 if 80 < x < 120 else 2)}" r="1.4" fill="{GOLDD}"/>' for x in range(70, 134, 10)],
             f'<ellipse cx="76" cy="68" rx="7" ry="3.5" fill="#FFF" opacity=".2"/>')
    rim = g("rim",
            f'<path d="M70 44Q76 22 94 12" fill="none" stroke="#FFF" stroke-width="2.2" opacity=".35"/>',
            f'<path d="M77 124L70 206" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>',
            f'<path d="M28 160Q24 180 30 198" fill="none" stroke="#FFE3C0" stroke-width="2" opacity=".6"/>')
    # en Magón la boca queda sobre la barba: un poco más oscura por dentro
    return lambda e: svg(e, [SHADOW, legs, amphora, tunic, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


for key, build in [("norica", norica()), ("pepa", pepa()), ("magon", magon())]:
    os.makedirs(os.path.join(SPR, key), exist_ok=True)
    for e in EXPR:
        with open(os.path.join(SPR, key, f"{key}_{e}.svg"), "w") as f:
            f.write(build(e))
print("sprites de Cádiz generados")
