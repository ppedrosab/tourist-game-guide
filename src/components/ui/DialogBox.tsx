import { ReactNode } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useI18n } from "@/i18n";
import { border, colors, fonts, hardShadow, radius, type } from "@/theme";
import { HardShadow } from "./HardShadow";
import { Icon } from "./Icon";
import { Panel } from "./Panel";

type Props = {
  speaker: string;
  text: string;
  speakerColor?: string;
  /** Retrato pequeño del personaje (p. ej. un <Sprite /> recortado). */
  portrait?: ReactNode;
  /** Si hay decisiones, sustituyen a la barra de audio y al botón de avance. */
  choices?: ReactNode;
  extra?: ReactNode;
  nextLabel?: string;
  onNext?: () => void;
  onReplay?: () => void;
  /** Progreso del audio entre 0 y 1. */
  audioProgress?: number;
};

/** Caja de diálogo estilo novela visual: placa con nombre, texto, audio y avance. */
export function DialogBox({
  speaker,
  text,
  speakerColor = colors.clay,
  portrait,
  choices,
  extra,
  nextLabel,
  onNext,
  onReplay,
  audioProgress = 0,
}: Props) {
  const { t } = useI18n();
  return (
    <Panel nameplate={speaker} nameplateColor={speakerColor}>
      {portrait ? <View style={styles.portrait}>{portrait}</View> : null}
      <Text style={type.dialogue} accessibilityRole="text">
        {text}
      </Text>
      {extra}
      {choices ? (
        <View style={{ gap: 10 }}>{choices}</View>
      ) : (
        <View style={styles.footer}>
          <Pressable style={styles.audio} onPress={onReplay} accessibilityRole="button" accessibilityLabel={t("jugar.repetirAudio")}>
            <Icon name="volume" size={18} />
            <View style={styles.track}>
              <View style={[styles.fill, { width: `${Math.round(audioProgress * 100)}%` }]} />
            </View>
            <Icon name="replay" size={16} />
          </Pressable>
          <Pressable onPress={onNext} accessibilityRole="button">
            {({ pressed }) => (
              <HardShadow radius={radius.md} offset={hardShadow.sm} pressed={pressed}>
                <View style={styles.next}>
                  <Text style={styles.nextText}>{nextLabel ?? t("comun.siguiente")}</Text>
                  <Icon name="next" size={16} color={colors.white} strokeWidth={2.6} />
                </View>
              </HardShadow>
            )}
          </Pressable>
        </View>
      )}
    </Panel>
  );
}

const styles = StyleSheet.create({
  portrait: {
    position: "absolute",
    top: -34,
    right: 16,
    width: 56,
    height: 56,
    borderRadius: 16,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.sand,
    overflow: "hidden",
    alignItems: "center",
  },
  footer: { flexDirection: "row", alignItems: "center", gap: 10 },
  audio: {
    flex: 1,
    height: 46,
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 12,
    borderRadius: radius.md,
    backgroundColor: colors.sand,
  },
  track: { flex: 1, height: 5, borderRadius: 3, backgroundColor: "#D5C6AC", overflow: "hidden" },
  fill: { height: 5, borderRadius: 3, backgroundColor: colors.clay },
  next: {
    height: 46,
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 18,
    borderRadius: radius.md,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.clay,
  },
  nextText: { fontFamily: fonts.bold, fontSize: 15, color: colors.white },
});
