# python 2 for pypy
#
# the version i used for my first time attempting the puzzle,
#   without any outside help/clues, took 4 days to run and
#   dropped every single rock!  (and got the right answer!)
#
# after completing the entire Advent of Code 2022, i went
#   back to see how people accomplished this one...
#
# this version uses a hash of the rock positions, the current
#   position in the jet loop, and the current rock type, to
#   detect a repeat scenario -- as soon as it finds a repeat,
#   it skips ahead as far as it can.  the simulation finishes
#   normally after that, and ends up at the correct answer
#   after a total of 1.75s!
#

import sys
import hashlib
import json

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

initial_hash_all_rocks = None
initial_stopped_rock_height = None
did_skip = False

a_trillion = 1000000000000

i = 0
while i < a_trillion:
	
	# reset for new rock
	rock_left_pos = 2
	rock_bottom_pos = highest_stopped_rock_pos + 4 - low_rows_eliminated
	rock_is_stopped = False
	rock_rel_coords = rel_coords_by_rock_type[i % 5]

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

	# use relative heights of lowest_solid_y_at_x for hashing
	#   to find a repeat of those values with a repeat in the
	#   jet pattern
	if i == 1000000:
		initial_stopped_rock_height = highest_stopped_rock_pos
		initial_hash_all_rocks = hashlib.sha256()
		# thanks to https://stackoverflow.com/a/22003440/259456
		initial_hash_all_rocks.update(json.dumps(stopped_rock_coords, sort_keys=True))
		initial_hash_all_rocks.update("-and jet_idx:{} and rock_type:{}".format(jet_idx, i % 5))
		initial_hash_all_rocks = initial_hash_all_rocks.hexdigest()
	elif not did_skip and i > 1000000:
		overall_rock_number = i
		compare_hash = hashlib.sha256()
		compare_hash = hashlib.sha256()
		compare_hash.update(json.dumps(stopped_rock_coords, sort_keys=True))
		compare_hash.update("-and jet_idx:{} and rock_type:{}".format(jet_idx, i % 5))
		if compare_hash.hexdigest() == initial_hash_all_rocks:
			new_stopped_rock_height = highest_stopped_rock_pos
			# increment the rock counter (without going past 1 trillion) and rock height, and that's it?
			print("rocks 1,000,000 and {:,} may be a match!".format(overall_rock_number))

			did_skip = True
			skip_i = overall_rock_number - 1000000
			skip_height = new_stopped_rock_height - initial_stopped_rock_height
			while i + skip_i < a_trillion:
				i += skip_i
				highest_stopped_rock_pos += skip_height
				low_rows_eliminated += skip_height

			print("skipped {:,} rocks...".format(i - overall_rock_number))

	i += 1

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
