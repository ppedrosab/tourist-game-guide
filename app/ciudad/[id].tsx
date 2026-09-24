import { router, useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Chip, ChoiceCard, Panel } from "@/components/ui";
import { getPack } from "@/engine/catalog";
import { routeFacts } from "@/engine/outline";
import { localize } from "@/engine/runner";
import { type } from "@/theme";

export default function Ciudad() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const pack = getPack(id);
  if (!pack) {
    return (
      <Screen>
        <TopBar title="Ciudad no disponible" onBack={() => router.back()} />
      </Screen>
    );
  }
  return (
    <Screen>
      <TopBar title={localize(pack.name)} onBack={() => router.back()} />
      {pack.routes.map((route) => {
        const facts = routeFacts(route);
        const guide = pack.characters.find((c) => c.id === route.guideCharacterId);
        return (
          <View key={route.id} style={{ gap: 12 }}>
            <Panel>
              <Text style={type.overline}>
                {route.era}
                {guide ? ` · con ${localize(guide.name)}` : ""}
              </Text>
              <Text style={type.subtitle}>{localize(route.title)}</Text>
              <View style={{ flexDirection: "row", gap: 6, flexWrap: "wrap" }}>
                {route.isFree ? <Chip label="Gratis" variant="clay" /> : null}
                {facts.branches > 0 ? <Chip label={`${facts.branches} caminos`} variant="sand" icon="split" /> : null}
                {facts.endings > 0 ? <Chip label={`${facts.endings} finales`} variant="sand" icon="star" /> : null}
                <Chip label={`${route.durationMin} min`} variant="sand" icon="clock" />
              </View>
            </Panel>
            <ChoiceCard
              title="Ver la ruta"
              hint="Paradas, caminos y descarga"
              icon="route"
              onPress={() => router.push(`/ruta/${route.id}`)}
            />
          </View>
        );
      })}
    </Screen>
  );
}
