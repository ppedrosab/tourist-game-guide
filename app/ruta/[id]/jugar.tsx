import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useMemo, useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ArrivalPanel } from "@/components/game/ArrivalPanel";
import { CaseClosed } from "@/components/game/CaseClosed";
import { ChallengePanel } from "@/components/game/ChallengePanel";
import { Screen, TopBar } from "@/components/layout/Screen";
import { AzulejoBackground, ChoiceCard, DialogBox, Hud } from "@/components/ui";
import type { CityPack, PlayerProgress, Route } from "@/content/types";
import { findRoute } from "@/engine/catalog";
import { useArrivalWatcher } from "@/hooks/useArrivalWatcher";
import { getNode, hasArrived, localize, routeStops } from "@/engine/runner";
import { buildSteps, SceneStep } from "@/engine/scene";
import { useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

/** Pantalla de juego (modo ruta): escena + HUD + diálogo, alimentada por el motor. */
export default function Jugar() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const found = useMemo(() => findRoute(id), [id]);
  const hydrated = useProgress((s) => s.hydrated);
  const run = useProgress((s) => s.runs[id]);
  const start = useProgress((s) => s.start);

  // Sin partida guardada: se empieza desde el nodo inicial.
  useEffect(() => {
    if (hydrated && found && !run) start(found.pack.id, found.route);
  }, [hydrated, found, run, start]);

  if (!found) {
    return (
      <Screen>
        <TopBar title="Ruta no encontrada" onBack={() => router.back()} />
        <Text style={type.body}>Esta ruta no existe o su contenido no es válido.</Text>
      </Screen>
    );
  }
  if (!hydrated || !run) return <AzulejoBackground />;
  if (run.completedAt) {
    return (
      <CaseClosed
        route={found.route}
        run={run}
        onReplay={() => start(found.pack.id, found.route)}
        onExit={() => router.dismissTo("/")}
      />
    );
  }
  // `key`: al cambiar de nodo la escena empieza desde su primer paso.
  return <NodePlayer key={run.currentNodeId} pack={found.pack} route={found.route} run={run} />;
}

function NodePlayer({ pack, route, run }: { pack: CityPack; route: Route; run: PlayerProgress }) {
  const insets = useSafeAreaInsets();
  const advance = useProgress((s) => s.advance);
  const demoMode = useProgress((s) => s.demoMode);
  const markArrived = useProgress((s) => s.markArrived);
  const node = getNode(route, run.currentNodeId);
  // Nodo con ubicación: la escena espera a la llegada (guardada en el progreso). Los narrativos empiezan ya.
  const arrived = hasArrived(route, run);
  const watch = useArrivalWatcher(node, !arrived, () => markArrived(route));
  const steps = useMemo(() => buildSteps(route, node, run.flags), [route, node, run.flags]);
  const [index, setIndex] = useState(0);
  const step = steps[Math.min(index, steps.length - 1)];
  // Al acabar los pasos de un nodo sin salida explícita, el siguiente nodo narrativo se lanza solo.
  const next = () => (index + 1 < steps.length ? setIndex(index + 1) : advance(route));
  const { stops, current } = routeStops(route, run);

  const characterName = (characterId?: string) =>
    localize(pack.characters.find((c) => c.id === (characterId ?? route.guideCharacterId))?.name ?? { es: "" });

  return (
    <View style={styles.root}>
      <AzulejoBackground />
      {/* Fase 3: <SceneStage> con fondo por capas, parallax y sprites. */}
      <View style={styles.stage}>
        <Text style={styles.stageText}>{localize(node.title)}</Text>
      </View>

      <View style={[styles.hud, { top: insets.top + 8 }]}>
        <Hud
          stops={stops}
          current={current}
          clues={run.clueIds.length}
          onPause={() => router.push("/pausa")}
          onNotebook={() => router.push("/cuaderno")}
        />
      </View>

      <View style={[styles.dialog, { bottom: insets.bottom + 12 }]}>
        {!arrived ? (
          <ArrivalPanel node={node} demoMode={demoMode} watch={watch} onArrive={() => markArrived(route)} />
        ) : (
          <StepView
            step={step}
            route={route}
            characterName={characterName}
            onNext={next}
            onChoose={(choice) => advance(route, choice)}
            onContinue={() => advance(route)}
          />
        )}
      </View>
    </View>
  );
}

type StepViewProps = {
  step: SceneStep;
  route: Route;
  characterName: (id?: string) => string;
  onNext: () => void;
  onChoose: (choice: Extract<SceneStep, { kind: "decision" }>["choices"][number]) => void;
  onContinue: () => void;
};

function StepView({ step, route, characterName, onNext, onChoose, onContinue }: StepViewProps) {
  switch (step.kind) {
    case "text": {
      const { speaker, color } = textSpeaker(step, characterName);
      return <DialogBox speaker={speaker} speakerColor={color} text={localize(step.text)} onNext={onNext} />;
    }
    case "challenge":
      return <ChallengePanel challenge={step.challenge} onDone={onNext} />;
    case "clue":
      return (
        <DialogBox
          speaker="¡Pista nueva!"
          speakerColor={colors.ink}
          text={localize(step.text)}
          nextLabel="Apuntada"
          onNext={onNext}
        />
      );
    case "decision":
      return (
        <DialogBox
          speaker={characterName(step.intro?.characterId)}
          text={step.intro ? localize(step.intro.text) : "¿Qué camino seguimos?"}
          choices={step.choices.map((choice) => {
            const target = getNode(route, choice.targetNodeId);
            const meta = [choice.distanceM && `${choice.distanceM} m`, choice.walkMin && `${choice.walkMin} min`]
              .filter(Boolean)
              .join(" · ");
            return (
              <ChoiceCard
                key={choice.targetNodeId}
                title={localize(choice.label)}
                hint={choice.hint && localize(choice.hint)}
                meta={meta || undefined}
                branch={target.branch ?? "comun"}
                icon={target.location ? "walk" : "book"}
                onPress={() => onChoose(choice)}
              />
            );
          })}
        />
      );
    case "continue":
      return (
        <DialogBox
          speaker={characterName()}
          text={step.hint ? localize(step.hint) : `Siguiente parada: ${localize(step.nextTitle)}.`}
          nextLabel="Seguir"
          onNext={onContinue}
        />
      );
    case "ending":
      return (
        <DialogBox
          speaker={characterName()}
          text="Caso resuelto, detective. ¿Lo cerramos?"
          nextLabel="Cerrar el caso"
          onNext={onContinue}
        />
      );
  }
}

function textSpeaker(step: Extract<SceneStep, { kind: "text" }>, characterName: (id?: string) => string) {
  switch (step.source) {
    case "dialogue":
      return { speaker: characterName(step.characterId), color: colors.clay };
    case "historical_fact":
      return { speaker: step.year ? `Dato histórico · ${step.year}` : "Dato histórico", color: colors.sea };
    case "anecdote":
      return { speaker: step.legend ? "Se cuenta…" : "Anécdota", color: colors.ink };
    case "then_now":
      return { speaker: "Antes y ahora", color: colors.sea };
    case "image":
    case "narration":
      return { speaker: "Narrador", color: colors.ink };
  }
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.ink },
  stage: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: "70%",
    backgroundColor: colors.sand,
    borderBottomWidth: border.thick,
    borderColor: colors.ink,
    alignItems: "center",
    justifyContent: "center",
  },
  stageText: { fontFamily: fonts.bold, color: colors.muted },
  hud: { position: "absolute", left: 14, right: 14 },
  dialog: { position: "absolute", left: 12, right: 12, borderRadius: radius.xl },
});
