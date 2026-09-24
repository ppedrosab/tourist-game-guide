import raw from "@content/malaga/misterio-manquita.pack.json";
import type { CityPack } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { COLLECTIBLE_ART } from "../assets.generated";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const pack: CityPack = result.pack;

it("cada coleccionable del pack tiene su arte", () => {
  const icons = pack.routes.flatMap((r) => (r.rewards ?? []).map((c) => c.icon));
  expect(icons).toHaveLength(6);
  for (const icon of icons) expect([icon, COLLECTIBLE_ART[icon] !== undefined]).toEqual([icon, true]);
});

it("los SVG son autónomos y con ids de recorte únicos", () => {
  const ids = Object.values(COLLECTIBLE_ART).map((xml) => {
    expect(xml.startsWith("<svg")).toBe(true);
    expect(xml).toContain('viewBox="0 0 120 124"');
    expect(xml).not.toMatch(/<image|href="http/); // sin recursos externos
    return /clipPath id="([^"]+)"/.exec(xml)?.[1];
  });
  expect(new Set(ids).size).toBe(ids.length);
});
