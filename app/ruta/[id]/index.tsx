import { router, useLocalSearchParams } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip, IconButton, Panel } from "@/components/ui";
import { findRoute } from "@/engine/catalog";
import { routeFacts, routeOutline } from "@/engine/outline";
import { localize } from "@/engine/runner";
import { useActiveRun, useProgress } from "@/store/progress";
import { border, branchColors, colors, fonts, type } from "@/theme";

const km = (n: number) => `${n.toLocaleString("es-ES")} km`;

export default function DetalleRuta() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const found = findRoute(id);
  const active = useActiveRun(id);
  const start = useProgress((s) => s.start);

  if (!found) {
    return (
      <Screen>
        <TopBar title="Ruta no encontrada" onBack={() => router.back()} />
      </Screen>
    );
  }
  const { pack, route } = found;
  const facts = routeFacts(route);
  const outline = routeOutline(route);
  const play = () => router.push(`/ruta/${route.id}/jugar`);
  const startFresh = () => {
    start(pack.id, route);
    play();
  };

  return (
    <Screen>
      <TopBar title={localize(route.title)} onBack={() => router.back()} />
      <View style={styles.chips}>
        <Chip label={`${route.durationMin} min`} icon="clock" />
        <Chip label={km(route.distanceKm)} icon="walk" />
        {facts.branches > 0 ? <Chip label={`${facts.branches} caminos`} icon="split" /> : null}
        {facts.endings > 0 ? <Chip label={`${facts.endings} finales`} icon="star" /> : null}
      </View>
      <Text style={type.body}>{localize(route.summary)}</Text>
      <Panel>
        {outline.map((item, i) =>
          item.kind === "stop" ? (
            <View key={item.node.id} style={styles.stop}>
              <View style={[styles.num, { backgroundColor: item.decision ? colors.clay : colors.ink }]}>
                <Text style={styles.numText}>{i + 1 /* un bloque de ramas cuenta como una parada */}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={type.label}>{localize(item.node.title)}</Text>
                {item.decision ? <Text style={type.caption}>Decisión {item.decision}</Text> : null}
              </View>
            </View>
          ) : (
            <View key={`ramas-${i}`} style={styles.branches}>
              {item.branches
                .filter((b) => b.nodes.length > 0)
                .map((b) => (
                  <View key={b.nodes[0].id} style={styles.branch}>
                    <View style={[styles.dot, { backgroundColor: branchColors[b.branch ?? "comun"] }]} />
                    <Text style={[type.caption, { flex: 1, color: colors.ink }]}>
                      {b.nodes.map((node) => localize(node.title)).join(" · ")}
                    </Text>
                  </View>
                ))}
            </View>
          ),
        )}
      </Panel>
      <View style={styles.actions}>
        <IconButton icon="download" label="Descargar ruta para jugar sin datos" />
        <View style={{ flex: 1 }}>
          {active ? (
            <Button3D label="Continuar" icon="play" onPress={play} />
          ) : (
            <Button3D label="Comenzar ruta" icon="play" onPress={startFresh} />
          )}
        </View>
      </View>
      {active ? <Button3D label="Empezar de nuevo" variant="ghost" onPress={startFresh} /> : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
  stop: { flexDirection: "row", alignItems: "center", gap: 12, paddingVertical: 4 },
  num: {
    width: 30,
    height: 30,
    borderRadius: 10,
    borderWidth: border.thin,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  numText: { fontFamily: fonts.bold, fontSize: 12, color: colors.white },
  branches: { gap: 6, paddingLeft: 42, paddingVertical: 6 },
  branch: { flexDirection: "row", alignItems: "center", gap: 8 },
  dot: { width: 10, height: 10, borderRadius: 5, borderWidth: border.thin, borderColor: colors.ink },
  actions: { flexDirection: "row", alignItems: "flex-start", gap: 10 },
});
