# Fastest reset baseline.
#
# This version adapts the main ideas from enihsyou's public fastest_reset.py:
# recursive resource-cost planning, repeated unlock routing, and resource-
# specific farmers. The implementation stays local to this project so we can
# debug it step by step inside the leaderboard simulation.


def merge_costs(target, source):
	for item in source:
		if item not in target:
			target[item] = 0
		target[item] += source[item]
	return target


def entity_for_item(item):
	if item == Items.Hay:
		return Entities.Grass
	if item == Items.Wood:
		return Entities.Bush
	if item == Items.Carrot:
		return Entities.Carrot
	if item == Items.Pumpkin:
		return Entities.Pumpkin
	if item == Items.Cactus:
		return Entities.Cactus
	if item == Items.Power:
		return Entities.Sunflower
	return None


def harvest_cost(item, amount):
	entity = entity_for_item(item)
	if entity == None:
		return {}

	needed = amount - num_items(item)
	if needed <= 0:
		return {}

	buffer = get_world_size() * get_world_size() * 2
	seed_cost = get_cost(entity) or {}
	total = {}

	for seed in seed_cost:
		seed_amount = seed_cost[seed] * (needed + buffer)
		total[seed] = seed_amount
		merge_costs(total, harvest_cost(seed, seed_amount))

	return total


def unlock_cost(thing):
	cost = get_cost(thing, num_unlocked(thing)) or {}
	total = {}
	extras = []

	for item in cost:
		total[item] = cost[item]
		extras.append(harvest_cost(item, cost[item]))

	for extra in extras:
		merge_costs(total, extra)

	return total


def wait_for_item(item):
	while num_items(item) == 0:
		pass


def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()


def water_if_available():
	if num_items(Items.Water) > 0 and get_water() < 0.75:
		use_item(Items.Water)


def force_growth_if_possible():
	while not can_harvest():
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		elif num_items(Items.Water) > 0:
			water_if_available()
			return
		else:
			return


def traverse_field(action):
	size = get_world_size()
	for _ in range(size):
		for _ in range(size):
			action()
			move(North)
		move(East)


def move_to(target_x, target_y):
	size = get_world_size()
	cur_x = get_pos_x()
	cur_y = get_pos_y()

	east_steps = (target_x - cur_x) % size
	west_steps = size - east_steps
	if east_steps <= west_steps:
		for _ in range(east_steps):
			move(East)
	else:
		for _ in range(west_steps):
			move(West)

	north_steps = (target_y - cur_y) % size
	south_steps = size - north_steps
	if north_steps <= south_steps:
		for _ in range(north_steps):
			move(North)
	else:
		for _ in range(south_steps):
			move(South)


def farm_hay(amount):
	def tile():
		if can_harvest():
			harvest()
		if num_unlocked(Unlocks.Plant) > 0 and get_entity_type() != Entities.Grass:
			harvest()
			plant(Entities.Grass)

	while num_items(Items.Hay) < amount:
		traverse_field(tile)


def farm_wood(amount):
	def tile():
		crop = Entities.Bush
		if num_unlocked(Unlocks.Trees) > 0 and (get_pos_x() + get_pos_y()) % 2 == 0:
			crop = Entities.Tree

		if can_harvest():
			harvest()
		if get_entity_type() != crop:
			harvest()
			plant(crop)
		water_if_available()

	while num_items(Items.Wood) < amount:
		traverse_field(tile)


def farm_simple_crop(crop, item, amount):
	def tile():
		if can_harvest():
			harvest()
		ensure_soil()
		if get_entity_type() != crop:
			harvest()
		plant(crop)
		water_if_available()

	while num_items(item) < amount:
		traverse_field(tile)


def farm_sunflowers(amount):
	def tile():
		if can_harvest():
			harvest()
		ensure_soil()
		if get_entity_type() != Entities.Sunflower:
			harvest()
		plant(Entities.Sunflower)
		water_if_available()

	while num_items(Items.Power) < amount:
		traverse_field(tile)


