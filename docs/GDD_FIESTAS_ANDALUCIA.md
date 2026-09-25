# Rutas de fiestas de Málaga, Sevilla, Granada, Córdoba, Huelva, Jaén y Almería

Siete rutas `theme: "fiestas"` (chip morado «Fiestas»), una por ciudad; Cádiz ya tenía Carnaval y
Semana Santa. Mismo formato de caso que el resto: tres sospechosos, dos decisiones y cuatro finales.
**Cada ruta tiene su propio reparto**, sin repetir personajes de otras rutas de la misma ciudad (lo
comprueba `allPacks.test.ts`). Arte:
- personajes en `scripts/art/andalucia_sprites.py`;
- coleccionables en `scripts/art/fiestas_andalucia_collectibles.py`;
- fondos nuevos en `scripts/art/fiestas_andalucia_scenes.py`.

Cuando una fiesta tiene raíz religiosa (Virgen del Mar, San Antón, Corpus, cruces de mayo), el tono
es respetuoso:
- se habla de «tradición» y de «se cuenta» (`legend: true`);
- **nunca se dibuja una imagen sagrada**: el santuario se ve por fuera y la cruz de mayo es una cruz de flores;
- no hay chistes sobre devociones.

Todas las rutas son `isFree: true` de forma provisional.

## Málaga · «¿Qué celebra la Feria de Agosto?» (`feria-agosto`)

**Sospechosos:**
- **la conquista**: los Reyes Católicos entraron en Málaga el 19 de agosto de 1487;
- **el verano**;
- **el centenario**: en 1887 la feria se relanzó a lo grande en plena crisis.

**Veredicto: la conquista.** El acta municipal de 1491 dispone celebrar cada año la entrada de los
reyes; el centenario de 1887 la relanzó.

| id | Personaje | Papel |
| --- | --- | --- |
| `cantaora` (guía) | Cantaora de malagueñas | Narra |
| `verdialero` | Violinista de una panda de verdiales | Coguía |
| `cochero` | Cochero de caballos | Coguía |

Caminos: `dinero` = **El mar**; `poder` = **La Alcazaba**.

| Nodo | Lugar | Coleccionable |
| --- | --- | --- |
| f1 | Plaza de la Constitución | El abanico |
| f2 | Calle Larios · **decisión 1** | El sombrero de verdiales |
| fa1 · fa2 | Muelle Uno · Malagueta | El coche de caballos · Los fuegos |
| fb1 · fb2 | Alcazaba (fondo nuevo) · Teatro Romano | El estandarte de 1487 · El acta de 1491 |
| f4 | Plaza de la Merced · **decisión 2** (verdiales / caballos) | — |
| f5 | La Manquita · **veredicto** | El farolillo |

## Sevilla · «¿Quién inventó la Feria de Abril?» (`feria-abril`)

**Sospechosos:**
- **los ganaderos**;
- **los forasteros**: José María de Ybarra (vasco) y Narciso Bonaplata (catalán), concejales que
  la propusieron en 1846;
- **las casetas**: las de recreo llegaron en 1848.

**Veredicto: los forasteros.** La primera feria fue el 18 de abril de 1847 en el Prado de San
Sebastián, con 19 casetas y unos 25 000 visitantes.

| id | Personaje | Papel |
| --- | --- | --- |
| `flamenca` (guía) | Sevillana con traje de volantes | Narra |
| `tratante` | Tratante de ganado del XIX | Coguía |
| `farolillero` | Hace los farolillos del real | Coguía |

Caminos: `dinero` = **El Prado**; `poder` = **El río**. Fondos nuevos: Prado, Plaza de España,
Fábrica de Tabacos y portada de la Feria (Los Remedios).

## Granada · «¿De dónde viene la Tarasca?» (`tarasca`)

**Sospechosos:** **Francia** (la leyenda de Tarascón y santa Marta), **Granada** y **la moda**.
**Veredicto: Francia.**
- La primera Tarasca documentada en Granada es de 1633; su forma actual es del siglo XIX.
- Cada año un diseñador viste su muñeca, y de ahí el dicho «vas peor vestida que la Tarasca».

| id | Personaje | Papel |
| --- | --- | --- |
| `cabezudo` (guía) | Lleva una cabeza de cartón en el Corpus | Narra |
| `modista` | Modista, experta en la muñeca | Coguía |
| `tamborilero` | Toca en el desfile de gigantes | Coguía |

Caminos: `dinero` = **La catedral**; `poder` = **El Darro**. Fondos nuevos: Plaza del Carmen
(ayuntamiento), Plaza de las Pasiegas y Plaza Nueva.

## Córdoba · «¿Cuál es la fiesta más antigua de mayo?» (`mayo-cordobes`)

**Sospechosos:** **las Cruces**, **los Patios** y **la Feria**. **Veredicto: la Feria.**
- Sancho IV concedió en 1284 el privilegio de una feria.
- En 1422 pasó a mayo.
- En 1665 se ligó a la Virgen de la Salud.
- El concurso de patios es de 1921.

| id | Personaje | Papel |
| --- | --- | --- |
| `crucera` (guía) | Monta la cruz de flores de su hermandad | Narra |
| `caballista` | Jinete de traje corto | Coguía |
| `pregonero` | Pregona la feria | Coguía |

Caminos: `dinero` = **Las cruces**; `poder` = **La feria antigua**. Fondos nuevos: cruz de mayo en
San Andrés, Puerta de Sevilla y El Arenal.

## Huelva · «¿Quién inventó las Colombinas?» (`colombinas`)

