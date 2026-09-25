import { estimateSpeechMs, mouthPhaseMs, speakerPitch } from "../voice";

it("estima la duración con ritmo de narración y límites", () => {
  expect(estimateSpeechMs("Hola")).toBe(1200);
  const frase = "Esta calle la pagó la Casa Larios pa' unir el centro con el puerto.";
  const ms = estimateSpeechMs(frase);
  expect(ms).toBeGreaterThan(4500);
  expect(ms).toBeLessThan(6500);
  expect(estimateSpeechMs("palabra ".repeat(500))).toBe(25000);
});

it("el ritmo de boca varía pero se mantiene en rangos naturales", () => {
  const phases = Array.from({ length: 40 }, (_, i) => mouthPhaseMs(7, i));
  expect(new Set(phases.map(Math.round)).size).toBeGreaterThan(20);
  phases.forEach((ms, i) => {
    if (i % 2 === 0) expect(ms).toBeGreaterThanOrEqual(90), expect(ms).toBeLessThanOrEqual(170);
    else expect(ms).toBeGreaterThanOrEqual(70), expect(ms).toBeLessThanOrEqual(130);
  });
  expect(mouthPhaseMs(7, 3)).toBe(mouthPhaseMs(7, 3));
});

describe("tono de la voz sintética", () => {
  it("es estable por personaje y está entre 0,85 y 1,2", () => {
    expect(speakerPitch("cenachero")).toBe(speakerPitch("cenachero"));
    for (const id of ["cenachero", "norica", "irving", "lagarto", "abderraman"]) {
      expect(speakerPitch(id)).toBeGreaterThanOrEqual(0.85);
      expect(speakerPitch(id)).toBeLessThanOrEqual(1.2);
    }
    expect(speakerPitch(undefined)).toBe(1);
  });
});
