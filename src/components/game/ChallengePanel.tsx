import { useMemo, useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { hintGate } from "@/ads/hints";
import type { Challenge, I18nText } from "@/content/types";
import { hintCount } from "@/engine/runner";
import { checkObserveAnswer } from "@/engine/scene";
import { useI18n } from "@/i18n";
import { border, colors, fonts, radius, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Icon } from "../ui/Icon";
import { Panel } from "../ui/Panel";

/**
 * `correct`: acertado sin «Ver respuesta» ni fallos (undefined en los retos de foto).
 * `onHint`: se ha concedido una pista (para apuntarla en el progreso).
 */
type Props = {
  challenge: Challenge;
  onDone: (correct?: boolean) => void;
  onHint?: () => void;
};
type Graded = Exclude<Challenge, { type: "photo" }>;

/** Reto de una parada: quiz, observación, acertijo, candado, ordenar o foto. Fallar no bloquea la historia. */
export function ChallengePanel({ challenge, onDone, onHint }: Props) {
  const { t, L } = useI18n();
  switch (challenge.type) {
    case "quiz":
      return <Quiz challenge={challenge} onDone={onDone} onHint={onHint} />;
    case "observe":
    case "riddle":
    case "lock":
      return (
        <TextAnswer challenge={challenge} onDone={onDone} onHint={onHint} />
      );
    case "order":
      return <Order challenge={challenge} onDone={onDone} onHint={onHint} />;
    case "photo":
      return (
        <Panel nameplate={t("reto.foto")} nameplateColor={colors.sea}>
          <Text style={type.dialogue}>{L(challenge.prompt)}</Text>
          {/* Fase 3: cámara real. De momento el jugador confirma que la ha hecho. */}
          <Button3D
            label={t("reto.hecha")}
            icon="camera"
            variant="sea"
            onPress={() => onDone()}
          />
          <Button3D
            label={t("reto.saltar")}
            variant="ghost"
            onPress={() => onDone()}
          />
        </Panel>
      );
  }
}

/** Pistas del reto: pide la siguiente a la puerta de pistas (gratis o con anuncio) y lleva la cuenta. */
function useHints(challenge: Graded, onHint?: () => void) {
  const [shown, setShown] = useState(0);
  const [asking, setAsking] = useState(false);
  const total = hintCount(challenge);
  const ask = async () => {
    if (asking || shown >= total) return;
    setAsking(true);
    try {
      if (await hintGate().request()) {
        setShown((n) => n + 1);
        onHint?.();
      }
    } finally {
      setAsking(false);
    }
  };
  return { shown, total, asking, ask };
}

/** Pistas escritas ya pedidas y el botón para pedir otra. */
function HintBar({
  hints,
  state,
  done,
}: {
  hints?: I18nText[];
  state: ReturnType<typeof useHints>;
  done: boolean;
}) {
  const { t, L } = useI18n();
  const withAd = hintGate().kind === "ad";
  return (
    <View style={{ gap: 8 }}>
      {(hints ?? []).slice(0, state.shown).map((h, i) => (
        <View
          key={i}
          style={styles.hint}
          accessibilityLabel={t("reto.pistaN", { n: i + 1 })}
        >
          <Icon name="bulb" size={18} color={colors.ink} />
          <Text style={[type.body, { flex: 1 }]}>{L(h)}</Text>
        </View>
      ))}
      {!done && state.shown < state.total ? (
        <Button3D
          label={
            withAd
              ? t("reto.pistaAnuncio", {
                  n: state.shown + 1,
                  total: state.total,
                })
              : t("reto.pedirPista", { n: state.shown + 1, total: state.total })
          }
          icon={withAd ? "ad" : "bulb"}
          variant="ghost"
          small
          disabled={state.asking}
          onPress={state.ask}
        />
      ) : null}
    </View>
  );
}

function Quiz({
  challenge,
  onDone,
  onHint,
}: {
  challenge: Extract<Challenge, { type: "quiz" }>;
  onDone: Props["onDone"];
  onHint?: () => void;
}) {
  const { t, L } = useI18n();
  const [picked, setPicked] = useState<number | null>(null);
  const hints = useHints(challenge, onHint);
  const answered = picked !== null;
  const right = picked === challenge.correctIndex;
  // Sin pistas escritas, cada pista quita una opción incorrecta (siempre las mismas, en orden).
  const removed = challenge.hints?.length
    ? []
    : challenge.options
        .map((_, i) => i)
        .filter((i) => i !== challenge.correctIndex)
        .slice(0, hints.shown);
  return (
    <Panel nameplate={t("reto.reto")} nameplateColor={colors.sea}>
      <Text style={type.dialogue}>{L(challenge.question)}</Text>
      <View style={{ gap: 8 }}>
        {challenge.options.map((option, i) => {
          if (removed.includes(i) && !answered) return null;
          const isCorrect = i === challenge.correctIndex;
          const bg = !answered
            ? colors.white
            : isCorrect
              ? colors.seaTint
              : i === picked
                ? colors.clayTint
                : colors.white;
          return (
            <Pressable
              key={i}
              disabled={answered}
              onPress={() => setPicked(i)}
              accessibilityRole="button"
              accessibilityState={{
                disabled: answered,
                selected: i === picked,
              }}
              style={[styles.option, { backgroundColor: bg }]}
            >
              <Text style={[type.label, { flex: 1 }]}>{L(option)}</Text>
              {answered && isCorrect ? (
                <Icon name="check" size={18} color={colors.sea} />
              ) : null}
              {answered && i === picked && !isCorrect ? (
                <Icon name="close" size={18} color={colors.clay} />
              ) : null}
            </Pressable>
          );
        })}
      </View>
      <HintBar hints={challenge.hints} state={hints} done={answered} />
      {answered ? (
        <>
          <Text
            style={[
              styles.verdict,
              { color: right ? colors.sea : colors.clay },
            ]}
          >
            {right ? t("reto.correcto") : t("reto.casi")}
          </Text>
          {challenge.explanation ? (
            <Text style={type.body}>{L(challenge.explanation)}</Text>
          ) : null}
          <Button3D
            label={t("comun.siguiente")}
            icon="next"
            small
            onPress={() => onDone(right)}
          />
        </>
      ) : null}
    </Panel>
  );
}

const TEXT_TITLES = {
  observe: "reto.observa",
  riddle: "reto.acertijo",
  lock: "reto.candado",
} as const;

/** Observación, acertijo o candado final: respuesta escrita. */
function TextAnswer({
  challenge,
  onDone,
  onHint,
}: {
  challenge: Extract<Challenge, { type: "observe" | "riddle" | "lock" }>;
  onDone: Props["onDone"];
  onHint?: () => void;
}) {
  // Acierto a la primera: ni fallos previos ni «Ver respuesta».
  const [missed, setMissed] = useState(false);
  const { t, L } = useI18n();
  const [input, setInput] = useState("");
  const [result, setResult] = useState<"ok" | "ko" | "revealed" | null>(null);
  const hints = useHints(challenge, onHint);
  const done = result === "ok" || result === "revealed";
  const check = () => {
    const ok = checkObserveAnswer(challenge.answer, input);
    if (!ok) setMissed(true);
    setResult(ok ? "ok" : "ko");
  };
  return (
    <Panel
      nameplate={t(TEXT_TITLES[challenge.type])}
      nameplateColor={challenge.type === "lock" ? colors.ink : colors.sea}
    >
      {challenge.type === "lock" ? (
        <View style={styles.lockHead}>
          <Icon name="lock" size={22} color={colors.ink} />
          <Text style={[type.caption, { flex: 1 }]}>
            {t("reto.candadoAyuda")}
          </Text>
        </View>
      ) : null}
      <Text style={type.dialogue}>{L(challenge.prompt)}</Text>
      {done ? (
        <>
          <Text
            style={[
              styles.verdict,
              { color: result === "ok" ? colors.sea : colors.clay },
            ]}
          >
            {result === "ok"
              ? t(challenge.type === "lock" ? "reto.abierto" : "reto.bienVisto")
              : t("reto.respuestaEra", { answer: challenge.answer[0] })}
          </Text>
          {challenge.explanation ? (
            <Text style={type.body}>{L(challenge.explanation)}</Text>
          ) : null}
          <Button3D
            label={t("comun.siguiente")}
            icon="next"
            small
            onPress={() => onDone(result === "ok" && !missed)}
          />
        </>
      ) : (
        <>
          <TextInput
            value={input}
            onChangeText={(v) => {
              setInput(v);
              setResult(null);
            }}
            onSubmitEditing={check}
            placeholder={t("reto.tuRespuesta")}
            placeholderTextColor={colors.muted}
            autoCapitalize="none"
            returnKeyType="done"
            accessibilityLabel={t("reto.tuRespuesta")}
            style={styles.input}
          />
          {result === "ko" ? (
            <Text style={[styles.verdict, { color: colors.clay }]}>
              {t("reto.otraVez")}
            </Text>
          ) : null}
          <HintBar hints={challenge.hints} state={hints} done={done} />
          <View style={styles.row}>
            <View style={{ flex: 1 }}>
              <Button3D
                label={t("reto.comprobar")}
                small
                disabled={!input.trim()}
                onPress={check}
              />
            </View>
            <Button3D
              label={t("reto.verRespuesta")}
              variant="ghost"
              onPress={() => setResult("revealed")}
            />
          </View>
        </>
      )}
    </Panel>
  );
}

/** Barajado fijo (el mismo cada vez para el mismo reto) y nunca en el orden correcto. */
function shuffled(n: number, seed: string): number[] {
  let h = 0;
  for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const idx = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    h = (h * 1103515245 + 12345) >>> 0;
    const j = h % (i + 1);
    [idx[i], idx[j]] = [idx[j], idx[i]];
  }
  if (idx.every((v, i) => v === i)) idx.reverse();
  return idx;
}

