import type { Challenge, Choice, ContentBlock, Expression, I18nText, StoryNode } from "@/content/types";
import { availableChoices, resolveText } from "./runner";

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
    }
  | { kind: "challenge"; challenge: Challenge }
  | { kind: "clue"; text: I18nText }
  | { kind: "decision"; intro?: { characterId: string; expression?: Expression; text: I18nText }; choices: Choice[] }
  | { kind: "continue"; hint?: I18nText }
  | { kind: "ending" };

export function buildSteps(node: StoryNode, flags: readonly string[]): SceneStep[] {
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
    });
  }
  if (node.challenge) steps.push({ kind: "challenge", challenge: node.challenge });
  if (node.clue) steps.push({ kind: "clue", text: node.clue.text });

  if (node.choices) steps.push({ kind: "decision", intro: node.decisionIntro, choices: availableChoices(node, flags) });
  else if (node.isEnding) steps.push({ kind: "ending" });
  else steps.push({ kind: "continue", hint: node.nextHint });
  return steps;
}

/** Minúsculas, sin tildes ni signos: "¡La Derecha!" → "la derecha". */
export function normalizeAnswer(input: string): string {
  return input
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
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
