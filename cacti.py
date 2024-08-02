
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

def is_sorted(arr):
	for i in range(len(arr)-1):
		if arr[i] > arr[i+1]:
			return False
	return True

# performance xyz s and xyz k ops
def cacti_sort_row_cocktail_2(field_size, _idx, is_row):
	# find top right "normally", by moving right
	# but remember values 
	# from there sort in array -> push requiered elements only
	if is_row:
		goto_pos(0, _idx)
		get_pos = get_pos_x
		dir_right = East
		dir_left = West
	else:
		goto_pos(_idx, 0)
		get_pos = get_pos_y
		dir_right = North
		dir_left = South
		
	#set_execution_speed(10)
	
	# find and move top value, remember others
	values = []
	if True: # TODO remove else-part 
		for ix in range(0, field_size-1):
			m_cur = measure()
			m_right = measure(dir_right)
			if m_right < m_cur:
			#if measure(dir_right) < values[-1]:
				values.append(m_right)
				swap(dir_right)
			else:
				values.append(m_cur)
			move(dir_right)
		values.append(measure()) # poped soon - used as max val
	else:
		for i in range(field_size):
			values.append(measure())
			move(dir_right)
		move(dir_left)
	
	if is_sorted(values):
		return
	
	# position on part of field still unfinished
	min_x = 0
	max_x = field_size-2
	cur_x = field_size-1
	# min/max values on the field
	min_val = 0
	max_val = values.pop()
	
	find_min = True
	while 1 < len(values):
		if is_sorted(values):
			return
		
		#print(values, find_min)
		
		# move min value leff
		if find_min:
			# skip if at correct place 
			if values[0] == min_val:
				values.pop(0)
				min_x += 1
				continue
			
			# in values - find index of smallest value farthest to the right
			arr_hit_idx = len(values)-1 # last
			for x in range(len(values)-2, -1, -1): #max_x is saved, min_x-1 to include
				if values[x] < values[arr_hit_idx]:
					arr_hit_idx = x
			
			min_val = values[arr_hit_idx] # update min
			hit_idx = arr_hit_idx+min_x # to index on the field
			
			# is at correct place
			# already there, or same value
			if values[arr_hit_idx] == values[0]:
				values.pop(0)
				min_x += 1
				continue		
			
			#print("moving", min_val, "from", hit_idx, "to", min_x)
			#move right if needed
			#while get_pos() < hit_idx:
			#	move(dir_right)
			# move left, begin swapping as soon as hit_idx is reached
			while min_x+1 < get_pos():
				move(dir_left)
				if not hit_idx < get_pos():
					swap(dir_left) 
				
			min_x += 1
			
		# move max value right
		else:
			# skip if at correct place
			if values[-1] == max_val:
				values.pop()
				max_x -= 1
				continue
			
			# in values - find index of largest value farthest to the left 
			arr_hit_idx = 0 # first 
			for x in range(1, len(values)):
				if values[arr_hit_idx] < values[x]:
					arr_hit_idx = x
			
			max_val = values[arr_hit_idx] # update max
			hit_idx = arr_hit_idx+min_x # to index on the field
			
			# is at correct place
			# already there, or same value
			if values[arr_hit_idx] == values[-1]:
				values.pop()
				max_x -= 1
				continue		
	
			#print("moving", "from", hit_idx, "to", max_x)
			#move right if needed
			#while hit_idx < get_pos():
			#	move(dir_left)
			# move right, begin swapping as soon as hit_idx is reached
			while get_pos() < max_x:
				if not get_pos() < hit_idx:
					swap(dir_right) 
				move(dir_right) 
				
			max_x -= 1
		
		# remove moved value from array
		values.pop(arr_hit_idx)
		find_min = not find_min
	
	return		
	
# performance 23,8s and 400k ops
def cacti_sort_row_cocktail(field_size, _idx, is_row):
	#print("almost works - usually correct after 2 times")
	#dir_right = [North, East][is_row]
	#dir_left = [South, West][is_row]
	#get_pos = [get_pos_y, get_pos_x][is_row]

	if is_row:
		goto_pos(0, _idx)
		get_pos = get_pos_x
		dir_right = East
		dir_left = West
	else:
		goto_pos(_idx, 0)
		get_pos = get_pos_y
		dir_right = North
		dir_left = South
		
	#set_execution_speed(10)
	
	i_left = 0
	i_right = field_size-1
	while i_left < i_right:
		# move right
		# check/swap then move
		for ix in range(i_left, i_right):
			if measure(dir_right) < measure():
				swap(dir_right)
			move(dir_right)
		i_right -= 1
		
		# move left
		# move then check/swap
		for ix in range(i_right, i_left, -1):
			move(dir_left)
			if measure() < measure(dir_left):
				swap(dir_left)
		i_left += 1

def cacti_sort_row_bubble(field_size, _idx, is_row):
	direction = [North, East][is_row]

	for step in range(field_size):	
		for j in range(field_size-1-step):
			if is_row:
				goto_pos(j, _idx)
			else:
				goto_pos(_idx, j)
			if measure() > measure(direction):
				swap(direction)
			move(direction)	

# new handle rows/cols in reparate fkt
def sort_cacti():
	field_size = get_world_size()
	# basically bubble sort
	# in x, then in y
	for row in range(field_size):
		cacti_sort_row_cocktail_2(field_size, row, True)
				
	for col in range(field_size):
		cacti_sort_row_cocktail_2(field_size, col, False)

# old - bubblesort all in one
# performance 30,5s and 500k ops
def sort_cacti_1():
	field_size = get_world_size()
	
	# basically bubble sort
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
