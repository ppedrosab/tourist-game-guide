import type { Route } from "@/content/types";
import { hoursAt, localParts, parseHours } from "../hours";
import { legTo, routePractical } from "../practical";

// 2026-07-15 es miércoles. Madrid en verano = UTC+2.
const at = (iso: string) => new Date(iso);

describe("horarios", () => {
  it("entiende las formas que guarda gen_practical", () => {
    for (const h of [
      "24/7",
      "Tu-Su 10:00-20:00; Mo off",
      "Apr-Oct 09:00-20:00; Nov-Mar 09:00-18:00",
      "Mo,Tu,Th 11:00-20:00; Fr-Su 11:00-21:00",
      "Mo-Sa 10:00-14:00,17:00-20:00; PH off",
      "Mo-Su 18:00-00:00",
    ])
      expect([h, parseHours(h) !== null]).toEqual([h, true]);
    expect(parseHours("sunrise-sunset")).toBeNull();
    expect(parseHours("Mo-Fr 9-14")).toBeNull();
  });

  it("hora local en la zona de la ciudad", () => {
    expect(localParts(at("2026-07-15T08:30:00Z"), "Europe/Madrid")).toEqual({ day: 2, month: 6, minute: 10 * 60 + 30 });
    // pasada la medianoche en Madrid ya es jueves
    expect(localParts(at("2026-07-15T22:30:00Z"), "Europe/Madrid").day).toBe(3);
  });

  it("abierto, cerrado y a qué hora abre o cierra", () => {
    const tz = "Europe/Madrid";
    expect(hoursAt("Tu-Su 10:00-20:00; Mo off", at("2026-07-15T10:00:00Z"), tz)).toEqual({
      open: true,
      closesAt: "20:00",
      allDay: false,
    });
    expect(hoursAt("Tu-Su 10:00-20:00; Mo off", at("2026-07-15T06:00:00Z"), tz)).toEqual({ open: false, opensAt: "10:00" });
    // 2026-07-13 es lunes
    expect(hoursAt("Tu-Su 10:00-20:00; Mo off", at("2026-07-13T10:00:00Z"), tz)).toEqual({ open: false, opensAt: undefined });
    expect(hoursAt("Mo-Sa 10:00-14:00,17:00-20:00", at("2026-07-15T13:00:00Z"), tz)).toEqual({ open: false, opensAt: "17:00" });
    expect(hoursAt("24/7", at("2026-07-15T13:00:00Z"), tz)).toMatchObject({ open: true, allDay: true });
  });

  it("horario de verano e invierno por meses", () => {
    const spec = "Apr-Oct 09:00-20:00; Nov-Mar 09:00-18:00";
    expect(hoursAt(spec, at("2026-07-15T17:00:00Z"), "Europe/Madrid")).toMatchObject({ open: true, closesAt: "20:00" });
    // 15 de enero, 18:30 en Madrid (UTC+1)
    expect(hoursAt(spec, at("2026-01-15T17:30:00Z"), "Europe/Madrid")).toEqual({ open: false, opensAt: undefined });
  });

  it("las franjas que pasan de medianoche siguen abiertas de madrugada", () => {
    // jueves 01:00 en Madrid: abierto desde el miércoles hasta las 02:00
    expect(hoursAt("Mo-Su 20:00-02:00", at("2026-07-15T23:00:00Z"), "Europe/Madrid")).toMatchObject({
      open: true,
      closesAt: "02:00",
    });
  });
});

describe("resumen práctico de la ruta", () => {
  const route = {
    practical: {
      stops: { a: { water: 50 }, b: {}, c: { water: 120, shade: true }, d: {} },
      legs: {
        "a->b": { up: 10, down: 0, grade: 4 },
        "a->c": { up: 30, down: 5, grade: 9, steps: 1 },
        "b->d": { up: 5, down: 2, grade: 3 },
        "c->d": { up: 0, down: 20, grade: 5 },
      },
    },
  } as unknown as Route;

  it("suma el camino más exigente, no todas las ramas", () => {
    expect(routePractical(route)).toEqual({
      up: 30,
      down: 25,
      grade: 9,
      stepLegs: 1,
      waterStops: 2,
      stops: 4,
      stepFree: false,
      gentle: false,
    });
  });

  it("el tramo hacia una parada sale de la última visitada", () => {
    expect(legTo(route, { visitedNodeIds: ["a", "x", "c"] }, "d")).toEqual({ up: 0, down: 20, grade: 5 });
    expect(legTo(route, { visitedNodeIds: [] }, "a")).toBeUndefined();
  });

  it("sin datos no hay resumen", () => {
    expect(routePractical({} as Route)).toBeNull();
  });
});
