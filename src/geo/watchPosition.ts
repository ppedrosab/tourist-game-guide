import * as Location from "expo-location";

export type Fix = { lat: number; lng: number; accuracy: number | null };
export type Watch = { remove: () => void };

/** Vigila la posición (nativo: expo-location). Ver watchPosition.web.ts. */
export async function watchPosition(
  options: { accuracy: "high" | "balanced"; distanceInterval: number },
  onFix: (fix: Fix) => void,
): Promise<Watch> {
  return Location.watchPositionAsync(
    {
      accuracy: options.accuracy === "high" ? Location.Accuracy.High : Location.Accuracy.Balanced,
      distanceInterval: options.distanceInterval,
      timeInterval: 3000,
    },
    ({ coords }) => onFix({ lat: coords.latitude, lng: coords.longitude, accuracy: coords.accuracy }),
  );
}
