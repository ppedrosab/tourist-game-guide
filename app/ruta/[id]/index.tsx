import { router, useLocalSearchParams } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Button3D, Chip, IconButton, Panel } from "@/components/ui";
import { border, branchColors, colors, fonts, type } from "@/theme";

const STOPS = [
  { n: "1", name: "Plaza de la Marina", sub: "Conoce a Er Cenachero" },
  { n: "2", name: "Calle Larios", sub: "Decisión 1 · ¿dinero o poder?", decision: true },
  { n: "4", name: "La Manquita", sub: "Decisión 2 · ¿leyenda o documentos?", decision: true },
  { n: "5", name: "Teatro Romano" },
  { n: "6", name: "Plaza de la Merced", sub: "Resuelve el misterio" },
];

export default function DetalleRuta() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return (
    <Screen>
      <TopBar title="El misterio de la Manquita" onBack={() => router.back()} />
      <View style={styles.chips}>
        <Chip label="90 min" icon="clock" />
        <Chip label="2,2 km" icon="walk" />
        <Chip label="2 caminos" icon="split" />
        <Chip label="4 finales" icon="star" />
      </View>
      <Panel>
        {STOPS.map((s, i) => (
          <View key={s.name}>
            <View style={styles.stop}>
              <View style={[styles.num, { backgroundColor: s.decision ? colors.clay : colors.ink }]}>
                <Text style={styles.numText}>{s.n}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={type.label}>{s.name}</Text>
                {s.sub ? <Text style={type.caption}>{s.sub}</Text> : null}
              </View>
            </View>
            {i === 1 ? (
              <View style={styles.branches}>
                <Chip label="Atarazanas · Casa de Guardia" dot={branchColors.dinero} />
                <Chip label="Constitución" dot={branchColors.poder} />
              </View>
            ) : null}
          </View>
        ))}
      </Panel>
      <View style={styles.actions}>
        <IconButton icon="download" label="Descargar ruta para jugar sin datos" />
        <View style={{ flex: 1 }}>
          <Button3D label="Comenzar ruta" icon="play" onPress={() => router.push(`/ruta/${id}/jugar`)} />
        </View>
      </View>
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
  actions: { flexDirection: "row", alignItems: "flex-start", gap: 10 },
});
