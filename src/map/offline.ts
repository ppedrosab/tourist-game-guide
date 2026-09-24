import type { CityPack } from "@/content/types";
import { MAP_STYLE_URL } from "./config";
import { MapLibre } from "./maplibre";
import { offlinePlan } from "./offlinePlan";

/**
 * Mapas sin conexión por ciudad (paquetes offline de MapLibre). Solo en
 * builds con código nativo; en Expo Go y web el mapa es el esquema SVG, que
 * ya funciona sin datos.
 */
export const offlineSupported = MapLibre !== undefined;

export type CityOffline = { state: "none" | "partial" | "complete"; percentage: number; bytes: number };

/** Paquetes de una ciudad. El id nativo lo asigna MapLibre; el nuestro va en `metadata.id`. */
async function packsOf(cityId: string) {
  if (!MapLibre) return [];
  const packs = await MapLibre.OfflineManager.getPacks();
  return packs.filter((p) => p.metadata?.cityId === cityId);
}

export async function cityOfflineStatus(pack: CityPack): Promise<CityOffline> {
  const current = (await packsOf(pack.id)).find((p) => p.metadata?.id === offlinePlan(pack).id);
  if (!current) return { state: "none", percentage: 0, bytes: 0 };
  const s = await current.status();
  return {
    state: s.state === "complete" || s.percentage >= 100 ? "complete" : "partial",
    percentage: s.percentage,
    bytes: s.completedResourceSize,
  };
}

/**
 * Descarga (o reanuda) el mapa de la ciudad. Borra antes los paquetes de
 * versiones anteriores del pack (otros límites).
 */
export async function downloadCity(
  pack: CityPack,
  onProgress: (percentage: number, bytes: number) => void,
  onError: (message: string) => void,
): Promise<void> {
  if (!MapLibre) throw new Error("Mapas sin conexión no disponibles en esta versión de la app");
  const { OfflineManager } = MapLibre;
  const plan = offlinePlan(pack);
  const existing = await packsOf(pack.id);
  for (const old of existing.filter((p) => p.metadata?.id !== plan.id)) await OfflineManager.deletePack(old.id);

  const progress = (_: unknown, s: { percentage: number; completedResourceSize: number }) =>
    onProgress(s.percentage, s.completedResourceSize);
  const error = (_: unknown, e: { message: string }) => onError(e.message);
  const current = existing.find((p) => p.metadata?.id === plan.id);
  if (current) {
    await OfflineManager.addListener(current.id, progress, error);
    await current.resume();
    return;
  }
  await OfflineManager.createPack(
    {
      mapStyle: MAP_STYLE_URL,
      bounds: plan.bounds,
      minZoom: plan.minZoom,
      maxZoom: plan.maxZoom,
      metadata: { id: plan.id, cityId: pack.id, version: pack.version },
    },
    progress,
    error,
  );
}

export async function deleteCity(pack: CityPack): Promise<void> {
  if (!MapLibre) return;
  for (const p of await packsOf(pack.id)) await MapLibre.OfflineManager.deletePack(p.id);
}
