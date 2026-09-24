#!/usr/bin/env python3
"""
Fondos de Cádiz (viewBox 390×560, como los de Málaga). Cada escena es un SVG con un
grupo de primer nivel por capa de parallax: sky · far · mid|sea · near · fx.
`render_layers.py` los convierte en assets/backgrounds/layers/bg_cadiz_{escena}_{n}_{capa}@2x|@3x.webp.

Uso: python3 scripts/art/cadiz_scenes.py && python3 scripts/art/render_layers.py cadiz_ && npm run gen:assets
"""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "backgrounds", "svg")
INK = "#1B2A3A"; CLAY = "#A8431F"; SEA = "#2F6F73"; GOLD = "#F2C14E"; PAPER = "#FFF8EC"
WIN = "#3E3024"; LIT = "#F4C66A"; SHUT = "#4E7A5E"; SHUTD = "#3B5F48"
FLOOR = "#E8CFAB"; FLOORL = "#D7B994"; SAND = "#EADFCB"
W, H = 390, 560

# Fachadas gaditanas: blanco, amarillo albero, rosa, verde agua (color, sombra, luz)
WHITE = ("#F7F0E4", "#E3D5BE", "#FFFBF3")
YELLOW = ("#F2D48F", "#DDB86A", "#F9E4B0")
PINK = ("#EFB7A0", "#D99A82", "#F7CDBB")
MINT = ("#C6DDD2", "#A8C4B8", "#DDEDE6")
STONE = ("#EFDCB8", "#D2B78C", "#FBF0DA")


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------------------
# Cielo
# ---------------------------------------------------------------------------
def defs_common(p):
    return (f'<defs><linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E79E70"/>'
            f'<stop offset=".4" stop-color="#F3C79B"/><stop offset=".6" stop-color="#F8DDB8"/><stop offset="1" stop-color="#FBEBD3"/></linearGradient>'
            f'<radialGradient id="{p}glow"><stop offset="0" stop-color="#FFF4DD" stop-opacity=".9"/><stop offset=".3" stop-color="#FFF4DD" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="#FFF4DD" stop-opacity="0"/></radialGradient>'
            f'<pattern id="{p}dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r=".8" fill="#C9A57E" opacity=".5"/>'
            f'<circle cx="5" cy="4.5" r=".6" fill="#C9A57E" opacity=".4"/></pattern>'
            f'<linearGradient id="{p}sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FB9B4"/><stop offset="1" stop-color="#6E9FA0"/></linearGradient>'
            f'<linearGradient id="{p}dome" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F9D776"/><stop offset=".45" stop-color="#EDB943"/><stop offset="1" stop-color="#C98E2A"/></linearGradient>'
            f'</defs>')


def cloud(x, y, s=1.0):
    return (f'<g opacity=".9"><ellipse cx="{f(x)}" cy="{f(y + 6 * s)}" rx="{f(34 * s)}" ry="{f(9 * s)}" fill="#FFF6EA"/>'
            f'<circle cx="{f(x - 14 * s)}" cy="{f(y)}" r="{f(11 * s)}" fill="#FFF6EA"/><circle cx="{f(x + 2 * s)}" cy="{f(y - 5 * s)}" r="{f(14 * s)}" fill="#FFF6EA"/>'
            f'<circle cx="{f(x + 17 * s)}" cy="{f(y + 1 * s)}" r="{f(9 * s)}" fill="#FFF6EA"/></g>')


def bird(x, y, s=1.0):
    return f'<path d="M{f(x - 6 * s)} {f(y)}Q{f(x - 3 * s)} {f(y - 4 * s)} {f(x)} {f(y)}Q{f(x + 3 * s)} {f(y - 4 * s)} {f(x + 6 * s)} {f(y)}" fill="none" stroke="{INK}" stroke-width="1.3" opacity=".7"/>'


def sky(p, sun, clouds=(), birds=()):
    sx, sy = sun
    return (f'<g id="sky"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}sky)"/>'
            f'<circle cx="{sx}" cy="{sy}" r="108.8" fill="url(#{p}glow)"/><circle cx="{sx}" cy="{sy}" r="34" fill="#FFF3DC"/>'
            + "".join(cloud(*c) for c in clouds) + "".join(bird(*b) for b in birds) + "</g>")


# ---------------------------------------------------------------------------
# Piezas
# ---------------------------------------------------------------------------
def window(x, y, w, h, shutters=True, lit=False, balcony=False, arch=False, sw=1.4):
    top = f"Q{f(x + w / 2)} {f(y - w * .55)} {f(x + w)} {f(y)}" if arch else f"L{f(x + w)} {f(y)}"
    s = f'<path d="M{f(x)} {f(y + h)}L{f(x)} {f(y)}{top}L{f(x + w)} {f(y + h)}Z" fill="{LIT if lit else WIN}" stroke="{INK}" stroke-width="{sw}"/>'
    if shutters:
        s += (f'<path d="M{f(x - w * .42)} {f(y)}L{f(x - 1)} {f(y)}L{f(x - 1)} {f(y + h)}L{f(x - w * .42)} {f(y + h)}Z" fill="{SHUT}" stroke="{INK}" stroke-width="{sw * .7:.2f}"/>'
              f'<path d="M{f(x + w + 1)} {f(y)}L{f(x + w * 1.42)} {f(y)}L{f(x + w * 1.42)} {f(y + h)}L{f(x + w + 1)} {f(y + h)}Z" fill="{SHUTD}" stroke="{INK}" stroke-width="{sw * .7:.2f}"/>')
    if balcony:
        by = y + h * .62
        s += f'<path d="M{f(x - w * .25)} {f(y + h)}L{f(x + w * 1.25)} {f(y + h)}" fill="none" stroke="{INK}" stroke-width="{sw * 1.6:.2f}"/>'
        s += f'<path d="M{f(x - w * .25)} {f(by)}L{f(x + w * 1.25)} {f(by)}" fill="none" stroke="{INK}" stroke-width="{sw * .8:.2f}"/>'
        n = 5
        s += "".join(f'<path d="M{f(x - w * .25 + i * w * 1.5 / n)} {f(by)}L{f(x - w * .25 + i * w * 1.5 / n)} {f(y + h)}" fill="none" stroke="{INK}" stroke-width="{sw * .6:.2f}"/>' for i in range(n + 1))
    return s


