import { useMemo } from "react";
import { StyleSheet } from "react-native";
import { branchColors, colors } from "@/theme";
import { MAP_LABEL_FONT, MAP_STYLE_URL } from "./config";
import { RouteMapData, toGeoJSON } from "./geometry";
import { MapLibre } from "./maplibre";

type Props = { data: RouteMapData; showUser: boolean };

// Colores por camino y estado como expresiones de estilo de MapLibre. Los tramos
// comunes van en arena (con contorno de tinta) para no confundirse con ningún camino.
const branchColor = ["match", ["get", "branch"], "dinero", branchColors.dinero, "poder", branchColors.poder, colors.sand];
const stopFill = [
  "match",
  ["get", "status"],
  "visited",
  branchColor,
  "current",
  colors.clay,
  "next",
  colors.gold,
  "other",
  colors.sand,
  colors.white,
];
const stopText = ["match", ["get", "status"], "visited", colors.white, "current", colors.white, "other", colors.muted, colors.ink];

/** Mapa real con MapLibre: callejero, tramos de los dos caminos y paradas numeradas. */
export function NativeRouteMap({ data, showUser }: Props) {
  const geojson = useMemo(() => toGeoJSON(data), [data]);
  if (!MapLibre) return null;
  const { Map, Camera, GeoJSONSource, Layer, UserLocation } = MapLibre;
  const [sw, ne] = data.bounds;
  return (
    <Map style={styles.map} mapStyle={MAP_STYLE_URL} attribution logo={false} compass={false} touchPitch={false}>
      <Camera initialViewState={{ bounds: [sw.lng, sw.lat, ne.lng, ne.lat], padding: { top: 60, right: 50, bottom: 60, left: 50 } }} />
      <GeoJSONSource id="ruta" data={geojson}>
        {/* Contorno de tinta bajo los tramos. */}
        <Layer
          id="tramos-contorno"
          type="line"
          filter={["==", ["get", "kind"], "segment"]}
          layout={{ "line-cap": "round", "line-join": "round" }}
          paint={{
            "line-color": colors.ink,
            "line-width": 9,
            "line-opacity": ["match", ["get", "status"], "other", 0.3, 1],
          }}
        />
        <Layer
          id="tramos"
          type="line"
          filter={["==", ["get", "kind"], "segment"]}
          layout={{ "line-cap": "round", "line-join": "round" }}
          paint={{
            "line-color": branchColor as never,
            "line-width": 5,
            "line-opacity": ["match", ["get", "status"], "other", 0.35, 1],
            // Discontinuo lo que queda por andar; continuo lo recorrido.
            "line-dasharray": ["match", ["get", "status"], "walked", ["literal", [1, 0]], ["literal", [0.4, 1.8]]],
          }}
        />
        <Layer
          id="paradas"
          type="circle"
          filter={["==", ["get", "kind"], "stop"]}
          paint={{
            "circle-radius": ["match", ["get", "status"], "current", 14, 11],
            "circle-color": stopFill as never,
            "circle-stroke-color": colors.ink,
            "circle-stroke-width": 2.5,
            "circle-opacity": ["match", ["get", "status"], "other", 0.5, 1],
            "circle-stroke-opacity": ["match", ["get", "status"], "other", 0.5, 1],
          }}
        />
        <Layer
          id="paradas-numero"
          type="symbol"
          filter={["==", ["get", "kind"], "stop"]}
          layout={{
            "text-field": ["to-string", ["get", "order"]],
            "text-font": MAP_LABEL_FONT,
            "text-size": 12,
            "text-allow-overlap": true,
            "text-ignore-placement": true,
          }}
          paint={{ "text-color": stopText as never }}
        />
      </GeoJSONSource>
      {showUser ? <UserLocation animated accuracy /> : null}
    </Map>
  );
}

const styles = StyleSheet.create({ map: { flex: 1 } });
