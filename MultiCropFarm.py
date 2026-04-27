"""
Granja multicultivo para The Farmer Was Replaced.

Este script divide el campo en zonas:
- calabazas en el area interior
- girasoles en una capa exterior
- cactus y zanahorias alternados
- arboles y arbustos alternados

Los limites de cada zona se calculan automaticamente con el tamano actual
del mundo, manteniendo una distribucion similar a la version 32x32 original.

Depende de farm_utils.py para preparar secciones del terreno.
"""

import farm_utils


def get_layout(size):
	# La version original usaba 15, 19, 23 y 28 en un area activa de 28 casillas.
	active_limit = size - size // 8
	if active_limit < 1:
		active_limit = size

	pumpkin_limit = active_limit * 15 // 28
	sunflower_limit = active_limit * 19 // 28
	mixed_limit = active_limit * 23 // 28
	tree_limit = active_limit

	if pumpkin_limit < 1:
		pumpkin_limit = 1
	if sunflower_limit <= pumpkin_limit:
		sunflower_limit = pumpkin_limit + 1
	if mixed_limit <= sunflower_limit:
		mixed_limit = sunflower_limit + 1
	if tree_limit <= mixed_limit:
		tree_limit = mixed_limit + 1

	if sunflower_limit > size:
		sunflower_limit = size
	if mixed_limit > size:
		mixed_limit = size
	if tree_limit > size:
		tree_limit = size

	return [pumpkin_limit, sunflower_limit, mixed_limit, tree_limit]


clear()
change_hat(Hats.Wizard_Hat)
size = get_world_size()
layout = get_layout(size)
pumpkin_limit = layout[0]
sunflower_limit = layout[1]
mixed_limit = layout[2]
tree_limit = layout[3]

# Prepara el terreno activo y deja un borde exterior proporcional.
farm_utils.till_grids(tree_limit, tree_limit)

while True:
	# Se asume que todas las calabazas estan sanas al inicio de cada ciclo.
	harvest_pumpkin = True

	for pos_x in range(size):
		for pos_y in range(size):

			# Area interior: zona principal de calabazas.
			# Las calabazas aprovechan patrones cuadrados adyacentes para crecer mejor.
			if pos_x < pumpkin_limit and pos_y < pumpkin_limit:

				# Si la casilla esta vacia o tiene una calabaza muerta,
				# se replanta y se evita cosechar la calabaza grande todavia.
				if get_entity_type() == Entities.Dead_Pumpkin or get_entity_type() == None:
					harvest_pumpkin = False
					plant(Entities.Pumpkin)

			# Capas exteriores: se cosecha lo maduro y se replanta por zona.
			else:
				harvest()

				if pos_x < sunflower_limit and pos_y < sunflower_limit:
					plant(Entities.Sunflower)

				elif pos_x < mixed_limit and pos_y < mixed_limit:
					if (pos_x + pos_y) % 2 == 0:
						plant(Entities.Cactus)
					else:
						plant(Entities.Carrot)

				elif pos_x < tree_limit and pos_y < tree_limit:
					if (pos_x + pos_y) % 2 == 0:
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)

			move(North)

		move(East)

	# Si no hubo calabazas muertas o faltantes, se cosecha la calabaza grande.
	if harvest_pumpkin:
		harvest()
