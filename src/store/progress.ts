import AsyncStorage from "@react-native-async-storage/async-storage";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { AnalyticsEvent, ArrivalMethod, track } from "@/analytics";
import type { Choice, PlayerProgress, Route } from "@/content/types";
import {
  advance as advanceRun,
  markArrived as markArrivedRun,
  recordChallenge as recordChallengeRun,
  starsFor,
  startRoute,
} from "@/engine/runner";

/** Lo conseguido en cualquier partida: sobrevive a "Probar otro camino". */
export type Collection = {
  collectibleIds: string[];
  endingIds: string[];
  clueIds: string[];
  /** Mejor puntuación (1–3 estrellas) de cada ruta terminada. */
  bestStars?: Record<string, number>;
};

type ProgressStore = {
  /** Partida por ruta (en curso o la última terminada). */
  runs: Record<string, PlayerProgress>;
  collection: Collection;
  /** Última ruta jugada, para el "Continuar" de Explorar. */
  lastRouteId?: string;
  /** true cuando ya se ha leído lo guardado en disco. */
  hydrated: boolean;
  /**
   * Modo demo: botón "Simular llegada" para jugar la ruta desde casa.
   * Activo por defecto solo en desarrollo; se cambia en Perfil.
   */
  demoMode: boolean;
  setDemoMode: (on: boolean) => void;
  /** Reproducir las voces grabadas. */
  voices: boolean;
  /** Mostrar el texto de los diálogos (siempre visible si no hay voz que escuchar). */
  subtitles: boolean;
  setVoices: (on: boolean) => void;
  /** Idioma de la interfaz y del contenido ("auto" = el del móvil). */
  language: "auto" | "es" | "en";
  setLanguage: (language: "auto" | "es" | "en") => void;
  setSubtitles: (on: boolean) => void;
  /** Consentimiento para estadísticas anónimas de uso (desactivado por defecto). */
  analytics: boolean;
  setAnalytics: (on: boolean) => void;
  /** Registra un evento solo si hay consentimiento. */
  track: (event: AnalyticsEvent) => void;

  /** Empieza (o reinicia) la ruta desde el nodo inicial. */
  start: (cityId: string, route: Route) => PlayerProgress;
  /** Avanza la partida de la ruta; el progreso queda guardado en cada nodo. */
  advance: (route: Route, choice?: Choice) => PlayerProgress;
  /** Registra la llegada al nodo actual (GPS, geofence, "Ya estoy aquí" o modo demo). */
  markArrived: (route: Route, method: ArrivalMethod) => void;
  /** Apunta si se acertó el reto del nodo actual (solo cuenta el primer intento). */
  recordChallenge: (route: Route, correct: boolean) => void;
  /** Borra la partida de una ruta sin tocar la colección. */
  discard: (routeId: string) => void;
};

const merge = (a: string[], b: readonly string[]) => [...a, ...b.filter((x) => !a.includes(x))];

function collect(collection: Collection, run: PlayerProgress, route?: Route): Collection {
  let bestStars = collection.bestStars;
  if (route && run.completedAt) {
    const { stars } = starsFor(route, run);
    if (stars > (bestStars?.[run.routeId] ?? 0)) bestStars = { ...bestStars, [run.routeId]: stars };
  }
  return {
    collectibleIds: merge(collection.collectibleIds, run.collectibleIds),
    endingIds: run.endingId ? merge(collection.endingIds, [run.endingId]) : collection.endingIds,
    clueIds: merge(collection.clueIds, run.clueIds),
    bestStars,
  };
}

const EMPTY: Collection = { collectibleIds: [], endingIds: [], clueIds: [] };

export const useProgress = create<ProgressStore>()(
  persist(
    (set, get) => {
      const save = (run: PlayerProgress, route?: Route) => {
        set((s) => ({
          runs: { ...s.runs, [run.routeId]: run },
          collection: collect(s.collection, run, route),
          lastRouteId: run.routeId,
        }));
        return run;
      };
      const emit = (event: AnalyticsEvent) => {
        if (get().analytics) track(event);
      };
      return {
        analytics: false,
        setAnalytics: (analytics) => set({ analytics }),
        track: emit,
        runs: {},
        collection: EMPTY,
        hydrated: false,
        demoMode: __DEV__,
        setDemoMode: (demoMode) => set({ demoMode }),
        voices: true,
        subtitles: true,
        setVoices: (voices) => set({ voices }),
        language: "auto",
        setLanguage: (language) => {
          set({ language });
          emit({ name: "language_changed", language });
        },
        setSubtitles: (subtitles) => set({ subtitles }),
        start: (cityId, route) => {
          const replay = get().runs[route.id] !== undefined;
          const run = save(startRoute(cityId, route));
          emit({ name: "route_started", routeId: route.id, cityId, replay });
          return run;
        },
        advance: (route, choice) => {
          const run = get().runs[route.id];
          if (!run) throw new Error(`No hay partida empezada en "${route.id}"`);
          const next = save(advanceRun(route, run, choice), route);
          if (choice) {
            emit({ name: "decision_made", routeId: route.id, nodeId: run.currentNodeId, targetNodeId: choice.targetNodeId });
          }
          if (next.completedAt && !run.completedAt) {
            const minutes = Math.round((Date.parse(next.completedAt) - Date.parse(next.startedAt)) / 60000);
            const { stars } = starsFor(route, next);
            emit({ name: "route_completed", routeId: route.id, endingId: next.endingId, stars, minutes });
          }
          return next;
        },
        recordChallenge: (route, correct) => {
          const run = get().runs[route.id];
          if (!run) return;
          const next = recordChallengeRun(route, run, correct);
          if (next === run) return;
          save(next);
          emit({ name: "challenge_answered", routeId: route.id, nodeId: run.currentNodeId, correct });
        },
        markArrived: (route, method) => {
          const run = get().runs[route.id];
          if (!run) return;
          const next = markArrivedRun(route, run);
          if (next === run) return;
          save(next);
          emit({ name: "stop_arrived", routeId: route.id, nodeId: run.currentNodeId, method });
        },
        discard: (routeId) =>
          set((s) => {
            const { [routeId]: _, ...runs } = s.runs;
            return { runs, lastRouteId: s.lastRouteId === routeId ? undefined : s.lastRouteId };
          }),
      };
    },
    {
      name: "progreso",
      version: 1,
      storage: createJSONStorage(() => AsyncStorage),
      partialize: ({ runs, collection, lastRouteId, demoMode, voices, subtitles, language, analytics }) => ({
        analytics,
        language,
        runs,
        collection,
        lastRouteId,
        demoMode,
        voices,
        subtitles,
      }),
      onRehydrateStorage: () => () => useProgress.setState({ hydrated: true }),
    },
  ),
);

/** Partida en curso (sin terminar) de una ruta, si la hay. */
export function useActiveRun(routeId: string | undefined): PlayerProgress | undefined {
  return useProgress((s) => {
    const run = routeId ? s.runs[routeId] : undefined;
    return run && !run.completedAt ? run : undefined;
  });
}
