import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Location from "expo-location";
import * as Notifications from "expo-notifications";
import * as TaskManager from "expo-task-manager";
import type { PlayerProgress, Route } from "@/content/types";
import { findRoute } from "@/engine/catalog";
import { geofenceRegions, parseRegionId, PendingArrival } from "@/engine/geo";
import { localize } from "@/engine/runner";
import { currentLang, translate } from "@/i18n";

/**
 * Geofences en segundo plano: el sistema despierta la app al entrar en una
 * parada aunque el móvil vaya en el bolsillo. La tarea no toca el store
 * (puede ejecutarse sin la interfaz cargada): apunta la llegada en
 * AsyncStorage y la app la aplica al volver a primer plano.
 *
 * Requiere build de desarrollo o de tienda: Expo Go en iOS no permite
 * ubicación en segundo plano. En web se usa background.ts (sin geofences).
 */
export const GEOFENCE_TASK = "geofences-ruta";
const PENDING_KEY = "llegadas-pendientes";

type GeofenceEvent = { eventType: Location.GeofencingEventType; region: Location.LocationRegion };

// La tarea debe definirse al cargar el módulo (se importa desde app/_layout.tsx).
TaskManager.defineTask<GeofenceEvent>(GEOFENCE_TASK, async ({ data, error }) => {
  if (error || !data || data.eventType !== Location.GeofencingEventType.Enter) return;
  const ids = data.region.identifier ? parseRegionId(data.region.identifier) : undefined;
  if (!ids) return;
  const pending = await readPending();
  pending.push({ ...ids, at: new Date().toISOString() });
  await AsyncStorage.setItem(PENDING_KEY, JSON.stringify(pending.slice(-20)));
  await notifyArrival(ids.routeId, ids.nodeId);
});

/** Aviso local "¡Has llegado!" con el nombre de la parada, si hay permiso de notificaciones. */
async function notifyArrival(routeId: string, nodeId: string) {
  try {
    const { granted } = await Notifications.getPermissionsAsync();
    const node = findRoute(routeId)?.route.nodes.find((n) => n.id === nodeId);
    if (!granted || !node) return;
    // El store puede no estar hidratado en segundo plano: entonces se usa el idioma del móvil.
    const lang = currentLang();
    await Notifications.scheduleNotificationAsync({
      content: {
        title: translate(lang, "avisos.llegada"),
        body: translate(lang, "avisos.llegadaTexto", { title: localize(node.title, lang) }),
      },
      trigger: null,
    });
  } catch {
    // Sin aviso no pasa nada: la llegada ya está apuntada.
  }
}

async function readPending(): Promise<PendingArrival[]> {
  try {
    const raw = await AsyncStorage.getItem(PENDING_KEY);
    return raw ? (JSON.parse(raw) as PendingArrival[]) : [];
  } catch {
    return [];
  }
}

/** Devuelve y borra las llegadas apuntadas por la tarea. */
export async function takePendingArrivals(): Promise<PendingArrival[]> {
  const pending = await readPending();
  if (pending.length > 0) await AsyncStorage.removeItem(PENDING_KEY);
  return pending;
}

/**
 * Registra los geofences de las siguientes paradas posibles (máx. 20) o los
 * quita si no hay partida. Solo actúa si ya hay permiso de ubicación
 * «siempre»; nunca lo pide (eso se hace en la pantalla de permisos).
 */
export async function syncGeofences(route: Route | undefined, run: PlayerProgress | undefined): Promise<void> {
  try {
    const regions = route && run ? geofenceRegions(route, run) : [];
    const started = await Location.hasStartedGeofencingAsync(GEOFENCE_TASK);
    if (regions.length === 0) {
      if (started) await Location.stopGeofencingAsync(GEOFENCE_TASK);
      return;
    }
    const { granted } = await Location.getBackgroundPermissionsAsync();
    if (!granted) return;
    // Volver a llamar sustituye las regiones vigiladas por las nuevas.
    await Location.startGeofencingAsync(GEOFENCE_TASK, regions);
  } catch (e) {
    console.warn("[geo] no se pudieron actualizar los geofences", e);
  }
}
