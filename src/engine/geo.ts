import type { LatLng, PlayerProgress, Route, StoryNode } from "@/content/types";
import { availableChoices, getNode, hasArrived, isFinished, needsArrival } from "./runner";

/** Radio por defecto si el nodo no trae `triggerRadiusM` (casco antiguo: 30–60 m). */
export const DEFAULT_RADIUS_M = 40;
/** iOS no permite más de 20 regiones vigiladas por app. */
export const MAX_GEOFENCES = 20;
/** Margen máximo que se concede por la imprecisión del GPS. */
const MAX_ACCURACY_BONUS_M = 20;

export type Fix = LatLng & { accuracy?: number | null };

/** Distancia en metros entre dos puntos (haversine). */
export function distanceM(a: LatLng, b: LatLng): number {
  const R = 6371000;
  const rad = (d: number) => (d * Math.PI) / 180;
  const dLat = rad(b.lat - a.lat);
  const dLng = rad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}

export function radiusOf(node: StoryNode): number {
  return node.triggerRadiusM ?? DEFAULT_RADIUS_M;
}

/** El jugador está dentro del radio del nodo, con algo de margen por la precisión del GPS. */
export function isInside(fix: Fix, node: StoryNode): boolean {
  if (!node.location) return false;
  const bonus = Math.min(Math.max(fix.accuracy ?? 0, 0), MAX_ACCURACY_BONUS_M);
  return distanceM(fix, node.location) <= radiusOf(node) + bonus;
}

/**
 * Nodos con ubicación a los que el jugador puede llegar a continuación: el
 * actual si aún no ha llegado; si no, las primeras paradas físicas de cada
 * salida posible (atravesando nodos narrativos). Es lo que hay que vigilar
 * con geofences, sin pasar del límite de iOS.
 */
export function geofenceTargets(route: Route, run: PlayerProgress, max: number = MAX_GEOFENCES): StoryNode[] {
  if (isFinished(run)) return [];
  const current = getNode(route, run.currentNodeId);
  if (!hasArrived(route, run)) return [current];

  const targets: StoryNode[] = [];
  const seen = new Set<string>([current.id]);
  const queue: string[] = exits(current, run.flags);
  while (queue.length > 0 && targets.length < max) {
    const id = queue.shift()!;
    if (seen.has(id)) continue;
    seen.add(id);
    const node = getNode(route, id);
    if (needsArrival(node)) targets.push(node);
    else queue.push(...exits(node, run.flags));
  }
  return targets;
}

function exits(node: StoryNode, flags: readonly string[]): string[] {
  if (node.choices) return availableChoices(node, flags).map((c) => c.targetNodeId);
  return node.nextNodeId ? [node.nextNodeId] : [];
}
