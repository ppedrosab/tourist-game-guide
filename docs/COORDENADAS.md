# Revisión de coordenadas de las paradas

Generado con `npm run check:stops`: cada parada se busca por «título, ciudad» en OSM y en
Wikidata (fuentes independientes). Entre paréntesis, la distancia a la coordenada del pack.

- **Bien** (138 de 183): al menos una fuente la sitúa a menos de 80 m.
- **Probable error** (2): las dos fuentes coinciden entre sí y el pack queda lejos.
- **Revisar a mano** (43): no se encuentra o las fuentes no coinciden. Muchas son paradas
  con nombre genérico o puntos elegidos a propósito (una esquina, un mirador): no son errores seguros.

Al mover una parada, regenerar los trazados (`npm run gen:paths`).

## Probable error

| Ciudad | Parada | Ruta | Pack (lat, lng) | OSM | Wikidata | Propuesta |
|---|---|---|---|---|---|---|
| Almería | Barrio de la Chanca | `desierto-huerta` | 36.83880, -2.47480 | 36.84001, -2.47582 (162 m) · Biblioteca Pública Municipal del Barrio de La Chanca | 36.84005, -2.47578 (164 m) · Biblioteca Pública Municipal del Barrio de La Chanca | 36.84003, -2.47580 |
| Sevilla | Real Alcázar | `donde-esta-colon` | 37.38360, -5.99150 | 37.38321, -5.99018 (124 m) · Real Alcázar de Sevilla | 37.38339, -5.99040 (100 m) · Jardines del Real Alcázar de Sevilla | 37.38330, -5.99029 |

## Revisar a mano