reset_pumpkin_ready = False


def farm_pumpkins(amount):
	def plant_tile():
		global reset_pumpkin_ready
		ensure_soil()
		entity = get_entity_type()
		if entity == Entities.Dead_Pumpkin or entity == None:
			reset_pumpkin_ready = False
			plant(Entities.Pumpkin)
		elif entity != Entities.Pumpkin:
			reset_pumpkin_ready = False
			if can_harvest():
				harvest()
			plant(Entities.Pumpkin)
		elif not can_harvest():
			reset_pumpkin_ready = False
		water_if_available()

	global reset_pumpkin_ready
	while num_items(Items.Pumpkin) < amount:
		reset_pumpkin_ready = True
		traverse_field(plant_tile)
		if reset_pumpkin_ready:
			harvest()
		else:
			force_growth_if_possible()


def farm_cactus(amount):
	farm_simple_crop(Entities.Cactus, Items.Cactus, amount)


def farm_weird_substance(amount):
	def tile():
		ensure_soil()
		if get_entity_type() != Entities.Sunflower:
			harvest()
			plant(Entities.Sunflower)

		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		force_growth_if_possible()
		if can_harvest():
			harvest()

	while num_items(Items.Weird_Substance) < amount:
		traverse_field(tile)


def maze_substance():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level < 1:
		maze_level = 1
	return get_world_size() * 2**(maze_level - 1)


def tile_key(x, y):
	return x * get_world_size() + y


def next_pos(direction):
	size = get_world_size()
	x = get_pos_x()
	y = get_pos_y()

	if direction == North:
		y = (y + 1) % size
	elif direction == South:
		y = (y - 1) % size
	elif direction == East:
		x = (x + 1) % size
	else:
		x = (x - 1) % size

	return [x, y]


def opposite(direction):
	if direction == North:
		return South
	if direction == South:
		return North
	if direction == East:
		return West
	return East


def distance_to_target(x, y, target_x, target_y):
	dx = x - target_x
	dy = y - target_y
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy
	return dx + dy


def best_maze_direction(target_x, target_y, visited):
	best = None
	best_score = 999999

	for direction in [North, East, South, West]:
		if can_move(direction):
			pos = next_pos(direction)
			key = tile_key(pos[0], pos[1])
			if key not in visited:
				score = distance_to_target(pos[0], pos[1], target_x, target_y)
				if score < best_score:
					best_score = score
					best = direction

	return best


def solve_maze_once():
	target_x, target_y = measure()
	visited = {tile_key(get_pos_x(), get_pos_y()): True}
	path = []

	while get_entity_type() != Entities.Treasure:
		direction = best_maze_direction(target_x, target_y, visited)

		if direction != None:
			move(direction)
			visited[tile_key(get_pos_x(), get_pos_y())] = True
			path.append(direction)
		else:
			if len(path) == 0:
				return False
			move(opposite(path.pop()))

	harvest()
	return True


def farm_gold(amount):
	while num_items(Items.Gold) < amount:
		cost = maze_substance()
		if num_items(Items.Weird_Substance) < cost:
			farm_weird_substance(cost)

		clear()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, cost)
		solve_maze_once()


def move_and_measure_apple(direction):
	global reset_apple_pos
	if not move(direction):
		return False
	if (get_pos_x(), get_pos_y()) == reset_apple_pos:
		reset_apple_pos = measure()
	return True


def chase_apples_for_bones():
	global reset_apple_pos
	reset_apple_pos = measure()
	move_budget = get_world_size() * get_world_size() * 2

	for _ in range(move_budget):
		target_x, target_y = reset_apple_pos
		moved = False

		if get_pos_x() < target_x and move_and_measure_apple(East):
			moved = True
		elif get_pos_x() > target_x and move_and_measure_apple(West):
			moved = True
		elif get_pos_y() < target_y and move_and_measure_apple(North):
			moved = True
		elif get_pos_y() > target_y and move_and_measure_apple(South):
			moved = True

		if not moved:
			for direction in [North, East, South, West]:
				if move_and_measure_apple(direction):
					moved = True
					break

		if not moved:
			return


