#!/usr/bin/env python3
"""
Versión nocturna de un fondo ya hecho: fondo_{escena}.svg → fondo_{escena}_noche.svg.
Cambia el cielo por uno de noche (luna y estrellas), quita los rayos de sol del fx, oscurece y
enfría el resto de capas con un filtro de color y enciende las ventanas y farolas.

Uso: python3 scripts/art/night_variants.py escena1 escena2 …   (luego render_layers.py y gen:assets)
"""
import os, re, sys, zlib
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
from cadiz_scenes import OUT, LIT, WIN
from cadiz_ssanta_scenes import night_sky, night_fx

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
# Oscurece y lleva a azul; deja pasar algo de rojo para que la piedra no quede gris muerta
NIGHT_MATRIX = ".28 .07 .03 0 0  .05 .30 .07 0 .01  .07 .12 .42 0 .06  0 0 0 1 0"
LIGHTS = ("#FFE7A8", LIT)   # farolas y ventanas encendidas: se pintan por encima, sin filtro


def frag(svg_text):
    """Parsea un trozo de SVG (uno o varios elementos) y devuelve sus elementos."""
    root = ET.fromstring(f'<svg xmlns="{NS}">{svg_text}</svg>')
    return list(root)


def night_variant(key):
    src = os.path.join(OUT, f"fondo_{key}.svg")
    tree = ET.parse(src)
    root = tree.getroot()
    grad = next(e for e in root.iter(f"{{{NS}}}linearGradient") if e.get("id", "").endswith("sky"))
    p = grad.get("id")[:-3] + "n"
    seed = zlib.crc32(key.encode()) % 97
    moon = (300 - seed, 70 + seed % 30) if seed % 2 else (80 + seed, 70 + seed % 30)
    defs = root.find(f"{{{NS}}}defs")
    defs.extend(frag(f'<filter id="{p}nightf" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="{NIGHT_MATRIX}"/></filter>'))
    for i, g in enumerate(list(root)):
        gid = g.get("id")
        if gid == "sky":
            root.remove(g); root.insert(i, frag(night_sky(p, moon, seed))[0])
        elif gid == "fx":
            root.remove(g); root.insert(i, frag(night_fx(p))[0])
        elif gid in ("far", "sea", "mid", "near"):
            lights = []
            n_win = 0
            for el in g.iter():
                if el.get("fill") in LIGHTS:
                    lights.append(ET.tostring(el, encoding="unicode"))
                elif el.get("fill") == WIN and el.tag.endswith("path"):
                    n_win += 1
                    if (n_win * 7 + seed) % 3 == 0:   # una de cada tres ventanas, encendida
                        lights.append(ET.tostring(el, encoding="unicode"))
            inner = ET.Element(f"{{{NS}}}g", {"filter": f"url(#{p}nightf)"})
            for child in list(g):
                g.remove(child); inner.append(child)
            g.append(inner)
            # las luces van encima, sin oscurecer, con un halo suave
            for k, l in enumerate(lights[:40]):
                for e in frag(l):
                    e.set("fill", "#F2C66E"); e.set("opacity", ".9"); g.append(e)
    dst = os.path.join(OUT, f"fondo_{key}_noche.svg")
    xml = ET.tostring(root, encoding="unicode")
    xml = re.sub(r'aria-label="([^"]*)"', lambda m: f'aria-label="{m.group(1)} (de noche)"', xml, count=1)
    open(dst, "w").write(xml + "\n")
    return dst


if __name__ == "__main__":
    for key in sys.argv[1:]:
        night_variant(key)
    print("fondos de noche generados:", ", ".join(sys.argv[1:]))
