#!/usr/bin/env node
/**
 * Genera src/scene/assets.generated.ts a partir de assets/:
 *  - Capas de fondo: assets/backgrounds/layers/bg_{escena}_{n}_{capa}@2x|@3x.webp
 *    (Metro elige @2x/@3x solo; `require` apunta al nombre sin escala).
 *  - Audios: assets/audio/**.mp3|m4a|aac|wav, con la ruta relativa a assets/ como
 *    clave (la misma que usa el pack: "audio/es/n1_a.mp3").
 *  - Coleccionables: assets/collectibles/*.svg, con la ruta que usa el pack como
 *    clave ("collectibles/cenacho.svg") y el SVG completo como texto.
 *  - Sprites: assets/sprites/{personaje}/{personaje}_{expresion}.svg, partidos en
 *    sombra · cuerpo · cara · luz de borde. Entre expresiones solo cambia `face`,
 *    así que la cara se guarda aparte y el resto una sola vez.
 *
 * Uso: npm run gen:assets (y commitear el resultado). Metro necesita `require`
 * estáticos, por eso el manifiesto se genera en vez de construirse en ejecución.
 */
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const layersDir = join(root, "assets/backgrounds/layers");
const spritesDir = join(root, "assets/sprites");
const out = join(root, "src/scene/assets.generated.ts");

// ---------------------------------------------------------------------------
// Capas
// ---------------------------------------------------------------------------
const layerRe = /^bg_(.+)_(\d|x)_([a-z]+)@[23]x\.webp$/;
const scenes = new Map();
for (const file of readdirSync(layersDir).sort()) {
  const m = layerRe.exec(file);
  if (!m) throw new Error(`Nombre de capa inesperado: ${file}`);
  const [, scene, order, role] = m;
  const base = file.replace(/@[23]x\.webp$/, ".webp");
  const layers = scenes.get(scene) ?? new Map();
  layers.set(base, { order, role, path: `../../assets/backgrounds/layers/${base}` });
  scenes.set(scene, layers);
}

// ---------------------------------------------------------------------------
// Sprites
// ---------------------------------------------------------------------------
/** Extrae los <g id="…"> de primer nivel respetando el anidamiento. */
function topLevelGroups(body) {
  const groups = [];
  const tag = /<g\b[^>]*>|<\/g>/g;
  let depth = 0;
  let start = -1;
  let id = "";
  for (let m; (m = tag.exec(body)); ) {
    if (m[0].startsWith("</")) {
      depth--;
      if (depth === 0) groups.push({ id, xml: body.slice(start, tag.lastIndex) });
    } else {
      if (depth === 0) {
        start = m.index;
        id = /id="([^"]+)"/.exec(m[0])?.[1] ?? "";
      }
      depth++;
    }
  }
  return groups;
}

const sprites = {};
for (const character of readdirSync(spritesDir).sort()) {
  const files = readdirSync(join(spritesDir, character)).filter((f) => f.endsWith(".svg")).sort();
  const faces = {};
  let parts;
  for (const file of files) {
    const expression = file.slice(character.length + 1, -4);
    const svg = readFileSync(join(spritesDir, character, file), "utf8");
    const open = /<svg\b[^>]*>/.exec(svg)[0];
    const viewBox = /viewBox="([^"]+)"/.exec(open)[1];
    const attrs = open
      .replace(/^<svg\b/, "")
      .replace(/>$/, "")
      .replace(/\s(width|height|viewBox|role|aria-label)="[^"]*"/g, "")
      .trim();
    const body = svg.slice(svg.indexOf(open) + open.length, svg.lastIndexOf("</svg>"));
    const groups = topLevelGroups(body);
    const face = groups.find((g) => g.id === "face");
    if (!face) throw new Error(`${file}: falta el grupo "face"`);
    faces[expression] = face.xml;
    if (!parts) {
      const faceIndex = groups.indexOf(face);
      parts = {
        viewBox,
        attrs,
        shadow: groups.filter((g) => g.id === "shadow").map((g) => g.xml).join(""),
        body: groups.slice(0, faceIndex).filter((g) => g.id !== "shadow").map((g) => g.xml).join(""),
        over: groups.slice(faceIndex + 1).map((g) => g.xml).join(""),
      };
    }
  }
  sprites[character] = { ...parts, faces };
}

// ---------------------------------------------------------------------------
// Audios
// ---------------------------------------------------------------------------
const audioDir = join(root, "assets/audio");
const audios = [];
function walk(dir, rel) {
  for (const name of readdirSync(dir).sort()) {
    const full = join(dir, name);
    const r = `${rel}/${name}`;
    if (statSync(full).isDirectory()) walk(full, r);
    else if (/\.(mp3|m4a|aac|wav)$/i.test(name)) audios.push(r);
  }
}
if (existsSync(audioDir)) walk(audioDir, "audio");

// ---------------------------------------------------------------------------
// Coleccionables
// ---------------------------------------------------------------------------
const collectiblesDir = join(root, "assets/collectibles");
const collectibles = {};
if (existsSync(collectiblesDir)) {
  for (const file of readdirSync(collectiblesDir).filter((f) => f.endsWith(".svg")).sort()) {
    // role/aria-label fuera: la accesibilidad la da el contenedor (en web SvgXml los pasa mal al DOM).
    collectibles[`collectibles/${file}`] = readFileSync(join(collectiblesDir, file), "utf8")
      .replace(/\s(role|aria-label)="[^"]*"/g, "")
      .trim();
  }
}

// ---------------------------------------------------------------------------
// Salida
// ---------------------------------------------------------------------------
const lines = [
  "/* eslint-disable */",
  "// ARCHIVO GENERADO por scripts/gen-scene-assets.mjs. No editar a mano: npm run gen:assets",
  'import type { SpriteParts, SceneLayerAsset } from "./types";',
  "",
  "export const SCENE_LAYERS: Record<string, SceneLayerAsset[]> = {",
];
for (const [scene, layers] of scenes) {
  lines.push(`  ${JSON.stringify(scene)}: [`);
  for (const { order, role, path } of layers.values()) {
    lines.push(`    { order: ${JSON.stringify(order)}, role: ${JSON.stringify(role)}, source: require(${JSON.stringify(path)}) },`);
  }
  lines.push("  ],");
}
lines.push("};", "");
lines.push("/** Audios disponibles, por la ruta que usa el pack. Vacío hasta que se graben las voces. */");
lines.push("export const AUDIO: Record<string, number> = {");
for (const a of audios) lines.push(`  ${JSON.stringify(a)}: require(${JSON.stringify(`../../assets/${a}`)}),`);
lines.push("};");
lines.push("", "/** Arte de los coleccionables (SVG completo), por la ruta que usa el pack en `icon`. */");
lines.push(`export const COLLECTIBLE_ART: Record<string, string> = ${JSON.stringify(collectibles, null, 2)};`);
lines.push("", `export const SPRITES: Record<string, SpriteParts> = ${JSON.stringify(sprites, null, 2)};`, "");
writeFileSync(out, lines.join("\n"));
console.log(`OK: ${scenes.size} escenas, ${audios.length} audios, ${Object.keys(collectibles).length} coleccionables, ${Object.keys(sprites).length} personajes → ${out}`);
