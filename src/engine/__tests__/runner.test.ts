import raw from "@content/malaga/misterio-manquita.pack.json";
import type { PlayerProgress, Route } from "@/content/types";
import { loadPack } from "../loadPack";
import {
  advance,
  availableChoices,
  findBottleneck,
  getNode,
  isFinished,
  resolveEnding,
  resolveText,
  routeStops,
  RunnerError,
  startRoute,
} from "../runner";

const T0 = "2026-01-01T10:00:00.000Z";
const T1 = "2026-01-01T11:30:00.000Z";

function loadRoute(): Route {
  const result = loadPack(raw);
  if (!result.ok) throw new Error(result.errors.join("\n"));
  return result.pack.routes[0];
}
const route = loadRoute();

/**
 * Juega la ruta entera. En cada decisión elige la opción que pone el flag
 * indicado en `decisions` (en orden). Devuelve el estado final y el recorrido.
 */
function play(decisions: string[]): PlayerProgress {
  let state = startRoute("malaga", route, T0);
  const pending = [...decisions];
  for (let steps = 0; !isFinished(state); steps++) {
    if (steps > route.nodes.length * 2) throw new Error("la partida no termina");
    const node = getNode(route, state.currentNodeId);
    if (node.choices) {
      const flag = pending.shift();
      const choice = availableChoices(node, state.flags).find((c) => c.setFlags?.includes(flag ?? ""));
      if (!choice) throw new Error(`no hay decisión con el flag "${flag}" en ${node.id}`);
      state = advance(route, state, choice, T1);
    } else {
      state = advance(route, state, undefined, T1);
    }
  }
  expect(pending).toEqual([]);
  return state;
}

describe("los 4 finales son alcanzables", () => {
  it.each([
    ["camino_dinero", "version_caminos", "detective_puerto", ["a1_atarazanas", "a2_casa_guardia", "n4b_antequera"]],
    ["camino_dinero", "version_america", "alma_marinera", ["a1_atarazanas", "a2_casa_guardia", "n4a_america"]],
    ["camino_poder", "version_caminos", "detective_despacho", ["b1_constitucion", "n4b_antequera"]],
    ["camino_poder", "version_america", "cuentacuentos", ["b1_constitucion", "n4a_america"]],
  ])("%s + %s → %s", (camino, version, endingId, branchNodes) => {
    const state = play([camino, version]);
    expect(state.endingId).toBe(endingId);
    expect(state.completedAt).toBe(T1);
    expect(state.startedAt).toBe(T0);
    expect(state.flags).toEqual([camino, version]);
    expect(state.visitedNodeIds).toEqual(expect.arrayContaining(branchNodes));
    // Los cuellos de botella se visitan siempre.
    expect(state.visitedNodeIds).toEqual(
      expect.arrayContaining(["n1_cenachero", "n2_larios", "n4_manquita", "n5_teatro", "n6_merced", "n7_final"]),
    );
    expect(state.collectibleIds).toEqual(
      expect.arrayContaining(["cenacho_dorado", "foto_con_picasso", "insignia_detective_manquita"]),
    );
  });

  it("recorriendo todas las combinaciones de decisiones se llega a todos los finales y todos los nodos", () => {
    const endings = new Set<string>();
    const visited = new Set<string>();
    const explore = (state: PlayerProgress, depth: number) => {
      expect(depth).toBeLessThan(route.nodes.length * 2);
      state.visitedNodeIds.forEach((id) => visited.add(id));
      if (isFinished(state)) {
        expect(state.endingId).toBeDefined();
        endings.add(state.endingId!);
        return;
      }
      const node = getNode(route, state.currentNodeId);
      if (node.choices) availableChoices(node, state.flags).forEach((c) => explore(advance(route, state, c), depth + 1));
      else explore(advance(route, state), depth + 1);
    };
    explore(startRoute("malaga", route), 0);
    expect([...endings].sort()).toEqual(route.endings!.map((e) => e.id).sort());
    expect([...visited].sort()).toEqual(route.nodes.map((n) => n.id).sort());
  });

  it("cada camino da sus pistas y coleccionables propios", () => {
    const dinero = play(["camino_dinero", "version_caminos"]);
    expect(dinero.clueIds).toEqual(["pista_puerto", "pista_caminos", "pista_reaprovechar"]);
    expect(dinero.collectibleIds).toEqual(expect.arrayContaining(["arco_nazari", "tiza_de_guardia"]));
    expect(dinero.collectibleIds).not.toContain("sello_real");

    const poder = play(["camino_poder", "version_america"]);
    expect(poder.clueIds).toEqual(["pista_madrid", "pista_reaprovechar"]);
    expect(poder.collectibleIds).toContain("sello_real");
    expect(poder.collectibleIds).not.toContain("arco_nazari");
  });
});

