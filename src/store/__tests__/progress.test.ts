import AsyncStorage from "@react-native-async-storage/async-storage";
import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { getNode } from "@/engine/runner";
import { useProgress } from "../progress";

jest.mock("@react-native-async-storage/async-storage", () =>
  require("@react-native-async-storage/async-storage/jest/async-storage-mock"),
);

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];

/** Juega hasta el final eligiendo siempre la opción `pick` en cada decisión. */
function playToEnd(pick: number) {
  const store = useProgress.getState();
  store.start("malaga", route);
  for (;;) {
    const run = useProgress.getState().runs[route.id];
    if (run.completedAt) return run;
    const node = getNode(route, run.currentNodeId);
    store.advance(route, node.choices?.[pick]);
  }
}

beforeEach(() => {
  useProgress.setState({ runs: {}, collection: { collectibleIds: [], endingIds: [], clueIds: [] }, lastRouteId: undefined });
});

it("guarda el progreso en cada nodo en AsyncStorage", async () => {
  useProgress.getState().start("malaga", route);
  useProgress.getState().advance(route);
  await new Promise((r) => setTimeout(r, 0));
  const saved = JSON.parse((await AsyncStorage.getItem("progreso"))!);
  expect(saved.state.runs[route.id].currentNodeId).toBe("n2_larios");
  expect(saved.state.lastRouteId).toBe(route.id);
  expect(saved.state.hydrated).toBeUndefined();
});

it("la colección acumula finales entre partidas", () => {
  expect(playToEnd(0).endingId).toBe("alma_marinera");
  expect(playToEnd(1).endingId).toBe("detective_despacho");
  const { collection } = useProgress.getState();
  expect(collection.endingIds).toEqual(["alma_marinera", "detective_despacho"]);
  expect(collection.collectibleIds).toEqual(expect.arrayContaining(["arco_nazari", "sello_real"]));
});

it("guarda la mejor puntuación de cada ruta", () => {
  const store = useProgress.getState();
  // Primera partida: falla el primer reto (Larios).
  store.start("malaga", route);
  store.advance(route);
  store.recordChallenge(route, false);
  let run = useProgress.getState().runs[route.id];
  while (!run.completedAt) {
    const node = getNode(route, run.currentNodeId);
    useProgress.getState().recordChallenge(route, true);
    useProgress.getState().advance(route, node.choices?.[0]);
    run = useProgress.getState().runs[route.id];
  }
  expect(useProgress.getState().collection.bestStars).toEqual({ [route.id]: 2 });
  // Una partida peor no baja la mejor puntuación.
  playToEnd(0);
  expect(useProgress.getState().collection.bestStars).toEqual({ [route.id]: 2 });
});

it("discard borra la partida pero no la colección", () => {
  playToEnd(0);
  useProgress.getState().discard(route.id);
  const s = useProgress.getState();
  expect(s.runs[route.id]).toBeUndefined();
  expect(s.lastRouteId).toBeUndefined();
  expect(s.collection.endingIds).toEqual(["alma_marinera"]);
});

it("no se puede avanzar sin empezar", () => {
  expect(() => useProgress.getState().advance(route)).toThrow(/No hay partida/);
});
