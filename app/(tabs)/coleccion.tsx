import { StyleSheet, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Icon } from "@/components/ui";
import type { Route } from "@/content/types";
import { getCatalog } from "@/engine/catalog";
import { localize } from "@/engine/runner";
import { useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

/** Combinación de decisiones que lleva a un final, con las etiquetas de las opciones del pack. */
function endingCombo(route: Route, requires: string[]): string {
  const labels = requires.map((flag) => {
    const choice = route.nodes.flatMap((n) => n.choices ?? []).find((c) => c.setFlags?.includes(flag));
    return choice ? localize(choice.label) : flag;
  });
  return labels.join(" + ");
}

export default function Coleccion() {
  const { packs } = getCatalog();
  const collection = useProgress((s) => s.collection);
  const routes = packs.flatMap((p) => p.routes);

  return (
    <Screen withTabBar>
      <Text style={type.title}>Colección</Text>
      {routes.map((route) => (
        <View key={route.id} style={{ gap: 12 }}>
          <Text style={type.subtitle}>{localize(route.title)}</Text>
          {route.endings?.length ? (
            <>
              <Text style={type.overline}>Finales</Text>
              <View style={styles.grid}>
                {route.endings.map((e) => {
                  const unlocked = collection.endingIds.includes(e.id);
                  const fg = unlocked ? colors.white : colors.muted;
                  return (
                    <View key={e.id} style={[styles.card, unlocked ? styles.unlocked : styles.locked]}>
                      <Icon name={unlocked ? "star" : "lock"} color={fg} />
                      <Text style={[styles.title, { color: fg }]}>{unlocked ? localize(e.title) : "???"}</Text>
                      <Text style={[styles.combo, { color: fg }]}>{endingCombo(route, e.requires)}</Text>
                    </View>
                  );
                })}
              </View>
            </>
          ) : null}
          {route.rewards?.length ? (
            <>
              <Text style={type.overline}>Coleccionables</Text>
              <View style={styles.grid}>
                {route.rewards.map((r) => {
                  const unlocked = collection.collectibleIds.includes(r.id);
                  const fg = unlocked ? colors.ink : colors.muted;
                  return (
                    <View key={r.id} style={[styles.card, unlocked ? styles.gold : styles.locked]}>
                      <Icon name={unlocked ? "trophy" : "lock"} color={fg} />
                      <Text style={[styles.title, { color: fg }]}>{unlocked ? localize(r.name) : "???"}</Text>
                    </View>
                  );
                })}
              </View>
            </>
          ) : null}
        </View>
      ))}
    </Screen>
  );
}

const styles = StyleSheet.create({
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  card: { width: "48%", gap: 6, padding: 12, borderRadius: radius.lg, borderWidth: border.base },
  unlocked: { backgroundColor: colors.clay, borderColor: colors.ink },
  gold: { backgroundColor: colors.gold, borderColor: colors.ink },
  locked: { backgroundColor: colors.sand, borderColor: colors.line, borderStyle: "dashed" },
  title: { fontFamily: fonts.bold, fontSize: 14 },
  combo: { fontFamily: fonts.body, fontSize: 11 },
});
