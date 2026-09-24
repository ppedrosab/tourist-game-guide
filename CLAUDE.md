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
  partidos (sombra · cuerpo · cara · luz de borde; entre expresiones solo cambia `face`), audios de
  `assets/audio/**` y coleccionables de `assets/collectibles/*.svg` (medallones 120×124 con sombra
  dura; el `icon` del pack es "collectibles/x.svg"), todo por la ruta del pack. Regenerar al añadir
  capas, sprites, voces o coleccionables.
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

**Fase 6 hecha** (pulido):
- i18n: `src/i18n` (es/en tipados; `useI18n()` → `t` interfaz, `L` contenido del pack, formatos).
  Idioma "auto" (el del móvil) o elegido en Perfil. **Ningún texto de interfaz fijo en el código.**
  El pack de Málaga está en inglés; `missingTranslations` + test exigen packs completos.
- Estrellas: `runner.recordChallenge/starsFor` (quiz y observación, primer intento); final con
  estrellas y colección con la mejor puntuación por ruta.
- Analítica: `src/analytics` (eventos tipados, sin datos personales ni coordenadas, solo con
  consentimiento; desactivada por defecto). El proveedor se conecta con `setAnalyticsSink`.
- "Antes y ahora": paso `then_now` con `ThenNowPanel` (deslizador ilustración de época ↔ hoy). `now:
  "camera"` = cámara en directo solo si el jugador la enciende (no se captura nada); sin cámara, la
  ilustración actual de la escena. En web la cámara es `getUserMedia` propio (`LiveCamera.tsx`):
  el módulo web de expo-camera descarga un lector QR de un CDN al importarse.
- Prueba de campo: `src/field` (registro y análisis por parada: coordenada y radio sugeridos),
  pantalla `/campo` y guía `docs/PRUEBAS_CALLE.md`.

**Segunda ciudad: Cádiz** («La ciudad que no cayó», diseño y datos a verificar en `docs/GDD_CADIZ.md`):
- Pack `content/cadiz/la-ciudad-que-no-cayo.pack.json` (es/en), guía la Tía Norica, con la Pepa y
  Magón. Asedio francés de 1810-1812; caminos Mar y Ciudad, 4 finales, 6 coleccionables.
- Los huecos de camino siguen siendo `dinero` (color mar) y `poder` (arcilla), pero cada ruta los
  nombra con `route.branches` (`name` para leyendas, `trail` en frases); `useI18n().branch()`.
- `src/engine/__tests__/allPacks.test.ts` se aplica a todo pack de `BUNDLED_PACKS`: idiomas,
  sprites con 8 expresiones, capas por escena, arte de coleccionables y todos los finales alcanzables.
- Arte generado por código en `scripts/art/` (sprites, medallones y fondos SVG por capas);
  `render_layers.py` pasa cada grupo del SVG a WebP @2x/@3x (Chromium + Pillow). Tras cambiarlo:
  `python3 scripts/art/cadiz_scenes.py && python3 scripts/art/render_layers.py cadiz_ && npm run gen:assets`.

**Tercera ciudad: Sevilla** («¿Dónde está Colón?», diseño y datos a verificar en `docs/GDD_SEVILLA.md`):
- Pack `content/sevilla/donde-esta-colon.pack.json` (es/en). Guía el Aguador de Velázquez (trata
  de «usted» al jugador), con el Giraldillo y Hernando Colón. Dos tumbas (Sevilla y Santo Domingo) y
  tres sospechosos; caminos Río y Papeles; pruebas de la caja de 1877 y del ADN de 2006.
- Arte en `scripts/art/sevilla_*.py` (reutiliza las piezas de los generadores de Cádiz).

**Rutas gastronómicas** (`route.theme: "gastronomia"`; sin `theme` = historia):
- Llevan la seña `ThemeBadge` (chip dorado con cubiertos, «Gastronomía» / «Food & drink») en la
  ciudad, el detalle, Explorar, Pausa, Colección y el final; en Mis rutas va en el texto.
- Primera: Cádiz «El recetario perdido» (segunda ruta del pack de Cádiz; ver `docs/GDD_CADIZ_GASTRO.md`).
  Mismo formato de caso (tres sospechosos, dos decisiones, cuatro finales). Personajes propios, sin
  repetir los de historia: guías `pescaera` (mar) y `chicharronero` (tierra), y `garumero` (romano del garum). Nunca exigir comer ni beber para resolver un reto; nada de nombres de bares.

