import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useMemo, useRef, useState } from "react";
import { StyleSheet, Text, useWindowDimensions, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { ArrivalPanel } from "@/components/game/ArrivalPanel";
import { CaseClosed } from "@/components/game/CaseClosed";
import { ChallengePanel } from "@/components/game/ChallengePanel";
import { ThenNowPanel } from "@/components/game/ThenNowPanel";
import { Screen, TopBar } from "@/components/layout/Screen";
import { AzulejoBackground, ChoiceCard, DialogBox, Hud } from "@/components/ui";
import type { CityPack, I18nText, PlayerProgress, Route } from "@/content/types";
import { findRoute } from "@/engine/catalog";
import { useArrivalWatcher } from "@/hooks/useArrivalWatcher";
import { useVoice, Voice } from "@/hooks/useVoice";
import { useIsFocused } from "@react-navigation/native";
import { getNode, hasArrived, routeStops } from "@/engine/runner";
import { buildSteps, SceneStep } from "@/engine/scene";
import { SCENE_ASPECT, SceneStage } from "@/scene/SceneStage";
import { stageCast } from "@/scene/cast";
import { sceneKeyFor } from "@/scene/sceneFor";
import { castShadow, sunPosition } from "@/scene/sun";
import { StringKey, useI18n } from "@/i18n";
import type { ArrivalMethod } from "@/analytics";
import { useFieldTest } from "@/field/store";
import type { Fix } from "@/geo/watchPosition";
import { useProgress } from "@/store/progress";
import { border, colors, fonts, radius, type } from "@/theme";

/** Pantalla de juego (modo ruta): escena + HUD + diálogo, alimentada por el motor. */
export default function Jugar() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const found = useMemo(() => findRoute(id), [id]);
  const hydrated = useProgress((s) => s.hydrated);
  const run = useProgress((s) => s.runs[id]);
  const start = useProgress((s) => s.start);
  const { t } = useI18n();

  // Sin partida guardada: se empieza desde el nodo inicial.
  useEffect(() => {
    if (hydrated && found && !run) start(found.pack.id, found.route);
  }, [hydrated, found, run, start]);

  if (!found) {
    return (
      <Screen>
        <TopBar title={t("ruta.noEncontrada")} onBack={() => router.back()} />
        <Text style={type.body}>{t("ruta.noValida")}</Text>
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
  const window = useWindowDimensions();
  const { L, lang } = useI18n();
  // Escenario con la proporción de las ilustraciones; en pantallas bajas se recorta ("cover").
  const stageHeight = Math.min(window.width / SCENE_ASPECT, window.height * 0.8);
  const advance = useProgress((s) => s.advance);
  const demoMode = useProgress((s) => s.demoMode);
  const markArrived = useProgress((s) => s.markArrived);
  const recordChallenge = useProgress((s) => s.recordChallenge);
  const node = getNode(route, run.currentNodeId);
  // Nodo con ubicación: la escena espera a la llegada (guardada en el progreso). Los narrativos empiezan ya.
  const arrived = hasArrived(route, run);
  // Prueba de campo: posiciones cerca de la parada y cómo se detectó cada llegada.
  const field = useFieldTest();
  const waitingSince = useRef(Date.now());
  const arrive = (method: ArrivalMethod, at?: Fix) => {
    // Con GPS, la posición que provocó la llegada; si no, la última conocida.
    const fix = at ?? watchRef.current?.lastFix;
    field.addArrival({
      routeId: route.id,
      nodeId: node.id,
      method,
      lat: fix?.lat,
      lng: fix?.lng,
      accuracy: fix?.accuracy,
      waitedS: Math.round((Date.now() - waitingSince.current) / 1000),
    });
    markArrived(route, method);
  };
  const watch = useArrivalWatcher(
    node,
    !arrived,
    (fix) => arrive("gps", fix),
    (fix) => field.addFix({ routeId: route.id, nodeId: node.id, ...fix }),
  );
  const watchRef = useRef(watch);
  watchRef.current = watch;
  const steps = useMemo(() => buildSteps(route, node, run.flags), [route, node, run.flags]);
  const [index, setIndex] = useState(0);
  const step = steps[Math.min(index, steps.length - 1)];
  // Al acabar los pasos de un nodo sin salida explícita, el siguiente nodo narrativo se lanza solo.
  const next = () => (index + 1 < steps.length ? setIndex(index + 1) : advance(route));
  const { stops, current } = routeStops(route, run);
  const sceneKey = sceneKeyFor(route, run);
  // Sombra de los personajes con el sol real de esta parada, a esta hora.
  const shadow = useMemo(() => {
    const at = node.location ?? pack.center;
    return castShadow(sunPosition(new Date(), at.lat, at.lng));
  }, [node, pack.center]);
  // Voz de la línea actual (real o simulada): lip-sync y barra de audio.
  const focused = useIsFocused();
  const voicesOn = useProgress((s) => s.voices);
  const subtitles = useProgress((s) => s.subtitles);
  const line = arrived ? spokenLine(step, `${node.id}:${index}`, L) : undefined;
  const voice = useVoice(line, { enabled: voicesOn, active: focused, lang });
  // Mientras se espera la llegada, en escena solo está el guía.
  const cast = useMemo(
    () => stageCast(pack, route, node, arrived ? step : undefined),
    [pack, route, node, arrived, step],
  );

  const characterName = (characterId?: string) =>
    L(pack.characters.find((c) => c.id === (characterId ?? route.guideCharacterId))?.name ?? { es: "" });

  return (
    <View style={styles.root}>
      <AzulejoBackground />
      <View style={[styles.stage, { height: stageHeight }]}>
        <SceneStage
          key={sceneKey}
          sceneKey={sceneKey}
          cast={cast}
          talking={voice.speaking}
          shadow={shadow}
          testID="escenario"
          fallback={<Text style={styles.stageText}>{L(node.title)}</Text>}
        />
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
          <ArrivalPanel
            node={node}
            demoMode={demoMode}
            watch={watch}
            onArrive={(method) => arrive(method)}
            fieldTest={field.enabled}
          />
        ) : (
          <StepView
            step={step}
            voice={voice}
            showText={subtitles || !voice.hasAudio}
            route={route}
            characterName={characterName}
            onNext={next}
            onChoose={(choice) => advance(route, choice)}
            onContinue={() => advance(route)}
            onChallenge={(correct) => recordChallenge(route, correct)}
            sceneKey={sceneKey}
          />
        )}
      </View>
    </View>
  );
}

