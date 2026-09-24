import raw from "@content/malaga/misterio-manquita.pack.json";
import type { CityPack, Route } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { getNode } from "@/engine/runner";
import { buildSteps } from "@/engine/scene";
import { SPRITES } from "../assets.generated";
import { spriteKeyOf, stageCast } from "../cast";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const pack: CityPack = result.pack;
const route: Route = pack.routes[0];
const castAt = (nodeId: string, stepIndex: number, flags: string[] = []) => {
  const node = getNode(route, nodeId);
  const step = buildSteps(route, node, flags)[stepIndex];
  return stageCast(pack, route, node, step).map((c) => `${c.position}:${c.characterId}:${c.expression}${c.speaking ? "*" : ""}`);
};

it("todos los personajes del pack tienen sprite con las 8 expresiones", () => {
  for (const c of pack.characters) {
    const key = spriteKeyOf(c.avatar);
    expect(key && SPRITES[key]).toBeTruthy();
    expect(Object.keys(SPRITES[key!].faces).sort()).toEqual(
      ["dramatic", "happy", "nervous", "neutral", "proud", "surprised", "talking", "thinking"],
    );
  }
  expect(spriteKeyOf("sprites/manquita/manquita_neutral.svg")).toBe("manquita");
  expect(spriteKeyOf("img/otra.png")).toBeUndefined();
});

it("usa el reparto del bloque scene y marca a quien habla con su expresión", () => {
  // n1: Cenachero a la izquierda; primer diálogo sin expresión → conserva "happy" del bloque scene.
  expect(castAt("n1_cenachero", 0)).toEqual(["left:cenachero:happy*"]);
  // Segundo diálogo con expresión "thinking".
  expect(castAt("n1_cenachero", 1)).toEqual(["left:cenachero:thinking*"]);
  // Anécdota: nadie habla.
  expect(castAt("n1_cenachero", 2)).toEqual(["left:cenachero:happy"]);
});

it("sin bloque scene pone al guía a la izquierda", () => {
  expect(castAt("n2_larios", 0)).toEqual(["left:cenachero:neutral"]); // antes y ahora
  expect(castAt("n2_larios", 1)).toEqual(["left:cenachero:talking*"]);
});

it("quien habla y no está en escena ocupa el hueco libre", () => {
  // La Manquita habla en su nodo; el bloque scene solo trae al Cenachero.
  expect(castAt("n4_manquita", 0, ["camino_poder"])).toEqual(["left:cenachero:nervous", "right:la_manquita:proud*"]);
});

it("respeta a dos personajes del bloque scene", () => {
  expect(castAt("n5_teatro", 0)).toEqual(["left:cenachero:surprised", "right:lucio:dramatic*"]);
  expect(castAt("n5_teatro", 2)).toEqual(["left:cenachero:happy*", "right:lucio:dramatic"]);
});

it("en la decisión y al seguir habla el guía", () => {
  const steps = buildSteps(route, getNode(route, "n2_larios"), []);
  expect(castAt("n2_larios", steps.length - 1)).toEqual(["left:cenachero:thinking*"]);
  const a2 = buildSteps(route, getNode(route, "a2_casa_guardia"), []);
  expect(castAt("a2_casa_guardia", a2.length - 1)).toEqual(["left:cenachero:happy*"]);
});
