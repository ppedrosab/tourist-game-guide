# Granada · «¿Quién mató a los Abencerrajes?»

Primera ruta de Granada. Pack: `content/granada/abencerrajes.pack.json` (es + en). Caso de
detective, «ramificar y reunir», dos decisiones y cuatro finales.

## El caso

En la Sala de los Abencerrajes (Palacios Nazaríes) hay una fuente con manchas rojizas. La leyenda
dice que un sultán mandó degollar allí a los caballeros Abencerrajes y que las manchas son su sangre.

**Tres sospechosos**; cada pista del cuaderno empieza por el suyo:

| Sospechoso | Pistas |
| --- | --- |
| **El sultán** | Algunas crónicas culpan a Muley Hacén de varias muertes de Abencerrajes (Puerta de la Justicia) |
| **Los Zegríes** | Los linajes se disputaban el poder a muerte (Capilla Real) · la ciudad partida en bandos (San Nicolás) |
| **Nadie** | Leyendas de vecinos (Arco de las Pesas) · la moda de las historias de moros y caballeros (Carlos V) · la novela de 1595 · las manchas de óxido |

Veredicto: hubo enemistades y muertes reales, pero la matanza en esa sala viene de la novela de
Ginés Pérez de Hita (1595) y las manchas se atribuyen al óxido. Irving, que la popularizó, lo
reconoce con humor.

## Personajes

| id | Quién | Tono |
| --- | --- | --- |
| `irving` (guía) | Washington Irving (1783-1859), vivió en la Alhambra en 1829; *Cuentos de la Alhambra* (1832) | Elegante, curioso, novelero; trata de «usted» y admite que exageró |
| `leon` | Uno de los doce leones de la fuente del Patio de los Leones | Juguetón, cotilla, «grrr» |
| `boabdil` | Muhammad XII, último sultán nazarí; entregó Granada el 2 de enero de 1492 | Orgulloso y melancólico |

## Caminos y finales

Huecos del motor: `dinero` (color mar) = **Albaicín**; `poder` (arcilla, «la roja») = **Alhambra**.

| Decisión 1 (Capilla Real) | Decisión 2 (Paseo de los Tristes) | Final |
| --- | --- | --- |
| `camino_alhambra` | `version_manchas` | Caballero Abencerraje |
| `camino_alhambra` | `version_novela` | Cronista de la Alhambra |
| `camino_albaicin` | `version_manchas` | Químico de leyendas |
| `camino_albaicin` | `version_novela` | Cuentista de Irving |

## Paradas (coordenadas estimadas)

| Nodo | Lugar | Reto | Coleccionable |
| --- | --- | --- | --- |
| n1 | Plaza Isabel la Católica | Quiz: *Cuentos de la Alhambra* | La pluma de Irving |
| n2 | Capilla Real (exterior) | Quiz: 1492 · **decisión 1** | — |
| a1 (Albaicín) | Mirador de San Nicolás | Quiz: «la roja» | Atardecer en San Nicolás |
| a2 (Albaicín) | Arco de las Pesas (Plaza Larga) | Observa: las pesas | Las pesas del arco |
| b1 (Alhambra) | Puerta de la Justicia | Quiz: la mano | La mano y la llave |
| b2 (Alhambra) | Palacio de Carlos V | Quiz: patio redondo | La granada |
| n4 | Paseo de los Tristes (el León) | Foto con la Alhambra · **decisión 2** | El león de la fuente |
| n4a / n4b | (narrativos) La novela de 1595 / Las manchas | — | — |
| n5 | El Bañuelo | Quiz: tragaluces | — |
| n6 | Corral del Carbón | Quiz: alhóndiga | — |
| n6b / n7 | Veredicto y caso cerrado | Quiz final | Insignia |

La ruta no entra en los Palacios Nazaríes (entrada con hora); se recomienda visitarlos aparte.
Puerta de la Justicia y Palacio de Carlos V son de acceso libre (comprobar horarios del recinto).
Hay cuestas fuertes: dificultad «medium».

## Datos que se afirman (revisar con un historiador)

- Irving vivió en la Alhambra en 1829; *Cuentos de la Alhambra*, 1832.
- Monumento a las Capitulaciones de Santa Fe, Mariano Benlliure, 1892.
- Capilla Real 1505-1517; Reyes Católicos, Juana y Felipe el Hermoso.
- Boabdil entrega Granada el 2 de enero de 1492.
- Guerras civiles del final del reino: Albaicín y Alhambra con sultanes distintos.
- Arco de las Pesas, muralla del s. XI; pesas confiscadas a tenderos tramposos.
- Puerta de la Justicia, 1348; mano y llave. **Leyenda**: cuando la mano alcance la llave…
- Algunas crónicas culpan a Muley Hacén de muertes de Abencerrajes (redacción prudente: verificar).
- Palacio de Carlos V, 1527, Pedro Machuca, patio circular.
- Ginés Pérez de Hita, *Guerras civiles de Granada* (1595).
- Manchas de la fuente atribuidas al óxido de hierro; cúpula de mocárabes estrellada.
- **Leyendas**: la frase de Bill Clinton en San Nicolás; el nombre del Paseo de los Tristes.
- El Bañuelo, baños del s. XI; tragaluces estrellados.
- Corral del Carbón, alhóndiga nazarí del s. XIV, la mejor conservada; nombre por los carboneros.

## Pendientes

- Coordenadas, radios, tiempos a pie y cuestas en la calle.
- ¿Ruta gratuita? `isFree: true` provisional.
- Voces y revisión nativa del inglés.
