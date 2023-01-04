# python 3

import sys
import time

floor_pos = []

# boolean values
# in [y][x] order
stopped_rock_coords = []

highest_stopped_rock_pos = -1

lowest_solid_y_at_x = [-1, -1, -1, -1, -1, -1, -1]

low_rows_eliminated = 0

# start with 10 rows
for y in range(0, 10):
	stopped_rock_coords.append([False, False, False, False, False, False, False])

for i in range(0, 7):
	floor_pos.append(0)

rel_coords_by_rock_type = []

#|  shape:
#|
#|
#|   ####
#|
#|
rel_coords_by_rock_type.append([(0,0),(1,0),(2,0),(3,0)])

#|  shape:
#|
#|    #
#|   ###
#|    #
#|
rel_coords_by_rock_type.append([(0,1),(1,0),(1,1),(1,2),(2,1)])

#|  shape:
#|
#|     #
#|     #
#|   ###
#|
rel_coords_by_rock_type.append([(0,0),(1,0),(2,0),(2,1),(2,2)])

#|  shape:
#|
#|    #
#|    #
#|    #
#|    #
#|
rel_coords_by_rock_type.append([(0,0),(0,1),(0,2),(0,3)])

#|  shape:
#|
#|   ##
#|   ##
#|      
rel_coords_by_rock_type.append([(0,0),(1,0),(0,1),(1,1)])

jet_pattern = '<>'

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# ">>><<><>><<<>><>>..."
	jet_pattern = line

jet_pattern_len = len(jet_pattern)

jet_pushes_left = []
for c in jet_pattern:
	jet_pushes_left.append(c == '<')

jet_idx = -1

last_rock_timestamp = -1

#for i in xrange(0, 1):
# 200000x5000000 = 1 trillion
for i in xrange(0, 200000):
	if i % 20 == 0:
		rocknum = i * 5000000
		print("dropping rock {} ({}%) from position {}".format(rocknum, ((rocknum * 100.0)/1000000000000.0), highest_stopped_rock_pos + 4))
	ts_now = time.time()
	if last_rock_timestamp > 0:
		ts_diff = ts_now - last_rock_timestamp
		#print("rocks per second: [{}]".format(500000.0 / ts_diff), end='\r')
		sys.stdout.write("rocks per second: [{}]\r".format(5000000.0 / ts_diff))
		sys.stdout.flush()
	last_rock_timestamp = ts_now
	#for j in xrange(0, 2022):
	for j in xrange(0, 5000000):
	
		# reset for new rock
		rock_left_pos = 2
		rock_bottom_pos = highest_stopped_rock_pos + 4 - low_rows_eliminated
		rock_is_stopped = False
		rock_rel_coords = rel_coords_by_rock_type[j % 5]

		# 1st of 3 moves without checking other rocks
		jet_idx += 1
		if jet_idx >= jet_pattern_len:
			jet_idx = 0
		if jet_pushes_left[jet_idx]:
			# move left without checking other stopped rocks, only check the walls
			rock_left_pos -= 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos < 0:
					rock_left_pos += 1
					break
		else:
			# move right without checking other stopped rocks, only check the walls
			rock_left_pos += 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos > 6:
					rock_left_pos -= 1
					break

		# 2nd of 3 moves without checking other rocks
		jet_idx += 1
		if jet_idx >= jet_pattern_len:
			jet_idx = 0
		if jet_pushes_left[jet_idx]:
			# move left without checking other stopped rocks, only check the walls
			rock_left_pos -= 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos < 0:
					rock_left_pos += 1
					break
		else:
			# move right without checking other stopped rocks, only check the walls
			rock_left_pos += 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos > 6:
					rock_left_pos -= 1
					break

		# 3rd of 3 moves without checking other rocks
		jet_idx += 1
		if jet_idx >= jet_pattern_len:
			jet_idx = 0
		if jet_pushes_left[jet_idx]:
			# move left without checking other stopped rocks, only check the walls
			rock_left_pos -= 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos < 0:
					rock_left_pos += 1
					break
		else:
			# move right without checking other stopped rocks, only check the walls
			rock_left_pos += 1
			for coord in rock_rel_coords:
				if coord[0] + rock_left_pos > 6:
					rock_left_pos -= 1
					break

		# move down 3 times
		rock_bottom_pos -= 3

		while not rock_is_stopped:
			jet_idx += 1
			if jet_idx >= jet_pattern_len:
				jet_idx = 0
			if jet_pushes_left[jet_idx]:
				# try to move left
				#can_move_left = True
				rock_left_pos -= 1
				for coord in rock_rel_coords:
					y = coord[1] + rock_bottom_pos
					#x = coord[0] + rock_left_pos - 1
					x = coord[0] + rock_left_pos
					if x < 0 or stopped_rock_coords[y][x]:
						#can_move_left = False
						rock_left_pos += 1
						break
				#if can_move_left:
				#	rock_left_pos -= 1
			else:
				# try to move right
				#can_move_right = True
				rock_left_pos += 1
				for coord in rock_rel_coords:
					y = coord[1] + rock_bottom_pos
					#x = coord[0] + rock_left_pos + 1
					x = coord[0] + rock_left_pos
					if x > 6 or stopped_rock_coords[y][x]:
						#can_move_right = False
						rock_left_pos -= 1
						break
				#if can_move_right:
				#	rock_left_pos += 1
			# try to move down
			for coord in rock_rel_coords:
				y = coord[1] + rock_bottom_pos - 1
				x = coord[0] + rock_left_pos
				if y < 0 or stopped_rock_coords[y][x]:
					rock_is_stopped = True
					break
			if not rock_is_stopped:
				rock_bottom_pos -= 1

		# become one with the pile
		for coord in rock_rel_coords:
			x = coord[0] + rock_left_pos
			y = coord[1] + rock_bottom_pos
			stopped_rock_coords[y][x] = True
			y_real = y + low_rows_eliminated
			if y_real > highest_stopped_rock_pos:
				highest_stopped_rock_pos = y_real
			if y_real > lowest_solid_y_at_x[x]:
				#print("lowest solid rock at x={} is at y={}".format(x, y))
				lowest_solid_y_at_x[x] = y_real

		lowest_solid_y = min(lowest_solid_y_at_x)

		# something is odd... keeping a few extra rows seems to get the
		#   right answer, so we'll do that
		while low_rows_eliminated + 10 < lowest_solid_y:
			del stopped_rock_coords[0]
			low_rows_eliminated += 1

		while highest_stopped_rock_pos - low_rows_eliminated + 10 > len(stopped_rock_coords):
			stopped_rock_coords.append([False, False, False, False, False, False, False])

		#if len(stopped_rock_coords) % 1_000 == 0:
		#	print("stopped_rock_coords y size is: {}".format(len(stopped_rock_coords)))
		#	print("low_rows_eliminated: {}".format(low_rows_eliminated))

# display final pile of rocks
#for y in range(len(stopped_rock_coords)-1, -1, -1):
#	row = ''.join([' ' if x == False else '#' for x in stopped_rock_coords[y]])
#	print('|{}|'.format(row))
#print("+-------+")
#print(".")
#print("..")
#print("...")

print("highest_stopped_rock_pos: [{}]".format(highest_stopped_rock_pos + 1))
print("final stopped_rock_coords y size is: {}".format(len(stopped_rock_coords)))
print("final low_rows_eliminated: {}".format(low_rows_eliminated))
