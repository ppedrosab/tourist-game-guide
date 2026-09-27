import html2canvas from "html2canvas";
import type { RefObject } from "react";
import type { View } from "react-native";

export const SHARE_SIZE = { width: 1080, height: 1350 };

/**
 * Web: captura la tarjeta con html2canvas (en react-native-web el ref es el nodo del DOM; el
 * captureRef de react-native-view-shot usa findNodeHandle, que en web no existe) y la comparte con
 * el menú del navegador si admite archivos; si no, la descarga como PNG.
 */
export async function shareImage(ref: RefObject<View | null>, title: string): Promise<boolean> {
  const node = ref.current as unknown as HTMLElement | null;
  if (!node) return false;
  const canvas = await html2canvas(node, {
    backgroundColor: null,
    scale: SHARE_SIZE.width / node.offsetWidth,
    // la tarjeta vive fuera de la pantalla: se clona en su sitio para que salga entera
    onclone: (_doc, el) => {
      const holder = el.parentElement;
      if (holder) holder.style.left = "0px";
    },
  });
  const blob = await new Promise<Blob | null>((ok) => canvas.toBlob(ok, "image/png"));
  if (!blob) return false;
  const file = new File([blob], "mi-final.png", { type: "image/png" });
  const nav = navigator as Navigator & { canShare?: (d: ShareData) => boolean };
  if (nav.share && nav.canShare?.({ files: [file] })) {
    try {
      await nav.share({ files: [file], title });
      return true;
    } catch {
      return false;
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "mi-final.png";
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return true;
}
