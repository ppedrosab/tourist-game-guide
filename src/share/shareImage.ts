import * as Sharing from "expo-sharing";
import type { RefObject } from "react";
import type { View } from "react-native";
import { captureRef } from "react-native-view-shot";

/** Tamaño de la imagen para redes (4:5, el formato vertical de Instagram). */
export const SHARE_SIZE = { width: 1080, height: 1350 };

/** Captura la tarjeta como PNG y abre el menú de compartir del sistema. Devuelve false si no se pudo. */
export async function shareImage(ref: RefObject<View | null>, title: string): Promise<boolean> {
  if (!ref.current || !(await Sharing.isAvailableAsync())) return false;
  const uri = await captureRef(ref, { format: "png", quality: 1, result: "tmpfile", ...SHARE_SIZE });
  await Sharing.shareAsync(uri, { mimeType: "image/png", dialogTitle: title, UTI: "public.png" });
  return true;
}
