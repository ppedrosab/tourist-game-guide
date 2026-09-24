import { StyleSheet, Text, View } from "react-native";
import { border, colors, fonts, radius, size } from "@/theme";
import { Icon, IconName } from "./Icon";

type Variant = "paper" | "clay" | "sea" | "ink" | "sand" | "gold" | "violet";
const VARIANTS: Record<Variant, { bg: string; fg: string }> = {
  paper: { bg: colors.paper, fg: colors.ink },
  clay: { bg: colors.clay, fg: colors.white },
  sea: { bg: colors.sea, fg: colors.white },
  ink: { bg: colors.ink, fg: colors.white },
  sand: { bg: colors.sand, fg: colors.ink },
  gold: { bg: colors.gold, fg: colors.ink },
  violet: { bg: colors.violet, fg: colors.white },
};

type Props = { label: string; variant?: Variant; icon?: IconName; dot?: string };

export function Chip({ label, variant = "paper", icon, dot }: Props) {
  const v = VARIANTS[variant];
  return (
    <View style={[styles.chip, { backgroundColor: v.bg }]}>
      {dot ? <View style={[styles.dot, { backgroundColor: dot }]} /> : null}
      {icon ? <Icon name={icon} size={14} color={v.fg} /> : null}
      <Text style={[styles.label, { color: v.fg }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "flex-start",
    gap: 6,
    height: size.chip,
    paddingHorizontal: 10,
    borderRadius: radius.sm,
    borderWidth: border.thin,
    borderColor: colors.ink,
  },
  dot: { width: 8, height: 8, borderRadius: 4, borderWidth: 1.5, borderColor: colors.ink },
  label: { fontFamily: fonts.bold, fontSize: 12 },
});
