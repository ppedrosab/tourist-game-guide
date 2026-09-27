import { de } from "../de";
import { en } from "../en";
import { es } from "../es";
import { fr } from "../fr";
import { deviceLang, translate } from "../index";
import { it as itStrings } from "../it";

const keys = (o: object, p = ""): string[] =>
  Object.entries(o).flatMap(([k, v]) => (typeof v === "string" ? [`${p}${k}`] : keys(v, `${p}${k}.`)));
const params = (s: string) => (s.match(/\{\w+\}/g) ?? []).sort().join(",");

it.each([
  ["en", en],
  ["fr", fr],
  ["de", de],
  ["it", itStrings],
])("%s tiene las mismas claves y los mismos parámetros que el español", (_, dict) => {
  expect(keys(dict).sort()).toEqual(keys(es).sort());
  const get = (o: object, k: string) => k.split(".").reduce<any>((n, p) => n[p], o) as string;
  for (const k of keys(es)) expect([k, params(get(dict, k))]).toEqual([k, params(get(es, k))]);
  for (const k of keys(dict)) expect([k, get(dict, k).trim().length > 0]).toEqual([k, true]);
});

it("el idioma automático es el del móvil si la app lo tiene; si no, inglés", () => {
  const spy = jest.spyOn(Intl, "DateTimeFormat");
  const as = (locale: string) =>
    spy.mockReturnValue({ resolvedOptions: () => ({ locale }) } as unknown as Intl.DateTimeFormat);
  as("de-AT");
  expect(deviceLang()).toBe("de");
  as("it-IT");
  expect(deviceLang()).toBe("it");
  as("ja-JP");
  expect(deviceLang()).toBe("en");
  spy.mockRestore();
});

it("traduce con parámetros y cae al español o a la clave", () => {
  expect(translate("es", "comun.paradaDe", { n: 2, total: 7 })).toBe("Parada 2 de 7");
  expect(translate("en", "comun.paradaDe", { n: 2, total: 7 })).toBe("Stop 2 of 7");
  expect(translate("fr", "comun.paradaDe", { n: 2, total: 7 })).toBe("Étape 2 sur 7");
  expect(translate("en", "no.existe")).toBe("no.existe");
});
