import { setAudioModeAsync } from "expo-audio";
import { useEffect } from "react";
import { useProgress } from "@/store/progress";

/**
 * Sesión de audio de la app: suena aunque el móvil esté en silencio y, en manos libres, sigue sonando
 * con la pantalla apagada (en iOS hace falta `UIBackgroundModes: audio`, en app.json). Baja el volumen
 * de otras apps (música) mientras habla un personaje en vez de cortarlas.
 */
export function useHandsFreeAudio() {
  const handsFree = useProgress((s) => s.handsFree);
  useEffect(() => {
    setAudioModeAsync({
      playsInSilentMode: true,
      shouldPlayInBackground: handsFree,
      interruptionMode: "duckOthers",
    }).catch(() => undefined);
  }, [handsFree]);
}
