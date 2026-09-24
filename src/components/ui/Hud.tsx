import { StyleSheet, View } from "react-native";
import { border, Branch, branchColors, colors, hardShadow, radius, size } from "@/theme";
import { HardShadow } from "./HardShadow";
import { IconButton } from "./IconButton";

export type HudStop = { id: string; branch?: Branch };
type Props = {
  stops: HudStop[];
  current: number;
  clues: number;
  onPause: () => void;
  onNotebook: () => void;
};

/** HUD de la ruta: pausa · progreso por paradas · cuaderno con contador de pistas. */
export function Hud({ stops, current, clues, onPause, onNotebook }: Props) {
  return (
    <View style={styles.row}>
      <IconButton icon="pause" label="Pausa" onPress={onPause} />
      <View style={{ flex: 1 }}>
        <HardShadow radius={radius.md} offset={hardShadow.sm}>
          <View
            style={styles.track}
            accessible
            accessibilityLabel={`Parada ${current + 1} de ${stops.length}`}
          >
            {stops.map((stop, i) => {
              const color = stop.branch ? branchColors[stop.branch] : colors.ink;
              const done = i < current;
              const isCurrent = i === current;
              return (
                <View key={stop.id} style={styles.segment}>
                  <View
                    style={[
                      styles.dot,
                      isCurrent && styles.dotCurrent,
                      { backgroundColor: done ? color : isCurrent ? (stop.branch ? color : colors.clay) : colors.paper },
                    ]}
                  />
                  {i < stops.length - 1 ? (
                    <View style={[styles.line, { backgroundColor: done ? colors.ink : colors.line }]} />
                  ) : null}
                </View>
              );
            })}
          </View>
        </HardShadow>
      </View>
      <IconButton icon="book" label="Cuaderno del detective" badge={clues} onPress={onNotebook} />
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "flex-start", gap: 10 },
  track: {
    height: size.iconButton,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    borderRadius: radius.md,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.paper,
  },
  segment: { flex: 1, flexDirection: "row", alignItems: "center" },
  dot: { width: 12, height: 12, borderRadius: 6, borderWidth: border.thin, borderColor: colors.ink },
  dotCurrent: { width: 22, height: 22, borderRadius: 11, borderWidth: border.base },
  line: { flex: 1, height: 3, marginHorizontal: 3, borderRadius: 2 },
});
