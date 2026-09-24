import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { advance, getNode, markArrived, startRoute } from "@/engine/runner";
import { SCENE_LAYERS } from "../assets.generated";
import { sceneKeyFor, sceneKeyOf } from "../sceneFor";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];

it("saca la clave del nombre del fondo", () => {
  expect(sceneKeyOf("fondos/fondo_marina.svg")).toBe("marina");
  expect(sceneKeyOf("fondos/fondo_casa_guardia.svg")).toBe("casa_guardia");
  expect(sceneKeyOf(undefined)).toBeUndefined();
});

it("todas las paradas del pack tienen capas generadas", () => {
  for (const node of route.nodes) {
    const key = sceneKeyOf(node.background);
    if (key) expect(Object.keys(SCENE_LAYERS)).toContain(key);
  }
});

it("cada escena tiene cielo o fondo, primer plano e imagen compuesta", () => {
  for (const [key, layers] of Object.entries(SCENE_LAYERS)) {
    const roles = layers.map((l) => l.role);
    expect([key, roles.includes("near")]).toEqual([key, true]);
    expect([key, roles.includes("flat")]).toEqual([key, true]);
    expect([key, roles.some((r) => r === "sky" || r === "far")]).toEqual([key, true]);
  }
});

it("los nodos narrativos heredan la escena de la última parada", () => {
  let run = startRoute("malaga", route);
  expect(sceneKeyFor(route, run)).toBe("marina");
  // Hasta la Manquita por el camino del poder y elegir la leyenda (nodo narrativo).
  run = advance(route, markArrived(route, run));
  run = advance(route, markArrived(route, run), getNode(route, "n2_larios").choices![1]);
  run = advance(route, markArrived(route, run));
  expect(sceneKeyFor(route, run)).toBe("manquita");
  run = advance(route, markArrived(route, run), getNode(route, "n4_manquita").choices![0]);
  expect(run.currentNodeId).toBe("n4a_america");
  expect(sceneKeyFor(route, run)).toBe("manquita");
});
