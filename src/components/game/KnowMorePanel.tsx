import { useState } from "react";
import { Text } from "react-native";
import { useI18n } from "@/i18n";
import { colors, type } from "@/theme";
import { Button3D } from "../ui/Button3D";
import { Panel } from "../ui/Panel";

type Props = {
  text: string;
  onNext: () => void;
};

/**
 * "Saber más" (capa "free tour"): plegado por defecto para no alargar el paso a paso
 * mientras se camina; un botón lo despliega y otro sigue en cualquier momento.
 */
export function KnowMorePanel({ text, onNext }: Props) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  return (
    <Panel nameplate={t("jugar.saberMas")} nameplateColor={colors.sea}>
      {open ? <Text style={type.body}>{text}</Text> : null}
      {!open ? (
        <Button3D label={t("jugar.saberMasAbrir")} icon="bulb" variant="secondary" small onPress={() => setOpen(true)} />
      ) : null}
      <Button3D label={t("comun.siguiente")} icon="next" small onPress={onNext} />
    </Panel>
  );
}
