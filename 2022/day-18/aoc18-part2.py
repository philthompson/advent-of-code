# python 3

import sys

lines = []

min_x = 1_000_000
min_y = 1_000_000
min_z = 1_000_000

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

	min_x = min(min_x, split[0])
	min_y = min(min_y, split[1])
	min_z = min(min_z, split[2])

	lines.append(split)

print("max x/y/z: {}/{}/{}".format(max_x, max_y, max_z))
print("min x/y/z: {}/{}/{}".format(min_x, min_y, min_z))

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

def check_for_exterior(from_position, relative_to_position):
	global cube_locations
	global exterior_cubes
	global min_x
	global min_y
	global min_z
	global max_x
	global max_y
	global max_z

	x = from_position[0] + relative_to_position[0]
	y = from_position[1] + relative_to_position[1]
	z = from_position[2] + relative_to_position[2]

	if x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z:
		return True

	int_representation = get_int_representation([x, y, z])

	return int_representation in exterior_cubes

def pathfind_to_boundary(x, y, z):
	global cube_locations
	global exterior_cubes
	global visited_cubes
	global min_x
	global min_y
	global min_z
	global max_x
	global max_y
	global max_z

	int_representation = get_int_representation([x, y, z])

	was_visited = int_representation in visited_cubes

	visited_cubes.add(int_representation)

	if was_visited or int_representation in cube_locations or int_representation in exterior_cubes:
		return

	if x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x - 1, y, z]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x + 1, y, z]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x, y - 1, z]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x, y + 1, z]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x, y, z - 1]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return

	neighbor = [x, y, z + 1]
	pathfind_to_boundary(neighbor[0], neighbor[1], neighbor[2])
	if get_int_representation(neighbor) in exterior_cubes:
		exterior_cubes.add(int_representation)
		return


cube_locations = set()

# store positions of cubes encoded into single ints
for line in lines:
	cube_locations.add(get_int_representation(line))

# from any position, if you can proceed along ANY path without
#   encountering a cube, all the way to the boundary, the position
#   is exterior to the rock (and so are all cubes along that path)

# from any position, if there are no paths to the boundary, the
#   position is INTERIOR to the rock, and can be filled in with
#   an artificial cube

# after all interior cubes are filled in, count the surface area
#   like before

exterior_cubes = set()

visited_cubes = set()

exterior_count_before = -1
exterior_count_after = 0

while exterior_count_after > exterior_count_before:

	print("running the algorithm")
	visited_cubes = set()
	exterior_count_before = len(exterior_cubes)

	# check for interior empty cubes to fill in
	for x in range(min_x, max_x + 1):
		for y in range(min_y, max_y + 1):
			for z in range(min_z, max_z + 1):
				pathfind_to_boundary(x, y, z)

	exterior_count_after = len(exterior_cubes)


total_surface_area = 0

# check for presence of cubes adjacent to each face of each cube
for line in lines:
	# minus x
	total_surface_area += 1 if check_for_exterior(line, (-1, 0, 0)) else 0

	# plus x
	total_surface_area += 1 if check_for_exterior(line, (1, 0, 0)) else 0

	# minus y
	total_surface_area += 1 if check_for_exterior(line, (0, -1, 0)) else 0

	# plus y
	total_surface_area += 1 if check_for_exterior(line, (0, 1, 0)) else 0

	# minus z
	total_surface_area += 1 if check_for_exterior(line, (0, 0, -1)) else 0

	# plus z
	total_surface_area += 1 if check_for_exterior(line, (0, 0, 1)) else 0

print("total_surface_area: {}".format(total_surface_area))
