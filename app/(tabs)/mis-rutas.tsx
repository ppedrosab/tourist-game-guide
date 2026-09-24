import { router } from "expo-router";
import { Text } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { ChoiceCard } from "@/components/ui";
import { findRoute } from "@/engine/catalog";
import { runProgress } from "@/engine/outline";
import { localize } from "@/engine/runner";
import { useProgress } from "@/store/progress";
import { type } from "@/theme";

export default function MisRutas() {
  const runs = useProgress((s) => s.runs);
  const items = Object.values(runs)
    .map((run) => ({ run, found: findRoute(run.routeId) }))
    .filter((x) => x.found !== undefined);

  return (
    <Screen withTabBar>
      <Text style={type.title}>Mis rutas</Text>
      {items.length === 0 ? (
        <Text style={type.secondary}>Aún no has empezado ninguna ruta. Elige una ciudad en Explorar.</Text>
      ) : null}
      {items.map(({ run, found }) => {
        const { pack, route } = found!;
        const p = runProgress(route, run);
        const camino = p.branch ? ` · camino del ${p.branch}` : "";
        const ending = route.endings?.find((e) => e.id === run.endingId);
        return (
          <ChoiceCard
            key={route.id}
            title={localize(route.title)}
            hint={`${localize(pack.name)} · ${run.completedAt ? "terminada" : "en curso"}`}
            meta={run.completedAt ? `Final: ${ending ? localize(ending.title) : "?"}` : `Parada ${p.stop} de ${p.total}${camino}`}
            branch={p.branch ?? "comun"}
            icon="route"
            onPress={() => router.push(`/ruta/${route.id}`)}
          />
        );
      })}
    </Screen>
  );
}