def house(x, y, w, h, col, floors=3, cols=2, stroke=1.8, lit=(), cierro=False, cornice=True, roof_rail=True, door=True):
    """Casa gaditana: fachada lisa de color, ventanas con postigos y balcón, azotea con pretil."""
    c, cd, cl = col
    s = f'<path d="M{f(x)} {f(y)}L{f(x + w)} {f(y)}L{f(x + w)} {f(y + h)}L{f(x)} {f(y + h)}Z" fill="{c}" stroke="{INK}" stroke-width="{stroke}"/>'
    s += f'<path d="M{f(x + w * .82)} {f(y + 2)}L{f(x + w - 1)} {f(y + 2)}L{f(x + w - 1)} {f(y + h)}L{f(x + w * .82)} {f(y + h)}Z" fill="{cd}" opacity=".6"/>'
    s += f'<path d="M{f(x + 2)} {f(y + 2)}L{f(x + w * .1)} {f(y + 2)}L{f(x + w * .1)} {f(y + h)}L{f(x + 2)} {f(y + h)}Z" fill="{cl}" opacity=".7"/>'
    if cornice:
        s += f'<path d="M{f(x - 3)} {f(y)}L{f(x + w + 3)} {f(y)}L{f(x + w + 3)} {f(y - 5)}L{f(x - 3)} {f(y - 5)}Z" fill="{cl}" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
    if roof_rail:
        s += f'<path d="M{f(x)} {f(y - 5)}L{f(x)} {f(y - 13)}L{f(x + w)} {f(y - 13)}L{f(x + w)} {f(y - 5)}" fill="{c}" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
    fh = h / floors
    ww = min(w / (cols * 2.2), 16)
    for fl in range(floors):
        wy = y + fl * fh + fh * .22
        whh = fh * .58
        for ci in range(cols):
            wx = x + (ci + .5) * w / cols - ww / 2
            ground = fl == floors - 1
            if ground and door and ci == cols // 2:
                s += f'<path d="M{f(wx - 2)} {f(y + h)}L{f(wx - 2)} {f(wy)}Q{f(wx + ww / 2)} {f(wy - ww * .6)} {f(wx + ww + 2)} {f(wy)}L{f(wx + ww + 2)} {f(y + h)}Z" fill="#5B3A26" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
                continue
            if cierro and fl == 0:
                # cierro: mirador acristalado de madera
                s += (f'<path d="M{f(wx - 4)} {f(wy - 3)}L{f(wx + ww + 4)} {f(wy - 3)}L{f(wx + ww + 4)} {f(wy + whh + 3)}L{f(wx - 4)} {f(wy + whh + 3)}Z" fill="{SHUT}" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
                      f'<path d="M{f(wx - 1)} {f(wy)}L{f(wx + ww + 1)} {f(wy)}L{f(wx + ww + 1)} {f(wy + whh)}L{f(wx - 1)} {f(wy + whh)}Z" fill="{LIT if (fl, ci) in lit else "#9BBFC0"}" stroke="{INK}" stroke-width="{stroke * .5:.2f}"/>'
                      f'<path d="M{f(wx + ww / 2)} {f(wy)}L{f(wx + ww / 2)} {f(wy + whh)}M{f(wx - 1)} {f(wy + whh * .4)}L{f(wx + ww + 1)} {f(wy + whh * .4)}" stroke="{INK}" stroke-width="{stroke * .45:.2f}"/>')
                continue
            s += window(wx, wy, ww, whh, shutters=True, lit=(fl, ci) in lit, balcony=not ground, sw=stroke * .75)
    return s


def mirador(x, y, w, h, col, stroke=1.6):
    """Torre mirador sobre la azotea."""
    c, cd, cl = col
    return (f'<path d="M{f(x)} {f(y)}L{f(x + w)} {f(y)}L{f(x + w)} {f(y + h)}L{f(x)} {f(y + h)}Z" fill="{c}" stroke="{INK}" stroke-width="{stroke}"/>'
            f'<path d="M{f(x + w * .7)} {f(y)}L{f(x + w)} {f(y)}L{f(x + w)} {f(y + h)}L{f(x + w * .7)} {f(y + h)}Z" fill="{cd}" opacity=".7"/>'
            f'<path d="M{f(x - 2)} {f(y)}L{f(x + w + 2)} {f(y)}L{f(x + w + 2)} {f(y - 4)}L{f(x - 2)} {f(y - 4)}Z" fill="{cl}" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
            + window(x + w * .3, y + h * .25, w * .4, h * .45, shutters=False, arch=True, sw=stroke * .7))


def palm(x, base, h, lean=0, s=1.0, leaf="#2F6F63", trunk="#8A6243"):
    tx, ty = x + lean, base - h
    out = f'<path d="M{f(x)} {f(base)}Q{f(x + lean * .2)} {f(base - h * .5)} {f(tx)} {f(ty)}" fill="none" stroke="{trunk}" stroke-width="{f(7 * s)}"/>'
    out += "".join(f'<path d="M{f(x + lean * k / 10 - 3.5 * s)} {f(base - h * k / 10)}L{f(x + lean * k / 10 + 3.5 * s)} {f(base - h * k / 10 - 2 * s)}" stroke="#6E4C33" stroke-width="{f(1.2 * s)}"/>' for k in range(1, 10))
    for a, L in [(-160, 44), (-130, 50), (-100, 40), (-60, 44), (-25, 50), (5, 40), (-80, 30)]:
        r = math.radians(a)
        ex, ey = tx + math.cos(r) * L * s, ty + math.sin(r) * L * s + 18 * s
        cx, cy = tx + math.cos(r) * L * .5 * s, ty + math.sin(r) * L * .5 * s - 10 * s
        out += f'<path d="M{f(tx)} {f(ty)}Q{f(cx)} {f(cy)} {f(ex)} {f(ey)}" fill="none" stroke="{leaf}" stroke-width="{f(5 * s)}"/>'
        out += f'<path d="M{f(tx)} {f(ty)}Q{f(cx)} {f(cy)} {f(ex)} {f(ey)}" fill="none" stroke="#4E8F7C" stroke-width="{f(1.6 * s)}"/>'
    out += f'<circle cx="{f(tx)}" cy="{f(ty + 2)}" r="{f(4 * s)}" fill="#6E4C33"/>'
    return out


def lamp(x, base, h=150):
    top = base - h
    return (f'<ellipse cx="{f(x)}" cy="{f(base + 2)}" rx="12" ry="3" fill="#5B3524" opacity=".2"/>'
            f'<path d="M{f(x - 5)} {f(base)}L{f(x + 5)} {f(base)}L{f(x + 3)} {f(base - 12)}L{f(x - 3)} {f(base - 12)}Z" fill="#2E3A48"/>'
            f'<path d="M{f(x)} {f(base - 12)}L{f(x)} {f(top + 14)}" stroke="#2E3A48" stroke-width="3.2"/>'
            f'<path d="M{f(x - 7)} {f(top + 14)}L{f(x + 7)} {f(top + 14)}L{f(x + 9)} {f(top)}L{f(x - 9)} {f(top)}Z" fill="#FFE7A8" stroke="#2E3A48" stroke-width="2.2"/>'
            f'<path d="M{f(x - 10)} {f(top)}L{f(x + 10)} {f(top)}L{f(x)} {f(top - 9)}Z" fill="#2E3A48"/>')


