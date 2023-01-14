# python 2 so this runs with pypy
#
# trying Dijkstra's, with start_pos and end_pos
#   are the start- and end-adjacent positions
#   for the purposes of the algorithm, where the
#   waiting+movement times for the start/end are
#   added on at the end
#
# 2D graph nodes are only passable at certain minutes
#   creating a 3D graph
#
# this uses proper dictionaries of dictionaries, rather
#   than a single dictionary keyed by 2-tuple
#
# this uses a single bitwise-encoded int for each node
#   (row, col, minute)
#
# this more intelligently tracks the smallest known
#   tentative distance with a separate smaller
#   "unvisited neighbors" dictionary
#
#

import sys
import hashlib
import time

# keys are (row, col)
#
# two dicts: alternate between them
cells = [{},{}]
this_map_idx = 0
next_map_idx = 1

# min/max row a blizzard gust can move through
#   (there are now up/down gusts at the start
#   and end columns)
min_gust_row = 1
max_gust_row = -1

# min/max col a blizzard gust can move through
#   (there are now up/down gusts at the start
#   and end columns)
min_gust_col = 1
max_gust_col = 1

start_pos = (0,1)

row = -1

for line in sys.stdin:
	row += 1
	line = line.strip()

	if len(line) == 0:
		continue

	# last columns of the last row look like this
	if line.endswith('###.#'):
		break

	max_gust_row += 1

	if max_gust_row == 0:
		max_gust_col = len(line) - 2
		continue

	for col in range(1, len(line) - 1):
		char = line[col]
		if char == '<':
			cells[0][(row, col)] = 'L'
		elif char == '>':
			cells[0][(row, col)] = 'R'
		elif char == '^':
			cells[0][(row, col)] = 'U'
		elif char == 'v':
			cells[0][(row, col)] = 'D'
		else:
			cells[0][(row, col)] = ''

end_pos = (max_gust_row + 1, max_gust_col)


print("min_gust_row: {}".format(min_gust_row))
print("max_gust_row: {}".format(max_gust_row))
print("min_gust_col: {}".format(min_gust_col))
print("max_gust_col: {}".format(max_gust_col))
print("end_pos: {}".format(end_pos))

# do initial iteration over the entire map for two
#   purposes:
# - calculate hash of blizzard gust state, to find
#     a potential repeat sooner than LCM(width,height)
# - initialize empty arrays for passable minutes
initial_hash = hashlib.sha256()
passable_mins_by_rowcol = {}
for row in range(min_gust_row, max_gust_row + 1):
	for col in range(min_gust_col, max_gust_col + 1):
		pos = (row, col)
		pos_gust = cells[0][pos]
		initial_hash.update(pos_gust + ',' if pos_gust != '' else '.,')
		passable_mins_by_rowcol[pos] = set()

initial_hash = initial_hash.hexdigest()

def find_lcm(a, b):
	big = a * b
	lcm = max(a, b)
	while lcm < big:
		if lcm % b == 0 and lcm % a == 0:
			return lcm
		lcm += max(a, b)
	return big

# the map will repeat itself every least common multiple
#   of length and width minutes (if not sooner, due to the
#   arrangement of the blizzard gusts)
repeat_period = find_lcm(max_gust_row - min_gust_row + 1, max_gust_col - min_gust_col + 1)

print("rows are [{}-{}], cols are [{}-{}], therefore the map will repeat itself every [{}] minutes, if not fewer".format(min_gust_row, max_gust_row, min_gust_col, max_gust_col, repeat_period))

