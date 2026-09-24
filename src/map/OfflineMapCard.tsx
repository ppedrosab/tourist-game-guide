import { Pressable, StyleSheet, Text, View } from "react-native";
import { Icon } from "@/components/ui";
import type { CityPack } from "@/content/types";
import { localize } from "@/engine/runner";
import { border, colors, fonts, radius, type } from "@/theme";
import { formatBytes, offlinePlan } from "./offlinePlan";
import { useCityOffline } from "./useCityOffline";

/** Tarjeta "Mapa sin conexión" de una ciudad: descargar, progreso, borrar. */
export function OfflineMapCard({ pack }: { pack: CityPack }) {
  const { state, download, remove } = useCityOffline(pack);
  const city = localize(pack.name);
  const plan = offlinePlan(pack);

  let title = `Descargar el mapa de ${city}`;
  let sub = `Para jugar sin datos · ≈ ${formatBytes(plan.approxBytes)}`;
  let action: (() => void) | undefined = download;
  let actionLabel = "Descargar";
  let progress: number | undefined;
  switch (state.kind) {
    case "unsupported":
      title = "Mapa sin conexión";
      sub = "En esta versión el mapa es un esquema que ya funciona sin datos. El callejero descargable llega con la app instalada.";
      action = undefined;
      break;
    case "checking":
      sub = "Comprobando…";
      action = undefined;
      break;
    case "downloading":
      title = `Descargando el mapa de ${city}`;
      sub = `${Math.round(state.percentage)} % · ${formatBytes(state.bytes)}`;
      progress = state.percentage / 100;
      action = undefined;
      break;
    case "complete":
      title = `Mapa de ${city} sin conexión`;
      sub = `Descargado · ${formatBytes(state.bytes)}`;
      action = remove;
      actionLabel = "Borrar";
      break;
    case "error":
      title = "No se pudo descargar el mapa";
      sub = "Revisa la conexión e inténtalo de nuevo.";
      actionLabel = "Reintentar";
      break;
  }

  return (
    <View style={styles.card} accessibilityLiveRegion="polite">
      <View style={styles.icon}>
        <Icon name={state.kind === "complete" ? "check" : "download"} size={20} color={colors.white} />
      </View>
      <View style={{ flex: 1, gap: 2 }}>
        <Text style={type.label}>{title}</Text>
        <Text style={type.caption}>{sub}</Text>
        {progress !== undefined ? (
          <View style={styles.track}>
            <View style={[styles.fill, { width: `${Math.round(progress * 100)}%` }]} />
          </View>
        ) : null}
      </View>
      {action ? (
        <Pressable onPress={action} accessibilityRole="button" accessibilityLabel={`${actionLabel} mapa de ${city}`} hitSlop={8}>
          <Text style={styles.action}>{actionLabel}</Text>
        </Pressable>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    padding: 12,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  icon: {
    width: 38,
    height: 38,
    borderRadius: 11,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.sea,
    alignItems: "center",
    justifyContent: "center",
  },
  track: { height: 5, borderRadius: 3, backgroundColor: colors.sand, overflow: "hidden", marginTop: 4 },
  fill: { height: 5, borderRadius: 3, backgroundColor: colors.sea },
  action: { fontFamily: fonts.bold, fontSize: 14, color: colors.clay, paddingVertical: 12 },
});
