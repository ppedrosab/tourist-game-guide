import {
  CHARACTER_DEPTH,
  depthOf,
  INITIAL_TILT,
  layerOffset,
  overscanScale,
  stageAmplitude,
  stepPointer,
  stepTilt,
  TiltState,
  wrapAngle,
} from "../parallax";

const deg = (d: number) => (d * Math.PI) / 180;
/** Simula `ms` milisegundos a 60 Hz con una postura fija. */
function hold(s: TiltState, roll: number, pitch: number, ms: number, hz = 60): TiltState {
  const dt = 1000 / hz;
  for (let t = 0; t < ms; t += dt) s = stepTilt(s, roll, pitch, dt);
  return s;
}

describe("profundidades", () => {
  it("siguen los factores del diseño y fx es fija", () => {
    expect([depthOf("sky"), depthOf("far"), depthOf("mid"), depthOf("sea"), depthOf("near")]).toEqual([
      0, 0.1, 0.25, 0.25, 0.6,
    ]);
    expect(depthOf("fx")).toBeNull();
    expect(depthOf("desconocida")).toBe(0.25);
    expect(CHARACTER_DEPTH).toBe(depthOf("near"));
  });
});

describe("garantía de bordes", () => {
  it("con cualquier inclinación ninguna capa descubre el borde del escenario", () => {
    for (const [w, h] of [
      [390, 560],
      [320, 460],
      [430, 617],
      [768, 1103],
    ]) {
      const maxDepth = 0.6;
      const scale = overscanScale(w, h, maxDepth);
      const { ax, ay } = stageAmplitude(w, h);
      const marginX = ((scale - 1) * w) / 2;
      const marginY = ((scale - 1) * h) / 2;
      // Inclinaciones extremas y aleatorias, más la saturación teórica ±1.
      const tilts = [[1, 1], [-1, -1], [1, -1], ...Array.from({ length: 200 }, () => [Math.random() * 2 - 1, Math.random() * 2 - 1])];
      for (const [x, y] of tilts) {
        for (const depth of [0, 0.1, 0.25, 0.6]) {
          const { tx, ty } = layerOffset(x, y, depth, ax, ay);
          expect(Math.abs(tx)).toBeLessThanOrEqual(marginX - 1 + 1e-9);
          expect(Math.abs(ty)).toBeLessThanOrEqual(marginY - 1 + 1e-9);
        }
      }
      // La ampliación es discreta (< 9 %) e igual en cualquier pantalla.
      expect(scale).toBeLessThan(1.09);
      expect(scale).toBeGreaterThan(1.07);
    }
  });

  it("stepTilt nunca sale de (-1, 1) aunque el giro sea enorme", () => {
    let s = hold(INITIAL_TILT, 0, 0, 100);
    for (const r of [deg(89), deg(-179), deg(179), deg(720)]) {
      s = hold(s, r, -r, 500);
      expect(Math.abs(s.x)).toBeLessThan(1);
      expect(Math.abs(s.y)).toBeLessThan(1);
    }
  });
});

describe("respuesta al giro", () => {
  it("la primera lectura fija el centro: empezar inclinado no desplaza la escena", () => {
    const s = hold(INITIAL_TILT, deg(35), deg(-20), 300);
    expect(Math.abs(s.x)).toBeLessThan(0.02);
    expect(Math.abs(s.y)).toBeLessThan(0.02);
  });

  it("un giro responde enseguida y suave, sin pasarse", () => {
    let s = hold(INITIAL_TILT, 0, 0, 100);
    const xs: number[] = [];
    for (let i = 0; i < 30; i++) {
      s = stepTilt(s, deg(12), 0, 1000 / 60);
      xs.push(s.x);
    }
    // Subida monótona (sin rebotes) durante la respuesta y cerca del objetivo en medio segundo.
    // Después el recentrado la hace bajar muy despacio, a propósito.
    for (let i = 1; i < 15; i++) expect(xs[i]).toBeGreaterThan(xs[i - 1]);
    expect(xs[5]).toBeGreaterThan(0.2);
    expect(xs[29]).toBeGreaterThan(0.5);
    expect(xs[29]).toBeLessThan(Math.tanh(12 / 18) + 1e-6);
  });

  it("mantener una postura nueva vuelve poco a poco al centro", () => {
    let s = hold(INITIAL_TILT, 0, 0, 100);
    s = hold(s, deg(15), 0, 400);
    const peak = s.x;
    s = hold(s, deg(15), 0, 8000);
    expect(peak).toBeGreaterThan(0.4);
    expect(s.x).toBeLessThan(0.1);
  });

  it("es igual de fluido a 60 y a 120 Hz", () => {
    const base60 = hold(INITIAL_TILT, 0, 0, 100, 60);
    const base120 = hold(INITIAL_TILT, 0, 0, 100, 120);
    const a = hold(base60, deg(10), deg(5), 250, 60);
    const b = hold(base120, deg(10), deg(5), 250, 120);
    expect(Math.abs(a.x - b.x)).toBeLessThan(0.03);
    expect(Math.abs(a.y - b.y)).toBeLessThan(0.03);
  });

  it("no salta al cruzar ±180° ni tras una pausa larga", () => {
    let s = hold(INITIAL_TILT, deg(179), 0, 100);
    s = stepTilt(s, deg(-179), 0, 16); // +2° reales, no -358°
    expect(s.x).toBeGreaterThan(0);
    expect(s.x).toBeLessThan(0.05);
    const before = s.x;
    s = stepTilt(s, deg(-170), 0, 5000); // la app vuelve del segundo plano
    expect(s.x - before).toBeLessThan(0.6);
  });

  it("ignora lecturas no válidas", () => {
    const s = hold(INITIAL_TILT, 0, 0, 100);
    expect(stepTilt(s, NaN, 0, 16)).toBe(s);
  });
});

describe("puntero (web)", () => {
  it("sigue al puntero suavizado y acotado", () => {
    let s = INITIAL_TILT;
    for (let i = 0; i < 120; i++) s = stepPointer(s, 3, -0.5, 16);
    expect(s.x).toBeCloseTo(1, 3);
    expect(s.y).toBeCloseTo(-0.5, 3);
  });
});

describe("utilidades", () => {
  it("wrapAngle deja el ángulo en [-π, π)", () => {
    expect(wrapAngle(deg(190))).toBeCloseTo(deg(-170));
    expect(wrapAngle(deg(-190))).toBeCloseTo(deg(170));
    expect(wrapAngle(0)).toBe(0);
  });

  it("las capas cercanas se mueven más y en sentido contrario", () => {
    const { ax, ay } = stageAmplitude(390, 560);
    expect(ax).toBeCloseTo(25.74);
    const far = layerOffset(1, 0, 0.1, ax, ay);
    const near = layerOffset(1, 0, 0.6, ax, ay);
    expect(near.tx).toBeLessThan(far.tx);
    expect(near.tx).toBeCloseTo(-ax * 0.6);
    expect(layerOffset(0.5, 0.5, 0, ax, ay).tx).toBeCloseTo(0);
  });
});
