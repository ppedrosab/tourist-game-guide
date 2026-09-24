import { ReactNode } from "react";
import { ScrollView, StyleProp, StyleSheet, Text, View, ViewStyle } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { colors, type } from "@/theme";
import { IconButton } from "../ui/IconButton";

type ScreenProps = {
  children: ReactNode;
  scroll?: boolean;
  /** Deja hueco para la barra de pestañas flotante. */
  withTabBar?: boolean;
  style?: StyleProp<ViewStyle>;
};

export function Screen({ children, scroll = true, withTabBar = false, style }: ScreenProps) {
  const insets = useSafeAreaInsets();
  const padding = {
    paddingTop: insets.top + 12,
    paddingBottom: (withTabBar ? 110 : 24) + insets.bottom,
    paddingHorizontal: 20,
    gap: 16,
  };
  return (
    <View style={styles.root}>
      {scroll ? (
        <ScrollView contentContainerStyle={[padding, style]} showsVerticalScrollIndicator={false}>
          {children}
        </ScrollView>
      ) : (
        <View style={[{ flex: 1 }, padding, style]}>{children}</View>
      )}
    </View>
  );
}

type TopBarProps = { title: string; onBack?: () => void; right?: ReactNode; closeIcon?: boolean };

export function TopBar({ title, onBack, right, closeIcon = false }: TopBarProps) {
  return (
    <View style={styles.topBar}>
      {onBack ? <IconButton icon={closeIcon ? "close" : "back"} label={closeIcon ? "Cerrar" : "Volver"} onPress={onBack} /> : null}
      <Text style={[type.subtitle, { flex: 1, fontSize: 22 }]} numberOfLines={1}>
        {title}
      </Text>
      {right}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.cream },
  topBar: { flexDirection: "row", alignItems: "center", gap: 12 },
});
