import { router } from "expo-router";
import { Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Button3D, Panel } from "@/components/ui";
import { LangSetting, useI18n } from "@/i18n";
import { useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

/** Los nombres de idioma van siempre en su propio idioma. */
const LANGS: { value: Exclude<LangSetting, "auto">; label: string }[] = [
  { value: "es", label: "Español" },
  { value: "en", label: "English" },
];

export default function Perfil() {
  const { t } = useI18n();
  const demoMode = useProgress((s) => s.demoMode);
  const setDemoMode = useProgress((s) => s.setDemoMode);
  const language = useProgress((s) => s.language);
  const setLanguage = useProgress((s) => s.setLanguage);
  const options: { value: LangSetting; label: string }[] = [{ value: "auto", label: t("perfil.idiomaAuto") }, ...LANGS];

  return (
    <Screen withTabBar>
      <Text style={type.title}>{t("tabs.perfil")}</Text>
      <Panel nameplate={t("perfil.ajustes")}>
        <Text style={type.label}>{t("perfil.idioma")}</Text>
        <View style={styles.segmented} accessibilityRole="radiogroup">
          {options.map((o) => {
            const selected = language === o.value;
            return (
              <Pressable
                key={o.value}
                onPress={() => setLanguage(o.value)}
                accessibilityRole="radio"
                accessibilityState={{ selected }}
                style={[styles.segment, selected && styles.segmentOn]}
              >
                <Text style={[styles.segmentText, selected && { color: colors.white }]}>{o.label}</Text>
              </Pressable>
            );
          })}
        </View>
        <View style={styles.row}>
          <View style={{ flex: 1 }}>
            <Text style={type.label}>{t("perfil.modoDemo")}</Text>
            <Text style={type.caption}>{t("perfil.modoDemoTexto")}</Text>
          </View>
          <Switch
            value={demoMode}
            onValueChange={setDemoMode}
            trackColor={{ true: colors.sea }}
            accessibilityLabel={t("perfil.modoDemo")}
          />
        </View>
      </Panel>
      <Button3D label={t("perfil.verBienvenida")} variant="secondary" onPress={() => router.push("/bienvenida")} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 12 },
  segmented: { flexDirection: "row", gap: 6 },
  segment: {
    flex: 1,
    minHeight: 44,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: radius.sm,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  segmentOn: { backgroundColor: colors.ink },
  segmentText: { fontFamily: fonts.bold, fontSize: 14, color: colors.ink },
});
