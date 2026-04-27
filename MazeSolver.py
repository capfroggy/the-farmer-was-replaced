"""
Solver continuo para laberintos en The Farmer Was Replaced.

Flujo:
- genera Weird Substance si no alcanza
- crea un laberinto de campo completo
- busca el tesoro con una DFS fisica guiada por distancia
- cosecha el tesoro y repite para siempre
"""

WEIRD_CROP = Entities.Sunflower


def maze_substance():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level < 1:
		maze_level = 1
	return get_world_size() * 2**(maze_level - 1)


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


def generate_weird_substance(target_amount):
	clear()

	while num_items(Items.Weird_Substance) < target_amount:
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				if num_items(Items.Weird_Substance) >= target_amount:
					return True

				ensure_soil()
				plant(WEIRD_CROP)
				fertilize_until_ready()
				harvest()

				move(North)
			move(East)

	return True


def create_full_maze():
	substance = maze_substance()
	if num_items(Items.Weird_Substance) < substance:
		generate_weird_substance(substance)

	clear()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)
	return True


def tile_key(x, y):
	return x * get_world_size() + y


def current_key():
	return tile_key(get_pos_x(), get_pos_y())


def wrapped_delta(a, b):
	n = get_world_size()
	delta = (b - a) % n
	if delta > n // 2:
		return delta - n
	return delta


def wrapped_distance(x, y, target_x, target_y):
	dx = wrapped_delta(x, target_x)
	dy = wrapped_delta(y, target_y)
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy
	return dx + dy


def next_pos(direction):
	n = get_world_size()
	x = get_pos_x()
	y = get_pos_y()

	if direction == North:
		y = (y + 1) % n
	elif direction == South:
		y = (y - 1) % n
	elif direction == East:
		x = (x + 1) % n
	else:
		x = (x - 1) % n

	return [x, y]


def opposite(direction):
	if direction == North:
		return South
	if direction == South:
		return North
	if direction == East:
		return West
	return East


def try_move_to_treasure(target_x, target_y):
	for direction in [North, East, South, West]:
		pos = next_pos(direction)
		if pos[0] == target_x and pos[1] == target_y and can_move(direction):
			move(direction)
			harvest()
			return True
	return False


def best_direction(target_x, target_y, visited):
	best = None
	best_score = 999999

	for direction in [North, East, South, West]:
		if can_move(direction):
			pos = next_pos(direction)
			key = tile_key(pos[0], pos[1])

			if key not in visited:
				score = wrapped_distance(pos[0], pos[1], target_x, target_y)
				if score < best_score:
					best_score = score
					best = direction

	return best


def solve_maze():
	target_x, target_y = measure()
	visited = {current_key(): True}
	path = []

	while get_entity_type() != Entities.Treasure:
		if try_move_to_treasure(target_x, target_y):
			return True

		direction = best_direction(target_x, target_y, visited)

		if direction != None:
			move(direction)
			visited[current_key()] = True
			path.append(direction)
		else:
			if len(path) == 0:
				return False
			move(opposite(path.pop()))

	harvest()
	return True


def run_forever():
	while True:
		create_full_maze()
		solve_maze()


run_forever()
