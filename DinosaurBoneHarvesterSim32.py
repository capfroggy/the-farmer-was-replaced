# Dinosaur simulation, one run, 32x32 world.
#
# This file is meant to be executed through simulate() so it must terminate.


def measure_apple():
	global apple_pos
	global squares_occupied
	apple_pos = measure()
	squares_occupied += 1


def move_and_check_apple(direction):
	global apple_pos

	if not move(direction):
		return False
	if (get_pos_x(), get_pos_y()) == apple_pos:
		measure_apple()

	return True


def move_to_col(target_x_pos, do_measure=True):
	curr_x = get_pos_x()
	direction = West
	if curr_x < target_x_pos:
		direction = East

	for _ in range(abs(target_x_pos - curr_x)):
		this_check = move
		if do_measure:
			this_check = move_and_check_apple
		if not this_check(direction):
			return False

	return True


def move_to_row(target_y_pos, do_measure=True):
	curr_y = get_pos_y()
	direction = South
	if curr_y < target_y_pos:
		direction = North

	for _ in range(abs(target_y_pos - curr_y)):
		this_check = move
		if do_measure:
			this_check = move_and_check_apple
		if not this_check(direction):
			return False

	return True


def transition_to_stage_2():
	global offlimit_columns_stage1

	if not move_to_col(world_size_minus_one):
		return False
	if not move_to_row(0):
		return False

	offlimit_columns_stage1 = {}
	return False


def transition_to_stage_1():
	global offlimit_columns_stage2

	if not move_to_col(0):
		return False
	if not move_to_row(world_size_minus_one):
		return False

	offlimit_columns_stage2 = {}
	return False


def stage_1_apple_collect():
	global offlimit_columns_stage2

	apple_pos_x, apple_pos_y = apple_pos
	if apple_pos_y == 0 or apple_pos_x in edge_positions or (apple_pos_x in offlimit_columns_stage1 and apple_pos_y <= offlimit_columns_stage1[apple_pos_x]):
		return transition_to_stage_2()

	target_x_pos = apple_pos_x
	if apple_pos_x % 2 == 0:
		target_x_pos = apple_pos_x - 1

	if target_x_pos <= get_pos_x():
		return transition_to_stage_2()

	if not move_to_col(target_x_pos):
		return False
	if not move_to_row(apple_pos_y):
		return False

	offlimit_columns_stage2[target_x_pos] = apple_pos_y
	offlimit_columns_stage2[target_x_pos + 1] = apple_pos_y
	if not move_and_check_apple(East):
		return False
	return move_to_row(world_size_minus_one)


def stage_2_apple_collect():
	global offlimit_columns_stage1

	apple_pos_x, apple_pos_y = apple_pos
	if apple_pos_y == world_size_minus_one or apple_pos_x in edge_positions or (apple_pos_x in offlimit_columns_stage2 and apple_pos_y >= offlimit_columns_stage2[apple_pos_x]):
		return transition_to_stage_1()

	target_x_pos = apple_pos_x
	if apple_pos_x % 2 == 1:
		target_x_pos = apple_pos_x + 1

	if target_x_pos >= get_pos_x():
		return transition_to_stage_1()

	if not move_to_col(target_x_pos):
		return False
	if not move_to_row(apple_pos_y):
		return False

	offlimit_columns_stage1[target_x_pos] = apple_pos_y
	offlimit_columns_stage1[target_x_pos - 1] = apple_pos_y
	if not move_and_check_apple(West):
		return False
	return move_to_row(0)


def move_to_right_col_wavy():
	for x in range(world_size):
		if x % 2:
			target_y = 1
			if x in offlimit_columns_stage1:
				target_y = offlimit_columns_stage1[x] + 1

			while get_pos_y() != target_y:
				if not move(South):
					return False
			if x < world_size_minus_one:
				if not move(East):
					return False
		else:
			while get_pos_y() != world_size_minus_one:
				if not move(North):
					return False
			if x < world_size_minus_one:
				if not move(East):
					return False

	return True


def find_top_left():
	while get_pos_x() > 0:
		if not move(West):
			return False
	while get_pos_y() < world_size_minus_one:
		if not move(North):
			return False
	return True


def transition_to_route():
	if not find_top_left():
		return False
	if not move_to_right_col_wavy():
		return False
	while get_pos_y() != 0:
		if not move(South):
			return False
	while get_pos_x() != 0:
		if not move(West):
			return False
	return True


def run_dinosaur_once():
	global world_size
	global world_size_minus_one
	global edge_positions
	global offlimit_columns_stage1
	global offlimit_columns_stage2
	global apple_pos
	global squares_occupied
	global game_complete

	set_world_size(32)
	world_size = get_world_size()
	world_size_minus_one = world_size - 1
	edge_positions = [0, world_size_minus_one]
	offlimit_columns_stage1 = {}
	offlimit_columns_stage2 = {}

	clear()
	change_hat(Hats.Dinosaur_Hat)

	apple_pos = measure()
	squares_occupied = 1
	game_complete = False

	move_to_row(world_size_minus_one)

	while True:
		while stage_1_apple_collect() and get_pos_x() < world_size_minus_one:
			pass

		while stage_2_apple_collect() and get_pos_x() > 0:
			pass

		if squares_occupied > world_size_minus_one * 4 - 4:
			break

	if transition_to_route():
		while True:
			for i in range(world_size // 2):
				game_complete = not move_to_row(world_size_minus_one, False)
				game_complete = game_complete or not move(East)
				game_complete = game_complete or not move_to_row(1, False)
				if i != world_size // 2 - 1:
					game_complete = game_complete or not move(East)

				if game_complete:
					break

			game_complete = game_complete or not move_to_row(0, False)
			game_complete = game_complete or not move_to_col(0, False)

			if game_complete:
				break

	change_hat(Hats.Straw_Hat)


run_dinosaur_once()
