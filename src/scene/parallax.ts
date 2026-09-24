/**
 * Parallax de las escenas. Funciones puras marcadas como worklet: se ejecutan
 * en el hilo de interfaz (reanimated) fotograma a fotograma y también en jest.
 *
 * Garantías:
 *  - La inclinación normalizada pasa por tanh → nunca supera ±1, así que el
 *    desplazamiento de una capa está acotado por amplitud × profundidad.
 *  - Todas las capas se amplían con el MISMO factor (overscanScale), calculado
 *    para cubrir ese desplazamiento máximo: nunca se ve un borde y, en reposo,
 *    la composición es idéntica a la del ilustrador.
 *  - Suavizado exponencial dependiente de dt: igual de fluido a 60 o 120 Hz.
 *  - Recentrado lento: la postura natural con la que se sostiene el móvil pasa
 *    a ser el centro; solo se notan los giros, no la inclinación de partida.
 */

export type ParallaxConfig = {
  /**
   * Desplazamiento máximo de una capa de profundidad 1, como fracción del ancho
   * y del alto del escenario: la sensación y el recorte son iguales en
   * cualquier pantalla.
   */
  amplitudeX: number;
  amplitudeY: number;
  /** Giro (rad) que lleva la inclinación a ~76 % (tanh(1)) del máximo. */
  maxAngle: number;
  /** Constante de tiempo del suavizado (ms). Más alto = más "peso". */
  smoothingMs: number;
  /** Constante de tiempo del recentrado (ms). */
  recenterMs: number;
};

export const PARALLAX: ParallaxConfig = {
  amplitudeX: 0.066, // 26 pt en un escenario de 390 pt
  amplitudeY: 0.025, // 14 pt en uno de 560 pt
  maxAngle: (18 * Math.PI) / 180,
  smoothingMs: 110,
  recenterMs: 3000,
};

/**
 * Profundidad por papel de capa (factores del documento de diseño). `null` =
 * capa fija sobre el fondo y bajo los personajes (fx: rayos de luz, brillos).
 */
const DEPTH_BY_ROLE: Record<string, number | null> = {
  sky: 0,
  far: 0.1,
  mid: 0.25,
  sea: 0.25,
  near: 0.6,
  fx: null,
};

/** Los personajes pisan el suelo del primer plano: se mueven con él para que no "patinen". */
export const CHARACTER_DEPTH = 0.6;

export function depthOf(role: string): number | null {
  return role in DEPTH_BY_ROLE ? DEPTH_BY_ROLE[role] : 0.25;
}

/** Amplitud en puntos para un escenario concreto. */
export function stageAmplitude(width: number, height: number, cfg: ParallaxConfig = PARALLAX) {
  return { ax: cfg.amplitudeX * width, ay: cfg.amplitudeY * height };
}

/** Escala común de todas las capas para que el desplazamiento máximo no descubra bordes (+1 pt de margen). */
export function overscanScale(width: number, height: number, maxDepth: number, cfg: ParallaxConfig = PARALLAX): number {
  if (width <= 0 || height <= 0) return 1;
  const { ax, ay } = stageAmplitude(width, height, cfg);
  const sx = 1 + (2 * (ax * maxDepth + 1)) / width;
  const sy = 1 + (2 * (ay * maxDepth + 1)) / height;
  return Math.max(sx, sy);
}

export function wrapAngle(a: number): number {
  "worklet";
  const TWO_PI = Math.PI * 2;
  return a - TWO_PI * Math.floor((a + Math.PI) / TWO_PI);
}

/** Fracción de acercamiento de un filtro exponencial para un paso de `dtMs`. */
export function smoothFactor(dtMs: number, tauMs: number): number {
  "worklet";
  return tauMs <= 0 ? 1 : 1 - Math.exp(-dtMs / tauMs);
}

export type TiltState = {
  /** Inclinación normalizada y suavizada, en (-1, 1). */
  x: number;
  y: number;
  /** Postura de referencia (rad) que se considera "centro". */
  baseRoll: number;
  basePitch: number;
  ready: boolean;
};

export const INITIAL_TILT: TiltState = { x: 0, y: 0, baseRoll: 0, basePitch: 0, ready: false };

/** Avanza un fotograma a partir de la orientación del móvil (roll/pitch en rad). */
export function stepTilt(
  s: TiltState,
  roll: number,
  pitch: number,
  dtMs: number,
  cfg: ParallaxConfig = PARALLAX,
): TiltState {
  "worklet";
  if (!Number.isFinite(roll) || !Number.isFinite(pitch)) return s;
  if (!s.ready) return { x: 0, y: 0, baseRoll: roll, basePitch: pitch, ready: true };
  // Tras una pausa larga (app en segundo plano) no se da un salto brusco.
  const dt = Math.min(Math.max(dtMs, 0), 100);
  const k = smoothFactor(dt, cfg.recenterMs);
  const baseRoll = s.baseRoll + wrapAngle(roll - s.baseRoll) * k;
  const basePitch = s.basePitch + wrapAngle(pitch - s.basePitch) * k;
  const targetX = Math.tanh(wrapAngle(roll - baseRoll) / cfg.maxAngle);
  const targetY = Math.tanh(wrapAngle(pitch - basePitch) / cfg.maxAngle);
  const a = smoothFactor(dt, cfg.smoothingMs);
  return { x: s.x + (targetX - s.x) * a, y: s.y + (targetY - s.y) * a, baseRoll, basePitch, ready: true };
}

/**
 * Entrada directa ya normalizada en [-1, 1] (puntero en web, pruebas). Se
 * suaviza igual que el giroscopio pero sin recentrado.
 */
export function stepPointer(s: TiltState, px: number, py: number, dtMs: number, cfg: ParallaxConfig = PARALLAX): TiltState {
  "worklet";
  const clamp = (v: number) => Math.max(-1, Math.min(1, v));
  const a = smoothFactor(Math.min(Math.max(dtMs, 0), 100), cfg.smoothingMs);
  return { ...s, x: s.x + (clamp(px) - s.x) * a, y: s.y + (clamp(py) - s.y) * a, ready: true };
}

/**
 * Desplazamiento de una capa: las cercanas se mueven más y en sentido
 * contrario a la inclinación (como mirar por una ventana).
 */
export function layerOffset(x: number, y: number, depth: number, ax: number, ay: number) {
  "worklet";
  return { tx: -x * ax * depth, ty: -y * ay * depth };
}
