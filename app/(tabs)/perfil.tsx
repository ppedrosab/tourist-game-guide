import { router } from "expo-router";
import { Text } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Button3D, Panel } from "@/components/ui";
import { type } from "@/theme";

export default function Perfil() {
  return (
    <Screen withTabBar>
      <Text style={type.title}>Perfil</Text>
      <Panel nameplate="Ajustes">
        <Text style={type.body}>Voces, subtítulos e idioma llegarán en la fase 3.</Text>
      </Panel>
      <Button3D label="Ver bienvenida" variant="secondary" onPress={() => router.push("/bienvenida")} />
    </Screen>
  );
}
