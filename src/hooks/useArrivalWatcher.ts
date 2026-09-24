import * as Location from "expo-location";
import { useEffect, useState } from "react";
import type { StoryNode } from "@/content/types";
import { distanceM, GpsStatus, isInside, offerManualArrival } from "@/engine/geo";
import { Fix, Watch, watchPosition } from "@/geo/watchPosition";

export type ArrivalWatch = {
  status: GpsStatus;
  /** Metros hasta la parada según la última posición, si la hay. */
  distance?: number;
  /** Mostrar "Ya estoy aquí": sin permiso, sin GPS o 60 s sin posición. */
  manualFallback: boolean;
  /** Última posición recibida (para la prueba de campo). */
  lastFix?: Fix;
};

/**
 * Vigila la posición en primer plano mientras la escena espera la llegada a
 * `node`. Al entrar en su radio llama a `onArrive`. Los geofences en segundo
 * plano (src/geo/background.ts) cubren el caso de la app cerrada.
 */
export function useArrivalWatcher(
  node: StoryNode,
  enabled: boolean,
  /** Recibe la posición que ha provocado la llegada. */
  onArrive: (fix: Fix) => void,
  onFix?: (fix: Fix) => void,
): ArrivalWatch {
  const [lastFix, setLastFix] = useState<Fix>();
  const [status, setStatus] = useState<GpsStatus>("asking");
  const [distance, setDistance] = useState<number>();
  const [watchStartedAt, setWatchStartedAt] = useState<number>();
  const [lastFixAt, setLastFixAt] = useState<number>();
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    if (!enabled || !node.location) return;
    let cancelled = false;
    let sub: Watch | undefined;
    (async () => {
      try {
        const services = await Location.hasServicesEnabledAsync();
        const { granted } = await Location.requestForegroundPermissionsAsync();
        if (cancelled) return;
        if (!granted) return setStatus("denied");
        if (!services) return setStatus("unavailable");
        setStatus("watching");
        setWatchStartedAt(Date.now());
        sub = await watchPosition({ accuracy: "high", distanceInterval: 5 }, (fix) => {
          setLastFixAt(Date.now());
          setLastFix(fix);
          onFix?.(fix);
          setDistance(distanceM(fix, node.location!));
          if (isInside(fix, node)) onArrive(fix);
        });
        if (cancelled) sub.remove();
      } catch {
        if (!cancelled) setStatus("unavailable");
      }
    })();
    return () => {
      cancelled = true;
      sub?.remove();
    };
    // onArrive cambia en cada render; el nodo y `enabled` son los que importan.
  }, [node, enabled]);

  // Reloj para el temporizador del fallback.
  useEffect(() => {
    if (!enabled) return;
    const timer = setInterval(() => setNow(Date.now()), 5000);
    return () => clearInterval(timer);
  }, [enabled]);

  return { status, distance, lastFix, manualFallback: offerManualArrival({ status, watchStartedAt, lastFixAt, now }) };
}
