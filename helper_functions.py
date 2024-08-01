def get_field_dim():
	return [10,10]
	
def get_dim():
	return 10

def goto_pos(x,y):
	# if always width=height -> simplify
	
	# wow this is terrible
	o_x = get_pos_x() #remove
	o_y = get_pos_y() #remove
	if get_pos_x() == x and get_pos_y() == y:
		return
	
	w, h = get_field_dim()
	w2 = w//2
	h2 = h//2
	
	x_diff = x-get_pos_x()
	y_diff = y-get_pos_y()
	
	
	dir_x = 0 # 0=east
	dir_y = 0 # 0=north
	
	# flip if negative
	if x_diff < 0:
		dir_x += 1
	
	if y_diff < 0:
		dir_y += 1
	
	# too big
	# flip again and reduce distance
	if w2 < abs(x_diff):
		x_diff = abs(x_diff) - w
		dir_x += 1
		
	if h2 < abs(y_diff):
		y_diff = abs(y_diff) - h
		dir_y += 1
	
	for i in range(abs(x_diff)):
		if dir_x%2 == 0:
			move(East)
		else:
			move(West)
			
	for i in range(abs(y_diff)):
		if dir_y%2 == 0:
			move(North)
		else:
			move(South)
	
	# todo remove
	if get_pos_x() != x or get_pos_y() != y:
		print(o_x, "->", x, o_y, "->", y, x_diff, y_diff)
		while True:
			pass

def goto_pos_alt_simpel(x,y):
	# maybe add check on which direction to move
	w, h = get_field_dim()
	
	x_diff = x-get_pos_x()
	y_diff = y-get_pos_y()
	
	move_right = 0 < x_diff
	move_up = 0 < y_diff
	
	while get_pos_x() != x:
		if move_right:
			move(East)
		else:
			move(West)
	
	while get_pos_y() != y:
		if move_up:
			move(North)
		else:
			move(South)

def goto_start():
	while 0 < get_pos_x():
		move(West)
	while 0 < get_pos_y():
		move(South)

def water_if_available():
	if 0 < num_items(Items.Water_Tank):
		water_level = get_water()
		if water_level <= 0.75:
			use_item(Items.Water_Tank)
			return True
	return False
			
def try_fertilizing():
	# use if available
	if 0 < num_items(Items.Fertilizer):
		use_item(Items.Fertilizer)
		return True
	
	# try buying 
	if trade(Items.Fertilizer):
		use_item(Items.Fertilizer)
		return True
	
	return False
			
def harvest_all(w=-1, h=-1):
	
	if w == -1 or h == -1:
		w = get_dim()
		h = w
	
	goto_start()
	for col in range(w):
		for row in range(h):
			harvest()
			move(North)
		move(East)
		
def farm_hay(w,h,limit=10000):
	if num_items(Items.Hay) > limit:
		return
	while num_items(Items.Hay) < limit:
		for col in range(w):
			for row in range(h):
				harvest()
				while get_ground_type() != Grounds.Turf:
					till()
				move(North)
			move(East)

def farm_wood_and_hay_with_trees(w,h, limit=10000):
	if num_items(Items.Wood) > limit:
		return
	harvest_all(w, h)
	while num_items(Items.Wood) < limit:
		for col in range(w):
			for row in range(h):
				if (col+row)%2 == 1:
					while get_ground_type() != Grounds.Turf:
						till()
					harvest()
				else:
					if can_harvest():
						harvest()
					
					while get_ground_type() != Grounds.Soil:
						till()
						
					while get_entity_type() != Entities.Tree:
						plant(Entities.Tree)
						
					water_if_available()
				move(North)
			move(East)

def buy_water_tanks(n):
	if num_unlocked(Unlocks.Multi_Trade) > 0:
		trade(Items.Empty_Tank, n)
	else:
		for i in range(n):
			trade(Items.Empty_Tank)

def buy_water_tanks(n):
	for i in range(n):
		trade(Items.Empty_Tank)

def prepare_gound_to(ground_type):
	while get_ground_type() != ground_type:
		till()
		
def try_buying_seeds(seed_type):
	while num_items(seed_type) < 1:
		trade(seed_type)
