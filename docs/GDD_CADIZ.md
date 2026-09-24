# Cádiz · «La ciudad que no cayó»

Primera ruta de Cádiz. Pack: `content/cadiz/la-ciudad-que-no-cayo.pack.json` (es + en).
Mismo motor que Málaga: «ramificar y reunir», dos decisiones y cuatro finales.

## El caso

**Expediente Cádiz, 1810-1812.** Napoleón tenía el ejército más temido de Europa: tomó Madrid y
Sevilla, pero se quedó dos años y medio atascado ante una ciudad que se cruza andando en veinte
minutos. ¿Por qué no pudo con ella?

La Tía Norica lo plantea como un caso de detective con **tres sospechosos**, y el jugador reúne
pistas contra cada uno:

| Sospechoso | Pistas |
| --- | --- |
| **El mar** | La riqueza llegaba por mar (catedral) · «Mientras hubiera barcos…» (mercado) · la bahía abierta (partes de guerra) |
| **La isla** | Nadie la pillaba por sorpresa (Torre Tavira) · casi una isla (partes de guerra) · puerto fácil de defender desde los fenicios (museo) |
| **Los gaditanos** | La Constitución escrita bajo las bombas (San Felipe) · las coplas contra las bombas (coplas) |

Cada pista del cuaderno empieza por su sospechoso («El mar · …», «La isla · …», «Los gaditanos · …»).

Veredicto (reto final): **los tres a la vez**; no hubo un solo culpable. Las dos decisiones son
«¿qué pista investigamos?» (el mar o la ciudad) y «¿qué testigo escuchamos?» (las coplas o los
partes de guerra).

## Personajes

| id | Quién | Tono |
| --- | --- | --- |
| `tia_norica` (guía) | Marioneta gaditana del s. XIX, abuela cotilla | Guasa, «pisha», exagera pero no miente |
| `la_pepa` | La Constitución de 1812 en persona | Solemne, idealista, orgullosa |
| `magon` | Mercader fenicio de Gadir | Presumido, comerciante, habla de barcos y atún |

## Caminos y finales

Los huecos de camino del motor son `dinero` (color mar) y `poder` (color arcilla); en esta ruta
se llaman **Mar** y **Ciudad** (`route.branches`).

| Decisión 1 (catedral) | Decisión 2 (Plaza de España) | Final |
| --- | --- | --- |
| `camino_mar` («Investigar el mar») | `version_documentos` («Leer los partes de guerra») | Vigía del Atlántico |
| `camino_mar` | `version_coplas` | Corsario de coplas |
| `camino_ciudad` | `version_documentos` | Diputado de las Cortes |
| `camino_ciudad` | `version_coplas` | Chirigotero |

## Paradas

| Nodo | Lugar | Reto | Pista / coleccionable |
| --- | --- | --- | --- |
| n1 | Plaza de San Juan de Dios | — | Títere de la Tía Norica |
| n2 | Catedral | Quiz: más de un siglo de obras | «La riqueza llegaba por mar» · **decisión 1** |
| a1 (mar) | Mercado Central | Quiz: almadraba → atún rojo | «Mientras hubiera barcos…» · Atún de almadraba |
| a2 (mar) | Torre Tavira | Observa: calle Marqués del Real Tesoro | «Nadie la pillaba por sorpresa» · Catalejo |
| b1 (ciudad) | Oratorio de San Felipe Neri | Quiz: por qué «la Pepa» | «Escribieron la Constitución» · Pepa de bolsillo |
| n4 | Plaza de España (monumento a las Cortes) | Quiz: duración del asedio | **decisión 2** |
| n4a | (narrativo) Bombas y tirabuzones | — | «Las bombas asustaban poco» |
| n4b | (narrativo) Una ciudad casi isla | — | «Casi una isla y la bahía abierta» |
| n5 | Museo de Cádiz, Plaza de Mina | Quiz: Gadir | «Un puerto abierto y fácil de defender» |
| n6 | La Caleta | Foto con el Balneario de la Palma | Postal de La Caleta |
| n6b | (narrativo) El veredicto | Quiz final: los tres sospechosos | — |
| n7 | Caso cerrado | — | Insignia «La ciudad que no cayó» |

Escenas (`fondos/fondo_cadiz_{clave}.svg` → capas `bg_cadiz_{clave}_…`): `sanjuan`, `catedral`,
`mercado`, `tavira`, `sanfelipe`, `espana`, `mina`, `caleta`.

## Datos que se afirman (revisar con un historiador local)

- Asedio: 5 de febrero de 1810 – 24/25 de agosto de 1812; la ciudad nunca fue tomada.
- Títeres de la Tía Norica: tradición gaditana desde el siglo XIX.
- Casa de Contratación trasladada de Sevilla a Cádiz en 1717; catedral nueva empezada en 1722 y
  consagrada en 1838. Manuel de Falla enterrado en la cripta, bajo el nivel del mar.
- Mercado Central: 1838, «se considera» el primer mercado cubierto de España.
- Almadraba: pesca de atún rojo, de origen fenicio.
- Torre Tavira: punto más alto del casco antiguo, torre vigía oficial desde 1778; más de un centenar
  de torres miradores; cámara oscura. La puerta da a la calle Marqués del Real Tesoro.
- Cortes: abiertas en septiembre de 1810 en la Isla de León; en San Felipe Neri desde febrero de
  1811. Constitución proclamada el 19 de marzo de 1812 (San José → «la Pepa»); soberanía nacional.
- Monumento de la Plaza de España: por el centenario de 1812.
- Bombas francesas desde el Trocadero que se quedaban cortas o no explotaban; la copla de los
  tirabuzones. **Leyenda** (`legend: true`): el plomo de las bombas para rizarse el pelo.
- Istmo, Isla de León y caño de Sancti Petri; flotas española y británica en la bahía.
- Gadir fundada por fenicios de Tiro hace unos 3.000 años **según la tradición**; «Gadir» ≈
  recinto amurallado; los romanos, Gades. Sarcófagos antropoides: masculino 1887, femenino 1980.
- Castillo de Santa Catalina desde 1598, tras el saqueo angloholandés de 1596.
- «Muere otro día» (2002) rodada en La Caleta, que hizo de La Habana.

## Pendientes

- Coordenadas y radios son estimaciones: prueba de campo con `docs/PRUEBAS_CALLE.md`.
- ¿Ruta gratuita? El pack la marca `isFree: true` como la de Málaga; decisión de negocio.
- Horarios: el reto de la Torre Tavira se hace desde la calle; el museo no hace falta visitarlo.
- Voces (no hay audios: el lip-sync simula la duración) y revisión nativa del inglés.
- Posible «antes y ahora» (La Caleta o la Plaza de San Juan de Dios con grabados del s. XIX).
