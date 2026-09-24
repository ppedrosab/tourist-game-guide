import { en } from "../en";
import { es } from "../es";
import { translate } from "../index";

const keys = (o: object, p = ""): string[] =>
  Object.entries(o).flatMap(([k, v]) => (typeof v === "string" ? [`${p}${k}`] : keys(v, `${p}${k}.`)));
const params = (s: string) => (s.match(/\{\w+\}/g) ?? []).sort().join(",");

it("inglés y español tienen las mismas claves y los mismos parámetros", () => {
  expect(keys(en).sort()).toEqual(keys(es).sort());
  const get = (o: object, k: string) => k.split(".").reduce<any>((n, p) => n[p], o) as string;
  for (const k of keys(es)) expect([k, params(get(en, k))]).toEqual([k, params(get(es, k))]);
  for (const k of keys(en)) expect([k, get(en, k).trim().length > 0]).toEqual([k, true]);
});

it("traduce con parámetros y cae al español o a la clave", () => {
  expect(translate("es", "comun.paradaDe", { n: 2, total: 7 })).toBe("Parada 2 de 7");
  expect(translate("en", "comun.paradaDe", { n: 2, total: 7 })).toBe("Stop 2 of 7");
  expect(translate("en", "no.existe")).toBe("no.existe");
});
