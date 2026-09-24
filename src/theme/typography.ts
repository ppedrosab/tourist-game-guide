import { TextStyle } from "react-native";
import { colors } from "./tokens";

/** Nombres que registra expo-font en app/_layout.tsx */
export const fonts = {
  display: "Fraunces_700Bold",
  body: "DMSans_400Regular",
  medium: "DMSans_500Medium",
  bold: "DMSans_700Bold",
} as const;

export const type = {
  display: { fontFamily: fonts.display, fontSize: 34, lineHeight: 38, color: colors.ink },
  title: { fontFamily: fonts.display, fontSize: 26, lineHeight: 30, color: colors.ink },
  subtitle: { fontFamily: fonts.display, fontSize: 20, lineHeight: 24, color: colors.ink },
  body: { fontFamily: fonts.body, fontSize: 16, lineHeight: 24, color: colors.ink },
  dialogue: { fontFamily: fonts.body, fontSize: 17, lineHeight: 25, color: colors.ink },
  secondary: { fontFamily: fonts.body, fontSize: 14, lineHeight: 20, color: colors.muted },
  label: { fontFamily: fonts.bold, fontSize: 15, color: colors.ink },
  overline: { fontFamily: fonts.bold, fontSize: 12, letterSpacing: 1, textTransform: "uppercase", color: colors.sea },
  caption: { fontFamily: fonts.medium, fontSize: 12, color: colors.muted },
} satisfies Record<string, TextStyle>;
