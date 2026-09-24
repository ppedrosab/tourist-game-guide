import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import {
  distanceM,
  geofenceRegions,
  geofenceTargets,
  isInside,
  offerManualArrival,
  parseRegionId,
  pendingArrivalFor,
  regionId,
} from "../geo";
import { loadPack } from "../loadPack";
import { advance, getNode, hasArrived, markArrived, startRoute } from "../runner";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];
const ids = (nodes: { id: string }[]) => nodes.map((n) => n.id);

describe("distancias", () => {
  it("calcula metros con haversine", () => {
    // Plaza de la Marina → Calle Larios: unos 200 m.
    const d = distanceM(getNode(route, "n1_cenachero").location!, getNode(route, "n2_larios").location!);
    expect(d).toBeGreaterThan(150);
    expect(d).toBeLessThan(250);
    expect(distanceM({ lat: 36.72, lng: -4.42 }, { lat: 36.72, lng: -4.42 })).toBe(0);
  });

  it("isInside respeta el radio y concede un margen limitado por la precisión", () => {
    const node = getNode(route, "n1_cenachero"); // radio 40 m
    const at = (metersNorth: number, accuracy?: number) => ({
      lat: node.location!.lat + metersNorth / 111_320,
      lng: node.location!.lng,
      accuracy,
    });
    expect(isInside(at(30), node)).toBe(true);
    expect(isInside(at(50), node)).toBe(false);
    expect(isInside(at(50, 15), node)).toBe(true);
    expect(isInside(at(70, 500), node)).toBe(false); // un GPS muy impreciso no regala la llegada
    expect(isInside(at(0), getNode(route, "n4a_america"))).toBe(false); // nodo narrativo
  });
});

describe("llegada", () => {
  it("los nodos con ubicación esperan la llegada y markArrived es idempotente", () => {
    let run = startRoute("malaga", route);
    expect(hasArrived(route, run)).toBe(false);
    run = markArrived(route, run, "t1");
    expect(run.arrivedAt).toBe("t1");
    expect(markArrived(route, run, "t2").arrivedAt).toBe("t1");
    run = advance(route, run);
    expect(run.arrivedAt).toBeUndefined(); // nuevo nodo, nueva llegada
  });
});

describe("geofenceTargets", () => {
  it("antes de llegar vigila solo el nodo actual", () => {
    expect(ids(geofenceTargets(route, startRoute("malaga", route)))).toEqual(["n1_cenachero"]);
  });

  it("tras llegar vigila las siguientes paradas posibles, las dos ramas en una decisión", () => {
    let run = markArrived(route, startRoute("malaga", route));
    expect(ids(geofenceTargets(route, run))).toEqual(["n2_larios"]);
    run = markArrived(route, advance(route, run));
    expect(ids(geofenceTargets(route, run))).toEqual(["a1_atarazanas", "b1_constitucion"]);
  });

  it("atraviesa los nodos narrativos hasta la siguiente parada física", () => {
    let run = startRoute("malaga", route);
    for (const choice of [undefined, 0, undefined, undefined]) {
      run = markArrived(route, run);
      const node = getNode(route, run.currentNodeId);
      run = advance(route, run, choice === undefined ? undefined : node.choices![choice]);
    }
    // En la Manquita, tras llegar: las dos versiones son narrativas y ambas llevan al Teatro.
    expect(run.currentNodeId).toBe("n4_manquita");
    expect(ids(geofenceTargets(route, markArrived(route, run)))).toEqual(["n5_teatro"]);
  });

  it("no pasa del máximo y no vigila nada al terminar", () => {
    const run = markArrived(route, advance(route, markArrived(route, startRoute("malaga", route))));
    expect(geofenceTargets(route, run, 1)).toHaveLength(1);
    expect(geofenceTargets(route, { ...run, completedAt: "fin" })).toEqual([]);
  });
});

describe("offerManualArrival", () => {
  const t0 = 1_000_000;
  it("se ofrece sin permiso o sin GPS", () => {
    expect(offerManualArrival({ status: "denied", now: t0 })).toBe(true);
    expect(offerManualArrival({ status: "unavailable", now: t0 })).toBe(true);
    expect(offerManualArrival({ status: "asking", now: t0 })).toBe(false);
  });

  it("se ofrece tras 60 s sin posición", () => {
    const gps = { status: "watching" as const, watchStartedAt: t0 };
    expect(offerManualArrival({ ...gps, now: t0 + 59_000 })).toBe(false);
    expect(offerManualArrival({ ...gps, now: t0 + 60_000 })).toBe(true);
    expect(offerManualArrival({ ...gps, lastFixAt: t0 + 30_000, now: t0 + 60_000 })).toBe(false);
    expect(offerManualArrival({ ...gps, lastFixAt: t0 + 30_000, now: t0 + 90_000 })).toBe(true);
  });
});

describe("geofences en segundo plano", () => {
  it("codifica y decodifica el id de región", () => {
    expect(parseRegionId(regionId("misterio-manquita", "n2_larios"))).toEqual({
      routeId: "misterio-manquita",
      nodeId: "n2_larios",
    });
    expect(parseRegionId("sin-separador")).toBeUndefined();
    expect(parseRegionId("|n2")).toBeUndefined();
  });

  it("genera regiones con el radio de cada nodo", () => {
    const run = markArrived(route, advance(route, markArrived(route, startRoute("malaga", route))));
    expect(geofenceRegions(route, run)).toEqual([
      expect.objectContaining({ identifier: "misterio-manquita|a1_atarazanas", radius: 40, notifyOnEnter: true }),
      expect.objectContaining({ identifier: "misterio-manquita|b1_constitucion", radius: 40 }),
    ]);
  });

  it("solo aplica la llegada pendiente del nodo actual", () => {
    const run = startRoute("malaga", route);
    const pending = [
      { routeId: "misterio-manquita", nodeId: "n2_larios", at: "t0" },
      { routeId: "otra", nodeId: "n1_cenachero", at: "t1" },
      { routeId: "misterio-manquita", nodeId: "n1_cenachero", at: "t2" },
    ];
    expect(pendingArrivalFor(run, pending)?.at).toBe("t2");
    expect(pendingArrivalFor(run, pending.slice(0, 2))).toBeUndefined();
  });
});
