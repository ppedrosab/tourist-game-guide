import { StyleSheet, Text, View } from "react-native";
import { Icon, type IconName } from "@/components/ui/Icon";
import { Panel } from "@/components/ui/Panel";
import type { CityPack, Route } from "@/content/types";
import { routePractical } from "@/engine/practical";
import { useI18n } from "@/i18n";
import { EXTREME_HEAT, HOT_DAY, useTodayMaxTemp } from "@/practical/weather";
import { colors, type } from "@/theme";

/** Por encima de esto el modelo del terreno (25 m) no da una cifra fiable: se dice "más del 20 %". */
const VERY_STEEP = 20;

function Row({ icon, text, tone }: { icon: IconName; text: string; tone?: string }) {
  return (
    <View style={styles.row} accessible accessibilityRole="text" accessibilityLabel={text}>
      <Icon name={icon} size={20} color={tone ?? colors.ink} />
      <Text style={[type.body, styles.text, tone ? { color: tone } : null]}>{text}</Text>
    </View>
  );
}

/** Tarjeta "Antes de salir" del detalle de ruta: cuestas, escaleras, accesibilidad, agua y calor. */
export function PracticalCard({ pack, route }: { pack: CityPack; route: Route }) {
  const { t } = useI18n();
  const max = useTodayMaxTemp(pack);
  const p = routePractical(route);
  if (!p) return null;
  const hot = max !== null && max >= HOT_DAY;
  return (
    <Panel>
      <Text style={type.overline}>{t("practico.titulo")}</Text>
      {hot ? (
        <Row
          icon="heat"
          tone={colors.clay}
          text={t(max >= EXTREME_HEAT ? "practico.calorExtremo" : "practico.calor", { temp: max })}
        />
      ) : null}
      <Row
        icon="slope"
        text={
          p.gentle && p.up < 20
            ? t("practico.llana", { up: p.up })
            : p.grade > VERY_STEEP
              ? t("practico.muyCuestas", { up: p.up })
              : t("practico.cuestas", { up: p.up, grade: p.grade })
        }
      />
      <Row
        icon="stairs"
        text={
          p.stepLegs === 0
            ? t("practico.sinEscaleras")
            : p.stepLegs === 1
              ? t("practico.escalerasUno")
              : t("practico.escaleras", { n: p.stepLegs })
        }
      />
      <Row icon="wheelchair" text={p.stepFree && p.gentle ? t("practico.accesible") : t("practico.noAccesible")} />
      <Row
        icon="water"
        tone={p.waterStops === 0 ? colors.clay : undefined}
        text={p.waterStops === 0 ? t("practico.sinAgua") : t("practico.agua", { n: p.waterStops, total: p.stops })}
      />
      <Text style={type.caption}>{t("practico.estimacion")}</Text>
    </Panel>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", alignItems: "center", gap: 10 },
  text: { flex: 1 },
});
