import { z } from "zod";
import type { CityPack } from "@/content/types";

/**
 * Esquema zod espejo de `src/content/types.ts`. Si cambias un tipo allí,
 * cambia aquí también: la comprobación del final del archivo rompe el
 * typecheck si ambos se desincronizan.
 */

const i18nText = z.object({ es: z.string().min(1) }).catchall(z.string());
const assetRef = z.string().min(1);
const latLng = z.object({ lat: z.number().min(-90).max(90), lng: z.number().min(-180).max(180) });
const audio = z.record(z.string(), assetRef);

const expression = z.enum(["neutral", "talking", "happy", "thinking", "surprised", "nervous", "proud", "dramatic"]);
const branchId = z.enum(["dinero", "poder"]);
const flags = z.array(z.string().min(1));

const variant = z.object({ requires: flags, text: i18nText });

const contentBlock = z.discriminatedUnion("type", [
  z
    .object({
      type: z.literal("dialogue"),
      characterId: z.string(),
      expression: expression.optional(),
      text: i18nText.optional(),
      variants: z.array(variant).optional(),
      audio: audio.optional(),
    })
    .refine((b) => b.text !== undefined || (b.variants !== undefined && b.variants.length > 0), {
      message: "un diálogo necesita `text` o al menos una variante",
    }),
  z.object({ type: z.literal("narration"), text: i18nText, audio: audio.optional() }),
  z.object({
    type: z.literal("scene"),
    layers: z.array(assetRef),
    characters: z.array(z.object({ id: z.string(), expression, position: z.enum(["left", "right"]) })),
  }),
  z.object({ type: z.literal("then_now"), then: assetRef, now: assetRef, caption: i18nText.optional() }),
  z.object({ type: z.literal("historical_fact"), text: i18nText, year: z.number().int().optional() }),
  z.object({ type: z.literal("anecdote"), text: i18nText, legend: z.boolean().optional(), source: z.string().optional() }),
  z.object({ type: z.literal("image"), src: assetRef, caption: i18nText.optional() }),
]);

const challenge = z.discriminatedUnion("type", [
  z
    .object({
      type: z.literal("quiz"),
      question: i18nText,
      options: z.array(i18nText).min(2),
      correctIndex: z.number().int().min(0),
      explanation: i18nText.optional(),
    })
    .refine((c) => c.correctIndex < c.options.length, {
      message: "`correctIndex` apunta fuera de `options`",
      path: ["correctIndex"],
    }),
  z.object({ type: z.literal("observe"), prompt: i18nText, answer: z.array(z.string().min(1)).min(1) }),
  z.object({ type: z.literal("photo"), prompt: i18nText }),
]);

const choice = z.object({
  label: i18nText,
  hint: i18nText.optional(),
  targetNodeId: z.string(),
  setFlags: flags.optional(),
  requires: flags.optional(),
  distanceM: z.number().nonnegative().optional(),
  walkMin: z.number().nonnegative().optional(),
});

const storyNode = z.object({
  id: z.string().min(1),
  title: i18nText,
  location: latLng.optional(),
  triggerRadiusM: z.number().positive().optional(),
  branch: branchId.optional(),
  background: assetRef.optional(),
  content: z.array(contentBlock),
  challenge: challenge.optional(),
  clue: z.object({ id: z.string().min(1), text: i18nText }).optional(),
  reward: z.string().optional(),
  decisionIntro: z.object({ characterId: z.string(), expression: expression.optional(), text: i18nText }).optional(),
  choices: z.array(choice).min(1).optional(),
  nextNodeId: z.string().optional(),
  nextHint: i18nText.optional(),
  isEnding: z.boolean().optional(),
});

const route = z.object({
  id: z.string().min(1),
  title: i18nText,
  summary: i18nText,
  era: z.string(),
  guideCharacterId: z.string(),
  durationMin: z.number().positive(),
  distanceKm: z.number().positive(),
  difficulty: z.enum(["easy", "medium", "hard"]),
  isFree: z.boolean(),
  structure: z.enum(["linear", "branch-and-bottleneck"]).optional(),
  startNodeId: z.string(),
  nodes: z.array(storyNode).min(1),
  endings: z.array(z.object({ id: z.string().min(1), requires: flags, title: i18nText })).optional(),
  rewards: z
    .array(z.object({ id: z.string().min(1), name: i18nText, icon: assetRef, awardedAtNodeId: z.string() }))
    .optional(),
});

export const cityPackSchema = z.object({
  id: z.string().min(1),
  version: z.number().int().positive(),
  name: i18nText,
  languages: z.array(z.string()).min(1),
  center: latLng,
  bounds: z.tuple([latLng, latLng]),
  coverImage: assetRef,
  characters: z.array(
    z.object({ id: z.string().min(1), name: i18nText, description: i18nText, avatar: assetRef, era: z.string().optional() }),
  ),
  routes: z.array(route).min(1),
});

// Comprobación en tiempo de compilación: lo que valida zod es un CityPack.
type Assert<T extends true> = T;
export type _SchemaMatchesTypes = Assert<z.infer<typeof cityPackSchema> extends CityPack ? true : false>;
