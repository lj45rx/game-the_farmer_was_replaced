def farm_pumplins(limit=10000):
	if limit < num_items(Items.Pumpkin):
		return True
		
	field_size = get_world_size()
	
	while num_items(Items.Pumpkin) < limit:
		# for each tile True if harvestable pumpkin
		num_unfinished_tiles = field_size*field_size
		tile_is_finished = []
		for i in range(num_unfinished_tiles):
			tile_is_finished.append(False)
		
		# until all are finished
		last_unfinished_cnt = num_unfinished_tiles
		while num_unfinished_tiles > 0: 
			num_unfinished_tiles = 0
			tile_idx = -1
			for col in range(field_size):
				for row in range(field_size):
					tile_idx += 1
					
					# is already finished
					if tile_is_finished[tile_idx]:
						continue
					
					# remove other plants if present
					if get_entity_type() != Entities.Pumpkin and get_entity_type() != None:
						harvest()
						
					goto_pos(col, row)
					# is ready to be harvested 
					if get_entity_type() == Entities.Pumpkin and can_harvest():
						tile_is_finished[tile_idx] = True
						continue
					
					num_unfinished_tiles += 1
					# plant new 
					if get_entity_type() != Entities.Pumpkin:
						plant_by_name(Entities.Pumpkin)
						
					# is pumpkin but not ready for harvest
					if last_unfinished_cnt < 50:
						# use fiertilizer if only few left, else water
						try_fertilizing()
					else:
						water_if_available()
			
			last_unfinished_cnt = num_unfinished_tiles
			
		# post loop - all finished -> harvest
		harvest()

farm_pumplins(1000000)
