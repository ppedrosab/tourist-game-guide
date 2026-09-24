import { memo, useMemo } from "react";
import { StyleSheet, View } from "react-native";
import { SvgXml } from "react-native-svg";
import { colors } from "@/theme";
import { SPRITES } from "./assets.generated";
import type { CastShadow } from "./sun";

const wrap = (viewBox: string, attrs: string, inner: string) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" ${attrs}>${inner}</svg>`;

/** Silueta en tinta (para la sombra proyectada): todos los rellenos y trazos a un color. */
const silhouette = (xml: string) =>
  xml
    .replace(/fill="(?!none)[^"]*"/g, `fill="${colors.ink}"`)
    .replace(/stroke="(?!none)[^"]*"/g, `stroke="${colors.ink}"`);

/** Altura de los pies dentro del sprite (centro de la sombra de contacto), 0..1. */
function feetOf(shadowXml: string, viewBoxHeight: number): number {
  const cy = /cy="([\d.]+)"/.exec(shadowXml)?.[1];
  return cy ? Number(cy) / viewBoxHeight : 0.96;
}

type Props = {
  sprite: string;
  expression: string;
  width: number;
  /** Dibujar la sombra de contacto del propio sprite. */
  contactShadow?: boolean;
  /** Sombra proyectada según el sol (ver sun.ts). */
  cast?: CastShadow;
};

/**
 * Personaje SVG en capas apiladas: sombra · cuerpo · cara · luz de borde.
 * Entre expresiones solo cambia la cara, así que al hablar (lip-sync) solo se
 * vuelve a dibujar ese SVG pequeño; el cuerpo se parsea una vez.
 */
export const Sprite = memo(function Sprite({ sprite, expression, width, contactShadow = true, cast }: Props) {
  const parts = SPRITES[sprite];
  const [, , vw, vh] = (parts?.viewBox ?? "0 0 200 260").split(/\s+/).map(Number);
  const height = (width * vh) / vw;
  const layers = useMemo(
    () =>
      parts
        ? {
            shadow: wrap(parts.viewBox, parts.attrs, parts.shadow),
            body: wrap(parts.viewBox, parts.attrs, parts.body),
            over: wrap(parts.viewBox, parts.attrs, parts.over),
            silhouette: wrap(parts.viewBox, parts.attrs, silhouette(parts.body + parts.over)),
          }
        : undefined,
    [parts],
  );
  const face = useMemo(
    () => (parts ? wrap(parts.viewBox, parts.attrs, parts.faces[expression] ?? parts.faces.neutral) : ""),
    [parts, expression],
  );
  if (!parts || !layers) return null;
  const size = { width, height };
  const feet = feetOf(parts.shadow, vh);
  return (
    <View style={size} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
      {cast?.visible ? (
        // Silueta tumbada hacia el fondo desde los pies (el sol queda a espaldas del jugador),
        // acortada por el escorzo del suelo e inclinada según el sol. Sin voltear: con los pies
        // cerca del borde inferior, una sombra hacia delante caería fuera del escenario.
        <View
          style={[
            styles.abs,
            size,
            {
              opacity: cast.opacity,
              transformOrigin: `50% ${feet * 100}%`,
              // skewX negativo: al no voltear, los puntos altos (y < 0) van hacia +skewDeg.
              transform: [{ skewX: `${-cast.skewDeg}deg` }, { scaleY: cast.length * GROUND_SQUASH }],
            },
          ]}
        >
          <SvgXml xml={layers.silhouette} {...size} />
        </View>
      ) : null}
      {contactShadow ? <SvgXml xml={layers.shadow} {...size} style={styles.abs} /> : null}
      <SvgXml xml={layers.body} {...size} style={styles.abs} />
      <SvgXml xml={face} {...size} style={styles.abs} />
      <SvgXml xml={layers.over} {...size} style={styles.abs} />
    </View>
  );
});

/** Escorzo: el suelo se ve inclinado, así que la sombra se acorta en vertical. */
const GROUND_SQUASH = 0.32;

const styles = StyleSheet.create({ abs: { position: "absolute", top: 0, left: 0 } });
