#!/usr/bin/env python3
"""
Personajes de Córdoba, Huelva, Jaén, Almería y de las rutas gastronómicas de Málaga, Sevilla y
Granada. Todos salen del generador paramétrico `figure.py` (misma cabeza y 8 caras que el resto).

Uso: python3 scripts/art/andalucia_sprites.py [personaje…] && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import CLAY, SEA, GOLD, PAPER, write
from figure import figure

INDIGO = "#33406E"; WINE = "#7A2335"; OLIVE = "#6E7A3E"; OCHRE = "#C9A05E"; GREY = "#8A8480"; BLACK = "#2B2A33"

CHARACTERS = {
    # --- Córdoba ---------------------------------------------------------
    "lubna": dict(skin="media", hair=("long", "#2A1E1A"), hat_=("veil", SEA), outfit="dress", main=INDIGO, accent=GOLD,
                  second="#E9DCC0", left="book", right="quill", raise_right=True),
    "almanzor": dict(skin="morena", hair=("short", "#1E1A1A"), beard_=("full", "#1E1A1A"), hat_=("turban", PAPER, CLAY),
                     outfit="tunic", main=WINE, accent=GOLD, right="sword", raise_right=True),
    "librero": dict(skin="media", hair=("short", "#4A3222"), beard_=("short", "#4A3222"), hat_=("turban", OCHRE, SEA),
                    outfit="vest", main="#E9DCC0", accent=SEA, second="#6E5A44", left="book", right="scroll"),
    "patiera": dict(skin="clara", hair=("bun", GREY), hat_=("flower", CLAY, GOLD), outfit="dress", main="#4F8B5A", accent=PAPER,
                    second="#F2D48F", apron=PAPER, left="basket", right="flower"),
    "ziryab": dict(skin="morena", hair=("long", "#1E1A1A"), beard_=("moustache", "#1E1A1A"), hat_=("turban", "#6E2C5E", GOLD),
                   outfit="toga", main="#E8C872", accent="#6E2C5E", second=SEA, left="lute"),
    "jornalero": dict(skin="morena", hair=("short", "#3A2A1E"), hat_=("straw", CLAY), outfit="shirt", main=PAPER, accent=BLACK,
                      second="#5A5048", left="dornillo"),
    # --- Huelva ----------------------------------------------------------
    "mackay": dict(skin="clara", eyes="#3A5A7A", hair=("short", "#B5653A"), beard_=("moustache", "#B5653A"), hat_=("bowler", BLACK, "#4A4A55"),
                   outfit="jacket", main="#6E5A44", accent=CLAY, second="#5A4A3A", left="bag", right="ball", raise_right=True),
    "minero": dict(skin="morena", hair=("short", "#2A1E1A"), beard_=("short", "#2A1E1A"), hat_=("miner", "#8C939C"), outfit="shirt",
                   main="#8C8478", accent="#4A3A2E", second="#3A3A48", right="pick"),
    "marinero": dict(skin="clara", eyes="#3A5A7A", hair=("short", "#D9B26A"), beard_=("short", "#D9B26A"), hat_=("sailor", INDIGO),
                     outfit="shirt", main=INDIGO, accent=PAPER, second=INDIGO, neck=PAPER, left="ball"),
    "choquera": dict(skin="media", hair=("bun", "#2A1E1A"), outfit="dress", main=SEA, accent=PAPER, second="#DCEBE6", apron=PAPER,
                     left="basket", right="cuttlefish", raise_right=True),
    "fresera": dict(skin="morena", hair=("braid", "#3A2A1E"), hat_=("straw", "#D8412F"), outfit="dress", main="#D8412F", accent=PAPER,
                    second="#4F8B5A", left="strawberries"),
    "cortador": dict(skin="media", hair=("slick", "#2A1E1A"), beard_=("short", "#2A1E1A"), outfit="vest", main=PAPER, accent=BLACK,
                     second=BLACK, apron=PAPER, left="ham", right="knife"),
    # --- Jaén ------------------------------------------------------------
    "sereno": dict(skin="media", hair=("short", GREY), beard_=("moustache", GREY), hat_=("peaked", "#2F3E5C", GOLD), outfit="jacket",
                   main="#2F3E5C", accent=GOLD, second="#2B2A33", left="lantern", right="staff"),
    "preso": dict(skin="media", hair=("curly", "#3A2A1E"), beard_=("short", "#3A2A1E"), outfit="shirt", main="#D9CDB4", accent="#8A6243",
                  second="#6E5A44", left="bread", right="bag"),
    "pastor": dict(skin="morena", hair=("short", "#4A3222"), beard_=("short", "#4A3222"), hat_=("straw", "#8A6243"), outfit="vest",
                   main=PAPER, accent="#C9A77E", second="#5A4A3A", right="staff"),
    "catadora": dict(skin="clara", hair=("bun", "#6B4A2A"), outfit="jacket", main=OLIVE, accent=GOLD, second="#3A3A48",
                     left="oil", right="blueglass", raise_right=True),
    "vareador": dict(skin="morena", hair=("short", "#2A1E1A"), hat_=("cap", "#5A4A3A"), outfit="shirt", main="#C9A05E", accent="#4A3A2E",
                     second="#3A3A48", right="staff", left="olive"),
    "molinero": dict(skin="media", hair=("bald", GREY), beard_=("moustache", GREY), outfit="shirt", main="#E9DCC0", accent=CLAY,
                     second="#5A4A3A", apron="#C9B48A", left="jug", right="oil"),
    # --- Almería ---------------------------------------------------------
    "vigia": dict(skin="morena", hair=("short", "#2A1E1A"), beard_=("short", "#2A1E1A"), hat_=("turban", SEA, GOLD), outfit="tunic",
                  main="#C9A05E", accent=SEA, right="horn", raise_right=True, left="staff"),
    "jayran": dict(skin="clara", eyes="#3A5A7A", hair=("short", "#8A5A3A"), beard_=("full", "#8A5A3A"), hat_=("turban", PAPER, "#2F6F9E"),
                   outfit="toga", main="#2F6F9E", accent=GOLD, second=PAPER, left="scroll"),
    "sedera": dict(skin="media", hair=("long", "#2A1E1A"), hat_=("veil", "#E8C872"), outfit="dress", main="#6E2C5E", accent=GOLD,
                   second="#C0476A", left="silk"),
    "hortelana": dict(skin="morena", hair=("braid", "#2A1E1A"), hat_=("straw", "#4F8B5A"), outfit="shirt", main="#4F8B5A", accent="#3A5A7A",
                      second="#3A5A7A", left="basket", right="tomato", raise_right=True),
    "barrilero": dict(skin="media", hair=("short", GREY), beard_=("moustache", GREY), hat_=("cap", "#4A3A2E"), outfit="vest",
                      main=PAPER, accent="#8A6243", second="#4A3A2E", apron="#8A6243", left="barrel", right="hammer"),
    "pescador": dict(skin="morena", hair=("curly", "#2A1E1A"), beard_=("short", "#2A1E1A"), hat_=("cap", INDIGO), outfit="shirt",
                     main="#E9DCC0", accent=INDIGO, second=INDIGO, left="net", right="shrimp", raise_right=True),
    # --- Gastronomía de Málaga, Sevilla y Granada -----------------------------
    "espetero": dict(skin="morena", hair=("short", "#2A1E1A"), beard_=("short", "#2A1E1A"), outfit="shirt", main=PAPER, accent=SEA,
                     second="#3A5A7A", apron=PAPER, right="espeto", raise_right=True),
    "jabegote": dict(skin="morena", hair=("curly", "#2A1E1A"), hat_=("kerchief", CLAY, PAPER), outfit="shirt", main="#DCEBE6", accent=CLAY,
                     second="#3A3A48", left="net", right="oar"),
    "pasera": dict(skin="morena", hair=("bun", "#3A2A1E"), hat_=("kerchief", PAPER, SEA), outfit="dress", main="#8A5A7A", accent=PAPER,
                   second="#E9DCC0", apron=PAPER, left="grapes"),
    "naranjera": dict(skin="media", hair=("bun", "#2A1E1A"), hat_=("flower", PAPER, GOLD), outfit="dress", main="#E8812E", accent=PAPER,
                      second="#4F8B5A", left="oranges", right="orange", raise_right=True),
    "escoces": dict(skin="clara", eyes="#3A5A7A", hair=("short", "#C0643A"), beard_=("moustache", "#C0643A"), hat_=("beret", "#2F4A6E"),
                    outfit="jacket", main="#4A6E4A", accent=CLAY, second="#6E5A44", left="scroll", right="jar", raise_right=True),
    "aceitunero": dict(skin="media", hair=("slick", "#2A1E1A"), beard_=("moustache", "#2A1E1A"), hat_=("cap", "#4A3A2E"), outfit="vest",
                       main=PAPER, accent=OLIVE, second="#3A3A48", left="olives"),
    "especiera": dict(skin="media", hair=("long", "#2A1E1A"), hat_=("kerchief", "#D98A2E", "#6E2C5E"), outfit="dress", main="#6E2C5E",
                      accent=GOLD, second="#D98A2E", apron="#F2E3C4", left="spicesack"),
    "ceferino": dict(skin="clara", hair=("slick", "#3A2A1E"), beard_=("moustache", "#3A2A1E"), hat_=("toque", PAPER), outfit="shirt",
                     main=PAPER, accent="#C9A05E", second="#3A3A48", apron=PAPER, right="pastrytray", raise_right=True),
    "tornera": dict(skin="clara", hair=None, hat_=("veil", "#2B2A33"), outfit="habit", main="#2B2A33", accent=PAPER, left="box",
                    extra=f'<path d="M66 84Q66 50 100 48Q134 50 134 84" fill="none" stroke="{PAPER}" stroke-width="5"/>', neck=PAPER),
    # --- Rutas de fiestas ---------------------------------------------------
    "cantaora": dict(skin="media", hair=("bun", "#1E1A1A"), hat_=("flower", "#D8412F", GOLD), outfit="dress", main=BLACK, accent="#D8412F",
                     second="#D8412F", neck="#D8412F", left="fan", raise_right=True),
    "verdialero": dict(skin="morena", hair=("short", "#2A1E1A"), hat_=("verdiales", "#2B2A33"), outfit="shirt", main=PAPER, accent="#D8412F",
                       second=BLACK, right="violin"),
    "cochero": dict(skin="clara", hair=("slick", "#3A2A1E"), beard_=("moustache", "#3A2A1E"), hat_=("bowler", "#6E5A44", BLACK), outfit="jacket",
                    main="#4A3A5E", accent=GOLD, second=BLACK, right="whip", raise_right=True),
    "flamenca": dict(skin="media", hair=("bun", "#2A1E1A"), hat_=("peineta", "#8A5A3A", "#D8412F"), outfit="dress", main="#E8744A", accent=PAPER,
                     second=PAPER, neck=PAPER, right="castanets", raise_right=True),
    "tratante": dict(skin="morena", hair=("short", GREY), beard_=("short", GREY), hat_=("cordobes", "#4A3A2E", BLACK), outfit="vest",
                     main=PAPER, accent="#6E4C33", second="#4A3A2E", right="staff"),
    "farolillero": dict(skin="clara", hair=("curly", "#8A5A3A"), outfit="shirt", main="#DCEBE6", accent="#4F8B5A", second="#3A3A48",
                        right="paperlantern", raise_right=True, left="scissors"),
    "cabezudo": dict(skin="media", hair=("short", "#2A1E1A"), outfit="tunic", main="#C0476A", accent=GOLD, second=PAPER, neck=PAPER,
                     left="bighead"),
    "modista": dict(skin="clara", hair=("long", "#8A5A3A"), outfit="dress", main="#6E2C5E", accent=GOLD, second="#E9DCC0", neck=PAPER,
                    right="scissors", raise_right=True, left="silk"),
    "tamborilero": dict(skin="morena", hair=("short", "#1E1A1A"), hat_=("beret", CLAY), outfit="jacket", main=INDIGO, accent=CLAY, second=PAPER,
                        left="drum"),
    "crucera": dict(skin="media", hair=("braid", "#2A1E1A"), hat_=("flower", "#D8412F", PAPER), outfit="dress", main="#F2E3C4", accent="#D8412F",
                    second="#D8412F", apron=PAPER, left="carnations"),
    "caballista": dict(skin="media", hair=("slick", "#1E1A1A"), hat_=("cordobes", BLACK, BLACK), outfit="jacket", main=GREY, accent=BLACK,
                       second=BLACK, right="whip"),
    "pregonero": dict(skin="clara", hair=("bald", GREY), beard_=("full", GREY), hat_=("tricorn", BLACK), outfit="toga", main="#7A2335", accent=GOLD,
                      second=PAPER, left="scroll", right="horn", raise_right=True),
    "grumete": dict(skin="morena", hair=("curly", "#3A2A1E"), hat_=("kerchief", "#D8412F", PAPER), outfit="shirt", main="#E9DCC0", accent="#6E4C33",
                    second="#6E5A44", left="ladle"),
    "pinzon": dict(skin="media", hair=("short", "#4A3A2E"), beard_=("full", "#4A3A2E"), hat_=("beret", "#7A2335"), outfit="toga", main="#6E4C33",
                   accent=GOLD, second="#7A2335", left="compass", right="sword", raise_right=True),
    "colombina": dict(skin="clara", hair=("bun", "#4A3222"), hat_=("flower", PAPER, GOLD), outfit="dress", main="#2F6F9E", accent=PAPER,
                      second="#DCEBE6", neck=PAPER, left="scroll", right="fan"),
    "melenchonera": dict(skin="media", hair=("braid", "#3A2A1E"), hat_=("kerchief", "#6E2C5E", GOLD), outfit="dress", main="#B8412A", accent=GOLD,
                         second="#3A3A48", left="pandero", raise_right=True),
    "podador": dict(skin="morena", hair=("short", "#2A1E1A"), beard_=("short", "#5A5048"), hat_=("cap", "#6E5A44"), outfit="jacket", main=OLIVE,
                    accent="#6E4C33", second="#3A3A48", right="shears", left="olive"),
    "ganadero": dict(skin="media", hair=("short", GREY), beard_=("moustache", GREY), hat_=("straw", "#6E4C33"), outfit="vest", main="#E9DCC0",
                     accent="#6E4C33", second="#4A3A2E", right="staff"),
    "bailaora": dict(skin="morena", hair=("bun", "#1E1A1A"), hat_=("flower", "#F2C14E", "#D8412F"), outfit="dress", main="#4F8B5A", accent=GOLD,
                     second=GOLD, neck="#D8412F", left="castanets", right="castanets", raise_right=True),
    "torrero": dict(skin="morena", hair=("short", "#2A1E1A"), beard_=("short", "#2A1E1A"), hat_=("morion", GREY), outfit="tunic", main="#8A6243",
                    accent="#B7BDC6", left="lantern", right="staff"),
    "cohetero": dict(skin="clara", hair=("curly", "#B5653A"), hat_=("cap", CLAY), outfit="shirt", main="#F2E3C4", accent=CLAY, second="#3A3A48",
                     apron="#6E5A44", right="rocket", raise_right=True),
}

if __name__ == "__main__":
    keys = sys.argv[1:] or list(CHARACTERS)
    for k in keys:
        write(k, figure(**CHARACTERS[k]))
    print("personajes generados:", ", ".join(keys))
