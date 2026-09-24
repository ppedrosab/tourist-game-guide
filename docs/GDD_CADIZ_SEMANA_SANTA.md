# Cádiz · «Sobre los hombros de Cádiz» (ruta de fiestas: Semana Santa)

Cuarta ruta del pack de Cádiz y segunda de **fiestas** (`"theme": "fiestas"`, seña morada
«Fiestas» / «Festivals»; los datos se rotulan «Tradición»). Mismo formato de caso que el resto:
«ramificar y reunir», dos decisiones y cuatro finales.

## Tono y límites

- **Respeto**: ni chistes sobre imágenes ni sobre hermandades. **No se dibujan imágenes sagradas**:
  en los fondos se ven pasos de palio desde fuera (faldón, candelería, varales, techo), cirios,
  colgaduras y nazarenos anónimos; bajo el palio solo hay luz de velas.
- Lo que no está documentado va como «se cuenta» (`legend: true`), como el origen portuario de los
  cargadores.
- Se habla de devoción y de tradición del barrio, sin pedir al jugador que rece, entre en un templo
  o pague entrada.

## El caso

¿**Por qué en Cádiz los pasos van a hombros, tan despacio, y son tan altos y estrechos?**
Tres respuestas posibles, y cada pista del cuaderno empieza por la suya:

- **El puerto**: se cuenta que los primeros cargadores eran hombres del muelle (leyenda).
- **Las calles**: el casco antiguo es muy estrecho; los pasos tienen que ser altos y estrechos y
  avanzar despacio, a golpe de horquilla.
- **El barrio**: la devoción se hereda en Santa María y en La Viña.

Veredicto (quiz en el Palillero): **las tres cosas juntas**.

## Personajes (ninguno repite de otras rutas)

| id | Quién | Papel |
| --- | --- | --- |
| `cargador` (guía) | Camisa blanca, faja negra, almohadilla al hombro | Cercano; orgulloso de su barrio |
| `maniguetero` | Túnica morada con cíngulo blanco y horquilla | Marca el ritmo; serio, de pocas palabras |
| `saetera` | Vestido negro y peineta (mantilla por detrás) | Canta la saeta desde el balcón |

## Caminos y finales

Huecos: `dinero` (mar) = **Santa María**; `poder` (arcilla) = **La Viña**.

| Decisión 1 (Catedral) | Decisión 2 (Candelaria) | Final |
| --- | --- | --- |
| `camino_santamaria` | `version_saeta` | Voz de Santa María |
| `camino_santamaria` | `version_silencio` | Cargador de honor |
| `camino_vina` | `version_saeta` | Saeta de La Viña |
| `camino_vina` | `version_silencio` | Guardián del silencio |

## Paradas

| Nodo | Lugar | Tema | Coleccionable |
| --- | --- | --- | --- |
| s1 | Plaza de San Juan de Dios | Cargadores (no costaleros); el caso; salida de la Carrera Oficial | El cirio |
| s2 | Catedral | El maniguetero y la horquilla; pasos altos y estrechos · **decisión 1** | La horquilla |
| sa1 (Santa María) | Iglesia de Santa María | El Nazareno, «el Greñúo», regidor perpetuo; Jueves Santo | La cruz de guía |
| sa2 (Santa María) | Plaza de la Merced | La saeta; el barrio, cuna del cante (Enrique el Mellizo) | La saeta |
| sb1 (La Viña) | Iglesia de la Palma | Lunes Santo; el maremoto de 1755 y el 1 de noviembre | El estandarte de la Palma |
| sb2 (La Viña) | Iglesia de San Agustín | La Buena Muerte, «el Silencio»: Viernes Santo con las luces apagadas desde 1921 | La vela del silencio |
| s4 | Plaza de la Candelaria | La Carrera Oficial · **decisión 2** (saeta o silencio) | — |
| s4a / s4b | La saeta (cantada) / El silencio (la horquilla) | Nodos narrativos | — |
| s5 | Plaza del Palillero | Torrijas y pestiños; **veredicto** | La torrija |
| s6 | Recogida | Final según caminos | Sobre los hombros de Cádiz |

Fondos: San Juan de Dios y Catedral se reutilizan de la ruta de historia; los demás salen de
`scripts/art/cadiz_ssanta_scenes.py` (San Agustín y el Palillero, de noche con la luna de Pascua).
Sprites en `scripts/art/cadiz_fiestas_sprites.py`, medallones en `cadiz_fiestas_collectibles.py`.

## Datos a verificar (antes de publicar)

- **Origen portuario de los cargadores**: va como leyenda. Hay referencias a cargadores del muelle
  en 1587, pero sin confirmar que sean de Cádiz y no de Sevilla.
- **«Regidor perpetuo»** del Nazareno de Santa María y la datación de la imagen (finales del XVI o
  principios del XVII).
- **Silencio desde 1921** con las luces apagadas y su recorrido hasta la Catedral.
- Días de salida (Nazareno: Jueves Santo; Palma: Lunes Santo) y recorrido actual de la
  **Carrera Oficial** (cambia algunos años).
- Rosario del 1 de noviembre en La Viña por el maremoto de 1755.
- Coordenadas y radios de todas las paradas (estimaciones); tiempos a pie.
- Revisión por alguien de las hermandades (trato, vocabulario: «cargador», «maniguetero»,
  «horquilla», «Carrera Oficial»).

## Fuentes consultadas

- Wikipedia: «Semana Santa en Cádiz».
- Web de la Hermandad del Nazareno de Santa María (nazarenodesantamaria.com).
- Web de la Cofradía de la Buena Muerte (cofradiabuenamuerte.es).
- Portal de Cádiz, Onda Cádiz y Canal Sur sobre el maremoto de 1755 y la Virgen de la Palma.
- El Debate, sobre los cargadores gaditanos.
