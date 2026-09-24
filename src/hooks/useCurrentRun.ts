import type { CityPack, PlayerProgress, Route } from "@/content/types";
import { findRoute } from "@/engine/catalog";
import { useProgress } from "@/store/progress";

export type CurrentRun = { pack: CityPack; route: Route; run: PlayerProgress };

/**
 * Ruta que se está jugando (la última abierta) con su partida. La usan los
 * modales de pausa y cuaderno, que no reciben parámetros de ruta.
 */
export function useCurrentRun(): CurrentRun | undefined {
  const routeId = useProgress((s) => s.lastRouteId);
  const run = useProgress((s) => (routeId ? s.runs[routeId] : undefined));
  const found = routeId ? findRoute(routeId) : undefined;
  return found && run ? { ...found, run } : undefined;
}
