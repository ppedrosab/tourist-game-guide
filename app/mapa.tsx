import { useIsFocused } from "@react-navigation/native";
import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip } from "@/components/ui";
import { distanceM, geofenceTargets } from "@/engine/geo";
import { localize } from "@/engine/runner";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { useUserPosition } from "@/hooks/useUserPosition";
import { RouteMap } from "@/map/RouteMap";
import { branchColors, colors, type } from "@/theme";

const fmt = (m: number) => (m < 1000 ? `${Math.round(m / 10) * 10} m` : `${(m / 1000).toLocaleString("es-ES", { maximumFractionDigits: 1 })} km`);

/** Mapa de la ruta en curso (modal): los dos caminos, tu posición y la siguiente parada. */
export default function Mapa() {
  const current = useCurrentRun();
  const focused = useIsFocused();
  const user = useUserPosition(focused);
  const close = () => router.back();

  if (!current) {
    return (
      <Screen>
        <TopBar title="Mapa" onBack={close} closeIcon />
        <Text style={type.secondary}>Empieza una ruta para ver su mapa.</Text>
      </Screen>
    );
  }
  const { route, run } = current;
  const next = run.completedAt ? [] : geofenceTargets(route, run);

  return (
    <Screen scroll={false}>
      <TopBar title="Mapa de la ruta" onBack={close} closeIcon />
      <View style={styles.legend}>
        <Chip label="Dinero" dot={branchColors.dinero} />
        <Chip label="Poder" dot={branchColors.poder} />
        <Chip label="Siguiente" dot={colors.gold} />
      </View>
      <RouteMap route={route} run={run} user={user} />
      {next.length > 0 ? (
        <View style={{ gap: 2 }}>
          <Text style={type.overline}>{next.length > 1 ? "Siguientes paradas posibles" : "Siguiente parada"}</Text>
          {next.map((n) => (
            <Text key={n.id} style={type.label}>
              {localize(n.title)}
              {user && n.location ? <Text style={type.caption}> · a {fmt(distanceM(user, n.location))}</Text> : null}
            </Text>
          ))}
        </View>
      ) : null}
      <Button3D label="Volver a la escena" icon="play" onPress={close} />
    </Screen>
  );
}

const styles = StyleSheet.create({ legend: { flexDirection: "row", flexWrap: "wrap", gap: 6 } });
