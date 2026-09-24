import { Pressable, StyleSheet, Text, View } from "react-native";
import { Icon } from "@/components/ui";
import type { CityPack } from "@/content/types";
import { useI18n } from "@/i18n";
import { border, colors, fonts, radius, type } from "@/theme";
import { formatBytes, offlinePlan } from "./offlinePlan";
import { useCityOffline } from "./useCityOffline";

/** Tarjeta "Mapa sin conexión" de una ciudad: descargar, progreso, borrar. */
export function OfflineMapCard({ pack }: { pack: CityPack }) {
  const { t, L, lang } = useI18n();
  const { state, download, remove } = useCityOffline(pack);
  const city = L(pack.name);
  const plan = offlinePlan(pack);

  let title = t("mapa.offlineDescargar", { city });
  let sub = t("mapa.offlineDescargarTexto", { size: formatBytes(plan.approxBytes, lang) });
  let action: (() => void) | undefined = download;
  let actionLabel = t("mapa.descargar");
  let progress: number | undefined;
  switch (state.kind) {
    case "unsupported":
      title = t("mapa.offlineTitulo");
      sub = t("mapa.offlineNoDisponible");
      action = undefined;
      break;
    case "checking":
      sub = t("mapa.offlineComprobando");
      action = undefined;
      break;
    case "downloading":
      title = t("mapa.offlineDescargando", { city });
      sub = `${Math.round(state.percentage)} % · ${formatBytes(state.bytes, lang)}`;
      progress = state.percentage / 100;
      action = undefined;
      break;
    case "complete":
      title = t("mapa.offlineListo", { city });
      sub = t("mapa.offlineDescargado", { size: formatBytes(state.bytes, lang) });
      action = remove;
      actionLabel = t("mapa.borrar");
      break;
    case "error":
      title = t("mapa.offlineError");
      sub = t("mapa.offlineErrorTexto");
      actionLabel = t("mapa.reintentar");
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
        <Pressable onPress={action} accessibilityRole="button" accessibilityLabel={`${actionLabel} · ${title}`} hitSlop={8}>
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
