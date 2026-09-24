import { useIsFocused } from "@react-navigation/native";
import { ReactNode, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AppState, Image, LayoutChangeEvent, Platform, PointerEvent, StyleSheet, View } from "react-native";
import Animated, {
  SensorType,
  SharedValue,
  useAnimatedSensor,
  useAnimatedStyle,
  useFrameCallback,
  useReducedMotion,
  useSharedValue,
  withTiming,
} from "react-native-reanimated";
import { colors } from "@/theme";
import { SCENE_LAYERS } from "./assets.generated";
import type { CastMember } from "./cast";
import { CastLayer } from "./CastLayer";
import type { CastShadow } from "./sun";
import {
  CHARACTER_DEPTH,
  depthOf,
  INITIAL_TILT,
  layerOffset,
  overscanScale,
  stageAmplitude,
  stepPointer,
  stepTilt,
  TiltState,
} from "./parallax";

/** Proporción de las ilustraciones (viewBox 390×560). */
export const SCENE_ASPECT = 390 / 560;

type Props = {
  /** Clave de escena (p. ej. "marina"); ver sceneKeyFor. */
  sceneKey: string | undefined;
  /** Personajes en escena (plano del primer plano). */
  cast?: CastMember[];
  /** Hay locución sonando (lip-sync de quien habla). */
  talking?: boolean;
  /** Sombra proyectada de los personajes según el sol. */
  shadow?: CastShadow;
  /** Fondo si la escena no tiene capas. */
  fallback?: ReactNode;
  testID?: string;
};

/**
 * Escenario con fondo por capas y parallax por giroscopio.
 *
 * Todo el movimiento ocurre en el hilo de interfaz: el sensor de rotación de
 * reanimated alimenta un callback por fotograma que suaviza la inclinación
 * (stepTilt) y cada capa lee su desplazamiento en useAnimatedStyle. React no
 * vuelve a renderizar mientras se mueve el móvil.
 *
 * En web no hay giroscopio: el puntero sobre el escenario hace de inclinación.
 * Con "Reducir movimiento" activado la escena queda quieta.
 */
