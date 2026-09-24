import { useAudioPlayer, useAudioPlayerStatus } from "expo-audio";
import { useCallback, useEffect, useRef, useState } from "react";
import type { AssetRef, LangCode } from "@/content/types";
import { AUDIO } from "@/scene/assets.generated";
import { estimateSpeechMs } from "@/scene/voice";

export type Voice = {
  /** Hay locución sonando (real o simulada): mueve la boca del personaje. */
  speaking: boolean;
  /** Progreso 0..1 para la barra de la caja de diálogo. */
  progress: number;
  /** Hay audio grabado para esta línea. */
  hasAudio: boolean;
  replay: () => void;
};

type Line = { key: string; text: string; audio?: Partial<Record<LangCode, AssetRef>> } | undefined;

/**
 * Voz de la línea actual. Con audio grabado (assets/audio, ver gen:assets) lo
 * reproduce con expo-audio; sin audio simula la duración según el texto, para
 * que el lip-sync y la barra funcionen igual. `active` pausa al salir de la
 * escena (modales, segundo plano).
 */
export function useVoice(line: Line, { enabled, active, lang = "es" }: { enabled: boolean; active: boolean; lang?: LangCode }): Voice {
  const ref = line?.audio?.[lang] ?? line?.audio?.es;
  const source = ref ? AUDIO[ref] : undefined;
  const hasAudio = source !== undefined && enabled;

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
  }, [line?.key, hasAudio]);

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
    }
  }, [hasAudio, player]);

  if (hasAudio) {
    const progress = status.duration > 0 ? Math.min(status.currentTime / status.duration, 1) : 0;
    return { speaking: status.playing, progress, hasAudio, replay };
  }
  return { speaking: simulating, progress: duration > 0 ? elapsed / duration : 0, hasAudio, replay };
}