describe("resolveText", () => {
  const manquita = getNode(route, "n4_manquita");
  const conVariantes = manquita.content[2];

  it("elige la variante según los flags", () => {
    expect(resolveText(conVariantes, ["camino_dinero"])?.es).toMatch(/^Vienes del puerto/);
    expect(resolveText(conVariantes, ["camino_poder"])?.es).toMatch(/^Vienes de la Plaza Mayor/);
  });

  it("gana la primera variante que encaja, y exige todos sus flags", () => {
    const final = getNode(route, "n7_final").content[0];
    expect(resolveText(final, ["camino_poder", "version_america"])?.es).toMatch(/guerra de América/);
    expect(resolveText(final, ["camino_poder"])).toBeNull();
  });

  it("usa `text` como respaldo y null si no hay texto", () => {
    const block = { type: "dialogue" as const, characterId: "x", text: { es: "hola" }, variants: [{ requires: ["f"], text: { es: "adiós" } }] };
    expect(resolveText(block, [])?.es).toBe("hola");
    expect(resolveText(block, ["f"])?.es).toBe("adiós");
    expect(resolveText(manquita.content[0], [])).toBeNull(); // bloque "scene"
  });
});

describe("availableChoices", () => {
  it("filtra por `requires`", () => {
    const node = {
      ...getNode(route, "n2_larios"),
      choices: [
        { label: { es: "libre" }, targetNodeId: "a1_atarazanas" },
        { label: { es: "secreta" }, targetNodeId: "b1_constitucion", requires: ["llave"] },
      ],
    };
    expect(availableChoices(node, []).map((c) => c.label.es)).toEqual(["libre"]);
    expect(availableChoices(node, ["llave"]).map((c) => c.label.es)).toEqual(["libre", "secreta"]);
  });
});

describe("advance", () => {
  const atLarios = () => advance(route, startRoute("malaga", route));

  it("exige decisión en los nodos con choices", () => {
    expect(() => advance(route, atLarios())).toThrow(RunnerError);
  });

  it("rechaza decisiones que no pertenecen al nodo", () => {
    const fake = { label: { es: "atajo" }, targetNodeId: "n7_final" };
    expect(() => advance(route, atLarios(), fake)).toThrow(/no está disponible/);
  });

  it("rechaza decisiones en nodos sin choices", () => {
    const choice = getNode(route, "n2_larios").choices![0];
    expect(() => advance(route, startRoute("malaga", route), choice)).toThrow(/no tiene decisiones/);
  });

  it("no deja avanzar una partida terminada", () => {
    const done = play(["camino_poder", "version_caminos"]);
    expect(() => advance(route, done)).toThrow(/ya ha terminado/);
  });

  it("no muta el estado de entrada", () => {
    const state = atLarios();
    const snapshot = JSON.parse(JSON.stringify(state));
    advance(route, state, getNode(route, "n2_larios").choices![0]);
    expect(state).toEqual(snapshot);
  });
});

describe("resolveEnding", () => {
  it("devuelve undefined si no encaja ningún final", () => {
    expect(resolveEnding(route, ["camino_dinero"])).toBeUndefined();
    expect(resolveEnding(route, ["camino_dinero", "version_america"])?.id).toBe("alma_marinera");
  });
});

describe("routeStops", () => {
  it("encuentra los cuellos de botella de las dos decisiones", () => {
    expect(findBottleneck(route, getNode(route, "n2_larios"))).toBe("n4_manquita");
    expect(findBottleneck(route, getNode(route, "n4_manquita"))).toBe("n5_teatro");
  });

  it("antes de decidir muestra la rama como una sola parada", () => {
    const { stops, current } = routeStops(route, startRoute("malaga", route));
    expect(stops.map((s) => s.id)).toEqual(["n1_cenachero", "n2_larios", "rama:n2_larios", "n4_manquita", "n5_teatro", "n6_merced"]);
    expect(current).toBe(0);
  });

  it("tras decidir muestra las paradas reales con su camino", () => {
    let state = advance(route, startRoute("malaga", route));
    state = advance(route, state, getNode(route, "n2_larios").choices![0]);
    const { stops, current } = routeStops(route, state);
    expect(stops.map((s) => [s.id, s.branch])).toEqual([
      ["n1_cenachero", undefined],
      ["n2_larios", undefined],
      ["a1_atarazanas", "dinero"],
      ["a2_casa_guardia", "dinero"],
      ["n4_manquita", undefined],
      ["n5_teatro", undefined],
      ["n6_merced", undefined],
    ]);
    expect(current).toBe(2);
  });

  it("en un nodo narrativo marca la última parada física", () => {
    const state = { ...play(["camino_poder", "version_america"]), completedAt: undefined, currentNodeId: "n4a_america" };
    const { stops, current } = routeStops(route, state);
    expect(stops[current].id).toBe("n4_manquita");
  });
});
