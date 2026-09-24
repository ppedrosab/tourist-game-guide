import { useMemo } from "react";
import { StyleSheet, View } from "react-native";
import type { LatLng, PlayerProgress, Route } from "@/content/types";
import { border, colors, radius } from "@/theme";
import { routeMapData } from "./geometry";
import { MapLibre } from "./maplibre";
import { NativeRouteMap } from "./NativeRouteMap";
import { SchematicMap } from "./SchematicMap";

type Props = {
  route: Route;
  run?: PlayerProgress;
  /** Posición del jugador (el mapa nativo usa la suya propia). */
  user?: LatLng;
  height?: number;
};

/** Mapa de la ruta: MapLibre si hay código nativo; si no (Expo Go, web), esquema SVG. */
export function RouteMap({ route, run, user, height }: Props) {
  const data = useMemo(() => routeMapData(route, run), [route, run]);
  return (
    <View style={[styles.frame, height ? { height } : styles.fill]} testID="mapa-ruta">
      {MapLibre ? <NativeRouteMap data={data} showUser={!!user} /> : <SchematicMap data={data} user={user} />}
    </View>
  );
}

/** Si el mapa es el callejero real (para avisar de la descarga offline). */
export const hasStreetMap = MapLibre !== undefined;

const styles = StyleSheet.create({
  frame: {
    overflow: "hidden",
    borderRadius: radius.lg,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.paper,
  },
  fill: { flex: 1 },
});
