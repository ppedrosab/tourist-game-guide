import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { CastList } from "@/components/game/CastList";
import { CollectibleArt } from "@/components/game/CollectibleArt";
import { routeCast } from "@/engine/outline";
import { Button3D, Icon } from "@/components/ui";
import { useI18n } from "@/i18n";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { branchColors, border, colors, fonts, radius, type } from "@/theme";

/** Cuaderno del detective (modal): pistas y objetos de la partida en curso. */
export default function Cuaderno() {
  const { t, L } = useI18n();
  const current = useCurrentRun();
  const close = () => router.back();

  if (!current) {
    return (
      <Screen>
        <TopBar title={t("jugar.cuaderno")} onBack={close} closeIcon />
        <Text style={type.secondary}>{t("cuaderno.vacio")}</Text>
      </Screen>
    );
  }

  const { pack, route, run } = current;
  const clueNodes = route.nodes.filter((n) => n.clue);
  const objects = (route.rewards ?? []).filter((r) => run.collectibleIds.includes(r.id));
  const chosenBranch = run.visitedNodeIds.map((id) => route.nodes.find((n) => n.id === id)?.branch).find(Boolean);

  return (
    <Screen>
      <TopBar title={t("jugar.cuaderno")} onBack={close} closeIcon />
      <Text style={type.overline}>{t("cuaderno.pistas")}</Text>
      {clueNodes.map((node) => {
        const clue = node.clue!;
        const color = branchColors[node.branch ?? "comun"];
        if (run.clueIds.includes(clue.id)) {
          return (
            <View key={clue.id} style={styles.clue}>
              <View style={[styles.medal, { backgroundColor: color }]}>
                <Icon name="search" size={16} color={colors.white} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={[styles.where, { color }]}>{L(node.title)}</Text>
                <Text style={type.body}>{L(clue.text)}</Text>
              </View>
            </View>
          );
        }
        // Pistas de la otra rama: se ven bloqueadas para invitar a rejugar.
        const otherBranch = node.branch && chosenBranch && node.branch !== chosenBranch;
        return (
          <View key={clue.id} style={[styles.clue, styles.locked]}>
            <Icon name="lock" size={16} color={colors.muted} />
            <Text style={type.secondary}>
              {otherBranch ? t("cuaderno.otroCamino", { title: L(node.title) }) : t("cuaderno.porDescubrir")}
            </Text>
          </View>
        );
      })}
      {objects.length > 0 ? (
        <>
          <Text style={type.overline}>{t("cuaderno.objetos")}</Text>
          <View style={styles.chips}>
            {objects.map((r) => (
              <View key={r.id} style={styles.object} accessible accessibilityLabel={L(r.name)}>
                <CollectibleArt icon={r.icon} size={64} />
                <Text style={[type.caption, { textAlign: "center", color: colors.ink }]}>{L(r.name)}</Text>
              </View>
            ))}
          </View>
        </>
      ) : null}
      <Text style={type.overline}>{t("cuaderno.personajes")}</Text>
      <CastList route={route} cast={routeCast(pack, route, [...run.visitedNodeIds, run.currentNodeId])} />
      <Button3D label={t("pausa.verMapa")} icon="map" variant="secondary" onPress={() => router.replace("/mapa")} />
      <Button3D label={t("comun.volver")} onPress={close} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  clue: {
    flexDirection: "row",
    gap: 12,
    padding: 12,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
    alignItems: "center",
  },
  locked: { borderStyle: "dashed", borderColor: colors.line, backgroundColor: "transparent" },
  medal: { width: 34, height: 34, borderRadius: 10, borderWidth: border.thin, borderColor: colors.ink, alignItems: "center", justifyContent: "center" },
  where: { fontFamily: fonts.bold, fontSize: 12 },
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  object: { width: 90, alignItems: "center", gap: 4 },
});
