import raw from "@content/malaga/misterio-manquita.pack.json";
import type { Route } from "@/content/types";
import { loadPack } from "@/engine/loadPack";
import { getNode } from "@/engine/runner";
import { useProgress } from "@/store/progress";
import { setAnalyticsSink, TrackedEvent } from "../index";

const result = loadPack(raw);
if (!result.ok) throw new Error(result.errors.join("\n"));
const route: Route = result.pack.routes[0];

let events: TrackedEvent[] = [];
beforeEach(() => {
  events = [];
  setAnalyticsSink((e) => events.push(e));
  useProgress.setState({ runs: {}, analytics: false });
});

function playPoderLeyenda() {
  const s = useProgress.getState();
  s.start("malaga", route);
  for (;;) {
    const run = useProgress.getState().runs[route.id];
    if (run.completedAt) return;
    const node = getNode(route, run.currentNodeId);
    if (node.location) useProgress.getState().markArrived(route, "demo");
    if (node.challenge && node.challenge.type !== "photo") useProgress.getState().recordChallenge(route, true);
    useProgress.getState().advance(route, node.choices?.[node.id === "n2_larios" ? 1 : 0]);
  }
}

it("sin consentimiento no se registra nada", () => {
  playPoderLeyenda();
  expect(events).toEqual([]);
});

it("con consentimiento registra el recorrido sin datos personales", () => {
  useProgress.getState().setAnalytics(true);
  playPoderLeyenda();
  const names = events.map((e) => e.name);
  expect(names[0]).toBe("route_started");
  expect(names.filter((n) => n === "decision_made")).toHaveLength(2);
  expect(names.filter((n) => n === "stop_arrived")).toHaveLength(6);
  expect(names.filter((n) => n === "challenge_answered")).toHaveLength(5);
  expect(names[names.length - 1]).toBe("route_completed");
  expect(events[events.length - 1]).toMatchObject({ endingId: "cuentacuentos", stars: 3 });
  expect(events.find((e) => e.name === "stop_arrived")).toMatchObject({ method: "demo", nodeId: "n1_cenachero" });
  // Nunca coordenadas.
  expect(JSON.stringify(events)).not.toMatch(/lat|lng|36\.7/);
});

it("un sink que falla no rompe el juego", () => {
  setAnalyticsSink(() => {
    throw new Error("sin red");
  });
  useProgress.getState().setAnalytics(true);
  expect(() => playPoderLeyenda()).not.toThrow();
});
