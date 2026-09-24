import { Text } from "react-native";
import type { StoryNode } from "@/content/types";
import { localize } from "@/engine/runner";
import type { ArrivalWatch } from "@/hooks/useArrivalWatcher";
import { colors, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Panel } from "../ui/Panel";

type Props = { node: StoryNode; demoMode: boolean; watch: ArrivalWatch; onArrive: () => void };

const formatDistance = (m: number) =>
  m < 1000 ? `${Math.max(10, Math.round(m / 10) * 10)} m` : `${(m / 1000).toLocaleString("es-ES", { maximumFractionDigits: 1 })} km`;

function gpsText({ status, distance }: ArrivalWatch): string {
  switch (status) {
    case "asking":
      return "Buscando tu ubicación…";
    case "denied":
      return "No tengo permiso para ver tu ubicación. Puedes activarlo en los ajustes del móvil.";
    case "unavailable":
      return "El GPS no está disponible ahora mismo.";
    case "watching":
      return distance === undefined ? "Buscando señal GPS…" : `Estás a ${formatDistance(distance)}.`;
  }
}

/**
 * Espera a que el jugador llegue a una parada con ubicación. El GPS (y los
 * geofences en segundo plano) marcan la llegada solos; "Ya estoy aquí"
 * aparece si el GPS falla 60 s, y "Simular llegada" en modo demo.
 */
export function ArrivalPanel({ node, demoMode, watch, onArrive }: Props) {
  return (
    <Panel nameplate="Próxima parada" nameplateColor={colors.sea}>
      <Text style={type.title}>{localize(node.title)}</Text>
      <Text style={type.body}>Camina hasta aquí: la escena empezará cuando llegues.</Text>
      <Text style={type.secondary} accessibilityLiveRegion="polite">
        {gpsText(watch)}
      </Text>
      {watch.manualFallback ? (
        <Button3D label="Ya estoy aquí" icon="pin" variant={demoMode ? "secondary" : "sea"} onPress={onArrive} />
      ) : null}
      {demoMode ? <Button3D label="Simular llegada" icon="pin" variant="sea" onPress={onArrive} /> : null}
    </Panel>
  );
}
