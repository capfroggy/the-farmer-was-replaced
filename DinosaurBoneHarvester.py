"""
Recolector de huesos con Dinosaur Hat para The Farmer Was Replaced.

El dinosaurio funciona como una serpiente: cada manzana aumenta la cola y al
quitarse el sombrero se cosechan huesos iguales a `longitud_de_cola ** 2`.

Este script usa un recorrido Hamiltoniano para llenar la granja sin chocar con
la cola. Cuando el dinosaurio ya no puede moverse, cambia de sombrero y cosecha
la cola automaticamente.
"""

DINO_HAT = Hats.Dinosaur_Hat
HARVEST_HAT = Hats.Wizard_Hat
CACTUS_BUFFER = 8


def use_even_world_size():
	size = get_world_size()
	if size % 2 == 1 and size > 2:
		set_world_size(size - 1)


def full_tail_cactus_target():
	size = get_world_size()
	return size * size + CACTUS_BUFFER


def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()


def use_fertilizer_if_available():
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)


def generate_cactus(target_amount):
	clear()

	while num_items(Items.Cactus) < target_amount:
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				if num_items(Items.Cactus) >= target_amount:
					return True

				ensure_soil()
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)

				while not can_harvest() and num_items(Items.Fertilizer) > 0:
					use_fertilizer_if_available()

				if can_harvest():
					harvest()

				move(North)
			move(East)

	return True


def ensure_cactus_for_dinosaur():
	target = full_tail_cactus_target()
	if num_items(Items.Cactus) < target:
		generate_cactus(target)


def safe_move(direction):
	return move(direction)


def walk(direction, steps):
	for _ in range(steps):
		if not safe_move(direction):
			return False
	return True


def walk_even_world_cycle():
	size = get_world_size()

	if not walk(East, size - 1):
		return False

	for row in range(1, size):
		if not walk(North, 1):
			return False

		if row % 2 == 1:
			if not walk(West, size - 2):
				return False
		else:
			if not walk(East, size - 2):
				return False

	if not walk(West, 1):
		return False

	if not walk(South, size - 1):
		return False

	return True


def harvest_tail():
	change_hat(HARVEST_HAT)


def dinosaur_cycle():
	ensure_cactus_for_dinosaur()
	clear()
	change_hat(DINO_HAT)

	while True:
		if not walk_even_world_cycle():
			harvest_tail()
			return


use_even_world_size()

while True:
	dinosaur_cycle()
