import { useEffect } from "react";
import { StyleSheet, View } from "react-native";
import Animated, { FadeIn, FadeOut, useAnimatedStyle, useSharedValue, withTiming } from "react-native-reanimated";
import type { CastMember } from "./cast";
import { Sprite } from "./Sprite";

/**
 * Proporciones dentro de la ilustración (390×560): los pies apoyan cerca del
 * borde inferior y cada personaje ocupa algo más de la mitad del alto.
 */
const FEET_Y = 0.985;
const HEIGHT = 0.5;
const CENTER_X = { left: 0.28, right: 0.72 } as const;
const SPRITE_ASPECT = 200 / 260;

type Props = { cast: CastMember[]; width: number; height: number };

/** Personajes en el plano del primer plano del escenario. */
export function CastLayer({ cast, width, height }: Props) {
  if (width === 0) return null;
  const h = height * HEIGHT;
  const w = h * SPRITE_ASPECT;
  return (
    <View style={styles.layer}>
      {cast.map((member) => (
        <Animated.View
          key={member.characterId}
          entering={FadeIn.duration(260)}
          exiting={FadeOut.duration(180)}
          style={[styles.member, { left: width * CENTER_X[member.position] - w / 2, top: height * FEET_Y - h, width: w, height: h }]}
        >
          <Speaking speaking={member.speaking}>
            <Sprite sprite={member.sprite} expression={member.expression} width={w} />
          </Speaking>
        </Animated.View>
      ))}
    </View>
  );
}

/** Quien habla da un pequeño paso al frente; el resto se queda un poco atrás. */
function Speaking({ speaking, children }: { speaking: boolean; children: React.ReactNode }) {
  const v = useSharedValue(speaking ? 1 : 0);
  useEffect(() => {
    v.value = withTiming(speaking ? 1 : 0, { duration: 200 });
  }, [speaking, v]);
  const style = useAnimatedStyle(() => ({
    transform: [{ translateY: -4 * v.value }, { scale: 0.96 + 0.04 * v.value }],
  }));
  return <Animated.View style={[styles.fill, style]}>{children}</Animated.View>;
}

const styles = StyleSheet.create({
  layer: { ...StyleSheet.absoluteFillObject, pointerEvents: "none" },
  member: { position: "absolute" },
  fill: { flex: 1, transformOrigin: "bottom" },
});
