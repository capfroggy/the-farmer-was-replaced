# Hay Single leaderboard strategy.
#
# Inspired by enihsyou's MIT-licensed hay_single.py:
# https://github.com/enihsyou/The-Farmer-Was-Replaced
#
# The key optimization is to avoid sweeping the whole 8x8 field. We shrink the
# simulation to 5x5 and harvest two grass tiles that repeatedly ask for bushes
# as their polyculture companion.

TARGET_HAY = 100000000
WATER_TARGET = 0.68
LEFT_GRASS = (0, 0)
RIGHT_GRASS = (1, 0)


def water_until_ready():
	while get_water() < WATER_TARGET:
		use_item(Items.Water)


def plant_companion_bushes():
	set_world_size(5)

	for direction in [
		North,
		North,
		North,
		North,
		East,
		South,
		South,
		South,
		East,
		North,
		North,
		North,
		North,
		East,
		North,
		East,
		North,
		North,
		West,
		North,
		East,
		North,
	]:
		move(direction)
		plant(Entities.Bush)

	move(East)


def harvest_until_companion(target_pos):
	harvest()
	companion, pos = get_companion()

	while companion != Entities.Bush or pos == target_pos:
		harvest()
		companion, pos = get_companion()


def warmup_pair():
	water_until_ready()
	harvest_until_companion(RIGHT_GRASS)
	move(East)

	water_until_ready()
	harvest_until_companion(LEFT_GRASS)
	move(West)


def harvest_pair_with_water():
	if get_water() < WATER_TARGET:
		use_item(Items.Water)
	harvest_until_companion(RIGHT_GRASS)
	move(East)

	if get_water() < WATER_TARGET:
		use_item(Items.Water)
	harvest_until_companion(LEFT_GRASS)
	move(West)


def harvest_pair_fast():
	harvest()
	if num_items(Items.Hay) >= TARGET_HAY:
		return True
	companion, pos = get_companion()
	while companion != Entities.Bush or pos == RIGHT_GRASS:
		harvest()
		companion, pos = get_companion()
	move(East)

	harvest()
	if num_items(Items.Hay) >= TARGET_HAY:
		return True
	companion, pos = get_companion()
	while companion != Entities.Bush or pos == LEFT_GRASS:
		harvest()
		companion, pos = get_companion()
	move(West)

	return False


plant_companion_bushes()
warmup_pair()

for _ in range(604):
	harvest_pair_with_water()

while True:
	if harvest_pair_fast():
		break
