import { TurboModuleRegistry } from "react-native";
import Constants from "expo-constants";
import { setHintGate } from "./hints";

type AdsModule = typeof import("react-native-google-mobile-ads");

/** Si el anuncio no carga (sin conexión, sin inventario), la pista se da igual tras esta espera. */
const OFFLINE_WAIT_MS = 20_000;
const LOAD_TIMEOUT_MS = 8_000;

/**
 * AdMob solo existe en builds con código nativo (desarrollo o tienda). En Expo Go no está y la
 * librería lanza al importarse, así que se carga bajo demanda tras comprobar el módulo nativo.
 */
function load(): AdsModule | undefined {
  if (!TurboModuleRegistry.get("RNGoogleMobileAdsModule")) return undefined;
  try {
    return require("react-native-google-mobile-ads") as AdsModule;
  } catch (e) {
    console.warn("[anuncios] AdMob no disponible", e);
    return undefined;
  }
}

const wait = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

/**
 * Prepara los anuncios con recompensa para las pistas: consentimiento (UMP de Google; en iOS, el aviso
 * de seguimiento), SDK y la puerta de pistas. Sin módulo nativo no hace nada y las pistas siguen gratis.
 * El bloque de anuncios sale de `extra.admob.rewardedUnitId` (app.json); sin él, el de pruebas de Google.
 */
export async function setupRewardedHints(): Promise<void> {
  const ads = load();
  if (!ads) return;
  let personalized = false;
  try {
    const info = await ads.AdsConsent.gatherConsent();
    if (!info.canRequestAds) return;
    const choices = await ads.AdsConsent.getUserChoices();
    personalized = choices.selectPersonalisedAds;
    try {
      const att = require("expo-tracking-transparency") as typeof import("expo-tracking-transparency");
      if ((await att.requestTrackingPermissionsAsync()).status !== "granted") personalized = false;
    } catch {
      // Android o sin el módulo: manda el consentimiento de UMP.
    }
    await ads.default().initialize();
  } catch (e) {
    console.warn("[anuncios] sin consentimiento o sin SDK", e);
    return;
  }
  const extra = Constants.expoConfig?.extra as { admob?: { rewardedUnitId?: string } } | undefined;
  const unitId = extra?.admob?.rewardedUnitId || ads.TestIds.REWARDED;

  setHintGate({
    kind: "ad",
    request: () =>
      new Promise<boolean>((resolve) => {
        const ad = ads.RewardedAd.createForAdRequest(unitId, { requestNonPersonalizedAdsOnly: !personalized });
        let earned = false;
        let settled = false;
        const unsubscribe: (() => void)[] = [];
        const finish = (ok: boolean) => {
          if (settled) return;
          settled = true;
          unsubscribe.forEach((u) => u());
          resolve(ok);
        };
        const fallback = () => {
          if (settled) return;
          // Sin anuncio no se castiga al jugador: la pista llega tras una espera.
          unsubscribe.forEach((u) => u());
          unsubscribe.length = 0;
          wait(OFFLINE_WAIT_MS).then(() => finish(true));
        };
        const timer = setTimeout(fallback, LOAD_TIMEOUT_MS);
        unsubscribe.push(() => clearTimeout(timer));
        unsubscribe.push(
          ad.addAdEventListener(ads.RewardedAdEventType.LOADED, () => {
            clearTimeout(timer);
            ad.show().catch(fallback);
          }),
          ad.addAdEventListener(ads.RewardedAdEventType.EARNED_REWARD, () => {
            earned = true;
          }),
          ad.addAdEventListener(ads.AdEventType.CLOSED, () => finish(earned)),
          ad.addAdEventListener(ads.AdEventType.ERROR, () => {
            clearTimeout(timer);
            fallback();
          }),
        );
        ad.load();
      }),
  });
}
