# [Nombre de la app] · El misterio de la Manquita

Juego narrativo geolocalizado para recorrer Málaga a pie. Expo + React Native + TypeScript.

## Puesta en marcha

```bash
npm install
npx expo install --fix     # alinea las versiones de todas las dependencias con tu SDK de Expo
npx expo start             # pulsa "a" (Android), "i" (iOS) o escanea el QR con Expo Go
```

> `package.json` fija Expo SDK 54 y deja el resto en `*` para que `expo install --fix`
> elija las versiones compatibles. Si quieres el SDK más reciente:
> `npx expo install expo@latest && npx expo install --fix`.

## Subir a GitHub

1. Crea un repositorio **vacío** en GitHub (sin README ni .gitignore).
2. En la carpeta del proyecto:

```bash
git remote add origin https://github.com/TU_USUARIO/cenachero-app.git
git push -u origin main
```

El historial de commits ya viene hecho, una fase por commit.

## Estructura

```
app/                      rutas (expo-router)
  (tabs)/                 fuera de la ruta: Explorar, Mis rutas, Colección, Perfil
  bienvenida.tsx, permisos.tsx
  ciudad/[id].tsx
  ruta/[id]/index.tsx     detalle de la ruta
  ruta/[id]/jugar.tsx     modo ruta: HUD + escena + diálogo
  pausa.tsx, cuaderno.tsx modales accesibles desde el HUD
src/
  theme/                  tokens "Azulejo y sal" (color, tipografía, radios, sombras duras)
  components/ui/          Button3D, IconButton, Chip, Panel, DialogBox, ChoiceCard, Hud, TabBar…
  components/layout/      Screen, TopBar
  content/types.ts        esquema de los packs de contenido
content/malaga/           pack JSON de la ruta
assets/
  sprites/                24 SVG (3 personajes × 8 expresiones)
  backgrounds/svg/        8 fondos SVG optimizados
  backgrounds/layers/     capas WebP @2x/@3x para parallax
```

## Hoja de ruta

- [x] **Fase 1 · Base**: tema, componentes de juego, navegación en dos modos.
- [ ] **Fase 2 · Motor narrativo**: carga y validación del pack (zod), grafo de nodos, flags y variantes, progreso persistido.
- [ ] **Fase 3 · Escenas**: parallax con giroscopio, sprites con expresiones y lip-sync, audio y subtítulos.
- [ ] **Fase 4 · Geolocalización**: geofencing en segundo plano (máx. 20 regiones en iOS) y permisos reales.
- [ ] **Fase 5 · Mapa**: MapLibre con los dos caminos y descarga offline.
- [ ] **Fase 6 · Pulido**: colección, finales, guardado, pruebas en la calle.

## Notas de diseño

- La sombra dura se dibuja con `HardShadow` (una forma de tinta desplazada) porque
  `elevation` en Android no permite sombras sin desenfoque.
- Color por camino: `branchColors.dinero` (verde azulado) y `branchColors.poder` (terracota).
