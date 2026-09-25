import { router } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Chip, Icon } from "@/components/ui";
import type { CityPack } from "@/content/types";
import { routeCast } from "@/engine/outline";
import { useI18n } from "@/i18n";
import { border, colors, fonts, radius, type } from "@/theme";
import { Portrait } from "./Portrait";

/**
 * Álbum de personajes de una ciudad: los ya conocidos con su retrato (abren la ficha) y los
 * demás bloqueados. Completar la ciudad da la seña dorada.
 */
export function CharacterAlbum({ pack, met }: { pack: CityPack; met: readonly string[] }) {
  const { t, L } = useI18n();
  // Orden del álbum: ruta a ruta, el guía primero; cada personaje con la primera ruta en la que sale.
  const entries = pack.routes.flatMap((route) => routeCast(pack, route).map((c) => ({ c, route })));
  const seen = new Set<string>();
  const cast = entries.filter(({ c }) => (seen.has(c.id) ? false : (seen.add(c.id), true)));
  const known = cast.filter(({ c }) => met.includes(`${pack.id}/${c.id}`)).length;
  const complete = known === cast.length;

  return (
    <View style={{ gap: 10 }}>
      <View style={styles.head}>
        <Text style={[type.subtitle, { flex: 1 }]}>{L(pack.name)}</Text>
        {complete ? (
          <Chip label={t("coleccion.albumCompleto")} variant="gold" icon="trophy" />
        ) : (
          <Text style={type.caption}>{t("coleccion.conocidos", { n: known, total: cast.length })}</Text>
        )}
      </View>
      {known === 0 ? <Text style={type.secondary}>{t("coleccion.nadieAun")}</Text> : null}
      <View style={[styles.grid, known === 0 && { display: "none" }]}>
        {cast.map(({ c, route }) => {
          const unlocked = met.includes(`${pack.id}/${c.id}`);
          return unlocked ? (
            <Pressable
              key={c.id}
              accessibilityRole="button"
              accessibilityLabel={t("personaje.verFicha", { name: L(c.name) })}
              onPress={() => router.push({ pathname: "/personaje", params: { ruta: route.id, id: c.id } })}
              style={({ pressed }) => [styles.cell, pressed && { opacity: 0.7 }]}
            >
              <Portrait character={c} size={64} />
              <Text style={styles.name} numberOfLines={2}>
                {L(c.name)}
              </Text>
            </Pressable>
          ) : (
            <View key={c.id} style={styles.cell} accessible accessibilityLabel={t("coleccion.personajeOculto")}>
              <View style={styles.locked}>
                <Icon name="lock" size={20} color={colors.muted} />
              </View>
              <Text style={[styles.name, { color: colors.muted }]}>{t("coleccion.oculto")}</Text>
            </View>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: "row", alignItems: "center", gap: 8 },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  cell: { width: "22%", alignItems: "center", gap: 4, minHeight: 44 },
  locked: {
    width: 64,
    height: 64,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.line,
    borderStyle: "dashed",
    alignItems: "center",
    justifyContent: "center",
  },
  name: { fontFamily: fonts.bold, fontSize: 11, textAlign: "center", color: colors.ink },
});
