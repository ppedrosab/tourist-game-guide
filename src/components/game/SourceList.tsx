import { Linking, Pressable, StyleSheet, Text, View } from "react-native";
import { Icon } from "@/components/ui";
import type { Source } from "@/content/types";
import { useI18n } from "@/i18n";
import { colors, type } from "@/theme";

/** Lista de referencias; las que tienen enlace se abren en el navegador. */
export function SourceList({ sources }: { sources: Source[] }) {
  const { t } = useI18n();
  return (
    <View style={{ gap: 4 }}>
      {sources.map((s) =>
        s.url ? (
          <Pressable
            key={s.title + s.url}
            accessibilityRole="link"
            accessibilityLabel={t("personaje.abrir", { title: s.title })}
            onPress={() => Linking.openURL(s.url!)}
            style={({ pressed }) => [styles.row, pressed && { opacity: 0.7 }]}
          >
            <Icon name="share" size={16} color={colors.sea} />
            <Text style={[type.secondary, styles.link]}>{s.title}</Text>
          </Pressable>
        ) : (
          <View key={s.title} style={styles.row}>
            <Icon name="book" size={16} color={colors.muted} />
            <Text style={[type.secondary, { flex: 1 }]}>{s.title}</Text>
          </View>
        ),
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 10, minHeight: 44 },
  link: { flex: 1, color: colors.sea, textDecorationLine: "underline" },
});
