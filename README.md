# The Farmer Was Replaced

Este repositorio reune codigos generados por mi para la eficientacion de granjas dentro del juego **The Farmer Was Replaced**.

La idea del proyecto es recopilar los mejores codigos de automatizacion, documentar como funcionan y revisar que posibles mejoras se pueden hacer en cada estrategia.

## Contenido actual

- `SunflowerFarm.py`: script para automatizar la granja de girasoles.
- `MultiCropFarm.py`: script de granja multicultivo con zonas para calabazas, girasoles, cactus, zanahorias, arboles y arbustos.
- `PolycultureFarm.py`: script de multicultivo que usa `get_companion()` para aprovechar policultivo.
- `MazeSolver.py`: script para crear un laberinto de campo completo y resolverlo buscando el tesoro.
- `DinosaurBoneHarvester.py`: script para recolectar huesos usando el sombrero de dinosaurio.
- `DinosaurBoneHarvesterSim32.py`: variante de una sola corrida para probar dinosaurio con `simulate()` en mundo 32.
- `BenchmarkDinosaurSim32.py`: benchmark que ejecuta la simulacion del dinosaurio en mundo 32.
- `farm_utils.py`: utilidades reutilizables para preparar tierra, plantar columnas y moverse por el mapa.
- `LEADERBOARD_SCRIPTS.md`: mapa de scripts para cada tabla de clasificacion.
- `OPTIMIZATION_IDEAS.md`: ideas y prototipos separados para probar mejoras antes de integrarlas.
- `THIRD_PARTY_NOTICES.md`: atribuciones de repositorios externos usados como referencia.

## Granja de girasoles

`SunflowerFarm.py` automatiza por completo una granja de girasoles.

Su objetivo es mantener el campo siempre ocupado, detectar cuales girasoles ya estan listos para cosechar y recolectarlos en un orden conveniente sin vaciar demasiado la granja.

## Como funciona

El script trabaja en ciclos infinitos:

1. Limpia y prepara el campo al inicio.
2. Recorre toda la granja en patron serpiente para revisar cada casilla.
3. Si una casilla no tiene un girasol, prepara la tierra, riega si hace falta y planta uno nuevo.
4. Mientras recorre el mapa, cuenta cuantos girasoles hay en total.
5. Si encuentra girasoles listos para cosecha, los clasifica por cantidad de petalos usando `measure()`.
6. Luego cosecha primero los girasoles con mas petalos, desde 15 hasta 7.
7. El script se detiene antes de bajar de 10 girasoles en el campo, para no vaciar la produccion por completo.
8. Al final vuelve a rellenar cualquier espacio vacio y repite todo el proceso.

## Idea general del algoritmo

- `move_to(x, y)` mueve al personaje a una coordenada exacta.
- `sweep(...)` recorre toda la granja fila por fila en forma de zigzag.
- `scan_tile(state)` revisa cada casilla, planta si falta un girasol y guarda la posicion de los que ya se pueden cosechar.
- `harvest_descending(state)` cosecha primero los girasoles mas valiosos segun su cantidad de petalos.
- `refill_field()` asegura que el campo vuelva a quedar completo despues de cada ciclo.

## Granja multicultivo

`MultiCropFarm.py` divide el terreno en varias zonas para producir diferentes recursos al mismo tiempo.

Los limites de cada zona se calculan automaticamente con `get_world_size()`, asi que la distribucion se adapta al tamano actual del grid sin que el usuario tenga que ajustar numeros manualmente.

La parte interior esta enfocada en calabazas. Durante cada ciclo revisa si hay calabazas muertas o espacios vacios; si encuentra alguno, replanta y espera antes de cosechar. Si todo el bloque esta sano, cosecha la calabaza grande.

Las capas exteriores se usan para otros cultivos:

1. Girasoles en una primera capa externa.
2. Cactus y zanahorias alternados en patron de tablero.
3. Arboles y arbustos alternados en otra capa.

Este script usa `farm_utils.py` para preparar el terreno antes de entrar al ciclo principal.

## Granja con policultivo

`PolycultureFarm.py` prueba la mecanica de policultivo. Planta cultivos principales en anclas separadas y usa `get_companion()` para saber que companion necesita cada planta y en que coordenada colocarlo.

Los cultivos principales rotan entre arbustos, arboles, zanahorias y pasto. Las anclas estan separadas cada 4 casillas para reducir el riesgo de que un companion sobrescriba otro cultivo principal.

## Laberintos

`MazeSolver.py` crea un laberinto usando `Items.Weird_Substance` sobre un arbusto y busca el tesoro con una exploracion guiada por `measure()`.

El solver corre en bucle infinito: cuando encuentra y cosecha el tesoro, limpia el campo, crea otro laberinto y vuelve a buscar. Si no hay suficiente `Items.Weird_Substance`, planta girasoles, los acelera con `Items.Fertilizer` para infectarlos y cosecha para generar mas sustancia.

Durante la busqueda usa `can_move()` para revisar paredes, guarda las casillas visitadas y evalua todas las salidas disponibles para tomar la que mas reduce la distancia al tesoro. Si llega a un callejon, retrocede por el camino recorrido y prueba otra rama.

## Dinosaurios

`DinosaurBoneHarvester.py` usa `Hats.Dinosaur_Hat` para generar una cola tipo serpiente y recolectar huesos al cambiar de sombrero.

El script sigue un recorrido Hamiltoniano por la granja para evitar chocar con la cola y crecer hasta llenar el campo. Si no hay suficiente cactus para comprar manzanas, primero genera cactus y luego empieza el ciclo de dinosaurio.

`BenchmarkDinosaurSim32.py` ejecuta una variante de una sola corrida en mundo 32 usando `simulate()` para medir rendimiento sin cambiar la granja real.

## Mejoras por revisar

- Probar los scripts `LB_*` con `leaderboard_run()` y ajustar segun los tiempos reales.
- Comparar y adaptar ideas del repo MIT `enihsyou/The-Farmer-Was-Replaced` sin copiar estrategias a ciegas.
- Probar generacion paralela de `Items.Weird_Substance` usando multiples drones.
- Usar `simulate()` para comparar tiempos entre versiones de scripts.
- Revisar si algunos `harvest()` deben depender de `can_harvest()` para evitar acciones innecesarias.
- Completar o eliminar funciones pendientes como `till_all()`.
- Comparar rendimiento entre scripts cuando se prueben dentro del juego.
