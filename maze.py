# follow left wall until treasure is found
def solve_maze_follow_left_wall():
	if get_entity_type() != Entities.Hedge:
		return False
		
	# follow left wall
	# north=0, east=1, south=2, west=3
	dir = 0
	
	while get_entity_type() != Entities.Treasure:
		# try moving left
		if move_by_index(dir-1):
			dir = (dir-1)%4
			continue
		
		# else try moving straight
		if move_by_index(dir):
			continue
			
		# else try moving right
		if move_by_index(dir+1):
			dir = (dir+1)%4
			continue
			
		# else move back
		move_by_index(dir+2)
		dir = (dir+2)%4
		
	if get_entity_type() == Entities.Treasure:
		harvest()
		return True
		
	return False


def farm_gold(limit=10000):
	while num_items(Items.Gold) < limit:
		if not create_maze():
			# failed to create maze
			return False
		if not solve_maze_follow_left_wall():
			return False
	
	return True


# create a maze on the field_size
# Return True if successful
def create_maze():
	if get_entity_type() == Entities.Hedge:
		return True # is already maze
	
	#goto_pos(0, 0) # not required
	harvest()
	plant(Entities.Bush)
	
	while get_entity_type() == Entities.Bush:
		if not try_fertilizing():
			# could not apply fertilizer
			return False
			
	return True

# create 2d-Array with dicts for each tile 
# holding info about connections between tiles (paritially initialized)
# (also holding x,y -> somewhat redundant, maybe remove)
def create_tile_objects_for_maze():
	field_size = get_world_size()
	
	tiles = []
	for col_idx in range(field_size):
		
		tmp_column = []
		for row_idx in range(field_size):
			# classes/objects not available, using dict
			tmp_tile = {
				"x":col_idx, 
				"y":row_idx,
				"visited":False, 
				"connections":[0,0,0,0]
			}
			tmp_column.append(tmp_tile)
			
		tiles.append(tmp_column)
		
	return tiles

# find all connections between the tiles
# Return updated tiles, position of treasure [x,y]
# Assumption/Prerequisite: "Mazes do not contain any loops" (unless reused)
def init_tile_connections_in_maze():
	field_size = get_world_size()
	num_unvisited_tiles = field_size*field_size
	
	tiles = create_tile_objects_for_maze()
	treasure_pos = None
	
	dir = 0 # north=0, east=1, south=2, west=3
	x_pos = get_pos_x()
	y_pos = get_pos_y()
	tile = tiles[x_pos][y_pos]
	while 0 < num_unvisited_tiles:
		if not tile["visited"]:
			tile["visited"] = True
			num_unvisited_tiles -= 1
		
		if get_entity_type() == Entities.Treasure:
			# dont harvest before fully initialized
			treasure_pos = [x_pos, y_pos]
	
		# relative to current direction
		# try moving where possible in order left->straight->right->back
		for j in range(-1,3):
			n_dir = (dir+j)%4
			if move_by_index(n_dir):
				dir = n_dir
				# set connections in current and neighbour tiles
				tile["connections"][n_dir] = 1
				
				x_pos = get_pos_x()
				y_pos = get_pos_y()
				tile = tiles[x_pos][y_pos]
				tile["connections"][(n_dir+2)%4] = 1 # reverse dir
				break
	
	return tiles, treasure_pos

# find path to treasure location, inspired by dijkstra
def find_path_in_maze(tiles, treasure_pos, _print=False):
	dx = [0,1,0,-1]
	dy = [1,0,-1,0]
	tr_x, tr_y = treasure_pos
	# x,y,route, dir to parent
	queue = [[get_pos_x(), get_pos_y(), None, None]]
	
	current_node = None
	while 0 < len(queue):
		current_node = queue.pop(0)
		if _print:
			quick_print(current_node)
		x,y,last_dir,parent = current_node
		
		if x == tr_x and y == tr_y:
			break
		
		# check all possible ways except parent
		# inn order up, right, down, left 
		connections = tiles[x][y]["connections"]
		for dir in range(4):
			rev_dir = (dir+2)%4
			# is wall or parent skip
			if connections[dir] == 0 or last_dir == rev_dir:
				continue			

			new_node = [x+dx[dir], y+dy[dir], dir, current_node]
			queue.append(new_node)
	
	route = []
	while current_node[2] != None:
		route.append(current_node[2])
		current_node = current_node[3]
	
	return route	


def walk_path(path):
	while len(path):
		move_by_index(path.pop())


# expect Gold = 100*MazeLevel*noReps
# average runtime 23,65sec in 20 tests with num_reps=20 
def solve_maze_remember_tiles(num_reps=10, _print=False):
	create_maze()

	tiles, treasure_pos = init_tile_connections_in_maze()

	for rep in range(num_reps):
		if _print:
			print(rep+1, "/", num_reps)
		
		# find path
		path = find_path_in_maze(tiles, treasure_pos, _print)
		
		# walk to treasure
		walk_path(path)
	
		# "replant", remember new location 
		if rep == num_reps-1:
			break	
		while get_entity_type() == Entities.Treasure:
			# TODO better - in case was same pos remeasure every step
			treasure_pos = measure()
			
			trade(Items.Fertilizer)
			use_item(Items.Fertilizer)
	
	# harvest only in last step
	gold_before = num_items(Items.Gold)
	harvest()
	gold_diff = num_items(Items.Gold) - gold_before
	quick_print("earned", gold_diff, "in", num_reps, "repetitions")

