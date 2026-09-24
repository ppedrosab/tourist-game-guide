#!/usr/bin/env python3
"""
Convierte assets/backgrounds/svg/fondo_{escena}.svg en las capas de parallax:
assets/backgrounds/layers/bg_{escena}_{n}_{capa}@2x|@3x.webp (+ x_flat, la composición).
La capa del cielo y la composición van opacas; el resto con transparencia.

Uso: python3 scripts/art/render_layers.py [prefijo]    (p. ej. "cadiz_": solo esas escenas)
Necesita playwright (Chromium) y Pillow.
"""
import glob, json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SVG = os.path.join(ROOT, "assets", "backgrounds", "svg")
OUT = os.path.join(ROOT, "assets", "backgrounds", "layers")
prefix = sys.argv[1] if len(sys.argv) > 1 else ""
env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"], text=True).strip())

for src in sorted(glob.glob(os.path.join(SVG, f"fondo_{prefix}*.svg"))):
    scene = os.path.basename(src)[len("fondo_"):-len(".svg")]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["node", os.path.join(ROOT, "scripts", "art", "render-svg-groups.js"), src, tmp, "2", "3"], check=True, env=env)
        groups = json.load(open(os.path.join(tmp, "groups.json")))
        for old in glob.glob(os.path.join(OUT, f"bg_{scene}_*")):
            os.remove(old)
        for scale in (2, 3):
            names = [(f"{n}_{g}", g) for n, g in enumerate(groups)] + [("x_flat", "flat")]
            for name, g in names:
                im = Image.open(os.path.join(tmp, f"{g}@{scale}x.png"))
                im = im.convert("RGB") if g in ("sky", "flat") else im.convert("RGBA")
                im.save(os.path.join(OUT, f"bg_{scene}_{name}@{scale}x.webp"), "WEBP", quality=86, method=6)
    print(f"{scene}: {', '.join(groups)}")
