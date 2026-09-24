import { useCallback, useEffect, useState } from "react";
import type { CityPack } from "@/content/types";
import { cityOfflineStatus, deleteCity, downloadCity, offlineSupported } from "./offline";

export type CityOfflineState =
  | { kind: "unsupported" }
  | { kind: "checking" }
  | { kind: "none" }
  | { kind: "downloading"; percentage: number; bytes: number }
  | { kind: "complete"; bytes: number }
  | { kind: "error"; message: string };

/** Estado y acciones del mapa sin conexión de una ciudad. */
export function useCityOffline(pack: CityPack | undefined) {
  const [state, setState] = useState<CityOfflineState>(offlineSupported ? { kind: "checking" } : { kind: "unsupported" });

  const refresh = useCallback(async () => {
    if (!pack || !offlineSupported) return;
    try {
      const s = await cityOfflineStatus(pack);
      setState(
        s.state === "complete"
          ? { kind: "complete", bytes: s.bytes }
          : s.state === "partial"
            ? { kind: "downloading", percentage: s.percentage, bytes: s.bytes }
            : { kind: "none" },
      );
    } catch (e) {
      setState({ kind: "error", message: String(e) });
    }
  }, [pack]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const download = useCallback(async () => {
    if (!pack || !offlineSupported) return;
    setState({ kind: "downloading", percentage: 0, bytes: 0 });
    try {
      await downloadCity(
        pack,
        (percentage, bytes) =>
          setState(percentage >= 100 ? { kind: "complete", bytes } : { kind: "downloading", percentage, bytes }),
        (message) => setState({ kind: "error", message }),
      );
    } catch (e) {
      setState({ kind: "error", message: String(e) });
    }
  }, [pack]);

  const remove = useCallback(async () => {
    if (!pack) return;
    await deleteCity(pack);
    setState({ kind: "none" });
  }, [pack]);

  return { state, download, remove };
}
