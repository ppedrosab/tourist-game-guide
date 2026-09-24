import * as Location from "expo-location";
import { useEffect, useState } from "react";
import type { StoryNode } from "@/content/types";
import { distanceM, GpsStatus, isInside, offerManualArrival } from "@/engine/geo";

/**
 * expo-location 19 en web llama a `LocationEventEmitter.removeSubscription`,
 * que no existe en el EventEmitter web, y lanza al quitar la última
 * suscripción. En nativo no pasa; en web el watch ya se ha cancelado antes.
 */
function stopWatch(sub: Location.LocationSubscription | undefined) {
  try {
    sub?.remove();
  } catch {
    // Solo web: ver comentario de arriba.
  }
}

export type ArrivalWatch = {
  status: GpsStatus;
  /** Metros hasta la parada según la última posición, si la hay. */
  distance?: number;
  /** Mostrar "Ya estoy aquí": sin permiso, sin GPS o 60 s sin posición. */
  manualFallback: boolean;
};

/**
 * Vigila la posición en primer plano mientras la escena espera la llegada a
 * `node`. Al entrar en su radio llama a `onArrive`. Los geofences en segundo
 * plano (src/geo/background.ts) cubren el caso de la app cerrada.
 */
export function useArrivalWatcher(node: StoryNode, enabled: boolean, onArrive: () => void): ArrivalWatch {
  const [status, setStatus] = useState<GpsStatus>("asking");
  const [distance, setDistance] = useState<number>();
  const [watchStartedAt, setWatchStartedAt] = useState<number>();
  const [lastFixAt, setLastFixAt] = useState<number>();
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    if (!enabled || !node.location) return;
    let cancelled = false;
    let sub: Location.LocationSubscription | undefined;
    (async () => {
      try {
        const services = await Location.hasServicesEnabledAsync();
        const { granted } = await Location.requestForegroundPermissionsAsync();
        if (cancelled) return;
        if (!granted) return setStatus("denied");
        if (!services) return setStatus("unavailable");
        setStatus("watching");
        setWatchStartedAt(Date.now());
        sub = await Location.watchPositionAsync(
          { accuracy: Location.Accuracy.High, distanceInterval: 5, timeInterval: 3000 },
          ({ coords }) => {
            const fix = { lat: coords.latitude, lng: coords.longitude, accuracy: coords.accuracy };
            setLastFixAt(Date.now());
            setDistance(distanceM(fix, node.location!));
            if (isInside(fix, node)) onArrive();
          },
        );
        if (cancelled) stopWatch(sub);
      } catch {
        if (!cancelled) setStatus("unavailable");
      }
    })();
    return () => {
      cancelled = true;
      stopWatch(sub);
    };
    // onArrive cambia en cada render; el nodo y `enabled` son los que importan.
  }, [node, enabled]);

  // Reloj para el temporizador del fallback.
  useEffect(() => {
    if (!enabled) return;
    const timer = setInterval(() => setNow(Date.now()), 5000);
    return () => clearInterval(timer);
  }, [enabled]);

  return { status, distance, manualFallback: offerManualArrival({ status, watchStartedAt, lastFixAt, now }) };
}
