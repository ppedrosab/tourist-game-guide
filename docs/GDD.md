# Documento de diseño del juego · El misterio de la Manquita

## Concepto
Aventura narrativa geolocalizada. Género: narrativa ramificada ("elige tu propia aventura"),
formato novela visual en la calle. Técnica de guion: **ramificar y reunir** (branch and bottleneck).

## Personajes
- **Er Cenachero** (guía): vendedor ambulante de pescado con dos cenachos. Pícaro, charlatán,
  habla malagueño ("quillo", "pa'"). Estatua de bronce de 1968 en la Plaza de la Marina.
- **La Manquita**: la catedral personificada. Solemne, presumida, dolida por su torre (lleva una
  tirita en la torre sur inacabada).
- **El Teatro Romano** (id `lucio`): el propio teatro de Malaca, que habla con su máscara de actor. Exagerado y teatral.
- Futuros: el biznaguero (s. XIX), un mercader fenicio, un poeta andalusí.

Sprites: 8 expresiones cada uno → neutral, talking, happy, thinking, surprised, nervous, proud,
dramatic. Estilo: cabeza grande, contorno de tinta, sombreado cel, sombra de contacto y luz de borde.

## Ruta: 12 nodos, 2 decisiones, 4 finales (≈ 90 min, 2,2 km)
1. **Plaza de la Marina** · estatua del Cenachero. Planteamiento del misterio.
2. **Calle Larios** · inaugurada el 27-08-1891, pagada por la Casa Larios para unir centro y puerto.
   Reto: esquinas curvas (Eduardo Strachan, Escuela de Chicago). Anécdota (se cuenta): suelo de
   tacos de madera levantado por la riada de 1907.
   **Decisión 1**: rastro del dinero (flag `camino_dinero`) o del poder (`camino_poder`).
   - **A1 · Mercado de Atarazanas**: puerta nazarí del antiguo astillero junto a la playa; se
     reutilizó en el mercado (derribo en 1880). Escudos: "Sólo Dios es el rico / el valiente".
     Reto: arco de herradura. Pista: el dinero entraba por el mar y salía por los caminos.
   - **A2 · Antigua Casa de Guardia** (1840, proveedora de Isabel II). Reto: apuntan la cuenta
     con tiza en la barra. Pista: sin caminos no llegaban vino y pasas al puerto.
   - **B1 · Plaza de la Constitución** (antigua Plaza Mayor). Pista: con Carlos III y Floridablanca
     la Corona dejó de financiar la catedral.
3. **La Manquita** (cuello de botella). Obras 1528–1782; torre sur inacabada (la de la derecha
   vista desde la Plaza del Obispo). Diálogo con variantes según el camino.
   **Decisión 2**: leyenda de América (`version_america`) o documentos de Antequera (`version_caminos`).
   - 4a (nodo narrativo): Bernardo de Gálvez, nacido en Macharaviaya (1746), tomó Pensacola.
   - 4b (nodo narrativo): el dinero fue al camino Málaga–Antequera–Vélez.
4. **Teatro Romano** (cuello de botella). Redescubierto en 1951 al construir la Casa de la Cultura.
   Capiteles y fustes reutilizados en las puertas de la Alcazaba. Pista: todo se reaprovecha.
5. **Plaza de la Merced**. Obelisco de Torrijos (fusilado el 11-12-1831 con sus compañeros; entre
   ellos el inglés Robert Boyd). Casa natal de Picasso (1881); estatua en un banco → reto de foto.
   Anécdota (según su madre): primera palabra "piz" por lápiz; al nacer lo reanimó su tío Salvador.
6. **Resolver el misterio** (quiz) → **Caso cerrado**.

Finales (camino × versión): Detective de puerto (dinero + documentos), Alma marinera
(dinero + leyenda), Detective de despacho (poder + documentos), Cuentacuentos (poder + leyenda).

Coleccionables: Cenacho dorado, Arco nazarí, La tiza de Guardia, El sello del rey,
Foto con Picasso, Detective de la Manquita.

## Pantallas (storyboard)
Descubrir: Bienvenida → Permisos → Inicio/Explorar (con "Continuar") → Rutas de la ciudad →
Detalle de ruta → Mapa en camino · Colección.
En la ruta: Llegada ("¡Has llegado!") → Escena (diálogo) → Antes/ahora (deslizador ilustración vs.
cámara) → Reto → Decisión → Cuaderno (modal) · Pausa (modal) → Caso cerrado (final, estrellas,
"Probar otro camino").

## Monetización (propuesta)
Primera ruta gratis; resto de rutas de pago. Posibles acuerdos con locales de la ruta.

## Competencia conocida en Málaga
Questo (quests de pago) y VoiceMap (audiotour desde el Cenachero). Diferencia: personajes con voz
y decisiones que cambian el recorrido.
