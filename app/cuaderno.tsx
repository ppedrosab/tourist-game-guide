import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip, Icon } from "@/components/ui";
import { localize } from "@/engine/runner";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { branchColors, border, colors, fonts, radius, type } from "@/theme";

/** Cuaderno del detective (modal): pistas y objetos de la partida en curso. */
export default function Cuaderno() {
  const current = useCurrentRun();
  const close = () => router.back();

  if (!current) {
    return (
      <Screen>
        <TopBar title="Cuaderno del detective" onBack={close} closeIcon />
        <Text style={type.secondary}>Empieza una ruta para ir llenando el cuaderno.</Text>
      </Screen>
    );
  }

  const { route, run } = current;
  const clueNodes = route.nodes.filter((n) => n.clue);
  const objects = (route.rewards ?? []).filter((r) => run.collectibleIds.includes(r.id));
  const chosenBranch = run.visitedNodeIds.map((id) => route.nodes.find((n) => n.id === id)?.branch).find(Boolean);

  return (
    <Screen>
      <TopBar title="Cuaderno del detective" onBack={close} closeIcon />
      <Text style={type.overline}>Pistas</Text>
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
                <Text style={[styles.where, { color }]}>{localize(node.title)}</Text>
                <Text style={type.body}>{localize(clue.text)}</Text>
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
              {otherBranch ? `${localize(node.title)} · otro camino` : "Pista por descubrir"}
            </Text>
          </View>
        );
      })}
      {objects.length > 0 ? (
        <>
          <Text style={type.overline}>Objetos</Text>
          <View style={styles.chips}>
            {objects.map((r) => (
              <Chip key={r.id} label={localize(r.name)} icon="trophy" variant="sand" />
            ))}
          </View>
        </>
      ) : null}
      <Button3D label="Ver mapa" icon="map" variant="secondary" onPress={() => router.replace("/mapa")} />
      <Button3D label="Volver" onPress={close} />
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
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
});
