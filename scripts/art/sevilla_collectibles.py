#!/usr/bin/env python3
"""
Coleccionables de Sevilla (medallón 120×124). Aro: oro = comunes, mar = pista del río,
arcilla = pista de los papeles.

Uso: python3 scripts/art/sevilla_collectibles.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_collectibles import (INK, CLAY, CLAYD, SEA, SEAD, SEAT, PEACH, GOLD, GOLDD, PAPER, SAND, WHITE,
                                WOOD, WOODL, sparkle, waves, write)

# Búcaro del Aguador: cántaro de barro, copa y gotas
bucaro = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E6CF"/>'
    f'<path d="M40 44Q24 62 32 88Q40 104 56 104Q72 104 80 88Q88 62 72 44Z" fill="#C9763F" stroke="{INK}" stroke-width="2.4"/>'
    f'<path d="M58 46Q80 64 74 90Q68 102 56 104Q70 86 62 50Z" fill="#A55A2C"/>'
    f'<path d="M46 34H66L70 46H42Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M32 72Q56 80 80 72" fill="none" stroke="#F0C69A" stroke-width="2"/>'
    f'<path d="M40 60Q46 56 50 62" fill="none" stroke="#7FB3B8" stroke-width="2"/>'
    f'<path d="M80 62L96 62Q95 76 88 78Q81 76 80 62Z" fill="{SEAT}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M82 68L94 68Q93 76 88 77Q83 76 82 68Z" fill="#8FB9B4"/>'
    f'<path d="M88 78V86M84 87H92" stroke="{INK}" stroke-width="1.8"/>'
    + "".join(f'<path d="M{x} {y}q3 5 0 7q-3 -2 0 -7Z" fill="#8FB9B4" stroke="{INK}" stroke-width="1"/>' for x, y in [(56, 22), (64, 18), (72, 24)])
    + sparkle(28, 36, 5, GOLD)
)

# Torre del Oro sobre el río
torre = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="86" cy="32" r="8" fill="#FFF3DC"/>'
    + waves(90)
    + f'<path d="M40 92V52H80V92Z" fill="#E7C47E" stroke="{INK}" stroke-width="2.3"/>'
    f'<path d="M66 52H80V92H66Z" fill="#D2A85E"/>'
    f'<path d="M36 52H84V46H36Z" fill="#F2D48F" stroke="{INK}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} 46V40H{x + 5}V46" fill="#F2D48F" stroke="{INK}" stroke-width="1.4"/>' for x in (38, 48, 58, 68, 77))
    + f'<path d="M48 40V26H72V40Z" fill="#E7C47E" stroke="{INK}" stroke-width="2"/><path d="M64 26H72V40H64Z" fill="#D2A85E"/>'
    f'<path d="M52 26V18H68V26Z" fill="#F2D48F" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M52 18Q60 6 68 18Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M55 70V60Q60 54 65 60V70Z" fill="{INK}" opacity=".85"/><path d="M57 36V30Q60 27 63 30V36Z" fill="{INK}" opacity=".85"/>'
    f'<path d="M42 96H78" stroke="#FFF6E0" stroke-width="2"/>'
    + sparkle(30, 30, 5, GOLD) + sparkle(92, 60, 3.5)
)

# ¡Tierra!: la cofa de La Pinta y una isla en el horizonte
tierra = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + waves(84)
    + f'<path d="M78 84Q88 70 104 84Z" fill="#6E9F7A" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M92 76Q91 66 94 60" fill="none" stroke="{WOOD}" stroke-width="1.6"/><path d="M94 60Q88 58 86 62M94 60Q100 57 102 61" fill="none" stroke="{SEA}" stroke-width="1.6"/>'
    f'<path d="M44 110V20" stroke="{INK}" stroke-width="7"/><path d="M44 110V20" stroke="{WOODL}" stroke-width="3.5"/>'
    f'<path d="M32 50H56L52 62H36Z" fill="{WOOD}" stroke="{INK}" stroke-width="2"/>'
    # vigía señalando
    f'<circle cx="44" cy="38" r="5" fill="#D9A07A" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M40 50L42 44H48L50 50Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>'
    f'<path d="M48 45L64 36" stroke="{INK}" stroke-width="4"/><path d="M48 45L64 36" stroke="{CLAY}" stroke-width="2"/>'
    f'<path d="M44 20L62 24L44 28Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    + sparkle(72, 28, 6, GOLD) + sparkle(96, 44, 3.5)
)

# Legajo de Indias: papeles atados con cinta y lacre
legajo = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    + "".join(f'<path d="M{30 + d} {40 + d * .6:.0f}L{88 + d} {36 + d * .6:.0f}L{92 + d} {90 + d * .6:.0f}L{34 + d} {94 + d * .6:.0f}Z" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
              for d, c in [(4, "#E8DCC4"), (2, "#F1E6D0"), (0, PAPER)])
    + "".join(f'<path d="M38 {50 + i * 7}L{80 - (i % 2) * 10} {47 + i * 7}" stroke="#8A7A5A" stroke-width="1.2"/>' for i in range(6))
    + f'<path d="M60 36L64 92" stroke="{CLAY}" stroke-width="4"/><path d="M30 66L92 62" stroke="{CLAY}" stroke-width="4"/>'
    f'<circle cx="62" cy="64" r="8" fill="{CLAYD}" stroke="{INK}" stroke-width="1.8"/><path d="M58 64L66 64M62 60L62 68" stroke="#E0766A" stroke-width="1.6"/>'
    + sparkle(96, 30, 5, GOLD) + sparkle(24, 96, 3.5)
)

# El león del Alcázar: azulejo con el león y la cruz
leon = (
    f'<rect x="0" y="0" width="120" height="124" fill="#F7E3DA"/>'
    f'<rect x="28" y="28" width="64" height="64" rx="3" fill="#F6EBD2" stroke="{INK}" stroke-width="2.4"/>'
    f'<rect x="33" y="33" width="54" height="54" rx="2" fill="none" stroke="{SEA}" stroke-width="2"/>'
    + "".join(f'<path d="M{x} {y}l3 -3l3 3l-3 3Z" fill="{SEA}"/>' for x, y in [(30, 31), (84, 31), (30, 88), (84, 88)])
    # león de perfil, en pie
    + f'<path d="M44 80L46 64Q44 56 50 52Q58 48 66 52L74 50Q80 52 78 58L72 62L74 80H68L66 68H54L52 80Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M50 52Q46 44 54 42Q60 38 66 44Q70 50 66 54Q58 58 50 52Z" fill="{GOLDD}" stroke="{INK}" stroke-width="1.6"/>'
    f'<circle cx="61" cy="47" r="1.3" fill="{INK}"/>'
    f'<path d="M44 66Q36 62 38 54" fill="none" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M80 40V64M74 46H86" stroke="{CLAY}" stroke-width="2.6"/>'
    + sparkle(98, 100, 4.5, GOLD)
)

# La carabela Santa María sobre las olas
carabela = (
    f'<rect x="0" y="0" width="120" height="124" fill="#E6F0EC"/>'
    + waves(84)
    + f'<path d="M30 76H92L84 90H38Z" fill="{WOOD}" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M30 76L24 68H36Z" fill="{WOOD}" stroke="{INK}" stroke-width="1.8"/><path d="M92 76L96 66L84 70Z" fill="{WOOD}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M34 82H88" stroke="{GOLD}" stroke-width="1.8"/>'
    f'<path d="M60 76V26M42 76V40M78 76V38" stroke="{INK}" stroke-width="2.2"/>'
    f'<path d="M50 34Q60 30 70 34Q72 50 70 64Q60 60 50 64Q48 50 50 34Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
    f'<path d="M60 40V58M52 48H68" stroke="{CLAY}" stroke-width="2.6"/>'
    f'<path d="M36 44Q42 42 48 44Q49 54 48 62Q42 60 36 62Q35 54 36 44Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M78 40L90 60H78Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M60 26L72 29L60 32Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"/>'
    + sparkle(96, 34, 5, GOLD) + sparkle(22, 40, 3.5)
)

# Insignia: rosa de los vientos y lupa sobre dos tumbas
insignia = (
    f'<rect x="0" y="0" width="120" height="124" fill="#FBE7CF"/>'
    f'<circle cx="60" cy="58" r="30" fill="{GOLD}" opacity=".3"/>'
    + "".join(f'<path d="M60 58L{60 + dx * 30} {58 + dy * 30}L{60 + dy * 6} {58 - dx * 6}Z" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
              for dx, dy, c in [(0, -1, CLAY), (1, 0, SEA), (0, 1, CLAY), (-1, 0, SEA)])
    + f'<circle cx="60" cy="58" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>'
    # dos tumbas: una a cada lado del océano
    f'<path d="M30 96V84Q36 76 42 84V96Z" fill="{SAND}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M78 96V84Q84 76 90 84V96Z" fill="{SAND}" stroke="{INK}" stroke-width="1.6"/>'
    f'<path d="M36 82V90M33 85H39M84 82V90M81 85H87" stroke="{INK}" stroke-width="1.2"/>'
    f'<path d="M44 94Q60 88 76 94" fill="none" stroke="{SEA}" stroke-width="2" stroke-dasharray="3 3"/>'
    f'<path d="M76 70L86 80" stroke="{INK}" stroke-width="6"/><path d="M76 70L86 80" stroke="{WOODL}" stroke-width="3"/>'
    f'<circle cx="70" cy="64" r="10" fill="{SEAT}" fill-opacity=".55" stroke="{INK}" stroke-width="2.6"/>'
    + sparkle(26, 34, 5, GOLD)
)

ART = {
    "sevilla_bucaro": (GOLD, bucaro, "El búcaro del Aguador"),
    "sevilla_torre_oro": (SEA, torre, "La Torre del Oro"),
    "sevilla_tierra": (SEA, tierra, "¡Tierra!"),
    "sevilla_legajo": (CLAY, legajo, "Legajo de Indias"),
    "sevilla_leon": (CLAY, leon, "El león del Alcázar"),
    "sevilla_carabela": (GOLD, carabela, "La carabela del monumento"),
    "sevilla_insignia": (GOLD, insignia, "¿Dónde está Colón?"),
}

if __name__ == "__main__":
    write(ART)
    print("coleccionables de Sevilla generados")
