import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { distanceM, geofenceTargets, isInside } from "../geo";
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
