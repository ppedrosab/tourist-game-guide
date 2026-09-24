import { StyleSheet, Text, View } from "react-native";
import type { PlayerProgress, Route } from "@/content/types";
import { starsFor } from "@/engine/runner";
import { useI18n } from "@/i18n";
import { useProgress } from "@/store/progress";
import { border, colors, radius, type } from "@/theme";
import { Screen } from "../layout/Screen";
import { Button3D } from "../ui/Button3D";
import { Icon } from "../ui/Icon";
import { Panel } from "../ui/Panel";
import { CollectibleArt } from "./CollectibleArt";
import { Stars } from "./Stars";

type Props = { route: Route; run: PlayerProgress; onReplay: () => void; onExit: () => void };

/** Pantalla "Caso cerrado": final conseguido, coleccionables y otro camino. */
export function CaseClosed({ route, run, onReplay, onExit }: Props) {
  const { t, L } = useI18n();
  const endingIds = useProgress((s) => s.collection.endingIds);
  const ending = route.endings?.find((e) => e.id === run.endingId);
  const total = route.endings?.length ?? 0;
  const found = route.endings?.filter((e) => endingIds.includes(e.id)).length ?? 0;
  const rewards = (route.rewards ?? []).filter((r) => run.collectibleIds.includes(r.id));
  const score = starsFor(route, run);

  return (
    <Screen>
      <View style={styles.header}>
        <View style={styles.badge}>
          <Icon name="star" size={34} color={colors.ink} />
        </View>
        <Text style={type.display}>{t("final.casoCerrado")}</Text>
        <Text style={type.secondary}>{L(route.title)}</Text>
      </View>
      <Panel nameplate={t("final.tuFinal")} nameplateColor={colors.ink}>
        <Text style={type.title}>{ending ? L(ending.title) : t("final.misterioso")}</Text>
        <Stars value={score.stars} label={t("final.estrellas", { n: score.stars })} />
        {score.total > 0 ? (
          <Text style={type.secondary}>{t("final.retos", { ok: score.correct, total: score.total })}</Text>
        ) : null}
        <Text style={type.caption}>{t("final.descubiertos", { n: found, total })}</Text>
      </Panel>
      {rewards.length > 0 ? (
        <Panel nameplate={t("final.coleccionables")}>
          <View style={styles.chips}>
            {rewards.map((r) => (
              <View key={r.id} style={styles.reward} accessible accessibilityLabel={L(r.name)}>
                <CollectibleArt icon={r.icon} size={72} />
                <Text style={[type.caption, { textAlign: "center", color: colors.ink }]}>{L(r.name)}</Text>
              </View>
            ))}
          </View>
        </Panel>
      ) : null}
      {found < total ? <Text style={type.body}>{t("final.otrasCalles")}</Text> : null}
      <Button3D label={t("final.otroCamino")} icon="split" onPress={onReplay} />
      <Button3D label={t("final.volverExplorar")} variant="secondary" icon="compass" onPress={onExit} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { alignItems: "center", gap: 8, paddingTop: 12 },
  badge: {
    width: 72,
    height: 72,
    borderRadius: radius.xl,
    borderWidth: border.thick,
    borderColor: colors.ink,
    backgroundColor: colors.gold,
    alignItems: "center",
    justifyContent: "center",
  },
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 10, justifyContent: "center" },
  reward: { width: 92, alignItems: "center", gap: 4 },
});
