import { router } from "expo-router";
import { Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { ReactNode } from "react";
import { Button3D, Icon, IconName, Panel, ThemeBadge } from "@/components/ui";
import { routeStops } from "@/engine/runner";
import { useI18n } from "@/i18n";
import { useCurrentRun } from "@/hooks/useCurrentRun";
import { useProgress } from "@/store/progress";
import { border, colors, radius, type } from "@/theme";

function Row({
  icon,
  title,
  sub,
  onPress,
  right,
}: {
  icon: IconName;
  title: string;
  sub: string;
  onPress?: () => void;
  right?: ReactNode;
}) {
  return (
    <Pressable
      onPress={onPress}
      disabled={!onPress}
      accessibilityRole={onPress ? "button" : undefined}
      style={styles.row}
    >
      <View style={styles.rowIcon}>
        <Icon name={icon} size={18} />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={type.label}>{title}</Text>
        <Text style={type.caption}>{sub}</Text>
      </View>
      {right ?? <Icon name="next" size={16} strokeWidth={2.4} />}
    </Pressable>
  );
}

/** Modal de pausa: se abre desde el HUD y vuelve exactamente al mismo punto. */
export default function Pausa() {
  const { t, L } = useI18n();
  const voces = useProgress((s) => s.voices);
  const setVoces = useProgress((s) => s.setVoices);
  const subtitulos = useProgress((s) => s.subtitles);
  const setSubtitulos = useProgress((s) => s.setSubtitles);
  const current = useCurrentRun();
  const where = (() => {
    if (!current) return "";
    const { route, run } = current;
    const { stops, current: index } = routeStops(route, run);
    const node = route.nodes.find((n) => n.id === run.currentNodeId);
    return `${t("comun.paradaDe", { n: index + 1, total: stops.length })}${node ? ` · ${L(node.title)}` : ""}`;
  })();
  return (
    <View style={styles.overlay}>
      <Panel nameplate={t("pausa.titulo")} nameplateColor={colors.ink} style={{ gap: 10 }}>
        <Text style={type.subtitle}>{current ? L(current.route.title) : ""}</Text>
        {current ? <ThemeBadge route={current.route} /> : null}
        <Text style={type.caption}>{where}</Text>
        <Button3D label={t("pausa.continuar")} icon="play" onPress={() => router.back()} />
        <Row icon="map" title={t("pausa.verMapa")} sub={t("pausa.verMapaTexto")} onPress={() => router.replace("/mapa")} />
        <Row
          icon="book"
          title={t("jugar.cuaderno")}
          sub={t("pausa.cuadernoTexto")}
          onPress={() => router.replace("/cuaderno")}
        />
        <Row
          icon="volume"
          title={t("pausa.voces")}
          sub={t("pausa.vocesTexto")}
          right={<Switch value={voces} onValueChange={setVoces} trackColor={{ true: colors.sea }} />}
        />
        <Row
          icon="subtitles"
          title={t("pausa.subtitulos")}
          sub={t("pausa.subtitulosTexto")}
          right={<Switch value={subtitulos} onValueChange={setSubtitulos} trackColor={{ true: colors.sea }} />}
        />
        <Row icon="exit" title={t("pausa.salir")} sub={t("pausa.salirTexto")} onPress={() => router.dismissTo("/")} />
      </Panel>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: { flex: 1, justifyContent: "center", padding: 16, backgroundColor: "rgba(27,42,58,0.62)" },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    padding: 10,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  rowIcon: {
    width: 38,
    height: 38,
    borderRadius: 11,
    backgroundColor: colors.sand,
    alignItems: "center",
    justifyContent: "center",
  },
});
