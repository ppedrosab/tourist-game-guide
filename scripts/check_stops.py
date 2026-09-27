#!/usr/bin/env python3
"""
Revisión de coordenadas (npm run check:stops): busca cada parada física en OpenStreetMap (Nominatim,
«{título}, {ciudad}») y compara con la coordenada del pack. Escribe docs/COORDENADAS.md con las
paradas que se alejan más de 80 m de lo que encuentra OSM, para revisarlas antes de salir a la calle.

Segunda opinión independiente de OSM: Wikidata (una consulta SPARQL por ciudad con todo lo que tiene
coordenadas dentro de sus límites; el nombre se empareja aquí). Si OSM y Wikidata coinciden entre sí y
el pack queda lejos, la parada sale como «probable error» con la coordenada propuesta.

Con la variable de entorno GOOGLE_MAPS_API_KEY (clave de Google Maps Platform con «Places API (New)»
activada) busca en Google Maps en vez de en OSM: Text Search limitado al rectángulo de la ciudad.

No cambia los packs: un título genérico («Cierre», «La Catedral») puede dar un resultado equivocado,
así que cada aviso se revisa a mano. Respuestas en caché (scripts/.cache/geocode*.json); 1 petición/s.
"""
import difflib, glob, json, math, os, re, time, unicodedata, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
SOURCE = "Google Maps" if GOOGLE_KEY else "OSM"
CACHE = os.path.join(ROOT, "scripts", ".cache", "geocode_google.json" if GOOGLE_KEY else "geocode.json")
OUT = os.path.join(ROOT, "docs", "COORDENADAS.md")
LIMIT_M = 80


def meters(a, b):
    k = math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot((a[1] - b[1]) * k, a[0] - b[0]) * 111_320


UA = "tourist-game-guide/1.0 (https://github.com/ppedrosab/tourist-game-guide)"
STOP = {"de", "del", "la", "las", "el", "los", "y", "e", "a", "en"}


def words(text):
    text = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode()
    return [w for w in re.findall(r"[a-z0-9]+", text) if w not in STOP]


def wikidata_places(city_id, box):
    """Todo lo que Wikidata sitúa dentro del rectángulo de la ciudad: [(etiqueta, lat, lng)]."""
    path = os.path.join(ROOT, "scripts", ".cache", f"wikidata_{city_id}.json")
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        pass
    (s, w), (n, e) = box
    q = f"""SELECT ?label ?coord WHERE {{
      SERVICE wikibase:box {{ ?item wdt:P625 ?coord .
        bd:serviceParam wikibase:cornerSouthWest "Point({w - 0.01} {s - 0.01})"^^geo:wktLiteral .
        bd:serviceParam wikibase:cornerNorthEast "Point({e + 0.01} {n + 0.01})"^^geo:wktLiteral . }}
      ?item rdfs:label ?label . FILTER(lang(?label) = "es") }}"""
    req = urllib.request.Request("https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q), headers={"User-Agent": UA})
    rows = json.load(urllib.request.urlopen(req, timeout=120))["results"]["bindings"]
    out = []
    for r in rows:
        m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", r["coord"]["value"])
        if m:
            out.append([r["label"]["value"], float(m.group(2)), float(m.group(1))])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), ensure_ascii=False)
    time.sleep(2)
    return out


