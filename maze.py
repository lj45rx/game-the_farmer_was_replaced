# follow left wall until treasure is found
def solve_maze_follow_left_wall():
	if get_entity_type() != Entities.Hedge:
		return False
	
	# start at bottom left
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
# set "connections" for outer walls
# Return initialized tiles, number of connections still to check
def create_tile_objects_for_maze():
	field_size = get_world_size()
	
	tiles = []
	total_unchecked_cnt = 0
	for col_idx in range(field_size):
		
		tmp_column = []
		for row_idx in range(field_size):
			# classes/objects not available, using dict
			tmp_tile_dict = {"x":col_idx, "y":row_idx}
			connections = [None,None,None,None]
			cnt_unchecked = 4
	 
			 # bottom cant move south
			if row_idx == 0:
				connections[2] = 0
				cnt_unchecked -= 1
			 # right cant move right
			if col_idx == field_size-1:
				connections[1] = 0
				cnt_unchecked -= 1
			# top cant move up
			if row_idx == field_size-1:
				connections[0] = 0
				cnt_unchecked -= 1
			# left cant move left
			if col_idx == 0:
				connections[3] = 0
				cnt_unchecked -= 1
				
			tmp_tile_dict["connections"] = connections
			tmp_tile_dict["unchecked_cnt"] = cnt_unchecked
			tmp_column.append(tmp_tile_dict)
			total_unchecked_cnt += cnt_unchecked
			
		tiles.append(tmp_column)
		
	return tiles, total_unchecked_cnt


# find connections for single current tile
# set shared walls for self and neighbour
# CAUTION: does not check bounds, assuming this is set in initial creation of array
# in last step check moving straight, dont move back if applicable
# Return: updated tile-array, has_moved, newly_checked_cnt
def check_connections_of_tile(tiles, current_direction):
	xIdx = get_pos_x() # use these to prevent errors
	yIdx = get_pos_y()
	
	tile_conns = tiles[xIdx][yIdx]["connections"]
	newly_checked_cnt = 0
	treasure_loc = None
	for k in range(1,5):
		# relative to current_direction, check right-(back-)left-front
		dir = (current_direction+k)%4
		# skip finished
		if tile_conns[dir] != None:
			continue
			
		back_dir_idx = (dir+2)%4
		dx = [0,1,0,-1][dir]
		dy = [1,0,-1,0][dir]
		other_x = xIdx + dx	
		other_y = yIdx + dy	
		
		has_moved = move_by_index(dir)
		newly_checked_cnt += 1
		if has_moved:
			# set for self+neighbour, move back
			tiles[xIdx][yIdx]["connections"][dir] = 1
			tiles[other_x][other_y]["connections"][back_dir_idx] = 1
			if get_entity_type() == Entities.Treasure:
				treasure_loc = [other_x, other_y]
		else:
			tiles[xIdx][yIdx]["connections"][dir] = 0
			tiles[other_x][other_y]["connections"][back_dir_idx] = 0

		tiles[xIdx][yIdx]["unchecked_cnt"] -= 1
		tiles[other_x][other_y]["unchecked_cnt"] -= 1
		
		# move back, unless last step (straight) and left is blocked
		if has_moved:
			# k==4 is last step
			# current_direction-1 is left
			if k == 4 and tile_conns[(current_direction-1)%4] == 0:
				return tiles, True, 2*newly_checked_cnt, treasure_loc
			move_by_index(back_dir_idx)
			
	return tiles, False, 2*newly_checked_cnt, treasure_loc


# find all connections between the tiles
# Return updated tiles, position of treasure [x,y]
# Assumption/Prerequisite: "Mazes do not contain any loops" (unless reused)
def init_tile_connections_in_maze(tiles, _unchecked_cnt, _print=False):
	treasure_pos = None
	total_unchecked_cnt = _unchecked_cnt
	
	# north=0, east=1, south=2, west=3
	dir = 0
	while 0 < total_unchecked_cnt:
		if _print:
			quick_print(total_unchecked_cnt)
		x_pos = get_pos_x()
		y_pos = get_pos_y()
		
		if get_entity_type() == Entities.Treasure:
			# dont harvest before fully initialized
			treasure_pos = [x_pos, y_pos]
		
		# check yet unchecked connections for this tile 
		if 0 < tiles[x_pos][y_pos]["unchecked_cnt"]:
			tiles, has_moved, checked_cnt, treasure_loc = check_connections_of_tile(tiles, dir)
			total_unchecked_cnt -= checked_cnt
			
			if treasure_loc != None: #TODO check - treasure might only be visited when checking
				treasure_pos = treasure_loc
			if has_moved:
				continue
	
		# relative to current direction
		# try moving where possible in order left->straight->right->back
		for j in range(-1,3):
			n_dir = (dir+j)%4
			if tiles[x_pos][y_pos]["connections"][ n_dir ]:
				dir = n_dir
				move_by_index(n_dir)
				break
	
	if _print:
		for i in range(get_world_size()):
			quick_print(tiles[i])
		quick_print("treasure is at", treasure_pos)
	
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
		# order up, right, down, left 
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
def solve_maze_remember_tiles(num_reps=10, _print=False):
	create_maze()
	
	# create array, set border cases
	tiles, cnt = create_tile_objects_for_maze()
	
	# find all other connections
	tiles, treasure_pos = init_tile_connections_in_maze(tiles, cnt)
	
	

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
	
	gold_before = num_items(Items.Gold)
	harvest()
	gold_diff = num_items(Items.Gold) - gold_before
	print("earned", gold_diff, "in", num_reps, "repetitions")



solve_maze_remember_tiles()






