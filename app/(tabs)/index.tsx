import { router } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Screen } from "@/components/layout/Screen";
import { Button3D, Chip, HardShadow, Icon } from "@/components/ui";
import { border, colors, fonts, radius, type } from "@/theme";

const CITIES = [
  { id: "malaga", name: "Málaga", status: "1 ruta gratis", available: true },
  { id: "sevilla", name: "Sevilla", status: "Pronto", available: false },
  { id: "granada", name: "Granada", status: "Pronto", available: false },
];

export default function Explorar() {
  return (
    <Screen withTabBar>
      <View style={styles.header}>
        <View style={{ flex: 1 }}>
          <Text style={type.secondary}>Hola,</Text>
          <Text style={type.title}>detective</Text>
        </View>
        <Chip label="3 pistas" icon="book" />
      </View>

      {/* Continuar: lleva a la parada exacta donde se quedó el jugador (fase 2: desde el progreso guardado). */}
      <HardShadow radius={radius.xl}>
        <View style={styles.continueCard}>
          <Chip label="En curso" variant="clay" />
          <Text style={[type.subtitle, { color: colors.white }]}>El misterio de la Manquita</Text>
          <View style={styles.progressRow}>
            <View style={styles.progressTrack}>
              <View style={[styles.progressFill, { width: "25%" }]} />
            </View>
            <Text style={styles.progressText}>Parada 2 de 8</Text>
          </View>
          <Button3D label="Continuar" icon="play" onPress={() => router.push("/ruta/misterio-manquita/jugar")} />
        </View>
      </HardShadow>

      <View style={styles.sectionHeader}>
        <Text style={type.subtitle}>Ciudades</Text>
        <Text style={type.caption}>1 de 4 disponibles</Text>
      </View>
      <View style={{ gap: 12 }}>
        {CITIES.map((city) => (
          <Pressable
            key={city.id}
            disabled={!city.available}
            onPress={() => router.push(`/ciudad/${city.id}`)}
            accessibilityRole="button"
            accessibilityState={{ disabled: !city.available }}
          >
            <View style={[styles.cityRow, !city.available && { opacity: 0.6 }]}>
              <Text style={[type.label, { flex: 1, fontSize: 17 }]}>{city.name}</Text>
              <Text style={[type.caption, city.available && { color: colors.clay, fontFamily: fonts.bold }]}>
                {city.status}
              </Text>
              <Icon name={city.available ? "next" : "lock"} size={18} />
            </View>
          </Pressable>
        ))}
      </View>
      <Button3D label="Ver bienvenida (demo)" variant="ghost" onPress={() => router.push("/bienvenida")} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { flexDirection: "row", alignItems: "center", gap: 12 },
  continueCard: {
    gap: 10,
    padding: 16,
    borderRadius: radius.xl,
    borderWidth: border.base,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  progressRow: { flexDirection: "row", alignItems: "center", gap: 10 },
  progressTrack: { flex: 1, height: 6, borderRadius: 3, backgroundColor: "#3C4B5B" },
  progressFill: { height: 6, borderRadius: 3, backgroundColor: colors.peach },
  progressText: { fontFamily: fonts.medium, fontSize: 12, color: "#C9D1D9" },
  sectionHeader: { flexDirection: "row", alignItems: "baseline", justifyContent: "space-between" },
  cityRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    padding: 16,
    borderRadius: radius.lg,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
  },
});
