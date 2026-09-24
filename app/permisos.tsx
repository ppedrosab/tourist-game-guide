import { router } from "expo-router";
import { useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AzulejoBackground, Button3D, Icon, IconButton, IconName, Panel } from "@/components/ui";
import { getCatalog } from "@/engine/catalog";
import { requestGamePermissions } from "@/geo/permissions";
import { StringKey, useI18n } from "@/i18n";
import { border, colors, type } from "@/theme";

const ITEMS: { icon: IconName; title: StringKey; text: StringKey; color: string }[] = [
  { icon: "pin", title: "permisos.ubicacion", text: "permisos.ubicacionTexto", color: colors.sea },
  { icon: "volume", title: "permisos.avisos", text: "permisos.avisosTexto", color: colors.clay },
  { icon: "subtitles", title: "permisos.audio", text: "permisos.audioTexto", color: colors.ink },
];

export default function Permisos() {
  const insets = useSafeAreaInsets();
  const { t, L } = useI18n();
  // El guía de la primera ruta del catálogo es quien pide los permisos.
  const firstPack = getCatalog().packs[0];
  const guide = firstPack?.characters.find((c) => c.id === firstPack.routes[0]?.guideCharacterId);
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
        <IconButton icon="back" label={t("comun.volver")} onPress={() => router.back()} />
      </View>
      <View style={{ flex: 1 }} />
      <View style={{ padding: 12, paddingBottom: insets.bottom + 16 }}>
        <Panel nameplate={guide ? L(guide.name) : undefined}>
          <Text style={type.title}>{t("permisos.titulo")}</Text>
          {ITEMS.map((item) => (
            <View key={item.title} style={styles.item}>
              <View style={[styles.medal, { backgroundColor: item.color }]}>
                <Icon name={item.icon} color={colors.white} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={type.label}>{t(item.title)}</Text>
                <Text style={type.secondary}>{t(item.text)}</Text>
              </View>
            </View>
          ))}
          <Button3D label={pidiendo ? t("permisos.pidiendo") : t("permisos.permitir")} disabled={pidiendo} onPress={permitir} />
          <Button3D label={t("permisos.ahoraNo")} variant="ghost" onPress={continuar} />
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
