import type { Route } from "@/content/types";
import { useI18n } from "@/i18n";
import { Chip } from "./Chip";

/**
 * Seña del tipo de ruta: gastronómica (chip dorado con cubiertos) o de fiestas (chip morado
 * con antifaz). Las de historia no muestran nada para no recargar las tarjetas.
 */
export function ThemeBadge({ route }: { route: Route }) {
  const { t } = useI18n();
  if (route.theme === "gastronomia") return <Chip label={t("comun.gastronomia")} variant="gold" icon="food" />;
  if (route.theme === "fiestas") return <Chip label={t("comun.fiestas")} variant="violet" icon="mask" />;
  return null;
}
