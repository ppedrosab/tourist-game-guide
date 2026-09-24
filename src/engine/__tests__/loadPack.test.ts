import raw from "@content/malaga/misterio-manquita.pack.json";
import { loadPack } from "../loadPack";

/** Copia profunda del pack real para romperlo a propósito en cada test. */
const clonePack = (): any => JSON.parse(JSON.stringify(raw));

const errorsOf = (pack: unknown) => {
  const result = loadPack(pack);
  if (result.ok) throw new Error("se esperaba un pack inválido");
  return result.errors;
};

describe("loadPack", () => {
  it("acepta el pack de Málaga", () => {
    const result = loadPack(raw);
    if (!result.ok) throw new Error(result.errors.join("\n"));
    expect(result.pack.routes[0].id).toBe("misterio-manquita");
  });

  it("no lanza con entradas absurdas", () => {
    for (const bad of [null, undefined, 42, "pack", [], {}]) {
      expect(loadPack(bad).ok).toBe(false);
    }
  });

  it("informa de errores de forma con su ruta", () => {
    const pack = clonePack();
    delete pack.routes[0].nodes[0].title;
    pack.routes[0].nodes[1].challenge.correctIndex = 7;
    const errors = errorsOf(pack);
    expect(errors).toEqual(
      expect.arrayContaining([
        expect.stringContaining("routes[0].nodes[0].title"),
        expect.stringContaining("routes[0].nodes[1].challenge.correctIndex"),
      ]),
    );
  });

  it("exige texto o variantes en los diálogos", () => {
    const pack = clonePack();
    delete pack.routes[0].nodes[0].content[1].text;
    expect(errorsOf(pack).join("\n")).toContain("un diálogo necesita `text`");
  });

  it("detecta startNodeId, nextNodeId y targetNodeId inexistentes", () => {
    const pack = clonePack();
    const route = pack.routes[0];
    route.startNodeId = "no_existe";
    route.nodes[0].nextNodeId = "fantasma";
    route.nodes[1].choices[0].targetNodeId = "perdido";
    const errors = errorsOf(pack).join("\n");
    expect(errors).toContain('startNodeId "no_existe" no existe');
    expect(errors).toContain('nodo "n1_cenachero": nextNodeId "fantasma" no existe');
    expect(errors).toContain('nodo "n2_larios": targetNodeId "perdido" no existe');
  });

  it("detecta personajes inexistentes", () => {
    const pack = clonePack();
    pack.routes[0].nodes[0].content[1].characterId = "picasso";
    pack.routes[0].guideCharacterId = "nadie";
    const errors = errorsOf(pack).join("\n");
    expect(errors).toContain('el personaje "picasso" no existe');
    expect(errors).toContain('el personaje "nadie" no existe');
  });

  it("detecta ids duplicados, callejones sin salida y recompensas rotas", () => {
    const pack = clonePack();
    const route = pack.routes[0];
    route.nodes.push({ ...route.nodes[0] });
    delete route.nodes[2].nextNodeId;
    route.nodes[9].reward = "no_existe";
    const errors = errorsOf(pack).join("\n");
    expect(errors).toContain("id de nodo duplicado");
    expect(errors).toContain("callejón sin salida");
    expect(errors).toContain('la recompensa "no_existe" no existe');
  });
});
