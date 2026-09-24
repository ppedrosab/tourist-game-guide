import { router } from "expo-router";
import { Text } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { ChoiceCard } from "@/components/ui";
import { type } from "@/theme";

export default function MisRutas() {
  return (
    <Screen withTabBar>
      <Text style={type.title}>Mis rutas</Text>
      <ChoiceCard
        title="El misterio de la Manquita"
        hint="Málaga · en curso"
        meta="Parada 2 de 8 · camino del dinero"
        branch="dinero"
        icon="route"
        onPress={() => router.push("/ruta/misterio-manquita")}
      />
    </Screen>
  );
}
