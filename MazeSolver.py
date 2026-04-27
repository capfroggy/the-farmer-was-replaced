"""
Solver rapido para laberintos en The Farmer Was Replaced.

Crea un laberinto de campo completo y busca el tesoro con una DFS fisica
guiada por la posicion de `measure()`. A diferencia de un wall-follow simple,
recuerda casillas visitadas para evitar vueltas innecesarias.
"""


def maze_substance():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level < 1:
		maze_level = 1
	return get_world_size() * 2**(maze_level - 1)


def create_full_maze():
	clear()
	plant(Entities.Bush)

	substance = maze_substance()
	if num_items(Items.Weird_Substance) < substance:
		return False

	use_item(Items.Weird_Substance, substance)
	return True


def tile_key(x, y):
	return x * get_world_size() + y


def current_key():
	return tile_key(get_pos_x(), get_pos_y())


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


def add_direction(directions, direction):
	for item in directions:
		if item == direction:
			return
	directions.append(direction)


def direction_priority(target_x, target_y):
	n = get_world_size()
	x = get_pos_x()
	y = get_pos_y()
	directions = []

	dx = (target_x - x) % n
	dy = (target_y - y) % n

	if dx != 0:
		if dx <= n // 2:
			add_direction(directions, East)
		else:
			add_direction(directions, West)

	if dy != 0:
		if dy <= n // 2:
			add_direction(directions, North)
		else:
			add_direction(directions, South)

	add_direction(directions, North)
	add_direction(directions, East)
	add_direction(directions, South)
	add_direction(directions, West)

	return directions


def is_target_pos(pos, target_x, target_y):
	return pos[0] == target_x and pos[1] == target_y


def try_move_to_treasure(target_x, target_y):
	for direction in [North, East, South, West]:
		pos = next_pos(direction)
		if is_target_pos(pos, target_x, target_y) and can_move(direction):
			move(direction)
			harvest()
			return True
	return False


def solve_maze():
	target_x, target_y = measure()
	visited = {current_key(): True}
	path = []

	while get_entity_type() != Entities.Treasure:
		if try_move_to_treasure(target_x, target_y):
			return True

		moved = False
		directions = direction_priority(target_x, target_y)

		for direction in directions:
			pos = next_pos(direction)
			key = tile_key(pos[0], pos[1])

			if key not in visited and can_move(direction):
				move(direction)
				visited[current_key()] = True
				path.append(direction)
				moved = True
				break

		if not moved:
			if len(path) == 0:
				return False

			move(opposite(path.pop()))

	harvest()
	return True


def run_maze_once():
	if create_full_maze():
		return solve_maze()
	return False


run_maze_once()