def farm_bones(amount):
	while num_items(Items.Bone) < amount:
		farm_cactus(num_items(Items.Cactus) + get_world_size() * get_world_size())
		change_hat(Hats.Dinosaur_Hat)
		chase_apples_for_bones()
		change_hat(Hats.Straw_Hat)


def farm_item(item, amount):
	if num_items(item) >= amount:
		return
	if item == Items.Hay:
		farm_hay(amount)
	elif item == Items.Wood:
		farm_wood(amount)
	elif item == Items.Carrot:
		farm_simple_crop(Entities.Carrot, Items.Carrot, amount)
	elif item == Items.Pumpkin:
		farm_pumpkins(amount)
	elif item == Items.Cactus:
		farm_cactus(amount)
	elif item == Items.Power:
		farm_sunflowers(amount)
	elif item == Items.Weird_Substance:
		farm_weird_substance(amount)
	elif item == Items.Gold:
		farm_gold(amount)
	elif item == Items.Bone:
		farm_bones(amount)


def unlock_step(thing):
	start_level = num_unlocked(thing)
	attempts = 0

	while num_unlocked(thing) == start_level and attempts < 3:
		cost = unlock_cost(thing)
		for item in cost:
			farm_item(item, cost[item])

		if unlock(thing):
			return True
		attempts += 1

	return num_unlocked(thing) > start_level


def run_unlock_route():
	route = [
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Plant,
		Unlocks.Expand,
		Unlocks.Speed,
		Unlocks.Carrots,
		Unlocks.Grass,
		Unlocks.Trees,
		Unlocks.Trees,
		Unlocks.Expand,
		Unlocks.Carrots,
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Watering,
		Unlocks.Watering,
		Unlocks.Carrots,
		Unlocks.Grass,
		Unlocks.Sunflowers,
		Unlocks.Fertilizer,
		Unlocks.Watering,
		Unlocks.Speed,
		Unlocks.Pumpkins,
		Unlocks.Watering,
		Unlocks.Polyculture,
		Unlocks.Speed,
		Unlocks.Expand,
		Unlocks.Fertilizer,
		Unlocks.Mazes,
		Unlocks.Megafarm,
		Unlocks.Trees,
		Unlocks.Trees,
		Unlocks.Carrots,
		Unlocks.Watering,
		Unlocks.Pumpkins,
		Unlocks.Pumpkins,
		Unlocks.Expand,
		Unlocks.Cactus,
		Unlocks.Hats,
		Unlocks.Dinosaurs,
		Unlocks.Dinosaurs,
		Unlocks.Pumpkins,
		Unlocks.Polyculture,
		Unlocks.Mazes,
		Unlocks.Mazes,
		Unlocks.Grass,
		Unlocks.Megafarm,
		Unlocks.Megafarm,
		Unlocks.Trees,
		Unlocks.Fertilizer,
		Unlocks.Fertilizer,
		Unlocks.Watering,
		Unlocks.Carrots,
		Unlocks.Carrots,
		Unlocks.Pumpkins,
		Unlocks.Expand,
		Unlocks.Megafarm,
		Unlocks.Cactus,
		Unlocks.Cactus,
		Unlocks.Dinosaurs,
		Unlocks.Dinosaurs,
		Unlocks.Dinosaurs,
		Unlocks.Mazes,
		Unlocks.Leaderboard,
	]

	for thing in route:
		if num_unlocked(Unlocks.Leaderboard) > 0:
			return
		unlock_step(thing)

	while num_unlocked(Unlocks.Leaderboard) == 0:
		unlock_step(Unlocks.Leaderboard)


run_unlock_route()
