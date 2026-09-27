import { useEffect, useState } from "react";
import type { CityPack } from "@/content/types";

/**
 * Máxima de hoy en la ciudad (Open-Meteo, sin clave ni datos del jugador: solo el centro de la
 * ciudad). Sin conexión o si falla, null: el aviso de calor simplemente no sale.
 */
const cache = new Map<string, number | null>();

export async function todayMaxTemp(pack: CityPack, signal?: AbortSignal): Promise<number | null> {
  const day = new Date().toISOString().slice(0, 10);
  const key = `${pack.id}:${day}`;
  if (cache.has(key)) return cache.get(key)!;
  const { lat, lng } = pack.center;
  const url =
    `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}` +
    `&daily=temperature_2m_max&forecast_days=1&timezone=${encodeURIComponent(pack.timeZone ?? "auto")}`;
  try {
    const res = await fetch(url, { signal });
    if (!res.ok) return null;
    const data = (await res.json()) as { daily?: { temperature_2m_max?: number[] } };
    const max = data.daily?.temperature_2m_max?.[0];
    const value = typeof max === "number" ? Math.round(max) : null;
    cache.set(key, value);
    return value;
  } catch {
    return null;
  }
}

/** A partir de esta máxima (°C) se avisa del calor; desde `EXTREME_HEAT`, con más insistencia. */
export const HOT_DAY = 30;
export const EXTREME_HEAT = 36;

export function useTodayMaxTemp(pack: CityPack): number | null {
  const [max, setMax] = useState<number | null>(null);
  useEffect(() => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 8000);
    todayMaxTemp(pack, ctrl.signal).then((t) => {
      if (!ctrl.signal.aborted) setMax(t);
    });
    return () => {
      clearTimeout(timer);
      ctrl.abort();
    };
  }, [pack]);
  return max;
}
