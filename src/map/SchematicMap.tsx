import { useState } from "react";
import { LayoutChangeEvent, StyleSheet, View } from "react-native";
import Svg, { Circle, G, Polyline, Rect, Text as SvgText } from "react-native-svg";
import type { LatLng } from "@/content/types";
import { useI18n } from "@/i18n";
import { branchColors, colors, fonts } from "@/theme";
import { MapStop, projector, RouteMapData, SegmentStatus, StopStatus } from "./geometry";

type Props = { data: RouteMapData; user?: LatLng };

const PADDING = 30;

/**
 * Mapa esquemático en SVG (Expo Go, web y reserva si MapLibre no carga): las
 * paradas en su posición real, unidas por los tramos de cada camino con su
 * color, sin callejero.
 */
export function SchematicMap({ data, user }: Props) {
  const { t } = useI18n();
  const [size, setSize] = useState({ width: 0, height: 0 });
  const onLayout = (e: LayoutChangeEvent) => setSize(e.nativeEvent.layout);
  const { width, height } = size;
  const project = projector(data.bounds, width, height, PADDING);
  const me = user ? project(user) : undefined;
  const meInside = me && me.x >= 0 && me.x <= width && me.y >= 0 && me.y <= height;

  return (
    <View style={styles.root} onLayout={onLayout} accessibilityLabel={t("mapa.esquema")}>
      {width > 0 ? (
        <Svg width={width} height={height}>
          <Rect width={width} height={height} fill={colors.paper} />
          {/* Contorno de tinta bajo los tramos, como el resto del juego. */}
          {data.segments.map((s) => {
            const points = s.coordinates.map((c) => project(c)).map((p) => `${p.x},${p.y}`).join(" ");
            return (
              <G key={s.id} opacity={s.status === "other" ? 0.35 : 1}>
                <Polyline points={points} fill="none" stroke={colors.ink} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
                <Polyline
                  points={points}
                  fill="none"
                  stroke={s.branch ? branchColors[s.branch] : colors.sand}
                  strokeWidth={5}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeDasharray={dash(s.status)}
                />
              </G>
            );
          })}
          {data.stops.map((s) => {
            const p = project(s.location);
            const r = s.status === "current" ? 14 : 11;
            const style = stopStyle(s);
            return (
              <G key={s.id} opacity={s.status === "other" ? 0.45 : 1}>
                <Circle cx={p.x} cy={p.y + 2.5} r={r} fill={colors.ink} />
                <Circle cx={p.x} cy={p.y} r={r} fill={style.fill} stroke={colors.ink} strokeWidth={2.5} />
                <SvgText
                  x={p.x}
                  y={p.y + 4.5}
                  fontSize={12}
                  fontFamily={fonts.bold}
                  fontWeight="700"
                  fill={style.text}
                  textAnchor="middle"
                >
                  {s.order}
                </SvgText>
              </G>
            );
          })}
          {me && meInside ? (
            <G>
              <Circle cx={me.x} cy={me.y} r={14} fill={colors.sea} opacity={0.2} />
              <Circle cx={me.x} cy={me.y} r={7} fill={colors.sea} stroke={colors.white} strokeWidth={2.5} />
            </G>
          ) : null}
        </Svg>
      ) : null}
    </View>
  );
}

const dash = (status: SegmentStatus) => (status === "walked" ? undefined : "2 9");

function stopStyle(s: MapStop): { fill: string; text: string } {
  const branch = branchColors[s.branch ?? "comun"];
  const map: Record<StopStatus, { fill: string; text: string }> = {
    visited: { fill: branch, text: colors.white },
    current: { fill: colors.clay, text: colors.white },
    next: { fill: colors.gold, text: colors.ink },
    pending: { fill: colors.white, text: colors.ink },
    other: { fill: colors.sand, text: colors.muted },
  };
  return map[s.status];
}

const styles = StyleSheet.create({ root: { flex: 1, overflow: "hidden" } });