/** Texto hablado del paso (lo que dice alguien), para la voz y el lip-sync. */
function spokenLine(step: SceneStep, key: string, L: (text: I18nText) => string) {
  switch (step.kind) {
    case "text":
      return step.source === "dialogue" || step.source === "narration"
        ? { key, text: L(step.text), audio: step.audio, speaker: step.characterId }
        : undefined;
    case "decision":
      return step.intro ? { key, text: L(step.intro.text), speaker: step.intro.characterId } : undefined;
    case "continue":
      return step.hint ? { key, text: L(step.hint) } : undefined;
    default:
      return undefined;
  }
}

type StepViewProps = {
  step: SceneStep;
  voice: Voice;
  /** Subtítulos desactivados y con voz grabada: se oculta el texto. */
  showText: boolean;
  route: Route;
  characterName: (id?: string) => string;
  onNext: () => void;
  onChoose: (choice: Extract<SceneStep, { kind: "decision" }>["choices"][number]) => void;
  onContinue: () => void;
  onChallenge: (correct: boolean) => void;
  sceneKey?: string;
};

function StepView({
  step,
  voice,
  showText,
  route,
  characterName,
  onNext,
  onChoose,
  onContinue,
  onChallenge,
  sceneKey,
}: StepViewProps) {
  const { t, L } = useI18n();
  const audio = { audioProgress: voice.progress, onReplay: voice.replay };
  const shown = (text: string) => (showText ? text : "…");
  switch (step.kind) {
    case "text": {
      const { speaker, color } = textSpeaker(step, characterName, t, route.theme);
      return <DialogBox speaker={speaker} speakerColor={color} text={shown(L(step.text))} onNext={onNext} {...audio} />;
    }
    case "then_now":
      return (
        <ThenNowPanel then={step.then} now={step.now} caption={step.caption} sceneKey={sceneKey} onNext={onNext} />
      );
    case "challenge":
      return (
        <ChallengePanel
          challenge={step.challenge}
          onDone={(correct) => {
            if (correct !== undefined) onChallenge(correct);
            onNext();
          }}
        />
      );
    case "clue":
      return (
        <DialogBox
          speaker={t("jugar.pistaNueva")}
          speakerColor={colors.ink}
          text={L(step.text)}
          nextLabel={t("jugar.apuntada")}
          onNext={onNext}
        />
      );
    case "decision":
      return (
        <DialogBox
          speaker={characterName(step.intro?.characterId)}
          text={step.intro ? shown(L(step.intro.text)) : t("jugar.queCamino")}
          choices={step.choices.map((choice) => {
            const target = getNode(route, choice.targetNodeId);
            const meta = [
              choice.distanceM && `${choice.distanceM} m`,
              choice.walkMin && t("comun.minutos", { n: choice.walkMin }),
            ]
              .filter(Boolean)
              .join(" · ");
            return (
              <ChoiceCard
                key={choice.targetNodeId}
                title={L(choice.label)}
                hint={choice.hint && L(choice.hint)}
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
          text={step.hint ? shown(L(step.hint)) : t("jugar.siguienteParada", { title: L(step.nextTitle) })}
          nextLabel={t("jugar.seguir")}
          onNext={onContinue}
          {...audio}
        />
      );
    case "ending":
      return (
        <DialogBox
          speaker={characterName()}
          text={t("jugar.casoResuelto")}
          nextLabel={t("jugar.cerrarCaso")}
          onNext={onContinue}
        />
      );
  }
}

function textSpeaker(
  step: Extract<SceneStep, { kind: "text" }>,
  characterName: (id?: string) => string,
  t: (key: StringKey, params?: Record<string, string | number>) => string,
  theme?: Route["theme"],
) {
  switch (step.source) {
    case "dialogue":
      return { speaker: characterName(step.characterId), color: colors.clay };
    case "historical_fact":
      // En las rutas gastronómicas y de fiestas los datos no son de historia.
      if (theme === "gastronomia") return { speaker: t("jugar.datoGastronomico"), color: colors.sea };
      if (theme === "fiestas") return { speaker: t("jugar.tradicion"), color: colors.sea };
      return { speaker: step.year ? t("jugar.datoAnio", { year: step.year }) : t("jugar.dato"), color: colors.sea };
    case "anecdote":
      return { speaker: step.legend ? t("jugar.seCuenta") : t("jugar.anecdota"), color: colors.ink };
    case "image":
    case "narration":
      return { speaker: t("jugar.narrador"), color: colors.ink };
  }
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: colors.ink },
  stage: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    borderBottomWidth: border.thick,
    borderColor: colors.ink,
  },
  stageText: { fontFamily: fonts.bold, color: colors.muted },
  hud: { position: "absolute", left: 14, right: 14 },
  dialog: { position: "absolute", left: 12, right: 12, borderRadius: radius.xl },
});
