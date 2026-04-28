import leaderboard_common


def farm_gold_until(amount):
	import leaderboard_maze_common
	leaderboard_maze_common.farm_maze_gold_until(amount)


def farm_bone_until(amount):
	while num_items(Items.Bone) < amount:
		leaderboard_common.farm_item_basic(Items.Cactus, num_items(Items.Cactus) + get_world_size() * get_world_size())
		change_hat(Hats.Dinosaur_Hat)
		chase_apples_for_bones()
		change_hat(Hats.Straw_Hat)


def move_and_measure_apple(direction):
	global reset_apple_pos
	if not move(direction):
		return False
	if (get_pos_x(), get_pos_y()) == reset_apple_pos:
		reset_apple_pos = measure()
	return True


def try_dino_direction(direction):
	return move_and_measure_apple(direction)


def chase_apples_for_bones():
	global reset_apple_pos
	reset_apple_pos = measure()
	move_budget = get_world_size() * get_world_size() * 2

	for _ in range(move_budget):
		target_x, target_y = reset_apple_pos
		moved = False

		if get_pos_x() < target_x and try_dino_direction(East):
			moved = True
		elif get_pos_x() > target_x and try_dino_direction(West):
			moved = True
		elif get_pos_y() < target_y and try_dino_direction(North):
			moved = True
		elif get_pos_y() > target_y and try_dino_direction(South):
			moved = True

		if not moved:
			for direction in [North, East, South, West]:
				if try_dino_direction(direction):
					moved = True
					break

		if not moved:
			return


def farm_item(item, amount):
	if num_items(item) >= amount:
		return
	if item == Items.Gold:
		farm_gold_until(amount)
	elif item == Items.Bone:
		farm_bone_until(amount)
	else:
		leaderboard_common.farm_item_basic(item, amount)


def ensure_cost(thing):
	cost = get_cost(thing)
	if cost == None:
		return
	for item in cost:
		farm_item(item, cost[item])


def unlock_when_possible(thing):
	if get_cost(thing) != None:
		ensure_cost(thing)
	unlock(thing)


unlock_order = [
	Unlocks.Loops,
	Unlocks.Speed,
	Unlocks.Expand,
	Unlocks.Plant,
	Unlocks.Senses,
	Unlocks.Operators,
	Unlocks.Variables,
	Unlocks.Functions,
	Unlocks.Trees,
	Unlocks.Carrots,
	Unlocks.Pumpkins,
	Unlocks.Cactus,
	Unlocks.Sunflowers,
	Unlocks.Mazes,
	Unlocks.Dinosaurs,
	Unlocks.Leaderboard,
]


while num_unlocked(Unlocks.Leaderboard) == 0:
	for thing in unlock_order:
		if num_unlocked(Unlocks.Leaderboard) > 0:
			break
		unlock_when_possible(thing)
