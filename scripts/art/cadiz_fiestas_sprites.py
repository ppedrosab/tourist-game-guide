#!/usr/bin/env python3
"""
Personajes del Carnaval de Cádiz: el Romancero (guía, con su cartelón y su puntero), el
Comparsista, el Corista y el Cuartetero. El Chirigotero está en cadiz_sprites.py.

Uso: python3 scripts/art/cadiz_fiestas_sprites.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import (INK, CLAY, CLAYD, SEA, SEAD, GOLD, GOLDD, PAPER, SHADOW, face_of, g, limb, svg, write)

VIOLET = "#6E2C5E"; VIOLETD = "#521E46"


def head_base(sk, skd, extra=()):
    return [f'<path d="M90 96L90 114L110 114L110 96Z" fill="{sk}"/>',
            f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>',
            f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{sk}" stroke="{INK}" stroke-width="2.6"/>',
            f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{sk}" stroke="{INK}" stroke-width="3"/>',
            f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{skd}" opacity=".5"/>', *extra]


def shoes(c="#2B2A33"):
    return [f'<path d="M78 248Q80 240 92 240Q98 241 98 248Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>',
            f'<path d="M102 248Q102 241 108 240Q120 240 122 248Z" fill="{c}" stroke="{INK}" stroke-width="2.4"/>']


# ---------------------------------------------------------------------------
# El Romancero: levita verde, chistera abollada con clavel, cartelón de viñetas y puntero
# ---------------------------------------------------------------------------
RS = "#E3AE88"; RSD = "#C58E68"


def romancero():
    board = g("cartelon",
              f'<path d="M140 30L150 30L150 246L140 246Z" fill="#8A6243" stroke="{INK}" stroke-width="2"/>',
              f'<path d="M122 36L196 30L198 150L124 156Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
              f'<path d="M160 33L161 153M123 96L197 90" stroke="{INK}" stroke-width="1.6"/>',
              # viñetas: el teatro, un coro, el levante y una bruja
              f'<path d="M130 80L130 58L144 48L156 58L156 80Z" fill="#C4623F" stroke="{INK}" stroke-width="1.2"/>',
              f'<path d="M168 76Q176 54 190 60" fill="none" stroke="{SEA}" stroke-width="3"/><path d="M168 66Q178 48 192 50" fill="none" stroke="{SEA}" stroke-width="2"/>',
              f'<circle cx="138" cy="122" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="1"/><circle cx="150" cy="124" r="6" fill="{CLAY}" stroke="{INK}" stroke-width="1"/><path d="M130 142H158L154 132H134Z" fill="{SEA}" stroke="{INK}" stroke-width="1"/>',
              f'<path d="M178 104L170 136L186 136Z" fill="{VIOLET}" stroke="{INK}" stroke-width="1.2"/><circle cx="178" cy="100" r="5" fill="#9BB58A" stroke="{INK}" stroke-width="1"/><path d="M172 138Q178 146 184 138" fill="none" stroke="#F29A2E" stroke-width="2"/>')
    legs = g("legs",
             f'<path d="M82 204L118 204L117 238L104 238L100 220L96 238L83 238Z" fill="#4A4A55" stroke="{INK}" stroke-width="2.6"/>', *shoes("#6E4C33"))
    coat = g("coat",
             f'<path d="M72 118Q100 106 128 118L134 214L66 214Z" fill="{SEA}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q120 112 128 118L134 214L112 214Z" fill="{SEAD}"/>',
             f'<path d="M90 114L110 114L106 190L94 190Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>',
             *[f'<circle cx="100" cy="{y}" r="2" fill="{CLAY}"/>' for y in (136, 152, 168)],
             f'<path d="M86 112Q100 124 114 112L110 122L100 118L90 122Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M92 118L100 124L108 118L108 128L100 124L92 128Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>',
             f'<path d="M80 120L92 170M120 120L108 170" stroke="{SEAD}" stroke-width="2"/>')
    arms = g("arms",
             limb("M76 124Q60 136 56 152", SEA, 12),
             limb("M124 124Q136 112 138 96", SEA, 12),
             f'<circle cx="56" cy="154" r="6" fill="{RS}" stroke="{INK}" stroke-width="2.4"/>',
             # puntero señalando una viñeta
             f'<path d="M138 96L170 70" stroke="{INK}" stroke-width="5"/><path d="M138 96L170 70" stroke="#C9A77E" stroke-width="2.6"/>',
             f'<circle cx="138" cy="94" r="6" fill="{RS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base(RS, RSD, [
        f'<path d="M62 76Q58 94 70 104M138 76Q142 94 130 104" fill="none" stroke="#B9B2A8" stroke-width="6"/>',
        # chistera abollada con clavel
        f'<path d="M62 46Q100 38 138 46L138 52Q100 44 62 52Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>',
        f'<path d="M74 46L72 8L126 4L126 44Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.6"/>',
        f'<path d="M100 6L126 4L126 44L106 45Z" fill="#1E1D25"/>',
        f'<path d="M74 22L126 18" stroke="#4A4A55" stroke-width="2"/>',
        f'<path d="M73 34L126 30L126 38L73 42Z" fill="{VIOLET}" stroke="{INK}" stroke-width="1.4"/>',
        *[f'<circle cx="{120 + dx}" cy="{30 + dy}" r="4" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"/>' for dx, dy in [(-3, -2), (3, -2), (0, 3)]],
        f'<ellipse cx="78" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".4"/><ellipse cx="122" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".4"/>']))
    rim = g("rim", f'<path d="M70 126L68 208" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    return lambda e: svg(e, [SHADOW, board, legs, coat, arms, head, face_of(e).replace("#5A3A22", "#4A3A2A"), rim])


# ---------------------------------------------------------------------------
# El Comparsista: tricornio con pluma, gola blanca, capa morada y medio rostro pintado
# ---------------------------------------------------------------------------
CS = "#E8B58E"; CSD = "#CB9670"


def comparsista():
    cape = g("cape",
             f'<path d="M64 120Q100 104 136 120L150 232L50 232Z" fill="{VIOLET}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M110 110Q128 114 136 120L150 232L126 232Z" fill="{VIOLETD}"/>',
             f'<path d="M50 232Q100 222 150 232" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    legs = g("legs",
             f'<path d="M84 206L116 206L115 238L104 238L100 222L96 238L85 238Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.6"/>', *shoes())
    body = g("body",
             f'<path d="M78 120Q100 110 122 120L126 208L74 208Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.6"/>',
             *[f'<path d="M84 {y}H116" stroke="{GOLD}" stroke-width="2"/>' for y in (140, 156, 172, 188)],
             # gola
             f'<path d="M78 116Q86 106 94 116Q100 106 106 116Q114 106 122 116Q116 128 100 128Q84 128 78 116Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    arms = g("arms",
             limb("M78 126Q62 120 54 100", "#2B2A33", 11),
             limb("M122 126Q140 136 146 152", "#2B2A33", 11),
             f'<path d="M48 96L60 92M48 100L60 104" stroke="{PAPER}" stroke-width="3"/>',
             f'<circle cx="54" cy="98" r="6" fill="{CS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="146" cy="154" r="6" fill="{CS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base(CS, CSD, [
        # media cara pintada de blanco con una lágrima dorada (maquillaje de comparsa)
        f'<path d="M100 36Q138 38 138 74Q140 104 100 108Z" fill="#F7F3EA" opacity=".85"/>',
        f'<path d="M122 96Q124 102 121 106Q118 102 122 96Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>',
        f'<path d="M62 70Q60 44 78 40Q70 54 70 74Z" fill="#2A1E1A"/>',
        # tricornio con pluma
        f'<path d="M54 50Q100 20 146 50Q126 46 100 54Q74 46 54 50Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>',
        f'<path d="M70 44Q100 8 130 44Q100 34 70 44Z" fill="#1E1D25" stroke="{INK}" stroke-width="2.2"/>',
        f'<path d="M58 50Q100 32 142 50" fill="none" stroke="{GOLD}" stroke-width="2.4"/>',
        f'<path d="M120 30Q146 6 160 14Q146 20 128 38Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>',
        f'<path d="M124 34Q144 14 156 16" fill="none" stroke="#D8CBB3" stroke-width="1.2"/>'])
    )
    rim = g("rim", f'<path d="M56 136L52 226" fill="none" stroke="#FFF" stroke-width="2" opacity=".35"/>')
    return lambda e: svg(e, [SHADOW, cape, legs, body, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


# ---------------------------------------------------------------------------
# El Corista: canotier, traje blanco con fajín rojo y una bandurria
# ---------------------------------------------------------------------------
KS = "#D9A27A"; KSD = "#B98260"


def corista():
    legs = g("legs",
             f'<path d="M82 204L118 204L117 238L104 238L100 220L96 238L83 238Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M100 206L117 206L116 238L105 238Z" fill="#E6DCC6"/>', *shoes("#6E4C33"))
    suit = g("suit",
             f'<path d="M72 118Q100 106 128 118L132 206L68 206Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q120 112 128 118L132 206L112 206Z" fill="#E6DCC6"/>',
             f'<path d="M70 168L130 168L131 182L69 182Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M126 172L140 196L130 196Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M92 112L100 128L108 112" fill="{SEA}" stroke="{INK}" stroke-width="1.6"/>')
    bandurria = g("bandurria",
                  f'<path d="M60 150Q46 150 46 166Q46 184 66 184Q86 184 86 166Q86 150 70 150Z" fill="#C9885A" stroke="{INK}" stroke-width="2.2"/>',
                  f'<circle cx="66" cy="166" r="6" fill="#3A2418" stroke="{INK}" stroke-width="1.4"/>',
                  f'<path d="M72 156L126 110" stroke="{INK}" stroke-width="7"/><path d="M72 156L126 110" stroke="#6E4C33" stroke-width="4"/>',
                  f'<path d="M124 104L136 100L136 110L128 114Z" fill="#6E4C33" stroke="{INK}" stroke-width="1.6"/>',
                  f'<path d="M58 172L124 108M62 174L126 110" stroke="#F4E4CC" stroke-width=".8"/>')
    arms = g("arms",
             limb("M76 124Q66 146 72 162", PAPER, 12),
             limb("M124 124Q124 138 110 138", PAPER, 12),
             f'<circle cx="72" cy="164" r="6" fill="{KS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="106" cy="138" r="6" fill="{KS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base(KS, KSD, [
        f'<path d="M62 74Q60 50 74 44Q70 58 70 76Z" fill="#3A2A20"/><path d="M138 74Q140 50 126 44Q130 58 130 76Z" fill="#3A2A20"/>',
        # canotier de paja con cinta morada
        f'<path d="M50 50Q100 40 150 50Q146 58 100 54Q54 58 50 50Z" fill="#E9CF8A" stroke="{INK}" stroke-width="2.4"/>',
        f'<path d="M70 48L72 22Q100 16 128 22L130 48Z" fill="#E9CF8A" stroke="{INK}" stroke-width="2.4"/>',
        f'<path d="M71 38L129 38L130 46L70 46Z" fill="{VIOLET}" stroke="{INK}" stroke-width="1.4"/>',
        *[f'<path d="M{x} 24L{x + 2} 36" stroke="#C9AE68" stroke-width="1"/>' for x in range(78, 126, 8)]]))
    rim = g("rim", f'<path d="M70 126L68 200" fill="none" stroke="#FFF" stroke-width="2" opacity=".5"/>')
    return lambda e: svg(e, [SHADOW, legs, suit, bandurria, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


# ---------------------------------------------------------------------------
# El Cuartetero: chaqueta de cuadros, gorra, pajarita enorme, claves en las manos y pito
# ---------------------------------------------------------------------------
QS = "#EDC19C"; QSD = "#CF9D78"


def cuartetero():
    legs = g("legs",
             f'<path d="M84 206L116 206L114 238L104 238L100 222L96 238L86 238Z" fill="{SEA}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M86 230H96M104 230H114" stroke="{SEAD}" stroke-width="2"/>', *shoes(CLAY))
    jacket = g("jacket",
               f'<path d="M72 118Q100 106 128 118L132 208L68 208Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.8"/>',
               *[f'<path d="M{x} 116V206" stroke="{GOLDD}" stroke-width="3"/>' for x in (80, 92, 108, 120)],
               *[f'<path d="M70 {y}H130" stroke="{GOLDD}" stroke-width="3"/>' for y in (132, 150, 168, 186)],
               f'<path d="M72 118Q100 106 128 118L132 208L68 208Z" fill="none" stroke="{INK}" stroke-width="2.8"/>',
               f'<path d="M92 114L100 150L108 114Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>',
               # pajarita enorme
               f'<path d="M100 122L72 108L74 138Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>',
               f'<path d="M100 122L128 108L126 138Z" fill="{CLAY}" stroke="{INK}" stroke-width="2"/>',
               f'<circle cx="100" cy="122" r="5" fill="{CLAYD}" stroke="{INK}" stroke-width="1.6"/>')
    arms = g("arms",
             limb("M76 126Q58 130 50 118", GOLD, 12),
             limb("M124 126Q142 130 150 118", GOLD, 12),
             # claves de madera
             f'<path d="M40 126L58 100" stroke="{INK}" stroke-width="7"/><path d="M40 126L58 100" stroke="#C9885A" stroke-width="4"/>',
             f'<path d="M142 100L160 126" stroke="{INK}" stroke-width="7"/><path d="M142 100L160 126" stroke="#C9885A" stroke-width="4"/>',
             f'<circle cx="50" cy="116" r="6" fill="{QS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="150" cy="116" r="6" fill="{QS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base(QS, QSD, [
        f'<path d="M62 70Q60 52 72 46M138 70Q140 52 128 46" fill="none" stroke="#6B3A22" stroke-width="7"/>',
        # nariz de payaso de cartón
        f'<circle cx="100" cy="86" r="0" fill="none"/>',
        # gorra de visera, del revés… no: de lado
        f'<path d="M62 52Q64 24 100 22Q136 24 138 52Q100 42 62 52Z" fill="{SEA}" stroke="{INK}" stroke-width="2.6"/>',
        f'<path d="M100 22Q134 26 138 52Q124 46 112 45Q114 30 100 22Z" fill="{SEAD}"/>',
        f'<path d="M62 52Q44 50 38 58Q54 60 66 56Z" fill="{SEAD}" stroke="{INK}" stroke-width="2"/>',
        f'<circle cx="100" cy="22" r="3.4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>',
        # pito de caña detrás de la oreja
        f'<path d="M140 64L156 50" stroke="{INK}" stroke-width="6"/><path d="M140 64L156 50" stroke="#D9B26A" stroke-width="3"/>',
        f'<ellipse cx="78" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".5"/><ellipse cx="122" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".5"/>']))
    rim = g("rim", f'<path d="M70 126L68 200" fill="none" stroke="#FFF" stroke-width="2" opacity=".4"/>')
    return lambda e: svg(e, [SHADOW, legs, jacket, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


# ---------------------------------------------------------------------------
# Semana Santa: el Cargador, el Maniguetero y la Saetera (tono sobrio)
# ---------------------------------------------------------------------------
AS = "#D9A27A"; ASD = "#B98260"; PURPLE = "#4A2A5A"; PURPLED = "#361E44"


def cargador():
    legs = g("legs",
             f'<path d="M82 200L118 200L117 238L104 238L100 218L96 238L83 238Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.6"/>', *shoes())
    body = g("body",
             f'<path d="M72 118Q100 106 128 118L132 204L68 204Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 112Q120 112 128 118L132 204L112 204Z" fill="#E6DCC6"/>',
             f'<path d="M92 112L100 128L108 112" fill="{AS}" stroke="{INK}" stroke-width="1.8"/>',
             # faja negra
             f'<path d="M68 170L132 170L133 188L67 188Z" fill="#2B2A33" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M126 176L138 204L128 202Z" fill="#2B2A33" stroke="{INK}" stroke-width="1.6"/>',
             # almohadilla sobre el hombro
             f'<path d="M110 110Q128 104 140 116L136 126Q124 116 112 120Z" fill="#8A6A4A" stroke="{INK}" stroke-width="1.8"/>')
    arms = g("arms",
             limb("M76 124Q60 136 58 154", PAPER, 12),
             limb("M124 124Q142 132 146 150", PAPER, 12),
             f'<circle cx="58" cy="156" r="6" fill="{AS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="146" cy="152" r="6" fill="{AS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base(AS, ASD, [
        f'<path d="M60 72Q56 38 100 34Q144 38 140 72Q132 50 112 48Q100 54 86 50Q68 54 60 72Z" fill="#2A1E1A" stroke="{INK}" stroke-width="2.4"/>',
        f'<path d="M62 72L64 88M138 72L136 88" stroke="#2A1E1A" stroke-width="5"/>',
        f'<path d="M70 94Q76 106 100 108Q124 106 130 94Q126 104 100 104Q74 104 70 94Z" fill="#6B5343" opacity=".4"/>']))
    rim = g("rim", f'<path d="M70 126L68 200" fill="none" stroke="#FFF" stroke-width="2" opacity=".5"/>')
    return lambda e: svg(e, [SHADOW, legs, body, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


def maniguetero():
    staff = g("staff",
              f'<path d="M156 40L156 246" stroke="{INK}" stroke-width="7"/><path d="M156 40L156 246" stroke="#8A6243" stroke-width="4"/>',
              f'<path d="M146 30Q146 44 156 44Q166 44 166 30" fill="none" stroke="{INK}" stroke-width="6"/><path d="M146 30Q146 44 156 44Q166 44 166 30" fill="none" stroke="#C9A77E" stroke-width="3"/>',
              f'<path d="M150 244H162" stroke="{INK}" stroke-width="3"/>')
    robe = g("robe",
             f'<path d="M72 116Q100 104 128 116L138 244L62 244Z" fill="{PURPLE}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M104 110Q120 110 128 116L138 244L112 244Z" fill="{PURPLED}"/>',
             f'<path d="M84 120Q82 180 76 240M116 120Q118 180 124 240" fill="none" stroke="{PURPLED}" stroke-width="1.8"/>',
             # cíngulo blanco
             f'<path d="M70 168Q100 176 130 168" fill="none" stroke="{PAPER}" stroke-width="4"/>',
             f'<path d="M92 172L88 214M96 172L94 206" stroke="{PAPER}" stroke-width="3"/>',
             f'<circle cx="88" cy="216" r="3" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    arms = g("arms",
             limb("M76 124Q62 140 70 160", PURPLE, 12),
             limb("M124 124Q142 118 152 104", PURPLE, 12),
             f'<circle cx="70" cy="162" r="6" fill="{AS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="154" cy="102" r="6" fill="{AS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base("#E3AE88", "#C58E68", [
        f'<path d="M60 70Q58 40 100 36Q142 40 140 70Q128 52 100 50Q72 52 60 70Z" fill="#8A8480" stroke="{INK}" stroke-width="2.2"/>',
        f'<path d="M62 70L64 86M138 70L136 86" stroke="#8A8480" stroke-width="5"/>']))
    rim = g("rim", f'<path d="M68 126L64 236" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')
    return lambda e: svg(e, [SHADOW, staff, robe, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


def saetera():
    dress = g("dress",
              f'<path d="M74 118Q100 106 126 118L140 244L60 244Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M104 112Q120 112 126 118L140 244L114 244Z" fill="#1E1D25"/>',
              f'<path d="M60 244Q100 234 140 244" fill="none" stroke="#4A4A55" stroke-width="2"/>',
              f'<circle cx="100" cy="124" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    arms = g("arms",
             limb("M76 124Q64 136 84 146", "#2B2A33", 11),
             limb("M124 124Q142 116 150 96", "#2B2A33", 11),
             f'<circle cx="88" cy="146" r="6" fill="{KS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="150" cy="94" r="6" fill="{KS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head", *head_base("#E8B58E", "#CB9670", [
        f'<path d="M60 76Q54 36 100 32Q146 36 140 76Q132 52 100 50Q68 52 60 76Z" fill="#2A1E1A" stroke="{INK}" stroke-width="2.4"/>',
        # peineta y mantilla negra de encaje
        f'<path d="M66 40Q100 -4 134 40Q124 30 100 28Q76 30 66 40Z" fill="#6B4A2A" stroke="{INK}" stroke-width="2"/>',
        f'<ellipse cx="78" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".45"/><ellipse cx="122" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".45"/>',
        f'<circle cx="61" cy="92" r="3" fill="{GOLD}" stroke="{INK}" stroke-width="1"/><circle cx="139" cy="92" r="3" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>']))
    rim = g("rim", f'<path d="M70 126L64 238" fill="none" stroke="#FFF" stroke-width="2" opacity=".3"/>')
    # la mantilla cae desde la peineta por detrás de la cabeza, hasta los hombros
    mantilla = g("mantilla",
                 f'<path d="M66 40Q100 6 134 40L150 128Q128 118 100 118Q72 118 50 128Z" fill="#1E1D25" stroke="{INK}" stroke-width="1.8"/>',
                 *[f'<circle cx="{x}" cy="{y}" r="2.2" fill="none" stroke="#6B6B78" stroke-width=".9"/>' for x, y in [(56, 100), (60, 116), (144, 100), (140, 116), (62, 76), (138, 76), (52, 124), (148, 124)]])
    return lambda e: svg(e, [SHADOW, mantilla, dress, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


if __name__ == "__main__":
    for key, build in [("romancero", romancero()), ("comparsista", comparsista()), ("corista", corista()), ("cuartetero", cuartetero()),
                       ("cargador", cargador()), ("maniguetero", maniguetero()), ("saetera", saetera())]:
        write(key, build)
    print("personajes del Carnaval generados")
