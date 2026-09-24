import { DMSans_400Regular, DMSans_500Medium, DMSans_700Bold } from "@expo-google-fonts/dm-sans";
import { Fraunces_700Bold } from "@expo-google-fonts/fraunces";
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { StatusBar } from "expo-status-bar";
import { useEffect } from "react";
import { colors } from "@/theme";

SplashScreen.preventAutoHideAsync();

/**
 * Dos modos de navegación:
 *  - Fuera de la ruta: pestañas (app/(tabs)).
 *  - Dentro de la ruta: pantalla de juego con HUD (app/ruta/[id]/jugar) y modales de pausa y cuaderno.
 */
export default function RootLayout() {
  const [loaded] = useFonts({ Fraunces_700Bold, DMSans_400Regular, DMSans_500Medium, DMSans_700Bold });

  useEffect(() => {
    if (loaded) SplashScreen.hideAsync();
  }, [loaded]);

  if (!loaded) return null;

  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: colors.cream } }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="bienvenida" />
        <Stack.Screen name="permisos" />
        <Stack.Screen name="ciudad/[id]" />
        <Stack.Screen name="ruta/[id]/index" />
        <Stack.Screen
          name="ruta/[id]/jugar"
          options={{ gestureEnabled: false, contentStyle: { backgroundColor: colors.ink } }}
        />
        <Stack.Screen name="pausa" options={{ presentation: "transparentModal", animation: "fade" }} />
        <Stack.Screen name="cuaderno" options={{ presentation: "modal" }} />
      </Stack>
    </>
  );
}
