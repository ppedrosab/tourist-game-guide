import * as Location from "expo-location";

/** Web: solo ubicación en primer plano (sin segundo plano ni notificaciones). */
export async function requestGamePermissions(): Promise<void> {
  try {
    await Location.requestForegroundPermissionsAsync();
  } catch (e) {
    console.warn("[permisos]", e);
  }
}