def person(x, y, s=1.0, body="#2F6F73", hat=False, dress=False):
    out = f'<ellipse cx="{f(x)}" cy="{f(y + 1)}" rx="{f(6 * s)}" ry="{f(1.6 * s)}" fill="#5B3524" opacity=".2"/>'
    if dress:
        out += f'<path d="M{f(x - 5 * s)} {f(y)}L{f(x - 2.5 * s)} {f(y - 14 * s)}L{f(x + 2.5 * s)} {f(y - 14 * s)}L{f(x + 5 * s)} {f(y)}Z" fill="{body}"/>'
    else:
        out += f'<path d="M{f(x - 2 * s)} {f(y)}L{f(x - 2 * s)} {f(y - 7 * s)}M{f(x + 2 * s)} {f(y)}L{f(x + 2 * s)} {f(y - 7 * s)}" stroke="#3A3A48" stroke-width="{f(2.4 * s)}"/>'
        out += f'<path d="M{f(x - 3.5 * s)} {f(y - 6 * s)}L{f(x - 3 * s)} {f(y - 15 * s)}L{f(x + 3 * s)} {f(y - 15 * s)}L{f(x + 3.5 * s)} {f(y - 6 * s)}Z" fill="{body}"/>'
    out += f'<circle cx="{f(x)}" cy="{f(y - 18 * s)}" r="{f(3 * s)}" fill="#D9A07A"/>'
    if hat:
        out += f'<path d="M{f(x - 4.5 * s)} {f(y - 19.5 * s)}L{f(x + 4.5 * s)} {f(y - 19.5 * s)}M{f(x - 2.5 * s)} {f(y - 20 * s)}L{f(x - 2.5 * s)} {f(y - 23 * s)}L{f(x + 2.5 * s)} {f(y - 23 * s)}L{f(x + 2.5 * s)} {f(y - 20 * s)}" fill="#2B2B33" stroke="#2B2B33" stroke-width="{f(1.6 * s)}"/>'
    return out


def floor(p, y0, vx=195, color=FLOOR, line=FLOORL):
    s = f'<rect x="0" y="{y0}" width="{W}" height="{H - y0}" fill="{color}"/><rect x="0" y="{y0}" width="{W}" height="{H - y0}" fill="url(#{p}dots)"/>'
    for k, yy in enumerate([y0 + 16, y0 + 36, y0 + 64, y0 + 102, y0 + 150]):
        if yy < H:
            s += f'<rect x="0" y="{yy}" width="{W}" height="1.2" fill="{line}"/>'
    for i in range(-9, 10):
        s += f'<path d="M{vx} {y0}L{vx + i * 52} {H}" fill="none" stroke="{line}" stroke-width="1"/>'
    return s


def bench(x, y):
    return (f'<ellipse cx="{f(x + 30)}" cy="{f(y + 22)}" rx="36" ry="4" fill="#5B3524" opacity=".15"/>'
            f'<rect x="{f(x)}" y="{f(y)}" width="60" height="5" fill="#7A5236"/><rect x="{f(x)}" y="{f(y + 8)}" width="60" height="4" fill="#8A6243"/>'
            f'<path d="M{f(x + 6)} {f(y + 12)}L{f(x + 6)} {f(y + 22)}M{f(x + 54)} {f(y + 12)}L{f(x + 54)} {f(y + 22)}" stroke="#2E3A48" stroke-width="3"/>')


def tree(x, base, r, c="#4F7F5A", cd="#3D6647", trunk="#6E4C33"):
    return (f'<path d="M{f(x)} {f(base)}L{f(x)} {f(base - r * 1.2)}" stroke="{trunk}" stroke-width="{f(r * .22)}"/>'
            f'<circle cx="{f(x)}" cy="{f(base - r * 1.6)}" r="{f(r)}" fill="{c}"/>'
            f'<circle cx="{f(x - r * .7)}" cy="{f(base - r * 1.3)}" r="{f(r * .7)}" fill="{c}"/>'
            f'<circle cx="{f(x + r * .7)}" cy="{f(base - r * 1.35)}" r="{f(r * .75)}" fill="{cd}"/>'
            f'<circle cx="{f(x + r * .2)}" cy="{f(base - r * 2.1)}" r="{f(r * .6)}" fill="{c}"/>'
            f'<circle cx="{f(x - r * .3)}" cy="{f(base - r * 1.9)}" r="{f(r * .35)}" fill="#6F9E73" opacity=".7"/>')


def columns(x, y, w, h, n, col=STONE, stroke=1.4):
    c, cd, cl = col
    s = ""
    step = w / (n - 1) if n > 1 else 0
    for i in range(n):
        cx = x + i * step
        s += f'<path d="M{f(cx - 4)} {f(y)}L{f(cx + 4)} {f(y)}L{f(cx + 4)} {f(y + h)}L{f(cx - 4)} {f(y + h)}Z" fill="{cl}" stroke="{INK}" stroke-width="{stroke}"/>'
        s += f'<path d="M{f(cx + 1)} {f(y)}L{f(cx + 4)} {f(y)}L{f(cx + 4)} {f(y + h)}L{f(cx + 1)} {f(y + h)}Z" fill="{cd}" opacity=".7"/>'
        s += f'<path d="M{f(cx - 6)} {f(y)}L{f(cx + 6)} {f(y)}L{f(cx + 6)} {f(y - 3)}L{f(cx - 6)} {f(y - 3)}Z" fill="{c}" stroke="{INK}" stroke-width="{stroke * .8:.2f}"/>'
    return s


def far_city(y, seed, tone="#E6B790", tone2="#EBC4A0", towers=5):
    """Silueta lejana: azoteas y torres miradores, sin contorno."""
    rnd = random.Random(seed)
    s = ""
    x = -10
    while x < W + 10:
        w = rnd.randint(22, 44)
        h = rnd.randint(18, 46)
        s += f'<rect x="{x}" y="{y - h}" width="{w}" height="{h + 60}" fill="{rnd.choice([tone, tone2])}"/>'
        for k in range(rnd.randint(1, 3)):
            s += f'<rect x="{x + 5 + k * 10}" y="{y - h + 8}" width="4" height="6" fill="#D29E7A" opacity=".7"/>'
        if rnd.random() < towers / 12:
            tw = rnd.randint(8, 12)
            th = rnd.randint(14, 24)
            tx = x + rnd.randint(2, max(3, w - tw - 2))
            s += f'<rect x="{tx}" y="{y - h - th}" width="{tw}" height="{th}" fill="{tone2}"/><rect x="{tx - 1}" y="{y - h - th - 3}" width="{tw + 2}" height="3" fill="{tone}"/>'
        x += w
    return s


