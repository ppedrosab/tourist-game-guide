import { useCallback, useMemo } from "react";
import type { I18nText } from "@/content/types";
import { localize } from "@/engine/runner";
import { useProgress } from "@/store/progress";
import { en } from "./en";
import { es, Strings } from "./es";

/** Idiomas de la interfaz. El contenido de cada pack declara los suyos en `languages`. */
export type UiLang = "es" | "en";
export type LangSetting = UiLang | "auto";

const DICTS: Record<UiLang, Strings> = { es, en };

/** Idioma del móvil: español si lo usa; si no, inglés (turistas). */
export function deviceLang(): UiLang {
  try {
    const locale = Intl.DateTimeFormat().resolvedOptions().locale ?? "es";
    return locale.toLowerCase().startsWith("es") ? "es" : "en";
  } catch {
    return "es";
  }
}

export const resolveLang = (setting: LangSetting | undefined): UiLang =>
  !setting || setting === "auto" ? deviceLang() : setting;

type Params = Record<string, string | number>;

/** Clave con puntos ("jugar.siguiente") → texto, con {parámetros}. */
export function translate(lang: UiLang, key: string, params?: Params): string {
  const find = (dict: Strings) =>
    key.split(".").reduce<unknown>((node, k) => (node as Record<string, unknown> | undefined)?.[k], dict);
  const raw = find(DICTS[lang]) ?? find(es);
  if (typeof raw !== "string") return key;
  return params ? raw.replace(/\{(\w+)\}/g, (_, p: string) => String(params[p] ?? `{${p}}`)) : raw;
}

/** Idioma actual fuera de React (tareas en segundo plano). */
export const currentLang = (): UiLang => resolveLang(useProgress.getState().language);

/**
 * Textos de la interfaz (`t`) y del contenido de los packs (`L`, con el
 * español como respaldo) en el idioma elegido.
 */
export function useI18n() {
  const setting = useProgress((s) => s.language);
  const lang = resolveLang(setting);
  const t = useCallback((key: StringKey, params?: Params) => translate(lang, key, params), [lang]);
  const L = useCallback((text: I18nText) => localize(text, lang), [lang]);
  const number = useCallback(
    (n: number, digits = 0) => n.toLocaleString(lang === "es" ? "es-ES" : "en-GB", { maximumFractionDigits: digits }),
    [lang],
  );
  /** "560 m" / "1,2 km" (a pie no tiene sentido más precisión). */
  const distance = useCallback(
    (m: number) => (m < 1000 ? `${Math.max(10, Math.round(m / 10) * 10)} m` : `${number(m / 1000, 1)} km`),
    [number],
  );
  return useMemo(() => ({ lang, t, L, number, distance }), [lang, t, L, number, distance]);
}

// Todas las claves válidas ("a.b.c") a partir del diccionario español.
type Leaves<T, P extends string = ""> = {
  [K in keyof T & string]: T[K] extends string ? `${P}${K}` : Leaves<T[K], `${P}${K}.`>;
}[keyof T & string];
export type StringKey = Leaves<Strings>;