**Rutas de fiestas** (`route.theme: "fiestas"`: chip morado con antifaz «Fiestas»; los datos se rotulan «Tradición»):
- Cádiz «El cartelón que se llevó el levante» (Carnaval; ver `docs/GDD_CADIZ_CARNAVAL.md`). Guía el
  `romancero`, que **siempre habla en romance** (cuatro octosílabos, rima en los pares; el texto lleva
  saltos de línea). Con `chirigotero`, `comparsista`, `corista` y `cuartetero`. María la Hierbabuena
  es una persona real: solo homenaje en la parada de su calle, sin dibujarla ni ponerle diálogos.
- Cádiz «Sobre los hombros de Cádiz» (Semana Santa; ver `docs/GDD_CADIZ_SEMANA_SANTA.md`). Guía el
  `cargador`, con `maniguetero` y `saetera`; caminos Santa María y La Viña. Tono respetuoso: nada de
  chistes sobre imágenes ni hermandades y **no se dibujan imágenes sagradas** (pasos de palio vistos
  desde fuera, cirios y nazarenos anónimos). Fondos en `scripts/art/cadiz_ssanta_scenes.py`.

**Cuarta ciudad: Granada** («¿Quién mató a los Abencerrajes?», ver `docs/GDD_GRANADA.md`):
- Pack `content/granada/abencerrajes.pack.json` (es/en). Guía Washington Irving (de «usted»), con el
  León de la fuente y Boabdil. Tres sospechosos (el sultán, los Zegríes, nadie); caminos Albaicín y
  Alhambra; pruebas de la novela de 1595 y de las manchas de la fuente. No entra en los Palacios
  Nazaríes (entrada con hora). Arte en `scripts/art/granada_*.py`.
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
  campo.tsx               informe de la prueba de campo (desde Perfil)
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
src/i18n/                 es.ts, en.ts, useI18n
src/analytics/            eventos y sink enchufable
src/field/                prueba de campo: registro y análisis
scripts/gen-scene-assets  genera el manifiesto de capas, sprites y audios
content/malaga/           misterio-manquita.pack.json
content/cadiz/            la-ciudad-que-no-cayo.pack.json (historia, gastronomía, Carnaval y Semana Santa)
content/sevilla/          donde-esta-colon.pack.json
content/granada/          abencerrajes.pack.json
scripts/art/              generadores del arte de Cádiz y render de capas
assets/sprites/           {cenachero,manquita,lucio,norica,pepa,magon,chirigotero,pescaera,chicharronero,garumero,romancero,comparsista,corista,cuartetero,cargador,maniguetero,saetera,aguador,giraldillo,hernando,irving,leon,boabdil}/{id}_{expresion}.svg  (viewBox 200×260)
assets/collectibles/      {coleccionable}.svg (medallón viewBox 120×124, color del camino en el aro)
assets/then_now/          ilustraciones de época para "antes y ahora" (viewBox 390×560, misma
                          perspectiva que la escena de hoy para que el deslizador coincida)
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
- **6 · Pulido** (hecha, ver arriba). Siguiente: salir a la calle con `docs/PRUEBAS_CALLE.md`.

## Contenido e historia (resumen; completo en docs/GDD.md)

Misterio: ¿por qué la catedral de Málaga ("la Manquita") tiene una sola torre? Las obras se
pararon en 1782 por falta de fondos. Leyenda: el dinero ayudó a la independencia de EE. UU.
Documentos: se usó en el camino de Antequera. El juego presenta ambas; nunca afirma la leyenda
como hecho. Las anécdotas "se cuenta" van con `legend: true`.

## Pendientes fuera del código

- Verificar sobre el terreno coordenadas, radios y tiempos a pie (son estimaciones).
- Pedir permiso a la Antigua Casa de Guardia (el reto implica entrar al local).
- Revisión de un historiador local antes de grabar audios.
- Voces: decidir locutores reales o síntesis (y si también en inglés).
- Revisión de la traducción inglesa por un nativo.
- Elegir proveedor de analítica (y texto de privacidad) y de teselas para el mapa offline.
- Revisar con un historiador la ilustración de calle Larios en 1891 (`assets/then_now`).
- Cádiz: coordenadas y radios en la calle, revisión histórica de los datos de `docs/GDD_CADIZ.md`,
  decidir si la ruta es gratuita (`isFree: true` provisional) y un posible "antes y ahora".
- Sevilla: lo mismo con `docs/GDD_SEVILLA.md`; el camino del río es mucho más largo que el de los papeles.
- Granada: lo mismo con `docs/GDD_GRANADA.md`; cuestas fuertes y horarios del recinto de la Alhambra.

## Qué NO hacer

- No meter contenido de ciudad en el código: todo sale del pack.
- No escribir textos de interfaz sueltos: añadirlos a `src/i18n/es.ts` y `en.ts`.
- No usar colores o tamaños sueltos: usar `src/theme`.
- No usar `localStorage`/web-only APIs; es React Native.
- No añadir dependencias pesadas sin justificarlo en el commit.
