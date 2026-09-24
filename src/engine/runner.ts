import type {
  BranchId,
  Choice,
  ContentBlock,
  Ending,
  I18nText,
  LangCode,
  PlayerProgress,
  Route,
  StoryNode,
} from "@/content/types";

/**
 * Motor narrativo: funciones puras sobre el grafo de una ruta.
 * No guardan estado ni tocan React; el store y las pantallas las usan.
 */

/** Uso incorrecto del motor (nodo inexistente, decisión no válida…). */
export class RunnerError extends Error {
  name = "RunnerError";
}

const now = () => new Date().toISOString();
const addUnique = (list: string[], items: readonly string[]) => [...list, ...items.filter((i) => !list.includes(i))];

export function hasAllFlags(requires: readonly string[] | undefined, flags: readonly string[]): boolean {
  return (requires ?? []).every((f) => flags.includes(f));
}

export function getNode(route: Route, nodeId: string): StoryNode {
  const node = route.nodes.find((n) => n.id === nodeId);
  if (!node) throw new RunnerError(`La ruta "${route.id}" no tiene el nodo "${nodeId}"`);
  return node;
}

/** Texto en el idioma pedido, con el español como respaldo. */
export function localize(text: I18nText, lang: LangCode = "es"): string {
  return text[lang] ?? text.es;
}

/**
 * Texto que muestra un bloque según los flags del jugador. En los diálogos
 * gana la primera variante cuyos `requires` estén todos en los flags; si
 * ninguna encaja, se usa `text`. Devuelve null si el bloque no tiene texto.
 */
export function resolveText(block: ContentBlock, flags: readonly string[]): I18nText | null {
  switch (block.type) {
    case "dialogue":
      return block.variants?.find((v) => hasAllFlags(v.requires, flags))?.text ?? block.text ?? null;
    case "narration":
    case "historical_fact":
    case "anecdote":
      return block.text;
    case "then_now":
    case "image":
      return block.caption ?? null;
    case "scene":
      return null;
  }
}

export function availableChoices(node: StoryNode, flags: readonly string[]): Choice[] {
  return (node.choices ?? []).filter((c) => hasAllFlags(c.requires, flags));
}

/** Primer final cuyos `requires` cumple el jugador. */
export function resolveEnding(route: Route, flags: readonly string[]): Ending | undefined {
  return route.endings?.find((e) => hasAllFlags(e.requires, flags));
}

/** Nodo con ubicación: la escena espera a que el jugador llegue (geofence o "Simular llegada"). */
export function needsArrival(node: StoryNode): boolean {
  return node.location !== undefined;
}

export function isFinished(state: PlayerProgress): boolean {
  return state.completedAt !== undefined;
}

/** Entrar en un nodo: pasa a ser el actual, queda visitado y, si es el último, fija el final. */
function enterNode(route: Route, state: PlayerProgress, nodeId: string): PlayerProgress {
  const node = getNode(route, nodeId);
  return {
    ...state,
    currentNodeId: node.id,
    visitedNodeIds: addUnique(state.visitedNodeIds, [node.id]),
    endingId: node.isEnding ? resolveEnding(route, state.flags)?.id : state.endingId,
  };
}

/** Completar un nodo (salir de él): se gana su pista y sus coleccionables. */
function completeNode(route: Route, state: PlayerProgress, node: StoryNode): PlayerProgress {
  const rewards = (route.rewards ?? []).filter((r) => r.awardedAtNodeId === node.id).map((r) => r.id);
  if (node.reward) rewards.push(node.reward);
  return {
    ...state,
    clueIds: node.clue ? addUnique(state.clueIds, [node.clue.id]) : state.clueIds,
    collectibleIds: addUnique(state.collectibleIds, rewards),
  };
}

/** Empieza una partida nueva en el nodo inicial de la ruta. */
export function startRoute(cityId: string, route: Route, startedAt: string = now()): PlayerProgress {
  const empty: PlayerProgress = {
    cityId,
    routeId: route.id,
    currentNodeId: route.startNodeId,
    visitedNodeIds: [],
    clueIds: [],
    collectibleIds: [],
    flags: [],
    startedAt,
  };
  return enterNode(route, empty, route.startNodeId);
}

/**
 * Avanza desde el nodo actual. En un nodo de decisión hay que pasar la
 * elección (una de `availableChoices`); en el resto, no. Al salir de un nodo
 * se ganan su pista y sus coleccionables. Avanzar desde el nodo final cierra
 * la partida (`completedAt`).
 */
