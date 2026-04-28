# Shared helpers for leaderboard qualification scripts.

LB_CROP = None
LB_ITEM = None
LB_TARGET = 0
LB_NEEDS_SOIL = False


def configure_crop(crop, item, target, needs_soil):
	global LB_CROP
	global LB_ITEM
	global LB_TARGET
	global LB_NEEDS_SOIL
	LB_CROP = crop
	LB_ITEM = item
	LB_TARGET = target
	LB_NEEDS_SOIL = needs_soil


def ensure_soil():
	if get_ground_type() != Grounds.Soil:
		till()


def prepare_crop_ground(crop, needs_soil):
	if needs_soil:
		ensure_soil()


def farm_configured_tile():
	prepare_crop_ground(LB_CROP, LB_NEEDS_SOIL)

	if can_harvest():
		harvest()

	if get_entity_type() != LB_CROP:
		prepare_crop_ground(LB_CROP, LB_NEEDS_SOIL)
		plant(LB_CROP)


def farm_configured_column():
	for _ in range(get_world_size()):
		if num_items(LB_ITEM) >= LB_TARGET:
			return
		farm_configured_tile()
		move(North)


def wait_for_drones():
	while num_drones() > 1:
		pass


def farm_full_until(crop, item, target, needs_soil):
	configure_crop(crop, item, target, needs_soil)
	clear()

	while num_items(item) < target:
		for _ in range(get_world_size()):
			if num_items(item) >= target:
				return

			if num_drones() < max_drones():
				spawn_drone(farm_configured_column)
			else:
				farm_configured_column()

			move(East)

		wait_for_drones()


def farm_single_until(crop, item, target, needs_soil):
	configure_crop(crop, item, target, needs_soil)
	clear()

	while num_items(item) < target:
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				if num_items(item) >= target:
					return
				farm_configured_tile()
				move(North)
			move(East)


def farm_wood_tile():
	crop = Entities.Bush
	if num_unlocked(Unlocks.Trees) > 0 and (get_pos_x() + get_pos_y()) % 2 == 0:
		crop = Entities.Tree

	if can_harvest():
		harvest()

	if get_entity_type() != crop:
		plant(crop)


def farm_wood_column():
	for _ in range(get_world_size()):
		if num_items(Items.Wood) >= LB_TARGET:
			return
		farm_wood_tile()
		move(North)


def farm_wood_full_until(target):
	global LB_TARGET
	LB_TARGET = target
	clear()

	while num_items(Items.Wood) < target:
		for _ in range(get_world_size()):
			if num_items(Items.Wood) >= target:
				return

			if num_drones() < max_drones():
				spawn_drone(farm_wood_column)
			else:
				farm_wood_column()

			move(East)

		wait_for_drones()


def farm_wood_single_until(target):
	clear()
	while num_items(Items.Wood) < target:
		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				if num_items(Items.Wood) >= target:
					return
				farm_wood_tile()
				move(North)
			move(East)


pumpkin_ready = False


def scan_pumpkin_tile():
	global pumpkin_ready
	ensure_soil()
	entity = get_entity_type()

	if entity == Entities.Dead_Pumpkin or entity == None:
		pumpkin_ready = False
		plant(Entities.Pumpkin)
	elif entity != Entities.Pumpkin:
		pumpkin_ready = False
		if can_harvest():
			harvest()
		plant(Entities.Pumpkin)


def scan_pumpkin_field():
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			scan_pumpkin_tile()
			move(North)
		move(East)


def farm_pumpkins_full_until(target):
	global pumpkin_ready
	clear()

	while num_items(Items.Pumpkin) < target:
		pumpkin_ready = True
		scan_pumpkin_field()
		if pumpkin_ready:
			harvest()


def farm_pumpkins_single_until(target):
	clear()

	while num_items(Items.Pumpkin) < target:
		pumpkin_ready = True

		for _ in range(get_world_size()):
			for _ in range(get_world_size()):
				if num_items(Items.Pumpkin) >= target:
					return
				scan_pumpkin_tile()
				if get_entity_type() != Entities.Pumpkin or not can_harvest():
					pumpkin_ready = False
				move(North)
			move(East)

		if pumpkin_ready:
			harvest()


def farm_item_basic(item, amount):
	if item == Items.Hay:
		farm_single_until(Entities.Grass, Items.Hay, amount, False)
	elif item == Items.Wood:
		farm_wood_single_until(amount)
	elif item == Items.Carrot:
		farm_single_until(Entities.Carrot, Items.Carrot, amount, True)
	elif item == Items.Pumpkin:
		farm_pumpkins_single_until(amount)
	elif item == Items.Cactus:
		farm_single_until(Entities.Cactus, Items.Cactus, amount, True)
	elif item == Items.Power:
		farm_single_until(Entities.Sunflower, Items.Power, amount, True)