def wikidata_match(places, title, near=None):
    """Mejor lugar de Wikidata para el título de la parada (todas sus palabras en la etiqueta, o casi igual)."""
    variants = {title, re.sub(r"\s*\(.*?\)", "", title)}
    best, best_score = [], 0.0
    for label, lat, lng in places:
        lw = words(label)
        for v in variants:
            tw = words(v)
            if not tw or not lw:
                continue
            ratio = difflib.SequenceMatcher(None, " ".join(tw), " ".join(lw)).ratio()
            contained = all(t in lw for t in tw) and len(lw) <= len(tw) + 3
            score = max(ratio if ratio >= 0.85 else 0, 0.9 - 0.02 * (len(lw) - len(tw)) if contained else 0)
            if score > best_score + 1e-9:
                best, best_score = [(label, lat, lng)], score
            elif score and abs(score - best_score) < 1e-9:
                best.append((label, lat, lng))
    if not best:
        return None
    if near and len(best) > 1:
        best.sort(key=lambda b: meters(near, (b[1], b[2])))
    return best[0]


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
    move, check, ok, seen = [], [], 0, set()
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "*.pack.json"))):
        pack = json.load(open(f))
        city = pack["name"]["es"]
        box = [(b["lat"], b["lng"]) for b in pack["bounds"]]
        (s, w), (n, e) = box
        viewbox = f"{w - 0.01},{n + 0.01},{e + 0.01},{s - 0.01}"
        places = wikidata_places(pack["city"] if isinstance(pack.get("city"), str) else os.path.basename(os.path.dirname(f)), box)
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
                query = f"{title}, {city}"
                hits = geocode_google(cache, query, box) if GOOGLE_KEY else geocode(cache, query, viewbox)
                geo = (hits[0][0], hits[0][1], hits[0][2].split(",")[0]) if hits else None
                wd = wikidata_match(places, title, near=geo[:2] if geo else None)
                srcs = [(SOURCE, geo), ("Wikidata", (wd[1], wd[2], wd[0]) if wd else None)]
                found = [(name, g) for name, g in srcs if g]
                if any(meters(here, g[:2]) <= LIMIT_M for _, g in found):
                    ok += 1
                    continue
                row = (city, title, r["id"], here, srcs)
                if len(found) == 2 and meters(found[0][1][:2], found[1][1][:2]) <= LIMIT_M:
                    move.append(row)
                else:
                    check.append(row)

    def cell(here, g):
        return f"{g[0]:.5f}, {g[1]:.5f} ({round(meters(here, g[:2]))} m) · {g[2]}" if g else "—"

    def table(rows, proposal):
        head = f"| Ciudad | Parada | Ruta | Pack (lat, lng) | {SOURCE} | Wikidata |" + (" Propuesta |" if proposal else "")
        out = [head, "|---" * (head.count("|") - 1) + "|"]
        for city, title, rid, here, srcs in sorted(rows, key=lambda x: (x[0], x[1])):
            line = f"| {city} | {title} | `{rid}` | {here[0]:.5f}, {here[1]:.5f} | {cell(here, srcs[0][1])} | {cell(here, srcs[1][1])} |"
            if proposal:
                a, b = srcs[0][1], srcs[1][1]
                line += f" {(a[0] + b[0]) / 2:.5f}, {(a[1] + b[1]) / 2:.5f} |"
            out.append(line)
        return out

    total = ok + len(move) + len(check)
    lines = [
        "# Revisión de coordenadas de las paradas",
        "",
        f"Generado con `npm run check:stops`: cada parada se busca por «título, ciudad» en {SOURCE} y en",
        "Wikidata (fuentes independientes). Entre paréntesis, la distancia a la coordenada del pack.",
        "",
        f"- **Bien** ({ok} de {total}): al menos una fuente la sitúa a menos de {LIMIT_M} m.",
        f"- **Probable error** ({len(move)}): las dos fuentes coinciden entre sí y el pack queda lejos.",
        f"- **Revisar a mano** ({len(check)}): no se encuentra o las fuentes no coinciden. Muchas son paradas",
        "  con nombre genérico o puntos elegidos a propósito (una esquina, un mirador): no son errores seguros.",
        "",
        "Al mover una parada, regenerar los trazados (`npm run gen:paths`).",
        "",
        "## Probable error",
        "",
        *table(move, True),
        "",
        "## Revisar a mano",
        "",
        *table(check, False),
    ]
    open(OUT, "w").write("\n".join(lines) + "\n")
    print(f"{total} paradas: {ok} bien, {len(move)} probable error, {len(check)} revisar → {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
