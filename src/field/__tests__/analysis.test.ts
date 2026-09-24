import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { distanceM } from "@/engine/geo";
import { loadPack } from "@/engine/loadPack";
import { FieldEntry, fieldExport, fieldReport, median, percentile } from "../analysis";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];
const larios = route.nodes.find((n) => n.id === "n2_larios")!.location!;
/** Punto a `m` metros al norte de la parada. */
const north = (m: number) => ({ lat: larios.lat + m / 111_320, lng: larios.lng });

const at = "2026-10-01T10:00:00Z";
const fix = (m: number, accuracy: number): FieldEntry => ({ kind: "fix", routeId: route.id, nodeId: "n2_larios", at, ...north(m), accuracy });
const arrival = (m: number, method: "gps" | "manual" | "demo", accuracy = 8, waitedS = 300): FieldEntry => ({
  kind: "arrival",
  routeId: route.id,
  nodeId: "n2_larios",
  at,
  method,
  ...north(m),
  accuracy,
  waitedS,
});

it("mediana y percentil", () => {
  expect(median([])).toBeUndefined();
  expect(median([3, 1, 2])).toBe(2);
  expect(median([4, 1, 3, 2])).toBe(2.5);
  expect(percentile([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 0.9)).toBe(90);
});

it("sin registros: todas las paradas, sin datos y con aviso de pocas muestras", () => {
  const report = fieldReport(route, []);
  expect(report.map((r) => r.nodeId)).toEqual(route.nodes.filter((n) => n.location).map((n) => n.id));
  expect(report[0]).toMatchObject({ arrivals: 0, warnings: ["pocas_muestras"] });
  expect(report[0].medianDistanceM).toBeUndefined();
});

it("resume llegadas, precisión y esperas de una parada", () => {
  const log = [fix(100, 25), fix(60, 12), fix(20, 8), arrival(40, "gps", 8, 240), arrival(30, "gps", 10, 360), arrival(45, "gps", 6, 300)];
  const r = fieldReport(route, log).find((s) => s.nodeId === "n2_larios")!;
  expect(r.arrivals).toBe(3);
  expect(r.byMethod).toEqual({ gps: 3, geofence: 0, manual: 0, demo: 0 });
  expect(r.medianDistanceM).toBeCloseTo(40, 0);
  expect(r.medianWaitS).toBe(300);
  expect(r.medianAccuracyM).toBe(9); // 25, 12, 8 (fixes cercanos) + 8, 10, 6
  expect(r.suggestedRadiusM).toBe(40); // p90 25 + 15
  expect(r.warnings).toEqual([]);
});

it("las llegadas manuales sugieren dónde está de verdad la parada", () => {
  const log = [arrival(55, "manual"), arrival(65, "manual"), arrival(60, "manual"), arrival(0, "demo")];
  const r = fieldReport(route, log).find((s) => s.nodeId === "n2_larios")!;
  expect(distanceM(r.suggestedLocation!, north(60))).toBeLessThan(1);
  expect(r.offsetM).toBeCloseTo(60, 0);
  expect(r.warnings).toEqual(expect.arrayContaining(["coordenada_desplazada", "llegadas_manuales"]));
  // Las llegadas en modo demo no cuentan como datos reales.
  expect(r.medianDistanceM).toBeCloseTo(60, 0);
});

it("el radio sugerido está entre 30 y 60 m y avisa del GPS impreciso", () => {
  const malo = [fix(10, 80), fix(15, 90), arrival(20, "gps", 70), arrival(25, "gps", 85), arrival(30, "gps", 75)];
  const r = fieldReport(route, malo).find((s) => s.nodeId === "n2_larios")!;
  expect(r.suggestedRadiusM).toBe(60);
  expect(r.warnings).toContain("gps_impreciso");
  const bueno = [fix(5, 3), arrival(5, "gps", 3), arrival(6, "gps", 4), arrival(4, "gps", 3)];
  expect(fieldReport(route, bueno).find((s) => s.nodeId === "n2_larios")!.suggestedRadiusM).toBe(30);
});

it("ignora la precisión de posiciones lejanas a la parada", () => {
  const r = fieldReport(route, [fix(500, 200), fix(10, 5)]).find((s) => s.nodeId === "n2_larios")!;
  expect(r.medianAccuracyM).toBe(5);
});

it("exporta informe y registro", () => {
  const out = fieldExport(route, [arrival(10, "gps")], new Date(at));
  expect(out).toMatchObject({ routeId: "misterio-manquita", generatedAt: "2026-10-01T10:00:00.000Z" });
  expect(out.log).toHaveLength(1);
  expect(out.stops.length).toBeGreaterThan(0);
});
