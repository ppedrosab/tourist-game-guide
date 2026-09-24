import * as Location from "expo-location";
import * as Notifications from "expo-notifications";

/**
 * Pide los permisos en orden: ubicación mientras se usa → «siempre» (para los
 * geofences) → notificaciones. Negar cualquiera no bloquea: el juego sigue
 * con GPS en primer plano o con "Ya estoy aquí".
 */
export async function requestGamePermissions(): Promise<void> {
  try {
    const foreground = await Location.requestForegroundPermissionsAsync();
    if (foreground.granted) await Location.requestBackgroundPermissionsAsync();
    await Notifications.requestPermissionsAsync();
  } catch (e) {
    console.warn("[permisos]", e);
  }
}
