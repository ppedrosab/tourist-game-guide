import { StyleSheet, Text, View } from "react-native";
import type { PlayerProgress, Route } from "@/content/types";
import { localize } from "@/engine/runner";
import { useProgress } from "@/store/progress";
import { border, colors, radius, type } from "@/theme";
import { Screen } from "../layout/Screen";
import { Button3D } from "../ui/Button3D";
import { Chip } from "../ui/Chip";
import { Icon } from "../ui/Icon";
import { Panel } from "../ui/Panel";

type Props = { route: Route; run: PlayerProgress; onReplay: () => void; onExit: () => void };

/** Pantalla "Caso cerrado": final conseguido, coleccionables y otro camino. */
export function CaseClosed({ route, run, onReplay, onExit }: Props) {
  const endingIds = useProgress((s) => s.collection.endingIds);
  const ending = route.endings?.find((e) => e.id === run.endingId);
  const total = route.endings?.length ?? 0;
  const found = route.endings?.filter((e) => endingIds.includes(e.id)).length ?? 0;
  const rewards = (route.rewards ?? []).filter((r) => run.collectibleIds.includes(r.id));

  return (
    <Screen>
      <View style={styles.header}>
        <View style={styles.badge}>
          <Icon name="star" size={34} color={colors.ink} />
        </View>
        <Text style={type.display}>¡Caso cerrado!</Text>
        <Text style={type.secondary}>{localize(route.title)}</Text>
      </View>
      <Panel nameplate="Tu final" nameplateColor={colors.ink}>
        <Text style={type.title}>{ending ? localize(ending.title) : "Final misterioso"}</Text>
        <Text style={type.caption}>
          {found} de {total} finales descubiertos
        </Text>
      </Panel>
      {rewards.length > 0 ? (
        <Panel nameplate="Coleccionables">
          <View style={styles.chips}>
            {rewards.map((r) => (
              <Chip key={r.id} label={localize(r.name)} icon="trophy" variant="sand" />
            ))}
          </View>
        </Panel>
      ) : null}
      {found < total ? <Text style={type.body}>Hay calles que hoy no has pisado. ¿Pruebas el otro camino?</Text> : null}
      <Button3D label="Probar otro camino" icon="split" onPress={onReplay} />
      <Button3D label="Volver a Explorar" variant="secondary" icon="compass" onPress={onExit} />
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
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
});
