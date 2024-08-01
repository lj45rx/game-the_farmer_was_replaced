def get_plant_dict():
	plant_dict = {
		Entities.Bush:{"use":Entities.Bush, "buy":None, "ground":None, "action":plant},
		Entities.Tree:{"use":Entities.Tree, "buy":None, "ground":None, "action":plant},
		Entities.Grass:{"use":Entities.Grass, "buy":None, "ground":None, "action":plant},
		Entities.Carrots:{"use":Entities.Carrots, "buy":Items.Carrot_Seed, "ground":Grounds.Soil, "action":plant},
		Entities.Pumpkin:{"use":Entities.Pumpkin, "buy":Items.Pumpkin_Seed, "ground":Grounds.Soil, "action":plant},
		Entities.Cactus:{"use":Entities.Cactus, "buy":Items.Cactus_Seed, "ground":Grounds.Soil, "action":plant},
		Entities.Dinosaur:{"use":Items.Egg, "buy":Items.Egg, "ground":None, "action":use_item}
	}
	return plant_dict

def plant_by_name(name):
	# not working from other "files", plant_dict not defined if used as variable
	#_dict = plant_dict[name]
	_dict = get_plant_dict()[name]
	seeds = _dict["buy"]
	ground = _dict["ground"]
	action = _dict["action"]
	action_param = _dict["use"]
	
	if seeds != None:
		trade(seeds)
	
	if ground != None:
		while get_ground_type() != ground:
			till()
	
	# do action, can be plant() or use_item()
	action(action_param)

def move_by_index(idx):
	# north=0, east=1, south=2, west=3
	idx %= 4
	
	if idx == 0:
		return move(North)
	if idx == 1:
		return move(East)
	if idx == 2:
		return move(South)
	if idx == 3:
		return move(West)

def rand_int(max_excl):
	return (random() * max_excl) // 1

def move_random(dist=1):
	for move_step in range(dist):
		move_by_index(rand_int(4))