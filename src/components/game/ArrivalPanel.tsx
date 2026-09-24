import { Text } from "react-native";
import type { StoryNode } from "@/content/types";
import { radiusOf } from "@/engine/geo";
import { useI18n } from "@/i18n";
import type { ArrivalWatch } from "@/hooks/useArrivalWatcher";
import { colors, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Panel } from "../ui/Panel";

type Props = {
  node: StoryNode;
  demoMode: boolean;
  watch: ArrivalWatch;
  onArrive: (method: "manual" | "demo") => void;
  /** Modo prueba de campo: muestra precisión, distancia y radio. */
  fieldTest?: boolean;
};

function gpsText({ status, distance }: ArrivalWatch, { t, distance: fmt }: ReturnType<typeof useI18n>): string {
  switch (status) {
    case "asking":
      return t("jugar.gpsBuscando");
    case "denied":
      return t("jugar.gpsSinPermiso");
    case "unavailable":
      return t("jugar.gpsNoDisponible");
    case "watching":
      return distance === undefined ? t("jugar.gpsSenal") : t("jugar.estasA", { distance: fmt(distance) });
  }
}

/**
 * Espera a que el jugador llegue a una parada con ubicación. El GPS (y los
 * geofences en segundo plano) marcan la llegada solos; "Ya estoy aquí"
 * aparece si el GPS falla 60 s, y "Simular llegada" en modo demo.
 */
export function ArrivalPanel({ node, demoMode, watch, onArrive, fieldTest }: Props) {
  const i18n = useI18n();
  const { t, L } = i18n;
  return (
    <Panel nameplate={t("jugar.proximaParada")} nameplateColor={colors.sea}>
      <Text style={type.title}>{L(node.title)}</Text>
      <Text style={type.body}>{t("jugar.caminaHasta")}</Text>
      <Text style={type.secondary} accessibilityLiveRegion="polite">
        {gpsText(watch, i18n)}
      </Text>
      {fieldTest ? (
        <Text style={[type.caption, { color: colors.sea }]} testID="diagnostico-campo">
          {watch.lastFix && watch.distance !== undefined
            ? t("campo.diagnostico", {
                accuracy: Math.round(watch.lastFix.accuracy ?? 0),
                distance: i18n.distance(watch.distance),
                radius: radiusOf(node),
              })
            : t("campo.sinSenal")}
        </Text>
      ) : null}
      {watch.manualFallback ? (
        <Button3D
          label={t("jugar.yaEstoy")}
          icon="pin"
          variant={demoMode ? "secondary" : "sea"}
          onPress={() => onArrive("manual")}
        />
      ) : null}
      {demoMode ? (
        <Button3D label={t("jugar.simular")} icon="pin" variant="sea" onPress={() => onArrive("demo")} />
      ) : null}
    </Panel>
  );
}
