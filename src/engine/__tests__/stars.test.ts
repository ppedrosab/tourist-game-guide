import raw from "@content/malaga/misterio-manquita.pack.json";
import type { PlayerProgress, Route } from "@/content/types";
import { loadPack } from "../loadPack";
import { advance, getNode, isFinished, isGraded, recordChallenge, starsFor, startRoute } from "../runner";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];

/** Juega por dinero + documentos respondiendo `answer(nodeId)` en cada reto. */
function play(answer: (nodeId: string) => boolean): PlayerProgress {
  let run = startRoute("malaga", route);
  const decisions = ["camino_dinero", "version_caminos"];
  while (!isFinished(run)) {
    const node = getNode(route, run.currentNodeId);
    run = recordChallenge(route, run, answer(node.id));
    const choice = node.choices?.find((c) => c.setFlags?.some((f) => decisions.includes(f)));
    run = advance(route, run, choice);
  }
  return run;
}

it("solo puntúan quiz y observación (la foto no)", () => {
  expect(isGraded(getNode(route, "n2_larios"))).toBe(true); // quiz
  expect(isGraded(getNode(route, "a2_casa_guardia"))).toBe(true); // observe
  expect(isGraded(getNode(route, "n6_merced"))).toBe(false); // foto
  expect(isGraded(getNode(route, "n1_cenachero"))).toBe(false); // sin reto
});

it("cuenta el primer intento y solo en nodos con reto puntuable", () => {
  let run = advance(route, startRoute("malaga", route)); // en Larios
  run = recordChallenge(route, run, false);
  run = recordChallenge(route, run, true);
  expect(run.challengeResults).toEqual({ n2_larios: false });
  const n1 = startRoute("malaga", route);
  expect(recordChallenge(route, n1, true)).toBe(n1);
});

it("3 estrellas acertando todo, 2 con al menos el 60 %, 1 con menos", () => {
  // Camino dinero + documentos: Larios, Atarazanas, Casa de Guardia, Manquita, Teatro, Resolver = 6 retos.
  expect(starsFor(route, play(() => true))).toEqual({ stars: 3, correct: 6, total: 6 });
  const fallos = new Set(["n2_larios", "a1_atarazanas"]);
  expect(starsFor(route, play((id) => !fallos.has(id)))).toEqual({ stars: 2, correct: 4, total: 6 });
  expect(starsFor(route, play(() => false))).toEqual({ stars: 1, correct: 0, total: 6 });
});

it("solo cuentan los retos del camino recorrido", () => {
  const run = play(() => true);
  expect(run.visitedNodeIds).not.toContain("b1_constitucion");
  expect(Object.keys(run.challengeResults ?? {})).not.toContain("b1_constitucion");
});
