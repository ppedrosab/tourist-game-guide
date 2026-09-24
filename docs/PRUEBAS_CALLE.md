# Pruebas en la calle · El misterio de la Manquita

Guía para recorrer la ruta en Málaga y ajustar el pack con datos reales. Objetivo: que cada
escena empiece sola al llegar, ni antes ni después, y que los tiempos a pie sean ciertos.

## Antes de salir

- **Build de desarrollo** en el móvil (`npx expo run:ios` / `run:android` o EAS). En Expo Go no
  hay geofences en segundo plano ni callejero MapLibre.
- Permisos: ubicación **«siempre»** y notificaciones (pantalla de bienvenida → permisos).
- Perfil → **Modo prueba de campo** activado. **Modo demo desactivado** (si no, las llegadas
  simuladas no sirven como dato).
- Opcional: Perfil → descargar el mapa de Málaga y probar parte de la ruta en modo avión.
- Batería al 100 % y una batería externa: GPS + pantalla durante 90 min.
- Ideal: **dos personas y dos móviles distintos** (iOS y Android) haciendo la ruta a la vez.

## Durante el recorrido

En cada parada, mientras se espera la llegada, el panel muestra `GPS ±X m · a Y m · radio Z m`.

1. Camina con normalidad, **sin mirar la pantalla** los últimos 50 m, y anota si la escena
   empezó sola (debería vibrar o avisar si la app está en segundo plano).
2. Si al estar en el sitio correcto la escena no ha empezado en 20–30 s, pulsa **«Ya estoy
   aquí»** (aparece a los 60 s sin GPS). Esas llegadas manuales son las que dicen dónde está de
   verdad la parada.
3. Haz cada ruta con la app **en primer plano** y al menos una vez con el móvil **en el
   bolsillo** (segundo plano: geofences y notificación «¡Has llegado!»).
4. Recorre **los dos caminos** (dinero y poder) y **las dos versiones** de la Manquita.
5. Apunta a mano lo que el registro no ve: calles cortadas, obras, sombra de GPS entre
   edificios altos (calle Larios), aglomeraciones, lugares sin sitio para pararse.

Paradas que conviene mirar con cuidado:

| Parada | Qué comprobar |
| --- | --- |
| Estatua del Cenachero | Que no salte desde la parada del autobús de la Alameda. |
| Calle Larios | Calle estrecha y alta: precisión del GPS; ¿el punto está en el tramo correcto? |
| Mercado de Atarazanas | ¿Salta frente a la puerta nazarí o al otro lado del mercado? |
| Antigua Casa de Guardia | Radio 30 m: ¿llega a saltar? Permiso del local para el reto de la barra. |
| Plaza de la Constitución | Que no salte ya en calle Larios (están a ~120 m). |
| La Manquita | Reto «¿qué torre está sin terminar?»: desde la Plaza del Obispo se ve bien. |
| Teatro Romano | Horario de acceso; el reto de la Alcazaba se ve desde la calle. |
| Plaza de la Merced | Banco de Picasso: colas para la foto a según qué horas. |

## Después: leer el informe

Perfil → **Ver informe de campo**. Por cada parada:

- **Distancia al llegar**: mediana de a cuántos metros saltó. Si es cercana al radio, bien; si
  hubo muchas llegadas manuales, la coordenada está desplazada.
- **Precisión típica**: ± metros del GPS cerca de la parada.
- **Coordenada sugerida**: media de las llegadas manuales. Si el aviso dice «Coordenada
  desplazada» (> 25 m), sustituir `location` en el pack por la sugerida (revisándola en un mapa).
- **Radio sugerido**: cubre la precisión típica (percentil 90 + 15 m), entre 30 y 60 m. Cambiar
  `triggerRadiusM` en el pack.
- **Tiempo hasta llegar**: sirve para revisar `walkMin` en las decisiones y `nextHint`
  («Unos 8 minutos andando»), y `durationMin` de la ruta.

**Exportar informe** genera un JSON (informe + registro completo) para compartirlo. Contiene
coordenadas: tratarlo como dato interno y borrarlo tras usarlo (**Borrar registro**).

## Cambios en el pack

Todo se corrige en `content/malaga/misterio-manquita.pack.json`, sin tocar código:

- `location` y `triggerRadiusM` de cada parada.
- `walkMin` y `distanceM` de las decisiones; `nextHint` en español e inglés.
- `durationMin` y `distanceKm` de la ruta.

Después: `npm test` (valida el pack y que los 4 finales siguen siendo alcanzables) y subir la
`version` del pack para que los móviles vuelvan a descargar el mapa offline con los límites nuevos.
