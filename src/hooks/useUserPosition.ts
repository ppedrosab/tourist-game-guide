import * as Location from "expo-location";
import { useEffect, useState } from "react";
import type { LatLng } from "@/content/types";
import { Watch, watchPosition } from "@/geo/watchPosition";

/**
 * Posición del jugador para el mapa. Pide el permiso si aún no se ha decidido
 * (si ya se concedió o se denegó, el sistema no vuelve a preguntar).
 */
export function useUserPosition(active: boolean): LatLng | undefined {
  const [pos, setPos] = useState<LatLng>();
  useEffect(() => {
    if (!active) return;
    let cancelled = false;
    let sub: Watch | undefined;
    (async () => {
      try {
        const { granted } = await Location.requestForegroundPermissionsAsync();
        if (!granted || cancelled) return;
        sub = await watchPosition({ accuracy: "high", distanceInterval: 10 }, ({ lat, lng }) =>
          setPos({ lat, lng }),
        );
        if (cancelled) sub.remove();
      } catch {
        // Sin posición el mapa se muestra igual.
      }
    })();
    return () => {
      cancelled = true;
      sub?.remove();
    };
  }, [active]);
  return pos;
}
