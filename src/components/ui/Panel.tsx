import { ReactNode } from "react";
import { StyleProp, StyleSheet, Text, View, ViewStyle } from "react-native";
import { border, colors, fonts, hardShadow, radius } from "@/theme";
import { HardShadow } from "./HardShadow";

type Props = {
  children: ReactNode;
  /** Placa con el nombre del personaje o título, sobre el borde superior. */
  nameplate?: string;
  nameplateColor?: string;
  style?: StyleProp<ViewStyle>;
};

export function Panel({ children, nameplate, nameplateColor = colors.clay, style }: Props) {
  return (
    <HardShadow radius={radius.xl} offset={hardShadow.md}>
      <View style={[styles.panel, nameplate ? { paddingTop: 26 } : null, style]}>
        {nameplate ? <Nameplate text={nameplate} color={nameplateColor} /> : null}
        {children}
      </View>
    </HardShadow>
  );
}

export function Nameplate({ text, color = colors.clay }: { text: string; color?: string }) {
  return (
    <HardShadow radius={10} offset={hardShadow.sm} style={styles.nameplateWrap}>
      <View style={[styles.nameplate, { backgroundColor: color }]}>
        <Text style={styles.nameplateText}>{text}</Text>
      </View>
    </HardShadow>
  );
}

const styles = StyleSheet.create({
  panel: {
    backgroundColor: colors.paper,
    borderWidth: border.base,
    borderColor: colors.ink,
    borderRadius: radius.xl,
    padding: 18,
    gap: 12,
  },
  nameplateWrap: { position: "absolute", top: -18, left: 16, zIndex: 2 },
  nameplate: {
    height: 32,
    paddingHorizontal: 14,
    borderRadius: 10,
    borderWidth: border.base,
    borderColor: colors.ink,
    justifyContent: "center",
  },
  nameplateText: { fontFamily: fonts.bold, fontSize: 13, letterSpacing: 0.8, textTransform: "uppercase", color: colors.white },
});
