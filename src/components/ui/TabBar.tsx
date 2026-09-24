import { BottomTabBarProps } from "@react-navigation/bottom-tabs";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { border, colors, fonts, hardShadow, radius } from "@/theme";
import { HardShadow } from "./HardShadow";
import { Icon, IconName } from "./Icon";

const ICONS: Record<string, IconName> = {
  index: "compass",
  "mis-rutas": "route",
  coleccion: "trophy",
  perfil: "user",
};

/** Barra de pestañas flotante: solo se muestra fuera de la ruta. */
export function TabBar({ state, descriptors, navigation }: BottomTabBarProps) {
  const insets = useSafeAreaInsets();
  return (
    <View style={[styles.wrap, { bottom: Math.max(insets.bottom, 12) + 8 }]} pointerEvents="box-none">
      <HardShadow radius={20} offset={hardShadow.md}>
        <View style={styles.bar}>
          {state.routes.map((route, index) => {
            const focused = state.index === index;
            const label = (descriptors[route.key].options.title ?? route.name) as string;
            const onPress = () => {
              const event = navigation.emit({ type: "tabPress", target: route.key, canPreventDefault: true });
              if (!focused && !event.defaultPrevented) navigation.navigate(route.name, route.params);
            };
            return (
              <Pressable
                key={route.key}
                onPress={onPress}
                accessibilityRole="tab"
                accessibilityState={{ selected: focused }}
                accessibilityLabel={label}
                style={[styles.item, focused && styles.itemActive]}
              >
                <Icon name={ICONS[route.name] ?? "compass"} color={focused ? colors.white : colors.ink} />
                <Text style={[styles.label, { color: focused ? colors.white : colors.ink }]}>{label}</Text>
              </Pressable>
            );
          })}
        </View>
      </HardShadow>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { position: "absolute", left: 14, right: 14 },
  bar: {
    flexDirection: "row",
    gap: 4,
    padding: 6,
    borderRadius: 20,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.paper,
  },
  item: {
    flex: 1,
    height: 54,
    alignItems: "center",
    justifyContent: "center",
    gap: 2,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: "transparent",
  },
  itemActive: { backgroundColor: colors.clay, borderColor: colors.ink },
  label: { fontFamily: fonts.bold, fontSize: 11 },
});
