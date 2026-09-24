import type { PlayerProgress, Route } from "@/content/types";
import type { PendingArrival } from "@/engine/geo";

/**
 * Versión web (y de tipos): no hay geofences ni tareas en segundo plano.
 * La implementación nativa está en background.native.ts.
 */
export const GEOFENCE_TASK = "geofences-ruta";

export async function takePendingArrivals(): Promise<PendingArrival[]> {
  return [];
}

export async function syncGeofences(_route: Route | undefined, _run: PlayerProgress | undefined): Promise<void> {}