def fx(p, sun, ground_y=420, strength=.3):
    sx, sy = sun
    s = (f'<g id="fx"><defs><radialGradient id="{p}fxv" cx=".5" cy=".4" r=".7"><stop offset=".5" stop-color="#5B3524" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="#3A2418" stop-opacity=".3"/></radialGradient>'
         f'<linearGradient id="{p}fxr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4DC" stop-opacity="{strength}"/><stop offset="1" stop-color="#FFF4DC" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="{p}fxb" x1="0" y1="0" x2="0" y2="1"><stop offset=".7" stop-color="#1B2A3A" stop-opacity="0"/><stop offset="1" stop-color="#1B2A3A" stop-opacity=".25"/></linearGradient></defs>')
    for a in (50, 70, 92, 112, 135):
        r1, r2 = math.radians(a - 3.5), math.radians(a + 3.5)
        L = 700
        s += f'<path d="M{sx} {sy}L{f(sx + math.cos(r1) * L)} {f(sy + math.sin(r1) * L)}L{f(sx + math.cos(r2) * L)} {f(sy + math.sin(r2) * L)}Z" fill="url(#{p}fxr)"/>'
    s += f'<rect x="0" y="{ground_y - 8}" width="{W}" height="16" fill="#3A2418" opacity=".06"/>'
    s += f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}fxb)"/><rect x="0" y="0" width="{W}" height="{H}" fill="url(#{p}fxv)"/></g>'
    return s


def doc(p, title, layers):
    return (f'<svg stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">'
            + defs_common(p) + "".join(layers) + "</svg>\n")


# ---------------------------------------------------------------------------
# Escenas
# ---------------------------------------------------------------------------
def sanjuan():
    p = "sj"; sun = (300, 120)
    far = f'<g id="far">{far_city(250, 1)}<rect x="0" y="250" width="{W}" height="90" fill="#E3B48E"/></g>'
    # Ayuntamiento: cuerpo central con columnas y torrecilla del reloj
    x0, y0, w = 70, 150, 250
    ay = (f'<path d="M{x0} {y0}L{x0 + w} {y0}L{x0 + w} 350L{x0} 350Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M{x0 + w - 30} {y0}L{x0 + w} {y0}L{x0 + w} 350L{x0 + w - 30} 350Z" fill="{STONE[1]}" opacity=".6"/>'
          f'<path d="M{x0 - 4} {y0}L{x0 + w + 4} {y0}L{x0 + w + 4} {y0 - 7}L{x0 - 4} {y0 - 7}Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
          + "".join(f'<path d="M{x0 + 6 + i * 20} {y0 - 7}L{x0 + 6 + i * 20} {y0 - 17}L{x0 + 16 + i * 20} {y0 - 17}L{x0 + 16 + i * 20} {y0 - 7}" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.2"/>' for i in range(13))
          # cuerpo central adelantado
          + f'<path d="M150 {y0 - 20}L240 {y0 - 20}L240 350L150 350Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.8"/>'
          f'<path d="M144 {y0 - 20}L195 {y0 - 44}L246 {y0 - 20}Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
          f'<circle cx="195" cy="{y0 - 29}" r="6" fill="{GOLD}" stroke="{INK}" stroke-width="1.4"/>'
          + columns(158, y0 - 10, 74, 118, 4, STONE, 1.3)
          + f'<path d="M150 {y0 + 108}L240 {y0 + 108}L240 {y0 + 114}L150 {y0 + 114}Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.3"/>'
          + "".join(window(x, y0 + 12, 12, 30, shutters=False, balcony=True, lit=(x == 189)) for x in (166, 189, 212))
          + "".join(window(x, y0 + 62, 12, 30, shutters=False, balcony=True) for x in (166, 212))
          # torrecilla del reloj
          + f'<path d="M175 {y0 - 44}L215 {y0 - 44}L215 {y0 - 84}L175 {y0 - 84}Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
          f'<circle cx="195" cy="{y0 - 64}" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/><path d="M195 {y0 - 64}L195 {y0 - 71}M195 {y0 - 64}L200 {y0 - 62}" stroke="{INK}" stroke-width="1.4"/>'
          f'<path d="M171 {y0 - 84}L219 {y0 - 84}L219 {y0 - 90}L171 {y0 - 90}Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.4"/>'
          f'<path d="M180 {y0 - 90}Q195 {y0 - 120} 210 {y0 - 90}Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>'
          f'<path d="M195 {y0 - 112}L195 {y0 - 126}" stroke="{INK}" stroke-width="1.6"/>'
          # alas laterales
          + "".join(window(x, yy, 11, 26, balcony=True, lit=(x, yy) == (90, y0 + 16)) for x in (90, 118, 262, 290) for yy in (y0 + 16, y0 + 66))
          + "".join(f'<path d="M{x} 350L{x} 310Q{x + 9} 298 {x + 18} 310L{x + 18} 350Z" fill="{WIN}" stroke="{INK}" stroke-width="1.4"/>' for x in (86, 114, 258, 286))
          + f'<path d="M180 350L180 300Q195 284 210 300L210 350Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>')
    side = house(-20, 200, 80, 150, YELLOW, floors=3, cols=2, lit={(1, 1)}) + house(322, 190, 90, 160, PINK, floors=3, cols=2, cierro=True)
    mid = f'<g id="mid">{ay}{side}<rect x="-10" y="344" width="{W + 20}" height="80" fill="#DDBE98"/></g>'
    near = (f'<g id="near">{floor(p, 412)}'
            + palm(40, 440, 250, 14, 1.0) + palm(352, 446, 240, -12, 1.0)
            + palm(110, 420, 150, 6, .7) + palm(290, 420, 150, -6, .7)
            + person(150, 432, .9, CLAY, dress=True) + person(170, 438, 1, "#34495E", hat=True) + person(250, 430, .85, SEA)
            + lamp(78, 520, 150) + bench(250, 480) + "</g>")
    return doc(p, "Plaza de San Juan de Dios", [sky(p, sun, [(60, 80, 1), (330, 60, .7)], [(120, 110), (140, 100, .8)]), far, mid, near, fx(p, sun, 412)])


def catedral():
    p = "ca"; sun = (80, 110)
    far = f'<g id="far">{far_city(270, 7)}</g>'
    # cúpula dorada detrás de la fachada
    cx = 195
    dome = (f'<path d="M110 150L280 150L280 200L110 200Z" fill="{STONE[1]}"/>'
            f'<path d="M122 150Q122 60 {cx} 52Q268 60 268 150Z" fill="url(#{p}dome)" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{f(cx + k * 4)} 54Q{f(cx + k * 20)} 70 {f(cx + k * 23)} 150" fill="none" stroke="#B9822A" stroke-width="1.6"/>' for k in (-3, -2, -1, 1, 2, 3))
            + f'<path d="M{cx} 52L{cx} 150" stroke="#B9822A" stroke-width="1.6"/>'
            f'<path d="M140 90Q160 70 180 64" fill="none" stroke="#FFF1C2" stroke-width="3" opacity=".7"/>'
            f'<path d="M181 52L209 52L207 30L183 30Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M181 30Q{cx} 10 209 30Z" fill="url(#{p}dome)" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{cx} 16L{cx} 2M{cx - 5} 8L{cx + 5} 8" stroke="{INK}" stroke-width="1.6"/>')
    far = far.replace("</g>", dome + "</g>")

    def tower(x):
        return (f'<path d="M{x} 140L{x + 56} 140L{x + 56} 360L{x} 360Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
                f'<path d="M{x + 40} 142L{x + 56} 142L{x + 56} 360L{x + 40} 360Z" fill="{STONE[1]}" opacity=".6"/>'
                f'<path d="M{x - 4} 140L{x + 60} 140L{x + 60} 132L{x - 4} 132Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{x + 6} 132L{x + 50} 132L{x + 46} 92L{x + 10} 92Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
                + window(x + 21, 102, 14, 24, shutters=False, arch=True, sw=1.2)
                + f'<path d="M{x + 10} 92Q{x + 28} 60 {x + 46} 92Z" fill="url(#{p}dome)" stroke="{INK}" stroke-width="1.6"/>'
                f'<path d="M{x + 28} 68L{x + 28} 52M{x + 23} 58L{x + 33} 58" stroke="{INK}" stroke-width="1.6"/>'
                + window(x + 20, 170, 16, 30, shutters=False, arch=True, sw=1.3)
                + window(x + 20, 240, 16, 30, shutters=False, arch=True, sw=1.3, lit=True)
                + f'<path d="M{x} 212L{x + 56} 212M{x} 290L{x + 56} 290" stroke="{STONE[1]}" stroke-width="2"/>')
    facade = (tower(66) + tower(268)
              + f'<path d="M122 180L268 180L268 360L122 360Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M116 180L195 150L274 180Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M150 180Q195 120 240 180" fill="none" stroke="{INK}" stroke-width="1.6"/>'
              + columns(134, 196, 122, 160, 6, STONE, 1.3)
              + f'<path d="M172 360L172 280Q195 252 218 280L218 360Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M195 262L195 360" stroke="#3A2418" stroke-width="1.4"/>'
              f'<circle cx="195" cy="222" r="15" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/><circle cx="195" cy="222" r="8" fill="{LIT}" stroke="{INK}" stroke-width="1.3"/>')
    side = house(-30, 250, 90, 110, WHITE, floors=2, cols=2) + house(330, 240, 80, 120, YELLOW, floors=2, cols=2, lit={(0, 0)})
    mid = f'<g id="mid">{facade}{side}<rect x="-10" y="354" width="{W + 20}" height="70" fill="#DDBE98"/>' \
          f'<path d="M100 360L290 360L300 380L90 380Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.4"/><path d="M90 380L300 380L310 396L80 396Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/></g>'
    near = (f'<g id="near">{floor(p, 410)}'
            + person(120, 424, .8, "#6E2C5E", dress=True) + person(275, 428, .9, "#34495E") + person(300, 422, .75, CLAY, hat=True)
            + lamp(30, 530, 170) + lamp(362, 530, 170) + palm(6, 470, 220, 18, .9) + "</g>")
    return doc(p, "Catedral de Cádiz", [sky(p, sun, [(300, 70, .9), (40, 190, .6)], [(260, 40), (280, 30, .8)]), far, mid, near, fx(p, sun, 410)])


