"""
Inserta fr/de/it en los packs, por texto (sin reformatear): tras cada "en" de un I18nText
{"es", "en"} añade los tres idiomas con el mismo separador que usa el archivo. Añade también las
respuestas traducidas de los retos de texto (answers.json) y los idiomas a `languages`.
Uso: python3 scripts/i18n/apply.py ciudad [--dry]  (tras extract.py y check.py)
"""
import glob, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ANSWERS = os.path.join(HERE, "answers.json")
os.chdir(os.path.join(ROOT, "scripts", ".cache", "i18n"))
LANGS = ("fr", "de", "it")
STR = r'"(?:[^"\\]|\\.)*"'
PAIR = re.compile(rf'"es":(\s*)({STR})(\s*,\s*)"en":(\s*)({STR})((?:\s*,\s*"(?:fr|de|it)":\s*{STR})*)')

def tid(es, en):
    return hashlib.sha1((es + "\x00" + en).encode()).hexdigest()[:8]

def load_tr(city):
    tr = {}
    for f in sorted(glob.glob(f"out/{city}_*.json")):
        tr.update(json.load(open(f)))
    same = json.load(open(f"src/{city}_same.json")) if os.path.exists(f"src/{city}_same.json") else {}
    return tr, same

def strip_new(obj):
    if isinstance(obj, dict):
        return {k: strip_new(v) for k, v in obj.items() if not (k in LANGS and isinstance(obj.get("es"), str))}
    if isinstance(obj, list):
        return [strip_new(v) for v in obj]
    return obj

def main(city, dry):
    path = glob.glob(f"{ROOT}/content/{city}/*.pack.json")[0]
    text = open(path).read()
    before = json.loads(text)
    tr, same = load_tr(city)
    missing = []
    def repl(m):
        es, en = json.loads(m.group(2)), json.loads(m.group(5))
        k = tid(es, en)
        if m.group(6) and k not in tr:
            return m.group(0)  # ya traducido
        if es == en:
            vals = [es, es, es]
        elif k in tr:
            vals = tr[k]
        else:
            missing.append((k, es[:60]))
            return m.group(0)
        sep, sp = m.group(3), m.group(4)
        extra = "".join(f'{sep}"{l}":{sp}{json.dumps(v, ensure_ascii=False)}' for l, v in zip(LANGS, vals))
        return m.group(0)[: m.end(5) - m.start(0)] + extra
    new = PAIR.sub(repl, text)
    # respuestas de los retos de texto
    answers = json.load(open(ANSWERS)) if os.path.exists(ANSWERS) else {}
    for old, add in answers.get(city, {}).items():
        arr = json.loads(old)
        full = arr + [a for a in add if a not in arr]
        pat = re.compile(r'"answer":(\s*)\[[^\]]*\]')
        def arepl(m):
            try:
                cur = json.loads(m.group(0).split(":", 1)[1])
            except ValueError:
                return m.group(0)
            if cur[: len(arr)] != arr:
                return m.group(0)
            return f'"answer":{m.group(1)}{json.dumps(full, ensure_ascii=False)}'
        new = pat.sub(arepl, new)
    # idiomas del pack
    new = re.sub(r'"languages":\s*\[[^\]]*\]', lambda m: m.group(0) if '"it"' in m.group(0) else '"languages": ["es", "en", "fr", "de", "it"]', new, count=1)
    after = json.loads(new)
    assert strip_new(after)["routes"] and True
    # es/en intactos: quitando los idiomas nuevos (y respuestas añadidas) queda el pack original
    a, b = strip_new(after), strip_new(before)
    a["languages"] = b["languages"]
    def drop_answers(o):
        if isinstance(o, dict):
            return {k: (None if k == "answer" else drop_answers(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [drop_answers(v) for v in o]
        return o
    assert drop_answers(a) == drop_answers(b), "el pack ha cambiado además de los idiomas nuevos"
    print(city, "sin traducir:", len(missing))
    for k, es in missing[:10]:
        print("  ", k, es)
    if not dry and not missing:
        open(path, "w").write(new)
        print("escrito", path)

if __name__ == "__main__":
    main(sys.argv[1], "--dry" in sys.argv)
