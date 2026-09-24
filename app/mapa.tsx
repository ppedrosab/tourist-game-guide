import { useIsFocused } from "@react-navigation/native";
import { router } from "expo-router";
import { useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip } from "@/components/ui";
import { distanceM, geofenceTargets } from "@/engine/geo";
import { useI18n } from "@/i18n";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { useUserPosition } from "@/hooks/useUserPosition";
import { useProgress } from "@/store/progress";
import { RouteMap } from "@/map/RouteMap";
import { branchColors, colors, type } from "@/theme";

/** Mapa de la ruta en curso (modal): los dos caminos, tu posición y la siguiente parada. */
export default function Mapa() {
  const { t, L, distance, branch } = useI18n();
  const current = useCurrentRun();
  const focused = useIsFocused();
  const user = useUserPosition(focused);
  const track = useProgress((s) => s.track);
  const routeId = current?.route.id;
  useEffect(() => {
    track({ name: "map_opened", routeId });
  }, [track, routeId]);
  const close = () => router.back();

  if (!current) {
    return (
      <Screen>
        <TopBar title={t("mapa.titulo")} onBack={close} closeIcon />
        <Text style={type.secondary}>{t("mapa.vacio")}</Text>
      </Screen>
    );
  }
  const { route, run } = current;
  const next = run.completedAt ? [] : geofenceTargets(route, run);

  return (
    <Screen scroll={false}>
      <TopBar title={t("mapa.tituloRuta")} onBack={close} closeIcon />
      <View style={styles.legend}>
        <Chip label={branch(route, "dinero")} dot={branchColors.dinero} />
        <Chip label={branch(route, "poder")} dot={branchColors.poder} />
        <Chip label={t("mapa.siguiente")} dot={colors.gold} />
      </View>
      <RouteMap route={route} run={run} user={user} />
      {next.length > 0 ? (
        <View style={{ gap: 2 }}>
          <Text style={type.overline}>{next.length > 1 ? t("mapa.siguientesParadas") : t("mapa.siguienteParada")}</Text>
          {next.map((n) => (
            <Text key={n.id} style={type.label}>
              {L(n.title)}
              {user && n.location ? (
                <Text style={type.caption}>{t("mapa.aDistancia", { distance: distance(distanceM(user, n.location)) })}</Text>
              ) : null}
            </Text>
          ))}
        </View>
      ) : null}
      <Button3D label={t("mapa.volverEscena")} icon="play" onPress={close} />
    </Screen>
  );
}

const styles = StyleSheet.create({ legend: { flexDirection: "row", flexWrap: "wrap", gap: 6 } });
