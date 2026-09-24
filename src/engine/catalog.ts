import type { CityPack, Route } from "@/content/types";
import malaga from "@content/malaga/misterio-manquita.pack.json";
import { loadPack } from "./loadPack";
import { missingTranslations } from "./translations";

/**
 * Packs incluidos en la app. Añadir una ciudad = añadir su JSON aquí;
 * el contenido nunca se escribe en el código.
 */
export const BUNDLED_PACKS: Record<string, unknown> = { malaga };

export type PackError = { source: string; errors: string[] };
type Catalog = { packs: CityPack[]; errors: PackError[] };

let cache: Catalog | null = null;

/** Carga y valida los packs una sola vez. Los packs inválidos se descartan y se informan. */
export function getCatalog(): Catalog {
  if (cache) return cache;
  const packs: CityPack[] = [];
  const errors: PackError[] = [];
  for (const [source, raw] of Object.entries(BUNDLED_PACKS)) {
    const result = loadPack(raw);
    if (result.ok) {
      packs.push(result.pack);
      const missing = __DEV__ ? missingTranslations(result.pack) : [];
      if (missing.length > 0)
        console.warn(`[packs] "${source}": faltan ${missing.length} traducciones (se usa el español)`);
    } else {
      errors.push({ source, errors: result.errors });
      console.warn(`[packs] "${source}" no es válido y se ignora:\n- ${result.errors.join("\n- ")}`);
    }
  }
  cache = { packs, errors };
  return cache;
}

export function getPack(cityId: string): CityPack | undefined {
  return getCatalog().packs.find((p) => p.id === cityId);
}

export function findRoute(routeId: string): { pack: CityPack; route: Route } | undefined {
  for (const pack of getCatalog().packs) {
    const route = pack.routes.find((r) => r.id === routeId);
    if (route) return { pack, route };
  }
  return undefined;
}
