import type { ImageSourcePropType } from "react-native";

/** Capa de fondo generada desde assets/backgrounds/layers. */
export type SceneLayerAsset = {
  /** Orden de dibujo ("0".."4"); "x" es la imagen compuesta de respaldo. */
  order: string;
  /** Papel de la capa en el nombre del archivo: sky, far, mid, sea, near, fx, flat. */
  role: string;
  source: ImageSourcePropType;
};

/** Sprite SVG partido: solo `faces` cambia entre expresiones. */
export type SpriteParts = {
  viewBox: string;
  /** Atributos del <svg> original (stroke-linecap…), sin tamaño ni viewBox. */
  attrs: string;
  shadow: string;
  body: string;
  /** Grupos que van encima de la cara (luz de borde). */
  over: string;
  faces: Record<string, string>;
};
