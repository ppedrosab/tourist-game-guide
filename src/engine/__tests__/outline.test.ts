import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "../loadPack";
import { routeFacts, routeOutline, runProgress } from "../outline";
import { advance, startRoute } from "../runner";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];

it("resume la ruta en paradas, decisiones y ramas", () => {
  const outline = routeOutline(route).map((item) =>
    item.kind === "stop"
      ? `${item.node.id}${item.decision ? ` (decisión ${item.decision})` : ""}`
      : item.branches.map((b) => `${b.branch}: ${b.nodes.map((n) => n.id).join(", ")}`).join(" | "),
  );
  expect(outline).toEqual([
    "n1_cenachero",
    "n2_larios (decisión 1)",
    "dinero: a1_atarazanas, a2_casa_guardia | poder: b1_constitucion",
    "n4_manquita (decisión 2)",
    "n5_teatro",
    "n6_merced",
  ]);
});

it("cuenta caminos y finales", () => {
  expect(routeFacts(route)).toEqual({ branches: 2, endings: 4 });
});

it("resume la partida en curso", () => {
  let run = startRoute("malaga", route);
  expect(runProgress(route, run)).toMatchObject({ stop: 1, total: 6, branch: undefined });
  run = advance(route, run);
  run = advance(route, run, route.nodes[1].choices![1]);
  expect(runProgress(route, run)).toMatchObject({ stop: 3, total: 6, branch: "poder" });
  expect(runProgress(route, run).node.id).toBe("b1_constitucion");
});
