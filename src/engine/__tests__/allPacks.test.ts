import type { CityPack, PlayerProgress, Route } from "@/content/types";
import { COLLECTIBLE_ART, SCENE_LAYERS, SPRITES, THEN_NOW_ART } from "@/scene/assets.generated";
import { spriteKeyOf } from "@/scene/cast";
import { sceneKeyOf } from "@/scene/sceneFor";
import { BUNDLED_PACKS } from "../catalog";
import { loadPack } from "../loadPack";
import { advance, availableChoices, getNode, isFinished, startRoute } from "../runner";
import { missingTranslations } from "../translations";

/**
 * Comprobaciones que debe cumplir cualquier ciudad incluida en la app: añadir un
 * pack a `BUNDLED_PACKS` basta para que se le apliquen.
 */
const T = "2026-01-01T10:00:00.000Z";
const EXPRESSIONS = ["neutral", "talking", "happy", "thinking", "surprised", "nervous", "proud", "dramatic"];

const packs: [string, CityPack][] = Object.entries(BUNDLED_PACKS).map(([source, raw]) => {
  const result = loadPack(raw);
  if (!result.ok) throw new Error(`${source}:\n${result.errors.join("\n")}`);
  return [source, result.pack];
});
const routes: [string, CityPack, Route][] = packs.flatMap(([, pack]) =>
  pack.routes.map((r) => [r.id, pack, r] as [string, CityPack, Route]),
);

/** Juega todas las combinaciones de decisiones y devuelve las partidas terminadas. */
function allPlaythroughs(pack: CityPack, route: Route): PlayerProgress[] {
  const done: PlayerProgress[] = [];
  const explore = (state: PlayerProgress, depth: number) => {
    if (depth > route.nodes.length * 2) throw new Error(`${route.id}: la partida no termina`);
    if (isFinished(state)) return void done.push(state);
    const node = getNode(route, state.currentNodeId);
    if (node.choices) {
      const choices = availableChoices(node, state.flags);
      if (choices.length === 0) throw new Error(`${route.id}: ${node.id} no tiene decisiones disponibles`);
      for (const c of choices) explore(advance(route, state, c, T), depth + 1);
    } else explore(advance(route, state, undefined, T), depth + 1);
  };
  explore(startRoute(pack.id, route, T), 0);
  return done;
}

describe.each(packs)("pack %s", (_source, pack) => {
  it("está completo en todos sus idiomas", () => {
    expect(pack.languages).toEqual(expect.arrayContaining(["es", "en"]));
    expect(missingTranslations(pack)).toEqual([]);
  });

  it("cada personaje tiene sprite con las 8 expresiones", () => {
    for (const c of pack.characters) {
      const key = spriteKeyOf(c.avatar);
      expect([c.id, key && SPRITES[key] !== undefined]).toEqual([c.id, true]);
      expect(Object.keys(SPRITES[key!].faces).sort()).toEqual([...EXPRESSIONS].sort());
    }
  });
});

/** Personajes que aparecen en una ruta: guía, hablantes, reparto de escena y quien presenta las decisiones. */
function routeCharacters(route: Route): Set<string> {
  const ids = new Set([route.guideCharacterId]);
  for (const node of route.nodes) {
    if (node.decisionIntro) ids.add(node.decisionIntro.characterId);
    for (const block of node.content) {
      if (block.type === "dialogue") ids.add(block.characterId);
      if (block.type === "scene") for (const c of block.characters) ids.add(c.id);
    }
  }
  return ids;
}

describe.each(packs)("reparto del pack %s", (_source, pack) => {
  it("ningún personaje se repite entre las rutas de la ciudad", () => {
    const owner = new Map<string, string>();
    const repeated: string[] = [];
    for (const route of pack.routes)
      for (const id of routeCharacters(route)) {
        const first = owner.get(id);
        if (first && first !== route.id) repeated.push(`${id} (${first} y ${route.id})`);
        else owner.set(id, route.id);
      }
    expect(repeated).toEqual([]);
  });
});

describe("colección compartida", () => {
  // La colección junta coleccionables, finales y pistas de todas las ciudades en una sola lista
  // de ids: si dos rutas repiten uno, ganarlo en una lo marca también en la otra.
  const kinds: [string, (r: Route) => string[]][] = [
    ["coleccionables", (r) => (r.rewards ?? []).map((c) => c.id)],
    ["finales", (r) => (r.endings ?? []).map((e) => e.id)],
    ["pistas", (r) => r.nodes.flatMap((n) => (n.clue ? [n.clue.id] : []))],
  ];
  it.each(kinds)("los ids de %s no se repiten entre rutas", (_kind, idsOf) => {
    const owner = new Map<string, string>();
    const repeated: string[] = [];
    for (const [, , route] of routes)
      for (const id of idsOf(route)) {
        const first = owner.get(id);
        if (first && first !== route.id) repeated.push(`${id} (${first} y ${route.id})`);
        else owner.set(id, route.id);
      }
    expect(repeated).toEqual([]);
  });
});

describe.each(routes)("ruta %s", (_id, pack, route) => {
  it("todos los finales son alcanzables y toda partida acaba en uno", () => {
    const games = allPlaythroughs(pack, route);
    const reached = new Set(games.map((g) => g.endingId));
    expect(reached.has(undefined)).toBe(false);
    expect([...reached].sort()).toEqual((route.endings ?? []).map((e) => e.id).sort());
  });

  it("cada escena tiene sus capas de parallax", () => {
    const keys = route.nodes.map((n) => sceneKeyOf(n.background)).filter((k): k is string => !!k);
    expect(keys.length).toBeGreaterThan(0);
    for (const key of keys) expect([key, SCENE_LAYERS[key] !== undefined]).toEqual([key, true]);
  });

  it("cada coleccionable y cada 'antes y ahora' tiene su arte", () => {
    for (const c of route.rewards ?? []) expect([c.icon, COLLECTIBLE_ART[c.icon] !== undefined]).toEqual([c.icon, true]);
    for (const b of route.nodes.flatMap((n) => n.content)) {
      if (b.type === "then_now") expect([b.then, THEN_NOW_ART[b.then] !== undefined]).toEqual([b.then, true]);
    }
  });

  it("las rutas ramificadas nombran sus dos caminos", () => {
    if (!route.nodes.some((n) => n.branch)) return;
    expect(route.branches?.dinero).toBeDefined();
    expect(route.branches?.poder).toBeDefined();
  });
});

describe("fichas y fuentes", () => {
  const characters = packs.flatMap(([, pack]) => pack.characters.map((c) => [`${pack.id}/${c.id}`, c] as const));

  it.each(characters)("%s tiene ficha: qué es y su historia", (_, c) => {
    expect(c.kind).toBeDefined();
    expect(c.bio?.es.length).toBeGreaterThan(80);
  });

  it.each(characters.filter(([, c]) => c.kind === "real" || c.kind === "leyenda"))(
    "%s cita al menos una referencia",
    (_, c) => {
      expect(c.sources?.length).toBeGreaterThan(0);
    },
  );

  it.each(routes.filter(([, , r]) => r.theme === "leyendas"))("%s se juega al anochecer", (_, pack, route) => {
    expect(route.bestTime).toBe("noche");
    expect(pack.timeZone).toBeDefined();
  });

  it.each(routes)("%s cita sus fuentes", (_, __, route) => {
    expect(route.sources?.length).toBeGreaterThan(0);
  });
});
