import { CameraView, Camera } from "expo-camera";
import { StyleSheet } from "react-native";

/** Pide permiso de cámara. true si se concede. */
export async function requestCamera(): Promise<boolean> {
  const current = await Camera.getCameraPermissionsAsync();
  if (current.granted) return true;
  return (await Camera.requestCameraPermissionsAsync()).granted;
}

/** Cámara trasera en directo (solo vista previa: no se captura nada). */
export function LiveCamera({ active, onError }: { active: boolean; onError: () => void }) {
  return <CameraView style={StyleSheet.absoluteFill} facing="back" active={active} onMountError={onError} />;
}
