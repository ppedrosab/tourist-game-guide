import { Text } from "react-native";
import type { StoryNode } from "@/content/types";
import { localize } from "@/engine/runner";
import { colors, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Panel } from "../ui/Panel";

type Props = { node: StoryNode; demoMode: boolean; onArrive: () => void };

/**
 * Espera a que el jugador llegue a una parada con ubicación. En modo demo,
 * "Simular llegada" permite jugar desde casa. Fase 4: el geofence llamará a
 * `onArrive` y "Ya estoy aquí" quedará como respaldo si el GPS falla.
 */
export function ArrivalPanel({ node, demoMode, onArrive }: Props) {
  return (
    <Panel nameplate="Próxima parada" nameplateColor={colors.sea}>
      <Text style={type.title}>{localize(node.title)}</Text>
      <Text style={type.body}>Camina hasta aquí: la escena empezará cuando llegues.</Text>
      {demoMode ? (
        <Button3D label="Simular llegada" icon="pin" variant="sea" onPress={onArrive} />
      ) : (
        <Button3D label="Ya estoy aquí" icon="pin" variant="sea" onPress={onArrive} />
      )}
    </Panel>
  );
}
