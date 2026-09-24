import { ReactNode } from "react";
import { StyleProp, View, ViewStyle } from "react-native";
import { colors, hardShadow } from "@/theme";

type Props = {
  children: ReactNode;
  radius: number;
  offset?: number;
  /** Al pulsar, el elemento "baja" y la sombra desaparece: efecto botón de juego. */
  pressed?: boolean;
  style?: StyleProp<ViewStyle>;
};

/**
 * Sombra dura multiplataforma. En Android `elevation` no permite sombras
 * desplazadas sin desenfoque, así que dibujamos una forma de tinta detrás.
 */
export function HardShadow({ children, radius, offset = hardShadow.md, pressed = false, style }: Props) {
  return (
    <View style={[{ paddingBottom: offset }, style]}>
      <View
        pointerEvents="none"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: offset,
          bottom: 0,
          borderRadius: radius,
          backgroundColor: colors.ink,
          opacity: pressed ? 0 : 1,
        }}
      />
      <View style={{ transform: [{ translateY: pressed ? offset : 0 }] }}>{children}</View>
    </View>
  );
}
