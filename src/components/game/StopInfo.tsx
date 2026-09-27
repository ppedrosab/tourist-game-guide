import { StyleSheet, View } from "react-native";
import { Chip } from "@/components/ui/Chip";
import type { CityPack, PlayerProgress, Route, StoryNode } from "@/content/types";
import { hoursAt } from "@/engine/hours";
import { legTo, STEEP_GRADE, stopPractical } from "@/engine/practical";
import { useI18n } from "@/i18n";

/** Cuestas que merecen aviso en el camino hacia una parada (m de subida). */
const CLIMB_WORTH_NOTING = 15;

/**
 * Lo práctico de la parada a la que se va: escaleras o cuesta en el camino, agua, aseos, sombra y si
 * el sitio está abierto ahora. Todo como chips pequeños: no debe quitar protagonismo a la escena.
 */
export function StopInfo({
  pack,
  route,
  run,
  node,
  now = new Date(),
}: {
  pack: CityPack;
  route: Route;
  run: Pick<PlayerProgress, "visitedNodeIds">;
  node: StoryNode;
  now?: Date;
}) {
  const { t, distance } = useI18n();
  const stop = stopPractical(route, node.id);
  const leg = legTo(route, run, node.id);
  const chips: { key: string; label: string; icon: Parameters<typeof Chip>[0]["icon"]; variant?: "sand" | "clay" | "sea" }[] =
    [];
  if (leg?.steps) chips.push({ key: "steps", label: t("practico.hayEscaleras"), icon: "stairs", variant: "clay" });
  if (leg && leg.up >= CLIMB_WORTH_NOTING && leg.grade >= STEEP_GRADE)
    chips.push({ key: "up", label: t("practico.cuestaArriba", { up: leg.up }), icon: "slope", variant: "clay" });
  if (stop?.hours && stop.hoursOf) {
    const state = hoursAt(stop.hours, now, pack.timeZone);
    const place = stop.hoursOf;
    if (state?.open)
      chips.push({
        key: "hours",
        label: state.allDay ? t("practico.abierto24", { place }) : t("practico.abiertoHasta", { place, hour: state.closesAt }),
        icon: "clock",
        variant: "sea",
      });
    else if (state)
      chips.push({
        key: "hours",
        label: state.opensAt ? t("practico.abreA", { place, hour: state.opensAt }) : t("practico.cerradoHoy", { place }),
        icon: "clock",
      });
  }
  if (stop?.water !== undefined) chips.push({ key: "water", label: t("practico.aguaA", { distance: distance(stop.water) }), icon: "water" });
  if (stop?.toilets !== undefined)
    chips.push({ key: "toilets", label: t("practico.aseosA", { distance: distance(stop.toilets) }), icon: "toilet" });
  if (stop?.shade) chips.push({ key: "shade", label: t("practico.sombra"), icon: "tree" });
  if (chips.length === 0) return null;
  return (
    <View style={styles.row} accessible accessibilityLabel={`${t("practico.infoParada")}: ${chips.map((c) => c.label).join(", ")}`}>
      {chips.map((c) => (
        <Chip key={c.key} label={c.label} icon={c.icon} variant={c.variant ?? "sand"} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
});
