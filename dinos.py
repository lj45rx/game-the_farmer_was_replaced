def create_dinos():	
	field_size = get_world_size()
	
	goto_pos(0,0)
	for col in range(field_size):
		for row in range(field_size):
			if get_entity_type() != None and get_entity_type() != Entities.Dinosaur:
				harvest()
			
			if get_entity_type() != Entities.Dinosaur:
				if not trade(Items.Egg):
					return
				use_item(Items.Egg)
			move(North)
		move(East)

def harvest_dinos():
	create_dinos()
	# "there are 4 kinds of dinos
	
	replant_after_x_harvests = 3
	harvest_cnt = 0
	while True:
		if harvest_cnt >= replant_after_x_harvests:
			harvest_cnt = 0
			create_dinos()
			
		move_random(1)
		
		if get_entity_type() != Entities.Dinosaur:
			plant_by_name(Entities.Dinosaur)
			
		measurements = [
			measure(),
			measure(North),
			measure(East),
			measure(South),
			measure(West)
		]
		
		counts = [0,0,0,0]
		for val in measurements:
			if val != None:
				counts[val] += 1 
		
		for i in range(4):
			if 4 <= counts[i]:
				harvest()
				harvest_cnt += 1
		

#create_dinos()

#move_random()
harvest_dinos()	
#print(get_plant_dict()[Entities.Carrots])	

	
	