import type { AssetRef, Challenge, Choice, ContentBlock, Expression, I18nText, LangCode, Route, StoryNode } from "@/content/types";
import { availableChoices, getNode, resolveText } from "./runner";

/**
 * Secuencia de pasos que la pantalla de juego muestra dentro de un nodo:
 * textos → reto → pista → decisión / seguir / final. Sin cadenas de interfaz:
 * la pantalla decide cómo rotular cada tipo.
 */
export type SceneStep =
  | {
      kind: "text";
      source: Exclude<ContentBlock["type"], "scene">;
      text: I18nText;
      characterId?: string;
      expression?: Expression;
      legend?: boolean;
      year?: number;
      /** Locución por idioma (ruta del pack), si la hay. */
      audio?: Partial<Record<LangCode, AssetRef>>;
    }
  | { kind: "challenge"; challenge: Challenge }
  | { kind: "clue"; text: I18nText }
  | { kind: "decision"; intro?: { characterId: string; expression?: Expression; text: I18nText }; choices: Choice[] }
  /** Ir a la siguiente parada física (los nodos narrativos se encadenan sin este paso). */
  | { kind: "continue"; hint?: I18nText; nextTitle: I18nText }
  | { kind: "ending" };

export function buildSteps(route: Route, node: StoryNode, flags: readonly string[]): SceneStep[] {
  const steps: SceneStep[] = [];
  for (const block of node.content) {
    if (block.type === "scene") continue;
    const text = resolveText(block, flags);
    if (!text) continue;
    steps.push({
      kind: "text",
      source: block.type,
      text,
      characterId: block.type === "dialogue" ? block.characterId : undefined,
      expression: block.type === "dialogue" ? block.expression : undefined,
      legend: block.type === "anecdote" ? block.legend : undefined,
      year: block.type === "historical_fact" ? block.year : undefined,
      audio: block.type === "dialogue" || block.type === "narration" ? block.audio : undefined,
    });
  }
  if (node.challenge) steps.push({ kind: "challenge", challenge: node.challenge });
  if (node.clue) steps.push({ kind: "clue", text: node.clue.text });

  if (node.choices) {
    // Sin decisionIntro, la pregunta la plantea el último diálogo del nodo.
    const lastDialogue = [...steps].reverse().find((s) => s.kind === "text" && s.source === "dialogue");
    const intro =
      node.decisionIntro ??
      (lastDialogue?.kind === "text" && lastDialogue.characterId
        ? { characterId: lastDialogue.characterId, expression: lastDialogue.expression, text: lastDialogue.text }
        : undefined);
    steps.push({ kind: "decision", intro, choices: availableChoices(node, flags) });
  } else if (node.isEnding) {
    steps.push({ kind: "ending" });
  } else if (node.nextNodeId) {
    const next = getNode(route, node.nextNodeId);
    if (node.nextHint || next.location) steps.push({ kind: "continue", hint: node.nextHint, nextTitle: next.title });
  }
  return steps;
}

/** Minúsculas, sin tildes ni signos: "¡La Derecha!" → "la derecha". */
export function normalizeAnswer(input: string): string {
  return input
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9ñ ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

/** Respuesta de un reto "observe": vale si coincide con alguna aceptada o la contiene como palabra. */
export function checkObserveAnswer(accepted: readonly string[], input: string): boolean {
  const answer = normalizeAnswer(input);
  if (!answer) return false;
  return accepted.some((a) => {
    const ok = normalizeAnswer(a);
    return answer === ok || ` ${answer} `.includes(` ${ok} `);
  });
}
