import { router } from "expo-router";
import { useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AzulejoBackground, Button3D, Icon, IconButton, IconName, Panel } from "@/components/ui";
import { requestGamePermissions } from "@/geo/permissions";
import { border, colors, type } from "@/theme";

const ITEMS: { icon: IconName; title: string; text: string; color: string }[] = [
  { icon: "pin", title: "Ubicación «siempre»", text: "Así las escenas empiezan solas al llegar, con el móvil en el bolsillo.", color: colors.sea },
  { icon: "volume", title: "Notificaciones", text: "Te aviso cuando llegues a cada parada.", color: colors.clay },
  { icon: "subtitles", title: "Auriculares o subtítulos", text: "Las voces se oyen mejor; los subtítulos van siempre activados.", color: colors.ink },
];

export default function Permisos() {
  const insets = useSafeAreaInsets();
  const [pidiendo, setPidiendo] = useState(false);
  const continuar = () => router.replace("/");
  const permitir = async () => {
    setPidiendo(true);
    await requestGamePermissions();
    continuar();
  };
  return (
    <View style={styles.root}>
      <AzulejoBackground />
      <View style={{ paddingTop: insets.top + 12, paddingHorizontal: 20 }}>
        <IconButton icon="back" label="Volver" onPress={() => router.back()} />
      </View>
      <View style={{ flex: 1 }} />
      <View style={{ padding: 12, paddingBottom: insets.bottom + 16 }}>
        <Panel nameplate="Er Cenachero">
          <Text style={type.title}>¿Me dejas acompañarte por la calle?</Text>
          {ITEMS.map((item) => (
            <View key={item.title} style={styles.item}>
              <View style={[styles.medal, { backgroundColor: item.color }]}>
                <Icon name={item.icon} color={colors.white} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={type.label}>{item.title}</Text>
                <Text style={type.secondary}>{item.text}</Text>
              </View>
            </View>
          ))}
          <Button3D label={pidiendo ? "Un momento…" : "Permitir y continuar"} disabled={pidiendo} onPress={permitir} />
          <Button3D label="Ahora no" variant="ghost" onPress={continuar} />
        </Panel>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.ink },
  item: { flexDirection: "row", gap: 12, alignItems: "flex-start" },
  medal: {
    width: 44,
    height: 44,
    borderRadius: 12,
    borderWidth: border.thin,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
});
