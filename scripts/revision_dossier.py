#!/usr/bin/env python3
"""
Dosier para la revisión histórica (npm run gen:dossier) → docs/REVISION_HISTORICA.md.

Reúne en un solo documento, ciudad por ciudad, lo que hay que comprobar antes de publicar:
- las listas «Datos a verificar» / «Datos que se afirman» de cada GDD;
- los personajes reales y de leyenda con sus fechas y referencias (del pack);
- los datos históricos y anécdotas «se cuenta» que dice cada ruta, con la parada.
Pensado para imprimirlo o compartirlo con los historiadores locales y marcar cada casilla.
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "REVISION_HISTORICA.md")
KIND = {"real": "persona real", "leyenda": "figura de leyenda", "tipo": "figura típica", "simbolo": "símbolo"}
# Qué GDD corresponde a cada pack (los temáticos de varias ciudades van aparte, al final).
GDD = {
    "malaga": ["GDD.md"], "cadiz": ["GDD_CADIZ.md", "GDD_CADIZ_GASTRO.md", "GDD_CADIZ_CARNAVAL.md", "GDD_CADIZ_SEMANA_SANTA.md"],
    "sevilla": ["GDD_SEVILLA.md"], "granada": ["GDD_GRANADA.md"], "cordoba": ["GDD_CORDOBA.md"],
    "huelva": ["GDD_HUELVA.md"], "jaen": ["GDD_JAEN.md"], "almeria": ["GDD_ALMERIA.md"],
}
SHARED = ["GDD_GASTRO_ANDALUCIA.md", "GDD_FIESTAS_ANDALUCIA.md", "GDD_LEYENDAS_ANDALUCIA.md"]
SECTION = re.compile(r"^## (Datos[^\n]*)\n(.*?)(?=^## |\Z)", re.M | re.S)


def checklist(md_text):
    """Secciones de datos a verificar de un GDD, como casillas."""
    out = []
    for title, body in SECTION.findall(md_text):
        items = re.split(r"\n(?=- |\d+\. )", body.strip())
        for it in items:
            it = re.sub(r"^(- |\d+\. )", "", it.strip()).replace("\n  ", " ").replace("\n", " ")
            if it:
                out.append(f"- [ ] {it}")
    return out


def main():
    lines = [
        "# Revisión histórica",
        "",
        "Dosier para los historiadores locales, generado con `npm run gen:dossier` a partir de los GDD y",
        "de los packs. Cada ciudad tiene tres bloques: lo que el diseño marcó para verificar, los",
        "personajes reales y de leyenda (fechas y referencias de su ficha) y todo lo que el juego afirma",
        "como dato histórico o cuenta como leyenda, parada por parada. Marcar cada casilla al revisarla y",
        "anotar la corrección al lado.",
        "",
        "Ya corregido al preparar este dosier: el cronista de la Malmuerta es Teodomiro (no Teodoro)",
        "Ramírez de Arellano, nacido en Cádiz; Galiana es leyenda de Toledo y en Almería la sustituye",
        "Abderramán III; la plaza de Mina de Cádiz estaba mal situada en el mapa.",
        "",
    ]
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*", "*.pack.json"))):
        pack = json.load(open(f))
        lines += [f"## {pack['name']['es']}", ""]
        items = []
        for g in GDD.get(pack["id"], []):
            p = os.path.join(ROOT, "docs", g)
            if os.path.exists(p):
                items += checklist(open(p).read())
        if items:
            lines += ["### Marcado en el diseño para verificar", ""] + items + [""]
        people = [c for c in pack["characters"] if c.get("kind") in ("real", "leyenda")]
        if people:
            lines += ["### Personajes reales y de leyenda", "", "| Personaje | Qué es | Fechas | Referencias |", "|---|---|---|---|"]
            for c in people:
                refs = " · ".join(f"[{s['title']}]({s['url']})" if s.get("url") else s["title"] for s in c.get("sources", []))
                lines.append(f"| {c['name']['es']} | {KIND[c['kind']]} | {c.get('lived', '—')} | {refs} |")
            lines.append("")
        for r in pack["routes"]:
            facts = []
            for n in r["nodes"]:
                for b in n["content"]:
                    if b["type"] == "historical_fact":
                        year = f" ({b['year']})" if b.get("year") else ""
                        facts.append(f"- [ ] **{n['title']['es']}**{year}: {b['text']['es']}")
                    elif b["type"] == "anecdote":
                        tag = "se cuenta" if b.get("legend") else "anécdota"
                        facts.append(f"- [ ] **{n['title']['es']}** ({tag}): {b['text']['es']}")
            if facts:
                lines += [f"### «{r['title']['es']}»: lo que afirma la ruta", ""] + facts + [""]
    lines += ["## Rutas temáticas de varias ciudades", ""]
    for g in SHARED:
        items = checklist(open(os.path.join(ROOT, "docs", g)).read())
        if items:
            lines += [f"### {g}", ""] + items + [""]
    open(OUT, "w").write("\n".join(lines))
    print(f"→ {os.path.relpath(OUT, ROOT)} ({len(lines)} líneas)")


if __name__ == "__main__":
    main()
