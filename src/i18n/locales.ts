/** Idiomas de la interfaz y su configuración regional (números, horas y voz del sistema). */
export const UI_LANGS = ["es", "en", "fr", "de", "it"] as const;
export type UiLang = (typeof UI_LANGS)[number];

export const LOCALES: Record<UiLang, string> = { es: "es-ES", en: "en-GB", fr: "fr-FR", de: "de-DE", it: "it-IT" };

/** Configuración regional de un idioma (la inglesa si no es uno de la interfaz). */
export const localeOf = (lang: string): string => LOCALES[lang as UiLang] ?? LOCALES.en;
