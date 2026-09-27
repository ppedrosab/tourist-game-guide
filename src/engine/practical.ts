import type { LegPractical, PlayerProgress, Route, StopPractical } from "@/content/types";

/** Pendiente a partir de la cual un tramo ya no es cómodo para sillas de ruedas y carritos (%). */
export const STEEP_GRADE = 6;

export interface RoutePracticalSummary {
  /** Subida y bajada del camino más exigente (las ramas no se suman entre sí). */
  up: number;
  down: number;
  /** Pendiente máxima de cualquier tramo (%). */
  grade: number;
  /** Tramos con escaleras. */
  stepLegs: number;
  /** Paradas con fuente de agua cerca, de cuántas. */
  waterStops: number;
  stops: number;
  /** Sin escaleras y sin cuestas fuertes en ningún tramo. */
  stepFree: boolean;
  gentle: boolean;
}

/**
 * Resumen práctico de la ruta, o null si no tiene datos. La subida es la del recorrido de principio
 * a fin que más sube: en una ruta ramificada el jugador solo hace uno de los caminos.
 */
export function routePractical(route: Route): RoutePracticalSummary | null {
  const p = route.practical;
  if (!p) return null;
  const legs = Object.entries(p.legs).map(([key, leg]) => {
    const [from, to] = key.split("->");
    return { from, to, leg };
  });
  const out = new Map<string, typeof legs>();
  for (const l of legs) out.set(l.from, [...(out.get(l.from) ?? []), l]);
  const targets = new Set(legs.map((l) => l.to));
  const starts = [...out.keys()].filter((id) => !targets.has(id));
  // recorrido que más sube (y su bajada), por búsqueda en el grafo de tramos (sin ciclos)
  let best = { up: 0, down: 0 };
  const walk = (id: string, up: number, down: number, seen: Set<string>) => {
    const next = (out.get(id) ?? []).filter((l) => !seen.has(l.to));
    if (next.length === 0) {
      if (up > best.up || (up === best.up && down > best.down)) best = { up, down };
      return;
    }
    for (const l of next) walk(l.to, up + l.leg.up, down + l.leg.down, new Set([...seen, l.to]));
  };
  for (const s of starts) walk(s, 0, 0, new Set([s]));
  const stops = Object.values(p.stops);
  const grade = Math.max(0, ...legs.map((l) => l.leg.grade));
  const stepLegs = legs.filter((l) => (l.leg.steps ?? 0) > 0).length;
  return {
    ...best,
    grade,
    stepLegs,
    waterStops: stops.filter((s) => s.water !== undefined).length,
    stops: stops.length,
    stepFree: stepLegs === 0,
    gentle: grade < STEEP_GRADE,
  };
}

/** Datos prácticos de una parada. */
export function stopPractical(route: Route, nodeId: string): StopPractical | undefined {
  return route.practical?.stops[nodeId];
}

/**
 * Tramo por el que el jugador va hacia `nodeId`: el que sale de la última parada física que ha
 * visitado. Si no ha visitado ninguna (la primera parada), no hay tramo.
 */
export function legTo(route: Route, run: Pick<PlayerProgress, "visitedNodeIds">, nodeId: string): LegPractical | undefined {
  const legs = route.practical?.legs;
  if (!legs) return undefined;
  for (let i = run.visitedNodeIds.length - 1; i >= 0; i--) {
    const leg = legs[`${run.visitedNodeIds[i]}->${nodeId}`];
    if (leg) return leg;
  }
  return undefined;
}
