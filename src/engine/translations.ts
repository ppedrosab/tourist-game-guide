import type { CityPack } from "@/content/types";

/**
 * Textos del pack a los que les falta alguno de los idiomas que declara en
 * `languages`. No bloquea la carga (la app cae al español), pero el test del
 * pack exige que esté completo.
 */
export function missingTranslations(pack: CityPack): string[] {
  const missing: string[] = [];
  const walk = (value: unknown, path: string) => {
    if (Array.isArray(value)) return value.forEach((v, i) => walk(v, `${path}[${i}]`));
    if (!value || typeof value !== "object") return;
    const obj = value as Record<string, unknown>;
    // Un I18nText es un objeto con "es" de texto. Los mapas de audio también tienen
    // "es" pero son rutas de archivo y cada idioma puede no tener locución aún.
    if (typeof obj.es === "string" && !path.endsWith(".audio")) {
      for (const lang of pack.languages) {
        if (typeof obj[lang] !== "string" || !(obj[lang] as string).trim()) missing.push(`${path} (${lang})`);
      }
      return;
    }
    for (const [k, v] of Object.entries(obj)) walk(v, path ? `${path}.${k}` : k);
  };
  walk(pack, "");
  return missing;
}
