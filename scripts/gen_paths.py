#!/usr/bin/env python3
"""
Trazado a pie de cada tramo del mapa (npm run gen:paths).

Para cada ruta de cada pack calcula los tramos entre paradas físicas (los mismos que
src/map/geometry.ts: de una parada a las siguientes, atravesando nodos narrativos), pide el
camino a pie al enrutador de OpenStreetMap (routing.openstreetmap.de, perfil «foot») y lo guarda
simplificado en `route.paths["desde->hasta"]` como [lng, lat], un tramo por línea. De paso corrige `distanceM` y
`walkMin` de las decisiones que los llevan, con la distancia real andando (4,5 km/h).

Las respuestas se guardan en scripts/.cache/paths.json para no repetir peticiones. Los packs se
editan por texto (el de Málaga tiene formato compacto hecho a mano), sin reformatear el resto.

Uso: python3 scripts/gen_paths.py [ruta ...]   (sin argumentos, todas)
"""
import glob, json, math, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "scripts", ".cache", "paths.json")
ROUTER = "https://routing.openstreetmap.de/routed-foot/route/v1/driving/{a};{b}?overview=full&geometries=geojson"
WALK_M_PER_MIN = 75  # 4,5 km/h
TOLERANCE_M = 4  # simplificación: el trazado no se aparta más de esto del original


def meters(a, b):
    """Distancia aproximada en metros entre dos [lng, lat] (equirectangular, vale a escala de ciudad)."""
    k = math.cos(math.radians((a[1] + b[1]) / 2))
    return math.hypot((a[0] - b[0]) * k, a[1] - b[1]) * 111_320


def simplify(pts, tol=TOLERANCE_M):
    """Douglas-Peucker en metros."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    k = math.cos(math.radians(a[1]))
    ax, ay, bx, by = a[0] * k, a[1], b[0] * k, b[1]
    dx, dy = bx - ax, by - ay
    worst, idx = 0, 0
    for i, p in enumerate(pts[1:-1], 1):
        px, py = p[0] * k, p[1]
        if dx == dy == 0:
            d = math.hypot(px - ax, py - ay)
        else:
            t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
            d = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
        d *= 111_320
        if d > worst:
            worst, idx = d, i
    if worst <= tol:
        return [a, b]
    return simplify(pts[: idx + 1], tol)[:-1] + simplify(pts[idx:], tol)


def load_cache():
    try:
        return json.load(open(CACHE))
    except (OSError, ValueError):
        return {}


def walk(cache, a, b):
    """Camino a pie entre dos {lat, lng}: (distancia en m, [[lng, lat], ...])."""
    key = f"{a['lng']:.5f},{a['lat']:.5f};{b['lng']:.5f},{b['lat']:.5f}"
    if key not in cache:
        url = ROUTER.format(a=f"{a['lng']},{a['lat']}", b=f"{b['lng']},{b['lat']}")
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "tourist-game-guide gen_paths"})
                data = json.load(urllib.request.urlopen(req, timeout=30))
                break
            except Exception:
                time.sleep(2 ** attempt)
        else:
            raise RuntimeError(f"sin respuesta del enrutador para {key}")
        route = data["routes"][0]
        cache[key] = {"distance": route["distance"], "coords": route["geometry"]["coordinates"]}
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cache, open(CACHE, "w"))
        time.sleep(1)  # uso respetuoso del servicio público
    hit = cache[key]
    return hit["distance"], hit["coords"]


def graph(route):
    nodes = {n["id"]: n for n in route["nodes"]}
    outs = lambda n: [c["targetNodeId"] for c in n.get("choices", [])] + ([n["nextNodeId"]] if n.get("nextNodeId") else [])

    def next_physical(start_ids, seen):
        found, queue = [], list(start_ids)
        while queue:
            i = queue.pop(0)
            if i in seen:
                continue
            seen.add(i)
            n = nodes[i]
            if "location" in n:
                found.append(n)
            else:
                queue += outs(n)
        return found

    physical = [n for n in route["nodes"] if "location" in n]
    segments = [(f, t) for f in physical for t in next_physical(outs(f), {f["id"]})]
    # Parada física desde la que se llega a cada nodo narrativo (para las decisiones).
    origin = {}
    for f in physical:
        queue, seen = outs(f), set()
        while queue:
            i = queue.pop(0)
            if i in seen or "location" in nodes[i]:
                continue
            seen.add(i)
            origin.setdefault(i, f)
            queue += outs(nodes[i])
    return nodes, segments, origin, next_physical


def compute(route, cache):
    """Trazados de la ruta y distancias reales de sus decisiones: (paths, {(nodo, destino): (m, min)})."""
    nodes, segments, origin, next_physical = graph(route)
    paths, dist = {}, {}
    for f, t in segments:
        d, coords = walk(cache, f["location"], t["location"])
        pts = simplify([[round(x, 5), round(y, 5)] for x, y in coords])
        paths[f"{f['id']}->{t['id']}"] = pts
        dist[(f["id"], t["id"])] = d
    choices = {}
    for n in route["nodes"]:
        src = n if "location" in n else origin.get(n["id"])
        for c in n.get("choices", []):
            if "distanceM" not in c or not src:
                continue
            first = next_physical([c["targetNodeId"]], set())
            if not first or (src["id"], first[0]["id"]) not in dist:
                continue
            d = dist[(src["id"], first[0]["id"])]
            choices[(n["id"], c["targetNodeId"])] = (max(10, round(d / 10) * 10), max(1, round(d / WALK_M_PER_MIN)))
    return paths, choices


def paths_block(paths, indent):
    pad = " " * indent
    rows = [f'{pad}  {json.dumps(k)}: {json.dumps(v, separators=(",", ":"))}' for k, v in paths.items()]
    return f'{pad}"paths": {{\n' + ",\n".join(rows) + f"\n{pad}}},\n"


def patch_text(text, route_id, paths, choices):
    """Pack de formato compacto: sustituye o inserta "paths" y retoca las decisiones de una ruta."""
    # (buscando tras "routes": un personaje puede llamarse igual que una ruta, p. ej. la Tarasca)
    start = text.index(f'\n    {{\n      "id": "{route_id}"', text.index('"routes": ['))
    # fin de la ruta: siguiente ruta o fin del array de rutas
    nxt = re.search(r'\n    \{\n      "id": "', text[start + 1 :])
    end = start + 1 + nxt.start() if nxt else len(text)
    body = text[start:end]
    body = re.sub(r'      "paths": \{\n(?:.*\n)*?      \},\n', "", body)
    i = body.index('      "rewards": [')
    body = body[:i] + paths_block(paths, 6) + body[i:]
    for (_, target), (m, mins) in choices.items():
        for mt in re.finditer(rf'"targetNodeId": "{re.escape(target)}"', body):
            lab = body.rfind('"label"', 0, mt.start())
            win = body[lab:mt.end()]
            new = re.sub(r'"distanceM": \d+', f'"distanceM": {m}', win)
            new = re.sub(r'"walkMin": \d+', f'"walkMin": {mins}', new)
            body = body[:lab] + new + body[mt.end():]
    return text[:start] + body + text[end:]


def main(only):
    cache = load_cache()
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "*.pack.json"))):
        text = open(f).read()
        for r in json.loads(text)["routes"]:
            if only and r["id"] not in only:
                continue
            paths, choices = compute(r, cache)
            text = patch_text(text, r["id"], paths, choices)
            print(f"{r['id']}: {len(paths)} tramos, {len(choices)} decisiones")
        json.loads(text)
        open(f, "w").write(text)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
