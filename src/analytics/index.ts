/**
 * Analítica mínima y respetuosa: eventos tipados, sin datos personales ni
 * coordenadas, y solo si el jugador ha dado su consentimiento (lo comprueba
 * quien llama: el store y useTrack). No envía nada por sí misma: el proveedor
 * (PostHog, Amplitude, un endpoint propio…) se conecta con setAnalyticsSink.
 */

export type ArrivalMethod = "gps" | "geofence" | "manual" | "demo";

export type AnalyticsEvent =
  | { name: "route_started"; routeId: string; cityId: string; replay: boolean }
  | { name: "stop_arrived"; routeId: string; nodeId: string; method: ArrivalMethod }
  | { name: "decision_made"; routeId: string; nodeId: string; targetNodeId: string }
  | { name: "challenge_answered"; routeId: string; nodeId: string; correct: boolean }
  | { name: "route_completed"; routeId: string; endingId?: string; stars: number; minutes: number }
  | { name: "map_opened"; routeId?: string }
  | { name: "offline_map"; cityId: string; action: "download" | "complete" | "delete" | "error" }
  | { name: "language_changed"; language: string };

export type TrackedEvent = AnalyticsEvent & { at: string };
export type AnalyticsSink = (event: TrackedEvent) => void;

/** Últimos eventos (para depurar en desarrollo y en la prueba de campo). */
const RECENT_MAX = 100;
const recent: TrackedEvent[] = [];

let sink: AnalyticsSink | undefined = __DEV__ ? (e) => console.log(`[analítica] ${e.name}`, e) : undefined;

export function setAnalyticsSink(next: AnalyticsSink | undefined) {
  sink = next;
}

/** Registra un evento. Quien llama debe haber comprobado el consentimiento. */
export function track(event: AnalyticsEvent, now: Date = new Date()) {
  const tracked: TrackedEvent = { ...event, at: now.toISOString() };
  recent.push(tracked);
  if (recent.length > RECENT_MAX) recent.shift();
  try {
    sink?.(tracked);
  } catch {
    // La analítica nunca puede romper el juego.
  }
}

export function recentEvents(): readonly TrackedEvent[] {
  return recent;
}
