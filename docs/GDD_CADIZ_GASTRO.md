# Cádiz · «El recetario perdido» (ruta gastronómica)

Segunda ruta del pack de Cádiz y primera **gastronómica** (`"theme": "gastronomia"`): en la
interfaz lleva la seña dorada con cubiertos «Gastronomía» / «Food & drink». Mismo formato que las
de historia: caso de detective, «ramificar y reunir», dos decisiones y cuatro finales.

## El caso

La Tía Norica tiene que preparar la comida de Carnaval para su chirigota y ha perdido su recetario.
El jugador recorre Cádiz probando (si quiere) y aprendiendo cada plato para descubrir quién se lo
llevó. **Tres sospechosos**; cada pista del cuaderno empieza por el suyo:

| Sospechoso | Pistas |
| --- | --- |
| **El gato** | Espinas y huellas junto al puesto de pescado (mercado) · falta un chicharrón (San Francisco) |
| **La chirigota** | Una copla con la receta de las tortillitas (La Viña) · una copla nueva sobre un recetario perdido (fino) |
| **La Norica** | Se equivoca con los ingredientes (Mentidero) · lo lleva todo en el delantal (San Antonio) · se toca el delantal al hablar de manzanilla |

Veredicto: nadie se lo llevó; el recetario estaba en el bolsillo de su delantal.

## Personajes

`tia_norica` (guía), `magon` (en el mercado: atún y garum) y **`chirigotero`** (nuevo: cantante de
chirigota de La Viña, bombín, peluca naranja y pito de caña).

## Caminos y finales

Huecos del motor: `dinero` (mar) = **recetas del mar**; `poder` (arcilla) = **recetas de la tierra**.

| Decisión 1 (mercado) | Decisión 2 (Plaza de Mina) | Final |
| --- | --- | --- |
| `camino_mar` | `version_fino` | Almirante del pescaíto |
| `camino_mar` | `version_manzanilla` | Catador de la bahía |
| `camino_tierra` | `version_fino` | Maestro chicharronero |
| `camino_tierra` | `version_manzanilla` | Rey del tapeo |

## Paradas y platos

| Nodo | Lugar | Plato o bebida | Coleccionable |
| --- | --- | --- | --- |
| g1 | Plaza de las Flores | Pescaíto frito en cartucho, cazón en adobo («bienmesabe») | Cartucho de pescaíto |
| g2 | Mercado Central (Magón) | Atún rojo de almadraba, ronqueo, garum · **decisión 1** | — |
| ga1 (mar) | Barrio de La Viña | Erizos y ortiguillas; fiestas gastronómicas del Carnaval | Erizo |
| ga2 (mar) | Plaza del Mentidero | Tortillitas de camarones | Tortillita |
| gb1 (tierra) | Plaza de San Francisco | Chicharrones de Cádiz | Chicharrón con limón |
| gb2 (tierra) | Plaza de San Antonio | Papas aliñás | Papas aliñás |
| g4 | Plaza de Mina (Chirigotero) | Marco de Jerez · **decisión 2** | — |
| g4a / g4b | (narrativos) | Fino de Jerez (flor, criaderas y soleras) / manzanilla de Sanlúcar | — |
| g5 | Calle Ancha | Pan de Cádiz; tocino de cielo (**leyenda** de las yemas) | Pan de Cádiz |
| g6 / g7 | Plaza de San Juan de Dios | Veredicto y foto brindando | Recetario |

Escenas nuevas `cadiz_{flores,vina,mentidero,sanfrancisco,sanantonio,ancha}`; se reutilizan
`cadiz_mercado`, `cadiz_mina` y `cadiz_sanjuan`.

## Criterios

- **No hace falta beber alcohol**: lo dice la guía en la decisión del vino (hay mosto) y el brindis
  final es «con lo que quieras». Los retos se resuelven mirando o respondiendo, nunca comiendo.
- No se nombran bares ni comercios concretos (no es publicidad). Los platos se explican en genérico.
- Datos a revisar: ingredientes y costumbres (cazón «bienmesabe», ronqueo, ortiguillas, chicharrones,
  papas aliñás, tortillitas, Marco de Jerez, crianza biológica, manzanilla solo en Sanlúcar, pan de
  Cádiz). Las anécdotas dudosas van con `legend: true` (nombre del Mentidero, tocino de cielo).

## Pendientes

- Coordenadas y tiempos en la calle; temporada (erizos en invierno; atún de almadraba en primavera).
- ¿Gratis o de pago? `isFree: true` provisional.
- Revisión nativa del inglés (nombres de platos: se dejan en español con explicación).
