"""Comprueba que cada out/{chunk}.json cubre su src/{chunk}.txt: ids, 3 idiomas y saltos de línea."""
import json, sys, glob, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache", "i18n"))
bad = 0
for src in sorted(glob.glob("src/*_[0-9][0-9].txt")):
    name = os.path.basename(src)[:-4]
    out = f"out/{name}.json"
    if not os.path.exists(out):
        continue
    ids, es = [], {}
    lines = open(src).read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith("@"):
            k = l[1:].split()[0]; ids.append(k); es[k] = json.loads(lines[i + 1][3:])
    tr = json.load(open(out))
    missing = [k for k in ids if k not in tr]
    extra = [k for k in tr if k not in es]
    wrong = [k for k in ids if k in tr and (len(tr[k]) != 3 or not all(isinstance(t, str) and t.strip() for t in tr[k]))]
    nl = [k for k in ids if k in tr and len(tr[k]) == 3 and any(t.count("\n") != es[k].count("\n") for t in tr[k])]
    if missing or extra or wrong or nl:
        bad += 1
        print(name, "faltan", missing[:5], "sobran", extra[:5], "mal", wrong[:5], "saltos", nl[:5])
    else:
        print(name, "ok", len(ids))
sys.exit(1 if bad else 0)
