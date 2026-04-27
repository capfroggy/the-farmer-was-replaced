"""
Granja multicultivo con policultivo para The Farmer Was Replaced.

La idea es plantar cultivos principales en posiciones separadas y usar
`get_companion()` para colocar el companion exacto que pide cada planta.

Se usan anclas cada 4 casillas porque las preferencias de companion aparecen
dentro de 3 movimientos. Asi se evita que los companions sobrescriban los
cultivos principales la mayor parte del tiempo.
"""

MAIN_CROPS = [Entities.Bush, Entities.Tree, Entities.Carrot, Entities.Grass]
ANCHOR_STEP = 4


def move_to(x_target, y_target):
	n = get_world_size()
	cur_x = get_pos_x()
	cur_y = get_pos_y()

	dx = (x_target - cur_x) % n
	if dx <= n // 2:
		for _ in range(dx):
			move(East)
	else:
		for _ in range(n - dx):
			move(West)

	dy = (y_target - cur_y) % n
	if dy <= n // 2:
		for _ in range(dy):
			move(North)
	else:
		for _ in range(n - dy):
			move(South)


def needs_soil(crop):
	return crop == Entities.Carrot


def prepare_ground(crop):
	if needs_soil(crop):
		if get_ground_type() != Grounds.Soil:
			till()


def crop_for_anchor(anchor_index):
	return MAIN_CROPS[anchor_index % len(MAIN_CROPS)]


def is_anchor(x, y):
	return x % ANCHOR_STEP == 0 and y % ANCHOR_STEP == 0


def plant_crop(crop):
	prepare_ground(crop)
	if get_entity_type() != crop:
		if can_harvest():
			harvest()
		plant(crop)


def place_companion(origin_x, origin_y, companion_crop, companion_x, companion_y):
	move_to(companion_x, companion_y)

	# Protege los cultivos principales. Si el juego pide un anchor como companion,
	# se prioriza no destruir ese cultivo principal.
	if not is_anchor(companion_x, companion_y):
		plant_crop(companion_crop)

	move_to(origin_x, origin_y)


def maintain_anchor(x, y, crop):
	move_to(x, y)

	if can_harvest():
		harvest()

	plant_crop(crop)

	companion = get_companion()
	if companion != None:
		companion_crop, companion_pos = companion
		companion_x, companion_y = companion_pos
		place_companion(x, y, companion_crop, companion_x, companion_y)


def run_polyculture_cycle():
	anchor_index = 0
	size = get_world_size()

	for x in range(0, size, ANCHOR_STEP):
		for y in range(0, size, ANCHOR_STEP):
			crop = crop_for_anchor(anchor_index)
			maintain_anchor(x, y, crop)
			anchor_index = anchor_index + 1


clear()

while True:
	run_polyculture_cycle()
