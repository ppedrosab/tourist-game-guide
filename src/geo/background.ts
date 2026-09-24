import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Location from "expo-location";
import * as TaskManager from "expo-task-manager";
import { Platform } from "react-native";
import type { PlayerProgress, Route } from "@/content/types";
import { geofenceRegions, parseRegionId, PendingArrival } from "@/engine/geo";

/**
 * Geofences en segundo plano: el sistema despierta la app al entrar en una
 * parada aunque el móvil vaya en el bolsillo. La tarea no toca el store
 * (puede ejecutarse sin la interfaz cargada): apunta la llegada en
 * AsyncStorage y la app la aplica al volver a primer plano.
 *
 * Requiere build de desarrollo o de tienda: Expo Go en iOS no permite
 * ubicación en segundo plano. En web no hay geofences.
 */
export const GEOFENCE_TASK = "geofences-ruta";
const PENDING_KEY = "llegadas-pendientes";

const supported = Platform.OS === "ios" || Platform.OS === "android";

type GeofenceEvent = { eventType: Location.GeofencingEventType; region: Location.LocationRegion };

// La tarea debe definirse al cargar el módulo (se importa desde app/_layout.tsx).
if (supported) {
  TaskManager.defineTask<GeofenceEvent>(GEOFENCE_TASK, async ({ data, error }) => {
    if (error || !data || data.eventType !== Location.GeofencingEventType.Enter) return;
    const ids = data.region.identifier ? parseRegionId(data.region.identifier) : undefined;
    if (!ids) return;
    const pending = await readPending();
    pending.push({ ...ids, at: new Date().toISOString() });
    await AsyncStorage.setItem(PENDING_KEY, JSON.stringify(pending.slice(-20)));
  });
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
  if (!supported) return;
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
