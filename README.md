# The Farmer Was Replaced

Este repositorio reune codigos generados por mi para la eficientacion de granjas dentro del juego **The Farmer Was Replaced**.

Por el momento solo llevo la automatizacion de la granja de girasoles, pero despues trabajare en mas scripts para otros tipos de granjas y procesos.

## Contenido actual

- `SunflowerFarm.py`: script para automatizar la granja de girasoles.

## Que hace este script

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
