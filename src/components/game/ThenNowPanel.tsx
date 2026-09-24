import { useIsFocused } from "@react-navigation/native";
import { useCallback, useMemo, useRef, useState } from "react";
import { Image, LayoutChangeEvent, PanResponder, StyleSheet, Text, useWindowDimensions, View } from "react-native";
import { SvgXml } from "react-native-svg";
import type { AssetRef, I18nText } from "@/content/types";
import { useI18n } from "@/i18n";
import { SCENE_LAYERS, THEN_NOW_ART } from "@/scene/assets.generated";
import { border, colors, fonts, radius, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Icon } from "../ui/Icon";
import { Panel } from "../ui/Panel";
import { LiveCamera, requestCamera } from "./LiveCamera";

type Props = {
  then: AssetRef;
  /** "camera" = cámara en directo; si no, clave de escena cuya ilustración actual se usa. */
  now: AssetRef;
  caption?: I18nText;
  /** Escena de la parada: su ilustración actual es el "ahora" si no hay cámara. */
  sceneKey?: string;
  onNext: () => void;
};

const clamp = (v: number) => Math.max(0.04, Math.min(0.96, v));

/** Rellena el hueco como "cover": la ilustración se recorta centrada, sin deformarse. */
const cover = (xml: string) => xml.replace("<svg ", '<svg preserveAspectRatio="xMidYMid slice" ');

/**
 * "Antes y ahora": la ilustración de época a la izquierda y hoy a la derecha,
 * con una barra que se arrastra. Hoy es la cámara en directo (solo si el
 * jugador la enciende; no se guarda nada) o, sin cámara, la ilustración
 * actual de la escena.
 */
export function ThenNowPanel({ then, now, caption, sceneKey, onNext }: Props) {
  const { t, L } = useI18n();
  const window = useWindowDimensions();
  const focused = useIsFocused();
  const [size, setSize] = useState({ width: 0, height: Math.min(360, window.height * 0.42) });
  const [split, setSplit] = useState(0.5);
  const [cameraOn, setCameraOn] = useState(false);
  const [cameraFailed, setCameraFailed] = useState(false);

  const thenXml = useMemo(() => (THEN_NOW_ART[then] ? cover(THEN_NOW_ART[then]) : undefined), [then]);
  const flat = sceneKey ? SCENE_LAYERS[sceneKey]?.find((l) => l.role === "flat") : undefined;
  const wantsCamera = now === "camera";
  const showCamera = wantsCamera && cameraOn && !cameraFailed;
  const onCameraError = useCallback(() => setCameraFailed(true), []);

  const widthRef = useRef(0);
  widthRef.current = size.width;
  const pan = useMemo(
    () =>
      PanResponder.create({
        onStartShouldSetPanResponder: () => true,
        onMoveShouldSetPanResponder: () => true,
        onPanResponderGrant: (e) => widthRef.current && setSplit(clamp(e.nativeEvent.locationX / widthRef.current)),
        onPanResponderMove: (e) => widthRef.current && setSplit(clamp(e.nativeEvent.locationX / widthRef.current)),
      }),
    [],
  );

  const onLayout = (e: LayoutChangeEvent) => setSize((s) => ({ ...s, width: e.nativeEvent.layout.width }));
  const toggleCamera = async () => {
    if (cameraOn) return setCameraOn(false);
    if (await requestCamera()) {
      setCameraFailed(false);
      setCameraOn(true);
    } else setCameraFailed(true);
  };

  const { width, height } = size;
  return (
    <Panel nameplate={t("jugar.antesAhora")} nameplateColor={colors.sea}>
      <View style={[styles.box, { height }]} onLayout={onLayout}>
        {/* Ahora (debajo, a pantalla completa del recuadro). */}
        {showCamera ? (
          <LiveCamera active={focused} onError={onCameraError} />
        ) : flat ? (
          <Image source={flat.source} style={styles.fill} resizeMode="cover" />
        ) : (
          <View style={[styles.fill, { backgroundColor: colors.sand }]} />
        )}
        {/* Antes (encima, recortado hasta la barra). */}
        {thenXml && width > 0 ? (
          <View style={[styles.then, { width: width * split }]}>
            <SvgXml xml={thenXml} width={width} height={height} />
          </View>
        ) : null}
        <Text style={[styles.label, { left: 8 }]}>{t("antesAhora.antes")}</Text>
        <Text style={[styles.label, { right: 8 }]}>{t("antesAhora.ahora")}</Text>
        {/* Barra. */}
        <View style={[styles.bar, { left: width * split - 1.5 }]} />
        <View style={[styles.knob, { left: width * split - 18, top: height / 2 - 18 }]}>
          <Icon name="back" size={12} strokeWidth={3} />
          <Icon name="next" size={12} strokeWidth={3} />
        </View>
        {/* Capa que recibe el arrastre (coordenadas relativas al recuadro). */}
        <View
          style={StyleSheet.absoluteFill}
          {...pan.panHandlers}
          accessible
          accessibilityRole="adjustable"
          accessibilityLabel={t("antesAhora.deslizador")}
          accessibilityHint={t("antesAhora.arrastra")}
          accessibilityValue={{ min: 0, max: 100, now: Math.round(split * 100) }}
          accessibilityActions={[{ name: "increment" }, { name: "decrement" }]}
          onAccessibilityAction={(e) =>
            setSplit((s) => clamp(s + (e.nativeEvent.actionName === "increment" ? 0.1 : -0.1)))
          }
        />
      </View>
      {caption ? <Text style={type.body}>{L(caption)}</Text> : null}
      {wantsCamera && cameraFailed ? <Text style={type.caption}>{t("antesAhora.sinCamara")}</Text> : null}
      {wantsCamera ? (
        <Button3D
          label={cameraOn && !cameraFailed ? t("antesAhora.verIlustracion") : t("antesAhora.usarCamara")}
          icon="camera"
          variant="secondary"
          small
          onPress={toggleCamera}
        />
      ) : null}
      <Button3D label={t("comun.siguiente")} icon="next" small onPress={onNext} />
    </Panel>
  );
}

const styles = StyleSheet.create({
  box: {
    overflow: "hidden",
    borderRadius: radius.md,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  fill: { position: "absolute", top: 0, left: 0, width: "100%", height: "100%" },
  then: { position: "absolute", top: 0, bottom: 0, left: 0, overflow: "hidden" },
  label: {
    position: "absolute",
    top: 8,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: radius.sm,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.paper,
    fontFamily: fonts.bold,
    fontSize: 12,
    color: colors.ink,
    overflow: "hidden",
  },
  bar: { position: "absolute", top: 0, bottom: 0, width: 3, backgroundColor: colors.paper },
  knob: {
    position: "absolute",
    width: 36,
    height: 36,
    borderRadius: 18,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.paper,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
  },
});
