import { router } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AzulejoBackground, Button3D, Panel } from "@/components/ui";
import { useI18n } from "@/i18n";
import { colors, type } from "@/theme";

export default function Bienvenida() {
  const insets = useSafeAreaInsets();
  const { t } = useI18n();
  return (
    <View style={styles.root}>
      <AzulejoBackground />
      {/* Fase 3: aquí va la escena de la Plaza de la Marina con el cenachero. */}
      <View style={{ flex: 1 }} />
      <View style={{ padding: 12, paddingBottom: insets.bottom + 16 }}>
        <Panel>
          <Text style={type.title}>{t("bienvenida.titulo")}</Text>
          <Text style={type.secondary}>{t("bienvenida.texto")}</Text>
          <Button3D label={t("bienvenida.empezar")} icon="next" onPress={() => router.push("/permisos")} />
          <Button3D label={t("bienvenida.yaTengo")} variant="ghost" onPress={() => router.replace("/")} />
        </Panel>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({ root: { flex: 1, backgroundColor: colors.ink } });
