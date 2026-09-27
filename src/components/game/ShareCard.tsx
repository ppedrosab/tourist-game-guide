import Constants from "expo-constants";
import { forwardRef } from "react";
import { StyleSheet, Text, View } from "react-native";
import type { Collectible, Route } from "@/content/types";
import { useI18n } from "@/i18n";
import { border, colors, fonts, radius } from "@/theme";
import { AzulejoBackground } from "../ui/AzulejoBackground";
import { ThemeBadge } from "../ui/ThemeBadge";
import { CollectibleArt } from "./CollectibleArt";
import { Stars } from "./Stars";

type Props = { route: Route; city: string; ending: string; stars: number; rewards: Collectible[] };

/** Ancho de la tarjeta en pantalla; se captura a 1080×1350 (4:5). */
export const CARD_WIDTH = 360;
const TILES_HEIGHT = 54;

/**
 * Tarjeta del final para compartir: ciudad, ruta, final conseguido, estrellas y coleccionables,
 * con la cabecera de azulejo. Se dibuja fuera de la vista y se captura como imagen.
 */
export const ShareCard = forwardRef<View, Props>(function ShareCard({ route, city, ending, stars, rewards }, ref) {
  const { t, L } = useI18n();
  const app = Constants.expoConfig?.name ?? "";
  return (
    <View ref={ref} collapsable={false} style={styles.card}>
      <View style={styles.tiles}>
        <AzulejoBackground size={{ width: CARD_WIDTH, height: TILES_HEIGHT }} />
      </View>
      <View style={styles.body}>
        <Text style={styles.city}>{city.toUpperCase()}</Text>
        <Text style={styles.route}>{L(route.title)}</Text>
        <ThemeBadge route={route} />
        <View style={styles.endingBox}>
          <Text style={styles.label}>{t("final.tuFinal").toUpperCase()}</Text>
          <Text style={styles.ending}>{ending}</Text>
          <Stars value={stars} size={30} label={t("final.estrellas", { n: stars })} />
        </View>
        <View style={styles.rewards}>
          {rewards.slice(0, 6).map((r) => (
            <CollectibleArt key={r.id} icon={r.icon} size={52} />
          ))}
        </View>
      </View>
      <View style={styles.footer}>
        <Text style={styles.footerText}>{t("final.tarjetaPie", { app })}</Text>
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    height: (CARD_WIDTH * 5) / 4,
    backgroundColor: colors.cream,
    borderWidth: border.thick,
    borderColor: colors.ink,
    borderRadius: radius.lg,
    overflow: "hidden",
  },
  tiles: { height: TILES_HEIGHT, overflow: "hidden", borderBottomWidth: border.thick, borderColor: colors.ink },
  body: { flex: 1, padding: 20, gap: 10, alignItems: "center" },
  city: { fontFamily: fonts.bold, fontSize: 13, letterSpacing: 2, color: colors.sea },
  route: { fontFamily: fonts.display, fontSize: 22, lineHeight: 26, color: colors.ink, textAlign: "center" },
  endingBox: {
    alignSelf: "stretch",
    alignItems: "center",
    gap: 6,
    padding: 14,
    backgroundColor: colors.paper,
    borderWidth: border.thick,
    borderColor: colors.ink,
    borderRadius: radius.md,
  },
  label: { fontFamily: fonts.bold, fontSize: 11, letterSpacing: 1.5, color: colors.muted },
  ending: { fontFamily: fonts.display, fontSize: 26, lineHeight: 30, color: colors.clay, textAlign: "center" },
  rewards: { flexDirection: "row", flexWrap: "wrap", justifyContent: "center", gap: 6 },
  footer: { backgroundColor: colors.ink, paddingVertical: 10, alignItems: "center" },
  footerText: { fontFamily: fonts.bold, fontSize: 12, color: colors.paper },
});
