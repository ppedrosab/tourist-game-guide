import { useAudioPlayer, useAudioPlayerStatus } from "expo-audio";
import * as Speech from "expo-speech";
import { useCallback, useEffect, useRef, useState } from "react";
import type { AssetRef, LangCode } from "@/content/types";
import { AUDIO } from "@/scene/assets.generated";
import { estimateSpeechMs, speakerPitch } from "@/scene/voice";

export type Voice = {
  /** Hay locución sonando (real o simulada): mueve la boca del personaje. */
  speaking: boolean;
  /** Progreso 0..1 para la barra de la caja de diálogo. */
  progress: number;
  /** Hay audio grabado para esta línea. */
  hasAudio: boolean;
  /** Se oye algo: audio grabado o la voz sintética del móvil. */
  audible: boolean;
  replay: () => void;
};

type Line = { key: string; text: string; audio?: Partial<Record<LangCode, AssetRef>>; speaker?: string } | undefined;

const SPEECH_LANG: Record<string, string> = { es: "es-ES", en: "en-GB" };

/**
 * Voz de la línea actual. Con audio grabado (assets/audio, ver gen:assets) lo
 * reproduce con expo-audio; sin audio la lee la voz sintética del móvil
 * (expo-speech) con un tono por personaje. El reloj simulado según el texto
 * sigue moviendo la boca y la barra (y es lo único si no hay voz del sistema).
 * `active` corta al salir de la escena (modales, segundo plano).
 */
export function useVoice(line: Line, { enabled, active, lang = "es" }: { enabled: boolean; active: boolean; lang?: LangCode }): Voice {
  const ref = line?.audio?.[lang] ?? line?.audio?.es;
  const source = ref ? AUDIO[ref] : undefined;
  const hasAudio = source !== undefined && enabled;

  const synthetic = enabled && !hasAudio && !!line;
  // Estado de la voz sintética de la línea actual.
  const [tts, setTts] = useState<"idle" | "speaking" | "done">("idle");
  const speak = useCallback(() => {
    if (!line) return;
    Speech.stop();
    setTts("idle");
    Speech.speak(line.text, {
      language: SPEECH_LANG[lang] ?? lang,
      pitch: speakerPitch(line.speaker),
      rate: 0.95,
      onStart: () => setTts("speaking"),
      onDone: () => setTts("done"),
      onStopped: () => setTts((s) => (s === "speaking" ? "idle" : s)),
      onError: () => setTts("idle"),
    });
  }, [line?.key, line?.text, line?.speaker, lang]);

  const player = useAudioPlayer(null);
  const status = useAudioPlayerStatus(player);

  // Simulación: tiempo transcurrido acumulado (se congela si no está activa).
  const [elapsed, setElapsed] = useState(0);
  const duration = line ? estimateSpeechMs(line.text) : 0;
  const lastTick = useRef<number | null>(null);

  // Nueva línea: arrancar desde el principio.
  useEffect(() => {
    setElapsed(0);
    lastTick.current = null;
    if (hasAudio) {
      player.replace(source);
      player.seekTo(0);
      player.play();
    } else {
      player.pause();
    }
    if (synthetic && active) speak();
    else Speech.stop();
  }, [line?.key, hasAudio, synthetic]);

  // La voz sintética no se puede pausar en todos los sistemas: al salir se corta y al volver empieza la línea.
  useEffect(() => {
    if (!synthetic) return;
    if (active) {
      setElapsed(0);
      lastTick.current = null;
      speak();
    } else Speech.stop();
  }, [active]);
  useEffect(() => () => void Speech.stop(), []);

  // Pausa/reanuda con la escena.
  useEffect(() => {
    if (!hasAudio) return;
    if (active) {
      if (status.currentTime < status.duration) player.play();
    } else player.pause();
  }, [active]);

  // Reloj de la simulación.
  const simulating = !hasAudio && !!line && active && elapsed < duration;
  useEffect(() => {
    if (!simulating) {
      lastTick.current = null;
      return;
    }
    const timer = setInterval(() => {
      const now = Date.now();
      const dt = lastTick.current === null ? 0 : now - lastTick.current;
      lastTick.current = now;
      setElapsed((e) => Math.min(e + dt, duration));
    }, 50);
    return () => clearInterval(timer);
  }, [simulating, duration]);

  const replay = useCallback(() => {
    if (hasAudio) {
      player.seekTo(0);
      player.play();
    } else {
      lastTick.current = null;
      setElapsed(0);
      if (synthetic) speak();
    }
  }, [hasAudio, player, synthetic, speak]);

  if (hasAudio) {
    const progress = status.duration > 0 ? Math.min(status.currentTime / status.duration, 1) : 0;
    return { speaking: status.playing, progress, hasAudio, audible: true, replay };
  }
  const simulated = duration > 0 ? elapsed / duration : 0;
  if (synthetic && tts !== "idle") {
    // Manda la voz del sistema: la boca se mueve mientras habla y la barra no acaba antes que ella.
    const speaking = tts === "speaking";
    return { speaking, progress: speaking ? Math.min(simulated, 0.95) : 1, hasAudio, audible: true, replay };
  }
  return { speaking: simulating, progress: simulated, hasAudio, audible: false, replay };
}
