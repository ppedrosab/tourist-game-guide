import { router } from "expo-router";
import { StyleSheet, Switch, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Button3D, Panel } from "@/components/ui";
import { useProgress } from "@/store/progress";
import { colors, type } from "@/theme";

export default function Perfil() {
  const demoMode = useProgress((s) => s.demoMode);
  const setDemoMode = useProgress((s) => s.setDemoMode);
  return (
    <Screen withTabBar>
      <Text style={type.title}>Perfil</Text>
      <Panel nameplate="Ajustes">
        <View style={styles.row}>
          <View style={{ flex: 1 }}>
            <Text style={type.label}>Modo demo</Text>
            <Text style={type.caption}>Botón «Simular llegada» para jugar la ruta desde casa.</Text>
          </View>
          <Switch
            value={demoMode}
            onValueChange={setDemoMode}
            trackColor={{ true: colors.sea }}
            accessibilityLabel="Modo demo"
          />
        </View>
        <Text style={type.secondary}>Voces, subtítulos e idioma llegarán en la fase 3.</Text>
      </Panel>
      <Button3D label="Ver bienvenida" variant="secondary" onPress={() => router.push("/bienvenida")} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 12 },
});
