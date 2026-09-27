#!/usr/bin/env python3
"""
Datos prácticos de cada ruta (npm run gen:practical): lo que el jugador quiere saber antes de salir.

Por parada física (`practical.stops[nodo]`), de OpenStreetMap (Overpass):
  - water:   metros hasta la fuente de agua potable más cercana (si hay alguna a ≤ 200 m).
  - toilets: metros hasta los aseos públicos más cercanos (≤ 250 m; sin los de clientes o privados).
  - shade:   true si hay al menos 5 árboles a ≤ 30 m (estimación: suele haber sombra).
  - hours / hoursOf: horario (sintaxis `opening_hours` de OSM) del monumento, museo, mercado o
    templo más cercano (≤ 40 m) y su nombre, para que se pueda revisar. Solo se guardan los horarios
    que entiende `src/engine/hours.ts` (días, meses, franjas, «off» y 24/7), ya normalizados.

Por tramo (`practical.legs["desde->hasta"]`, las claves de `route.paths`):
  - up / down: metros de subida y bajada (modelo de elevación EU-DEM de 25 m, vía OpenTopoData).
  - grade:     pendiente máxima en %, medida en tramos de ≥ 100 m.
  - steps:     escaleras (highway=steps de OSM) que recorre el camino del enrutador (pasa por dos
               nodos seguidos suyos; se mira el trazado completo que guarda gen_paths en su caché).

Las respuestas se guardan en scripts/.cache/ para no repetir peticiones. El bloque se inserta en el
pack por texto, como `paths`, sin reformatear el resto del archivo. Antes hay que tener los trazados
(`npm run gen:paths`).

Uso: python3 scripts/gen_practical.py [ruta ...]   (sin argumentos, todas)
"""
import glob, json, math, os, re, sys, time, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_paths import load_cache as load_paths_cache, meters  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(ROOT, "scripts", ".cache")
UA = "tourist-game-guide/1.0 (https://github.com/ppedrosab/tourist-game-guide)"
OVERPASS = [
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
ELEVATION = "https://api.opentopodata.org/v1/eudem25m?locations={locations}"

WATER_MAX, TOILETS_MAX, TREES_R, TREES_MIN, HOURS_R = 200, 250, 30, 5, 40
SAMPLE_M = 30  # muestreo de la elevación a lo largo del trazado
GRADE_WINDOW_M = 100

# Qué se considera "el sitio" de una parada para darle horario.
PLACE_TAGS = {
    "tourism": {"museum", "attraction", "gallery", "viewpoint", "zoo", "aquarium"},
    "amenity": {"place_of_worship", "marketplace", "theatre", "library", "arts_centre"},
    "leisure": {"park", "garden"},
    "building": {"cathedral", "church", "basilica", "chapel", "castle"},
}

# Sintaxis de horario que entiende src/engine/hours.ts (mantener a la par).
_M = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
_D = r"(?:Mo|Tu|We|Th|Fr|Sa|Su|PH)"
_T = r"\d\d:\d\d-\d\d:\d\d"
RULE = re.compile(
    rf"^(?:{_M}(?:-{_M})?(?:,{_M}(?:-{_M})?)*\s+)?(?:{_D}(?:-{_D})?(?:,{_D}(?:-{_D})?)*\s+)?(?:{_T}(?:,{_T})*|off|closed)$"
)


def normalize_hours(spec):
    """Horario en la forma que entiende la app (sin espacios sueltos, "Apr-Oct:" → "Apr-Oct"), o None."""
    spec = spec.strip()
    if spec == "24/7":
        return spec
    rules = []
    for r in spec.split(";"):
        r = re.sub(r"\s*([,-])\s*", r"\1", r.strip())
        r = re.sub(rf"^({_M}(?:-{_M})?(?:,{_M}(?:-{_M})?)*):\s*", r"\1 ", r)
        r = re.sub(r"\s+", " ", r)
        if r:
            rules.append(r)
    if not rules or not all(RULE.match(r) for r in rules):
        return None
    return "; ".join(rules)


def cached(name):
    path = os.path.join(CACHE_DIR, name)
    try:
        return path, json.load(open(path))
    except (OSError, ValueError):
        return path, {}


def overpass(query):
    body = urllib.parse.urlencode({"data": query}).encode()
    for attempt in range(6):
        url = OVERPASS[attempt % len(OVERPASS)]
        try:
            req = urllib.request.Request(url, data=body, headers={"User-Agent": UA})
            return json.load(urllib.request.urlopen(req, timeout=180))
        except Exception:
            time.sleep(2 ** attempt)
    raise RuntimeError("sin respuesta de Overpass")


def city_osm(pack):
    """Fuentes, aseos, árboles, escaleras y sitios con horario de la zona de la ciudad (una consulta)."""
    path, cache = cached(f"practical_{pack['id']}.json")
    if cache:
        return cache
    (a, b) = pack["bounds"]
    s, n = min(a["lat"], b["lat"]) - 0.01, max(a["lat"], b["lat"]) + 0.01
    w, e = min(a["lng"], b["lng"]) - 0.01, max(a["lng"], b["lng"]) + 0.01
    bb = f"({s},{w},{n},{e})"
    q = f"""[out:json][timeout:170];
(
  node[amenity=drinking_water]{bb};
  nwr[amenity=toilets]{bb};
  node[natural=tree]{bb};
  way[highway=steps]{bb};
  nwr[opening_hours][name][tourism~"^(museum|attraction|gallery|viewpoint|zoo|aquarium)$"]{bb};
  nwr[opening_hours][name][amenity~"^(place_of_worship|marketplace|theatre|library|arts_centre)$"]{bb};
  nwr[opening_hours][name][leisure~"^(park|garden)$"]{bb};
  nwr[opening_hours][name][building~"^(cathedral|church|basilica|chapel|castle)$"]{bb};
  nwr[opening_hours][name][historic]{bb};
);
out tags center geom;"""
    data = overpass(q)
    os.makedirs(CACHE_DIR, exist_ok=True)
    json.dump(data, open(path, "w"))
    time.sleep(2)
    return data


def point(el):
    if "lat" in el:
        return [el["lon"], el["lat"]]
    c = el.get("center")
    return [c["lon"], c["lat"]] if c else None


def classify(data):
    water, toilets, trees, steps, places = [], [], [], [], []
    for el in data["elements"]:
        t = el.get("tags", {})
        p = point(el)
        if t.get("amenity") == "drinking_water" and t.get("drinking_water") != "no" and p:
            water.append(p)
        elif t.get("amenity") == "toilets" and t.get("access") not in ("private", "customers", "no") and p:
            toilets.append(p)
        elif t.get("natural") == "tree" and p:
            trees.append(p)
        elif t.get("highway") == "steps" and el.get("geometry"):
            steps.append([[g["lon"], g["lat"]] for g in el["geometry"]])
        if "opening_hours" in t and "name" in t and p and ("historic" in t or any(t.get(k) in v for k, v in PLACE_TAGS.items())):
            places.append((p, t["name"], t["opening_hours"]))
    return water, toilets, trees, steps, places


def nearest(p, pts, limit):
    best = min((meters(p, q) for q in pts), default=None)
    return round(best / 10) * 10 if best is not None and best <= limit else None


def words(s):
    return {w for w in re.findall(r"\w{4,}", s.lower())}


def stop_info(node, pack, osm):
    water, toilets, trees, _, places = osm
    p = [node["location"]["lng"], node["location"]["lat"]]
    info = {}
    w = nearest(p, water, WATER_MAX)
    if w is not None:
        info["water"] = max(10, w)
    t = nearest(p, toilets, TOILETS_MAX)
    if t is not None:
        info["toilets"] = max(10, t)
    if sum(1 for q in trees if meters(p, q) <= TREES_R) >= TREES_MIN:
        info["shade"] = True
    title = words(node["title"]["es"])
    near = [(meters(p, q), name, normalize_hours(h)) for q, name, h in places if meters(p, q) <= HOURS_R]
    near = [x for x in near if x[2]]
    # el que comparte una palabra con el título de la parada; si no, el más cercano
    near.sort(key=lambda x: (not (words(x[1]) & title), x[0]))
    if near:
        info["hours"] = near[0][2]
        info["hoursOf"] = near[0][1]
    return info


def densify(path, step):
    out = [path[0]]
    for a, b in zip(path, path[1:]):
        n = max(1, int(meters(a, b) // step))
        out += [[a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n] for i in range(1, n + 1)]
    return out


def elevations(pts, cache):
    keys = [f"{p[1]:.4f},{p[0]:.4f}" for p in pts]
    missing = sorted({k for k in keys if k not in cache})
    for i in range(0, len(missing), 100):
        chunk = missing[i : i + 100]
        url = ELEVATION.format(locations="|".join(chunk))
        for attempt in range(6):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                data = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except Exception:
                time.sleep(2 ** (attempt + 1))
        else:
            raise RuntimeError("sin respuesta del servicio de elevación")
        cache.update(zip(chunk, (r["elevation"] for r in data["results"])))
        time.sleep(1.1)  # el servicio público admite una petición por segundo
    return [cache[k] for k in keys]


def full_trace(nodes, key, paths_cache):
    """Trazado sin simplificar del enrutador (la caché de gen_paths) para el tramo "desde->hasta"."""
    a, b = (nodes[i]["location"] for i in key.split("->"))
    k = f"{a['lng']:.5f},{a['lat']:.5f};{b['lng']:.5f},{b['lat']:.5f}"
    hit = paths_cache.get(k)
    return hit["coords"] if hit else None


def leg_info(path, trace, osm, elev_cache):
    steps = osm[3]
    pts = densify(path, SAMPLE_M)
    h = elevations(pts, elev_cache)
    # puntos fuera del modelo (en el agua, por ejemplo): el valor válido más cercano
    valid = [i for i, x in enumerate(h) if x is not None]
    h = [x if x is not None else (h[min(valid, key=lambda j: abs(j - i))] if valid else 0.0) for i, x in enumerate(h)]
    # subida y bajada con histéresis de 2 m (el modelo tiene ruido)
    up = down = 0.0
    ref = h[0]
    for x in h[1:]:
        if x - ref >= 2:
            up, ref = up + x - ref, x
        elif ref - x >= 2:
            down, ref = down + ref - x, x
    dist = [0.0]
    for a, b in zip(pts, pts[1:]):
        dist.append(dist[-1] + meters(a, b))
    grade, j = 0.0, 0
    for i in range(len(pts)):
        while j < len(pts) and dist[j] - dist[i] < GRADE_WINDOW_M:
            j += 1
        if j < len(pts):
            grade = max(grade, abs(h[j] - h[i]) / (dist[j] - dist[i]) * 100)
    if dist[-1] < GRADE_WINDOW_M and dist[-1] > 30:
        grade = abs(h[-1] - h[0]) / dist[-1] * 100
    # Una escalera cuenta si el camino pasa por dos nodos seguidos suyos (la recorre, no la roza).
    on = 0
    if trace:
        onpath = {(round(x, 5), round(y, 5)) for x, y in trace}
        for way in steps:
            hits = [(round(x, 5), round(y, 5)) in onpath for x, y in way]
            if any(h1 and h2 for h1, h2 in zip(hits, hits[1:])):
                on += 1
    info = {"up": round(up), "down": round(down), "grade": round(grade)}
    if on:
        info["steps"] = on
    return info


def practical_block(practical, indent):
    pad = " " * indent
    rows = [f'{pad}"practical": {{', f'{pad}  "stops": {{']
    rows.append(",\n".join(f'{pad}    {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in practical["stops"].items()))
    rows += [f"{pad}  }},", f'{pad}  "legs": {{']
    rows.append(",\n".join(f'{pad}    {json.dumps(k)}: {json.dumps(v)}' for k, v in practical["legs"].items()))
    rows += [f"{pad}  }}", f"{pad}}},"]
    return "\n".join(r for r in rows if r) + "\n"


def patch_text(text, route_id, practical):
    start = text.index(f'\n    {{\n      "id": "{route_id}"', text.index('"routes": ['))
    nxt = re.search(r'\n    \{\n      "id": "', text[start + 1 :])
    end = start + 1 + nxt.start() if nxt else len(text)
    body = text[start:end]
    body = re.sub(r'      "practical": \{\n(?:.*\n)*?      \},\n', "", body)
    i = body.index('      "rewards": [')
    body = body[:i] + practical_block(practical, 6) + body[i:]
    return text[:start] + body + text[end:]


def main(only):
    elev_path, elev_cache = cached("elevation.json")
    paths_cache = load_paths_cache()
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "*.pack.json"))):
        text = open(f).read()
        pack = json.loads(text)
        routes = [r for r in pack["routes"] if not only or r["id"] in only]
        if not routes:
            continue
        osm = classify(city_osm(pack))
        for r in routes:
            stops = {n["id"]: stop_info(n, pack, osm) for n in r["nodes"] if "location" in n}
            nodes = {n["id"]: n for n in r["nodes"]}
            legs = {
                k: leg_info(p, full_trace(nodes, k, paths_cache), osm, elev_cache) for k, p in (r.get("paths") or {}).items()
            }
            json.dump(elev_cache, open(elev_path, "w"))
            text = patch_text(text, r["id"], {"stops": stops, "legs": legs})
            up = sum(l["up"] for l in legs.values())
            print(
                f"{r['id']}: agua en {sum('water' in s for s in stops.values())}/{len(stops)} paradas, "
                f"horario en {sum('hours' in s for s in stops.values())}, subida {up} m, "
                f"pendiente máx. {max((l['grade'] for l in legs.values()), default=0)} %, "
                f"escaleras {sum(l.get('steps', 0) for l in legs.values())}"
            )
        json.loads(text)
        open(f, "w").write(text)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
