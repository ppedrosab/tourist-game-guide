import raw from "@content/malaga/misterio-manquita.pack.json";
import type { CityPack } from "@/content/types";
import { loadPack } from "../loadPack";
import { missingTranslations } from "../translations";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const pack: CityPack = result.pack;

it("el pack de Málaga está completo en todos sus idiomas", () => {
  expect(pack.languages).toEqual(["es", "en"]);
  expect(missingTranslations(pack)).toEqual([]);
});

it("detecta textos sin traducir e ignora los mapas de audio", () => {
  const copy: CityPack = JSON.parse(JSON.stringify(pack));
  delete (copy.routes[0].nodes[0].title as Record<string, string>).en;
  const missing = missingTranslations(copy);
  expect(missing).toEqual(["routes[0].nodes[0].title (en)"]);
});

it("los retos de observación aceptan respuestas en todos los idiomas", () => {
  // Las respuestas se comparan sin traducir: deben incluir la palabra en cada idioma.
  const answers = pack.routes[0].nodes.flatMap((n) => (n.challenge?.type === "observe" ? [n.challenge.answer] : []));
  expect(answers).toEqual(expect.arrayContaining([expect.arrayContaining(["tiza", "chalk"])]));
  expect(answers).toEqual(expect.arrayContaining([expect.arrayContaining(["derecha", "right"])]));
});
