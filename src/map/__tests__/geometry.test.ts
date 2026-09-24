import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { advance, getNode, markArrived, startRoute } from "@/engine/runner";
import { projector, routeMapData, toGeoJSON } from "../geometry";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];
const byId = <T extends { id: string }>(xs: T[]) => Object.fromEntries(xs.map((x) => [x.id, x]));

it("sin partida: todas las paradas y los tramos de los dos caminos", () => {
  const { stops, segments } = routeMapData(route);
  expect(stops.map((s) => `${s.order}:${s.id}`)).toEqual([
    "1:n1_cenachero",
    "2:n2_larios",
    "3:a1_atarazanas",
    "4:a2_casa_guardia",
    "3:b1_constitucion",
    "5:n4_manquita",
    "6:n5_teatro",
    "7:n6_merced",
  ]);
  expect(segments.map((s) => `${s.id}:${s.branch ?? "-"}`)).toEqual([
    "n1_cenachero->n2_larios:-",
    "n2_larios->a1_atarazanas:dinero",
    "n2_larios->b1_constitucion:poder",
    "a1_atarazanas->a2_casa_guardia:dinero",
    "a2_casa_guardia->n4_manquita:dinero",
    "b1_constitucion->n4_manquita:poder",
    "n4_manquita->n5_teatro:-", // atraviesa los nodos narrativos 4a/4b
    "n5_teatro->n6_merced:-",
  ]);
  expect(stops.every((s) => s.status === "pending")).toBe(true);
});

it("con partida: recorrido, parada actual, siguientes y el otro camino", () => {
  let run = markArrived(route, startRoute("malaga", route));
  run = markArrived(route, advance(route, run));
  run = advance(route, run, getNode(route, "n2_larios").choices![1]); // poder
  const { stops, segments } = routeMapData(route, run);
  const s = byId(stops);
  expect(s.n1_cenachero.status).toBe("visited");
  expect(s.b1_constitucion.status).toBe("current");
  expect(s.a1_atarazanas.status).toBe("other");
  expect(s.a2_casa_guardia.status).toBe("other");
  expect(s.n4_manquita.status).toBe("pending");
  const g = byId(segments);
  expect(g["n1_cenachero->n2_larios"].status).toBe("walked");
  expect(g["n2_larios->b1_constitucion"].status).toBe("walked");
  expect(g["n2_larios->a1_atarazanas"].status).toBe("other");
  expect(g["b1_constitucion->n4_manquita"].status).toBe("pending");

  // Tras llegar a Constitución, la Manquita pasa a ser la siguiente.
  expect(byId(routeMapData(route, markArrived(route, run)).stops).n4_manquita.status).toBe("next");
});

it("exporta GeoJSON con [lng, lat]", () => {
  const geo = toGeoJSON(routeMapData(route));
  const stop = geo.features.find((f) => f.id === "n1_cenachero")!;
  expect(stop.geometry).toEqual({ type: "Point", coordinates: [-4.4196, 36.7188] });
  expect(stop.properties).toMatchObject({ kind: "stop", branch: "comun", order: 1 });
  expect(geo.features.filter((f) => f.properties?.kind === "segment")).toHaveLength(8);
});

it("la proyección encaja las paradas en el lienzo sin deformar", () => {
  const { bounds, stops } = routeMapData(route);
  const project = projector(bounds, 300, 400, 20);
  for (const s of stops) {
    const { x, y } = project(s.location);
    expect(x).toBeGreaterThanOrEqual(19.99);
    expect(x).toBeLessThanOrEqual(280.01);
    expect(y).toBeGreaterThanOrEqual(19.99);
    expect(y).toBeLessThanOrEqual(380.01);
  }
  // El norte queda arriba: la Merced (más al norte) tiene menor y que la Marina.
  const merced = project(stops.find((s) => s.id === "n6_merced")!.location);
  const marina = project(stops.find((s) => s.id === "n1_cenachero")!.location);
  expect(merced.y).toBeLessThan(marina.y);
});
