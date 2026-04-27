# Project Context

## Proposito

Este repositorio recopila codigos para eficientar granjas en **The Farmer Was Replaced**.
La meta es guardar los mejores scripts disponibles, documentar como funcionan y detectar posibles mejoras para futuras versiones.

## Instruccion de trabajo

Leer este archivo al inicio de cada nueva request relacionada con el proyecto.
Actualizarlo cuando aparezca informacion importante sobre objetivos, scripts, decisiones o mejoras pendientes.

## Estado actual

- Repositorio publico: `capfroggy/the-farmer-was-replaced`.
- Rama principal: `main`.
- El proyecto usa scripts estilo Python del juego y depende de las APIs internas de The Farmer Was Replaced.
- Se mantiene texto en ASCII para evitar problemas de codificacion en terminales Windows.

## Scripts incluidos

- `SunflowerFarm.py`: automatiza una granja de girasoles. Mantiene el campo sembrado, clasifica girasoles cosechables por petalos y cosecha primero los de mayor valor.
- `MultiCropFarm.py`: granja multicultivo. Divide el campo en zonas para calabazas, girasoles, cactus, zanahorias, arboles y arbustos.
- `farm_utils.py`: funciones reutilizables para preparar terreno, plantar columnas y moverse por el mapa.

## Informacion importante de la granja multicultivo

- Usa `farm_utils.till_grids(size - 4, size - 4)` para preparar el terreno dejando fuera una zona de borde.
- Cambia al sombrero `Hats.Wizard_Hat` al iniciar.
- La zona interior usa calabazas y solo cosecha la calabaza grande si no detecta calabazas muertas o casillas vacias durante el ciclo.
- Las capas exteriores plantan girasoles, luego alternan cactus/zanahoria y finalmente alternan arbol/arbusto.
- Los limites actuales estan fijos en coordenadas `15`, `19`, `23` y `28`, por lo que una mejora probable es adaptarlos dinamicamente a `get_world_size()`.

## Posibles mejoras pendientes

- Parametrizar limites de zonas para distintos tamanos de mundo.
- Revisar si conviene validar `can_harvest()` antes de algunos `harvest()` en la granja multicultivo.
- Completar `till_all()` o eliminarlo si no se usa.
- Unificar nombres de variables y estilo entre scripts.
- Documentar rendimiento esperado de cada granja cuando se pruebe dentro del juego.
