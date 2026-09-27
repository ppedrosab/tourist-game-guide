/**
 * Horarios en la sintaxis `opening_hours` de OpenStreetMap, en el subconjunto que guarda
 * `scripts/gen_practical.py` (ya normalizado):
 *
 *   "Tu-Su 10:00-20:00; Mo off"   "Apr-Oct 09:00-20:00; Nov-Mar 09:00-18:00"   "24/7"
 *
 * Reglas separadas por ";", cada una con meses y días opcionales y franjas u "off". Como en OSM,
 * una regla posterior sustituye a las anteriores en los días a los que se aplica. Los festivos
 * (PH) no se tienen en cuenta. Funciones puras: la hora local de la ciudad se calcula con su zona.
 */

const DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

type Rule = { months?: Set<number>; days?: Set<number>; spans: [number, number][] };

/** "Mo-We,Fr" → {0,1,2,4}; con listas circulares ("Sa-Mo", "Nov-Feb"). */
function expand(list: string, names: string[]): Set<number> | null {
  const out = new Set<number>();
  for (const part of list.split(",")) {
    const [a, b] = part.split("-");
    const i = names.indexOf(a);
    const j = b === undefined ? i : names.indexOf(b);
    if (i < 0 || j < 0) return null;
    for (let k = i; ; k = (k + 1) % names.length) {
      out.add(k);
      if (k === j) break;
    }
  }
  return out;
}

const minutes = (hhmm: string) => {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
};

/** Reglas del horario, o null si no se entiende. */
export function parseHours(spec: string): Rule[] | null {
  if (spec.trim() === "24/7") return [{ spans: [[0, 24 * 60]] }];
  const rules: Rule[] = [];
  for (const raw of spec.split(";").map((r) => r.trim()).filter(Boolean)) {
    const tokens = raw.split(" ");
    const rule: Rule = { spans: [] };
    if (tokens.length > 1 && /^[A-Z][a-z]{2}\b/.test(tokens[0])) {
      const months = expand(tokens.shift()!, MONTHS);
      if (!months) return null;
      rule.months = months;
    }
    if (tokens.length > 1) {
      const list = tokens.shift()!;
      const withoutPH = list
        .split(",")
        .filter((d) => d !== "PH")
        .join(",");
      if (!withoutPH) continue; // regla solo de festivos
      const days = expand(withoutPH, DAYS);
      if (!days) return null;
      rule.days = days;
    }
    if (tokens.length !== 1) return null;
    const times = tokens[0];
    if (times !== "off" && times !== "closed") {
      for (const span of times.split(",")) {
        const m = /^(\d\d:\d\d)-(\d\d:\d\d)$/.exec(span);
        if (!m) return null;
        const start = minutes(m[1]);
        let end = minutes(m[2]);
        if (end <= start) end += 24 * 60; // pasa de medianoche ("18:00-00:00", "20:00-02:00")
        rule.spans.push([start, end]);
      }
    }
    rules.push(rule);
  }
  return rules.length ? rules : null;
}

/** Día de la semana (0 = lunes), mes (0 = enero) y minuto del día en la zona horaria dada. */
export function localParts(date: Date, timeZone?: string): { day: number; month: number; minute: number } {
  if (!timeZone) {
    return { day: (date.getDay() + 6) % 7, month: date.getMonth(), minute: date.getHours() * 60 + date.getMinutes() };
  }
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    weekday: "short",
    month: "numeric",
    hour: "numeric",
    minute: "numeric",
    hourCycle: "h23",
  }).formatToParts(date);
  const get = (t: string) => parts.find((p) => p.type === t)?.value ?? "";
  const day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].indexOf(get("weekday"));
  return { day, month: Number(get("month")) - 1, minute: (Number(get("hour")) % 24) * 60 + Number(get("minute")) };
}

/** Franjas del día (en minutos) según las reglas: la última regla que se aplica manda. */
function spansFor(rules: Rule[], day: number, month: number): [number, number][] {
  let spans: [number, number][] = [];
  for (const r of rules) {
    if (r.months && !r.months.has(month)) continue;
    if (r.days && !r.days.has(day)) continue;
    spans = r.spans;
  }
  return spans;
}

const hhmm = (m: number) => `${String(Math.floor(m / 60) % 24).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;

export type HoursState =
  /** Abierto; cierra a `closesAt` ("HH:MM"). `allDay`: no cierra hoy. */
  | { open: true; closesAt: string; allDay: boolean }
  /** Cerrado; abre hoy a `opensAt`, o no vuelve a abrir hoy. */
  | { open: false; opensAt?: string };

/** ¿Está abierto ahora? null si el horario no se entiende. */
export function hoursAt(spec: string, date: Date, timeZone?: string): HoursState | null {
  const rules = parseHours(spec);
  if (!rules) return null;
  const { day, month, minute } = localParts(date, timeZone);
  // lo que sigue abierto de ayer pasada la medianoche
  const yesterday = spansFor(rules, (day + 6) % 7, month).filter(([, e]) => e > 24 * 60);
  for (const [, e] of yesterday) if (minute < e - 24 * 60) return { open: true, closesAt: hhmm(e), allDay: false };
  const today = spansFor(rules, day, month);
  for (const [s, e] of today) {
    if (minute >= s && minute < e) return { open: true, closesAt: hhmm(e), allDay: s === 0 && e >= 24 * 60 };
  }
  const next = today.map(([s]) => s).filter((s) => s > minute).sort((a, b) => a - b)[0];
  return { open: false, opensAt: next === undefined ? undefined : hhmm(next) };
}
