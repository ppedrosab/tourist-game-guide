import { router, useLocalSearchParams } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { Screen, TopBar } from "@/components/layout/Screen";
import { useCharacterKind } from "@/components/game/CastList";
import { Portrait } from "@/components/game/Portrait";
import { SourceList } from "@/components/game/SourceList";
import { Panel } from "@/components/ui";
import { findRoute } from "@/engine/catalog";
import { useI18n } from "@/i18n";
import { type } from "@/theme";

/** Ficha de un personaje (modal): quién fue, su historia y dónde saber más. */
export default function Personaje() {
  const { ruta, id } = useLocalSearchParams<{ ruta: string; id: string }>();
  const { t, L } = useI18n();
  const kindOf = useCharacterKind();
  const character = findRoute(ruta)?.pack.characters.find((c) => c.id === id);
  const close = () => router.back();

  if (!character) {
    return (
      <Screen>
        <TopBar title={t("personaje.noEncontrado")} onBack={close} closeIcon />
      </Screen>
    );
  }
  const kind = kindOf(character);
  return (
    <Screen>
      <TopBar title={L(character.name)} onBack={close} closeIcon />
      <View style={styles.head}>
        <Portrait character={character} size={112} />
        <View style={{ flex: 1, gap: 4 }}>
          {kind ? <Text style={type.overline}>{kind}</Text> : null}
          <Text style={type.secondary}>{L(character.description)}</Text>
        </View>
      </View>
      {character.bio ? (
        <Panel>
          <Text style={type.overline}>{t("personaje.historia")}</Text>
          <Text style={type.body}>{L(character.bio)}</Text>
        </Panel>
      ) : null}
      {character.sources?.length ? (
        <Panel>
          <Text style={type.overline}>{t("personaje.referencias")}</Text>
          <SourceList sources={character.sources} />
        </Panel>
      ) : null}
    </Screen>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: "row", alignItems: "center", gap: 16 },
});