**Sospechosos:**
- **Colón**;
- **los Pinzón**: Martín Alonso capitaneó la Pinta y Vicente Yáñez, la Niña;
- **la Real Sociedad Colombina Onubense**: fundada en 1880, celebró ese verano el aniversario del
  3 de agosto.

**Veredicto: la Sociedad Colombina.** El IV Centenario de 1892 consolidó las fiestas.

| id | Personaje | Papel |
| --- | --- | --- |
| `grumete` (guía) | El más joven de la tripulación | Narra |
| `pinzon` | Martín Alonso Pinzón (1441-1493) | Sospechoso |
| `colombina` | Socia de la Sociedad Colombina | Coguía |

Caminos: `dinero` = **La ría**; `poder` = **La ciudad**. Fondo nuevo: Paseo de la Ría con la noria
de la feria.

## Jaén · «¿Por qué Jaén enciende lumbres por San Antón?» (`lumbres`)

**Sospechosos:** **el santo** (San Antonio Abad, 17 de enero), **el invierno** y **el olivo**.
**Veredicto: el olivo.**
- El santo pone la fecha: las lumbres se encienden la víspera, el 16.
- Las lumbres se alimentaban con la leña de la poda del olivo, que llega esas semanas.
- Alrededor del fuego se cantan melenchones.

| id | Personaje | Papel |
| --- | --- | --- |
| `melenchonera` (guía) | Canta melenchones | Narra |
| `podador` | Poda olivos | Coguía |
| `ganadero` | Lleva a bendecir a sus animales | Coguía |

Caminos: `dinero` = **El centro**; `poder` = **El Jaén antiguo**. Fondo nuevo: Plaza de San Juan de
noche, con la lumbre y el corro de melenchones.

## Almería · «¿Por qué la feria de Almería es en agosto?» (`feria-virgen-mar`)

**Sospechosos:** **la patrona**, **el verano** y **el puerto**. **Veredicto: la patrona.**
- La feria es «en honor a la Virgen del Mar», en torno al último domingo de agosto.
- La tradición cuenta que Andrés de Jaén, guarda de la torre de Torregarcía, encontró la imagen en
  la orilla en diciembre de 1502 (`legend: true`).
- Fue proclamada patrona en 1806.

| id | Personaje | Papel |
| --- | --- | --- |
| `bailaora` (guía) | Baila en la feria de día y de noche | Narra |
| `torrero` | Andrés de Jaén, guarda de Torregarcía (según la tradición) | Coguía, tono sereno |
| `cohetero` | Maestro pirotécnico | Coguía |

Caminos: `dinero` = **El puerto**; `poder` = **La patrona**. Fondo nuevo: fachada del santuario (antiguo
convento de Santo Domingo), sin la imagen.

## Datos a verificar antes de publicar

- **Málaga.** Fecha y texto del acta municipal de 1491 (Archivo Municipal), y el relato del
  relanzamiento de 1887.
- **Sevilla.**
  - Los datos de 1847: 19 casetas y 25 000 visitantes.
  - La autoría de Ybarra y Bonaplata.
  - Las casetas de 1848: Montpensier, el Ayuntamiento y el Casino.
  - Coordenadas de la portada: cambia de sitio según la feria.
- **Granada.**
  - Que 1633 sea la primera Tarasca documentada y que su forma actual sea del siglo XIX.
  - La costumbre del diseñador que viste la muñeca.
  - Que la feria del Corpus se celebre en Almanjáyar.
- **Córdoba.**
  - Los años 1284, 1422, 1665 y 1921.
  - Las coordenadas se corrigieron (antes estaban 1° de latitud por debajo); confirmarlas en la calle.
- **Huelva.**
  - La fecha de fundación de la Sociedad y que su primera celebración fuera en el verano de 1880.
  - Los años de la Casa Colón (hotel de la década de 1880).
  - El Trofeo Colombino desde 1965.
  - Ubicación exacta del recinto de la feria en el Paseo de la Ría.
- **Jaén.**
  - La relación de las lumbres con la leña de la poda es la explicación popular; confirmarla con un
    historiador local.
  - La carrera nocturna «desde los años ochenta».
  - La lumbre principal en la Plaza de San Juan.
- **Almería.**
  - Fechas de 1502 y 1806, y que la feria gire en torno al último domingo de agosto.
  - Revisar el tono de la parada del santuario con la hermandad o la parroquia.

## Fuentes consultadas

- Feria de Málaga: [Wikipedia](https://es.wikipedia.org/wiki/Feria_de_M%C3%A1laga), Archivo Municipal
  de Málaga (acta de 1491) y prensa local (101tv).
- Feria de Abril: [Wikipedia](https://es.wikipedia.org/wiki/Feria_de_Abril), [sevilla.org](https://www.sevilla.org)
  y National Geographic España.
- Tarasca de Granada: [Wikipedia](https://es.wikipedia.org/wiki/Tarasca) y Rincones de Granada.
- Mayo cordobés: [Feria de Córdoba en Wikipedia](https://es.wikipedia.org/wiki/Feria_de_Nuestra_Se%C3%B1ora_de_la_Salud),
  artencordoba.com y [Fiesta de los Patios](https://es.wikipedia.org/wiki/Fiesta_de_los_Patios_de_C%C3%B3rdoba).
- Colombinas: [Wikipedia](https://es.wikipedia.org/wiki/Fiestas_Colombinas) y Huelva24.
- San Antón en Jaén: [Wikipedia](https://es.wikipedia.org/wiki/Fiesta_de_San_Ant%C3%B3n_(Ja%C3%A9n)) y Jaén24h.
- Feria de Almería y Virgen del Mar: [Wikipedia](https://es.wikipedia.org/wiki/Virgen_del_Mar_(Almer%C3%ADa)) y El Debate.
