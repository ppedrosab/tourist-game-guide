#!/usr/bin/env python3
"""
Revisión de coordenadas (npm run check:stops): busca cada parada física en OpenStreetMap (Nominatim,
«{título}, {ciudad}») y compara con la coordenada del pack. Escribe docs/COORDENADAS.md con las
paradas que se alejan más de 80 m de lo que encuentra OSM, para revisarlas antes de salir a la calle.

Con la variable de entorno GOOGLE_MAPS_API_KEY (clave de Google Maps Platform con «Places API (New)»
activada) busca en Google Maps en vez de en OSM: Text Search limitado al rectángulo de la ciudad.

No cambia los packs: un título genérico («Cierre», «La Catedral») puede dar un resultado equivocado,
así que cada aviso se revisa a mano. Respuestas en caché (scripts/.cache/geocode*.json); 1 petición/s.
"""
import glob, json, math, os, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
SOURCE = "Google Maps" if GOOGLE_KEY else "OSM"
CACHE = os.path.join(ROOT, "scripts", ".cache", "geocode_google.json" if GOOGLE_KEY else "geocode.json")
OUT = os.path.join(ROOT, "docs", "COORDENADAS.md")
LIMIT_M = 80


def meters(a, b):
    k = math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot((a[1] - b[1]) * k, a[0] - b[0]) * 111_320


def geocode_google(cache, query, box):
    """Places API (New) · Text Search, con el resultado obligado a caer en el rectángulo de la ciudad."""
    if query not in cache:
        (s, w), (n, e) = box
        body = json.dumps({"textQuery": query, "languageCode": "es", "pageSize": 1,
                           "locationRestriction": {"rectangle": {"low": {"latitude": s - 0.01, "longitude": w - 0.01},
                                                                 "high": {"latitude": n + 0.01, "longitude": e + 0.01}}}}).encode()
        req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=body, headers={
            "Content-Type": "application/json", "X-Goog-Api-Key": GOOGLE_KEY,
            "X-Goog-FieldMask": "places.displayName,places.location,places.formattedAddress"})
        try:
            places = json.load(urllib.request.urlopen(req, timeout=30)).get("places", [])
        except urllib.error.HTTPError as err:
            raise SystemExit(f"Google Maps rechaza la petición ({err.code}): {err.read().decode()[:300]}")
        except Exception:
            places = []
        cache[query] = [[p["location"]["latitude"], p["location"]["longitude"],
                         f'{p["displayName"]["text"]}, {p.get("formattedAddress", "")}'] for p in places]
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cache, open(CACHE, "w"), ensure_ascii=False)
        time.sleep(0.2)
    return cache[query]


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
        box = [(b["lat"], b["lng"]) for b in pack["bounds"]]
        (s, w), (n, e) = box
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
                query = f"{title}, {city}"
                hits = geocode_google(cache, query, box) if GOOGLE_KEY else geocode(cache, query, viewbox)
                if not hits:
                    rows.append((city, title, r["id"], here, None, None, f"{SOURCE} no lo encuentra con ese nombre"))
                    continue
                lat, lng, name = hits[0]
                d = meters(here, (lat, lng))
                if d > LIMIT_M:
                    rows.append((city, title, r["id"], here, (lat, lng), round(d), name.split(",")[0]))
    lines = [
        "# Revisión de coordenadas de las paradas",
        "",
        f"Generado con `npm run check:stops` ({'Google Maps, Places API' if GOOGLE_KEY else 'OpenStreetMap/Nominatim'}). Paradas cuya coordenada se aleja",
        f"más de {LIMIT_M} m de lo que {SOURCE} encuentra con «título, ciudad». No todo aviso es un error: {SOURCE}",
        "puede devolver otro sitio con el mismo nombre, o la parada estar a propósito en un punto de la",
        "plaza. Revisar cada una y, al moverla, regenerar los trazados (`npm run gen:paths`).",
        "",
        f"Paradas revisadas: {checked}. Con aviso: {len(rows)}.",
        "",
        f"| Ciudad | Parada | Ruta | Pack (lat, lng) | {SOURCE} (lat, lng) | Distancia | Qué encontró {SOURCE} |",
        "|---|---|---|---|---|---|---|",
    ]
    for city, title, rid, here, osm, d, name in sorted(rows, key=lambda x: (x[0], -(x[5] or 0))):
        o = f"{osm[0]:.5f}, {osm[1]:.5f}" if osm else "—"
        lines.append(f"| {city} | {title} | `{rid}` | {here[0]:.5f}, {here[1]:.5f} | {o} | {f'{d} m' if d else '—'} | {name} |")
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"{checked} paradas, {len(rows)} avisos → {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
