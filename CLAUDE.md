# CLAUDE.md · Contexto del proyecto

Lee este archivo entero antes de tocar código. El detalle del juego está en `docs/GDD.md`.

## Qué es

App móvil (iOS y Android) de **juego narrativo geolocalizado** para turistas: el jugador camina por
la ciudad, un personaje histórico le guía con diálogos y audio, resuelve retos y **toma decisiones
que le llevan por calles distintas** (narrativa ramificada tipo "elige tu propia aventura").
Primera ciudad: **Málaga**. Primera ruta (gratis): **"El misterio de la Manquita"**, guiada por
**Er Cenachero**. La app debe escalar a muchas ciudades: el código es un **motor genérico** y cada
ciudad es solo **contenido** (un pack JSON + assets).

- Nombre comercial de la app: pendiente → usar siempre `[Nombre de la app]`.
- Idioma de la interfaz y del código de producto: **español**. Comentarios en español.
- Plataforma: Expo + React Native + TypeScript estricto + expo-router.

## Comandos

```bash
npm install && npx expo install --fix   # primera vez: alinea versiones con el SDK de Expo
npx expo start                          # desarrollo
npm run typecheck                       # tsc --noEmit (debe quedar en 0 errores)
npm test                                # jest-expo: motor, cargador de packs, store y escenas
npm run gen:assets                      # regenerar src/scene/assets.generated.ts
npx expo start --web                    # probar en navegador (sin simulador)
```

Tras cada cambio relevante: `npm run typecheck` y probar en Expo Go o simulador.
Commits pequeños por tarea, mensajes en español con prefijo convencional (`feat(motor): …`).

## Estado actual

**Fase 1 hecha y verificada**: dependencias fijadas al SDK 54, typecheck en 0, bundles iOS/Android/web OK.

**Fase 2 hecha** (motor narrativo):
- `src/engine/schema.ts` + `loadPack.ts`: validación zod y de referencias; nunca lanza.
- `src/engine/catalog.ts`: packs incluidos (añadir ciudad = añadir su JSON aquí).
- `src/engine/runner.ts`: funciones puras (`advance`, `resolveText`, `routeStops`…). La pista y los
  coleccionables de un nodo se ganan al **completarlo** (salir de él), no al entrar.
- `src/engine/scene.ts`: pasos de un nodo para la pantalla de juego. `outline.ts`: ficha y progreso.
- `src/store/progress.ts`: zustand + AsyncStorage (funciona en Expo Go). Colección acumulada entre
  partidas y ajuste `demoMode` (activo por defecto solo en desarrollo, `__DEV__`).
- Todas las pantallas leen del pack y del store. Tests: los 4 finales son alcanzables.
- `babel.config.js` activa `unstable_transformImportMeta` (zustand usa `import.meta` en web).

**Fase 3 hecha** (escenas; probada en navegador, falta probar el giroscopio en dispositivo):
- `npm run gen:assets` → `src/scene/assets.generated.ts` (no editar): capas por escena, sprites
  partidos (sombra · cuerpo · cara · luz de borde; entre expresiones solo cambia `face`) y audios de
  `assets/audio/**` por la ruta del pack. Regenerar al añadir capas, sprites o voces.
- `src/scene/parallax.ts` (puro/worklet, con tests): profundidades cielo 0 · fondo 0.1 · medio/mar
  0.25 · primer plano 0.6 · fx fija. Inclinación con tanh (acotada), amplitud proporcional al
  escenario y **misma escala para todas las capas** (~8 %): nunca asoma un borde y en reposo se ve la
  composición original. Suavizado por dt y recentrado lento a la postura natural.
- `src/scene/SceneStage.tsx`: todo el parallax en el hilo de interfaz (sensor de reanimated →
  `useFrameCallback` → estilos). Personajes a la profundidad del primer plano (no "patinan"), por
  encima de fx. Congelado bajo modales/segundo plano, quieto con "Reducir movimiento". En web, el
  puntero hace de giroscopio.
- `cast.ts` (reparto por paso), `Sprite`/`CastLayer` (expresiones, lip-sync), `sun.ts` (sombra según
  el sol real de la parada), `useVoice` (expo-audio; sin audio simula la duración para el lip-sync).
- Pendiente de dispositivo: confirmar el sentido de roll/pitch del sensor en iOS y Android (si el
  parallax va "al revés", invertir el signo en `stepTilt`).

**Fase 4 hecha** (geolocalización; sin probar aún en dispositivo real):
- `src/engine/geo.ts` (puro, con tests): distancias, `isInside` con margen por precisión (máx. 20 m),
  `geofenceTargets` (nodo actual si no se ha llegado; si no, primeras paradas físicas de cada salida,
  máx. 20 por el límite de iOS) y `offerManualArrival` (60 s sin GPS → "Ya estoy aquí").
