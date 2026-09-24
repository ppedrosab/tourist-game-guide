# Cádiz · «El cartelón que se llevó el levante» (ruta de fiestas: Carnaval)

Tercera ruta del pack de Cádiz y primera de **fiestas** (`"theme": "fiestas"`): en la interfaz lleva
la seña morada con antifaz «Fiestas» / «Festivals», y los datos se rotulan «Tradición».
Formato de caso de detective: «ramificar y reunir», dos decisiones y cuatro finales.

## Narrador en romance

El guía es **el Romancero** y **todo lo que dice va en romance**: estrofas de cuatro octosílabos con
rima en los versos pares, como los romanceros del Carnaval, que recitan señalando las viñetas de su
cartelón con un puntero. En inglés, cuartetas con rima en los pares. El resto de personajes habla
en prosa.

## El caso

Anoche, cantando en Puertas de Tierra, el levante le voló al Romancero las viñetas del cartelón.
**Sospechosos** (cada pista del cuaderno empieza por el suyo): **el Chirigotero** (llevaba una viñeta
«pa' inspirarse» y ya tenía un cuplé del suceso), **el Cuartetero** (ensaya una parodia de «un
romancero sin cartelón») y **el levante** (las viñetas aparecen cada vez más al este: en la batea de
un coro, en los ficus de Mina…). Veredicto: el levante.

## Personajes (ninguno repite de otras rutas)

| id | Quién | Papel |
| --- | --- | --- |
| `romancero` (guía) | Levita verde, chistera con clavel, cartelón y puntero | Narra en romance |
| `chirigotero` | Bombín, peluca naranja, chaqueta de rayas, pito | Coguía del camino de La Viña; sospechoso |
| `comparsista` | Tricornio con pluma, gola, capa morada, media cara pintada | Coguía del camino de las plazas |
| `corista` | Canotier, traje blanco, fajín rojo, bandurria | Carrusel de coros |
| `cuartetero` | Chaqueta de cuadros, gorra, pajarita, claves | Sospechoso |

**María la Hierbabuena** (María del Carmen Llovet, 1935?-2016) es una persona real: aparece solo
como **homenaje** en la parada de su calle (tramo de la calle Sacramento detrás del Falla, rotulado
en 2023). No se la dibuja ni se le ponen diálogos. El reto es completar su grito: «¡Ole, ole mi Caí!
Lo digo a boca llena. Y quien no diga ole, que se le seque la hierbabuena. ¡Ole, ole y ole!».

## Caminos y finales

Huecos: `dinero` (mar) = **La Viña**; `poder` (arcilla) = **Las plazas**.

| Decisión 1 (calle María la Hierbabuena) | Decisión 2 (Catedral) | Final |
| --- | --- | --- |
| `camino_vina` | `version_pasodoble` | Poeta de La Viña |
| `camino_vina` | `version_cuple` | Ilegal de La Viña |
| `camino_plazas` | `version_pasodoble` | Comparsista del Falla |
| `camino_plazas` | `version_cuple` | Pregonero del Carnaval |

## Paradas

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| c1 | Gran Teatro Falla | El Concurso y sus cuatro modalidades; romanceros en la calle | Antifaz |
| c2 | Calle María la Hierbabuena | Homenaje · **decisión 1** | La hierbabuena de María |
| ca1 (Viña) | Barrio de La Viña (Cuartetero) | Ilegales; cuartetos y parodia | Las claves |
| ca2 (Viña) | Plaza de Abastos (Corista) | Carrusel de coros y bateas | La batea |
| cb1 (plazas) | Plaza de San Antonio (Cuartetero) | El pregón; el repertorio | El pregón |
| cb2 (plazas) | Plaza de Mina (Corista) | Carrusel de coros; instrumentos del coro | La bandurria |
| c4 | Plaza de la Catedral | La Bruja Piti · **decisión 2** (pasodoble o cuplé) | — |
| c5 | Puertas de Tierra | Entrada por tierra; la última viñeta; foto | — |
| c6 / c7 | Veredicto y cierre en romance («la voluntad… ¡y a otra parte!») | | El cartelón |

Escenas nuevas: `cadiz_{falla,sacramento,coros,puertas}`; reutiliza `cadiz_{vina,sanantonio,mina,catedral}`.

## Datos (verificar antes de publicar)

- Concurso Oficial en el Falla: comparsas, chirigotas, coros y cuartetos; romanceros con concurso propio en la calle.
- Romancero: octosílabos con rima en los pares, cartelón, puntero, libretos y «la voluntad».
- Cuartetos: de 3 a 5 componentes, claves, pitos, a veces guitarra; su fuerte es la parodia.
- Coros: guitarras, bandurrias y laúdes; carrusel de coros el domingo desde la Plaza de Abastos y
  la Plaza de Mina, en bateas tiradas por tractor.
- Pregón: se suele dar en la Plaza de San Antonio (confirmar el lugar de cada año).
- Bruja Piti: la quema cierra el Carnaval; ha sido en La Caleta, en la Plaza de la Catedral y, en
  2026, en Puertas de Tierra.
- Gran Teatro Falla, neomudéjar, inaugurado en 1905.
- Coordenadas de la calle María la Hierbabuena y del Falla: estimadas.

## Pendiente

- Segunda ruta de fiestas: **Semana Santa** (cargadores, manigueteros, Nazareno de Santa María,
  Buena Muerte), con personajes propios y tono respetuoso.
