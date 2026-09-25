#!/usr/bin/env python3
"""
Revisión de coordenadas (npm run check:stops): busca cada parada física en OpenStreetMap (Nominatim,
«{título}, {ciudad}») y compara con la coordenada del pack. Escribe docs/COORDENADAS.md con las
paradas que se alejan más de 80 m de lo que encuentra OSM, para revisarlas antes de salir a la calle.

No cambia los packs: un título genérico («Cierre», «La Catedral») puede dar un resultado equivocado,
así que cada aviso se revisa a mano. Respuestas en caché (scripts/.cache/geocode.json); 1 petición/s.
"""
import glob, json, math, os, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "scripts", ".cache", "geocode.json")
OUT = os.path.join(ROOT, "docs", "COORDENADAS.md")
LIMIT_M = 80


def meters(a, b):
    k = math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot((a[1] - b[1]) * k, a[0] - b[0]) * 111_320


def geocode(cache, query, viewbox):
    if query not in cache:
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
            {"format": "json", "limit": 1, "q": query, "viewbox": viewbox, "bounded": 1}
        )
        req = urllib.request.Request(url, headers={"User-Agent": "tourist-game-guide check_stops"})
        try:
            hits = json.load(urllib.request.urlopen(req, timeout=30))
        except Exception:
            hits = []
        cache[query] = [[float(h["lat"]), float(h["lon"]), h["display_name"]] for h in hits]
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
        time.sleep(1.1)
    return cache[query]


def main():
    try:
        cache = json.load(open(CACHE))
    except (OSError, ValueError):
        cache = {}
    rows, seen, checked = [], set(), 0
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "*.pack.json"))):
        pack = json.load(open(f))
        city = pack["name"]["es"]
        (s, w), (n, e) = [(b["lat"], b["lng"]) for b in pack["bounds"]]
        viewbox = f"{w - 0.01},{n + 0.01},{e + 0.01},{s - 0.01}"
        for r in pack["routes"]:
            for node in r["nodes"]:
                if "location" not in node:
                    continue
                title = node["title"]["es"]
                here = (node["location"]["lat"], node["location"]["lng"])
                key = (city, title, here)
                if key in seen:
                    continue
                seen.add(key)
                checked += 1
                hits = geocode(cache, f"{title}, {city}", viewbox)
                if not hits:
                    rows.append((city, title, r["id"], here, None, None, "OSM no lo encuentra con ese nombre"))
                    continue
                lat, lng, name = hits[0]
                d = meters(here, (lat, lng))
                if d > LIMIT_M:
                    rows.append((city, title, r["id"], here, (lat, lng), round(d), name.split(",")[0]))
    lines = [
        "# Revisión de coordenadas de las paradas",
        "",
        "Generado con `npm run check:stops` (OpenStreetMap/Nominatim). Paradas cuya coordenada se aleja",
        f"más de {LIMIT_M} m de lo que OSM encuentra con «título, ciudad». No todo aviso es un error: OSM",
        "puede devolver otro sitio con el mismo nombre, o la parada estar a propósito en un punto de la",
        "plaza. Revisar cada una y, al moverla, regenerar los trazados (`npm run gen:paths`).",
        "",
        f"Paradas revisadas: {checked}. Con aviso: {len(rows)}.",
        "",
        "| Ciudad | Parada | Ruta | Pack (lat, lng) | OSM (lat, lng) | Distancia | Qué encontró OSM |",
        "|---|---|---|---|---|---|---|",
    ]
    for city, title, rid, here, osm, d, name in sorted(rows, key=lambda x: (x[0], -(x[5] or 0))):
        o = f"{osm[0]:.5f}, {osm[1]:.5f}" if osm else "—"
        lines.append(f"| {city} | {title} | `{rid}` | {here[0]:.5f}, {here[1]:.5f} | {o} | {f'{d} m' if d else '—'} | {name} |")
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"{checked} paradas, {len(rows)} avisos → {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
