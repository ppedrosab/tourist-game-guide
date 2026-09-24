import { Pressable, StyleSheet, Text, View } from "react-native";
import { border, colors, fonts, hardShadow, radius, size } from "@/theme";
import { HardShadow } from "./HardShadow";
import { Icon, IconName } from "./Icon";

type Props = { icon: IconName; label: string; onPress?: () => void; badge?: number };

export function IconButton({ icon, label, onPress, badge }: Props) {
  return (
    <Pressable onPress={onPress} accessibilityRole="button" accessibilityLabel={label} hitSlop={6}>
      {({ pressed }) => (
        <HardShadow radius={radius.md} offset={hardShadow.sm} pressed={pressed}>
          <View style={styles.body}>
            <Icon name={icon} size={20} />
            {badge ? (
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{badge}</Text>
              </View>
            ) : null}
          </View>
        </HardShadow>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  body: {
    width: size.iconButton,
    height: size.iconButton,
    borderRadius: radius.md,
    backgroundColor: colors.paper,
    borderWidth: border.base,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  badge: {
    position: "absolute",
    top: -8,
    right: -8,
    minWidth: 20,
    height: 20,
    paddingHorizontal: 5,
    borderRadius: 10,
    backgroundColor: colors.clay,
    borderWidth: border.thin,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  badgeText: { fontFamily: fonts.bold, fontSize: 11, color: colors.white },
});
