def create_maze():
	if get_entity_type() == Entities.Hedge:
		return True# is already maze
	
	goto_pos(0, 0)
	harvest()
	
	plant(Entities.Bush)
	while get_entity_type() == Entities.Bush:
		if not try_fertilizing():
			# could not apply fertilizer
			return False
			
	return True

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

def farm_treasure(limit=10000):
	while num_items(Items.Gold) < limit:
		if not create_maze():
			# failed to crete maze
			return False
		if not solve_maze_follow_left_wall():
			return False
	
	return True


farm_treasure(100000)
