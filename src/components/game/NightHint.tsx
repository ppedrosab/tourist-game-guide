import { StyleSheet, Text, View } from "react-native";
import { Icon } from "@/components/ui";
import type { CityPack, Route } from "@/content/types";
import { useI18n } from "@/i18n";
import { isDark, nextDusk } from "@/scene/sun";
import { border, colors, radius, type } from "@/theme";

/** Rutas pensadas para el anochecer: dice si ya es buen momento o a qué hora anochece hoy en la ciudad. */
export function NightHint({ pack, route, now = new Date() }: { pack: CityPack; route: Route; now?: Date }) {
  const { t, lang } = useI18n();
  if (route.bestTime !== "noche") return null;
  const { lat, lng } = pack.center;
  const dark = isDark(now, lat, lng);
  const dusk = dark ? undefined : nextDusk(now, lat, lng);
  const hour = dusk?.toLocaleTimeString(lang === "es" ? "es-ES" : "en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: pack.timeZone,
  });
  return (
    <View style={styles.box} accessible accessibilityRole="text">
      <Icon name="moon" size={20} color={colors.white} />
      <Text style={[type.body, styles.text]}>
        {dark ? t("ruta.yaDeNoche") : hour ? t("ruta.mejorAnochecer", { hour }) : t("ruta.mejorAnochecerSinHora")}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  box: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    padding: 12,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.night,
  },
  text: { flex: 1, color: colors.white },
});
