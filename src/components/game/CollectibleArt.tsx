import { memo, useMemo } from "react";
import { View } from "react-native";
import { SvgXml } from "react-native-svg";
import { COLLECTIBLE_ART } from "@/scene/assets.generated";
import { colors } from "@/theme";
import { Icon } from "../ui/Icon";

/** Proporción del medallón (viewBox 120×124: incluye la sombra dura). */
const ASPECT = 124 / 120;

/** Versión bloqueada: la misma forma en arena, sin revelar el dibujo. */
const lockedXml = (xml: string) =>
  xml
    .replace(/fill="(?!none)[^"]*"/g, `fill="${colors.sand}"`)
    .replace(/stroke="(?!none)[^"]*"/g, `stroke="${colors.line}"`)
    .replace(/fill-opacity="[^"]*"/g, "")
    .replace(/opacity="[^"]*"/g, "");

type Props = {
  /** Ruta del pack (`icon` del coleccionable), p. ej. "collectibles/cenacho.svg". */
  icon: string;
  size: number;
  locked?: boolean;
};

/** Medallón de un coleccionable (arte SVG del pack); bloqueado se ve como silueta. */
export const CollectibleArt = memo(function CollectibleArt({ icon, size, locked = false }: Props) {
  const art = COLLECTIBLE_ART[icon];
  const xml = useMemo(() => (art && locked ? lockedXml(art) : art), [art, locked]);
  if (!xml) {
    // Sin arte (pack nuevo aún sin ilustrar): trofeo genérico.
    return (
      <View style={{ width: size, height: size, alignItems: "center", justifyContent: "center" }}>
        <Icon name={locked ? "lock" : "trophy"} size={size * 0.45} color={locked ? colors.muted : colors.ink} />
      </View>
    );
  }
  return (
    <View accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      <SvgXml xml={xml} width={size} height={size * ASPECT} />
    </View>
  );
});
