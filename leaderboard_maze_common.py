# Shared maze leaderboard helpers.


def maze_substance():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level < 1:
		maze_level = 1
	return get_world_size() * 2**(maze_level - 1)


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


def solve_to_treasure():
	target_x, target_y = measure()
	visited = {current_key(): True}
	path = []

	while get_entity_type() != Entities.Treasure:
		direction = best_direction(target_x, target_y, visited)

		if direction != None:
			move(direction)
			visited[current_key()] = True
			path.append(direction)
		else:
			if len(path) == 0:
				return False
			move(opposite(path.pop()))

	return True


def create_maze():
	clear()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, maze_substance())


def farm_maze_gold_until(target):
	create_maze()

	while num_items(Items.Gold) < target:
		if solve_to_treasure():
			use_item(Items.Weird_Substance, maze_substance())
		else:
			create_maze()
