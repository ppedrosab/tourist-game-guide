import type { CityPack, LatLng } from "@/content/types";
import { OFFLINE_ZOOM } from "./config";

/**
 * Plan de descarga offline de una ciudad (puro): zona con margen, número de
 * teselas y tamaño aproximado para avisar antes de descargar.
 */

/** Margen alrededor de los límites de la ciudad (m): por si la calle de llegada queda justo fuera. */
const MARGIN_M = 150;
/** Peso medio de una tesela vectorial de casco urbano (bytes), estimación conservadora. */
const AVG_TILE_BYTES = 30_000;

export type OfflinePlan = {
  id: string;
  /** [oeste, sur, este, norte], como pide MapLibre. */
  bounds: [number, number, number, number];
  minZoom: number;
  maxZoom: number;
  tiles: number;
  approxBytes: number;
};

/** Id del paquete offline: cambia con la versión del pack para volver a descargar si cambian los límites. */
export const offlinePackId = (pack: CityPack) => `ciudad-${pack.id}@${pack.version}`;

export function expandBounds([a, b]: [LatLng, LatLng], meters: number): [LatLng, LatLng] {
  const south = Math.min(a.lat, b.lat);
  const north = Math.max(a.lat, b.lat);
  const west = Math.min(a.lng, b.lng);
  const east = Math.max(a.lng, b.lng);
  const dLat = meters / 111_320;
  const dLng = meters / (111_320 * Math.cos((((south + north) / 2) * Math.PI) / 180));
  return [
    { lat: south - dLat, lng: west - dLng },
    { lat: north + dLat, lng: east + dLng },
  ];
}

const lngToX = (lng: number, z: number) => Math.floor(((lng + 180) / 360) * 2 ** z);
const latToY = (lat: number, z: number) => {
  const r = (lat * Math.PI) / 180;
  return Math.floor(((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 2 ** z);
};

/** Teselas XYZ que cubren la zona en cada zoom. */
export function countTiles([sw, ne]: [LatLng, LatLng], minZoom: number, maxZoom: number): number {
  let total = 0;
  for (let z = minZoom; z <= maxZoom; z++) {
    const xs = lngToX(ne.lng, z) - lngToX(sw.lng, z) + 1;
    const ys = latToY(sw.lat, z) - latToY(ne.lat, z) + 1;
    total += xs * ys;
  }
  return total;
}

export function offlinePlan(pack: CityPack): OfflinePlan {
  const [sw, ne] = expandBounds(pack.bounds, MARGIN_M);
  const tiles = countTiles([sw, ne], OFFLINE_ZOOM.min, OFFLINE_ZOOM.max);
  return {
    id: offlinePackId(pack),
    bounds: [sw.lng, sw.lat, ne.lng, ne.lat],
    minZoom: OFFLINE_ZOOM.min,
    maxZoom: OFFLINE_ZOOM.max,
    tiles,
    approxBytes: tiles * AVG_TILE_BYTES,
  };
}

export function formatBytes(bytes: number): string {
  if (bytes < 1_000_000) return `${Math.max(1, Math.round(bytes / 1000))} KB`;
  return `${(bytes / 1_000_000).toLocaleString("es-ES", { maximumFractionDigits: 1 })} MB`;
}