- La llegada se guarda en `PlayerProgress.arrivedAt` (runner `markArrived`/`hasArrived`).
- `src/hooks/useArrivalWatcher.ts`: GPS en primer plano mientras la escena espera.
- `src/geo/background.native.ts`: tarea de geofences (apunta llegadas en AsyncStorage y lanza la
  notificación "¡Has llegado!"); `GeofenceSync` en `_layout` sincroniza regiones y aplica llegadas.
  Web usa `background.ts`/`permissions.ts` sin segundo plano.
- La ubicación en segundo plano **no funciona en Expo Go (iOS)**: hace falta build de desarrollo
  (`npx expo run:ios` o EAS). En Expo Go funciona el GPS en primer plano.

**Fase 5 hecha** (mapa; el esquema SVG probado en navegador, MapLibre sin probar en dispositivo):
- `src/map/geometry.ts` (puro, con tests): paradas numeradas por el camino más largo (las ramas
  paralelas comparten número; la lista del detalle usa los mismos), tramos por camino con estado
  (recorrido / pendiente / otro camino), GeoJSON y proyector para el SVG.
- `RouteMap`: MapLibre (`@maplibre/maplibre-react-native`, estilo OpenFreeMap en `src/map/config.ts`)
  si la build tiene el módulo nativo; si no (Expo Go, web), `SchematicMap` en SVG. MapLibre se
  carga bajo demanda (`maplibre.native.ts`) porque al importarse sin módulo nativo lanza.
- Pantalla modal `/mapa` (desde Pausa y Cuaderno) y vista previa en el detalle de ruta.
- Offline: `offlinePlan.ts` (zona + 150 m, zooms 13–17, estimación de tamaño), `offline.ts`
  (paquetes de MapLibre por `metadata.id`, borra versiones viejas), `OfflineMapCard`.
- `src/geo/watchPosition(.web).ts`: en web se usa `navigator.geolocation` directamente (expo-location
  19 en web pierde las suscripciones a partir de la segunda).
- Antes de publicar: confirmar condiciones de OpenFreeMap para descargas offline o usar teselas
  propias (solo cambia `MAP_STYLE_URL`).

## Arquitectura

```
app/                      rutas (expo-router)
  _layout.tsx             carga fuentes, Stack raíz, modales
  (tabs)/                 Explorar (index), Mis rutas, Colección, Perfil → TabBar propia
  bienvenida.tsx, permisos.tsx
  ciudad/[id].tsx
  ruta/[id]/index.tsx     detalle de ruta
  ruta/[id]/jugar.tsx     MODO RUTA: escena + HUD + caja de diálogo (sin pestañas)
  pausa.tsx               modal transparente, vuelve al mismo punto
  cuaderno.tsx            modal: pistas, mapa, objetos
  mapa.tsx                modal: mapa de la ruta en curso
src/theme/                tokens (colores, radios, sombras, tipografía)
src/components/ui/        Button3D, IconButton, Chip, Panel(+Nameplate), DialogBox, ChoiceCard,
                          Hud, TabBar, HardShadow, AzulejoBackground, Icon
src/components/layout/    Screen, TopBar
src/components/game/      ChallengePanel, ArrivalPanel, CaseClosed
src/content/types.ts      ESQUEMA de los packs (fuente de verdad del contenido)
src/engine/               loadPack, schema, catalog, runner, scene, outline (+ __tests__)
src/store/progress.ts     progreso persistido
src/hooks/                useCurrentRun (modales), useArrivalWatcher (GPS en primer plano)
src/geo/                  geofences en segundo plano, permisos, GeofenceSync
src/scene/                SceneStage, parallax, cast, Sprite, CastLayer, sun, voice, assets.generated
src/map/                  geometry, RouteMap (MapLibre / SchematicMap), offline, OfflineMapCard
scripts/gen-scene-assets  genera el manifiesto de capas, sprites y audios
content/malaga/           misterio-manquita.pack.json
assets/sprites/           {cenachero,manquita,lucio}/{id}_{expresion}.svg  (viewBox 200×260)
assets/backgrounds/svg/   fondo_{parada}.svg (viewBox 390×560)
assets/backgrounds/layers bg_{parada}_{n}_{capa}@2x/@3x.webp  (capas para parallax)
```

Reglas de navegación (no romperlas):
1. **Fuera de la ruta** manda la barra de pestañas. **Dentro de la ruta** no hay pestañas: el HUD
   (pausa · progreso por paradas · cuaderno con contador) ocupa su lugar.
2. Pausa y Cuaderno son **modales** que siempre devuelven al punto exacto de la escena.
3. El progreso se guarda en cada nodo. Explorar muestra "Continuar" con la parada exacta.