/** Ordenar: toca los elementos en orden. Sin pistas escritas, cada pista coloca el siguiente. */
function Order({
  challenge,
  onDone,
  onHint,
}: {
  challenge: Extract<Challenge, { type: "order" }>;
  onDone: Props["onDone"];
  onHint?: () => void;
}) {
  const { t, L } = useI18n();
  const deck = useMemo(
    () =>
      shuffled(
        challenge.items.length,
        challenge.items.map((i) => i.es).join("|"),
      ),
    [challenge],
  );
  const [placed, setPlaced] = useState<number[]>([]);
  const [missed, setMissed] = useState(false);
  const [result, setResult] = useState<"ok" | "ko" | "revealed" | null>(null);
  const hints = useHints(challenge, () => {
    onHint?.();
    // Pista sin texto: fija el siguiente elemento correcto al principio.
    if (!challenge.hints?.length)
      setPlaced((p) => [
        ...Array.from({ length: fixedCount(p) + 1 }, (_, i) => i),
      ]);
  });
  const fixedCount = (p: number[]) =>
    p.findIndex((v, i) => v !== i) === -1
      ? p.length
      : p.findIndex((v, i) => v !== i);
  const n = challenge.items.length;
  const done = result === "ok" || result === "revealed";
  const shown =
    result === "revealed" ? Array.from({ length: n }, (_, i) => i) : placed;
  const place = (i: number) => {
    const next = [...placed, i];
    setPlaced(next);
    setResult(null);
    if (next.length === n) {
      const ok = next.every((v, k) => v === k);
      if (!ok) {
        setMissed(true);
        setPlaced(next.slice(0, fixedCount(next)));
      }
      setResult(ok ? "ok" : "ko");
    }
  };
  return (
    <Panel nameplate={t("reto.ordena")} nameplateColor={colors.sea}>
      <Text style={type.dialogue}>{L(challenge.prompt)}</Text>
      <View style={{ gap: 6 }}>
        {shown.map((i, k) => (
          <View
            key={i}
            style={[styles.option, { backgroundColor: colors.seaTint }]}
          >
            <Text style={styles.num}>{k + 1}</Text>
            <Text style={[type.label, { flex: 1 }]}>
              {L(challenge.items[i])}
            </Text>
          </View>
        ))}
      </View>
      {done ? (
        <>
          <Text
            style={[
              styles.verdict,
              { color: result === "ok" ? colors.sea : colors.clay },
            ]}
          >
            {result === "ok" ? t("reto.correcto") : t("reto.ordenCorrecto")}
          </Text>
          {challenge.explanation ? (
            <Text style={type.body}>{L(challenge.explanation)}</Text>
          ) : null}
          <Button3D
            label={t("comun.siguiente")}
            icon="next"
            small
            onPress={() => onDone(result === "ok" && !missed)}
          />
        </>
      ) : (
        <>
          <View style={{ gap: 8 }}>
            {deck
              .filter((i) => !placed.includes(i))
              .map((i) => (
                <Pressable
                  key={i}
                  onPress={() => place(i)}
                  accessibilityRole="button"
                  accessibilityLabel={t("reto.ponerEnPosicion", {
                    item: L(challenge.items[i]),
                    n: placed.length + 1,
                  })}
                  style={[styles.option, { backgroundColor: colors.white }]}
                >
                  <Text style={[type.label, { flex: 1 }]}>
                    {L(challenge.items[i])}
                  </Text>
                </Pressable>
              ))}
          </View>
          {result === "ko" ? (
            <Text style={[styles.verdict, { color: colors.clay }]}>
              {t("reto.ordenMal")}
            </Text>
          ) : null}
          <HintBar hints={challenge.hints} state={hints} done={done} />
          <View style={styles.row}>
            <View style={{ flex: 1 }}>
              <Button3D
                label={t("reto.deshacer")}
                icon="undo"
                small
                variant="secondary"
                disabled={placed.length === 0}
                onPress={() => setPlaced((p) => p.slice(0, -1))}
              />
            </View>
            <Button3D
              label={t("reto.verRespuesta")}
              variant="ghost"
              onPress={() => setResult("revealed")}
            />
          </View>
        </>
      )}
    </Panel>
  );
}

const styles = StyleSheet.create({
  option: {
    minHeight: 46,
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
  },
  hint: {
    flexDirection: "row",
    gap: 8,
    alignItems: "flex-start",
    padding: 10,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.goldTint,
  },
  lockHead: { flexDirection: "row", alignItems: "center", gap: 8 },
  num: { fontFamily: fonts.bold, fontSize: 16, color: colors.ink, width: 20 },
  verdict: { fontFamily: fonts.bold, fontSize: 16 },
  input: {
    height: 48,
    paddingHorizontal: 14,
    borderRadius: radius.md,
    borderWidth: border.thin,
    borderColor: colors.ink,
    backgroundColor: colors.white,
    fontFamily: fonts.body,
    fontSize: 16,
    color: colors.ink,
  },
  row: { flexDirection: "row", alignItems: "center", gap: 10 },
});
