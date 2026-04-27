def farm_column(crop):
	can_plant_list = [None, Entities.Dead_Pumpkin, Entities.Grass]
	for i in range(get_world_size()):
		if can_harvest():
			harvest()
		if get_entity_type() in can_plant_list:
			plant(crop)
		move(North)


def plant_column(crop):
	need_till_list = [Entities.Carrot, Entities.Pumpkin, Entities.Cactus, Entities.Sunflower]
	for i in range(get_world_size()):
		if crop in need_till_list:
			till()
		plant(crop)
		move(North)


def plant_columns(crops):
	for i in range(len(crops)):
		crop = crops[i]
		plant_column(crop)
		move(East)


def till_columns(n):
	for i in range(n):
		for j in range(get_world_size()):
			till()
			move(North)
		move(East)
	for i in range(n):
		move(West)


def till_grids(n, m):
	for i in range(n):
		for j in range(get_world_size()):
			if j < m:
				harvest()
				till()
			move(North)
		move(East)
	for i in range(n):
		move(West)


def till_all():
	pass


def goto_naive(x_target, y_target):
	n = get_world_size()
	curX = get_pos_x()
	curY = get_pos_y()

	# Calcula la ruta horizontal mas corta considerando que el mapa se envuelve.
	dx = (x_target - curX) % n

	if dx <= n // 2:
		steps_x = dx
		dirX = East
	else:
		steps_x = n - dx
		dirX = West

	# Calcula la ruta vertical mas corta considerando que el mapa se envuelve.
	dy = (y_target - curY) % n

	if dy <= n // 2:
		steps_y = dy
		dirY = North
	else:
		steps_y = n - dy
		dirY = South

	while steps_x > 0 or steps_y > 0:
		if steps_x >= steps_y and steps_x > 0:
			move(dirX)
			steps_x -= 1
		elif steps_y > 0:
			move(dirY)
			steps_y -= 1
