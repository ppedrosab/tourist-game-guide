import { castShadow, isDark, nextDusk, sunPosition } from "../sun";

// Plaza de la Marina, Málaga.
const LAT = 36.7188;
const LNG = -4.4196;

describe("posición del sol en Málaga", () => {
  it("solsticio de verano a mediodía solar: muy alto y al sur", () => {
    // Mediodía solar ≈ 12:18 UTC en Málaga (longitud −4,4°).
    const s = sunPosition(new Date("2026-06-21T12:18:00Z"), LAT, LNG);
    expect(s.elevation).toBeGreaterThan(75.5);
    expect(s.elevation).toBeLessThan(77.5); // 90 − 36,7 + 23,4 ≈ 76,7
    expect(s.azimuth).toBeGreaterThan(170);
    expect(s.azimuth).toBeLessThan(190);
  });

  it("solsticio de invierno a mediodía solar: bajo", () => {
    const s = sunPosition(new Date("2026-12-21T12:15:00Z"), LAT, LNG);
    expect(s.elevation).toBeGreaterThan(28.8);
    expect(s.elevation).toBeLessThan(30.8); // 90 − 36,7 − 23,4 ≈ 29,8
  });

  it("mañana al este, tarde al oeste y noche bajo el horizonte", () => {
    const manana = sunPosition(new Date("2026-09-24T08:30:00Z"), LAT, LNG);
    const tarde = sunPosition(new Date("2026-09-24T16:30:00Z"), LAT, LNG);
    const noche = sunPosition(new Date("2026-09-24T23:00:00Z"), LAT, LNG);
    expect(manana.azimuth).toBeGreaterThan(90);
    expect(manana.azimuth).toBeLessThan(135);
    expect(tarde.azimuth).toBeGreaterThan(225);
    expect(tarde.azimuth).toBeLessThan(270);
    expect(noche.elevation).toBeLessThan(0);
  });
});

describe("sombra proyectada", () => {
  it("cae al lado contrario del sol y se alarga cuando está bajo", () => {
    const manana = castShadow({ elevation: 20, azimuth: 100 });
    const tarde = castShadow({ elevation: 20, azimuth: 260 });
    const mediodia = castShadow({ elevation: 75, azimuth: 180 });
    expect(manana.skewDeg).toBeLessThan(-25); // sol al este → sombra a la izquierda
    expect(tarde.skewDeg).toBeGreaterThan(25);
    expect(Math.abs(mediodia.skewDeg)).toBeLessThan(1);
    expect(manana.length).toBeGreaterThan(mediodia.length * 4);
    expect(mediodia.length).toBeCloseTo(1 / Math.tan((75 * Math.PI) / 180));
  });

  it("está acotada y de noche desaparece", () => {
    const rasante = castShadow({ elevation: 3, azimuth: 90 });
    expect(rasante.length).toBe(1.4);
    expect(Math.abs(rasante.skewDeg)).toBeLessThanOrEqual(35);
    expect(castShadow({ elevation: -10, azimuth: 0 }).visible).toBe(false);
  });
});

describe("anochecer", () => {
  const [lat, lng] = [36.7213, -4.4214];
  it("a mediodía es de día y a medianoche de noche", () => {
    expect(isDark(new Date("2026-06-21T12:00:00Z"), lat, lng)).toBe(false);
    expect(isDark(new Date("2026-06-21T23:30:00Z"), lat, lng)).toBe(true);
  });
  it("en junio anochece en Málaga entre la puesta de sol (21:43) y el fin del crepúsculo civil (22:13)", () => {
    const dusk = nextDusk(new Date("2026-06-21T12:00:00Z"), lat, lng)!.getTime();
    expect(dusk).toBeGreaterThan(Date.parse("2026-06-21T19:43:00Z"));
    expect(dusk).toBeLessThan(Date.parse("2026-06-21T20:13:00Z"));
  });
});
