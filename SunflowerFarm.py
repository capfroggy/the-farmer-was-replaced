def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)


def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()


def maybe_water():
	if get_water() < 0.5:
		use_item(Items.Water)


def make_buckets():
	# indices 0..15, usaremos 7..15
	b = []
	for _ in range(16):
		b.append([])
	return b


def scan_tile(state):
	ensure_soil()
	maybe_water()

	entity = get_entity_type()

	# Mantener el campo lleno
	if entity != Entities.Sunflower:
		plant(Entities.Sunflower)
		entity = Entities.Sunflower

	# Cuenta total en la granja
	if entity == Entities.Sunflower:
		state["count"] = state["count"] + 1

	# Solo bucketear las maduras
	if can_harvest():
		p = measure()
		state["buckets"][p].append([get_pos_x(), get_pos_y()])


def sweep(action, state=None):
	n = get_world_size()

	for row in range(n):
		if row % 2 == 0:
			for col in range(n):
				if state == None:
					action()
				else:
					action(state)
				if col < n - 1:
					move(East)
		else:
			for col in range(n):
				if state == None:
					action()
				else:
					action(state)
				if col < n - 1:
					move(West)

		if row < n - 1:
			move(North)


def refill_tile():
	ensure_soil()
	maybe_water()

	if get_entity_type() != Entities.Sunflower:
		plant(Entities.Sunflower)


def refill_field():
	move_to(0, 0)
	sweep(refill_tile)
	move_to(0, 0)


def harvest_descending(state):
	# 15 -> 7
	for petals in range(15, 6, -1):
		for pos in state["buckets"][petals]:
			# Si antes de cosechar ya no hay 10, parar
			if state["count"] < 10:
				return

			move_to(pos[0], pos[1])

			# Revalidar por seguridad
			if get_entity_type() == Entities.Sunflower and can_harvest():
				if measure() == petals:
					harvest()
					state["count"] = state["count"] - 1


def sunflower_cycle():
	state = {
		"count": 0,
		"buckets": make_buckets()
	}

	move_to(0, 0)
	sweep(scan_tile, state)
	harvest_descending(state)
	refill_field()


clear()
refill_field()

while True:
	sunflower_cycle()