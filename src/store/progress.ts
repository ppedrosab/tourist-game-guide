import AsyncStorage from "@react-native-async-storage/async-storage";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { Choice, PlayerProgress, Route } from "@/content/types";
import { advance as advanceRun, markArrived as markArrivedRun, startRoute } from "@/engine/runner";

/** Lo conseguido en cualquier partida: sobrevive a "Probar otro camino". */
export type Collection = { collectibleIds: string[]; endingIds: string[]; clueIds: string[] };

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

  /** Empieza (o reinicia) la ruta desde el nodo inicial. */
  start: (cityId: string, route: Route) => PlayerProgress;
  /** Avanza la partida de la ruta; el progreso queda guardado en cada nodo. */
  advance: (route: Route, choice?: Choice) => PlayerProgress;
  /** Registra la llegada al nodo actual (GPS, geofence, "Ya estoy aquí" o modo demo). */
  markArrived: (route: Route) => void;
  /** Borra la partida de una ruta sin tocar la colección. */
  discard: (routeId: string) => void;
};

const merge = (a: string[], b: readonly string[]) => [...a, ...b.filter((x) => !a.includes(x))];

function collect(collection: Collection, run: PlayerProgress): Collection {
  return {
    collectibleIds: merge(collection.collectibleIds, run.collectibleIds),
    endingIds: run.endingId ? merge(collection.endingIds, [run.endingId]) : collection.endingIds,
    clueIds: merge(collection.clueIds, run.clueIds),
  };
}

const EMPTY: Collection = { collectibleIds: [], endingIds: [], clueIds: [] };

export const useProgress = create<ProgressStore>()(
  persist(
    (set, get) => {
      const save = (run: PlayerProgress) => {
        set((s) => ({
          runs: { ...s.runs, [run.routeId]: run },
          collection: collect(s.collection, run),
          lastRouteId: run.routeId,
        }));
        return run;
      };
      return {
        runs: {},
        collection: EMPTY,
        hydrated: false,
        demoMode: __DEV__,
        setDemoMode: (demoMode) => set({ demoMode }),
        start: (cityId, route) => save(startRoute(cityId, route)),
        advance: (route, choice) => {
          const run = get().runs[route.id];
          if (!run) throw new Error(`No hay partida empezada en "${route.id}"`);
          return save(advanceRun(route, run, choice));
        },
        markArrived: (route) => {
          const run = get().runs[route.id];
          if (!run) return;
          const next = markArrivedRun(route, run);
          if (next !== run) save(next);
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
      partialize: ({ runs, collection, lastRouteId, demoMode }) => ({ runs, collection, lastRouteId, demoMode }),
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