def mercado():
    p = "me"; sun = (310, 100)
    far = f'<g id="far">{far_city(230, 3, towers=8)}<rect x="0" y="230" width="{W}" height="100" fill="#E3B48E"/></g>'
    # soportales dóricos del mercado
    col = YELLOW
    arc = (f'<path d="M-10 170L400 170L400 330L-10 330Z" fill="{col[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M-14 170L404 170L404 160L-14 160Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M-14 160L404 160L404 150L-14 150Z" fill="{col[2]}" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M150 150L195 124L240 150Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x} 330L{x} 206Q{x + 20} 186 {x + 40} 206L{x + 40} 330Z" fill="#5E4232" stroke="{INK}" stroke-width="1.4"/>' for x in range(0, 390, 56))
           + columns(-4, 186, 392, 144, 8, WHITE, 1.3)
           + f'<path d="M-10 330L400 330L400 338L-10 338Z" fill="{WHITE[1]}" stroke="{INK}" stroke-width="1.3"/>'
           # rótulo sin texto y farolillos
           + f'<rect x="160" y="132" width="70" height="0" fill="none"/>'
           + "".join(f'<circle cx="{x + 20}" cy="214" r="4" fill="{LIT}" stroke="{INK}" stroke-width="1"/>' for x in range(0, 390, 56)))
    mid = f'<g id="mid">{arc}<rect x="-10" y="336" width="{W + 20}" height="90" fill="#DCC3A0"/></g>'
    # puesto de pescado en primer plano
    stall = (f'<path d="M-10 420L400 420L400 470L-10 470Z" fill="#7A5236"/>'
             f'<path d="M-10 404L400 404L400 424L-10 424Z" fill="#EAF3F2" stroke="{INK}" stroke-width="1.6"/>'
             + "".join(f'<circle cx="{x}" cy="{408 + (x * 7) % 9}" r="{2 + (x % 3)}" fill="#FFFFFF" opacity=".9"/>' for x in range(0, 390, 11))
             # atún
             + f'<path d="M20 402Q60 378 118 386Q134 390 142 398L156 388Q152 400 156 412L142 404Q132 412 116 414Q60 418 20 402Z" fill="#2B3F5C" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M22 404Q62 418 118 410Q132 408 140 402Q100 404 60 402Z" fill="#B9C8D0"/>'
             f'<circle cx="34" cy="398" r="3" fill="#FFF" stroke="{INK}" stroke-width="1.2"/>'
             + "".join(f'<path d="M{x} {392 + (x - 120) * .2:.0f}l2 -3l2 3Z" fill="{GOLD}"/>' for x in (120, 126, 132))
             # pescaítos
             + "".join(f'<g transform="rotate({r} {x} 404)"><path d="M{x - 14} 404Q{x} 396 {x + 12} 404Q{x} 412 {x - 14} 404Z" fill="#C4D3DA" stroke="{INK}" stroke-width="1.2"/><path d="M{x + 12} 404L{x + 18} 399L{x + 18} 409Z" fill="#C4D3DA" stroke="{INK}" stroke-width="1.2"/></g>'
                       for x, r in [(206, -8), (236, 6), (266, -4), (296, 10), (326, -6), (356, 4), (220, 170), (310, 175)])
             # etiquetas de precio (sin texto)
             + "".join(f'<path d="M{x} 382L{x + 22} 382L{x + 22} 396L{x} 396Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/><path d="M{x + 11} 396L{x + 11} 406" stroke="{INK}" stroke-width="1.4"/>' for x in (86, 250, 340))
             + f'<path d="M-10 470L400 470" stroke="{INK}" stroke-width="2"/>')
    near = (f'<g id="near">{floor(p, 420, color="#E3CBAA")}'
            + person(60, 440, .9, CLAY, dress=True) + person(90, 446, 1, SEA) + person(330, 442, .9, "#34495E", hat=True)
            + f'<g transform="translate(0 70)">{stall}</g>' + "</g>")
    return doc(p, "Mercado Central de Cádiz", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, mid, near, fx(p, sun, 420, .25)])


