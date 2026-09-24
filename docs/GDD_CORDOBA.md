# Córdoba · pack `content/cordoba/cordoba.pack.json`

Quinta ciudad. Dos rutas con el formato de caso de detective: tres sospechosos, «ramificar y
reunir», dos decisiones y cuatro finales.

## Ruta de historia · «La biblioteca del califa»

**Caso:** en el siglo X, la biblioteca de al-Hakam II tenía, según las crónicas, unos 400.000
libros (el catálogo ocupaba 44 volúmenes). Desapareció. ¿Quién acabó con ella?

**Sospechosos** (cada pista empieza por el suyo): **Almanzor** (quemó libros de filosofía y
astronomía para ganarse a los sabios de la religión), **la guerra** (la fitna de 1009: asedios,
venta de libros para pagar la defensa, saqueo de Medina Azahara y de Córdoba en 1013) y **los
libreros** (compraban lo que otros vendían). **Veredicto: la guerra.** Almanzor quemó una parte;
la fitna vació la biblioteca. Algunos libros sobrevivieron en las taifas.

| id | Personaje | Papel |
| --- | --- | --- |
| `lubna` (guía) | Lubna, copista y secretaria de al-Hakam II (s. X). Persona real. | Narra |
| `almanzor` | Almanzor, hayib de Hisham II (c. 938-1002). Persona real. | Sospechoso |
| `librero` | Librero del zoco (ficticio) | Sospechoso |

Caminos: `dinero` (mar) = **El río**; `poder` (arcilla) = **La Judería**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| n1 | Puerta del Puente | El caso; puente romano | El cálamo de Lubna |
| n2 | Patio de los Naranjos | Mezquita, mihrab de al-Hakam II; Almanzor · **decisión 1** | Los arcos de la Mezquita |
| a1 (Judería) | Sinagoga (1315), Maimónides | El librero; 170 copistas | El candil de la Judería |
| a2 (Judería) | Puerta de Almodóvar, Averroes | La fitna; venta de libros en el asedio | El libro de Averroes |
| b1 (río) | Molino de la Albolafia | Noria (leyenda de Isabel); Almanzor muere en 1002 | La noria de la Albolafia |
| b2 (río) | Alcázar de los Reyes Cristianos (1328) | Colón en 1486; saqueo de Medina Azahara | Los jardines del Alcázar |
| n4 | Campo Santo de los Mártires | **decisión 2**: el humo (Almanzor) o el dinero (el librero) | — |
| n5 | Torre de la Calahorra | **Veredicto** | Los 44 catálogos |
| n6 | Cierre | Finales: Sabio de la Judería · Copista de Lubna · Cronista del califa · Cazador de manuscritos | La biblioteca del califa |

## Ruta gastronómica · «¿Quién le puso tomate al salmorejo?»

`theme: "gastronomia"`. Nunca exige comer ni beber; no se nombra ningún bar.

**Caso:** el salmorejo es el orgullo de Córdoba, pero el tomate llegó de América. **Sospechosos:**
**los romanos** (pan majado con aceite, vinagre y ajo), **los andalusíes** (Ziryab y la cocina de
la corte) y **los jornaleros** (el dornillo en el olivar). **Veredicto: los jornaleros**: el
salmorejo antiguo era blanco (pan, ajo, aceite, vinagre, sal) y el tomate entró en el dornillo en
el siglo XIX.

| id | Personaje | Papel |
| --- | --- | --- |
| `patiera` (guía) | Cuida un patio de flores; defiende el salmorejo de su abuela | Narra |
| `ziryab` | Ziryab, músico de Bagdad en la corte de Abderramán II (llegó en 822). Persona real. | Sospechoso |
| `jornalero` | Jornalero de los olivares, con su dornillo | Sospechoso |

Caminos: `dinero` (mar) = **Santa Marina**; `poder` (arcilla) = **La Judería**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Plaza de la Corredera | Mercado; el caso | El dornillo |
| g2 | Templo romano | Aceite de la Bética en ánforas; monte Testaccio · **decisión 1** | El ánfora de la Bética |
| ga1 | Palacio de Viana | 12 patios; Fiesta de los Patios (UNESCO 2012); salmorejo blanco | La maceta del patio |
| ga2 | Plaza de Santa Marina | Manolete; rabo de toro y flamenquín | El flamenquín |
| gb1 | Calleja de las Flores | Berenjenas con miel (se cuenta); Ziryab no conocía el tomate | Berenjenas con miel |
| gb2 | Puerta de Almodóvar | Ziryab y el orden de los platos | El laúd de Ziryab |
| g4 | Plaza de las Tendillas | Reloj con guitarra · **decisión 2**: el mortero o el banquete | — |
| g5 | Plaza del Potro | Posada del Potro (Quijote); pastel cordobés · **veredicto** | El pastel cordobés |
| g6 | Cierre | Maestro del dornillo · Catador de patios · Cronista del salmorejo · Invitado de Ziryab | ¿Quién le puso tomate…? |

## Datos a verificar

- Cifra de 400.000 volúmenes y 44 catálogos (cifras de las crónicas, probablemente exageradas).
- Papel exacto de Lubna (las fuentes le atribuyen cargos distintos) y las «170 copistas».
- Quién vendió los libros durante el asedio (las fuentes citan al general Wadih) y fechas de la fitna.
- Leyenda de la noria de la Albolafia e Isabel la Católica (va como «se cuenta»).
- Origen de las berenjenas con miel (va como «se cuenta») y del flamenquín (Bujalance/Andújar).
- Historia del salmorejo: el paso del salmorejo blanco al de tomate (siglo XIX) según divulgación
  gastronómica; conviene contrastarlo con un historiador de la alimentación.
- Coordenadas y radios de todas las paradas (estimaciones).

## Fuentes consultadas

- Biblioteca Nacional de España, «Alhaquén II, el califa bibliófilo».
- Wikipedia: Alhakén II, Almanzor, Lubna de Córdoba, Ziryab.
- Hispania Histórica, «Al-Hakam II y la Biblioteca de Córdoba».
- Casa Árabe, sobre la calle «Escriba Lubna».
- Divulgación sobre el salmorejo: Directo al Paladar, Mercado Calabajío, Andalucía Sabe.
- Sobre Ziryab: Fundación Ibercaja, Hammam al Ándalus.
