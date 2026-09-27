import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Challenge, Route } from "@/content/types";
import { loadPack } from "../loadPack";
import { advance, hintCount, isGraded, recordChallenge, recordHint, startRoute, starsFor } from "../runner";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];
const t = (es: string) => ({ es, en: es });

it("cuenta las pistas pedidas por reto sin tocar el acierto", () => {
  let run = advance(route, startRoute("malaga", route)); // Larios, con quiz
  run = recordHint(route, run);
  run = recordHint(route, run);
  run = recordChallenge(route, run, true);
  expect(run.hintsUsed).toEqual({ n2_larios: 2 });
  expect(run.challengeResults).toEqual({ n2_larios: true });
  const first = startRoute("malaga", route); // Cenachero: sin reto
  expect(recordHint(route, first)).toBe(first);
});

it("una pista no quita estrellas", () => {
  let run = advance(route, startRoute("malaga", route));
  const without = starsFor(route, recordChallenge(route, run, true));
  run = recordHint(route, run);
  expect(starsFor(route, recordChallenge(route, run, true))).toEqual(without);
});

it("número de pistas: escritas, o quitar opciones del quiz / colocar en ordenar", () => {
  const quiz: Challenge = { type: "quiz", question: t("?"), options: [t("a"), t("b"), t("c"), t("d")], correctIndex: 1 };
  expect(hintCount(quiz)).toBe(2);
  expect(hintCount({ ...quiz, hints: [t("una")] })).toBe(1);
  const order: Challenge = { type: "order", prompt: t("?"), items: [t("1"), t("2"), t("3"), t("4"), t("5")] };
  expect(hintCount(order)).toBe(3);
  expect(hintCount({ type: "lock", prompt: t("?"), answer: ["x"] })).toBe(0);
  expect(hintCount({ type: "riddle", prompt: t("?"), answer: ["x"], hints: [t("a"), t("b")] })).toBe(2);
  expect(hintCount({ type: "photo", prompt: t("?") })).toBe(0);
});

it("acertijo, candado y ordenar son retos puntuables y el esquema los acepta", () => {
  const pack = JSON.parse(JSON.stringify(raw));
  const nodes = pack.routes[0].nodes;
  nodes[1].challenge = { type: "riddle", prompt: t("¿?"), answer: ["sí"], hints: [t("piensa")] };
  nodes[2].challenge = { type: "lock", prompt: t("¿?"), answer: ["1782"] };
  nodes[3].challenge = { type: "order", prompt: t("¿?"), items: [t("a"), t("b"), t("c")] };
  const loaded = loadPack(pack);
  expect(loaded.ok).toBe(true);
  if (!loaded.ok) return;
  for (const n of loaded.pack.routes[0].nodes.slice(1, 4)) expect(isGraded(n)).toBe(true);
  pack.routes[0].nodes[3].challenge = { type: "order", prompt: t("¿?"), items: [t("a"), t("b")] };
  expect(loadPack(pack).ok).toBe(false); // ordenar necesita al menos tres elementos
});
