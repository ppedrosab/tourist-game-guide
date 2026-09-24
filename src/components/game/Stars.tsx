import { View } from "react-native";
import { Icon } from "@/components/ui";
import { colors } from "@/theme";

/** Fila de 3 estrellas: las conseguidas en oro con contorno de tinta. */
export function Stars({ value, size = 28, label }: { value: number; size?: number; label: string }) {
  return (
    <View style={{ flexDirection: "row", gap: 4 }} accessible accessibilityLabel={label}>
      {[1, 2, 3].map((i) => (
        <Icon key={i} name="star" size={size} color={colors.ink} fill={i <= value ? colors.gold : colors.sand} />
      ))}
    </View>
  );
}
