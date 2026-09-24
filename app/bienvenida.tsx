import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AzulejoBackground, Button3D, Panel } from "@/components/ui";
import { colors, type } from "@/theme";

export default function Bienvenida() {
  const insets = useSafeAreaInsets();
  return (
    <View style={styles.root}>
      <AzulejoBackground />
      {/* Fase 3: aquí va la escena de la Plaza de la Marina con el cenachero. */}
      <View style={{ flex: 1 }} />
      <View style={{ padding: 12, paddingBottom: insets.bottom + 16 }}>
        <Panel>
          <Text style={type.title}>Camina la historia. Decide el camino.</Text>
          <Text style={type.secondary}>
            Personajes de otra época te guían por la calle, te plantean retos y tú eliges por dónde seguir.
          </Text>
          <Button3D label="Empezar la aventura" icon="next" onPress={() => router.push("/permisos")} />
          <Button3D label="Ya tengo cuenta" variant="ghost" onPress={() => router.replace("/")} />
        </Panel>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({ root: { flex: 1, backgroundColor: colors.ink } });