def tavira():
    p = "ta"; sun = (290, 90)
    far = f'<g id="far">{far_city(300, 11, towers=10)}</g>'
    # la torre al fondo de la calle, con mástil y banderas de señales
    tx, tw = 160, 70
    tower = (f'<path d="M{tx} 110L{tx + tw} 110L{tx + tw} 380L{tx} 380Z" fill="{YELLOW[0]}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M{tx + tw - 18} 112L{tx + tw} 112L{tx + tw} 380L{tx + tw - 18} 380Z" fill="{YELLOW[1]}" opacity=".7"/>'
             f'<path d="M{tx} 110L{tx + 8} 110L{tx + 8} 380L{tx} 380ZM{tx + tw - 8} 110L{tx + tw} 110L{tx + tw} 380L{tx + tw - 8} 380Z" fill="{CLAY}" opacity=".55"/>'
             f'<path d="M{tx - 5} 110L{tx + tw + 5} 110L{tx + tw + 5} 100L{tx - 5} 100Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M{tx} 100L{tx} 88L{tx + tw} 88L{tx + tw} 100" fill="{YELLOW[2]}" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(f'<path d="M{tx + 6 + i * 12} 88L{tx + 6 + i * 12} 80L{tx + 10 + i * 12} 80L{tx + 10 + i * 12} 88" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1"/>' for i in range(6))
             + window(tx + 24, 130, 22, 36, shutters=False, arch=True, sw=1.3)
             + window(tx + 26, 200, 18, 30, shutters=False, balcony=True, sw=1.2, lit=True)
             + window(tx + 26, 260, 18, 30, shutters=False, balcony=True, sw=1.2)
             # mástil y banderas
             + f'<path d="M{tx + 35} 80L{tx + 35} 20M{tx + 20} 34L{tx + 50} 34" stroke="{INK}" stroke-width="2"/>'
             f'<path d="M{tx + 35} 24L{tx + 58} 28L{tx + 35} 33Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M{tx + 50} 36L{tx + 64} 38L{tx + 64} 46L{tx + 50} 44Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
             f'<path d="M{tx + 20} 36L{tx + 8} 38L{tx + 8} 46L{tx + 20} 44Z" fill="{SEA}" stroke="{INK}" stroke-width="1.2"/>')
    far = far.replace("</g>", tower + "</g>")
    # calle estrecha: fachadas en perspectiva a los lados

    def side(left):
        s = ""
        cols = [WHITE, PINK, YELLOW, MINT]
        for k in range(4):
            x0 = -30 + k * 36 if left else W + 30 - k * 36
            x1 = x0 + (46 if left else -46)
            top0, top1 = 60 + k * 36, 80 + k * 38
            bot = 460 - k * 26
            c = cols[k]
            xa, xb = (x0, x1) if left else (x1, x0)
            ta, tb = (top0, top1) if left else (top1, top0)
            s += f'<path d="M{xa} {ta}L{xb} {tb}L{xb} {bot - 10}L{xa} {bot}Z" fill="{c[0]}" stroke="{INK}" stroke-width="1.6"/>'
            for fl in range(3):
                y = ta + 40 + fl * 90
                s += f'<path d="M{xa + 12} {y}L{xb - 12} {y + 4}L{xb - 12} {y + 44}L{xa + 12} {y + 40}Z" fill="{SHUT if fl != 1 else WIN}" stroke="{INK}" stroke-width="1.2"/>'
                s += f'<path d="M{xa + 6} {y + 44}L{xb - 6} {y + 48}" stroke="{INK}" stroke-width="2.2"/>'
                s += f'<path d="M{xa + 6} {y + 30}L{xb - 6} {y + 34}" stroke="{INK}" stroke-width="1"/>'
                s += "".join(f'<path d="M{xa + 6 + i * (xb - xa - 12) / 4:.1f} {y + 30 + i:.1f}L{xa + 6 + i * (xb - xa - 12) / 4:.1f} {y + 44 + i:.1f}" stroke="{INK}" stroke-width=".8"/>' for i in range(5))
                if fl == 0 and k % 2 == 0:
                    s += f'<circle cx="{(xa + xb) / 2:.0f}" cy="{y + 50}" r="5" fill="{CLAY}"/><circle cx="{(xa + xb) / 2 + 6:.0f}" cy="{y + 52}" r="4" fill="#E0766A"/>'
        return s
    mid = f'<g id="mid">{side(True)}{side(False)}<rect x="-10" y="378" width="{W + 20}" height="50" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E0C7A4")}'
            + person(170, 434, .8, SEA) + person(215, 430, .75, "#6E2C5E", dress=True)
            + lamp(40, 540, 170) + "</g>")
    return doc(p, "Torre Tavira", [sky(p, sun, [(90, 60, .8)], [(240, 40), (260, 30, .8), (120, 90, .7)]), far, mid, near, fx(p, sun, 420)])


