import type { Route } from "@/content/types";
import { useI18n } from "@/i18n";
import { Chip } from "./Chip";

/**
 * Seña del tipo de ruta. Solo las rutas gastronómicas la llevan (chip dorado con
 * cubiertos); las de historia no muestran nada para no recargar las tarjetas.
 */
export function ThemeBadge({ route }: { route: Route }) {
  const { t } = useI18n();
  if (route.theme !== "gastronomia") return null;
  return <Chip label={t("comun.gastronomia")} variant="gold" icon="food" />;
}
