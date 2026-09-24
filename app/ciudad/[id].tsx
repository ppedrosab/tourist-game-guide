import { router, useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { Chip, ChoiceCard, Panel, ThemeBadge } from "@/components/ui";
import { getPack } from "@/engine/catalog";
import { routeFacts } from "@/engine/outline";
import { useI18n } from "@/i18n";
import { type } from "@/theme";

export default function Ciudad() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { t, L } = useI18n();
  const pack = getPack(id);
  if (!pack) {
    return (
      <Screen>
        <TopBar title={t("ciudad.noDisponible")} onBack={() => router.back()} />
      </Screen>
    );
  }
  return (
    <Screen>
      <TopBar title={L(pack.name)} onBack={() => router.back()} />
      {pack.routes.map((route) => {
        const facts = routeFacts(route);
        const guide = pack.characters.find((c) => c.id === route.guideCharacterId);
        return (
          <View key={route.id} style={{ gap: 12 }}>
            <Panel>
              <Text style={type.overline}>
                {route.era}
                {guide ? ` · ${t("ciudad.con", { name: L(guide.name) })}` : ""}
              </Text>
              <Text style={type.subtitle}>{L(route.title)}</Text>
              <View style={{ flexDirection: "row", gap: 6, flexWrap: "wrap" }}>
                <ThemeBadge route={route} />
                {route.isFree ? <Chip label={t("comun.gratis")} variant="clay" /> : null}
                {facts.branches > 0 ? <Chip label={t("comun.caminos", { n: facts.branches })} variant="sand" icon="split" /> : null}
                {facts.endings > 0 ? <Chip label={t("comun.finales", { n: facts.endings })} variant="sand" icon="star" /> : null}
                <Chip label={t("comun.minutos", { n: route.durationMin })} variant="sand" icon="clock" />
              </View>
            </Panel>
            <ChoiceCard
              title={t("ciudad.verRuta")}
              hint={t("ciudad.verRutaTexto")}
              icon="route"
              onPress={() => router.push(`/ruta/${route.id}`)}
            />
          </View>
        );
      })}
    </Screen>
  );
}
