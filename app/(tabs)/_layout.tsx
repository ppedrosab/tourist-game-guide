import { Tabs } from "expo-router";
import { TabBar } from "@/components/ui";

export default function TabsLayout() {
  return (
    <Tabs tabBar={(props) => <TabBar {...props} />} screenOptions={{ headerShown: false }}>
      <Tabs.Screen name="index" options={{ title: "Explorar" }} />
      <Tabs.Screen name="mis-rutas" options={{ title: "Mis rutas" }} />
      <Tabs.Screen name="coleccion" options={{ title: "Colección" }} />
      <Tabs.Screen name="perfil" options={{ title: "Perfil" }} />
    </Tabs>
  );
}
