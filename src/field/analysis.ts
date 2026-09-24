import type { LatLng, Route } from "@/content/types";
import { distanceM, radiusOf } from "@/engine/geo";
import { getNode, needsArrival } from "@/engine/runner";

/**
 * Prueba de campo (puro): a partir de lo registrado en la calle, cómo se
 * comporta cada parada y qué coordenadas y radios convendría poner en el pack.
 */

export type FieldFix = { kind: "fix"; routeId: string; nodeId: string; at: string; lat: number; lng: number; accuracy: number | null };
export type FieldArrival = {
  kind: "arrival";
  routeId: string;
  nodeId: string;
  at: string;
  method: "gps" | "geofence" | "manual" | "demo";
  /** Última posición conocida al llegar (si la había). */
  lat?: number;
  lng?: number;
  accuracy?: number | null;
  /** Segundos desde que la parada empezó a esperar la llegada. */
  waitedS?: number;
};
export type FieldEntry = FieldFix | FieldArrival;

export type StopReport = {
  nodeId: string;
  title: string;
  location: LatLng;
  radiusM: number;
  arrivals: number;
  byMethod: Record<FieldArrival["method"], number>;
  /** Mediana de la distancia a la parada al llegar (m). */
  medianDistanceM?: number;
  /** Mediana de la precisión del GPS cerca de la parada (m). */
  medianAccuracyM?: number;
  /** Mediana de lo que se tardó en llegar (s). */
  medianWaitS?: number;
  /** Punto medio de las llegadas manuales: dónde creía el probador que estaba la parada. */
  suggestedLocation?: LatLng;
  /** Distancia entre la coordenada del pack y la sugerida (m). */
  offsetM?: number;
  /** Radio recomendado: cubre la precisión típica, entre 30 y 60 m. */
  suggestedRadiusM?: number;
  warnings: ("pocas_muestras" | "coordenada_desplazada" | "gps_impreciso" | "llegadas_manuales")[];
};

export function median(xs: number[]): number | undefined {
  if (xs.length === 0) return undefined;
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

/** Percentil p (0..1) por el método del rango más cercano. */
export function percentile(xs: number[], p: number): number | undefined {
  if (xs.length === 0) return undefined;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.max(0, Math.ceil(p * s.length) - 1))];
}

/** Más lejos que esto de la parada, una posición no cuenta para su precisión. */
const NEARBY_M = 150;

export function fieldReport(route: Route, log: readonly FieldEntry[]): StopReport[] {
  return route.nodes.filter(needsArrival).map((node) => {
    const location = node.location!;
    const mine = log.filter((e) => e.routeId === route.id && e.nodeId === node.id);
    const arrivals = mine.filter((e): e is FieldArrival => e.kind === "arrival");
    const fixes = mine.filter((e): e is FieldFix => e.kind === "fix");
    const byMethod = { gps: 0, geofence: 0, manual: 0, demo: 0 };
    arrivals.forEach((a) => byMethod[a.method]++);

    const real = arrivals.filter((a) => a.method !== "demo" && a.lat !== undefined && a.lng !== undefined);
    const distances = real.map((a) => distanceM({ lat: a.lat!, lng: a.lng! }, location));
    const accuracies = [
      ...fixes.filter((f) => distanceM(f, location) <= NEARBY_M).map((f) => f.accuracy),
      ...real.map((a) => a.accuracy),
    ].filter((a): a is number => typeof a === "number" && a > 0);
    const waits = arrivals.map((a) => a.waitedS).filter((w): w is number => typeof w === "number");

    const manual = real.filter((a) => a.method === "manual");
    const suggestedLocation =
      manual.length > 0
        ? {
            lat: manual.reduce((s, a) => s + a.lat!, 0) / manual.length,
            lng: manual.reduce((s, a) => s + a.lng!, 0) / manual.length,
          }
        : undefined;
    const offsetM = suggestedLocation ? distanceM(suggestedLocation, location) : undefined;
    const p90 = percentile(accuracies, 0.9);
    const suggestedRadiusM = p90 !== undefined ? Math.round(Math.min(60, Math.max(30, p90 + 15))) : undefined;
    const medianAccuracyM = median(accuracies);

    const warnings: StopReport["warnings"] = [];
    if (real.length < 3) warnings.push("pocas_muestras");
    if (offsetM !== undefined && offsetM > 25) warnings.push("coordenada_desplazada");
    if (medianAccuracyM !== undefined && medianAccuracyM > 30) warnings.push("gps_impreciso");
    if (arrivals.length > 0 && byMethod.manual / arrivals.length >= 0.5) warnings.push("llegadas_manuales");

    return {
      nodeId: node.id,
      title: getNode(route, node.id).title.es,
      location,
      radiusM: radiusOf(node),
      arrivals: arrivals.length,
      byMethod,
      medianDistanceM: median(distances),
      medianAccuracyM,
      medianWaitS: median(waits),
      suggestedLocation,
      offsetM,
      suggestedRadiusM,
      warnings,
    };
  });
}

/** Informe exportable (JSON) con lo necesario para corregir el pack. */
export function fieldExport(route: Route, log: readonly FieldEntry[], now: Date = new Date()) {
  return {
    routeId: route.id,
    generatedAt: now.toISOString(),
    stops: fieldReport(route, log),
    log,
  };
}
