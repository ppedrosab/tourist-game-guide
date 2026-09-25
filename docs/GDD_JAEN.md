# Jaén · pack `content/jaen/jaen.pack.json`

Séptima ciudad. Dos rutas con el formato de caso de detective: tres sospechosos, «ramificar y
reunir», dos decisiones y cuatro finales.

## Ruta de historia · «¿Quién mató al lagarto de la Malena?»

**Caso:** cuenta la leyenda que un lagarto gigante vivía junto a la fuente de la Magdalena y
aterrorizaba Jaén. ¿Quién lo mató? **Sospechosos:** **el preso** (a cambio del indulto, con panes
y un zurrón de pólvora), **el pastor** (con una piel de cordero llena de yesca) y **la piel** (la de
un gran reptil que colgó durante siglos en San Ildefonso). **Veredicto: nadie**: no hay prueba de
ningún lagarto gigante; las versiones cambian, nadie lo vio y la piel era probablemente de un
caimán. La leyenda sí es real y muy querida (Tesoro del Patrimonio Cultural Inmaterial, 2009).
Tercera versión, la del caballero de la armadura de espejos, contada como «se cuenta».

| id | Personaje | Papel |
| --- | --- | --- |
| `lagarto` (guía) | El propio lagarto de la Malena, que no recuerda quién lo mató | Narra |
| `preso` | El preso de la versión del pan y la pólvora | Sospechoso |
| `pastor` | El pastor de la versión de la piel de cordero | Sospechoso |

Caminos: `dinero` (mar) = **El preso**; `poder` (arcilla) = **El pastor**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| n1 | Catedral (Vandelvira, s. XVI) | El caso; primera noticia escrita en 1628 | El farol |
| n2 | Arco de San Lorenzo | El preso · **decisión 1** | El arco de San Lorenzo |
| a1 (preso) | Basílica de San Ildefonso | Pan y pólvora; la piel colgada, luego tapada con un San Cristóbal | Los panes del preso |
| a2 (preso) | Plaza de la Constitución | Santo Reino (1246); el preso no estuvo allí | Las llaves del Santo Reino |
| b1 (pastor) | Baños árabes (s. XI) | La piel de cordero con yesca | El zurrón del pastor |
| b2 (pastor) | Plaza de San Juan | El caballero de los espejos (se cuenta); dragones en muchas ciudades | La armadura de espejos |
| n4 | Iglesia de la Magdalena (antigua mezquita) | **decisión 2**: la cueva (pastor) o la piel (preso) | — |
| n5 | Fuente del Lagarto, raudal de la Magdalena | **Veredicto** | La piel del caimán |
| n6 | Cierre | Indultado de honor · Cazador de caimanes · Guardián de la Malena · Cazador de leyendas | ¿Quién mató al lagarto…? |

## Ruta gastronómica · «¿Quién plantó el mar de olivos?»

`theme: "gastronomia"`. Nunca exige comer ni beber; no se nombra ningún bar.

**Caso:** Jaén es la mayor productora de aceite de oliva del mundo. **Sospechosos:** **los
romanos** (olivos en la Bética, pero mezclados con otros cultivos), **los andalusíes** (las
palabras aceite, aceituna y almazara) y **el siglo XIX** (desamortizaciones y mercado
internacional: expansión de 1830 a 1880 y en el siglo XX). **Veredicto: los agricultores de los
siglos XIX y XX.**

| id | Personaje | Papel |
| --- | --- | --- |
| `catadora` (guía) | Catadora de aceite, con su copa azul | Narra |
| `vareador` | Vareador de aceituna | Coguía |
| `molinero` | Molinero de almazara | Coguía |

Caminos: `dinero` (mar) = **La plaza**; `poder` (arcilla) = **Los baños**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Mercado de San Francisco | Aceite virgen extra; Jaén, primera productora | La aceituna |
| g2 | Plaza de Santa María | Vareo; olivos en la Bética · **decisión 1** | La vara del vareador |
| ga1 | Plaza de la Constitución | Pipirrana | La pipirrana |
| ga2 | Basílica de San Ildefonso | Andrajos; trigales arrancados para plantar olivos | Los andrajos |
| gb1 | Baños árabes | Az-zayt, az-zaytuna, almazara | La almazara |
| gb2 | Plaza de San Juan | Ochíos; el aceite se vende por el mundo | El ochío |
| g4 | Iglesia de la Magdalena | Olivos centenarios · **decisión 2**: el molino o el olivar | — |
| g5 | Raudal de la Magdalena | Tapas con la bebida · **veredicto** | La alcuza |
| g6 | Cierre | Maestro almazarero · Vareador de honor · Catador de palabras · Guardián del mar de olivos | ¿Quién plantó el mar de olivos? |

## Datos a verificar

- Fecha de 1628 como primera referencia escrita del lagarto; ubicación exacta de la piel en San
  Ildefonso y su identificación como caimán.
- Tamaño de los baños árabes («de los más grandes que se conservan en España»).
- Recorrido de la calle Maestra y del Arco de San Lorenzo; torre del reloj de San Juan.
- Periodización de la expansión del olivar (1830-1880) según la historiografía citada.
- Ingredientes de pipirrana, andrajos y ochíos (varían según pueblo y familia).
- Coordenadas y radios de todas las paradas (estimaciones). Algunas calles tienen cuesta.

## Fuentes consultadas

- Wikipedia: Lagarto de la Malena; Catedral de la Asunción (Jaén).
- Archivo Histórico Provincial de Jaén (Junta de Andalucía), «El Lagarto de la Magdalena y los
  dragones de la ciudad de Jaén».
- Andalucía.org, «Jaén y el Lagarto de la Malena».
- Editorial Universidad de Jaén, «El olivar en Jaén en los siglos XIX y XX: una trayectoria de éxito».
- Dialnet: L. Garrido González, «La industria giennense en el siglo XIX».
