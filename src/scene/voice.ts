/**
 * Duración estimada de una locución (ms) cuando aún no hay audio grabado:
 * ritmo de narración pausada en español (~2,6 palabras/s), con pausas por
 * puntuación. Sirve para el lip-sync y la barra de progreso de la caja de diálogo.
 */
export function estimateSpeechMs(text: string): number {
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  const pauses = (text.match(/[.!?…]/g) ?? []).length * 250 + (text.match(/[,;:]/g) ?? []).length * 120;
  const ms = (words / 2.6) * 1000 + pauses + 300;
  return Math.round(Math.min(Math.max(ms, 1200), 25000));
}

/**
 * Ritmo de boca para el lip-sync: duraciones (ms) de cada fase abierta/cerrada,
 * deterministas a partir de una semilla para que no parezca un metrónomo.
 */
export function mouthPhaseMs(seed: number, phase: number): number {
  const x = Math.sin(seed * 12.9898 + phase * 78.233) * 43758.5453;
  const r = x - Math.floor(x);
  return phase % 2 === 0 ? 90 + r * 80 : 70 + r * 60; // abierta 90–170 ms, cerrada 70–130 ms
}

/**
 * Tono de la voz sintética de un personaje: el suyo si lo trae el pack; si no, uno según el género
 * (mujer más aguda, hombre más grave) con un matiz estable por personaje (±0,08) para que no suenen igual.
 */
export function speakerPitch(speaker: string | undefined, voice?: { gender: "f" | "m"; pitch?: number }): number {
  if (voice?.pitch) return voice.pitch;
  const base = voice ? (voice.gender === "f" ? 1.15 : 0.9) : 1;
  if (!speaker) return base;
  let h = 0;
  for (const ch of speaker) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return Math.round((base - 0.08 + (h % 17) / 100) * 100) / 100;
}

/** Voz del sistema, tal como la describe expo-speech. */
export type SystemVoice = { identifier: string; name: string; language: string; quality?: string };

// Nombres habituales de las voces de iOS, Android, Windows y Chrome para saber si son de hombre o de mujer.
const FEMALE = /m[oó]nica|marisol|paulina|helena|laura|luc[ií]a|elvira|sabina|paloma|carmen|isabel|esperanza|conchita|pen[eé]lope|lupe|samantha|karen|serena|kate|susan|hazel|zira|tessa|moira|fiona|victoria|allison|ava|female|mujer/i;
const MALE = /jorge|juan|diego|pablo|[aá]lvaro|enrique|ra[uú]l|carlos|miguel|andr[eé]s|daniel|arthur|oliver|george|fred|alex|tom\b|aaron|rishi|david|mark|james|gordon|\bmale\b|hombre/i;

/**
 * Elige la voz del sistema para un idioma y un género: primero la del país (es-ES, en-GB), luego
 * cualquiera del idioma; entre ellas, la de mejor calidad cuyo nombre sea del género pedido.
 * Sin voz de ese género devuelve undefined y el tono (`speakerPitch`) hace el resto.
 */
export function pickVoice(voices: readonly SystemVoice[], locale: string, gender: "f" | "m"): SystemVoice | undefined {
  const lang = locale.slice(0, 2).toLowerCase();
  const norm = (l: string) => l.replace("_", "-").toLowerCase();
  const byLang = voices.filter((v) => norm(v.language).startsWith(lang));
  const local = byLang.filter((v) => norm(v.language) === locale.toLowerCase());
  const want = gender === "f" ? FEMALE : MALE;
  const other = gender === "f" ? MALE : FEMALE;
  const rank = (v: SystemVoice) => (v.quality === "Enhanced" ? 0 : 1);
  for (const pool of [local, byLang]) {
    const match = pool.filter((v) => want.test(v.name) && !other.test(v.name)).sort((a, b) => rank(a) - rank(b));
    if (match.length > 0) return match[0];
  }
  return undefined;
}
