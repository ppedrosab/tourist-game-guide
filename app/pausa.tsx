import { router } from "expo-router";
import { Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { ReactNode, useState } from "react";
import { Button3D, Icon, IconName, Panel } from "@/components/ui";
import { localize, routeStops } from "@/engine/runner";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { border, colors, radius, type } from "@/theme";

function Row({ icon, title, sub, onPress, right }: { icon: IconName; title: string; sub: string; onPress?: () => void; right?: ReactNode }) {
  return (
    <Pressable onPress={onPress} disabled={!onPress} accessibilityRole={onPress ? "button" : undefined} style={styles.row}>
      <View style={styles.rowIcon}>
        <Icon name={icon} size={18} />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={type.label}>{title}</Text>
        <Text style={type.caption}>{sub}</Text>
      </View>
      {right ?? <Icon name="next" size={16} strokeWidth={2.4} />}
    </Pressable>
  );
}

/** Modal de pausa: se abre desde el HUD y vuelve exactamente al mismo punto. */
export default function Pausa() {
  const [voces, setVoces] = useState(true);
  const [subtitulos, setSubtitulos] = useState(true);
  const current = useCurrentRun();
  const where = (() => {
    if (!current) return "";
    const { route, run } = current;
    const { stops, current: index } = routeStops(route, run);
    const node = route.nodes.find((n) => n.id === run.currentNodeId);
    return `Parada ${index + 1} de ${stops.length}${node ? ` · ${localize(node.title)}` : ""}`;
  })();
  return (
    <View style={styles.overlay}>
      <Panel nameplate="Pausa" nameplateColor={colors.ink} style={{ gap: 10 }}>
        <Text style={type.subtitle}>{current ? localize(current.route.title) : ""}</Text>
        <Text style={type.caption}>{where}</Text>
        <Button3D label="Continuar escena" icon="play" onPress={() => router.back()} />
        <Row icon="map" title="Ver mapa" sub="Siguiente parada y caminos" onPress={() => router.back()} />
        <Row icon="book" title="Cuaderno del detective" sub="Pistas y objetos" onPress={() => router.replace("/cuaderno")} />
        <Row icon="volume" title="Voces" sub="Volumen y velocidad" right={<Switch value={voces} onValueChange={setVoces} trackColor={{ true: colors.sea }} />} />
        <Row icon="subtitles" title="Subtítulos" sub="Siempre visibles" right={<Switch value={subtitulos} onValueChange={setSubtitulos} trackColor={{ true: colors.sea }} />} />
        <Row icon="exit" title="Salir y guardar" sub="Retoma donde lo dejaste" onPress={() => router.dismissTo("/")} />
      </Panel>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: { flex: 1, justifyContent: "center", padding: 16, backgroundColor: "rgba(27,42,58,0.62)" },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    padding: 10,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  rowIcon: { width: 38, height: 38, borderRadius: 11, backgroundColor: colors.sand, alignItems: "center", justifyContent: "center" },
});
