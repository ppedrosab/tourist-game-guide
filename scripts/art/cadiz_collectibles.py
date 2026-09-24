#!/usr/bin/env python3
"""
Coleccionables de Cádiz (viewBox 120×124, mismo medallón que los de Málaga).
Aro: oro = comunes, mar = camino del mar, arcilla = camino de la ciudad.

Uso: python3 scripts/art/cadiz_collectibles.py && npm run gen:assets
"""
import math, os

INK = "#1B2A3A"; CLAY = "#A8431F"; CLAYD = "#7E3015"; SEA = "#2F6F73"; SEAD = "#22575A"; SEAT = "#DCEBE6"
PEACH = "#F0A27F"; GOLD = "#F2C14E"; GOLDD = "#C9962A"; PAPER = "#FFF8EC"; SAND = "#EADFCB"; WHITE = "#FFFFFF"
SILVER = "#B9C8D0"; SILVERD = "#8FA6B3"; WOOD = "#7A5236"; WOODL = "#9A6B45"; NAVY = "#2B3F5C"; PURPLE = "#6E2C5E"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "collectibles")


def frame(ring, art, title, cid):
    dots = []
    for k in range(8):
        a = math.radians(k * 45 - 90)
        x = 60 + 47 * math.cos(a); y = 60 + 47 * math.sin(a)
        dots.append(f'<path d="M{x:.1f} {y-4:.1f}L{x+4:.1f} {y:.1f}L{x:.1f} {y+4:.1f}L{x-4:.1f} {y:.1f}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 124" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{title}">
<defs><clipPath id="{cid}"><circle cx="60" cy="60" r="40.8"/></clipPath></defs>
<circle cx="60" cy="64" r="52" fill="{INK}"/>
<circle cx="60" cy="60" r="52" fill="{ring}" stroke="{INK}" stroke-width="3"/>
{''.join(dots)}
<circle cx="60" cy="60" r="42" fill="{PAPER}"/>
<g clip-path="url(#{cid})">{art}</g>
<circle cx="60" cy="60" r="42" fill="none" stroke="{INK}" stroke-width="2.5"/>
</svg>
'''


def sparkle(x, y, s, c=WHITE):
    return f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'


def waves(y, c=SEA, fill=SEAT):
    return (f'<path d="M14 {y}Q24 {y-5} 34 {y}T54 {y}T74 {y}T94 {y}T114 {y}L114 110L14 110Z" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M22 {y+8}Q28 {y+5} 34 {y+8}M60 {y+10}Q66 {y+7} 72 {y+10}M88 {y+7}Q94 {y+4} 100 {y+7}" fill="none" stroke="{c}" stroke-width="1.6"/>')


# Títere de la Tía Norica: cruceta, hilos y la abuela en miniatura
titere = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    + "".join(f'<path d="M{x1} 26L{x2} {y2}" stroke="{INK}" stroke-width=".9" opacity=".45"/>' for x1, x2, y2 in [(42, 44, 72), (78, 76, 72), (52, 52, 46), (68, 68, 46)])
    + f'<path d="M36 26H84" stroke="{INK}" stroke-width="7"/><path d="M36 26H84" stroke="{WOODL}" stroke-width="3.5"/>'
    f'<path d="M60 16V36" stroke="{INK}" stroke-width="7"/><path d="M60 16V36" stroke="{WOODL}" stroke-width="3.5"/>'
    # cuerpo
    f'<path d="M48 64Q60 58 72 64L78 100H42Z" fill="#2E2833" stroke="{INK}" stroke-width="2.3"/>'
    f'<path d="M51 78H69L72 100H48Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M46 66Q60 82 74 66L76 74Q60 90 44 74Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/>'
    f'<circle cx="52" cy="73" r="1.3" fill="{PEACH}"/><circle cx="60" cy="78" r="1.3" fill="{PEACH}"/><circle cx="68" cy="73" r="1.3" fill="{PEACH}"/>'
    f'<path d="M48 68Q42 70 44 72" stroke="{INK}" stroke-width="7"/><path d="M72 68Q78 70 76 72" stroke="{INK}" stroke-width="7"/>'
    f'<circle cx="44" cy="73" r="3.4" fill="#EDBE98" stroke="{INK}" stroke-width="1.6"/><circle cx="76" cy="73" r="3.4" fill="#EDBE98" stroke="{INK}" stroke-width="1.6"/>'
    # cabeza con moño
    f'<circle cx="60" cy="41" r="6" fill="#CFC9C0" stroke="{INK}" stroke-width="2"/>'
    f'<circle cx="60" cy="53" r="11" fill="#EDBE98" stroke="{INK}" stroke-width="2.3"/>'
    f'<path d="M49 52Q49 41 60 41Q71 41 71 52Q66 46 60 46Q54 46 49 52Z" fill="#CFC9C0" stroke="{INK}" stroke-width="1.8"/>'
    f'<circle cx="56" cy="54" r="1.4" fill="{INK}"/><circle cx="64" cy="54" r="1.4" fill="{INK}"/>'
    f'<path d="M56.5 58.5Q60 61 63.5 58.5" fill="none" stroke="{INK}" stroke-width="1.5"/>'
    f'<circle cx="53" cy="58" r="2" fill="#E88A78" opacity=".5"/><circle cx="67" cy="58" r="2" fill="#E88A78" opacity=".5"/>'
    f'<circle cx="69" cy="44" r="2.6" fill="{CLAY}" stroke="{INK}" stroke-width="1"/>'
    + sparkle(90, 48, 5, GOLD) + sparkle(30, 86, 3.5)
)

# Atún de almadraba saltando sobre las olas
atun = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + waves(84)
    + f'<g transform="translate(8 7) scale(.86) rotate(-14 60 60)">'
    f'<path d="M22 60Q40 40 72 44Q86 46 92 56L104 46Q100 58 104 70L92 62Q86 72 72 74Q40 78 22 60Z" fill="{NAVY}" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M24 62Q44 76 72 72Q84 70 90 62Q70 66 48 64Q34 64 24 62Z" fill="{SILVER}"/>'
    f'<path d="M26 62Q44 68 70 66" fill="none" stroke="{SILVERD}" stroke-width="1.3"/>'
    f'<path d="M50 46L58 34L64 45Z" fill="{NAVY}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M50 72L56 80L60 73Z" fill="{SILVERD}" stroke="{INK}" stroke-width="1.6"/>'
    + "".join(f'<path d="M{x} {46 + (x - 70) * .5:.0f}l2 -3l2 3Z" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for x in (70, 76, 82))
    + "".join(f'<path d="M{x} {73 - (x - 70) * .5:.0f}l2 3l2 -3Z" fill="{GOLD}" stroke="{INK}" stroke-width=".8"/>' for x in (70, 76, 82))
    + f'<circle cx="32" cy="56" r="3.6" fill="{WHITE}" stroke="{INK}" stroke-width="1.6"/><circle cx="32.6" cy="56" r="1.8" fill="{INK}"/>'
    f'<path d="M38 52Q41 58 38 64" fill="none" stroke="#1C2B40" stroke-width="1.6"/>'
    f'<path d="M26 44Q34 40 44 42" fill="none" stroke="{WHITE}" stroke-width="1.8" opacity=".6"/>'
    f'</g>'
    f'<circle cx="30" cy="88" r="2.5" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/><circle cx="96" cy="80" r="2" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>'
    + sparkle(92, 30, 5, GOLD)
)

# Catalejo del vigía, delante de la Torre Tavira
catalejo = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="84" cy="34" r="9" fill="#FFF3DC"/>'
    f'<path d="M26 104V52H50V104Z" fill="{SAND}" stroke="{INK}" stroke-width="2.3"/>'
    f'<path d="M42 52H50V104H42Z" fill="#D2B78C"/>'
    f'<path d="M22 52H54V46H22Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} 46V40" stroke="{INK}" stroke-width="2"/>' for x in (24, 31, 38, 45, 52))
    + f'<path d="M22 40H54" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M33 70V60Q38 55 43 60V70Z" fill="{INK}" opacity=".85"/><path d="M33 92V82Q38 77 43 82V92Z" fill="{INK}" opacity=".85"/>'
    f'<path d="M14 104H106" stroke="{INK}" stroke-width="2.3"/>'
    f'<g transform="rotate(-28 70 76)">'
    f'<rect x="38" y="70" width="22" height="13" rx="2" fill="{GOLDD}" stroke="{INK}" stroke-width="2.2"/>'
    f'<rect x="58" y="68" width="22" height="17" rx="2" fill="{GOLD}" stroke="{INK}" stroke-width="2.2"/>'
    f'<rect x="78" y="66" width="16" height="21" rx="2" fill="{GOLDD}" stroke="{INK}" stroke-width="2.2"/>'
    f'<rect x="92" y="64" width="6" height="25" rx="2" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M42 73H56M62 71H76" stroke="{WHITE}" stroke-width="1.6" opacity=".7"/>'
    f'</g>'
    + sparkle(96, 44, 5, GOLD) + sparkle(70, 28, 3.5)
)

# La Pepa de bolsillo: el libro de 1812 con laurel
pepa = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<path d="M78 34L86 38V98L78 96Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    f'<rect x="36" y="32" width="46" height="66" rx="3" fill="{CLAY}" stroke="{INK}" stroke-width="2.4"/>'
    f'<rect x="36" y="32" width="7" height="66" rx="2" fill="{CLAYD}" stroke="{INK}" stroke-width="2"/>'
    f'<rect x="47" y="38" width="30" height="54" rx="2" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
    f'<rect x="50" y="68" width="24" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M53 72l2 -1.5V81M59 71.5a2.2 2.2 0 1 0 .01 0ZM59 76a2.6 2.3 0 1 0 .01 0ZM64 72l2 -1.5V81M68 72.5Q70 70 72 72.5Q72 75 68 81H72.5" fill="none" stroke="{CLAYD}" stroke-width="1.5"/>'
    f'<path d="M50 54Q62 44 74 54" fill="none" stroke="#3F6A3A" stroke-width="1.6"/>'
    + "".join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2" transform="rotate({r} {x} {y})" fill="#5E8B4F" stroke="{INK}" stroke-width="1"/>' for x, y, r in [(53, 51, -40), (58, 48, -20), (66, 48, 20), (71, 51, 40)])
    + f'<circle cx="62" cy="47" r="2" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>'
    f'<path d="M70 98V108L73 105L76 108V98" fill="{SEA}" stroke="{INK}" stroke-width="1.6"/>'
    # pluma
    f'<path d="M88 88L100 42Q104 38 103 46Q98 70 90 88Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M88 90L101 42" stroke="{INK}" stroke-width="1.2"/>'
    + sparkle(28, 40, 5, GOLD) + sparkle(96, 100, 3.5)
)

# Postal de La Caleta con el balneario y un sello
caleta = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    f'<g transform="rotate(-8 60 64)">'
    f'<rect x="20" y="36" width="80" height="56" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
    f'<rect x="25" y="41" width="70" height="46" fill="#F9D9B6"/>'
    f'<circle cx="44" cy="54" r="6" fill="#FFF3DC"/>'
    f'<path d="M25 70H95V87H25Z" fill="#8FB9B4"/>'
    f'<path d="M25 70Q40 67 55 70T95 70" fill="none" stroke="{SEA}" stroke-width="1.4"/>'
    # balneario sobre pilotes
    f'<path d="M50 70V76M62 70V76M74 70V76" stroke="{INK}" stroke-width="1.4"/>'
    f'<rect x="46" y="60" width="34" height="10" fill="{WHITE}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M48 60Q52 53 56 60M58 60Q63 51 68 60M70 60Q74 53 78 60" fill="{WHITE}" stroke="{INK}" stroke-width="1.4"/>'
    f'<path d="M50 63V68M56 63V68M62 63V68M68 63V68M74 63V68" stroke="{SEA}" stroke-width="1.2"/>'
    # castillo a la izquierda y palmera
    f'<path d="M25 70V62H36V70Z" fill="{SAND}" stroke="{INK}" stroke-width="1.4"/><path d="M25 62L27 59L29 62L31 59L33 62L35 59L36 62" fill="none" stroke="{INK}" stroke-width="1.2"/>'
    f'<path d="M88 70Q87 58 89 50" fill="none" stroke="{WOOD}" stroke-width="2"/>'
    f'<path d="M89 50Q82 48 80 53M89 50Q96 47 98 52M89 50Q88 44 84 43M89 50Q92 44 96 44" fill="none" stroke="{SEA}" stroke-width="2"/>'
    f'<path d="M30 82Q34 80 38 82M70 84Q74 82 78 84" fill="none" stroke="{WHITE}" stroke-width="1.2"/>'
    f'</g>'
    # sello en la esquina
    f'<g transform="rotate(10 80 38)"><rect x="70" y="28" width="18" height="20" fill="{CLAY}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="2 1.4"/>'
    f'<circle cx="79" cy="38" r="4.5" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/></g>'
    + sparkle(26, 100, 4.5, GOLD)
)

# Insignia final: muralla sobre el mar y una bomba francesa que se queda corta
insignia = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="60" cy="58" r="30" fill="{GOLD}" opacity=".35"/>'
    + waves(86)
    + f'<path d="M30 88V58H90V88Z" fill="{SAND}" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M76 58H90V88H76Z" fill="#D2B78C"/>'
    f'<path d="M30 58V50H36V56H42V50H48V56H54V50H60V56H66V50H72V56H78V50H84V56H90V58" fill="{SAND}" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M52 88V74Q60 66 68 74V88Z" fill="{INK}" opacity=".85"/>'
    f'<path d="M38 66H44M76 66H82" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M60 50V30" stroke="{INK}" stroke-width="2"/>'
    f'<path d="M60 30L76 34L60 40Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/>'
    # la bomba cae al agua, lejos de la muralla
    f'<path d="M78 44L88 58" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="2 3" opacity=".6"/>'
    f'<circle cx="92" cy="66" r="6" fill="{INK}"/><path d="M95 61Q99 56 96 52" fill="none" stroke="{WOOD}" stroke-width="1.6"/>'
    + sparkle(96, 51, 3.2, PEACH)
    + f'<path d="M84 90Q88 82 92 90M92 90Q96 80 100 90" fill="none" stroke="{WHITE}" stroke-width="1.8"/>'
    f'<path d="M20 38Q26 30 34 34" fill="none" stroke="{INK}" stroke-width="1.3"/>'
    + sparkle(26, 70, 4.5, GOLD)
)

ART = {
    "cadiz_titere": (GOLD, titere, "El títere de la Tía Norica"),
    "cadiz_atun": (SEA, atun, "Atún de almadraba"),
    "cadiz_catalejo": (SEA, catalejo, "El catalejo del vigía"),
    "cadiz_pepa": (CLAY, pepa, "La Pepa de bolsillo"),
    "cadiz_caleta": (GOLD, caleta, "Postal de La Caleta"),
    "cadiz_insignia": (GOLD, insignia, "La ciudad que no cayó"),
}
def write(art_map):
    os.makedirs(OUT, exist_ok=True)
    for name, (ring, art, title) in art_map.items():
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(frame(ring, art, title, f"clip-{name}"))


if __name__ == "__main__":
    write(ART)
    print("coleccionables de Cádiz generados")