for i in range(0, repeat_period):

	cells[next_map_idx] = {}

	if i > 0:
		gusts_hash = hashlib.sha256()
		for row in range(min_gust_row, max_gust_row + 1):
			for col in range(min_gust_col, max_gust_col + 1):
				pos = (row, col)
				pos_gust = cells[this_map_idx].get(pos, '')
				gusts_hash.update(pos_gust + ',' if pos_gust != '' else '.,')
		if gusts_hash.hexdigest() == initial_hash:
			print("repeat of gusts found early, at minute {}".format(i))
			repeat_period = i
			break

	for row in range(min_gust_row, max_gust_row + 1):
		for col in range(min_gust_col, max_gust_col + 1):
			pos = (row, col)

			gusts = cells[this_map_idx].get(pos, '')
			#if pos == (1,1):
			#	print("at minute {} (map idx {}), pos {} has gusts: {}".format(i, this_map_idx, pos, gusts))

			# if there are no gusts at this position, mark
			#   this as a "passable" minute at this position
			if gusts == '':
				passable_mins_by_rowcol[pos].add(i)
				#if pos == (1,1):
				#	print("now passable in minutes {}".format(passable_mins_by_rowcol[pos][0:10]))
				continue

			# if there are gusts, move them to their neighbor
			#   position for the next minute
			for gust in gusts:
				new_row = row
				new_col = col
				if gust == 'L':
					new_col = col - 1
					if col == min_gust_col:
						new_col = max_gust_col
				elif gust == 'R':
					new_col = col + 1
					if col == max_gust_col:
						new_col = min_gust_col
				elif gust == 'U':
					new_row = row - 1
					if row == min_gust_row:
						new_row = max_gust_row
				elif gust == 'D':
					new_row = row + 1
					if row == max_gust_row:
						new_row = min_gust_col
				else:
					print("unexpected gust at {}: {}".format(pos, gust))
					sys.exit(1)
				new_pos = (new_row, new_col)
				if not new_pos in cells[next_map_idx]:
					cells[next_map_idx][new_pos] = ''
				cells[next_map_idx][new_pos] += gust

	this_map_idx  = (this_map_idx + 1) % 2
	next_map_idx  = (next_map_idx + 1) % 2


#
##
####
########
################
################################
################################################################

# release memory...
cells = None

all_nodes = set([end_pos])

# start at each passable minute of the start-adjacent node
start_adjacent_pos = (start_pos[0]+1, start_pos[1])
end_adjacent_pos = (end_pos[0]-1, end_pos[1])
start_nodes = set()
end_nodes = set()

neighbors_by_node = {}

for pos,passable_mins in passable_mins_by_rowcol.items():
	row = pos[0]
	col = pos[1]
	for minute in passable_mins:
		# shift left 7 bits to make room for all 100 columns
		# shift left 10 bits to make room for all 700 minutes 
		bitwise_encoded = ((row <<17) | (col <<10)) | minute
		all_nodes.add(bitwise_encoded)
		neighbors_by_node[bitwise_encoded] = set()
		if pos == start_adjacent_pos:
			start_nodes.add(bitwise_encoded)
		elif pos == end_adjacent_pos:
			end_nodes.add(bitwise_encoded)

		next_minute = (minute + 1) % repeat_period

		# go up, if possible
		new_pos = (row - 1, col)
		if row > min_gust_row and next_minute in passable_mins_by_rowcol[new_pos]:
			neighbors_by_node[bitwise_encoded].add(((new_pos[0] <<17) | (new_pos[1] <<10)) | next_minute)

		# go down, if possible
		new_pos = (row + 1, col)
		if row < max_gust_row and next_minute in passable_mins_by_rowcol[new_pos]:
			neighbors_by_node[bitwise_encoded].add(((new_pos[0] <<17) | (new_pos[1] <<10)) | next_minute)

		# go left, if possible
		new_pos = (row, col - 1)
		if col > min_gust_col and next_minute in passable_mins_by_rowcol[new_pos]:
			neighbors_by_node[bitwise_encoded].add(((new_pos[0] <<17) | (new_pos[1] <<10)) | next_minute)

		# go right, if possible
		new_pos = (row, col + 1)
		if col < max_gust_col and next_minute in passable_mins_by_rowcol[new_pos]:
			neighbors_by_node[bitwise_encoded].add(((new_pos[0] <<17) | (new_pos[1] <<10)) | next_minute)

		# wait in place (if possible)
		new_pos = (row, col)
		if next_minute in passable_mins_by_rowcol[new_pos]:
			neighbors_by_node[bitwise_encoded].add(((new_pos[0] <<17) | (new_pos[1] <<10)) | next_minute)

