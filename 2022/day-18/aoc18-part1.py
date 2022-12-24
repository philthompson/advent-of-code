# python 3

import sys

lines = []

max_x = 0
max_y = 0
max_z = 0

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	split = [int(i) for i in line.split(',')]

	max_x = max(max_x, split[0])
	max_y = max(max_y, split[1])
	max_z = max(max_z, split[2])

	lines.append(split)


def get_int_representation(position):
	global max_x
	global max_y
	global max_z
	# x
	int_representation = position[0] <<(max_y.bit_length() + max_z.bit_length())
	# y
	int_representation |= position[1] <<(max_z.bit_length())
	# z
	int_representation |= position[2]

	return int_representation

def check_for_cube(from_position, relative_to_position):
	global cube_locations
	global max_x
	global max_y
	global max_z

	x = from_position[0] + relative_to_position[0]
	y = from_position[1] + relative_to_position[1]
	z = from_position[2] + relative_to_position[2]

	if x < 0 or x > max_x or y < 0 or y > max_y or z < 0 or z > max_z:
		return False

	return get_int_representation([x, y, z]) in cube_locations

cube_locations = set()

# store positions of cubes encoded into single ints
for line in lines:
	cube_locations.add(get_int_representation(line))

total_surface_area = 0

# check for presence of cubes adjacent to each face of each cube
for line in lines:
	# minus x
	total_surface_area += 0 if check_for_cube(line, (-1, 0, 0)) else 1

	# plus x
	total_surface_area += 0 if check_for_cube(line, (1, 0, 0)) else 1

	# minus y
	total_surface_area += 0 if check_for_cube(line, (0, -1, 0)) else 1

	# plus y
	total_surface_area += 0 if check_for_cube(line, (0, 1, 0)) else 1

	# minus z
	total_surface_area += 0 if check_for_cube(line, (0, 0, -1)) else 1

	# plus z
	total_surface_area += 0 if check_for_cube(line, (0, 0, 1)) else 1

print("total_surface_area: {}".format(total_surface_area))
