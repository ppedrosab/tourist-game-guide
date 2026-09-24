import { StyleSheet } from "react-native";
import Svg, { Circle, Defs, Path, Pattern, Rect } from "react-native-svg";
import { colors } from "@/theme";

/** Fondo con el motivo de azulejo malagueño (detrás de escenas y modales). */
export function AzulejoBackground({ variant = "ink" }: { variant?: "ink" | "clay" }) {
  const base = variant === "ink" ? colors.ink : colors.clay;
  return (
    <Svg style={StyleSheet.absoluteFill} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      <Defs>
        <Pattern id={`az-${variant}`} width={36} height={36} patternUnits="userSpaceOnUse">
          <Rect width={36} height={36} fill={base} />
          {variant === "ink" ? (
            <>
              <Path d="M18 3L22 14L33 18L22 22L18 33L14 22L3 18L14 14Z" fill="none" stroke={colors.sea} strokeWidth={1.5} />
              <Circle cx={18} cy={18} r={3} fill={colors.clay} />
              <Path d="M0 0H6L0 6ZM36 0H30L36 6ZM0 36H6L0 30ZM36 36H30L36 30Z" fill={colors.sea} />
            </>
          ) : (
            <Path d="M18 3L22 14L33 18L22 22L18 33L14 22L3 18L14 14Z" fill={colors.peach} opacity={0.5} />
          )}
        </Pattern>
      </Defs>
      <Rect width="100%" height="100%" fill={`url(#az-${variant})`} />
    </Svg>
  );
}
