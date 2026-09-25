import { StyleSheet, View } from "react-native";
import type { Character } from "@/content/types";
import { spriteKeyOf } from "@/scene/cast";
import { Sprite } from "@/scene/Sprite";
import { border, colors, radius } from "@/theme";

/** Retrato: la cabeza y los hombros del sprite del personaje en un marco de tinta. */
export function Portrait({ character, size }: { character: Character; size: number }) {
  const sprite = spriteKeyOf(character.avatar);
  // El sprite mide 200×260 y la cabeza ocupa más o menos la franja 30-150: se amplía y se recorta.
  const width = size * 1.9;
  return (
    <View style={[styles.frame, { width: size, height: size }]}>
      {sprite ? (
        <View style={{ position: "absolute", left: (size - width) / 2, top: -size * 0.2 }}>
          <Sprite sprite={sprite} expression="neutral" width={width} contactShadow={false} />
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.sand,
    overflow: "hidden",
  },
});
