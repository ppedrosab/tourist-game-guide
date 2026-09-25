# Revisión de coordenadas de las paradas

Generado con `npm run check:stops` (OpenStreetMap/Nominatim). Paradas cuya coordenada se aleja
más de 80 m de lo que OSM encuentra con «título, ciudad». No todo aviso es un error: OSM
puede devolver otro sitio con el mismo nombre, o la parada estar a propósito en un punto de la
plaza. Revisar cada una y, al moverla, regenerar los trazados (`npm run gen:paths`).

Paradas revisadas: 140. Con aviso: 95.

| Ciudad | Parada | Ruta | Pack (lat, lng) | OSM (lat, lng) | Distancia | Qué encontró OSM |
|---|---|---|---|---|---|---|
| Almería | Cable Inglés | `desierto-huerta` | 36.83050, -2.46550 | 36.83381, -2.45825 | 744 m | Cable Inglés |
| Almería | Mercado Central | `desierto-huerta` | 36.84400, -2.46110 | 36.84030, -2.46263 | 433 m | Mercado Central |
| Almería | Refugios de la Guerra Civil | `atalaya` | 36.83980, -2.46310 | 36.84167, -2.46451 | 243 m | Refugios de la Guerra Civil Española de Almería |
| Almería | Barrio de la Chanca | `desierto-huerta` | 36.83880, -2.47480 | 36.84001, -2.47582 | 162 m | Biblioteca Pública Municipal del Barrio de La Chanca |
| Almería | Muralla de Jayrán | `atalaya` | 36.84300, -2.46920 | 36.84228, -2.47031 | 127 m | Muralla de Jayrán |
| Almería | Puerta de Purchena | `atalaya` | 36.84250, -2.46300 | 36.84175, -2.46398 | 120 m | Puerta de Purchena |
| Almería | Parque de Nicolás Salmerón | `atalaya` | 36.83660, -2.46600 | — | — | OSM no lo encuentra con ese nombre |
| Almería | Plaza Vieja | `atalaya` | 36.84100, -2.46600 | — | — | OSM no lo encuentra con ese nombre |
| Almería | Aljibes de Jayrán | `atalaya` | 36.84210, -2.46360 | — | — | OSM no lo encuentra con ese nombre |
| Almería | Paseo de Almería | `feria-virgen-mar` | 36.83980, -2.46310 | — | — | OSM no lo encuentra con ese nombre |
| Almería | Santuario de la Virgen del Mar | `feria-virgen-mar` | 36.83910, -2.46490 | — | — | OSM no lo encuentra con ese nombre |
| Almería | Barrio de La Chanca | `tesoro-alcazaba` | 36.83880, -2.47480 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Oratorio de San Felipe Neri | `la-ciudad-que-no-cayo` | 36.53520, -6.29770 | 36.53286, -6.29980 | 321 m | Oratorio de San Felipe Neri |
| Cádiz | Calle Ancha | `el-recetario-perdido` | 36.53520, -6.29480 | 36.53377, -6.29788 | 318 m | Calle Ancha |
| Cádiz | Plaza de la Merced | `sobre-los-hombros` | 36.52690, -6.28800 | 36.52840, -6.29102 | 318 m | Plaza de la Merced |
| Cádiz | Puertas de Tierra | `el-cartelon-y-el-levante` | 36.52450, -6.28950 | 36.52690, -6.28910 | 269 m | Puertas de Tierra |
| Cádiz | Iglesia de Santa María | `sobre-los-hombros` | 36.52770, -6.28930 | 36.52775, -6.29175 | 220 m | Iglesia Conventual de Santa Maria |
| Cádiz | Plaza de San Antonio | `el-recetario-perdido` | 36.53540, -6.29660 | 36.53483, -6.29893 | 218 m | Plaza de San Antonio |
| Cádiz | Plaza de España | `la-ciudad-que-no-cayo` | 36.53690, -6.29220 | 36.53513, -6.29320 | 217 m | Plaza de España |
| Cádiz | Calle María la Hierbabuena | `el-cartelon-y-el-levante` | 36.53350, -6.30460 | 36.53343, -6.30259 | 180 m | Calle María la Hierbabuena |
| Cádiz | Plaza de San Francisco | `el-recetario-perdido` | 36.53450, -6.29450 | 36.53428, -6.29632 | 165 m | Plaza de San Francisco |
| Cádiz | Plaza de las Flores | `el-recetario-perdido` | 36.53220, -6.29660 | 36.53099, -6.29733 | 149 m | Plaza de las Flores |
| Cádiz | Iglesia de San Agustín | `sobre-los-hombros` | 36.53280, -6.29520 | 36.53212, -6.29423 | 115 m | Iglesia de San Agustín |
| Cádiz | Plaza de San Juan de Dios | `la-ciudad-que-no-cayo` | 36.52960, -6.29210 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Mercado Central | `la-ciudad-que-no-cayo` | 36.53380, -6.30000 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Torre Tavira | `la-ciudad-que-no-cayo` | 36.53430, -6.29680 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | La Caleta | `la-ciudad-que-no-cayo` | 36.53270, -6.30600 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Barrio de La Viña | `el-recetario-perdido` | 36.53190, -6.30320 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Gran Teatro Falla | `el-cartelon-y-el-levante` | 36.53410, -6.30370 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Plaza de Abastos | `el-cartelon-y-el-levante` | 36.53380, -6.30000 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Iglesia de la Palma | `sobre-los-hombros` | 36.53160, -6.30400 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Plaza de la Candelaria | `sobre-los-hombros` | 36.53340, -6.29310 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Plaza del Palillero | `sobre-los-hombros` | 36.53460, -6.29380 | — | — | OSM no lo encuentra con ese nombre |
| Cádiz | Plaza de San Juan de Dios | `sangre-drago` | 36.53020, -6.29240 | — | — | OSM no lo encuentra con ese nombre |
| Córdoba | Plaza de Colón | `malmuerta` | 37.88900, -4.77720 | 37.89099, -4.77887 | 266 m | Plaza de Colón |
| Córdoba | El Arenal | `mayo-cordobes` | 37.87120, -4.76690 | 37.87322, -4.76604 | 237 m | El Arenal |
| Córdoba | Alcázar de los Reyes Cristianos | `biblioteca-del-califa` | 37.87660, -4.78330 | 37.87523, -4.78306 | 154 m | Alcázar de los Reyes Cristianos |
| Córdoba | Palacio de Viana | `tomate-salmorejo` | 37.88780, -4.77560 | 37.88867, -4.77432 | 148 m | Palacio de Viana |
| Córdoba | La Sinagoga | `biblioteca-del-califa` | 37.88050, -4.78200 | 37.87981, -4.78338 | 144 m | La Sinagoga |
| Córdoba | Puerta del Puente | `biblioteca-del-califa` | 37.87890, -4.77870 | 37.87775, -4.77913 | 133 m | Puerta del Puente |
| Córdoba | Plaza del Potro | `tomate-salmorejo` | 37.88110, -4.77350 | 37.88101, -4.77482 | 116 m | Plaza del Potro |
| Córdoba | Plaza de la Corredera | `tomate-salmorejo` | 37.88260, -4.77480 | 37.88357, -4.77449 | 111 m | Plaza de la Corredera |
| Córdoba | Molino de la Albolafia | `biblioteca-del-califa` | 37.87760, -4.78060 | 37.87678, -4.77999 | 106 m | Molino de la Albolafia |
| Córdoba | Puerta de Almodóvar | `biblioteca-del-califa` | 37.88110, -4.78340 | 37.88061, -4.78418 | 87 m | Córdoba Tips Tours |
| Córdoba | Campo Santo de los Mártires | `biblioteca-del-califa` | 37.87760, -4.78230 | 37.87829, -4.78274 | 86 m | Parking la Mezquita de Cordoba |
| Córdoba | Plaza de Santa Marina | `tomate-salmorejo` | 37.88890, -4.77720 | — | — | OSM no lo encuentra con ese nombre |
| Córdoba | Cruz de mayo en San Andrés | `mayo-cordobes` | 37.88580, -4.77310 | — | — | OSM no lo encuentra con ese nombre |
| Córdoba | Plaza de San Andrés | `malmuerta` | 37.88580, -4.77310 | — | — | OSM no lo encuentra con ese nombre |
| Granada | Arco de las Pesas | `abencerrajes` | 37.18260, -3.59200 | 37.18247, -3.59377 | 158 m | Arco de Las Pesas |
| Granada | Plaza Isabel la Católica | `abencerrajes` | 37.17600, -3.59850 | 37.17552, -3.59740 | 111 m | Plaza de Isabel la Católica |
| Granada | El Bañuelo | `abencerrajes` | 37.17780, -3.59220 | 37.17845, -3.59299 | 100 m | El Bañuelo |
| Granada | Puerta de la Justicia | `abencerrajes` | 37.17540, -3.59090 | 37.17610, -3.59029 | 95 m | Puerta de la Justicia |
| Granada | Capilla Real | `abencerrajes` | 37.17630, -3.59960 | 37.17630, -3.59857 | 92 m | Capilla Real |
| Granada | Paseo de los Tristes | `abencerrajes` | 37.17920, -3.59050 | — | — | OSM no lo encuentra con ese nombre |
| Granada | Plaza de Bib-Rambla | `pionono` | 37.17520, -3.60030 | — | — | OSM no lo encuentra con ese nombre |
| Granada | Casa de Castril | `ventana-castril` | 37.17870, -3.59170 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Museo de Huelva | `decano` | 37.26160, -6.94420 | 37.25499, -6.94359 | 737 m | Museo Provincial de Huelva |
| Huelva | Plaza del Punto | `choqueros` | 37.25950, -6.95190 | 37.25470, -6.94692 | 693 m | Plaza del Punto |
| Huelva | Plaza de la Merced | `decano` | 37.26380, -6.94780 | 37.26242, -6.95238 | 434 m | Plaza de la Merced |
| Huelva | Mercado del Carmen | `decano` | 37.25480, -6.95350 | 37.25481, -6.95574 | 199 m | Mercado del Carmen |
| Huelva | Plaza de las Monjas | `decano` | 37.25830, -6.95020 | 37.25717, -6.95148 | 169 m | Plaza de las Monjas |
| Huelva | Muelle del Tinto | `decano` | 37.25230, -6.95690 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Antigua Estación de Sevilla | `decano` | 37.25540, -6.94910 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Barrio Obrero | `decano` | 37.26450, -6.93370 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Casa Colón | `decano` | 37.26060, -6.94500 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Muelle de Levante | `choqueros` | 37.25300, -6.94420 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Iglesia de San Pedro | `choqueros` | 37.26060, -6.95140 | — | — | OSM no lo encuentra con ese nombre |
| Huelva | Paseo de la Ría | `colombinas` | 37.25000, -6.95850 | — | — | OSM no lo encuentra con ese nombre |
| Jaén | Iglesia de la Magdalena | `lagarto-malena` | 37.77290, -3.79320 | 37.77198, -3.79664 | 320 m | Iglesia de la Magdalena |
| Jaén | Raudal de la Magdalena | `mar-de-olivos` | 37.77240, -3.79380 | 37.77174, -3.79663 | 260 m | Raudal de la Magdalena |
| Jaén | Baños árabes | `lagarto-malena` | 37.77020, -3.79150 | 37.77102, -3.79397 | 236 m | Baños Árabes |
| Jaén | Arco de San Lorenzo | `lagarto-malena` | 37.76800, -3.79080 | 37.76654, -3.79235 | 212 m | Arco de San Lorenzo |
| Jaén | Plaza de San Juan | `lagarto-malena` | 37.76970, -3.79200 | 37.77002, -3.79392 | 172 m | Plaza de San Juan |
| Jaén | Mercado de San Francisco | `mar-de-olivos` | 37.76710, -3.78800 | 37.76698, -3.78989 | 167 m | Mercado de San Francisco |
| Jaén | Plaza de la Constitución | `lagarto-malena` | 37.76650, -3.78670 | 37.76757, -3.78786 | 157 m | Plaza de la Constitución |
| Jaén | Plaza de Santa María | `mar-de-olivos` | 37.76540, -3.78970 | 37.76485, -3.79063 | 102 m | Plaza de Santa María |
| Jaén | Basílica de San Ildefonso | `lagarto-malena` | 37.76440, -3.78620 | — | — | OSM no lo encuentra con ese nombre |
| Jaén | Fuente del Lagarto | `lagarto-malena` | 37.77240, -3.79380 | — | — | OSM no lo encuentra con ese nombre |
| Málaga | Playa de la Malagueta | `espeto` | 36.71950, -4.40900 | 36.71644, -4.41094 | 382 m | Playa de La Malagueta |
| Málaga | Muelle Uno | `espeto` | 36.71830, -4.41470 | 36.71599, -4.41380 | 269 m | Muelle Uno |
| Málaga | La estatua del Cenachero | `misterio-manquita` | 36.71880, -4.41960 | — | — | OSM no lo encuentra con ese nombre |
| Málaga | La Manquita | `misterio-manquita` | 36.72010, -4.41920 | — | — | OSM no lo encuentra con ese nombre |
| Málaga | Alcazaba | `feria-agosto` | 36.72100, -4.41550 | — | — | OSM no lo encuentra con ese nombre |
| Sevilla | Fábrica de Tabacos | `feria-abril` | 37.38080, -5.99180 | 37.37680, -5.99510 | 532 m | Fábrica de Tabacos |
| Sevilla | Portada de la Feria | `feria-abril` | 37.37450, -6.00050 | 37.37095, -5.99734 | 484 m | Portada de la Feria de Abril |
| Sevilla | Monumento a Colón | `donde-esta-colon` | 37.38220, -5.98730 | 37.38544, -5.98687 | 362 m | Cementerio de la Judería |
| Sevilla | Prado de San Sebastián | `feria-abril` | 37.38000, -5.98450 | 37.37944, -5.98670 | 205 m | Prado de San Sebastián |
| Sevilla | Jardines de Murillo | `feria-abril` | 37.38220, -5.98730 | 37.38368, -5.98783 | 172 m | Jardines de Murillo |
| Sevilla | Real Alcázar | `donde-esta-colon` | 37.38360, -5.99150 | 37.38321, -5.99018 | 124 m | Real Alcázar de Sevilla |
| Sevilla | Plaza de España | `feria-abril` | 37.37720, -5.98690 | 37.37658, -5.98600 | 105 m | Plaza de España |
| Sevilla | Callejón del Agua | `donde-esta-colon` | 37.38400, -5.98850 | 37.38450, -5.98947 | 102 m | Callejón del Agua |
| Sevilla | Plaza del Salvador | `azahar` | 37.38950, -5.99400 | 37.39003, -5.99310 | 99 m | Plaza del Salvador |
| Sevilla | Puente de Triana | `donde-esta-colon` | 37.38560, -6.00300 | 37.38628, -6.00243 | 91 m | Puente de Isabel II |
| Sevilla | Plaza del Triunfo | `donde-esta-colon` | 37.38500, -5.99160 | 37.38491, -5.99257 | 86 m | Plaza del Triunfo |
| Sevilla | La tumba de Colón | `donde-esta-colon` | 37.38510, -5.99340 | — | — | OSM no lo encuentra con ese nombre |
