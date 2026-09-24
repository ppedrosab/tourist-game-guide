# Sevilla · «¿Dónde está Colón?»

Primera ruta de Sevilla. Pack: `content/sevilla/donde-esta-colon.pack.json` (es + en).
Mismo formato que Cádiz: caso de detective, «ramificar y reunir», dos decisiones y cuatro finales.

## El caso

En la catedral de Sevilla, cuatro heraldos llevan a hombros el ataúd de Cristóbal Colón. En Santo
Domingo, el Faro a Colón dice guardar los mismos huesos. Un almirante y dos tumbas: ¿dónde está?

El Aguador lo plantea con **tres sospechosos**; cada pista del cuaderno empieza por el suyo:

| Sospechoso | Pistas |
| --- | --- |
| **Sevilla** | Hernando, el hijo, enterrado en la catedral: sirve para comparar (catedral) · los restos volvieron por el Guadalquivir (Torre del Oro) |
| **Santo Domingo** | En 1795 se llevaron una caja sin nombre (Archivo) · la caja de plomo de 1877 con su nombre, sin analizar (prueba de la caja) |
| **Las dos** | Cinco viajes en cuatro siglos (Triana) · nadie apuntó qué huesos viajaban (Alcázar) · el ADN confirma Sevilla, pero solo una parte del esqueleto (prueba del ADN) |

Veredicto: en Sevilla hay restos de Colón confirmados por ADN, pero pocos; lo de Santo Domingo no
se ha comprobado. Lo más probable es que esté repartido. El juego no da por cierta ninguna versión
más allá de lo que dicen los estudios.

## Personajes

| id | Quién | Tono |
| --- | --- | --- |
| `aguador` (guía) | El aguador del cuadro de Velázquez (h. 1620, hoy en Apsley House, Londres) | Castizo, trata de «usted» al detective, sabe todos los chismes |
| `giraldillo` | La veleta de la Giralda (la Fe, de Bartolomé Morel, 1568) | Vanidoso, grandilocuente, «lo ve todo desde arriba» |
| `hernando` | Hernando Colón (1488-1539), hijo del Almirante y bibliófilo | Serio, erudito, algo pedante; su ADN es clave |

## Caminos y finales

Huecos del motor: `dinero` (color mar) = **Río**; `poder` (arcilla) = **Papeles**.

| Decisión 1 (catedral) | Decisión 2 (Plaza del Triunfo) | Final |
| --- | --- | --- |
| `camino_rio` | `version_adn` | Almirante del río |
| `camino_rio` | `version_caja` | Cazador de leyendas |
| `camino_papeles` | `version_adn` | Sabueso del Archivo |
| `camino_papeles` | `version_caja` | Cronista de Indias |

## Paradas (coordenadas estimadas)

| Nodo | Lugar | Reto | Coleccionable |
| --- | --- | --- | --- |
| n1 | Giralda (Plaza Virgen de los Reyes) | Quiz: fue alminar | Búcaro del Aguador |
| n2 | Catedral, Puerta del Príncipe | Quiz: los cuatro heraldos · **decisión 1** | — |
| a1 (río) | Torre del Oro | Quiz: defender el puerto | Torre del Oro |
| a2 (río) | Puente de Triana | Quiz: Isabel II | ¡Tierra! |
| b1 (papeles) | Archivo de Indias | Quiz: era una lonja | Legajo de Indias |
| b2 (papeles) | Real Alcázar, Puerta del León | Observa: el león del azulejo | El león del Alcázar |
| n4 | Plaza del Triunfo (el Giraldillo desde abajo) | Quiz: la Fe · **decisión 2** | — |
| n4a / n4b | (narrativos) La caja de 1877 / El ADN de 2006 | — | — |
| n5 | Callejón del Agua (Santa Cruz) | Quiz: la conducción al Alcázar | — |
| n6 | Monumento a Colón (Jardines de Murillo) | Foto con la carabela | La carabela |
| n6b | (narrativo) El veredicto | Quiz final | — |
| n7 | Caso cerrado | — | Insignia |

El camino del río es bastante más largo (~3 km en total) que el de los papeles (~1,5 km).

## Datos que se afirman (revisar con un historiador)

- Colón murió en Valladolid (1506); Cartuja de Sevilla (1509); Santo Domingo (h. 1544); La Habana
  (1795); de vuelta a Sevilla tras 1898, remontando el Guadalquivir.
- Sepulcro de Arturo Mélida, hecho para La Habana; heraldos de Castilla, León, Aragón y Navarra.
- Hernando Colón y su hermano Diego (tío de Hernando) enterrados en Sevilla; estudio de ADN de 2006
  (equipo de José Antonio Lorente, Universidad de Granada); en Sevilla solo hay una parte pequeña
  del esqueleto. Santo Domingo no ha permitido analizar sus restos.
- 1877: caja de plomo con inscripción en la catedral de Santo Domingo; hoy en el Faro a Colón.
  Santo Domingo sostiene que en 1795 se llevaron los restos de otro Colón.
- Giralda: alminar almohade de finales del s. XII, cuerpo de campanas de 1568; rampas interiores.
  **Leyenda**: el almuédano subía a caballo.
- Giraldillo: la Fe, bronce de Bartolomé Morel, 1568.
- Torre del Oro: almohade, h. 1220; museo naval. **Leyenda**: el origen del nombre.
- Triana: **leyenda** de Rodrigo de Triana (en Lepe lo reclaman). Magallanes y Elcano salen de
  Sevilla en 1519; la Victoria vuelve en 1522. Puente de Isabel II, 1852, el de hierro más antiguo
  conservado en España.
- Casa Lonja 1584-1598 (por los tratos en las gradas de la catedral); Archivo de Indias desde 1785.
- Casa de la Contratación en el Alcázar desde 1503. **Leyenda**: Colón en la Virgen de los Mareantes.
- Callejón del Agua: conducción que abastecía al Alcázar. Santa Cruz, antigua judería.
- Monumento a Colón de los Jardines de Murillo (1921): carabela, león de bronce; comprobar las
  inscripciones de las columnas.

## Pendientes

- Coordenadas, radios y tiempos a pie en la calle; el camino del río es largo.
- ¿Ruta gratuita? `isFree: true` provisional.
- Voces y revisión nativa del inglés.
