import { TurboModuleRegistry } from "react-native";

type MapLibreModule = typeof import("@maplibre/maplibre-react-native");

/**
 * MapLibre solo existe en builds con código nativo (desarrollo o tienda). En
 * Expo Go no está y la librería lanza al importarse, así que se carga bajo
 * demanda tras comprobar que el módulo nativo está registrado.
 */
function load(): MapLibreModule | undefined {
  if (!TurboModuleRegistry.get("MLRNOfflineModule")) return undefined;
  try {
    return require("@maplibre/maplibre-react-native") as MapLibreModule;
  } catch (e) {
    console.warn("[mapa] MapLibre no disponible", e);
    return undefined;
  }
}

export const MapLibre = load();
