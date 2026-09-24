import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "../loadPack";
import { getNode } from "../runner";
import { buildSteps, checkObserveAnswer, normalizeAnswer } from "../scene";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];
const kinds = (nodeId: string, flags: string[] = []) => buildSteps(getNode(route, nodeId), flags).map((s) => s.kind);

describe("buildSteps", () => {
  it("omite los bloques scene y termina en seguir", () => {
    expect(kinds("n1_cenachero")).toEqual(["text", "text", "text", "continue"]);
  });

  it("pone reto antes de la decisión", () => {
    expect(kinds("n2_larios")).toEqual(["text", "text", "text", "challenge", "decision"]);
  });

  it("añade la pista tras el reto", () => {
    expect(kinds("a1_atarazanas")).toEqual(["text", "text", "text", "text", "challenge", "clue", "continue"]);
  });

  it("resuelve variantes con los flags y salta las que no encajan", () => {
    const withFlag = buildSteps(getNode(route, "n4_manquita"), ["camino_poder"]);
    expect(withFlag.filter((s) => s.kind === "text")).toHaveLength(3);
    expect(kinds("n4_manquita")).toEqual(["text", "text", "challenge", "decision"]);
  });

  it("el nodo final acaba en ending", () => {
    expect(kinds("n7_final", ["camino_dinero", "version_america"])).toEqual(["text", "text", "ending"]);
  });

  it("copia la pista de siguiente parada", () => {
    const steps = buildSteps(getNode(route, "a2_casa_guardia"), []);
    const last = steps[steps.length - 1];
    expect(last.kind === "continue" && last.hint?.es).toMatch(/Manquita/);
  });
});

describe("respuestas de observación", () => {
  it("normaliza tildes, mayúsculas y signos", () => {
    expect(normalizeAnswer("  ¡La DERECHA!  ")).toBe("la derecha");
    expect(normalizeAnswer("Tíza")).toBe("tiza");
  });

  it("acepta coincidencias exactas y como palabra", () => {
    const tiza = ["tiza", "con tiza", "chalk"];
    expect(checkObserveAnswer(tiza, "Con TIZA")).toBe(true);
    expect(checkObserveAnswer(tiza, "creo que con tiza blanca")).toBe(true);
    expect(checkObserveAnswer(tiza, "con boli")).toBe(false);
    expect(checkObserveAnswer(tiza, "tizana")).toBe(false);
    expect(checkObserveAnswer(tiza, "")).toBe(false);
  });
});
