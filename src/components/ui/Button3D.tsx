import { Pressable, StyleSheet, Text, View } from "react-native";
import { border, colors, fonts, hardShadow, radius, size } from "@/theme";
import { HardShadow } from "./HardShadow";
import { Icon, IconName } from "./Icon";

type Variant = "primary" | "secondary" | "dark" | "sea" | "ghost";
type Props = {
  label: string;
  onPress?: () => void;
  variant?: Variant;
  icon?: IconName;
  small?: boolean;
  disabled?: boolean;
};

const VARIANTS: Record<Exclude<Variant, "ghost">, { bg: string; fg: string }> = {
  primary: { bg: colors.clay, fg: colors.white },
  secondary: { bg: colors.paper, fg: colors.ink },
  dark: { bg: colors.ink, fg: colors.white },
  sea: { bg: colors.sea, fg: colors.white },
};

export function Button3D({ label, onPress, variant = "primary", icon, small = false, disabled = false }: Props) {
  if (variant === "ghost") {
    return (
      <Pressable onPress={onPress} disabled={disabled} accessibilityRole="button" style={styles.ghost} hitSlop={8}>
        <Text style={[styles.label, { color: colors.ink, fontSize: 15 }]}>{label}</Text>
      </Pressable>
    );
  }
  const v = VARIANTS[variant];
  const height = small ? size.buttonSmall : size.button;
  return (
    <Pressable onPress={onPress} disabled={disabled} accessibilityRole="button" accessibilityState={{ disabled }}>
      {({ pressed }) => (
        <HardShadow radius={radius.lg} offset={small ? hardShadow.sm : hardShadow.md} pressed={pressed && !disabled}>
          <View style={[styles.body, { height, backgroundColor: v.bg, opacity: disabled ? 0.5 : 1 }]}>
            <Text style={[styles.label, { color: v.fg, fontSize: small ? 15 : 17 }]}>{label}</Text>
            {icon ? <Icon name={icon} size={18} color={v.fg} strokeWidth={2.4} /> : null}
          </View>
        </HardShadow>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  body: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingHorizontal: 20,
    borderRadius: radius.lg,
    borderWidth: border.base,
    borderColor: colors.ink,
  },
  label: { fontFamily: fonts.bold, letterSpacing: 0.2 },
  ghost: { height: 44, alignItems: "center", justifyContent: "center" },
});
