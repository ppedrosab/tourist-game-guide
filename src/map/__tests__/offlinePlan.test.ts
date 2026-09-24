import raw from "@content/malaga/misterio-manquita.pack.json";
import type { CityPack } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { routeMapData } from "../geometry";
import { countTiles, expandBounds, formatBytes, offlinePlan } from "../offlinePlan";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const pack: CityPack = result.pack;

it("la zona de descarga cubre todas las paradas con margen", () => {
  const plan = offlinePlan(pack);
  const [west, south, east, north] = plan.bounds;
  for (const s of routeMapData(pack.routes[0]).stops) {
    expect(s.location.lng).toBeGreaterThan(west);
    expect(s.location.lng).toBeLessThan(east);
    expect(s.location.lat).toBeGreaterThan(south);
    expect(s.location.lat).toBeLessThan(north);
  }
  expect(plan.id).toBe("ciudad-malaga@4");
  expect([plan.minZoom, plan.maxZoom]).toEqual([13, 17]);
});

it("el casco antiguo son unos cientos de teselas y pocos MB", () => {
  const plan = offlinePlan(pack);
  expect(plan.tiles).toBeGreaterThan(50);
  expect(plan.tiles).toBeLessThan(1500);
  expect(plan.approxBytes).toBeLessThan(40_000_000);
});

it("cuenta teselas XYZ: un punto es una tesela por zoom", () => {
  const p = { lat: 36.72, lng: -4.42 };
  expect(countTiles([p, p], 13, 17)).toBe(5);
  // Cada zoom multiplica por ~4 una zona amplia.
  const big = expandBounds([p, p], 2000);
  expect(countTiles(big, 16, 16)).toBeGreaterThan(countTiles(big, 15, 15) * 3);
});

it("el margen es simétrico en metros", () => {
  const [sw, ne] = expandBounds([{ lat: 36.72, lng: -4.42 }, { lat: 36.72, lng: -4.42 }], 150);
  expect((ne.lat - sw.lat) * 111_320).toBeCloseTo(300, 0);
  expect((ne.lng - sw.lng) * 111_320 * Math.cos((36.72 * Math.PI) / 180)).toBeCloseTo(300, 0);
});

it("formatea tamaños en español", () => {
  expect(formatBytes(500)).toBe("1 KB");
  expect(formatBytes(250_000)).toBe("250 KB");
  expect(formatBytes(12_345_678)).toBe("12,3 MB");
});
