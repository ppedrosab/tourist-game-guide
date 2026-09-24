import { StyleSheet, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Icon } from "@/components/ui";
import { border, colors, fonts, radius, type } from "@/theme";

const ENDINGS = [
  { title: "Detective de puerto", combo: "Dinero + documentos", unlocked: true },
  { title: "Alma marinera", combo: "Dinero + leyenda", unlocked: false },
  { title: "Detective de despacho", combo: "Poder + documentos", unlocked: false },
  { title: "Cuentacuentos", combo: "Poder + leyenda", unlocked: false },
];

export default function Coleccion() {
  return (
    <Screen withTabBar>
      <Text style={type.title}>Colección</Text>
      <Text style={type.subtitle}>El misterio de la Manquita</Text>
      <View style={styles.grid}>
        {ENDINGS.map((e) => (
          <View key={e.title} style={[styles.card, e.unlocked ? styles.unlocked : styles.locked]}>
            <Icon name={e.unlocked ? "star" : "lock"} color={e.unlocked ? colors.white : colors.muted} />
            <Text style={[styles.title, { color: e.unlocked ? colors.white : colors.muted }]}>
              {e.unlocked ? e.title : "???"}
            </Text>
            <Text style={[styles.combo, { color: e.unlocked ? colors.white : colors.muted }]}>{e.combo}</Text>
          </View>
        ))}
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  card: { width: "48%", gap: 6, padding: 12, borderRadius: radius.lg, borderWidth: border.base },
  unlocked: { backgroundColor: colors.clay, borderColor: colors.ink },
  locked: { backgroundColor: colors.sand, borderColor: "#B9A98C", borderStyle: "dashed" },
  title: { fontFamily: fonts.bold, fontSize: 14 },
  combo: { fontFamily: fonts.body, fontSize: 11 },
});
