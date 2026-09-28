"""
Saca a trozos los textos de los packs que aún no tienen fr/de/it, para traducirlos.
Deja en scripts/.cache/i18n/src/{pack}_NN.txt bloques «@id ruta / ES / EN»; la traducción se escribe
en out/{pack}_NN.json como {id: [fr, de, it]} y la aplican check.py y apply.py.
Uso: python3 scripts/i18n/extract.py
"""
import json, glob, hashlib, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.join(ROOT, "scripts", ".cache", "i18n")
os.makedirs(WORK, exist_ok=True)
os.chdir(WORK)
CHUNK = 12000
def tid(es, en):
    return hashlib.sha1((es + "\x00" + en).encode()).hexdigest()[:8]
os.makedirs("src", exist_ok=True)
index = {}
for f in sorted(glob.glob(f"{ROOT}/content/*/*.pack.json")):
    pack = json.load(open(f))
    seen, items = set(), []
    def walk(x, path):
        if isinstance(x, dict):
            if isinstance(x.get("es"), str) and not path.endswith(".audio"):
                if all(isinstance(x.get(l), str) for l in ("fr", "de", "it")):
                    return
                es, en = x["es"], x.get("en", "")
                k = tid(es, en)
                if k not in seen:
                    seen.add(k)
                    items.append((k, es, en, path))
                return
            for kk, v in x.items():
                walk(v, f"{path}.{kk}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
    walk(pack, "")
    todo = [(k, es, en, p) for k, es, en, p in items if es != en]
    same = [(k, es) for k, es, en, p in items if es == en]
    index[pack["id"]] = {"file": f, "items": len(items), "todo": len(todo), "same": len(same)}
    chunks, cur, size = [], [], 0
    for it in todo:
        cur.append(it); size += len(it[2])
        if size >= CHUNK:
            chunks.append(cur); cur, size = [], 0
    if cur: chunks.append(cur)
    for n, ch in enumerate(chunks):
        with open(f"src/{pack['id']}_{n:02d}.txt", "w") as out:
            for k, es, en, p in ch:
                out.write(f"@{k} {p.split('.')[-1] if '.' in p else p}\nES {json.dumps(es, ensure_ascii=False)}\nEN {json.dumps(en, ensure_ascii=False)}\n")
    json.dump(dict(same), open(f"src/{pack['id']}_same.json", "w"), ensure_ascii=False)
    index[pack["id"]]["chunks"] = len(chunks)
json.dump(index, open("index.json", "w"), indent=1)
for k, v in index.items(): print(k, v["items"], v["todo"], v["chunks"])