| Ciudad | Parada | Ruta | Pack (lat, lng) | OSM | Wikidata |
|---|---|---|---|---|---|
| Almería | Aljibes de Jayrán | `atalaya` | 36.84210, -2.46360 | — | — |
| Almería | Barrio de La Chanca | `tesoro-alcazaba` | 36.83880, -2.47480 | — | 36.84005, -2.47578 (164 m) · Biblioteca Pública Municipal del Barrio de La Chanca |
| Almería | Cable Inglés | `desierto-huerta` | 36.83310, -2.46280 | 36.83381, -2.45825 (413 m) · Cable Inglés | — |
| Almería | Cerro de San Cristóbal | `cine-almeria` | 36.84272, -2.46828 | 36.84091, -2.47135 (339 m) · Conjunto Monumental la Alcazaba de Almería | 36.84397, -2.47143 (313 m) · Cerro de San Cristóbal |
| Almería | Muralla de Jayrán | `atalaya` | 36.84300, -2.46920 | 36.84228, -2.47031 (127 m) · Muralla de Jayrán | — |
| Almería | Parque de Nicolás Salmerón | `atalaya` | 36.83660, -2.46600 | — | 36.83685, -2.47030 (384 m) · Parque Nicolás Salmerón |
| Almería | Paseo de Almería | `feria-virgen-mar` | 36.84167, -2.46451 | — | 36.83791, -2.46330 (432 m) · Paseo de Almería |
| Almería | Plaza Vieja | `atalaya` | 36.84100, -2.46600 | — | — |
| Almería | Puerto | `cine-almeria` | 36.83490, -2.46400 | 36.83153, -2.47663 (1186 m) · Puerto de Almería | 36.83368, -2.46690 (292 m) · Puerto de Almería |
| Almería | Santuario de la Virgen del Mar | `feria-virgen-mar` | 36.83910, -2.46490 | — | — |
| Cádiz | Barrio de La Viña | `el-recetario-perdido` | 36.53190, -6.30320 | — | 36.53013, -6.30344 (199 m) · Barrio de La Viña |
| Cádiz | Gran Teatro Falla | `el-cartelon-y-el-levante` | 36.53410, -6.30370 | — | — |
| Cádiz | Iglesia de la Palma | `sobre-los-hombros` | 36.53160, -6.30400 | — | — |
| Cádiz | La Caleta | `la-ciudad-que-no-cayo` | 36.53270, -6.30600 | — | 36.53333, -6.30000 (541 m) · La Caleta |
| Cádiz | Mercado Central | `la-ciudad-que-no-cayo` | 36.53380, -6.30000 | — | — |
| Cádiz | Plaza de Abastos | `el-cartelon-y-el-levante` | 36.53380, -6.30000 | — | — |
| Cádiz | Plaza del Palillero | `sobre-los-hombros` | 36.53460, -6.29380 | — | — |
| Córdoba | Alcázar de los Reyes Cristianos | `biblioteca-del-califa` | 37.87660, -4.78330 | 37.87523, -4.78306 (154 m) · Alcázar de los Reyes Cristianos | 37.87660, -4.78138 (169 m) · Alcázar de los Reyes Cristianos |
| Córdoba | Cruz de mayo en San Andrés | `mayo-cordobes` | 37.88580, -4.77310 | — | — |
| Córdoba | El Arenal | `mayo-cordobes` | 37.87120, -4.76690 | 37.87322, -4.76604 (237 m) · El Arenal | 37.87456, -4.77050 (490 m) · Puente del Arenal |
| Córdoba | Plaza de Colón | `malmuerta` | 37.88900, -4.77720 | 37.89099, -4.77887 (266 m) · Plaza de Colón | 37.89000, -4.77853 (161 m) · Plaza de Colón |
| Córdoba | Plaza de Santa Marina | `tomate-salmorejo` | 37.88890, -4.77720 | — | — |
| Granada | Carrera del Darro | `libros-plomo` | 37.17795, -3.59370 | 37.17858, -3.59199 (167 m) · Calle Carrera del Darro | 37.17828, -3.59288 (82 m) · carrera del Darro |
| Granada | Cuevas del Sacromonte | `libros-plomo` | 37.18158, -3.58511 | 37.18121, -3.58819 (276 m) · Cuevas Los Tarantos | 37.18201, -3.58401 (108 m) · Museo Cuevas del Sacromonte |
| Granada | Paseo de los Tristes | `abencerrajes` | 37.17920, -3.59050 | — | 37.17891, -3.58935 (107 m) · Paseo de los Tristes |
| Granada | San Juan de los Reyes | `libros-plomo` | 37.17993, -3.59182 | 37.17848, -3.59432 (275 m) · Calle San Juan de los Reyes | 37.17950, -3.59268 (90 m) · calle San Juan de los Reyes |
| Granada | Torre Turpiana (catedral) | `libros-plomo` | 37.17650, -3.59950 | — | — |
| Huelva | Antigua Estación de Sevilla | `decano` | 37.25540, -6.94910 | — | — |
| Huelva | Iglesia de San Pedro | `choqueros` | 37.26060, -6.95140 | — | 37.26010, -6.95070 (84 m) · Iglesia de San Pedro Apóstol |
| Huelva | Mirador de la Cinta | `promesa-cinta` | 37.27558, -6.94403 | — | — |
| Huelva | Mirador del Conquero | `promesa-cinta` | 37.26742, -6.94847 | — | — |
| Huelva | Muelle de Levante | `choqueros` | 37.25300, -6.94420 | — | — |
| Huelva | Muelle del Tinto | `decano` | 37.25230, -6.95690 | — | — |
| Huelva | Parque Moret | `promesa-cinta` | 37.27000, -6.94040 | 37.27345, -6.93964 (389 m) · Parque Moret | 37.27194, -6.94417 (398 m) · Parque Moret |
| Huelva | Paseo de la Ría | `colombinas` | 37.25000, -6.95850 | — | 37.24690, -6.95651 (387 m) · Paseo de la Ría |
| Huelva | Santuario de la Cinta | `promesa-cinta` | 37.27798, -6.94437 | — | — |
| Jaén | Basílica de San Ildefonso | `lagarto-malena` | 37.76440, -3.78620 | — | — |
| Málaga | Alcazaba | `feria-agosto` | 36.72100, -4.41550 | — | 36.72176, -4.41484 (103 m) · Túnel de la Alcazaba |
| Málaga | El banco de Picasso | `picasso` | 36.72361, -4.41764 | — | — |
| Málaga | La Manquita | `misterio-manquita` | 36.72010, -4.41920 | — | — |
| Málaga | La estatua del Cenachero | `misterio-manquita` | 36.71880, -4.41960 | — | — |
| Málaga | Playa de la Malagueta | `espeto` | 36.71950, -4.40900 | 36.71644, -4.41094 (382 m) · Playa de La Malagueta | 36.71720, -4.40981 (266 m) · Playa de La Malagueta |
| Sevilla | Puente de Triana | `donde-esta-colon` | 37.38560, -6.00300 | 37.38628, -6.00243 (91 m) · Puente de Isabel II | — |
