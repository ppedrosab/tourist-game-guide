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
  lock: "M7 11h10a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2zM8 11V7a4 4 0 0 1 8 0v4",
  camera: "M4 8h3l2-3h6l2 3h3v11H4zM12 9.5a3.5 3.5 0 1 0 0 7a3.5 3.5 0 1 0 0-7z",
  search: "M11 5a6 6 0 1 0 0 12a6 6 0 1 0 0-12zM20 20l-4.5-4.5",
  share:
    "M18 2a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM6 9a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM18 16a3 3 0 1 0 0 6a3 3 0 1 0 0-6zM8.6 13.5l6.8 4M15.4 6.5l-6.8 4",
  download: "M12 4v11M7 10l5 5 5-5M5 20h14",
  exit: "M14 4h5v16h-5M10 16l-4-4 4-4M6 12h10",
  subtitles:
    "M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM10 10a2 2 0 1 0 0 4M16 10a2 2 0 1 0 0 4",
} as const;

const FILLED = new Set<IconName>(["play"]);
export type IconName = keyof typeof PATHS;

type Props = { name: IconName; size?: number; color?: string; strokeWidth?: number };

export function Icon({ name, size = 20, color = colors.ink, strokeWidth = 2.2 }: Props) {
  const filled = FILLED.has(name);
  return (
    // Las props de accesibilidad van en un View: Svg no las admite en web.
    <View accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      <Svg width={size} height={size} viewBox="0 0 24 24">
        <Path
          d={PATHS[name]}
          fill={filled ? color : "none"}
          stroke={filled ? "none" : color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
    </View>
  );
}
