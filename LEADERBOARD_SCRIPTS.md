# Leaderboard Scripts

Estos archivos son baselines para clasificar en las tablas de clasificacion.
Cada script `LB_*` intenta cumplir la condicion de exito y terminar.
Cada script `Run_*` llama a `leaderboard_run(...)` con el leaderboard correcto.

## Como usarlos

Ejecuta el archivo `Run_*` de la categoria que quieras probar.

Ejemplo:

```python
leaderboard_run(Leaderboards.Hay_Single, "LB_Hay_Single", 1000)
```

## Categorias principales

| Categoria | Runner | Script |
| --- | --- | --- |
| Fastest Reset | `Run_Fastest_Reset.py` | `LB_Fastest_Reset.py` |
| Maze | `Run_Maze.py` | `LB_Maze.py` |
| Dinosaur | `Run_Dinosaur.py` | `LB_Dinosaur.py` |
| Cactus | `Run_Cactus.py` | `LB_Cactus.py` |
| Sunflowers | `Run_Sunflowers.py` | `LB_Sunflowers.py` |
| Pumpkins | `Run_Pumpkins.py` | `LB_Pumpkins.py` |
| Wood | `Run_Wood.py` | `LB_Wood.py` |
| Carrots | `Run_Carrots.py` | `LB_Carrots.py` |
| Hay | `Run_Hay.py` | `LB_Hay.py` |

## Categorias de un solo dron

| Categoria | Runner | Script |
| --- | --- | --- |
| Maze Single | `Run_Maze_Single.py` | `LB_Maze_Single.py` |
| Cactus Single | `Run_Cactus_Single.py` | `LB_Cactus_Single.py` |
| Sunflowers Single | `Run_Sunflowers_Single.py` | `LB_Sunflowers_Single.py` |
| Pumpkins Single | `Run_Pumpkins_Single.py` | `LB_Pumpkins_Single.py` |
| Wood Single | `Run_Wood_Single.py` | `LB_Wood_Single.py` |
| Carrots Single | `Run_Carrots_Single.py` | `LB_Carrots_Single.py` |
| Hay Single | `Run_Hay_Single.py` | `LB_Hay_Single.py` |

## Notas

- Los scripts de recursos usan metas absolutas, igual que las condiciones del juego.
- Los scripts multi-dron intentan usar `spawn_drone()` cuando esta disponible.
- Los scripts single usan un solo dron, pero recorren todo el grid disponible.
- `LB_Hay_Single.py` usa un barrido serpentino especializado y evita checks/replantado por casilla para reducir ticks.
- `LB_Maze.py` y `LB_Maze_Single.py` reutilizan el laberinto usando `Items.Weird_Substance` sobre el tesoro.
- `LB_Dinosaur.py` usa la variante simulable `DinosaurBoneHarvesterSim32.py`.
- `LB_Fastest_Reset.py` es experimental. La version actual usa calculo recursivo de costos y una ruta fija de unlocks/upgrades para evitar dependencias tempranas.