export function SceneStage({ sceneKey, cast, talking, shadow, fallback, testID }: Props) {
  const layers = sceneKey ? SCENE_LAYERS[sceneKey] : undefined;
  const [size, setSize] = useState({ width: 0, height: 0 });
  const onLayout = useCallback((e: LayoutChangeEvent) => {
    const { width, height } = e.nativeEvent.layout;
    setSize((s) => (s.width === width && s.height === height ? s : { width, height }));
  }, []);

  const reduceMotion = useReducedMotion();
  const sensor = useAnimatedSensor(SensorType.ROTATION, { interval: "auto" });
  const tilt = useSharedValue<TiltState>(INITIAL_TILT);
  const pointer = useSharedValue({ active: false, x: 0, y: 0 });

  const frame = useFrameCallback(({ timeSincePreviousFrame }) => {
    "worklet";
    const dt = timeSincePreviousFrame ?? 16;
    const prev = tilt.value;
    if (reduceMotion) {
      if (prev.x !== 0 || prev.y !== 0) tilt.value = { ...prev, x: 0, y: 0 };
      return;
    }
    let next: TiltState;
    if (pointer.value.active || !sensor.isAvailable) {
      const p = pointer.value;
      next = stepPointer(prev, p.active ? p.x : 0, p.active ? p.y : 0, dt);
    } else {
      const { roll, pitch } = sensor.sensor.value;
      next = stepTilt(prev, roll, pitch, dt);
    }
    // Con el móvil quieto no se escribe: las capas no se recalculan y se ahorra batería.
    // (La referencia de recentrado sí se guarda cuando cambia apreciablemente.)
    const moved = Math.abs(next.x - prev.x) > 0.0003 || Math.abs(next.y - prev.y) > 0.0003;
    const rebased =
      next.ready !== prev.ready ||
      Math.abs(next.baseRoll - prev.baseRoll) > 0.002 ||
      Math.abs(next.basePitch - prev.basePitch) > 0.002;
    if (moved || rebased) tilt.value = next;
  });

  // Congelado si la escena no está a la vista (modal encima o app en segundo plano).
  const focused = useIsFocused();
  const [appActive, setAppActive] = useState(AppState.currentState === "active");
  useEffect(() => {
    const sub = AppState.addEventListener("change", (s) => setAppActive(s === "active"));
    return () => sub.remove();
  }, []);
  useEffect(() => {
    frame.setActive(focused && appActive);
  }, [frame, focused, appActive]);

  // Capas que se mueven (con profundidad) y efectos fijos (fx), sin la compuesta.
  const moving = layers?.filter((l) => l.role !== "flat" && depthOf(l.role) !== null) ?? [];
  const fx = layers?.filter((l) => depthOf(l.role) === null) ?? [];
  const total = moving.length + fx.length;
  // Escala común y amplitud para el tamaño real del escenario.
  const maxDepth = Math.max(CHARACTER_DEPTH, ...moving.map((l) => depthOf(l.role) ?? 0));
  const scale = overscanScale(size.width, size.height, maxDepth);
  const { ax, ay } = stageAmplitude(size.width, size.height);
  // Caja de la ilustración: "cover" del escenario, centrada.
  const box = useMemo(() => {
    const w = Math.max(size.width, size.height * SCENE_ASPECT);
    const h = w / SCENE_ASPECT;
    return { width: w, height: h, left: (size.width - w) / 2, top: (size.height - h) / 2 };
  }, [size]);

  // Las capas aparecen juntas cuando todas han cargado (debajo está la imagen compuesta).
  const layersOpacity = useSharedValue(0);
  const loadedRef = useRef(0);
  const onLayerLoad = useCallback(() => {
    loadedRef.current += 1;
    if (loadedRef.current >= total) layersOpacity.value = withTiming(1, { duration: 220 });
  }, [total, layersOpacity]);

  // Web: el puntero sobre el escenario hace de giroscopio (relativo al propio escenario,
  // no a la capa desplazada que haya debajo del cursor).
  const pointerHandlers =
    Platform.OS === "web"
      ? {
          onPointerMove: (e: PointerEvent) => {
            // En web currentTarget es el <div> del escenario.
            const r = (e.currentTarget as unknown as Element).getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return;
            pointer.value = {
              active: true,
              x: ((e.nativeEvent.clientX - r.left) / r.width) * 2 - 1,
              y: ((e.nativeEvent.clientY - r.top) / r.height) * 2 - 1,
            };
          },
          onPointerLeave: () => {
            pointer.value = { active: false, x: 0, y: 0 };
          },
        }
      : {};

  const fxStyle = useAnimatedStyle(() => ({ opacity: layersOpacity.value }));
  const flat = layers?.find((l) => l.role === "flat");
  const ready = size.width > 0 && layers;

  return (
    <View style={styles.stage} onLayout={onLayout} testID={testID} {...pointerHandlers}>
      {!layers ? <View style={styles.fallback}>{fallback}</View> : null}
      {ready ? (
        <>
          {flat ? (
            <View style={[styles.abs, box, { transform: [{ scale }] }]}>
              <Image source={flat.source} style={styles.fill} resizeMode="stretch" />
            </View>
          ) : null}
          {moving.map((layer) => (
            <ParallaxLayer
              key={`${sceneKey}-${layer.order}`}
              depth={depthOf(layer.role) ?? 0}
              tilt={tilt}
              scale={scale}
              ax={ax}
              ay={ay}
              opacity={layersOpacity}
              box={box}
            >
              <Image source={layer.source} style={styles.fill} resizeMode="stretch" onLoad={onLayerLoad} />
            </ParallaxLayer>
          ))}
          {/* Efectos (rayos, brillos): fijos, con la misma escala, sobre el fondo. */}
          {fx.map((layer) => (
            <Animated.View
              key={`${sceneKey}-${layer.order}`}
              style={[styles.abs, styles.noTouch, box, { transform: [{ scale }] }, fxStyle]}
            >
              <Image source={layer.source} style={styles.fill} resizeMode="stretch" onLoad={onLayerLoad} />
            </Animated.View>
          ))}
          {/* Personajes: pisan el primer plano y se mueven con él; por encima de los efectos
              para que la luz no los lave. */}
          {cast && cast.length > 0 ? (
            <ParallaxLayer depth={CHARACTER_DEPTH} tilt={tilt} scale={scale} ax={ax} ay={ay} box={box}>
              <CastLayer cast={cast} width={box.width} height={box.height} talking={talking} shadow={shadow} />
            </ParallaxLayer>
          ) : null}
        </>
      ) : null}
    </View>
  );
}

type LayerProps = {
  depth: number;
  tilt: SharedValue<TiltState>;
  scale: number;
  ax: number;
  ay: number;
  box: { width: number; height: number; left: number; top: number };
  opacity?: SharedValue<number>;
  children: ReactNode;
};

function ParallaxLayer({ depth, tilt, scale, ax, ay, box, opacity, children }: LayerProps) {
  const style = useAnimatedStyle(() => {
    const { tx, ty } = layerOffset(tilt.value.x, tilt.value.y, depth, ax, ay);
    return {
      opacity: opacity ? opacity.value : 1,
      transform: [{ translateX: tx }, { translateY: ty }, { scale }],
    };
  }, [depth, scale, ax, ay]);
  return <Animated.View style={[styles.abs, box, style]}>{children}</Animated.View>;
}

const styles = StyleSheet.create({
  stage: { flex: 1, overflow: "hidden", backgroundColor: colors.ink },
  abs: { position: "absolute" },
  // width/height explícitos: en web la Image aplica el tamaño intrínseco del asset por encima de absoluteFill.
  fill: { position: "absolute", top: 0, left: 0, width: "100%", height: "100%" },
  fallback: {
    ...StyleSheet.absoluteFillObject,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.sand,
  },
  noTouch: { pointerEvents: "none" },
});
