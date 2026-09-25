import { estimateSpeechMs, mouthPhaseMs, pickVoice, speakerPitch } from "../voice";

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

describe("voz del sistema por género", () => {
  const voices = [
    { identifier: "a", name: "Mónica", language: "es-ES" },
    { identifier: "b", name: "Jorge", language: "es-ES", quality: "Enhanced" },
    { identifier: "c", name: "Paulina", language: "es-MX" },
    { identifier: "d", name: "Google UK English Female", language: "en-GB" },
    { identifier: "e", name: "Daniel", language: "en_GB" },
  ];
  it("prefiere la del país y del género pedido", () => {
    expect(pickVoice(voices, "es-ES", "f")?.identifier).toBe("a");
    expect(pickVoice(voices, "es-ES", "m")?.identifier).toBe("b");
    expect(pickVoice(voices, "en-GB", "f")?.identifier).toBe("d");
    expect(pickVoice(voices, "en-GB", "m")?.identifier).toBe("e");
  });
  it("sin voz de ese género no elige ninguna", () => {
    expect(pickVoice([{ identifier: "x", name: "Google español", language: "es-ES" }], "es-ES", "f")).toBeUndefined();
  });
  it("el tono va con el género", () => {
    expect(speakerPitch("norica", { gender: "f" })).toBeGreaterThan(1);
    expect(speakerPitch("cenachero", { gender: "m" })).toBeLessThan(1);
    expect(speakerPitch("x", { gender: "m", pitch: 1.3 })).toBe(1.3);
  });
});