print("total of {} nodes".format(len(all_nodes)))

best_solution = 99999999
initial_infinity_distance = 99999999

# Dijkstra's, written from prose description at:
#   https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
for start_node in start_nodes:

	start_minute = start_node & 0b000000000000001111111111
	print("starting algorithm from {}".format((start_adjacent_pos[0], start_adjacent_pos[1], start_minute)))

	# copy end nodes
	ends_nodes_remaining = set(end_nodes)
	unvisited_nodes = set()
	tentative_distances = {}

	nearest_unvisited = [(initial_infinity_distance,None)]

	unvisited_neighbors = {}

	for node in all_nodes:
		unvisited_nodes.add(node)
		tentative_distances[node] = initial_infinity_distance

	tentative_distances[start_node] = 0

	current_node = start_node
	unvisited_nodes_count = len(unvisited_nodes)

	last_speed_timestamp = -1

	while unvisited_nodes_count > 0:

		if unvisited_nodes_count % 10000 == 0:
			ts_now = time.time()
			if last_speed_timestamp > 0:
				ts_diff = ts_now - last_speed_timestamp
				visited_nodes_per_sec = 10000 / ts_diff
				secs_remaining = unvisited_nodes_count / visited_nodes_per_sec
				sys.stdout.write("    {:,} unvisited nodes remain -- at {:,} nodes/sec, ETA {:.2f}s for this start node        \r".format(unvisited_nodes_count, int(visited_nodes_per_sec), secs_remaining))
				sys.stdout.flush()
			last_speed_timestamp = ts_now

		for neighbor in neighbors_by_node[current_node]:
			if not neighbor in unvisited_nodes:
				continue

			neighbor_distance = tentative_distances[current_node] + 1

			if neighbor_distance < tentative_distances[neighbor]:
				tentative_distances[neighbor] = neighbor_distance
				unvisited_neighbors[neighbor] = neighbor_distance

		if current_node in unvisited_neighbors:
			del unvisited_neighbors[current_node]
		unvisited_nodes.remove(current_node)
		unvisited_nodes_count -= 1

		# since we stop once all end_nodes have been visited, we
		#   will likely never have a totally empty unvisited_nodes
		#   set -- therefore, we don't need to check whether the
		#   set is empty here

		if current_node in ends_nodes_remaining:
			ends_nodes_remaining.remove(current_node)
			if len(ends_nodes_remaining) % 100 == 0:
				print("    {:,} end_nodes remaining to pathfind to...".format(len(ends_nodes_remaining)))
			if len(ends_nodes_remaining) == 0:
				break

		nearest_unvisited_dist = None
		nearest_unvisited_node = None

		for unvisited in unvisited_neighbors:
			if nearest_unvisited_dist == None or unvisited_neighbors[unvisited] < nearest_unvisited_dist:
				nearest_unvisited_dist = unvisited_neighbors[unvisited]
				nearest_unvisited_node = unvisited

		if nearest_unvisited_dist == None:
			for unvisited in unvisited_nodes:
				if nearest_unvisited_dist == None or tentative_distances[unvisited] < nearest_unvisited_dist:
					nearest_unvisited_dist = tentative_distances[unvisited]
					nearest_unvisited_node = unvisited

		if nearest_unvisited_dist == initial_infinity_distance:
			print("there are {:,} unreachable nodes...".format(len(unvisited_nodes)))
			break

		current_node = nearest_unvisited_node

	for end_node in end_nodes:
		end_minute = end_node & 0b000000000000001111111111
		total_minutes = start_minute + tentative_distances[end_node] + 1
		if total_minutes < best_solution:
			best_solution = total_minutes
			print("from {} to {} takes {} minutes, for a total solution of {}".format((start_adjacent_pos[0], start_adjacent_pos[1], start_minute), (end_adjacent_pos[0], end_adjacent_pos[1], end_minute), tentative_distances[end_node], total_minutes))

print("best solution: {}".format(best_solution))
