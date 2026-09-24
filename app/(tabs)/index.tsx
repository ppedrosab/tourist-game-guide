import { router } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Button3D, Chip, HardShadow, Icon } from "@/components/ui";
import { findRoute, getCatalog } from "@/engine/catalog";
import { runProgress } from "@/engine/outline";
import { useI18n } from "@/i18n";
import { useActiveRun, useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

export default function Explorar() {
  const { t, L } = useI18n();
  const cityStatus = (free: number, routes: number) =>
    free > 0
      ? free === 1
        ? t("explorar.rutaGratis")
        : t("explorar.rutasGratis", { n: free })
      : routes === 1
        ? t("explorar.ruta")
        : t("explorar.rutas", { n: routes });
  const { packs } = getCatalog();
  const clues = useProgress((s) => s.collection.clueIds.length);
  const lastRouteId = useProgress((s) => s.lastRouteId);
  const active = useActiveRun(lastRouteId);
  const found = active ? findRoute(active.routeId) : undefined;
  const progress = found && active ? runProgress(found.route, active) : undefined;

  return (
    <Screen withTabBar>
      <View style={styles.header}>
        <View style={{ flex: 1 }}>
          <Text style={type.secondary}>{t("explorar.hola")}</Text>
          <Text style={type.title}>{t("explorar.detective")}</Text>
        </View>
        <Chip label={clues === 1 ? t("explorar.pista") : t("explorar.pistas", { n: clues })} icon="book" />
      </View>

      {/* Continuar: lleva a la parada exacta donde se quedó el jugador. */}
      {found && progress ? (
        <HardShadow radius={radius.xl}>
          <View style={styles.continueCard}>
            <Chip label={t("explorar.enCurso")} variant="clay" />
            <Text style={[type.subtitle, { color: colors.white }]}>{L(found.route.title)}</Text>
            <View style={styles.progressRow}>
              <View style={styles.progressTrack}>
                <View style={[styles.progressFill, { width: `${Math.round((progress.stop / progress.total) * 100)}%` }]} />
              </View>
              <Text style={styles.progressText}>{t("comun.paradaDe", { n: progress.stop, total: progress.total })}</Text>
            </View>
            <Text style={styles.progressText}>{L(progress.node.title)}</Text>
            <Button3D
              label={t("comun.continuar")}
              icon="play"
              onPress={() => router.push(`/ruta/${found.route.id}/jugar`)}
            />
          </View>
        </HardShadow>
      ) : null}

      <View style={styles.sectionHeader}>
        <Text style={type.subtitle}>{t("explorar.ciudades")}</Text>
        <Text style={type.caption}>{t("explorar.masPronto")}</Text>
      </View>
      <View style={{ gap: 12 }}>
        {packs.map((pack) => (
          <Pressable
            key={pack.id}
            onPress={() => router.push(`/ciudad/${pack.id}`)}
            accessibilityRole="button"
            accessibilityLabel={L(pack.name)}
          >
            <View style={styles.cityRow}>
              <Text style={[type.label, { flex: 1, fontSize: 17 }]}>{L(pack.name)}</Text>
              <Text style={[type.caption, { color: colors.clay, fontFamily: fonts.bold }]}>
                {cityStatus(pack.routes.filter((r) => r.isFree).length, pack.routes.length)}
              </Text>
              <Icon name="next" size={18} />
            </View>
          </Pressable>
        ))}
      </View>
      <Button3D label={t("explorar.verBienvenida")} variant="ghost" onPress={() => router.push("/bienvenida")} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { flexDirection: "row", alignItems: "center", gap: 12 },
  continueCard: {
    gap: 10,
    padding: 16,
    borderRadius: radius.xl,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  progressRow: { flexDirection: "row", alignItems: "center", gap: 10 },
  progressTrack: { flex: 1, height: 6, borderRadius: 3, backgroundColor: "#3C4B5B" },
  progressFill: { height: 6, borderRadius: 3, backgroundColor: colors.peach },
  progressText: { fontFamily: fonts.medium, fontSize: 12, color: "#C9D1D9" },
  sectionHeader: { flexDirection: "row", alignItems: "baseline", justifyContent: "space-between" },
  cityRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    padding: 16,
    borderRadius: radius.lg,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
});
