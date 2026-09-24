import { Pressable, StyleSheet, Text, View } from "react-native";
import { border, Branch, branchColors, colors, fonts, hardShadow, radius } from "@/theme";
import { HardShadow } from "./HardShadow";
import { Icon, IconName } from "./Icon";

type Props = {
  title: string;
  hint?: string;
  meta?: string;
  branch?: Branch;
  icon?: IconName;
  onPress?: () => void;
};

/** Tarjeta de decisión: el color identifica el camino (dinero / poder). */
export function ChoiceCard({ title, hint, meta, branch = "comun", icon = "walk", onPress }: Props) {
  const color = branchColors[branch];
  return (
    <Pressable onPress={onPress} accessibilityRole="button" accessibilityHint={hint}>
      {({ pressed }) => (
        <HardShadow radius={radius.lg} offset={hardShadow.sm} pressed={pressed}>
          <View style={styles.card}>
            <View style={[styles.medal, { backgroundColor: color }]}>
              <Icon name={icon} color={colors.white} />
            </View>
            <View style={styles.text}>
              <Text style={styles.title}>{title}</Text>
              {hint ? <Text style={styles.hint}>{hint}</Text> : null}
              {meta ? <Text style={[styles.meta, { color }]}>{meta}</Text> : null}
            </View>
            <Icon name="next" size={18} strokeWidth={2.6} />
          </View>
        </HardShadow>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    padding: 10,
    paddingRight: 14,
    borderRadius: radius.lg,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
  medal: {
    width: 44,
    height: 44,
    borderRadius: 12,
    borderWidth: border.thin,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  text: { flex: 1, gap: 2 },
  title: { fontFamily: fonts.bold, fontSize: 16, color: colors.ink },
  hint: { fontFamily: fonts.body, fontSize: 13, color: colors.muted },
  meta: { fontFamily: fonts.bold, fontSize: 13 },
});
