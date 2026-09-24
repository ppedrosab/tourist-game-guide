#!/usr/bin/env python3
"""
Guías de la ruta gastronómica de Cádiz: la Pescaera (mar) y el Chicharronero (tierra).
El Chirigotero está en cadiz_sprites.py.

Uso: python3 scripts/art/cadiz_gastro_sprites.py && npm run gen:assets
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_sprites import (INK, CLAY, CLAYD, SEA, SEAD, GOLD, GOLDD, PAPER, SHADOW, face_of, g, limb, svg, write)

# ---------------------------------------------------------------------------
# La Pescaera: coleta, aros, camiseta de rayas, mandil verde, botas blancas y un pescado
# ---------------------------------------------------------------------------
PS = "#E3A982"; PSD = "#C88A63"; HAIR = "#2A1E1A"; APRON = "#3F7A6E"; APROND = "#2F5F55"


def pescaera():
    legs = g("legs",
             limb("M90 214L89 236", PS, 9), limb("M110 214L111 236", PS, 9),
             f'<path d="M80 226L96 226L97 248L78 248Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 226L120 226L122 248L103 248Z" fill="#E6DCC6" stroke="{INK}" stroke-width="2.4"/>')
    body = g("body",
             f'<path d="M74 118Q100 106 126 118L130 190L70 190Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
             *[f'<path d="M72 {y}Q100 {y - 4} 128 {y}" fill="none" stroke="{SEA}" stroke-width="3.4"/>' for y in (128, 142, 156, 170, 184)],
             f'<path d="M74 118Q100 106 126 118L130 190L70 190Z" fill="none" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M72 188L128 188L124 222L76 222Z" fill="#2E3A48" stroke="{INK}" stroke-width="2.4"/>',
             # mandil largo
             f'<path d="M80 124Q100 118 120 124L126 226L74 226Z" fill="{APRON}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 122L120 124L126 226L108 226Z" fill="{APROND}"/>',
             f'<path d="M80 124L72 112M120 124L128 112" stroke="{APRON}" stroke-width="3"/>',
             f'<path d="M86 170H114V190H86Z" fill="{APROND}" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M90 164Q94 158 98 164" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    arms = g("arms",
             limb("M76 124Q60 134 54 148", PS, 11),
             limb("M124 124Q142 118 150 104", PS, 11),
             f'<path d="M80 120Q70 124 66 132L74 136Q78 128 84 126Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M120 120Q130 118 136 110L142 116Q134 126 124 128Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>',
             f'<circle cx="54" cy="150" r="6" fill="{PS}" stroke="{INK}" stroke-width="2.4"/>',
             # pescado (una dorada) cogido por la cola, en alto
             f'<path d="M150 98Q170 70 182 60Q176 90 160 112Z" fill="#B9C8D0" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M152 100Q176 64 184 58" fill="none" stroke="#8FA6B3" stroke-width="1.6"/>',
             f'<path d="M182 60L192 50L184 48L186 40L178 50Z" fill="#8FA6B3" stroke="{INK}" stroke-width="1.6"/>',
             f'<path d="M164 94Q168 90 172 92" fill="none" stroke="{GOLD}" stroke-width="2.4"/>',
             f'<circle cx="160" cy="104" r="1.8" fill="{INK}"/>',
             f'<circle cx="150" cy="104" r="6" fill="{PS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M91 96L91 114L109 114L109 96Z" fill="{PS}"/>',
             # coleta por detrás
             f'<path d="M126 50Q156 60 150 100Q146 84 132 76Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.2"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{PS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{PS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<circle cx="61" cy="94" r="5" fill="none" stroke="{GOLD}" stroke-width="2.4"/>',
             f'<circle cx="139" cy="94" r="5" fill="none" stroke="{GOLD}" stroke-width="2.4"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{PS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{PSD}" opacity=".5"/>',
             f'<path d="M60 72Q54 30 100 28Q146 30 140 72Q132 50 112 46Q104 56 84 52Q70 56 60 72Z" fill="{HAIR}" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M78 38Q90 32 102 32" fill="none" stroke="#4A3A32" stroke-width="2.2"/>',
             # pañuelo rojo como diadema
             f'<path d="M62 56Q100 36 138 56L136 62Q100 44 64 62Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M136 58L148 50L146 62Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>',
             f'<ellipse cx="78" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".4"/><ellipse cx="122" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".4"/>')
    rim = g("rim", f'<path d="M70 126L68 188" fill="none" stroke="#FFF" stroke-width="2" opacity=".5"/>')
    return lambda e: svg(e, [SHADOW, legs, body, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


# ---------------------------------------------------------------------------
# El Chicharronero: bata y gorro blancos, pañuelo rojo, bigote y un papel con chicharrones
# ---------------------------------------------------------------------------
CS = "#E0A77A"; CSD = "#C28862"; MUST = "#2A1E1A"


def chicharronero():
    legs = g("legs",
             f'<path d="M80 204L120 204L118 238L104 238L100 220L96 238L82 238Z" fill="#4A4A55" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M76 248Q78 238 92 238Q98 240 98 248Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M102 248Q102 240 108 238Q122 238 124 248Z" fill="#2B2A33" stroke="{INK}" stroke-width="2.4"/>')
    coat = g("coat",
             # barriga redonda bajo la bata
             f'<path d="M70 120Q100 106 130 120Q146 160 132 210L68 210Q54 160 70 120Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.8"/>',
             f'<path d="M108 112Q126 114 130 120Q146 160 132 210L112 210Q128 160 108 112Z" fill="#E6DCC6"/>',
             f'<path d="M100 124L100 208" stroke="#D8CBB3" stroke-width="1.8"/>',
             *[f'<circle cx="104" cy="{y}" r="2.4" fill="#D8CBB3" stroke="{INK}" stroke-width="1"/>' for y in (140, 160, 180, 200)],
             f'<path d="M86 112Q100 124 114 112L112 122Q100 132 88 122Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.8"/>',
             f'<path d="M96 124L100 136L104 124Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.4"/>',
             f'<path d="M80 180Q100 186 120 180" fill="none" stroke="#E6DCC6" stroke-width="2"/>',
             f'<path d="M116 150H128V160H116Z" fill="none" stroke="#D8CBB3" stroke-width="1.6"/>')
    arms = g("arms",
             limb("M74 126Q56 136 50 150", PAPER, 13),
             limb("M126 126Q146 134 152 148", PAPER, 13),
             f'<circle cx="50" cy="152" r="6.5" fill="{CS}" stroke="{INK}" stroke-width="2.4"/>',
             # papel de estraza con chicharrones y medio limón
             f'<path d="M136 150L180 142L184 160L140 168Z" fill="#E8D8B8" stroke="{INK}" stroke-width="2"/>',
             *[f'<g transform="rotate(-10 {x} 152)"><rect x="{x - 6}" y="146" width="12" height="9" rx="1.5" fill="#C9885A" stroke="{INK}" stroke-width="1.2"/><rect x="{x - 6}" y="146" width="12" height="2.4" fill="#F4E4CC"/></g>' for x in (148, 160, 172)],
             f'<path d="M176 136A7 7 0 0 1 186 144L176 144Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>',
             f'<circle cx="152" cy="152" r="6.5" fill="{CS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{CS}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{CS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{CS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 38 100 36Q140 38 138 74Q140 106 100 110Q60 106 62 74Z" fill="{CS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 42Q140 52 138 74Q138 102 110 109Q128 92 126 68Q124 50 118 42Z" fill="{CSD}" opacity=".5"/>',
             f'<path d="M62 70L64 90M138 70L136 90" stroke="#3A2A20" stroke-width="5"/>',
             # bigote por encima de la boca
             f'<path d="M80 90Q90 82 100 88Q110 82 120 90Q112 94 100 91Q88 94 80 90Z" fill="{MUST}" stroke="{INK}" stroke-width="1.4"/>',
             f'<ellipse cx="78" cy="96" rx="6" ry="3.4" fill="#E88A78" opacity=".45"/><ellipse cx="122" cy="96" rx="6" ry="3.4" fill="#E88A78" opacity=".45"/>',
             # gorro blanco de obrador
             f'<path d="M60 54Q58 20 100 18Q142 20 140 54Q120 46 100 46Q80 46 60 54Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M100 18Q134 20 140 54Q128 48 116 47Q118 30 100 18Z" fill="#E6DCC6"/>',
             f'<path d="M60 54Q100 44 140 54L140 60Q100 50 60 60Z" fill="#E6DCC6" stroke="{INK}" stroke-width="2"/>',
             f'<ellipse cx="80" cy="68" rx="7" ry="3.2" fill="#FFF" opacity=".2"/>')
    # la boca va un poco más abajo para no quedar bajo el bigote
    face = lambda e: face_of(e).replace('<g id="face">', '<g id="face" transform="translate(0 2)">').replace("#5A3A22", "#3A2A1E")
    rim = g("rim", f'<path d="M66 132Q60 170 70 206" fill="none" stroke="#FFF" stroke-width="2" opacity=".6"/>')
    return lambda e: svg(e, [SHADOW, legs, coat, arms, head, face(e), rim])


# ---------------------------------------------------------------------------
# El Garumero: romano de Gades que fabrica garum. Túnica corta, delantal, ánfora y tablilla
# ---------------------------------------------------------------------------
GS = "#D9A27A"; GSD = "#B98260"; TUN = "#C9A77E"; TUND = "#A88A63"


def garumero():
    legs = g("legs",
             limb("M90 206L89 240", GS, 9), limb("M110 206L111 240", GS, 9),
             f'<path d="M84 228L95 234M84 236L95 242M105 234L116 228M105 242L116 236" stroke="#6E4C33" stroke-width="2"/>',
             f'<path d="M78 248Q80 241 90 242Q97 243 96 248Z" fill="#8A6243" stroke="{INK}" stroke-width="2.4"/>',
             f'<path d="M104 248Q103 243 110 242Q120 241 122 248Z" fill="#8A6243" stroke="{INK}" stroke-width="2.4"/>')
    amphora = g("amphora",
                f'<path d="M160 118Q180 130 178 170Q176 196 166 212L160 222L154 212Q144 196 142 170Q140 130 160 118Z" fill="#B8683A" stroke="{INK}" stroke-width="2.4"/>',
                f'<path d="M160 120Q178 132 176 170Q174 194 164 212L160 222Q168 190 166 160Q164 132 160 120Z" fill="#96532C"/>',
                f'<path d="M152 106H168V118H152Z" fill="#B8683A" stroke="{INK}" stroke-width="2"/>',
                f'<path d="M152 112Q140 110 144 126M168 112Q180 110 176 126" fill="none" stroke="{INK}" stroke-width="2.4"/>',
                f'<path d="M146 150Q160 156 174 150" fill="none" stroke="#F0C69A" stroke-width="2"/>',
                # etiqueta pintada: un pececillo
                f'<path d="M152 166Q160 160 166 166Q160 172 152 166ZM166 166L170 162V170Z" fill="#F4E4CC" stroke="{INK}" stroke-width="1"/>')
    tunic = g("tunic",
              f'<path d="M72 118Q100 106 128 118L134 210L66 210Z" fill="{TUN}" stroke="{INK}" stroke-width="2.8"/>',
              f'<path d="M104 112Q120 112 128 118L134 210L112 210Z" fill="{TUND}"/>',
              f'<path d="M88 112Q100 122 112 112" fill="none" stroke="{TUND}" stroke-width="3"/>',
              f'<path d="M68 156L132 156L133 166L67 166Z" fill="#6E4C33" stroke="{INK}" stroke-width="2"/>',
              f'<circle cx="100" cy="161" r="3.4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>',
              # delantal de faena con manchas
              f'<path d="M82 166L118 166L122 206L78 206Z" fill="#E6DCC6" stroke="{INK}" stroke-width="2"/>',
              *[f'<circle cx="{x}" cy="{y}" r="{r}" fill="#A86F47" opacity=".5"/>' for x, y, r in [(90, 180, 3), (108, 190, 2.4), (98, 198, 2)]],
              f'<path d="M66 208Q100 214 134 208" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    arms = g("arms",
             limb("M76 124Q58 132 50 146", GS, 11),
             limb("M124 124Q142 132 152 146", GS, 11),
             # tablilla de cera con estilo
             f'<path d="M28 138L60 132L64 160L32 166Z" fill="#8A6243" stroke="{INK}" stroke-width="2"/>',
             f'<path d="M32 142L58 137L61 157L35 162Z" fill="#E0C06A" stroke="{INK}" stroke-width="1.2"/>',
             *[f'<path d="M36 {146 + k * 5}L56 {142 + k * 5}" stroke="#8A6243" stroke-width="1"/>' for k in range(3)],
             f'<circle cx="50" cy="148" r="6" fill="{GS}" stroke="{INK}" stroke-width="2.4"/>',
             f'<circle cx="152" cy="148" r="6" fill="{GS}" stroke="{INK}" stroke-width="2.4"/>')
    head = g("head",
             f'<path d="M90 96L90 114L110 114L110 96Z" fill="{GS}"/>',
             f'<ellipse cx="61" cy="80" rx="6" ry="8" fill="{GS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<ellipse cx="139" cy="80" rx="6" ry="8" fill="{GS}" stroke="{INK}" stroke-width="2.6"/>',
             f'<path d="M62 74Q60 36 100 34Q140 36 138 74Q140 104 100 108Q60 104 62 74Z" fill="{GS}" stroke="{INK}" stroke-width="3"/>',
             f'<path d="M118 40Q140 50 138 74Q138 100 110 107Q128 90 126 66Q124 48 118 40Z" fill="{GSD}" opacity=".5"/>',
             # calvo por arriba, flequillo de rizos a los lados
             *[f'<circle cx="{x}" cy="{y}" r="6" fill="#4A3222" stroke="{INK}" stroke-width="1.6"/>' for x, y in [(64, 60), (66, 48), (72, 40), (136, 60), (134, 48), (128, 40)]],
             f'<ellipse cx="96" cy="46" rx="16" ry="6" fill="#FFF" opacity=".25"/>',
             # barba de tres días
             f'<path d="M70 94Q76 108 100 110Q124 108 130 94Q126 104 100 106Q74 104 70 94Z" fill="#6B5343" opacity=".45"/>',
             f'<ellipse cx="78" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".35"/><ellipse cx="122" cy="92" rx="6" ry="3.4" fill="#E88A78" opacity=".35"/>')
    rim = g("rim", f'<path d="M70 126L68 206" fill="none" stroke="#FFF" stroke-width="2" opacity=".4"/>')
    return lambda e: svg(e, [SHADOW, legs, amphora, tunic, arms, head, face_of(e).replace("#5A3A22", "#3A2A1E"), rim])


if __name__ == "__main__":
    for key, build in [("pescaera", pescaera()), ("chicharronero", chicharronero()), ("garumero", garumero())]:
        write(key, build)
    print("guías gastronómicos de Cádiz generados")
