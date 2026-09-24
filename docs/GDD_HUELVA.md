# Huelva · pack `content/huelva/huelva.pack.json`

Sexta ciudad. Dos rutas con el formato de caso de detective: tres sospechosos, «ramificar y
reunir», dos decisiones y cuatro finales.

## Ruta de historia · «¿Quién trajo el fútbol a España?»

**Caso:** Huelva presume del club más antiguo de España (el Recreativo, «el Decano», 1889), pero
la pelota ya rodaba antes. **Sospechosos:** **los mineros** (los británicos de la compañía Rio
Tinto, que jugaban en las minas desde la década de 1870), **los marineros** (jugaban en los
muelles, pero se iban) y **los estudiantes** (volvían de Inglaterra y fundaron clubes más tarde).
**Veredicto: los mineros**, es decir, los británicos de las minas, que acabaron fundando el club de
Huelva.

| id | Personaje | Papel |
| --- | --- | --- |
| `mackay` (guía) | El doctor William Alexander Mackay, médico escocés de la Rio Tinto (llegó en 1883). Persona real; trata de «usted». | Narra |
| `minero` | Minero de Riotinto (ficticio) | Sospechoso |
| `marinero` | Marinero de un vapor británico (ficticio) | Sospechoso |

Caminos: `dinero` (mar) = **El puerto**; `poder` (arcilla) = **Los barrios ingleses**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| n1 | Muelle del Tinto (1874-1876) | El caso; la compañía Rio Tinto (1873) | El Muelle del Tinto |
| n2 | Antigua Estación de Sevilla (1880) | El minero; fútbol en las minas · **decisión 1** | La locomotora de la mina |
| a1 (puerto) | Mercado del Carmen | Marineros británicos en los puertos | El ancla del vapor |
| a2 (puerto) | Plaza de las Monjas | Colón y Palos (1492); los estudiantes llegaron tarde | La carabela |
| b1 (barrios) | Museo de Huelva | Rueda romana de Riotinto; 5.000 años de minería | La rueda romana |
| b2 (barrios) | Barrio Obrero (1917-1929) | Barrio de la compañía | La casita inglesa |
| n4 | Casa Colón (Gran Hotel Colón, 1883) | Acta del Huelva Recreation Club (23-12-1889) · **decisión 2** | El balón de 1889 |
| n4a / n4b | El primer partido (1890) / Las minas (hacia 1874) | Nodos narrativos | — |
| n5 | Plaza de la Merced (catedral desde 1953) | **Veredicto** | — |
| n6 | Cierre | Capitán del Decano · Estibador del balón · Socio fundador · Minero del balón | ¿Quién trajo el fútbol…? |

## Ruta gastronómica · «¿Por qué nos llaman choqueros?»

`theme: "gastronomia"`. Nunca exige comer ni beber; no se nombra ningún bar.

**Caso:** a los de Huelva les llaman «choqueros». **Sospechosos:** **la ría** (el choco abundaba y
era comida diaria), **los vecinos** (el mote pudo empezar con retintín) y **la cocina** (la fama
del choco frito). **Veredicto: la ría**; el mote vino de fuera por eso y Huelva lo hizo orgullo.

| id | Personaje | Papel |
| --- | --- | --- |
| `choquera` (guía) | Pescadera del Mercado del Carmen | Narra |
| `fresera` | Cultiva fresas en Palos | Coguía |
| `cortador` | Cortador de jamón de la sierra de Aracena (Jabugo) | Coguía |

Caminos: `dinero` (mar) = **La ría**; `poder` (arcilla) = **El centro**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Mercado del Carmen | Choco = sepia; el caso | El choco |
| g2 | Muelle del Tinto | Ría del Tinto y el Odiel; fresas · **decisión 1** | La fresa |
| ga1 | Muelle de Levante | Gamba blanca; chocos a cubos | La gamba blanca |
| ga2 | Antigua Estación de Sevilla | Jamón de Jabugo, dehesa; el mote de fuera (se cuenta) | El jamón de la sierra |
| gb1 | Plaza de las Monjas | Fresas; motes de los pueblos | El mote |
| gb2 | Iglesia de San Pedro | Onuba; mojama y almadraba | La mojama |
| g4 | Plaza del Punto | Chocos con habas · **decisión 2**: la sartén o el mote | Chocos con habas |
| g5 | Casa Colón | Vinos del Condado (zalema); leyenda del vino en las carabelas · **veredicto** | — |
| g6 | Cierre | Choquero de honor · Pescador de la ría · Freidor de oro · Cronista de motes | ¿Por qué nos llaman choqueros? |

## Datos a verificar

- Fecha y lugar del primer partido entre clubes (marzo de 1890, contra británicos de Sevilla) y
  el resultado: las fuentes de Huelva y Sevilla no coinciden.
- Fútbol en Riotinto «hacia 1874» (fuentes del propio club y divulgación).
- Origen del apodo «choquero» y la versión del mote con retintín (va como «se cuenta»).
- Porcentaje de fresa española que produce Huelva (se dice «la gran mayoría»).
- Leyenda del vino del Condado en las carabelas de Colón (va como «se cuenta»).
- Coordenadas y radios de todas las paradas (estimaciones).

## Fuentes consultadas

- Web del Recreativo de Huelva: «Historia», «Hitos» e «Inicios de la práctica del fútbol en la
  provincia de Huelva (1874-1889)».
- Wikipedia: Real Club Recreativo de Huelva, William Alexander Mackay, Muelle de mineral de la
  compañía Riotinto, Casa Colón.
- Turismo de Huelva, «Ruta del legado británico» (Muelle, Barrio Reina Victoria, Casa Colón).
- Archivo Histórico Provincial de Huelva (Junta de Andalucía), sobre el Hotel Colón.
- Huelva24, «¿Sabes por qué a los onubenses se les conoce como choqueros?».
