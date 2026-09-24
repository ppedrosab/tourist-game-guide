/**
 * Posición del sol (algoritmo simplificado de la NOAA, error < 1°) y sombra
 * proyectada del personaje a partir de ella. Puro y testeable.
 */
export type SunPosition = { elevation: number; azimuth: number };

const rad = (d: number) => (d * Math.PI) / 180;
const deg = (r: number) => (r * 180) / Math.PI;

/** Elevación y azimut (grados; azimut desde el norte en sentido horario). */
export function sunPosition(date: Date, lat: number, lng: number): SunPosition {
  const jd = date.getTime() / 86400000 + 2440587.5;
  const t = (jd - 2451545) / 36525;
  const l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360;
  const m = 357.52911 + t * (35999.05029 - 0.0001537 * t);
  const e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t);
  const c =
    Math.sin(rad(m)) * (1.914602 - t * (0.004817 + 0.000014 * t)) +
    Math.sin(rad(2 * m)) * (0.019993 - 0.000101 * t) +
    Math.sin(rad(3 * m)) * 0.000289;
  const trueLong = l0 + c;
  const omega = 125.04 - 1934.136 * t;
  const lambda = trueLong - 0.00569 - 0.00478 * Math.sin(rad(omega));
  const eps0 = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60;
  const eps = eps0 + 0.00256 * Math.cos(rad(omega));
  const decl = deg(Math.asin(Math.sin(rad(eps)) * Math.sin(rad(lambda))));
  const y = Math.tan(rad(eps / 2)) ** 2;
  const eqTime =
    4 *
    deg(
      y * Math.sin(2 * rad(l0)) -
        2 * e * Math.sin(rad(m)) +
        4 * e * y * Math.sin(rad(m)) * Math.cos(2 * rad(l0)) -
        0.5 * y * y * Math.sin(4 * rad(l0)) -
        1.25 * e * e * Math.sin(2 * rad(m)),
    );
  const minutes = date.getUTCHours() * 60 + date.getUTCMinutes() + date.getUTCSeconds() / 60;
  const trueSolar = (((minutes + eqTime + 4 * lng) % 1440) + 1440) % 1440;
  const hourAngle = trueSolar / 4 < 0 ? trueSolar / 4 + 180 : trueSolar / 4 - 180;
  const cosZenith =
    Math.sin(rad(lat)) * Math.sin(rad(decl)) + Math.cos(rad(lat)) * Math.cos(rad(decl)) * Math.cos(rad(hourAngle));
  const zenith = deg(Math.acos(Math.max(-1, Math.min(1, cosZenith))));
  const azDen = Math.cos(rad(lat)) * Math.sin(rad(zenith));
  let azimuth: number;
  if (Math.abs(azDen) < 1e-6) azimuth = lat > 0 ? 180 : 0;
  else {
    const cosAz = (Math.sin(rad(lat)) * Math.cos(rad(zenith)) - Math.sin(rad(decl))) / azDen;
    const a = deg(Math.acos(Math.max(-1, Math.min(1, cosAz))));
    azimuth = hourAngle > 0 ? (a + 180) % 360 : (540 - a) % 360;
  }
  return { elevation: 90 - zenith, azimuth };
}

export type CastShadow = {
  /** false de noche: solo queda la sombra de contacto. */
  visible: boolean;
  /** Longitud relativa a la altura del personaje (sol bajo = sombra larga). */
  length: number;
  /** Inclinación lateral en grados (skewX): la sombra cae al lado contrario del sol. */
  skewDeg: number;
  opacity: number;
};

/**
 * Sombra sobre el suelo de la escena. Convención: miramos la escena de cara al
 * norte con el sol a la espalda, así que la sombra se tiende hacia el fondo;
 * el sol del este (mañana) la lleva a la izquierda y el del oeste (tarde) a la
 * derecha.
 */
export function castShadow(sun: SunPosition): CastShadow {
  if (sun.elevation <= 2) return { visible: false, length: 0, skewDeg: 0, opacity: 0 };
  // Topes pensados para el encuadre: una sombra rasante real mediría varias veces
  // la altura del personaje y se saldría del escenario.
  const length = Math.min(Math.max(1 / Math.tan(rad(sun.elevation)), 0.25), 1.4);
  // Componente este-oeste del sol: +1 al este (sombra a la izquierda), -1 al oeste.
  const eastWest = Math.sin(rad(sun.azimuth));
  const skewDeg = Math.max(-35, Math.min(35, -eastWest * 38));
  // Con el sol muy bajo la sombra es más tenue (luz difusa).
  const opacity = 0.2 + 0.1 * Math.min(1, sun.elevation / 30);
  return { visible: true, length, skewDeg, opacity };
}