def sanfelipe():
    p = "sf"; sun = (320, 100)
    far = f'<g id="far">{far_city(250, 5)}<rect x="0" y="250" width="{W}" height="100" fill="#E3B48E"/></g>'
    # fachada del oratorio: sobria, portada de piedra, espadaña y lápidas conmemorativas
    x0, w = 100, 190
    church = (f'<path d="M{x0} 130L{x0 + w} 130L{x0 + w} 380L{x0} 380Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.8"/>'
              f'<path d="M{x0 + w - 26} 132L{x0 + w} 132L{x0 + w} 380L{x0 + w - 26} 380Z" fill="{WHITE[1]}" opacity=".7"/>'
              f'<path d="M{x0 - 5} 130L{x0 + w + 5} 130L{x0 + w + 5} 120L{x0 - 5} 120Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
              # espadaña con campana
              f'<path d="M170 120L220 120L220 70L170 70Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M166 70L195 44L224 70Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M184 116L184 88Q195 76 206 88L206 116Z" fill="{WIN}" stroke="{INK}" stroke-width="1.3"/>'
              f'<path d="M188 104Q195 90 202 104L204 110L186 110Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>'
              f'<path d="M195 44L195 30M190 36L200 36" stroke="{INK}" stroke-width="1.6"/>'
              # portada de piedra
              f'<path d="M150 380L150 230L240 230L240 380Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
              + columns(160, 246, 70, 134, 2, STONE, 1.2)
              + f'<path d="M144 230L195 204L246 230Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M176 380L176 300Q195 280 214 300L214 380Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M195 290L195 380" stroke="#3A2418" stroke-width="1.3"/>'
              + window(185, 150, 20, 34, shutters=False, arch=True, sw=1.3, lit=True)
              # lápidas de mármol en la fachada
              + "".join(f'<path d="M{x} {y}L{x + ww} {y}L{x + ww} {y + hh}L{x} {y + hh}Z" fill="#E9E6E0" stroke="{INK}" stroke-width="1.2"/>'
                        + "".join(f'<path d="M{x + 4} {y + 6 + i * 5}L{x + ww - 4} {y + 6 + i * 5}" stroke="#9AA3AA" stroke-width="1"/>' for i in range(int(hh // 6)))
                        for x, y, ww, hh in [(108, 170, 30, 34), (108, 220, 30, 28), (252, 170, 30, 34), (252, 222, 30, 26), (112, 272, 24, 20), (254, 272, 24, 20)]))
    side = house(-20, 170, 110, 210, PINK, floors=3, cols=2, lit={(0, 0)}) + house(300, 160, 110, 220, MINT, floors=3, cols=2, cierro=True)
    mid = f'<g id="mid">{side}{church}<rect x="-10" y="374" width="{W + 20}" height="54" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E0C7A4")}'
            + person(120, 438, .9, "#34495E", hat=True) + person(292, 434, .85, CLAY, dress=True)
            + lamp(350, 540, 160) + tree(34, 520, 34) + "</g>")
    return doc(p, "Oratorio de San Felipe Neri", [sky(p, sun, [(70, 70, .9)], [(250, 60), (270, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def espana():
    p = "es"; sun = (90, 100)
    far = (f'<g id="far">{far_city(270, 13)}'
           + house(250, 190, 150, 110, WHITE, floors=2, cols=3, stroke=0.01) + "</g>").replace(f'stroke="{INK}" stroke-width="0.01"', 'stroke="none"')
    # monumento a las Cortes: hemiciclo de columnas y pilar central con estatua
    cx = 195
    mon = (f'<path d="M40 330Q{cx} 250 350 330L350 380L40 380Z" fill="{STONE[1]}" stroke="{INK}" stroke-width="1.6"/>'
           + "".join(f'<path d="M{f(cx + math.cos(math.radians(a)) * 150 - 5)} {f(338 - math.sin(math.radians(a)) * 58)}L{f(cx + math.cos(math.radians(a)) * 150 + 5)} {f(338 - math.sin(math.radians(a)) * 58)}L{f(cx + math.cos(math.radians(a)) * 150 + 5)} 378L{f(cx + math.cos(math.radians(a)) * 150 - 5)} 378Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.2"/>'
                     for a in range(10, 171, 16))
           + f'<path d="M40 328Q{cx} 244 350 328L350 320Q{cx} 236 40 320Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
           # pilar central
           + f'<path d="M168 380L168 140L222 140L222 380Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M206 142L222 142L222 380L206 380Z" fill="{STONE[1]}" opacity=".7"/>'
           f'<path d="M160 140L230 140L230 128L160 128Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M176 128L214 128L210 60L180 60Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M184 116L206 116M184 100L206 100" stroke="{STONE[1]}" stroke-width="1.6"/>'
           # alegoría de bronce arriba
           f'<path d="M186 60L186 36Q195 28 204 36L204 60Z" fill="#4E6B5E" stroke="{INK}" stroke-width="1.6"/>'
           f'<circle cx="195" cy="28" r="6" fill="#4E6B5E" stroke="{INK}" stroke-width="1.4"/>'
           f'<path d="M204 40L216 22" stroke="#4E6B5E" stroke-width="3.4"/><path d="M216 22L218 12" stroke="{INK}" stroke-width="1.6"/>'
           # relieves y grupos escultóricos laterales en bronce
           f'<path d="M176 180L214 180L214 230L176 230Z" fill="#E9DCC0" stroke="{INK}" stroke-width="1.3"/>'
           + "".join(f'<ellipse cx="{f(195 + math.cos(math.radians(a)) * 13)}" cy="{f(205 + math.sin(math.radians(a)) * 13)}" rx="4" ry="2" transform="rotate({a + 90} {f(195 + math.cos(math.radians(a)) * 13)} {f(205 + math.sin(math.radians(a)) * 13)})" fill="#9A8A66"/>' for a in range(-240, 61, 30))
           + f'<path d="M188 222L202 222" stroke="#9A8A66" stroke-width="1.6"/>'
           + "".join(f'<path d="M{x - 14} 380L{x - 14} 340L{x + 14} 340L{x + 14} 380Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>'
                     f'<path d="M{x - 10} 340L{x - 8} 316Q{x} 300 {x + 8} 316L{x + 10} 340Z" fill="#4E6B5E" stroke="{INK}" stroke-width="1.4"/>'
                     f'<circle cx="{x}" cy="306" r="5" fill="#4E6B5E" stroke="{INK}" stroke-width="1.2"/>' for x in (130, 260))
           + f'<path d="M150 380L240 380L250 392L140 392Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.4"/>')
    mid = f'<g id="mid">{mon}<rect x="-10" y="390" width="{W + 20}" height="38" fill="#DCC3A0"/></g>'
    near = (f'<g id="near">{floor(p, 420)}'
            + palm(26, 470, 250, 16, 1.0) + palm(368, 470, 250, -16, 1.0)
            + person(110, 440, .9, SEA) + person(290, 436, .85, "#6E2C5E", dress=True) + person(310, 442, 1, "#34495E", hat=True)
            + bench(140, 490) + "</g>")
    return doc(p, "Plaza de España", [sky(p, sun, [(300, 80, .9), (340, 170, .6)], [(250, 50), (270, 40, .8)]), far, mid, near, fx(p, sun, 420)])


def mina():
    p = "mi"; sun = (300, 110)
    far = f'<g id="far">{far_city(240, 21)}<rect x="0" y="240" width="{W}" height="100" fill="#E3B48E"/></g>'
    # Museo de Cádiz: fachada neoclásica
    x0, w = 60, 270
    mus = (f'<path d="M{x0} 150L{x0 + w} 150L{x0 + w} 370L{x0} 370Z" fill="{STONE[0]}" stroke="{INK}" stroke-width="1.8"/>'
           f'<path d="M{x0 + w - 30} 152L{x0 + w} 152L{x0 + w} 370L{x0 + w - 30} 370Z" fill="{STONE[1]}" opacity=".6"/>'
           f'<path d="M{x0 - 5} 150L{x0 + w + 5} 150L{x0 + w + 5} 140L{x0 - 5} 140Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M150 140L195 116L240 140Z" fill="{STONE[2]}" stroke="{INK}" stroke-width="1.6"/>'
           + columns(156, 166, 78, 200, 4, STONE, 1.3)
           + "".join(window(x, y, 13, 30, balcony=True, lit=(x, y) == (84, 176), sw=1.2) for x in (84, 116, 262, 294) for y in (176, 252))
           + f'<path d="M180 370L180 310Q195 296 210 310L210 370Z" fill="#5B3A26" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M{x0} 236L{x0 + w} 236" stroke="{STONE[1]}" stroke-width="2"/>')
    trees = tree(40, 400, 50, "#4B7C58", "#3A6446") + tree(350, 404, 54, "#4B7C58", "#3A6446") + tree(250, 396, 30, "#5A8B63", "#46714F")
    mid = f'<g id="mid">{mus}{trees}<rect x="-10" y="368" width="{W + 20}" height="60" fill="#D8C09A"/>' \
          + "".join(f'<path d="M{x} 400L{x} 380" stroke="#2E3A48" stroke-width="2"/>' for x in range(0, 390, 12)) \
          + f'<path d="M-10 382L400 382M-10 398L400 398" stroke="#2E3A48" stroke-width="2"/></g>'
    near = (f'<g id="near">{floor(p, 420, color="#E4CDA8")}'
            + palm(330, 470, 260, -8, 1.0) + tree(20, 560, 40, "#3F6F4C", "#2F5A3C")
            + person(150, 440, .9, CLAY, dress=True) + person(170, 446, 1, "#34495E") + bench(220, 480) + lamp(100, 540, 160) + "</g>")
    return doc(p, "Plaza de Mina", [sky(p, sun, [(80, 70, .8)], [(200, 60), (220, 50, .8)]), far, mid, near, fx(p, sun, 420)])


def caleta():
    p = "cl"; sun = (230, 140)
    far = (f'<g id="far"><rect x="-10" y="280" width="{W + 20}" height="60" fill="#E7BE98"/>'
           # castillo de Santa Catalina (izquierda) y de San Sebastián con su faro (derecha)
           f'<path d="M-10 290L80 290L80 260L-10 260Z" fill="#E1B28C"/>'
           + "".join(f'<rect x="{x}" y="252" width="7" height="9" fill="#E1B28C"/>' for x in range(-6, 80, 12))
           + f'<path d="M300 292L400 292L400 268L300 268Z" fill="#E1B28C"/>'
           f'<path d="M338 268L352 268L350 196L340 196Z" fill="#EDCBA8"/><path d="M336 196L354 196L354 188L336 188Z" fill="#D9A782"/>'
           f'<path d="M339 188L351 188L349 176L341 176Z" fill="#FFF3DC"/><path d="M338 176L352 176L345 168Z" fill="#D9A782"/>'
           f'<path d="M180 294L300 294L300 290L180 290Z" fill="#E1B28C"/></g>')
    sea = (f'<g id="sea"><rect x="-10" y="286" width="{W + 20}" height="130" fill="url(#{p}sea)"/>'
           + "".join(f'<path d="M{x} {y}L{x + ln} {y}" stroke="#E6F2EF" stroke-width="1.6" opacity=".7"/>' for x, y, ln in [(20, 310, 30), (120, 330, 24), (260, 316, 34), (60, 360, 22), (300, 356, 28), (180, 386, 26)])
           + f'<path d="M205 300L215 300M200 312L220 312M198 326L222 326" stroke="#FFF6E0" stroke-width="2" opacity=".8"/>'
           # balneario sobre pilotes
           f'<path d="M34 344L34 368M62 344L62 368M90 344L90 368M118 344L118 368M146 344L146 368" stroke="{INK}" stroke-width="2"/>'
           f'<path d="M24 316L156 316L156 346L24 346Z" fill="{WHITE[0]}" stroke="{INK}" stroke-width="1.6"/>'
           f'<path d="M20 346L160 346L160 350L20 350Z" fill="{WHITE[1]}" stroke="{INK}" stroke-width="1.2"/>'
           + "".join(f'<path d="M{x} 316Q{x + 11} 292 {x + 22} 316Z" fill="{WHITE[2]}" stroke="{INK}" stroke-width="1.4"/><path d="M{x + 11} 296L{x + 11} 288" stroke="{INK}" stroke-width="1.2"/>' for x in (28, 79, 130 - 2))
           + "".join(f'<path d="M{x} 340L{x} 324Q{x + 5} 318 {x + 10} 324L{x + 10} 340Z" fill="{SEA}" stroke="{INK}" stroke-width="1"/>' for x in range(32, 150, 16))
           # barquitas fondeadas
           + "".join(f'<path d="M{x - 14} {y}L{x + 14} {y}L{x + 10} {y + 6}L{x - 10} {y + 6}Z" fill="{c}" stroke="{INK}" stroke-width="1.2"/><path d="M{x - 12} {y + 2}L{x + 12} {y + 2}" stroke="{PAPER}" stroke-width="1.2"/>'
                     for x, y, c in [(250, 350, CLAY), (300, 372, SEA), (210, 396, "#E9C46A")])
           + f'<path d="M-10 410Q60 402 130 410T270 410T400 408L400 420L-10 420Z" fill="#F4F0E6" opacity=".9"/></g>')
    near = (f'<g id="near"><rect x="-10" y="412" width="{W + 20}" height="150" fill="#EBD3AC"/><rect x="-10" y="412" width="{W + 20}" height="150" fill="url(#{p}dots)"/>'
            f'<path d="M-10 414Q60 406 130 414T270 414T400 412" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".8"/>'
            # barcas varadas en la arena
            + "".join(f'<g transform="rotate({r} {x} {y})"><path d="M{x - 40} {y - 14}L{x + 40} {y - 14}Q{x + 34} {y + 6} {x + 20} {y + 8}L{x - 24} {y + 8}Q{x - 38} {y} {x - 40} {y - 14}Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
                      f'<path d="M{x - 38} {y - 8}L{x + 38} {y - 8}" stroke="{c}" stroke-width="4"/><path d="M{x - 40} {y - 14}L{x + 40} {y - 14}" stroke="{c}" stroke-width="2.2"/></g>'
                      f'<ellipse cx="{x}" cy="{y + 12}" rx="42" ry="4" fill="#5B3524" opacity=".15"/>'
                      for x, y, c, r in [(70, 470, SEA, -4), (330, 486, CLAY, 5)])
            + person(190, 440, .9, CLAY, dress=True) + person(214, 446, 1, SEA)
            + f'<path d="M150 520l6 -4l6 4" fill="none" stroke="#C9A57E" stroke-width="1.4"/><circle cx="260" cy="530" r="3" fill="#F2C14E" opacity=".7"/>'
            + palm(372, 440, 230, -10, .95) + "</g>")
    return doc(p, "La Caleta", [sky(p, sun, [(70, 90, .9), (320, 70, .7)], [(150, 80), (170, 70, .8), (300, 130, .7)]), far, sea, near, fx(p, sun, 412, .25)])


SCENES = {"sanjuan": sanjuan, "catedral": catedral, "mercado": mercado, "tavira": tavira,
          "sanfelipe": sanfelipe, "espana": espana, "mina": mina, "caleta": caleta}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for key, build in SCENES.items():
        with open(os.path.join(OUT, f"fondo_cadiz_{key}.svg"), "w") as fh:
            fh.write(build())
    print("fondos de Cádiz generados:", ", ".join(SCENES))
