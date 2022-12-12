# python 3

import sys
import random

start_x = 0
start_y = 0
end_x = 0
end_y = 0
size_x = 0
size_y = 0
grid = []

# since there's no need to visit the same position
#   twice, we can track the fewest steps taken for
#   each position, and cancel the traversal if we
#   end up at a position having taken more steps to
#   get there than we've previously taken via another
#   route
best_step_counts = []

# whelp, the puzzle input exceeds python's recursion
#   depth limit.  so save our place and resume later
#   if recursion depth gets big
recursion_save_points = []

shortest_route_length = -1

def take_all_possible_steps(from_x, from_y, route, recursion_depth):
	global end_x
	global end_y
	global size_x
	global size_y
	global grid
	global best_step_counts
	global recursion_save_points
	global shortest_route_length

	# check stop condition
	if end_x == from_x and end_y == from_y:
		if shortest_route_length < 0 or len(route) -1 < shortest_route_length:
			shortest_route_length = len(route) - 1
			# the first position doesn't count as a step, so subtract 1
			print("route found with [{}] steps".format(len(route)-1))
			print(route)

	if recursion_depth > 10:
		recursion_save_points.append((from_x, from_y, route))
		return

	current_height = grid[from_x][from_y]

	if best_step_counts[from_x][from_y] < 0 or best_step_counts[from_x][from_y] > len(route):
		best_step_counts[from_x][from_y] = len(route)
	else:
		return

	if len(route) > 10000:
		return

	new_route = route.copy()
	new_x = from_x - 1
	if new_x >= 0:
		if grid[new_x][from_y] <= current_height + 1:
			#if best_step_counts[new_x][from_y] < 0 or best_step_counts[new_x][from_y] > len(route) + 1:
			new_route.append((new_x, from_y))
			take_all_possible_steps(new_x, from_y, new_route, recursion_depth+1)

	new_route = route.copy()
	new_x = from_x + 1
	if new_x < size_x:
		if grid[new_x][from_y] <= current_height + 1:
			new_route.append((new_x, from_y))
			take_all_possible_steps(new_x, from_y, new_route, recursion_depth+1)

	new_route = route.copy()
	new_y = from_y - 1
	if new_y >= 0:
		if grid[from_x][new_y] <= current_height + 1:
			new_route.append((from_x, new_y))
			take_all_possible_steps(from_x, new_y, new_route, recursion_depth+1)

	new_route = route.copy()
	new_y = from_y + 1
	if new_y < size_y:
		if grid[from_x][new_y] <= current_height + 1:
			new_route.append((from_x, new_y))
			take_all_possible_steps(from_x, new_y, new_route, recursion_depth+1)

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# use ord() function to translate chars to ints
	grid.append([ord(i) for i in line])

	start_index = line.find('S')
	if start_index != -1:
		start_x = len(grid) - 1
		start_y = start_index
		# the start position is always at "a" height
		grid[-1][start_index] = ord('a')

	end_index = line.find('E')	
	if end_index != -1:
		end_x = len(grid) - 1
		end_y = end_index
		# the end position is always at "z" height
		grid[-1][end_index] = ord('z')

	#print("line [{}] becomes".format(line))
	#print(grid[-1])

size_x = len(grid)
size_y = len(grid[0])
for x in range(0, size_x):
	best_step_counts.append([])
	for y in range(0, size_y):
		best_step_counts[-1].append(-1)


#print("start is at ({},{})".format(start_x, start_y))
#print("end is at ({},{})".format(end_x, end_y))

take_all_possible_steps(start_x, start_y, [(start_x, start_y)], 0)

while len(recursion_save_points) > 0:
	# probabilistic printing of recursion save points size
	if random.randint(0, 100) == 100:
		print("recursion save points: {}".format(len(recursion_save_points)))

	#recursion_save_points.append((from_x, from_y, route))
	recursion_start = recursion_save_points.pop()
	take_all_possible_steps(recursion_start[0], recursion_start[1], recursion_start[2], 0)

print("shortest route length: {}".format(shortest_route_length))
