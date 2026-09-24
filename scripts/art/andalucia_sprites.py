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
}

if __name__ == "__main__":
    keys = sys.argv[1:] or list(CHARACTERS)
    for k in keys:
        write(k, figure(**CHARACTERS[k]))
    print("personajes generados:", ", ".join(keys))
