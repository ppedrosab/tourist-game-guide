/**
 * Sistema de diseño "Azulejo y sal" v2.
 * Todos los valores salen del storyboard (tablero 00 · Sistema de diseño).
 */
export const colors = {
  ink: "#1B2A3A",
  clay: "#A8431F",
  clayDark: "#7E3015",
  sea: "#2F6F73",
  peach: "#F0A27F",
  gold: "#F2C14E",
  paper: "#FFF8EC",
  cream: "#F6EFE3",
  sand: "#EADFCB",
  line: "#C9BBA2",
  muted: "#5A6470",
  white: "#FFFFFF",
  seaTint: "#DCEBE6",
  clayTint: "#F6E3D6",
  /** Morado del Carnaval de Cádiz: seña de las rutas de fiestas. */
  violet: "#6E2C5E",
} as const;

/** Color de cada camino de la historia: se repite en mapa, decisiones, pistas y HUD. */
export const branchColors = {
  dinero: colors.sea,
  poder: colors.clay,
  comun: colors.ink,
} as const;
export type Branch = keyof typeof branchColors;

export const radius = { sm: 9, md: 14, lg: 16, xl: 22 } as const;
export const border = { thin: 2, base: 2.5, thick: 3 } as const;
/** Sombra dura (desplazamiento vertical, sin desenfoque). */
export const hardShadow = { sm: 3, md: 4 } as const;
export const space = { xs: 4, sm: 8, md: 12, lg: 16, xl: 20, xxl: 28 } as const;
export const size = { button: 54, buttonSmall: 46, iconButton: 46, chip: 28 } as const;
