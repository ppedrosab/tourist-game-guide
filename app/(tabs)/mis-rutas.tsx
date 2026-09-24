import { router } from "expo-router";
import { Text } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { ChoiceCard } from "@/components/ui";
import { findRoute } from "@/engine/catalog";
import { runProgress } from "@/engine/outline";
import { useI18n } from "@/i18n";
import { useProgress } from "@/store/progress";
import { type } from "@/theme";

export default function MisRutas() {
  const { t, L, branch } = useI18n();
  const runs = useProgress((s) => s.runs);
  const items = Object.values(runs)
    .map((run) => ({ run, found: findRoute(run.routeId) }))
    .filter((x) => x.found !== undefined);

  return (
    <Screen withTabBar>
      <Text style={type.title}>{t("tabs.misRutas")}</Text>
      {items.length === 0 ? (
        <Text style={type.secondary}>{t("misRutas.vacio")}</Text>
      ) : null}
      {items.map(({ run, found }) => {
        const { pack, route } = found!;
        const p = runProgress(route, run);
        const camino = p.branch ? ` · ${branch(route, p.branch, "trail")}` : "";
        const ending = route.endings?.find((e) => e.id === run.endingId);
        return (
          <ChoiceCard
            key={route.id}
            title={L(route.title)}
            hint={`${L(pack.name)}${route.theme === "gastronomia" ? ` · ${t("comun.gastronomia")}` : route.theme === "fiestas" ? ` · ${t("comun.fiestas")}` : ""} · ${run.completedAt ? t("misRutas.terminada") : t("misRutas.enCurso")}`}
            meta={
              run.completedAt
                ? t("misRutas.final", { title: ending ? L(ending.title) : "?" })
                : `${t("comun.paradaDe", { n: p.stop, total: p.total })}${camino}`
            }
            branch={p.branch ?? "comun"}
            icon="route"
            onPress={() => router.push(`/ruta/${route.id}`)}
          />
        );
      })}
    </Screen>
  );
}
