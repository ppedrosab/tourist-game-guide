import { createElement, useEffect, useRef } from "react";
import { StyleSheet, View } from "react-native";

/**
 * Web: vista previa con getUserMedia y un <video>. No se usa expo-camera en
 * web porque su módulo arranca un lector de QR que descarga un script de un
 * CDN aunque no se use. Nativo: LiveCamera.native.tsx.
 */
export async function requestCamera(): Promise<boolean> {
  try {
    if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) return false;
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    stream.getTracks().forEach((t) => t.stop());
    return true;
  } catch {
    return false;
  }
}

export function LiveCamera({ active, onError }: { active: boolean; onError: () => void }) {
  const video = useRef<HTMLVideoElement | null>(null);
  useEffect(() => {
    if (!active) return;
    let stream: MediaStream | undefined;
    let cancelled = false;
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "environment" } })
      .then((s) => {
        if (cancelled) return s.getTracks().forEach((t) => t.stop());
        stream = s;
        if (video.current) video.current.srcObject = s;
      })
      .catch(onError);
    return () => {
      cancelled = true;
      stream?.getTracks().forEach((t) => t.stop());
    };
  }, [active, onError]);
  return (
    <View style={StyleSheet.absoluteFill}>
      {createElement("video", {
        ref: video,
        autoPlay: true,
        playsInline: true,
        muted: true,
        style: { width: "100%", height: "100%", objectFit: "cover" },
      })}
    </View>
  );
}
