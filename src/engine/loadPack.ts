import type { CityPack, Route } from "@/content/types";
import { cityPackSchema } from "./schema";

export type LoadPackResult = { ok: true; pack: CityPack } | { ok: false; errors: string[] };

/**
 * Valida un pack de ciudad (JSON ya parseado) contra el esquema y comprueba
 * que todas las referencias internas existen. Nunca lanza: un pack mal
 * formado devuelve `ok: false` con la lista de errores legibles.
 */
export function loadPack(raw: unknown): LoadPackResult {
  const parsed = cityPackSchema.safeParse(raw);
  if (!parsed.success) {
    return {
      ok: false,
      errors: parsed.error.issues.map((issue) => `${formatPath(issue.path)}: ${issue.message}`),
    };
  }
  // El esquema garantiza la forma; `_SchemaMatchesTypes` garantiza que encaja con CityPack.
  const pack: CityPack = parsed.data;
  const errors = checkReferences(pack);
  return errors.length > 0 ? { ok: false, errors } : { ok: true, pack };
}

function checkReferences(pack: CityPack): string[] {
  const errors: string[] = [];
  const characterIds = new Set<string>();
  for (const c of pack.characters) {
    if (characterIds.has(c.id)) errors.push(`personaje "${c.id}" duplicado`);
    characterIds.add(c.id);
  }

  const routeIds = new Set<string>();
  for (const route of pack.routes) {
    if (routeIds.has(route.id)) errors.push(`ruta "${route.id}" duplicada`);
    routeIds.add(route.id);
    errors.push(...checkRoute(route, characterIds));
  }
  return errors;
}

function checkRoute(route: Route, characterIds: Set<string>): string[] {
  const errors: string[] = [];
  const where = (nodeId?: string) => (nodeId ? `ruta "${route.id}" › nodo "${nodeId}"` : `ruta "${route.id}"`);

  const nodeIds = new Set<string>();
  for (const node of route.nodes) {
    if (nodeIds.has(node.id)) errors.push(`${where(node.id)}: id de nodo duplicado`);
    nodeIds.add(node.id);
  }
  const rewardIds = new Set((route.rewards ?? []).map((r) => r.id));

  const character = (id: string, ctx: string) => {
    if (!characterIds.has(id)) errors.push(`${ctx}: el personaje "${id}" no existe`);
  };
  const target = (id: string, ctx: string, field: string) => {
    if (!nodeIds.has(id)) errors.push(`${ctx}: ${field} "${id}" no existe`);
  };

  if (!nodeIds.has(route.startNodeId)) errors.push(`${where()}: startNodeId "${route.startNodeId}" no existe`);
  character(route.guideCharacterId, `${where()} (guideCharacterId)`);

  for (const node of route.nodes) {
    const ctx = where(node.id);
    for (const block of node.content) {
      if (block.type === "dialogue") character(block.characterId, ctx);
      if (block.type === "scene") block.characters.forEach((c) => character(c.id, ctx));
    }
    if (node.decisionIntro) character(node.decisionIntro.characterId, `${ctx} (decisionIntro)`);
    if (node.nextNodeId) target(node.nextNodeId, ctx, "nextNodeId");
    node.choices?.forEach((c) => target(c.targetNodeId, ctx, "targetNodeId"));
    if (node.reward && !rewardIds.has(node.reward)) errors.push(`${ctx}: la recompensa "${node.reward}" no existe`);

    const exits = (node.nextNodeId ? 1 : 0) + (node.choices ? 1 : 0);
    if (exits > 1) errors.push(`${ctx}: tiene a la vez nextNodeId y choices`);
    if (exits === 0 && !node.isEnding) errors.push(`${ctx}: callejón sin salida (sin nextNodeId, choices ni isEnding)`);
    if (exits > 0 && node.isEnding) errors.push(`${ctx}: un nodo final no puede tener salidas`);
  }

  for (const reward of route.rewards ?? []) {
    target(reward.awardedAtNodeId, `${where()} › recompensa "${reward.id}"`, "awardedAtNodeId");
  }
  return errors;
}

function formatPath(path: PropertyKey[]): string {
  if (path.length === 0) return "(raíz)";
  return path.map((p, i) => (typeof p === "number" ? `[${p}]` : `${i === 0 ? "" : "."}${String(p)}`)).join("");
}
