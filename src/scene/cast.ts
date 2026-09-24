import type { CityPack, Expression, Route, StoryNode } from "@/content/types";
import type { SceneStep } from "@/engine/scene";
import { SPRITES } from "./assets.generated";

export type Position = "left" | "right";

export type CastMember = {
  characterId: string;
  /** Carpeta del sprite en assets/sprites (sale del `avatar` del personaje). */
  sprite: string;
  position: Position;
  expression: Expression;
  speaking: boolean;
};

/** "sprites/manquita/manquita_neutral.svg" → "manquita". */
export function spriteKeyOf(avatar: string | undefined): string | undefined {
  const m = avatar ? /(?:^|\/)sprites\/([^/]+)\//.exec(avatar) : null;
  return m?.[1];
}

/** Quién habla en un paso, y con qué cara (misma lógica que los rótulos de la caja de diálogo). */
export function speakerOf(step: SceneStep | undefined, guideId: string): { id: string; expression?: Expression } | undefined {
  if (!step) return undefined;
  switch (step.kind) {
    case "text":
      return step.source === "dialogue" && step.characterId ? { id: step.characterId, expression: step.expression } : undefined;
    case "decision":
      return { id: step.intro?.characterId ?? guideId, expression: step.intro?.expression ?? "thinking" };
    case "continue":
      return { id: guideId, expression: "happy" };
    case "ending":
      return { id: guideId, expression: "proud" };
    default:
      return undefined;
  }
}

/**
 * Reparto en escena: el del último bloque `scene` del nodo (o el guía a la
 * izquierda si no hay), más quien hable en el paso actual, que ocupa el hueco
 * libre. Solo personajes con sprite; como mucho uno a cada lado.
 */
export function stageCast(pack: CityPack, route: Route, node: StoryNode, step: SceneStep | undefined): CastMember[] {
  const spriteOf = (id: string) => {
    const key = spriteKeyOf(pack.characters.find((c) => c.id === id)?.avatar);
    return key && SPRITES[key] ? key : undefined;
  };
  const sceneBlock = [...node.content].reverse().find((b) => b.type === "scene");
  const base =
    sceneBlock?.type === "scene"
      ? sceneBlock.characters.map((c) => ({ id: c.id, expression: c.expression, position: c.position }))
      : [{ id: route.guideCharacterId, expression: "neutral" as Expression, position: "left" as Position }];

  const cast: CastMember[] = [];
  for (const b of base) {
    const sprite = spriteOf(b.id);
    if (sprite && !cast.some((c) => c.position === b.position)) {
      cast.push({ characterId: b.id, sprite, position: b.position, expression: b.expression, speaking: false });
    }
  }

  const speaker = speakerOf(step, route.guideCharacterId);
  const sprite = speaker && spriteOf(speaker.id);
  if (speaker && sprite) {
    const present = cast.find((c) => c.characterId === speaker.id);
    if (present) {
      present.speaking = true;
      present.expression = speaker.expression ?? present.expression;
    } else {
      // Hueco libre; si no lo hay, sustituye a quien no sea el guía (o al de la derecha).
      const free: Position = !cast.some((c) => c.position === "left") ? "left" : "right";
      const taken = cast.findIndex((c) => c.position === free);
      const member: CastMember = {
        characterId: speaker.id,
        sprite,
        position: free,
        expression: speaker.expression ?? "talking",
        speaking: true,
      };
      if (taken >= 0) cast[taken] = member;
      else cast.push(member);
    }
  }
  return cast.sort((a, b) => (a.position === b.position ? 0 : a.position === "left" ? -1 : 1));
}
