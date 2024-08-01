def get_list_of_lists(length):
	# this  does not work
	#  res = [ [] for _ in range(length) ]
	res = []
	for i in range(length):
		res.append([])	
	return res
	
def plant_sunflower():
	prepare_gound_to(Grounds.Soil)
	water_if_available()
	try_buying_seeds(Items.Sunflower_Seed)
	while get_entity_type() != Entities.Sunflower:
		plant(Entities.Sunflower)

def farm_energy(w,h,limit=10000):
	if num_items(Items.Power) > limit:
		return
	harvest_all(w, h)
	
	replant = False # use with low num of buckets
	num_buckets = 6 # eg 6 for [10,15], max 9 for [7, 15]
	# create lists to remember petal counts per plant
	while  num_items(Items.Power) < limit:
		min_value = 15
		min_plant_xy = None
		petal_counts = get_list_of_lists(num_buckets) # (re)set
		
		# (re)plant all
		for col in range(w):
			for row in range(h):
				plant_sunflower()
				
				# remember plants with 15,14,13 petals
				value = measure()
				bucket_idx = 15-value
				if bucket_idx < num_buckets:
					petal_counts[bucket_idx].append([col, row])
				
				if value < min_value:
					min_value = value
					min_plant_xy = [col, row]
					
				move(North)
			move(East)
		
		# harvest "good flowers" with 15,14,13 petals
		current_bucket = 0
		while current_bucket < num_buckets:
			# current bucket is empty - look at lower
			if len(petal_counts[current_bucket]) == 0:
				current_bucket += 1
				continue
			
			# harvest plant - first(oldest) in bucket
			x_, y_ = petal_counts[current_bucket].pop(0)
			goto_pos(x_, y_)
			
			while not can_harvest():
				pass
				#do_a_flip()
			harvest()
			
			# replant
			if replant:
				plant_sunflower()
						
				# remember petal counts
				bucket_idx = 15-measure()
				if bucket_idx < num_buckets:
					petal_counts[bucket_idx].append([x_, y_])
					
				# move up if new flower falls in higher bucket
				# eg currently harvesting 14, new flower has 15 -> next must be 15
				if bucket_idx < current_bucket:
					current_bucket = bucket_idx
		
		# all 15,14,13 hervested -> replant
		# marvest min-plant to reset all - then go to 0,0
		x_, y_ = min_plant_xy
		goto_pos(x_, y_)
		harvest()
		goto_pos(0,0)
			
		
	


farm_energy(10,10,100000)


