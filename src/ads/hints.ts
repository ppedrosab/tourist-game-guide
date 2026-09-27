/**
 * Puerta de las pistas: antes de dar una pista, la app la pide aquí. Por defecto se concede sin más
 * (web, Expo Go, desarrollo); la build con anuncios enchufa su proveedor con `setHintGate` (un anuncio
 * con recompensa y, si no hay conexión, la pista gratis tras una espera).
 */
export type HintGate = {
  /** Qué ve el jugador en el botón: gratis o a cambio de un anuncio. */
  kind: "free" | "ad";
  /** Resuelve `true` si se concede la pista. */
  request: () => Promise<boolean>;
};

const free: HintGate = { kind: "free", request: async () => true };
let gate: HintGate = free;

export function setHintGate(next: HintGate | null): void {
  gate = next ?? free;
}

export function hintGate(): HintGate {
  return gate;
}
