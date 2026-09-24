import type { PlayerProgress, Route } from "@/content/types";
import { getNode } from "@/engine/runner";

/**
 * Clave de escena de un `background` del pack: "fondos/fondo_marina.svg" → "marina".
 * Coincide con los nombres de assets/backgrounds/layers/bg_{clave}_….
 */
export function sceneKeyOf(background: string | undefined): string | undefined {
  if (!background) return undefined;
  const file = background.split("/").pop() ?? "";
  const key = file.replace(/\.[a-z0-9]+$/i, "").replace(/^fondo_/, "");
  return key || undefined;
}

/**
 * Escena del nodo actual. Los nodos narrativos (sin fondo propio) siguen en el
 * escenario de la última parada visitada que lo tenga.
 */
export function sceneKeyFor(route: Route, run: PlayerProgress): string | undefined {
  const own = sceneKeyOf(getNode(route, run.currentNodeId).background);
  if (own) return own;
  for (let i = run.visitedNodeIds.length - 1; i >= 0; i--) {
    const key = sceneKeyOf(route.nodes.find((n) => n.id === run.visitedNodeIds[i])?.background);
    if (key) return key;
  }
  return undefined;
}
