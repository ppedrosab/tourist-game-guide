import { router } from "expo-router";
import { Share, StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip } from "@/components/ui";
import { getCatalog } from "@/engine/catalog";
import { fieldExport, fieldReport, StopReport } from "@/field/analysis";
import { useFieldTest } from "@/field/store";
import { StringKey, useI18n } from "@/i18n";
import { border, colors, radius, type } from "@/theme";

const WARNING_KEYS: Record<StopReport["warnings"][number], StringKey> = {
  pocas_muestras: "campo.avisoPocas",
  coordenada_desplazada: "campo.avisoDesplazada",
  gps_impreciso: "campo.avisoImpreciso",
  llegadas_manuales: "campo.avisoManual",
};

/**
 * Informe de la prueba de campo: por parada, cómo se detectaron las llegadas
 * y qué coordenada y radio convendría poner en el pack. Se exporta como JSON.
 */
export default function Campo() {
  const { t, L, distance, number } = useI18n();
  const log = useFieldTest((s) => s.log);
  const clear = useFieldTest((s) => s.clear);
  const routes = getCatalog().packs.flatMap((p) => p.routes);

  const exportar = () => {
    const data = routes.map((r) => fieldExport(r, log));
    Share.share({ title: t("campo.titulo"), message: JSON.stringify(data, null, 2) });
  };

  return (
    <Screen>
      <TopBar title={t("campo.titulo")} onBack={() => router.back()} />
      <Text style={type.caption}>{t("campo.registros", { n: log.length })}</Text>
      {log.length === 0 ? <Text style={type.secondary}>{t("campo.vacio")}</Text> : null}
      {routes.map((route) => (
        <View key={route.id} style={{ gap: 10 }}>
          <Text style={type.subtitle}>{L(route.title)}</Text>
          {fieldReport(route, log).map((s) => (
            <View key={s.nodeId} style={styles.card}>
              <Text style={type.label}>{L(route.nodes.find((n) => n.id === s.nodeId)!.title)}</Text>
              <Text style={type.caption}>
                {t("campo.llegadas", { n: s.arrivals })} · {t("campo.metodos", s.byMethod)}
              </Text>
              {s.medianDistanceM !== undefined ? (
                <Text style={type.caption}>{t("campo.distancia", { value: distance(s.medianDistanceM) })}</Text>
              ) : null}
              {s.medianAccuracyM !== undefined ? (
                <Text style={type.caption}>{t("campo.precision", { value: Math.round(s.medianAccuracyM) })}</Text>
              ) : null}
              {s.medianWaitS !== undefined ? (
                <Text style={type.caption}>{t("campo.espera", { value: number(s.medianWaitS / 60, 1) })}</Text>
              ) : null}
              {s.suggestedLocation ? (
                <Text style={type.caption}>
                  {t("campo.sugerida", {
                    lat: s.suggestedLocation.lat.toFixed(5),
                    lng: s.suggestedLocation.lng.toFixed(5),
                    offset: Math.round(s.offsetM ?? 0),
                  })}
                </Text>
              ) : null}
              {s.suggestedRadiusM !== undefined ? (
                <Text style={type.caption}>{t("campo.radio", { current: s.radiusM, suggested: s.suggestedRadiusM })}</Text>
              ) : null}
              {s.warnings.length > 0 ? (
                <View style={styles.chips}>
                  {s.warnings.map((w) => (
                    <Chip key={w} label={t(WARNING_KEYS[w])} variant="sand" />
                  ))}
                </View>
              ) : null}
            </View>
          ))}
        </View>
      ))}
      <Button3D label={t("campo.exportar")} icon="share" onPress={exportar} disabled={log.length === 0} />
      <Button3D label={t("campo.borrar")} variant="ghost" onPress={clear} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  card: {
    gap: 3,
    padding: 12,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 6, marginTop: 4 },
});
