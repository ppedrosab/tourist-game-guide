import { Tabs } from "expo-router";
import { TabBar } from "@/components/ui";
import { useI18n } from "@/i18n";

export default function TabsLayout() {
  const { t } = useI18n();
  return (
    <Tabs tabBar={(props) => <TabBar {...props} />} screenOptions={{ headerShown: false }}>
      <Tabs.Screen name="index" options={{ title: t("tabs.explorar") }} />
      <Tabs.Screen name="mis-rutas" options={{ title: t("tabs.misRutas") }} />
      <Tabs.Screen name="coleccion" options={{ title: t("tabs.coleccion") }} />
      <Tabs.Screen name="perfil" options={{ title: t("tabs.perfil") }} />
    </Tabs>
  );
}
