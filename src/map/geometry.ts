import type { BranchId, LatLng, PlayerProgress, Route, StoryNode } from "@/content/types";
import { geofenceTargets } from "@/engine/geo";
import { getNode, localize, needsArrival } from "@/engine/runner";

/**
 * Geometría del mapa de una ruta, pura y testeable: paradas físicas y tramos
 * entre ellas (atravesando nodos narrativos), con el camino y el estado según
 * la partida. La usan el mapa de MapLibre (GeoJSON) y el esquema SVG.
 */

export type StopStatus = "visited" | "current" | "next" | "pending" | "other";
export type SegmentStatus = "walked" | "pending" | "other";

export type MapStop = {
  id: string;
  title: string;
  location: LatLng;
  branch?: BranchId;
  status: StopStatus;
  /** Número de parada en el orden del recorrido (las de una rama comparten numeración). */
  order: number;
};

export type MapSegment = {
  id: string;
  from: string;
  to: string;
  /** Por las calles si la ruta trae su trazado (`route.paths`); si no, en línea recta. */
  coordinates: LatLng[];
  branch?: BranchId;
  status: SegmentStatus;
};

export type RouteMapData = { stops: MapStop[]; segments: MapSegment[]; bounds: [LatLng, LatLng] };

/** Siguientes paradas físicas desde un nodo, por todas sus salidas (sin mirar flags). */
function nextPhysical(route: Route, from: StoryNode): StoryNode[] {
  const out: StoryNode[] = [];
  const seen = new Set<string>([from.id]);
  const queue = [...(from.choices ?? []).map((c) => c.targetNodeId), ...(from.nextNodeId ? [from.nextNodeId] : [])];
  while (queue.length > 0) {
    const id = queue.shift()!;
    if (seen.has(id)) continue;
    seen.add(id);
    const node = getNode(route, id);
    if (needsArrival(node)) out.push(node);
    else queue.push(...(node.choices ?? []).map((c) => c.targetNodeId), ...(node.nextNodeId ? [node.nextNodeId] : []));
  }
  return out;
}

/** Camino que ha tomado el jugador (el de la primera parada con rama visitada). */
function chosenBranch(route: Route, run?: PlayerProgress): BranchId | undefined {
  return run?.visitedNodeIds.map((id) => route.nodes.find((n) => n.id === id)?.branch).find(Boolean);
}

export function routeMapData(route: Route, run?: PlayerProgress): RouteMapData {
  const physical = route.nodes.filter(needsArrival);
  const branch = chosenBranch(route, run);
  const next = new Set(run && !run.completedAt ? geofenceTargets(route, run).map((n) => n.id) : []);
  const isOther = (n: StoryNode) => !!(branch && n.branch && n.branch !== branch);

  // Número de parada = camino más largo desde el inicio: las ramas paralelas comparten
  // número y el cuello de botella va detrás de la rama más larga.
  const start = getNode(route, route.startNodeId);
  const order = new Map<string, number>();
  const queue = (needsArrival(start) ? [start] : nextPhysical(route, start)).map((node) => ({ node, depth: 1 }));
  for (let guard = 0; queue.length > 0 && guard < physical.length * physical.length; guard++) {
    const { node, depth } = queue.shift()!;
    if ((order.get(node.id) ?? 0) >= depth) continue;
    order.set(node.id, depth);
    for (const t of nextPhysical(route, node)) queue.push({ node: t, depth: depth + 1 });
  }

  const stops: MapStop[] = physical.map((node) => {
    let status: StopStatus = "pending";
    if (run) {
      if (node.id === run.currentNodeId && !run.completedAt) status = "current";
      else if (run.visitedNodeIds.includes(node.id)) status = "visited";
      else if (next.has(node.id)) status = "next";
      else if (isOther(node)) status = "other";
    }
    return {
      id: node.id,
      title: localize(node.title),
      location: node.location!,
      branch: node.branch,
      status,
      order: order.get(node.id) ?? 0,
    };
  });

  const segments: MapSegment[] = [];
  for (const from of physical) {
    for (const to of nextPhysical(route, from)) {
      const visited = (id: string) => run?.visitedNodeIds.includes(id) ?? false;
      let status: SegmentStatus = "pending";
      if (visited(from.id) && visited(to.id)) status = "walked";
      else if (isOther(from) || isOther(to)) status = "other";
      const id = `${from.id}->${to.id}`;
      const path = (route.paths?.[id] ?? []).map(([lng, lat]) => ({ lat, lng }));
      segments.push({
        id,
        from: from.id,
        to: to.id,
        coordinates: [from.location!, ...path, to.location!],
        branch: to.branch ?? from.branch,
        status,
      });
    }
  }

  const points = [...physical.map((s) => s.location!), ...segments.flatMap((s) => s.coordinates)];
  const lats = points.map((p) => p.lat);
  const lngs = points.map((p) => p.lng);
  const bounds: [LatLng, LatLng] = [
    { lat: Math.min(...lats), lng: Math.min(...lngs) },
    { lat: Math.max(...lats), lng: Math.max(...lngs) },
  ];
  return { stops, segments, bounds };
}

/** GeoJSON para MapLibre: líneas (tramos) y puntos (paradas) con sus propiedades. */
export function toGeoJSON(data: RouteMapData): GeoJSON.FeatureCollection {
  return {
    type: "FeatureCollection",
    features: [
      ...data.segments.map(
        (s): GeoJSON.Feature => ({
          type: "Feature",
          id: s.id,
          properties: { kind: "segment", branch: s.branch ?? "comun", status: s.status },
          geometry: { type: "LineString", coordinates: s.coordinates.map((c) => [c.lng, c.lat]) },
        }),
      ),
      ...data.stops.map(
        (s): GeoJSON.Feature => ({
          type: "Feature",
          id: s.id,
          properties: { kind: "stop", branch: s.branch ?? "comun", status: s.status, order: s.order, title: s.title },
          geometry: { type: "Point", coordinates: [s.location.lng, s.location.lat] },
        }),
      ),
    ],
  };
}

/**
 * Proyección para el esquema SVG: equirectangular corregida por la latitud
 * (a escala de ciudad es indistinguible de Mercator), encajada en un lienzo
 * con margen y manteniendo la proporción.
 */
export function projector(bounds: [LatLng, LatLng], width: number, height: number, padding: number) {
  const [sw, ne] = bounds;
  const k = Math.cos(((sw.lat + ne.lat) / 2) * (Math.PI / 180));
  const spanX = Math.max((ne.lng - sw.lng) * k, 1e-9);
  const spanY = Math.max(ne.lat - sw.lat, 1e-9);
  const scale = Math.min((width - 2 * padding) / spanX, (height - 2 * padding) / spanY);
  const offX = (width - spanX * scale) / 2;
  const offY = (height - spanY * scale) / 2;
  return (p: LatLng) => ({ x: offX + (p.lng - sw.lng) * k * scale, y: offY + (ne.lat - p.lat) * scale });
}
