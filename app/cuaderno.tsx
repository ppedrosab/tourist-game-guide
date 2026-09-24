import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Icon } from "@/components/ui";
import { Branch, branchColors, border, colors, fonts, radius, type } from "@/theme";

const CLUES: { where: string; text: string; branch: Branch; found: boolean }[] = [
  { where: "Calle Larios", text: "Sin caminos no hay comercio.", branch: "comun", found: true },
  { where: "Atarazanas", text: "El dinero de Málaga entraba por el mar y salía por los caminos.", branch: "dinero", found: true },
  { where: "Plaza de la Constitución", text: "", branch: "poder", found: false },
];

/** Cuaderno del detective (modal). Fase 2: las pistas salen del progreso del jugador. */
export default function Cuaderno() {
  return (
    <Screen>
      <TopBar title="Cuaderno del detective" onBack={() => router.back()} closeIcon />
      {CLUES.map((c) =>
        c.found ? (
          <View key={c.where} style={styles.clue}>
            <View style={[styles.medal, { backgroundColor: branchColors[c.branch] }]}>
              <Icon name="search" size={16} color={colors.white} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={[styles.where, { color: branchColors[c.branch] }]}>{c.where}</Text>
              <Text style={type.body}>{c.text}</Text>
            </View>
          </View>
        ) : (
          <View key={c.where} style={[styles.clue, styles.locked]}>
            <Icon name="lock" size={16} color={colors.muted} />
            <Text style={type.secondary}>{c.where} · otro camino</Text>
          </View>
        ),
      )}
      <Button3D label="Volver" icon="map" onPress={() => router.back()} />
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
  locked: { borderStyle: "dashed", borderColor: "#B9A98C", backgroundColor: "transparent" },
  medal: { width: 34, height: 34, borderRadius: 10, borderWidth: border.thin, borderColor: colors.ink, alignItems: "center", justifyContent: "center" },
  where: { fontFamily: fonts.bold, fontSize: 12 },
});
