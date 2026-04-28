TARGET_HAY = 100000000
size = get_world_size()


def harvest_line(direction):
	for _ in range(size - 1):
		harvest()
		move(direction)
	harvest()


def farm_hay_single():
	direction = North

	while num_items(Items.Hay) < TARGET_HAY:
		for _ in range(size):
			harvest_line(direction)

			if num_items(Items.Hay) >= TARGET_HAY:
				return

			move(East)

			if direction == North:
				direction = South
			else:
				direction = North


farm_hay_single()
