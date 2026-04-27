"""
Granja multicultivo para The Farmer Was Replaced.

Este script divide el campo en zonas:
- calabazas en el area interior
- girasoles en una capa exterior
- cactus y zanahorias alternados
- arboles y arbustos alternados

Depende de farm_utils.py para preparar secciones del terreno.
"""

import farm_utils

clear()
change_hat(Hats.Wizard_Hat)
size = get_world_size()

# Prepara el terreno dejando fuera el borde mas externo.
farm_utils.till_grids(size - 4, size - 4)

while True:
	# Se asume que todas las calabazas estan sanas al inicio de cada ciclo.
	harvestPumpkin = True

	for pos_x in range(size):
		for pos_y in range(size):

			# Area interior: zona principal de calabazas.
			# Las calabazas aprovechan patrones cuadrados adyacentes para crecer mejor.
			if pos_x < 15 and pos_y < 15:

				# Si la casilla esta vacia o tiene una calabaza muerta,
				# se replanta y se evita cosechar la calabaza grande todavia.
				if get_entity_type() == Entities.Dead_Pumpkin or get_entity_type() == None:
					harvestPumpkin = False
					plant(Entities.Pumpkin)

			# Capas exteriores: se cosecha lo maduro y se replanta por zona.
			else:
				harvest()

				if pos_x < 19 and pos_y < 19:
					plant(Entities.Sunflower)

				elif pos_x < 23 and pos_y < 23:
					if (pos_x + pos_y) % 2 == 0:
						plant(Entities.Cactus)
					else:
						plant(Entities.Carrot)

				elif pos_x < 28 and pos_y < 28:
					if (pos_x + pos_y) % 2 == 0:
						plant(Entities.Tree)
					else:
						plant(Entities.Bush)

			move(North)

		move(East)

	# Si no hubo calabazas muertas o faltantes, se cosecha la calabaza grande.
	if harvestPumpkin:
		harvest()
