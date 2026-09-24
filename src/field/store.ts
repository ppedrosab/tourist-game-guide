import AsyncStorage from "@react-native-async-storage/async-storage";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { FieldArrival, FieldEntry, FieldFix } from "./analysis";

/** Tope del registro: de sobra para varias rutas completas. */
const MAX_ENTRIES = 3000;
/** Como mucho una posición cada 5 s por parada. */
const FIX_EVERY_MS = 5000;

type FieldStore = {
  /** Modo prueba de campo: registra posiciones y llegadas (solo en el móvil). */
  enabled: boolean;
  log: FieldEntry[];
  setEnabled: (on: boolean) => void;
  addFix: (fix: Omit<FieldFix, "kind" | "at">) => void;
  addArrival: (arrival: Omit<FieldArrival, "kind" | "at">) => void;
  clear: () => void;
};

const append = (log: FieldEntry[], entry: FieldEntry) => {
  const next = [...log, entry];
  return next.length > MAX_ENTRIES ? next.slice(next.length - MAX_ENTRIES) : next;
};

/**
 * Registro de la prueba de campo, separado del progreso del jugador. Guarda
 * coordenadas, pero no sale del móvil salvo que el probador lo exporte.
 */
export const useFieldTest = create<FieldStore>()(
  persist(
    (set, get) => ({
      enabled: false,
      log: [],
      setEnabled: (enabled) => set({ enabled }),
      addFix: (fix) => {
        if (!get().enabled) return;
        const last = [...get().log].reverse().find((e) => e.kind === "fix" && e.nodeId === fix.nodeId);
        if (last && Date.now() - Date.parse(last.at) < FIX_EVERY_MS) return;
        set((s) => ({ log: append(s.log, { ...fix, kind: "fix", at: new Date().toISOString() }) }));
      },
      addArrival: (arrival) => {
        if (!get().enabled) return;
        set((s) => ({ log: append(s.log, { ...arrival, kind: "arrival", at: new Date().toISOString() }) }));
      },
      clear: () => set({ log: [] }),
    }),
    { name: "prueba-campo", version: 1, storage: createJSONStorage(() => AsyncStorage) },
  ),
);
