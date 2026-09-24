import { router } from "expo-router";
import { useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AzulejoBackground, ChoiceCard, DialogBox, Hud, HudStop } from "@/components/ui";
import { border, colors, fonts, radius } from "@/theme";

/**
 * Pantalla de juego (modo ruta). En la fase 1 es una maqueta con datos fijos;
 * en la fase 2 la alimenta el motor narrativo con el pack JSON.
 */
const STOPS: HudStop[] = [
  { id: "n1" },
  { id: "n2" },
  { id: "rama", branch: "dinero" },
  { id: "n4" },
  { id: "n5" },
  { id: "n6" },
];

export default function Jugar() {
  const insets = useSafeAreaInsets();
  const [showChoices, setShowChoices] = useState(false);

  return (
    <View style={styles.root}>
      <AzulejoBackground />
      {/* Fase 3: <SceneStage> con fondo por capas, parallax y sprites. */}
      <View style={styles.stage}>
        <Text style={styles.stageText}>Escena · Calle Larios, 1891</Text>
      </View>

      <View style={[styles.hud, { top: insets.top + 8 }]}>
        <Hud
          stops={STOPS}
          current={1}
          clues={1}
          onPause={() => router.push("/pausa")}
          onNotebook={() => router.push("/cuaderno")}
        />
      </View>

      <View style={[styles.dialog, { bottom: insets.bottom + 12 }]}>
        {showChoices ? (
          <DialogBox
            speaker="Er Cenachero"
            text="Aquí se nos parte el camino, detective. ¿Qué rastro seguimos?"
            choices={
              <>
                <ChoiceCard
                  title="El rastro del dinero"
                  hint="Hacia el antiguo puerto y las tabernas"
                  meta="350 m · 5 min · 2 paradas"
                  branch="dinero"
                  onPress={() => setShowChoices(false)}
                />
                <ChoiceCard
                  title="El rastro del poder"
                  hint="Hacia la antigua Plaza Mayor"
                  meta="120 m · 2 min · 1 parada"
                  branch="poder"
                  onPress={() => setShowChoices(false)}
                />
              </>
            }
          />
        ) : (
          <DialogBox
            speaker="Er Cenachero"
            text="Esta calle la pagó la Casa Larios pa' unir el centro con el puerto. En Málaga todo gira alrededor del comercio."
            audioProgress={0.45}
            onNext={() => setShowChoices(true)}
          />
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.ink },
  stage: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: "70%",
    backgroundColor: colors.sand,
    borderBottomWidth: border.thick,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  stageText: { fontFamily: fonts.bold, color: colors.muted },
  hud: { position: "absolute", left: 14, right: 14 },
  dialog: { position: "absolute", left: 12, right: 12, borderRadius: radius.xl },
});
