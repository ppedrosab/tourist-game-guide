import type { BranchId, Character, CityPack, PlayerProgress, Route, StoryNode } from "@/content/types";
import { findBottleneck, getNode, needsArrival, routeStops } from "./runner";

/** Esquema de una ruta para la pantalla de detalle: paradas, decisiones y ramas. */
export type OutlineItem =
  | { kind: "stop"; node: StoryNode; decision?: number }
  | { kind: "branches"; branches: { branch?: BranchId; nodes: StoryNode[] }[] };

export function routeOutline(route: Route): OutlineItem[] {
  const items: OutlineItem[] = [];
  let decisions = 0;
  let node: StoryNode | undefined = getNode(route, route.startNodeId);
  for (let guard = 0; node && guard < route.nodes.length; guard++) {
    const decision = node.choices ? ++decisions : undefined;
    if (needsArrival(node)) items.push({ kind: "stop", node, decision });
    if (!node.choices) {
      node = node.nextNodeId ? getNode(route, node.nextNodeId) : undefined;
      continue;
    }
    const bottleneck = findBottleneck(route, node);
    const branches = node.choices.map((c) => {
      const nodes: StoryNode[] = [];
      let id: string | undefined = c.targetNodeId;
      while (id && id !== bottleneck && nodes.length < route.nodes.length) {
        const n = getNode(route, id);
        if (needsArrival(n)) nodes.push(n);
        id = n.nextNodeId;
      }
      return { branch: getNode(route, c.targetNodeId).branch, nodes };
    });
    if (branches.some((b) => b.nodes.length > 0)) items.push({ kind: "branches", branches });
    node = bottleneck ? getNode(route, bottleneck) : undefined;
  }
  return items;
}

/** Datos de la ficha: número de caminos (ramas con color) y de finales. */
export function routeFacts(route: Route) {
  const branches = new Set(route.nodes.map((n) => n.branch).filter(Boolean));
  return { branches: branches.size, endings: route.endings?.length ?? 0 };
}

/** Resumen de una partida para "Continuar" y "Mis rutas": parada X de N, nodo actual y camino elegido. */
export function runProgress(route: Route, run: PlayerProgress) {
  const { stops, current } = routeStops(route, run);
  const branch = run.visitedNodeIds.map((id) => route.nodes.find((n) => n.id === id)?.branch).find(Boolean);
  return { stop: current + 1, total: stops.length, node: getNode(route, run.currentNodeId), branch };
}

/**
 * Reparto de una ruta para su ficha: el guía primero y luego por orden de aparición.
 * Con `nodeIds`, solo los que salen en esos nodos (el cuaderno enseña a quien ya has conocido).
 */
export function routeCast(pack: CityPack, route: Route, nodeIds?: string[]): Character[] {
  const ids = [route.guideCharacterId];
  for (const node of route.nodes) {
    if (nodeIds && !nodeIds.includes(node.id)) continue;
    for (const block of node.content) {
      if (block.type === "dialogue") ids.push(block.characterId);
      else if (block.type === "scene") ids.push(...block.characters.map((c) => c.id));
    }
    if (node.decisionIntro) ids.push(node.decisionIntro.characterId);
  }
  return [...new Set(ids)]
    .map((id) => pack.characters.find((c) => c.id === id))
    .filter((c): c is Character => Boolean(c));
}

/** Personajes que el jugador ya ha conocido en una partida, como "ciudad/personaje". */
export function metCharacters(pack: CityPack, route: Route, run: PlayerProgress): string[] {
  return routeCast(pack, route, [...run.visitedNodeIds, run.currentNodeId]).map((c) => `${pack.id}/${c.id}`);
}
