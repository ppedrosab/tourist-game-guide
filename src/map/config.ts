/**
 * Estilo de mapa y zooms de descarga. Es configuración del motor, no contenido
 * de ciudad: cada pack aporta sus límites (`bounds`).
 *
 * OpenFreeMap (datos de OpenStreetMap) no pide clave. Antes de publicar hay que
 * confirmar sus condiciones para descargas offline o usar un proveedor propio
 * (p. ej. teselas autoalojadas): basta con cambiar esta URL.
 */
export const MAP_STYLE_URL = "https://tiles.openfreemap.org/styles/liberty";

/** Zooms que se guardan para jugar sin datos: de barrio (13) a portal (17). */
export const OFFLINE_ZOOM = { min: 13, max: 17 } as const;

/** Fuente de las etiquetas numéricas (debe existir en los glifos del estilo). */
export const MAP_LABEL_FONT = ["Noto Sans Bold"];
