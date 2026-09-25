# Rutas gastronómicas de Málaga, Sevilla y Granada

Tres rutas `theme: "gastronomia"` que se suman a la de historia de cada pack. Mismo formato de caso
(tres sospechosos, dos decisiones, cuatro finales). Personajes propios, sin repetir los de
historia. Nunca exigen comer ni beber y no nombran ningún bar. La mayoría de paradas reutiliza los
fondos de la ruta de historia; los nuevos están en `scripts/art/gastro_andalucia_scenes.py`.

## Málaga · «¿Quién inventó el espeto?» (`espeto`)

**Sospechosos:** **los fenicios** (fundaron Malaka y salaban el pescado), **los pescadores** (asaban
sardinas en la playa al volver de la jábega) y **el Migué** (Miguel Martínez Soler, que hacia 1882,
en El Palo, fue el primero en ensartar las sardinas en una caña junto a la lumbre). **Veredicto:
el Migué**, a partir de lo que ya hacían los pescadores.

| id | Personaje | Papel |
| --- | --- | --- |
| `espetero` (guía) | Espetero de la playa | Narra |
| `jabegote` | Remero de la jábega | Coguía |
| `pasera` | Pasera de la Axarquía | Coguía |

Caminos: `dinero` = **El mar**; `poder` = **El centro**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Mercado de Atarazanas | Puerta nazarí; el caso | La sardina |
| g2 | Calle Larios | Pasas de la Axarquía (SIPAM de la FAO) · **decisión 1** | La pasa moscatel |
| ga1 | Muelle Uno (nuevo fondo) | La jábega y su ojo en la proa (se cuenta) | La jábega |
| ga2 | Playa de la Malagueta (nuevo fondo) | La barca de brasas; meses sin erre | El espeto |
| gb1 | Plaza de la Constitución | DO Málaga (1933); el tranvía al Palo | El vino de Málaga |
| gb2 | Teatro Romano | Salazones y garum | El ánfora de garum |
| g4 | La Manquita | Ajoblanco, gazpachuelo · **decisión 2**: la barca o el rey | — |
| g5 | Plaza de la Merced | Los nombres del café · **veredicto** | El café de nueve nombres |

Leyenda contada como «se cuenta»: Alfonso XII y el «Majestá, asín no, con los deos» (1885).

## Sevilla · «¿Por qué Sevilla huele a azahar?» (`azahar`)

**Sospechosos:** **los andalusíes** (trajeron el naranjo amargo por su flor, su sombra y su
perfume), **los escoceses** (mermelada de Dundee desde 1797; se llevan la fruta) y **los
jardineros** (siguen plantándolos hoy). **Veredicto: los andalusíes.**

| id | Personaje | Papel |
| --- | --- | --- |
| `naranjera` (guía) | Recoge las naranjas de las calles | Narra |
| `keiller` | Janet Keiller, de Dundee, a la que la tradición atribuye la primera mermelada comercial de naranja de Sevilla | Sospechosa |
| `aceitunero` | Aliña aceitunas manzanillas y gordales | Coguía |

Caminos: `dinero` = **El río**; `poder` = **El centro**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Mercado de Triana (nuevo fondo) | Castillo de San Jorge; el caso | La naranja amarga |
| g2 | Puente de Triana (1852) | Aceituna de mesa · **decisión 1** | Las aceitunas aliñadas |
| ga1 | Torre del Oro | Mermelada de Dundee (1797) | La mermelada |
| ga2 | Real Alcázar | El naranjo de Pedro I (se cuenta) | El naranjo del rey |
| gb1 | Plaza del Salvador (nuevo fondo) | Agua de azahar | El agua de azahar |
| gb2 | La Giralda | Patio de los Naranjos de la mezquita almohade | El Patio de los Naranjos |
| g4 | Plaza del Triunfo | Más de 25.000 naranjos · **decisión 2**: el barco o el azahar | — |
| g5 | Callejón del Agua | La costumbre de las tapas · **veredicto** | La tapa |

## Granada · «¿Quién inventó el pionono?» (`pionono`)

**Sospechosos:** **las monjas** (dulces de convento por el torno), **los moriscos** (dulces de miel
y almendra) y **Ceferino** (Ceferino Isla, pastelero de Santa Fe, 1897). **Veredicto: Ceferino
Isla**, que lo llamó así en honor al papa Pío IX, «Pío Nono», y le dio forma que lo recordara.

| id | Personaje | Papel |
| --- | --- | --- |
| `lorca` (guía) | Federico García Lorca, de Fuente Vaqueros, a un paso de Santa Fe | Narra |
| `ceferino` | Ceferino Isla, pastelero de Santa Fe (1897). Persona real. | Sospechoso |
| `tornera` | Monja que atiende el torno del convento | Sospechosa |

Caminos: `dinero` = **El zoco**; `poder` = **El Albaicín**.

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| g1 | Mercado de San Agustín (nuevo fondo) | Especias; tapa con la bebida; el caso | Las especias |
| g2 | Plaza de Bib-Rambla (nuevo fondo) | «Puerta del arenal»; churros · **decisión 1** | Churros con chocolate |
| ga1 | Alcaicería (nuevo fondo) | Mercado de la seda (incendio de 1843); dulces moriscos | La seda de la Alcaicería |
| ga2 | Corral del Carbón | Alhóndiga nazarí; Pío Nono | La alhóndiga |
| gb1 | El Bañuelo | El torno del convento | El torno |
| gb2 | Mirador de San Nicolás | La forma del pionono | Las yemas |
| g4 | Plaza Isabel la Católica | Habas con jamón, tortilla del Sacromonte, remojón · **decisión 2** | — |
| g5 | Capilla Real | Santa Fe (1491) · **veredicto** | El remojón |

## Datos a verificar

- Málaga: fecha y autoría del espeto (Migué, 1882) y la anécdota de Alfonso XII; origen fenicio del
  ojo de la jábega; restos de salazones bajo el centro; los nombres del café malagueño.
- Sevilla: fecha y lugar de la primera mermelada comercial; número de naranjos; el naranjo de
  Pedro I en el Alcázar; la cáscara de naranja en el aliño de aceitunas; puente de Triana (1852).
- Granada: la historia de Ceferino Isla y el pionono (1897); incendio de la Alcaicería (1843);
  qué conventos del Albaicín venden dulces hoy.
- Coordenadas y radios de todas las paradas (estimaciones).

## Fuentes consultadas

- Visita Costa del Sol, «La historia del famoso espeto de sardinas»; Wikipedia, Espeto.
- Junta de Andalucía, «SIPAM Uva Pasa de Málaga en la Axarquía»; Consejo Regulador Vino Málaga.
- El Blog de la Tabla, «Naranjas amargas de Sevilla»; Tu guía de Sevilla, «La naranja amarga».
- Turismo de Santa Fe, «Origen del pionono»; Infobae y ACI Prensa sobre el pionono.
