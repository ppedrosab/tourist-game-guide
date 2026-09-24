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
}

if __name__ == "__main__":
    keys = sys.argv[1:] or list(CHARACTERS)
    for k in keys:
        write(k, figure(**CHARACTERS[k]))
    print("personajes generados:", ", ".join(keys))
