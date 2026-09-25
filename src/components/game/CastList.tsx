import { router } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Icon } from "@/components/ui";
import type { Character, Route } from "@/content/types";
import { useI18n } from "@/i18n";
import { colors, type } from "@/theme";
import { Portrait } from "./Portrait";

/** Qué es un personaje, para la ficha y las listas: «Persona real · 1860-1935», «Figura de leyenda»… */
export function useCharacterKind() {
  const { t } = useI18n();
  return (c: Character) =>
    [c.kind ? t(`personaje.${c.kind}`) : undefined, c.lived].filter(Boolean).join(" · ");
}

/** Reparto de una ruta: cada fila abre la ficha del personaje. */
export function CastList({ route, cast }: { route: Route; cast: Character[] }) {
  const { t, L } = useI18n();
  const kindOf = useCharacterKind();
  return (
    <View style={{ gap: 6 }}>
      {cast.map((c) => (
        <Pressable
          key={c.id}
          accessibilityRole="button"
          accessibilityLabel={t("personaje.verFicha", { name: L(c.name) })}
          onPress={() => router.push({ pathname: "/personaje", params: { ruta: route.id, id: c.id } })}
          style={({ pressed }) => [styles.row, pressed && { opacity: 0.7 }]}
        >
          <Portrait character={c} size={48} />
          <View style={{ flex: 1 }}>
            <Text style={type.label}>{L(c.name)}</Text>
            <Text style={type.caption}>{kindOf(c) || L(c.description)}</Text>
          </View>
          <Icon name="next" size={18} color={colors.muted} />
        </Pressable>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 12, minHeight: 56 },
});
