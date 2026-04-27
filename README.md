# The Farmer Was Replaced

Este repositorio reune codigos generados por mi para la eficientacion de granjas dentro del juego **The Farmer Was Replaced**.

La idea del proyecto es recopilar los mejores codigos de automatizacion, documentar como funcionan y revisar que posibles mejoras se pueden hacer en cada estrategia.

## Contenido actual

- `SunflowerFarm.py`: script para automatizar la granja de girasoles.
- `MultiCropFarm.py`: script de granja multicultivo con zonas para calabazas, girasoles, cactus, zanahorias, arboles y arbustos.
- `farm_utils.py`: utilidades reutilizables para preparar tierra, plantar columnas y moverse por el mapa.
- `PROJECT_CONTEXT.md`: contexto del proyecto, objetivos, decisiones y mejoras pendientes.

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

La parte interior esta enfocada en calabazas. Durante cada ciclo revisa si hay calabazas muertas o espacios vacios; si encuentra alguno, replanta y espera antes de cosechar. Si todo el bloque esta sano, cosecha la calabaza grande.

Las capas exteriores se usan para otros cultivos:

1. Girasoles en una primera capa externa.
2. Cactus y zanahorias alternados en patron de tablero.
3. Arboles y arbustos alternados en otra capa.

Este script usa `farm_utils.py` para preparar el terreno antes de entrar al ciclo principal.

## Mejoras por revisar

- Ajustar los limites de zonas de la granja multicultivo segun el tamano real del mundo.
- Revisar si algunos `harvest()` deben depender de `can_harvest()` para evitar acciones innecesarias.
- Completar o eliminar funciones pendientes como `till_all()`.
- Comparar rendimiento entre scripts cuando se prueben dentro del juego.
