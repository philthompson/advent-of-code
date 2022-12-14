# python 3

import sys
import random

# find bounds of rock
rock_min_x = -1
rock_max_x = -1
rock_min_y = 0
rock_max_y = -1

# parsed segments
rock_segments = []

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	segment = []

	for point in line.split('->'):
		coords = point.split(',')
		x = int(coords[0].strip())
		y = int(coords[1].strip())

		if rock_min_x == -1 or x < rock_min_x:
			rock_min_x = x

		if rock_max_x == -1 or x > rock_max_x:
			rock_max_x = x

		if rock_min_y == -1 or y < rock_min_y:
			rock_min_y = y

		if rock_max_y == -1 or y > rock_max_y:
			rock_max_y = y

		segment.append((x, y))

	rock_segments.append(segment)

# expand bounds to allow sand to pile up on endless floor
#endless_floor_y = rock_max_y + 2
rock_max_y += 2

# max width of pile on endless floor cannot exceed width of triangle
#   with tip at (widest_x, 0)

# find max extent of possible sand pile in minus x
#   direction
widest_triangle_tip_x = min(0, rock_min_x)
# 10 units wider, for breathing room
widest_triangle_tip_x -= 10
# the base of the widest tip is equal to the height
#   above the floor
rock_min_x = widest_triangle_tip_x - rock_max_y

# find max extent of possible sand pile in plus x
#   direction
widest_triangle_tip_x = max(0, rock_max_x)
# 10 units wider, for breathing room
widest_triangle_tip_x += 10
# the base of the widest tip is equal to the height
#   above the floor
rock_max_x = widest_triangle_tip_x + rock_max_y


# build 2D list using min x/y as offsets
range_x = rock_max_x - rock_min_x
range_y = rock_max_y - rock_min_y

# ints for the type
AIR = 0
ROCK = 1
SAND = 2

arena = []

for x in range(0, range_x + 1):
	at_x = []
	for y in range(0, range_y + 1):
		if y >= rock_max_y:
			at_x.append(ROCK)
		else:
			at_x.append(AIR)
	arena.append(at_x)

prev_segment = -1
for segment in rock_segments:
	
	prev_coord = -1
	for coord in segment:
		if prev_coord == -1:
			prev_coord = coord
			continue

		#print("filling in all points of segment ({},{}) to ({},{})".format(prev_coord[0], prev_coord[1], coord[0], coord[1]))

		for x in range(min(prev_coord[0], coord[0]), max(prev_coord[0], coord[0]) + 1):	
			cursor_x = x
			for y in range(min(prev_coord[1], coord[1]), max(prev_coord[1], coord[1]) + 1):
				cursor_y = y
				#print("    rock at ({},{}) - translated to ({},{})".format(cursor_x, cursor_y, cursor_x - rock_min_x, cursor_y - rock_min_y))
				arena[cursor_x - rock_min_x][cursor_y - rock_min_y] = ROCK

		prev_coord = coord

# print out grid here, for debugging
for x in arena:
	print(''.join(['.' if i == AIR else '#' if i == ROCK else '?' for i in x]))

print("=======~=======~=======~=======~=======~=======")

sand_count = 0

# sand enters at (500,0)
while True:
	sand_x = 500
	sand_y = 0

	# check that the sand hasn't piled up to block the
	#   entry point
	if arena[sand_x - rock_min_x][sand_y - rock_min_y] == SAND:
		break

	while True:
		if arena[sand_x - rock_min_x][sand_y - rock_min_y + 1] == AIR:
			sand_y += 1
		elif arena[sand_x - rock_min_x - 1][sand_y - rock_min_y + 1] == AIR:
			sand_x -= 1
			sand_y += 1
		elif arena[sand_x - rock_min_x + 1][sand_y - rock_min_y + 1] == AIR:
			sand_x += 1
			sand_y += 1
		else:
			arena[sand_x - rock_min_x][sand_y - rock_min_y] = SAND
			sand_count += 1
			break

# print out grid here, for debugging
for x in arena:
	print(''.join(['.' if i == AIR else '#' if i == ROCK else 'o' if i == SAND else '?' for i in x]))

print("units of sand that came to a rest: [{}]".format(sand_count))