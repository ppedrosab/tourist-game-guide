import { router, useLocalSearchParams } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip, Panel, ThemeBadge } from "@/components/ui";
import { findRoute } from "@/engine/catalog";
import { routeFacts, routeOutline } from "@/engine/outline";
import { useI18n } from "@/i18n";
import { routeMapData } from "@/map/geometry";
import { OfflineMapCard } from "@/map/OfflineMapCard";
import { RouteMap } from "@/map/RouteMap";
import { useActiveRun, useProgress } from "@/store/progress";
import { border, branchColors, colors, fonts, type } from "@/theme";

export default function DetalleRuta() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const found = findRoute(id);
  const active = useActiveRun(id);
  const start = useProgress((s) => s.start);
  const { t, L, number } = useI18n();

  if (!found) {
    return (
      <Screen>
        <TopBar title={t("ruta.noEncontrada")} onBack={() => router.back()} />
      </Screen>
    );
  }
  const { pack, route } = found;
  const facts = routeFacts(route);
  const outline = routeOutline(route);
  // Mismos números de parada que el mapa (las ramas paralelas comparten número).
  const stopNumber = new Map(routeMapData(route).stops.map((s) => [s.id, s.order]));
  const play = () => router.push(`/ruta/${route.id}/jugar`);
  const startFresh = () => {
    start(pack.id, route);
    play();
  };

  return (
    <Screen>
      <TopBar title={L(route.title)} onBack={() => router.back()} />
      <View style={styles.chips}>
        <ThemeBadge route={route} />
        <Chip label={t("comun.minutos", { n: route.durationMin })} icon="clock" />
        <Chip label={`${number(route.distanceKm, 1)} km`} icon="walk" />
        {facts.branches > 0 ? <Chip label={t("comun.caminos", { n: facts.branches })} icon="split" /> : null}
        {facts.endings > 0 ? <Chip label={t("comun.finales", { n: facts.endings })} icon="star" /> : null}
      </View>
      <Text style={type.body}>{L(route.summary)}</Text>
      <RouteMap route={route} run={active} height={230} />
      <OfflineMapCard pack={pack} />
      <Panel>
        {outline.map((item, i) =>
          item.kind === "stop" ? (
            <View key={item.node.id} style={styles.stop}>
              <View style={[styles.num, { backgroundColor: item.decision ? colors.clay : colors.ink }]}>
                <Text style={styles.numText}>{stopNumber.get(item.node.id)}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={type.label}>{L(item.node.title)}</Text>
                {item.decision ? <Text style={type.caption}>{t("ruta.decision", { n: item.decision })}</Text> : null}
              </View>
            </View>
          ) : (
            <View key={`ramas-${i}`} style={styles.branches}>
              {item.branches
                .filter((b) => b.nodes.length > 0)
                .map((b) => (
                  <View key={b.nodes[0].id} style={styles.branch}>
                    <View style={[styles.dot, { backgroundColor: branchColors[b.branch ?? "comun"] }]} />
                    <Text style={[type.caption, { flex: 1, color: colors.ink }]}>
                      {b.nodes.map((node) => `${stopNumber.get(node.id)} · ${L(node.title)}`).join("  →  ")}
                    </Text>
                  </View>
                ))}
            </View>
          ),
        )}
      </Panel>
      <View style={styles.actions}>
        <View style={{ flex: 1 }}>
          {active ? (
            <Button3D label={t("comun.continuar")} icon="play" onPress={play} />
          ) : (
            <Button3D label={t("ruta.comenzar")} icon="play" onPress={startFresh} />
          )}
        </View>
      </View>
      {active ? <Button3D label={t("ruta.deNuevo")} variant="ghost" onPress={startFresh} /> : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
  stop: { flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 4 },
  num: {
    width: 30,
    height: 30,
    borderRadius: 10,
    borderWidth: border.thin,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  numText: { fontFamily: fonts.bold, fontSize: 12, color: colors.white },
  branches: { gap: 6, paddingLeft: 42, paddingVertical: 6 },
  branch: { flexDirection: "row", alignItems: "center", gap: 8 },
  dot: { width: 10, height: 10, borderRadius: 5, borderWidth: border.thin, borderColor: colors.ink },
  actions: { flexDirection: "row", alignItems: "flex-start", gap: 10 },
});
