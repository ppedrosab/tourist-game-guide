import { useEffect } from "react";
import { AppState } from "react-native";
import { findRoute } from "@/engine/catalog";
import { pendingArrivalFor } from "@/engine/geo";
import { useProgress } from "@/store/progress";
import { syncGeofences, takePendingArrivals } from "./background";

/**
 * Sin interfaz. Mantiene los geofences al día con la partida en curso y, al
 * volver a primer plano, aplica las llegadas detectadas en segundo plano.
 */
export function GeofenceSync() {
  const hydrated = useProgress((s) => s.hydrated);
  const routeId = useProgress((s) => s.lastRouteId);
  const run = useProgress((s) => (routeId ? s.runs[routeId] : undefined));
  const found = routeId ? findRoute(routeId) : undefined;
  const active = run && !run.completedAt ? run : undefined;
  // Clave estable: solo cambia cuando cambian las paradas a vigilar.
  const key = active ? `${active.routeId}:${active.currentNodeId}:${active.arrivedAt ?? ""}:${active.flags.join(",")}` : "";

  useEffect(() => {
    if (hydrated) syncGeofences(found?.route, active);
  }, [hydrated, key]);

  useEffect(() => {
    if (!hydrated) return;
    const apply = async () => {
      const pending = await takePendingArrivals();
      const { runs, markArrived } = useProgress.getState();
      for (const run of Object.values(runs)) {
        const route = findRoute(run.routeId)?.route;
        if (route && !run.completedAt && pendingArrivalFor(run, pending)) markArrived(route, "geofence");
      }
    };
    apply();
    const sub = AppState.addEventListener("change", (state) => state === "active" && apply());
    return () => sub.remove();
  }, [hydrated]);

  return null;
}
