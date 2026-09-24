import { router, useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Chip, ChoiceCard, Panel } from "@/components/ui";
import { type } from "@/theme";

export default function Ciudad() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return (
    <Screen>
      <TopBar title={id === "malaga" ? "Málaga" : String(id)} onBack={() => router.back()} right={<Chip label="5 épocas" />} />
      <Panel>
        <Text style={type.overline}>s. I – s. XIX · con Er Cenachero</Text>
        <Text style={type.subtitle}>El misterio de la Manquita</Text>
        <View style={{ flexDirection: "row", gap: 6, flexWrap: "wrap" }}>
          <Chip label="Gratis" variant="clay" />
          <Chip label="2 caminos" variant="sand" icon="split" />
          <Chip label="4 finales" variant="sand" icon="star" />
          <Chip label="90 min" variant="sand" icon="clock" />
        </View>
      </Panel>
      <ChoiceCard title="Ver la ruta" hint="Paradas, caminos y descarga" icon="route" onPress={() => router.push("/ruta/misterio-manquita")} />
    </Screen>
  );
}
