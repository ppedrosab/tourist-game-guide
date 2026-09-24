import type { Fix, Watch } from "./watchPosition";

/**
 * Web: navigator.geolocation directamente. expo-location 19 en web confunde
 * sus identificadores de suscripción con los del navegador (la segunda
 * suscripción no recibe posiciones) y lanza al quitar la última.
 */
export async function watchPosition(
  options: { accuracy: "high" | "balanced"; distanceInterval: number },
  onFix: (fix: Fix) => void,
): Promise<Watch> {
  if (typeof navigator === "undefined" || !navigator.geolocation) return { remove: () => {} };
  let active = true;
  const report = ({ coords }: GeolocationPosition) => {
    if (active) onFix({ lat: coords.latitude, lng: coords.longitude, accuracy: coords.accuracy });
  };
  const opts = { enableHighAccuracy: options.accuracy === "high" };
  // Algunos navegadores no avisan a un segundo watch hasta que la posición cambia:
  // se pide la actual una vez para tener posición desde el principio.
  navigator.geolocation.getCurrentPosition(report, undefined, opts);
  const id = navigator.geolocation.watchPosition(report, undefined, opts);
  return {
    remove: () => {
      active = false;
      navigator.geolocation.clearWatch(id);
    },
  };
}
