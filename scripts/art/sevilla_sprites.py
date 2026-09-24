#!/usr/bin/env python3
"""
Sprites de Sevilla: el Aguador, el Giraldillo y Hernando Colón (mismo formato que los de Cádiz).

Uso: python3 scripts/art/sevilla_sprites.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import (INK, CLAY, SEA, SEAD, GOLD, GOLDD, PAPER, SHADOW, face_of, g, limb, svg, write)

# ---------------------------------------------------------------------------
# El Aguador: viejo de Velázquez, capa parda, cántaro de barro y copa de agua
# ---------------------------------------------------------------------------
SK = "#D9A27A"; SKD = "#B98260"; CAPE = "#8A5A3A"; CAPED = "#6E4630"; GREY = "#C9C2B8"; GREYD = "#A39A8E"


def aguador():
    legs = g("legs",
             f'<path d="M82 196L118 196L117 232L104 232L100 214L96 232L83 232Z" fill="#6B5A48" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M100 198L117 198L116 232L105 232Z" fill="#574837"/>',
             limb("M89 232L88 244", SK, 8), limb("M111 232L112 244", SK, 8),
             f'<path d="M78 248Q80 241 90 242Q97 243 96 248Z" fill="#6E4C33" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 248Q103 243 110 242Q120 241 122 248Z" fill="#6E4C33" stroke="{INK}" stroke-width="2.4"/>')
    jar = g("jar",
            f'<path d="M28 150Q14 170 22 198Q30 214 44 216Q58 214 64 198Q72 170 58 150Z" fill="#C9763F" stroke="{INK}" stroke-width="2.6"/>',
            f'<path d="M46 152Q66 172 60 200Q54 212 44 216Q56 196 50 156Z" fill="#A55A2C"/>',
            f'<path d="M34 140L52 140L56 152L30 152Z" fill="#C9763F" stroke="{INK}" stroke-width="2.2"/>',
            f'<path d="M22 178Q43 186 64 178" fill="none" stroke="#F0C69A" stroke-width="2"/>',
            f'<path d="M26 190Q34 186 40 192" fill="none" stroke="#7FB3B8" stroke-width="2.2"/>')
    torso = g("torso",
              f'<path d="M74 118Q100 106 126 118L130 200L70 200Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M90 112L100 128L110 112" fill="{SK}" stroke="{INK}" stroke-width="2"/>',
              # capa parda, raída, sobre los hombros
              f'<path d="M66 122Q100 104 134 122L140 206L126 200L120 210L110 200L100 212L90 200L80 210L74 200L60 206Z" fill="{CAPE}" stroke="{INK}" stroke-width="2.6"/>',
              f'<path d="M106 110Q124 112 134 122L140 206L126 200L120 210L112 200Z" fill="{CAPED}"/>',
              f'<path d="M84 122L96 200M116 122L106 200" fill="none" stroke="{PAPER}" stroke-width="0"/>',
              f'<path d="M86 124Q100 136 114 124L110 200L90 200Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>',
              f'<path d="M100 132L100 196" stroke="#DDD3C2" stroke-width="1.6"/>',
              f'<path d="M78 150Q76 172 80 196" fill="none" stroke="{CAPED}" stroke-width="1.8"/>')
    arms = g("arms",
             limb("M76 126Q58 134 50 146", CAPE, 12),
             limb("M124 126Q142 132 154 140", CAPE, 12),
             f'<circle cx="50" cy="148" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="156" cy="142" r="6" fill="{SK}" stroke="{INK}" stroke-width="2.4"/>',
             # copa de cristal con agua (y un higo, como en el cuadro)
             f'<path d="M148 110L168 110Q166 128 158 130Q150 128 148 110Z" fill="#DCEBE6" fill-opacity=".8" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M150 118L166 118Q164 128 158 129Q152 128 150 118Z" fill="#8FB9B4"/>',
             f'<circle cx="158" cy="123" r="3" fill="#6B3A4A" stroke="{INK}" stroke-width="1"/>',
             f'<path d="M158 130L158 138M153 139L163 139" stroke="{INK}" stroke-width="2"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{SK}"/>',
             f'<ellipse cx="61" cy="78" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="78" rx="6" ry="8" fill="{SK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{SK}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{SKD}" opacity=".5"/>',
             # calva con pelo cano a los lados y barba de tres días
             f'<path d="M60 76Q56 50 70 44Q66 58 68 76Z" fill="{GREY}" stroke="{INK}" stroke-width="2.2"/>',
             f'<path d="M140 76Q144 50 130 44Q134 58 132 76Z" fill="{GREY}" stroke="{INK}" stroke-width="2.2"/>',
             f'<path d="M84 40Q92 36 100 37" fill="none" stroke="{SKD}" stroke-width="2"/>',
             f'<path d="M70 92Q76 106 100 108Q124 106 130 92Q126 102 100 104Q74 102 70 92Z" fill="{GREYD}" opacity=".55"/>',
             *[f'<circle cx="{x}" cy="{y}" r=".9" fill="{GREYD}"/>' for x, y in [(80, 100), (88, 104), (112, 104), (120, 100), (96, 106), (104, 106)]],
             f'<path d="M72 56Q80 52 88 56M112 56Q120 52 128 56" fill="none" stroke="{SKD}" stroke-width="1.4"/>',
             f'<ellipse cx="80" cy="54" rx="9" ry="4" fill="#FFF" opacity=".25"/>')
    rim = g("rim",
            f'<path d="M70 58Q76 42 92 38" fill="none" stroke="#FFF" stroke-width="2.2" opacity=".4"/>',
            f'<path d="M70 130L66 196" fill="none" stroke="#F4D3A6" stroke-width="2" opacity=".5"/>',
            f'<path d="M24 164Q20 182 26 198" fill="none" stroke="#FFE3C0" stroke-width="2" opacity=".6"/>')
    return lambda e: svg(e, [SHADOW, legs, jar, torso, arms, head, face_of(e).replace("#5A3A22", "#5A4632"), rim])


# ---------------------------------------------------------------------------
# El Giraldillo: la Fe de bronce, con casco, lábaro y palma, sobre la bola de la veleta
# ---------------------------------------------------------------------------
BR = "#B8895A"; BRD = "#8E6640"; BRL = "#E2B57E"; PAT = "#5E8676"


def giraldillo():
    base = g("base",
             f'<path d="M100 236L100 250" stroke="{INK}" stroke-width="5"/>',
             f'<circle cx="100" cy="226" r="14" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M92 218Q98 214 104 216" fill="none" stroke="#FFF1C2" stroke-width="2.2"/>')
    banner = g("banner",
               f'<path d="M156 48L156 206" stroke="{INK}" stroke-width="6"/><path d="M156 48L156 206" stroke="{BRD}" stroke-width="3"/>',
               f'<path d="M156 40L162 50L156 56L150 50Z" fill="{BR}" stroke="{INK}" stroke-width="1.8"/>',
               # lábaro: estandarte que hace de veleta
               f'<path d="M158 60L190 64Q186 78 190 92L158 88Z" fill="{BR}" stroke="{INK}" stroke-width="2.4"/>',
               f'<path d="M160 64L186 67Q183 77 186 88L160 85Z" fill="{PAT}" opacity=".35"/>',
               f'<path d="M168 70L176 80M176 70L168 80" stroke="{BRD}" stroke-width="2"/>')
    robe = g("robe",
             f'<path d="M74 118Q100 106 126 118L136 214L64 214Z" fill="{BR}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q118 112 126 118L136 214L110 214Z" fill="{BRD}"/>',
             f'<path d="M84 130Q82 170 76 210M100 128L100 212M116 130Q118 170 124 210" fill="none" stroke="{BRD}" stroke-width="1.8"/>',
             f'<path d="M72 150Q100 162 128 150L130 162Q100 174 70 162Z" fill="{BRL}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M64 214Q100 206 136 214L136 220Q100 212 64 220Z" fill="{BRL}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M78 136Q80 156 76 180" fill="none" stroke="{PAT}" stroke-width="3" opacity=".45"/>')
    arms = g("arms",
             limb("M76 124Q58 118 50 100", BR, 11),
             limb("M124 124Q142 118 154 104", BR, 11),
             # palma en la mano izquierda
             f'<path d="M48 98Q40 60 30 40" fill="none" stroke="{INK}" stroke-width="5"/><path d="M48 98Q40 60 30 40" fill="none" stroke="{BR}" stroke-width="2.6"/>',
             *[f'<path d="M{44 - k * 2.2:.1f} {84 - k * 9}L{32 - k * 2.2:.1f} {80 - k * 9}M{44 - k * 2.2:.1f} {84 - k * 9}L{54 - k * 2.2:.1f} {76 - k * 9}" stroke="{BRD}" stroke-width="2.4"/>' for k in range(5)],
             f'<circle cx="50" cy="100" r="6" fill="{BR}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="155" cy="104" r="6" fill="{BR}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{BR}"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{BR}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{BRD}" opacity=".6"/>',
             f'<path d="M64 80Q60 100 70 112M136 80Q140 100 130 112" fill="none" stroke="{BRD}" stroke-width="5"/>',
             # casco con cimera
             f'<path d="M58 58Q58 16 100 14Q142 16 142 58Q128 44 100 42Q72 44 58 58Z" fill="{BRL}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M100 14Q132 18 142 58Q132 48 118 44Q116 26 100 14Z" fill="{BR}"/>',
             f'<path d="M58 58Q72 46 100 44Q128 46 142 58L142 62Q128 52 100 50Q72 52 58 62Z" fill="{BRD}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M100 16Q94 6 80 4Q96 2 106 8Q118 2 130 6Q112 8 104 18Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M72 34Q84 24 98 22" fill="none" stroke="#FFF1C2" stroke-width="2.4" opacity=".7"/>',
             f'<ellipse cx="80" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".35"/><ellipse cx="120" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".35"/>')
    rim = g("rim",
            f'<path d="M70 124L68 206" fill="none" stroke="#FFE6B8" stroke-width="2" opacity=".6"/>',
            f'<path d="M66 60Q72 34 92 24" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    return lambda e: svg(e, [SHADOW, base, banner, robe, arms, head, face_of(e).replace("#5A3A22", "#4A3A2A"), rim])


# ---------------------------------------------------------------------------
# Hernando Colón: erudito del s. XVI, bonete y ropa negra, cuello blanco y un gran libro
# ---------------------------------------------------------------------------
HS = "#E8B58E"; HSD = "#C9906A"; BLK = "#2B2A33"; BLKD = "#1E1D25"; FUR = "#8A6A4A"; HAIR = "#5A3A26"


def hernando():
    legs = g("legs",
             limb("M90 214L89 242", BLK, 9), limb("M110 214L111 242", BLK, 9),
             f'<path d="M78 248Q80 241 90 242Q97 243 96 248Z" fill="{BLKD}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 248Q103 243 110 242Q120 241 122 248Z" fill="{BLKD}" stroke="{INK}" stroke-width="2.4"/>')
    gown = g("gown",
             f'<path d="M72 118Q100 106 128 118L138 222L62 222Z" fill="{BLK}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q120 112 128 118L138 222L112 222Z" fill="{BLKD}"/>',
             # solapas de piel
             f'<path d="M78 118L90 222L80 222L66 124Z" fill="{FUR}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M122 118L110 222L120 222L134 124Z" fill="{FUR}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M90 114L110 114L108 150L92 150Z" fill="{SEA}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M86 112Q100 122 114 112L112 118Q100 128 88 118Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>',
             f'<circle cx="100" cy="134" r="3.2" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    arms = g("arms",
             limb("M76 124Q60 134 58 150", BLK, 12),
             limb("M124 124Q142 132 152 148", BLK, 12),
             # libro gordo en el brazo izquierdo
             f'<path d="M34 146L74 140L78 180L38 186Z" fill="{CLAY}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M38 186L78 180L80 186L40 192Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M44 154L68 150L70 170L46 174Z" fill="none" stroke="{GOLD}" stroke-width="1.6"/>',
             f'<circle cx="58" cy="152" r="6" fill="{HS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="152" cy="150" r="6" fill="{HS}" stroke="{INK}" stroke-width="2.4"/>',
             # pluma en la derecha
             f'<path d="M152 146L170 110Q176 104 174 116Q166 136 154 148Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{HS}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{HS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{HS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{HS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{HSD}" opacity=".5"/>',
             # melena corta a la altura de la mandíbula
             f'<path d="M58 90Q54 44 100 40Q146 44 142 90L134 92Q136 62 122 56Q100 64 78 56Q64 62 66 92Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M110 44Q140 50 142 90L134 92Q136 62 122 56Z" fill="#452C1C"/>',
             # bonete negro
             f'<path d="M60 52Q58 22 100 20Q142 22 140 52Q120 44 100 44Q80 44 60 52Z" fill="{BLK}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M100 20Q134 22 140 52Q126 46 114 45Q116 28 100 20Z" fill="{BLKD}"/>',
             f'<path d="M100 20L100 12" stroke="{INK}" stroke-width="3"/>',
             f'<ellipse cx="78" cy="68" rx="7" ry="3.5" fill="#FFF" opacity=".2"/>')
    rim = g("rim",
            f'<path d="M66 44Q76 26 96 22" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>',
            f'<path d="M72 126L66 214" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')
    return lambda e: svg(e, [SHADOW, legs, gown, arms, head, face_of(e).replace("#5A3A22", "#4A3020"), rim])


if __name__ == "__main__":
    for key, build in [("aguador", aguador()), ("giraldillo", giraldillo()), ("hernando", hernando())]:
        write(key, build)
    print("sprites de Sevilla generados")