## Sistema de diseño "Azulejo y sal" v2 (usar SIEMPRE los tokens de `src/theme`)

- Colores: ink `#1B2A3A` (contornos y texto) · clay `#A8431F` (acción, camino del poder) ·
  sea `#2F6F73` (secundario, camino del dinero) · peach `#F0A27F` (acento sobre oscuro) ·
  gold `#F2C14E` (logros) · paper `#FFF8EC` (paneles de juego) · cream `#F6EFE3` (fondo) ·
  sand `#EADFCB` (superficies suaves).
- **Color por camino**: `branchColors.dinero` = sea, `branchColors.poder` = clay. Se repite en
  mapa, decisiones, pistas, HUD y coleccionables. Nunca mezclarlos.
- Estilo de juego: contorno de tinta 2–3 px, **sombra dura** desplazada 3–4 px sin desenfoque
  (componente `HardShadow`; en Android `elevation` no sirve), radios 9/14/16/22, botones que
  "bajan" al pulsar, motivo de azulejo malagueño en fondos y cabeceras.
- Tipografía: Fraunces 700 (títulos) + DM Sans 400/500/700 (texto). Diálogos a 17 px.
- Caja de diálogo estilo novela visual: placa con el nombre del personaje, retrato opcional,
  texto, barra de audio con repetir y botón de avance. Los personajes quedan detrás de la caja.
- Accesibilidad: objetivos táctiles ≥ 44 px, `accessibilityRole/Label` en todo lo pulsable,
  subtítulos siempre disponibles.

## Motor narrativo (fase 2, hecha)

El pack es un **grafo** de `StoryNode` (ver `src/content/types.ts`):
- Nodo **con `location`** → espera al geofence (o al botón "Simular llegada" en modo demo).
- Nodo **sin `location`** → nodo narrativo: se lanza al terminar el anterior.
- `choices` con `setFlags` → decisiones; `variants` en diálogos → texto según flags
  (se elige la primera variante cuyos `requires` estén todos en los flags del jugador).
- `clue` añade una pista al cuaderno; `rewards` dan coleccionables; `endings` según flags.
- Estructura "ramificar y reunir": las ramas se reúnen en nodos cuello de botella.

Tareas de la fase 2:
1. `src/engine/loadPack.ts`: cargar el JSON y validarlo con **zod** (esquema espejo de types.ts).
   Validar además referencias: todo `nextNodeId`/`targetNodeId` existe, `startNodeId` existe,
   cada `characterId` existe. Errores claros, nunca crashear la app por un pack mal formado.
2. `src/engine/runner.ts`: funciones puras y testeables → `getNode`, `resolveText(block, flags)`,
   `availableChoices(node, flags)`, `advance(state, choice?)`, `resolveEnding(route, flags)`.
3. `src/store/progress.ts`: zustand + persistencia (MMKV o AsyncStorage) con `PlayerProgress`.
4. Conectar `ruta/[id]/jugar.tsx`, HUD, cuaderno, colección y "Continuar" al motor.
5. Modo demo: botón "Simular llegada" para jugar toda la ruta desde casa.
6. Tests unitarios del runner (jest-expo): los 4 finales deben ser alcanzables.

## Fases siguientes

- **3 · Escenas** (hecha, ver arriba). Se usó el sensor de reanimated en vez de expo-sensors para
  que el parallax no pase por el hilo de JS.
- **4 · Geolocalización** (hecha, ver arriba). Pendiente: probar en la calle con build de desarrollo.
- **5 · Mapa** (hecha, ver arriba). Mejora posible: trazado por calles (`path` opcional en el pack)
  en vez de líneas rectas entre paradas.
- **6 · Pulido**: colección, finales, i18n (inglés), analítica, pruebas en la calle.

## Contenido e historia (resumen; completo en docs/GDD.md)

Misterio: ¿por qué la catedral de Málaga ("la Manquita") tiene una sola torre? Las obras se
pararon en 1782 por falta de fondos. Leyenda: el dinero ayudó a la independencia de EE. UU.
Documentos: se usó en el camino de Antequera. El juego presenta ambas; nunca afirma la leyenda
como hecho. Las anécdotas "se cuenta" van con `legend: true`.

## Pendientes fuera del código

- Verificar sobre el terreno coordenadas, radios y tiempos a pie (son estimaciones).
- Pedir permiso a la Antigua Casa de Guardia (el reto implica entrar al local).
- Revisión de un historiador local antes de grabar audios.
- Voces: decidir locutores reales o síntesis.

## Qué NO hacer

- No meter contenido de ciudad en el código: todo sale del pack.
- No usar colores o tamaños sueltos: usar `src/theme`.
- No usar `localStorage`/web-only APIs; es React Native.
- No añadir dependencias pesadas sin justificarlo en el commit.
