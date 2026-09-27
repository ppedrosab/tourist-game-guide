import { View } from "react-native";
import Svg, { Path } from "react-native-svg";
import { colors } from "@/theme";

/** Iconos de trazo del storyboard (24×24). Los marcados en FILLED se rellenan. */
const PATHS = {
  back: "M15 18l-6-6 6-6",
  next: "M9 18l6-6-6-6",
  close: "M6 6l12 12M18 6L6 18",
  pause: "M9 5v14M15 5v14",
  book: "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 19V5",
  compass: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM15.5 8.5l-2 5-5 2 2-5z",
  route: "M6 17a2 2 0 1 0 0 4a2 2 0 1 0 0-4zM18 3a2 2 0 1 0 0 4a2 2 0 1 0 0-4zM8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7",
  trophy: "M8 4h8v5a4 4 0 0 1-8 0zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6",
  user: "M12 4a4 4 0 1 0 0 8a4 4 0 1 0 0-8zM4 21a8 8 0 0 1 16 0",
  map: "M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2zM9 4v14M15 6v14",
  walk: "M13 2a2 2 0 1 0 0 4a2 2 0 1 0 0-4zM10 21l2-6 3 3v3M7 12l3-4 4 1 2 3M12 15l-1-6",
  clock: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM12 7v5l3 2",
  pin: "M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11zM12 7.5a2.5 2.5 0 1 0 0 5a2.5 2.5 0 1 0 0-5z",
  split: "M6 3v6a6 6 0 0 0 6 6a6 6 0 0 1 6 6M18 3v6M15 6l3-3 3 3",
  star: "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z",
  check: "M5 12l5 5 9-10",
  play: "M7 5v14l12-7z",
  volume: "M4 9h4l5-4v14l-5-4H4zM16 9a4 4 0 0 1 0 6",
  replay: "M3 12a9 9 0 1 0 3-6.7M3 4v5h5",
  bulb: "M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z",
  undo: "M9 14l-4-4 4-4M5 10h9a5 5 0 0 1 0 10h-3",
  ad: "M3 6h18v12H3zM10 9v6l5-3z",
  lock: "M7 11h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2zM8 11V7a4 4 0 0 1 8 0v4",
  camera: "M4 8h3l2-3h6l2 3h3v11H4zM12 9.5a3.5 3.5 0 1 0 0 7a3.5 3.5 0 1 0 0-7z",
  search: "M11 5a6 6 0 1 0 0 12a6 6 0 1 0 0-12zM20 20l-4.5-4.5",
  share:
    "M18 2a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM6 9a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM18 16a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM8.6 13.5l6.8 4M15.4 6.5l-6.8 4",
  download: "M12 4v11M7 10l5 5 5-5M5 20h14",
  /** Tenedor y cuchillo: rutas gastronómicas. */
  food: "M6 3v7a2 2 0 0 0 4 0V3M8 10v11M17 21V3c-2.5 1.5-3.5 4.5-3.5 8.5H17",
  /** Antifaz de Carnaval: rutas de fiestas. */
  mask: "M3 8c3-1.5 6-1.5 9 0c3-1.5 6-1.5 9 0c0 5-3 8-6 8c-1.5 0-2.5-1-3-2c-.5 1-1.5 2-3 2c-3 0-6-3-6-8zM7 10.5h2.5M14.5 10.5H17",
  /** Luna creciente: rutas de leyendas. */
  moon: "M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z",
  exit: "M14 4h5v16h-5M10 16l-4-4 4-4M6 12h10",
  /** Auriculares: modo manos libres. */
  headphones: "M4 15v-3a8 8 0 0 1 16 0v3M4 15h3v6H5a1 1 0 0 1-1-1zM20 15h-3v6h2a1 1 0 0 0 1-1z",
  /** Gota: fuente de agua potable. */
  water: "M12 3c-3 4.5-6 7.6-6 11a6 6 0 0 0 12 0c0-3.4-3-6.5-6-11z",
  /** Aseos. */
  toilet: "M7 4a1.5 1.5 0 1 0 0 3a1.5 1.5 0 1 0 0-3zM17 4a1.5 1.5 0 1 0 0 3a1.5 1.5 0 1 0 0-3zM5 20v-6H4l1-5h4l1 5H9v6M15 20v-5M19 20v-5M15 9h4v6h-4zM12 3v18",
  /** Árbol: sombra. */
  tree: "M12 21v-6M12 3a5 5 0 0 0-4.6 7A4 4 0 0 0 8 17h8a4 4 0 0 0 .6-7A5 5 0 0 0 12 3z",
  /** Escalones. */
  stairs: "M3 20h5v-4h4v-4h4V8h5",
  /** Cuesta. */
  slope: "M3 19h18L21 7zM14 15l3-3",
  /** Termómetro: calor. */
  heat: "M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0zM12 11v6",
  /** Silla de ruedas: accesibilidad. */
  wheelchair: "M11 4a1.5 1.5 0 1 0 0 3a1.5 1.5 0 1 0 0-3zM11 9v5h5l2 5M11 12h4M8.5 11.5A5 5 0 1 0 15 18",
  subtitles:
    "M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM10 10a2 2 0 1 0 0 4M16 10a2 2 0 1 0 0 4",
} as const;

const FILLED = new Set<IconName>(["play"]);
export type IconName = keyof typeof PATHS;

type Props = {
  name: IconName;
  size?: number;
  color?: string;
  strokeWidth?: number;
  /** Relleno del color en vez de trazo (p. ej. estrella conseguida). */
  fill?: string;
};

export function Icon({ name, size = 20, color = colors.ink, strokeWidth = 2.2, fill }: Props) {
  const filled = FILLED.has(name);
  return (
    // Las props de accesibilidad van en un View: Svg no las admite en web.
    <View accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      <Svg width={size} height={size} viewBox="0 0 24 24">
        <Path
          d={PATHS[name]}
          fill={fill ?? (filled ? color : "none")}
          stroke={filled ? "none" : color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
    </View>
  );
}
