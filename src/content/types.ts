/**
 * Modelo de contenido: el motor solo entiende estos tipos.
 * Cada ciudad es un "pack" JSON que cumple este esquema (ver content/malaga).
 * En la fase 2 se añade la validación en tiempo de carga con zod.
 */
export type LangCode = "es" | "en" | (string & {});
export type I18nText = Partial<Record<LangCode, string>> & { es: string };
export type AssetRef = string;
export type LatLng = { lat: number; lng: number };

export type Expression = "neutral" | "talking" | "happy" | "thinking" | "surprised" | "nervous" | "proud" | "dramatic";
/**
 * Huecos de camino: cada ruta ramificada tiene dos. Los nombres internos vienen de Málaga, pero
 * cada ruta puede llamarlos como quiera con `Route.branches` (en Cádiz: mar y ciudad).
 * El color va con el hueco: "dinero" = mar (sea), "poder" = arcilla (clay).
 */
export type BranchId = "dinero" | "poder";

/** Tipo de ruta: de historia (por defecto), gastronómica, de fiestas o de leyendas. Se muestra como una seña en la interfaz. */
export type RouteTheme = "historia" | "gastronomia" | "fiestas" | "leyendas";

/** Cómo se llama un camino en una ruta: `name` para leyendas ("Mar"), `trail` en frases ("camino del mar"). */
export interface BranchLabel {
  name: I18nText;
  trail: I18nText;
}

export interface CityPack {
  id: string;
  version: number;
  name: I18nText;
  languages: LangCode[];
  center: LatLng;
  bounds: [LatLng, LatLng];
  coverImage: AssetRef;
  characters: Character[];
  routes: Route[];
}

/** Qué es un personaje: persona real, figura de una leyenda, figura típica de la ciudad o un símbolo suyo que habla (un monumento, una marioneta…). */
export type CharacterKind = "real" | "leyenda" | "tipo" | "simbolo";

/** Referencia para saber más: la cita tal cual (no se traduce) y, si hay, un enlace. */
export interface Source {
  title: string;
  url?: string;
}

export interface Character {
  id: string;
  name: I18nText;
  description: I18nText;
  avatar: AssetRef;
  era?: string;
  kind?: CharacterKind;
  /** Años de vida ("1860-1935") o época ("s. XI") de una persona real. */
  lived?: string;
  /** Su historia, para la ficha del personaje. */
  bio?: I18nText;
  sources?: Source[];
}

export interface Route {
  id: string;
  title: I18nText;
  summary: I18nText;
  era: string;
  guideCharacterId: string;
  durationMin: number;
  distanceKm: number;
  difficulty: "easy" | "medium" | "hard";
  isFree: boolean;
  structure?: "linear" | "branch-and-bottleneck";
  /** Sin `theme` es una ruta de historia. */
  theme?: RouteTheme;
  /** Nombres de los caminos en esta ruta; si faltan, se usan "dinero" y "poder" de la interfaz. */
  branches?: Partial<Record<BranchId, BranchLabel>>;
  startNodeId: string;
  nodes: StoryNode[];
  endings?: Ending[];
  rewards?: Collectible[];
  /** Fuentes de la ruta: de dónde salen la historia y los datos. */
  sources?: Source[];
}

export interface StoryNode {
  id: string;
  title: I18nText;
  /** Sin location = nodo narrativo: se lanza en cuanto termina el anterior. */
  location?: LatLng;
  triggerRadiusM?: number;
  branch?: BranchId;
  background?: AssetRef;
  content: ContentBlock[];
  challenge?: Challenge;
  clue?: { id: string; text: I18nText };
  reward?: string;
  decisionIntro?: { characterId: string; expression?: Expression; text: I18nText };
  choices?: Choice[];
  nextNodeId?: string;
  nextHint?: I18nText;
  isEnding?: boolean;
}

/** Texto alternativo que se usa si el jugador tiene todos los flags de `requires`. */
export interface Variant {
  requires: string[];
  text: I18nText;
}

export type ContentBlock =
  | { type: "dialogue"; characterId: string; expression?: Expression; text?: I18nText; variants?: Variant[]; audio?: Partial<Record<LangCode, AssetRef>> }
  | { type: "narration"; text: I18nText; audio?: Partial<Record<LangCode, AssetRef>> }
  | { type: "scene"; layers: AssetRef[]; characters: { id: string; expression: Expression; position: "left" | "right" }[] }
  /** `then`: ilustración de época. `now`: "camera" (cámara en directo) o una imagen. */
  | { type: "then_now"; then: AssetRef; now: AssetRef; caption?: I18nText }
  | { type: "historical_fact"; text: I18nText; year?: number }
  | { type: "anecdote"; text: I18nText; legend?: boolean; source?: string }
  | { type: "image"; src: AssetRef; caption?: I18nText };

export type Challenge =
  | { type: "quiz"; question: I18nText; options: I18nText[]; correctIndex: number; explanation?: I18nText }
  | { type: "observe"; prompt: I18nText; answer: string[] }
  | { type: "photo"; prompt: I18nText };

export interface Choice {
  label: I18nText;
  hint?: I18nText;
  targetNodeId: string;
  setFlags?: string[];
  requires?: string[];
  distanceM?: number;
  walkMin?: number;
}

export interface Ending {
  id: string;
  requires: string[];
  title: I18nText;
}

export interface Collectible {
  id: string;
  name: I18nText;
  icon: AssetRef;
  awardedAtNodeId: string;
}

export interface PlayerProgress {
  cityId: string;
  routeId: string;
  currentNodeId: string;
  visitedNodeIds: string[];
  clueIds: string[];
  collectibleIds: string[];
  flags: string[];
  startedAt: string;
  /** Momento en que el jugador llegó al nodo actual (solo nodos con `location`). */
  arrivedAt?: string;
  /** Resultado de cada reto puntuable (quiz, observación): acertado a la primera o no. */
  challengeResults?: Record<string, boolean>;
  completedAt?: string;
  endingId?: string;
}
