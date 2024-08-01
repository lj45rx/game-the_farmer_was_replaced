
def plant_cacti():
	field_size = get_world_size()
	goto_pos(0, 0)
	
	values = []
	for col in range(field_size):
		for row in range(field_size):
			entity_type = get_entity_type()
				
			if entity_type != None and entity_type != Entities.Cactus:
				harvest()
					
			if entity_type != Entities.Cactus:
				plant_by_name(Entities.Cactus)
					
			values.append(measure())
				
			move(North)
		move(East)

	return values
	

def sort_cacti():
	field_size = get_world_size()
	
	# basically insetion sort
	# in x, then in y
	
	for row in range(field_size):
		for i in range(field_size):
			goto_pos(0, row)
			for j in range(field_size-1-i):
				if measure() > measure(East):
					swap(East)
				move(East)
				
	for col in range(field_size):
		for i in range(field_size):
			goto_pos(col, 0)
			for j in range(field_size-1-i):
				if measure() > measure(North):
					swap(North)
				move(North)

def check_cacti():
	field_size = get_world_size()
	for row in range(field_size):
		for col in range(field_size):
			goto_pos(col, row)
			val = measure()
			
			if 0 < col and measure(West) > val:
				print("left bigger")
				return False
			if col < field_size-1 and measure(East) < val:
				print("right smaller")
				return False
			if 0 < row and measure(South) > val:
				print("bottom bigger")
				return False
			if row < field_size-1 and measure(North) < val:
				print("top smaller")
				return False
	
	return True
	
def farm_cacti(limit=10000):
	while num_items(Items.Cactus) < limit:
		plant_cacti()
		sort_cacti()
		if check_cacti():
			harvest()
		else:
			while True:
				print("error")
				do_a_flip()
	
farm_cacti(50000)