export function advance(route: Route, state: PlayerProgress, choice?: Choice, at: string = now()): PlayerProgress {
  if (isFinished(state)) throw new RunnerError("La partida ya ha terminado");
  const node = getNode(route, state.currentNodeId);
  const done = completeNode(route, state, node);

  if (node.choices) {
    if (!choice) throw new RunnerError(`El nodo "${node.id}" necesita una decisión`);
    const picked = availableChoices(node, done.flags).find((c) => c.targetNodeId === choice.targetNodeId);
    if (!picked) throw new RunnerError(`La decisión hacia "${choice.targetNodeId}" no está disponible en "${node.id}"`);
    return enterNode(route, { ...done, flags: addUnique(done.flags, picked.setFlags ?? []) }, picked.targetNodeId);
  }
  if (choice) throw new RunnerError(`El nodo "${node.id}" no tiene decisiones`);
  if (node.isEnding) return { ...done, completedAt: at };
  if (!node.nextNodeId) throw new RunnerError(`El nodo "${node.id}" no tiene salida`);
  return enterNode(route, done, node.nextNodeId);
}

// ---------------------------------------------------------------------------
// Paradas para el HUD y los contadores "Parada X de N"
// ---------------------------------------------------------------------------

export type Stop = {
  /** Id del nodo, o `rama:<nodo de decisión>` para una rama aún sin elegir. */
  id: string;
  nodeId?: string;
  branch?: BranchId;
};

/** Distancia en saltos desde `fromId` a cada nodo alcanzable. */
function distances(route: Route, fromId: string): Map<string, number> {
  const dist = new Map<string, number>([[fromId, 0]]);
  const queue = [fromId];
  while (queue.length > 0) {
    const node = getNode(route, queue.shift()!);
    const next = [...(node.choices ?? []).map((c) => c.targetNodeId), ...(node.nextNodeId ? [node.nextNodeId] : [])];
    for (const id of next) {
      if (!dist.has(id)) {
        dist.set(id, dist.get(node.id)! + 1);
        queue.push(id);
      }
    }
  }
  return dist;
}

/** Nodo "cuello de botella" donde se reúnen las ramas de una decisión (el más cercano). */
export function findBottleneck(route: Route, node: StoryNode): string | undefined {
  const maps = (node.choices ?? []).map((c) => distances(route, c.targetNodeId));
  if (maps.length === 0) return undefined;
  let best: string | undefined;
  let bestCost = Infinity;
  for (const [id] of maps[0]) {
    if (!maps.every((m) => m.has(id))) continue;
    const cost = maps.reduce((sum, m) => sum + m.get(id)!, 0);
    if (cost < bestCost) {
      best = id;
      bestCost = cost;
    }
  }
  return best;
}

/** Nodos de una rama, desde su primer nodo hasta (sin incluir) el cuello de botella. */
function branchNodes(route: Route, fromId: string, untilId: string | undefined): StoryNode[] {
  const out: StoryNode[] = [];
  let id: string | undefined = fromId;
  while (id && id !== untilId && out.length < route.nodes.length) {
    const node = getNode(route, id);
    out.push(node);
    id = node.nextNodeId;
  }
  return out;
}

/**
 * Paradas físicas (nodos con ubicación) del recorrido del jugador. Las ramas
 * ya elegidas aparecen con sus paradas reales y su color; una rama pendiente
 * se muestra como una sola parada sin color.
 */
export function routeStops(route: Route, state: PlayerProgress): { stops: Stop[]; current: number } {
  const stops: Stop[] = [];
  let current = 0;
  const visit = (node: StoryNode, stop?: Stop) => {
    if (stop) stops.push(stop);
    if (node.id === state.currentNodeId) current = Math.max(0, stops.length - 1);
  };

  let node: StoryNode | undefined = getNode(route, route.startNodeId);
  for (let guard = 0; node && guard < route.nodes.length; guard++) {
    visit(node, needsArrival(node) ? { id: node.id, nodeId: node.id, branch: node.branch } : undefined);
    if (!node.choices) {
      node = node.nextNodeId ? getNode(route, node.nextNodeId) : undefined;
      continue;
    }
    const bottleneck = findBottleneck(route, node);
    const chosen = node.choices.find((c) => state.visitedNodeIds.includes(c.targetNodeId));
    if (chosen) {
      for (const n of branchNodes(route, chosen.targetNodeId, bottleneck)) {
        visit(n, needsArrival(n) ? { id: n.id, nodeId: n.id, branch: n.branch } : undefined);
      }
    } else {
      const anyPhysical = node.choices.some((c) =>
        branchNodes(route, c.targetNodeId, bottleneck).some(needsArrival),
      );
      if (anyPhysical) stops.push({ id: `rama:${node.id}` });
    }
    node = bottleneck ? getNode(route, bottleneck) : undefined;
  }
  return { stops, current };
}
