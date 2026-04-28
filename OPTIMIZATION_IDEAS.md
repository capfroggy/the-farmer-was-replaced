# Optimization Ideas

Este documento separa ideas de optimizacion de los scripts principales.
Sirve para probar estrategias antes de moverlas a codigo productivo.

## Nuevas funciones desbloqueadas

- `set_execution_speed(speed)`: reduce o aumenta la velocidad de ejecucion durante pruebas.
- `set_world_size(size)`: cambia temporalmente el tamano del grid durante pruebas.
- `simulate(filename, unlocks, items, globals, seed, speedup)`: prueba un archivo sin cambiar la granja real y devuelve el tiempo simulado.
- `spawn_drone(function)`: crea un dron adicional que ejecuta una funcion propia.
- `max_drones()`: devuelve la cantidad maxima de drones disponibles.
- `num_drones()`: devuelve cuantos drones existen actualmente.

## Mejoras claras para el proyecto actual

1. Produccion de Weird Substance con multiples drones.

El cuello de botella del `MazeSolver.py` actual aparece cuando falta `Items.Weird_Substance`. Hoy un solo dron planta, fertiliza y cosecha casilla por casilla. Con Mega Farm, el dron principal puede moverse por columnas y crear drones trabajadores para producir sustancia en paralelo.

2. Benchmark con simulaciones.

`simulate()` permite comparar versiones del solver sin destruir la granja real. Podemos crear archivos separados como `MazeSolver.py`, `MazeSolverMultiDrone.py` y `MazeSolverWallFollow.py`, correrlos con la misma seed y comparar tiempos.

3. Debug con mundo reducido.

Para inspeccionar algoritmos nuevos conviene usar `set_world_size()` y `set_execution_speed()` en archivos de prueba. Esto ayuda a detectar bucles o movimientos raros sin esperar en un laberinto grande.

4. Busqueda multi-dron del laberinto.

Es posible intentar que dos o mas drones busquen el tesoro desde la misma entrada con estrategias distintas, por ejemplo mano izquierda y mano derecha. Sin embargo, esto necesita coordinacion para evitar que drones sigan corriendo despues de que otro coseche el tesoro.

## Ideas importadas del repo de referencia MIT

Referencia: `https://github.com/enihsyou/The-Farmer-Was-Replaced`.

- `hay_single.py`: usa `set_world_size(5)` y dos tiles de Grass con companion Bush. Ya se adapto en `LB_Hay_Single.py`; falta medir si baja de 3 horas.
- `leaderboards.py`: usa `speedup=40960` en `leaderboard_run()`. Ya se adapto en los `Run_*.py` para acelerar pruebas.
- `fastest_reset.py`: usa costos recursivos y una ruta fija de upgrades repetidos. Ya se adapto parcialmente en `LB_Fastest_Reset.py`, pero sigue siendo experimental.
- `maze.py` y `maze_single.py`: usan una representacion mas completa del laberinto y pueden mejorar nuestros solvers de `LB_Maze.py`/`LB_Maze_Single.py`.
- `cactus_single.py`: resuelve cactus con ordenamiento local usando `measure()`/`swap()`. Candidato fuerte para reemplazar nuestros cactus basicos.
- `dianosaus.py`: tiene ruta de dinosaurio con rank alto. Conviene compararlo con nuestro `DinosaurBoneHarvester.py` cuando el archivo local del usuario este listo para integrarse.

## Prototipo: generador paralelo de Weird Substance

Este enfoque puede reemplazar `generate_weird_substance()` despues de probarlo.

```python
WEIRD_CROP = Entities.Sunflower


def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()


def wait_for_fertilizer():
	while num_items(Items.Fertilizer) == 0:
		pass


def fertilize_until_ready():
	wait_for_fertilizer()
	use_item(Items.Fertilizer)

	while not can_harvest():
		wait_for_fertilizer()
		use_item(Items.Fertilizer)


def produce_weird_column():
	for _ in range(get_world_size()):
		ensure_soil()
		plant(WEIRD_CROP)
		fertilize_until_ready()
		harvest()
		move(North)


def generate_weird_substance_parallel(target_amount):
	clear()

	while num_items(Items.Weird_Substance) < target_amount:
		for _ in range(get_world_size()):
			if num_items(Items.Weird_Substance) >= target_amount:
				return True

			if num_drones() < max_drones():
				spawn_drone(produce_weird_column)

			move(East)

		while num_drones() > 1:
			pass

	return True
```

## Prototipo: benchmark con simulation

Este archivo podria llamarse `BenchmarkMazeSolvers.py`.

```python
def benchmark_maze_solver(filename):
	sim_unlocks = Unlocks
	sim_items = {
		Items.Weird_Substance: 100000,
		Items.Fertilizer: 100000,
	}
	sim_globals = {}
	seed = 1
	speedup = 64

	return simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)


time_current = benchmark_maze_solver("MazeSolver")
```

## Recomendacion

La primera optimizacion que conviene convertir en script real es `generate_weird_substance_parallel()`, porque no cambia la logica delicada del laberinto y aprovecha Mega Farm en una tarea perfectamente paralelizable.

La busqueda multi-dron del tesoro puede ser la siguiente mejora, pero necesita mas pruebas porque todos los drones comparten el mismo laberinto y el tesoro desaparece cuando uno lo cosecha.
