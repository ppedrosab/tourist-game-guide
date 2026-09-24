import raw from "@content/malaga/misterio-manquita.pack.json";
import type { CityPack } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { THEN_NOW_ART } from "../assets.generated";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const pack: CityPack = result.pack;

it("cada 'antes y ahora' del pack tiene su ilustración de época y un 'ahora' válido", () => {
  const blocks = pack.routes.flatMap((r) => r.nodes.flatMap((n) => n.content)).filter((b) => b.type === "then_now");
  expect(blocks.length).toBeGreaterThan(0);
  for (const b of blocks) {
    if (b.type !== "then_now") continue;
    expect([b.then, THEN_NOW_ART[b.then] !== undefined]).toEqual([b.then, true]);
    expect(b.now).toBe("camera");
  }
});

it("las ilustraciones de época son SVG autónomos con la proporción de las escenas", () => {
  for (const xml of Object.values(THEN_NOW_ART)) {
    expect(xml).toContain('viewBox="0 0 390 560"');
    expect(xml).not.toMatch(/<image|href="http/);
  }
});
