import { StyleSheet, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Icon } from "@/components/ui";
import type { LangCode, Route } from "@/content/types";
import { Stars } from "@/components/game/Stars";
import { getCatalog } from "@/engine/catalog";
import { localize } from "@/engine/runner";
import { useI18n } from "@/i18n";
import { useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

/** Combinación de decisiones que lleva a un final, con las etiquetas de las opciones del pack. */
function endingCombo(route: Route, requires: string[], lang: LangCode): string {
  const labels = requires.map((flag) => {
    const choice = route.nodes.flatMap((n) => n.choices ?? []).find((c) => c.setFlags?.includes(flag));
    return choice ? localize(choice.label, lang) : flag;
  });
  return labels.join(" + ");
}

export default function Coleccion() {
  const { packs } = getCatalog();
  const { t, L, lang } = useI18n();
  const collection = useProgress((s) => s.collection);
  const routes = packs.flatMap((p) => p.routes);

  return (
    <Screen withTabBar>
      <Text style={type.title}>{t("tabs.coleccion")}</Text>
      {routes.map((route) => (
        <View key={route.id} style={{ gap: 12 }}>
          <Text style={type.subtitle}>{L(route.title)}</Text>
          {collection.bestStars?.[route.id] ? (
            <Stars
              value={collection.bestStars[route.id]}
              size={22}
              label={t("coleccion.estrellas", { n: collection.bestStars[route.id] })}
            />
          ) : null}
          {route.endings?.length ? (
            <>
              <Text style={type.overline}>{t("coleccion.finales")}</Text>
              <View style={styles.grid}>
                {route.endings.map((e) => {
                  const unlocked = collection.endingIds.includes(e.id);
                  const fg = unlocked ? colors.white : colors.muted;
                  return (
                    <View key={e.id} style={[styles.card, unlocked ? styles.unlocked : styles.locked]}>
                      <Icon name={unlocked ? "star" : "lock"} color={fg} />
                      <Text style={[styles.title, { color: fg }]}>{unlocked ? L(e.title) : t("coleccion.oculto")}</Text>
                      <Text style={[styles.combo, { color: fg }]}>{endingCombo(route, e.requires, lang)}</Text>
                    </View>
                  );
                })}
              </View>
            </>
          ) : null}
          {route.rewards?.length ? (
            <>
              <Text style={type.overline}>{t("coleccion.coleccionables")}</Text>
              <View style={styles.grid}>
                {route.rewards.map((r) => {
                  const unlocked = collection.collectibleIds.includes(r.id);
                  const fg = unlocked ? colors.ink : colors.muted;
                  return (
                    <View key={r.id} style={[styles.card, unlocked ? styles.gold : styles.locked]}>
                      <Icon name={unlocked ? "trophy" : "lock"} color={fg} />
                      <Text style={[styles.title, { color: fg }]}>{unlocked ? L(r.name) : t("coleccion.oculto")}</Text>
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
