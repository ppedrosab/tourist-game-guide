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
