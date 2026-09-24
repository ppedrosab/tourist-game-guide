import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import type { Challenge } from "@/content/types";
import { localize } from "@/engine/runner";
import { checkObserveAnswer } from "@/engine/scene";
import { border, colors, fonts, radius, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Icon } from "../ui/Icon";
import { Panel } from "../ui/Panel";

type Props = { challenge: Challenge; onDone: () => void };

/** Reto de una parada: quiz, observación o foto. Fallar no bloquea la historia. */
export function ChallengePanel({ challenge, onDone }: Props) {
  switch (challenge.type) {
    case "quiz":
      return <Quiz challenge={challenge} onDone={onDone} />;
    case "observe":
      return <Observe challenge={challenge} onDone={onDone} />;
    case "photo":
      return (
        <Panel nameplate="Reto de foto" nameplateColor={colors.sea}>
          <Text style={type.dialogue}>{localize(challenge.prompt)}</Text>
          {/* Fase 3: cámara real. De momento el jugador confirma que la ha hecho. */}
          <Button3D label="¡Hecha!" icon="camera" variant="sea" onPress={onDone} />
          <Button3D label="Saltar" variant="ghost" onPress={onDone} />
        </Panel>
      );
  }
}

function Quiz({ challenge, onDone }: { challenge: Extract<Challenge, { type: "quiz" }>; onDone: () => void }) {
  const [picked, setPicked] = useState<number | null>(null);
  const answered = picked !== null;
  const right = picked === challenge.correctIndex;
  return (
    <Panel nameplate="Reto" nameplateColor={colors.sea}>
      <Text style={type.dialogue}>{localize(challenge.question)}</Text>
      <View style={{ gap: 8 }}>
        {challenge.options.map((option, i) => {
          const isCorrect = i === challenge.correctIndex;
          const bg = !answered ? colors.white : isCorrect ? colors.seaTint : i === picked ? colors.clayTint : colors.white;
          return (
            <Pressable
              key={i}
              disabled={answered}
              onPress={() => setPicked(i)}
              accessibilityRole="button"
              accessibilityState={{ disabled: answered, selected: i === picked }}
              style={[styles.option, { backgroundColor: bg }]}
            >
              <Text style={[type.label, { flex: 1 }]}>{localize(option)}</Text>
              {answered && isCorrect ? <Icon name="check" size={18} color={colors.sea} /> : null}
              {answered && i === picked && !isCorrect ? <Icon name="close" size={18} color={colors.clay} /> : null}
            </Pressable>
          );
        })}
      </View>
      {answered ? (
        <>
          <Text style={[styles.verdict, { color: right ? colors.sea : colors.clay }]}>
            {right ? "¡Correcto!" : "¡Casi!"}
          </Text>
          {challenge.explanation ? <Text style={type.body}>{localize(challenge.explanation)}</Text> : null}
          <Button3D label="Siguiente" icon="next" small onPress={onDone} />
        </>
      ) : null}
    </Panel>
  );
}

function Observe({ challenge, onDone }: { challenge: Extract<Challenge, { type: "observe" }>; onDone: () => void }) {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<"ok" | "ko" | "revealed" | null>(null);
  const check = () => setResult(checkObserveAnswer(challenge.answer, input) ? "ok" : "ko");
  return (
    <Panel nameplate="Observa" nameplateColor={colors.sea}>
      <Text style={type.dialogue}>{localize(challenge.prompt)}</Text>
      {result === "ok" || result === "revealed" ? (
        <>
          <Text style={[styles.verdict, { color: result === "ok" ? colors.sea : colors.clay }]}>
            {result === "ok" ? "¡Bien visto!" : `La respuesta era: ${challenge.answer[0]}`}
          </Text>
          <Button3D label="Siguiente" icon="next" small onPress={onDone} />
        </>
      ) : (
        <>
          <TextInput
            value={input}
            onChangeText={(t) => {
              setInput(t);
              setResult(null);
            }}
            onSubmitEditing={check}
            placeholder="Tu respuesta"
            placeholderTextColor={colors.muted}
            autoCapitalize="none"
            returnKeyType="done"
            accessibilityLabel="Tu respuesta"
            style={styles.input}
          />
          {result === "ko" ? <Text style={[styles.verdict, { color: colors.clay }]}>Mmm… mira otra vez.</Text> : null}
          <View style={styles.row}>
            <View style={{ flex: 1 }}>
              <Button3D label="Comprobar" small disabled={!input.trim()} onPress={check} />
            </View>
            <Button3D label="Ver respuesta" variant="ghost" onPress={() => setResult("revealed")} />
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
