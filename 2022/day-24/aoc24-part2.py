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
# for part 2, we can track all of our start-adjacent
#   to end-adjacent paths (from all possible nodes,
#   and therefore all possible times)
#
# we can then try every combination with the appropriate
#   waiting time between them
#
# prints more status updates, and abandons guaranteed
#   inferior solutions while in the final solution phase
#
# attempt to get an ETA for script completion during the
#   final solution-finding phase (doesn't seem to work)
#
# improve waiting calculation, and abandon sequences
#   involving a long wait at one end and more definitely
#   inferior sequences
#
# just adds caching for best_traversal dict lookups
#
# adds more abandoning criteria involving the best known
#   traversals in both directions
#
# removes inaccurate ETA calculations/display
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

#all_nodes = set([end_pos])
all_nodes = set()

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




initial_infinity_distance = 99999999

# dictionary of best solutions for each "start" to
#   each "end" (both directions) where we also
#   keep the (row,col,minute) node itself
best_traversals = {}

best_from_one_end = {'start-to-end': initial_infinity_distance, 'end-to-start': initial_infinity_distance}

for algo_params in [(start_nodes, end_nodes, 'start-to-end'),(end_nodes, start_nodes, 'end-to-start')]:

	# Dijkstra's, written from prose description at:
	#   https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
	for start_node in algo_params[0]:
		start_row = start_node >>17
		start_col = (start_node >> 10) & 0b00000001111111
		start_minute = start_node & 0b000000000000001111111111
		print("starting algorithm from {}".format((start_row, start_col, start_minute)))

		# copy end nodes
		ends_nodes_remaining = set(algo_params[1])
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

		#(<minutes>, <node>)
		all_ends = {}
		best_in_this_direction = initial_infinity_distance
		for end_node in algo_params[1]:
			if tentative_distances[end_node] == initial_infinity_distance:
				continue
			end_minute = end_node & 0b000000000000001111111111
			all_ends[end_node] = (tentative_distances[end_node], end_node)
			if tentative_distances[end_node] < best_in_this_direction:
				print("new best {}: {}".format(algo_params[2], tentative_distances[end_node]))
				best_in_this_direction = tentative_distances[end_node]
			#print("from {} to {} takes {} minutes".format((start_adjacent_pos[0], start_adjacent_pos[1], start_minute), (end_adjacent_pos[0], end_adjacent_pos[1], end_minute), tentative_distances[end_node]))
		best_traversals[start_node] = all_ends
		if best_in_this_direction < best_from_one_end[algo_params[2]]:
			best_from_one_end[algo_params[2]] = best_in_this_direction

# release memory
neighbors_by_node = None
passable_mins_by_rowcol = None
all_nodes = None

best_solution = 99999999
solutions_tried = 0
solutions_abandoned = 0

print("we have {} traversals from either end".format(len(best_traversals)))

len_start_nodes = len(start_nodes)
len_end_nodes = len(end_nodes)

abandoned_possible_solutions = 0
last_speed_timestamp = -1
best_start_to_end = best_from_one_end['start-to-end']
best_end_to_start = best_from_one_end['end-to-start']

print("best best_start_to_end: {}".format(best_start_to_end))
print("best best_end_to_start: {}".format(best_end_to_start))

for start in best_traversals:
	if not start in start_nodes:
		continue
	start_minute = start & 0b000000000000001111111111
	# we can heuristically abandon any sequence that requires
	#   waiting a long time at one end
	if start_minute > 50:
		solutions_abandoned += 1
		abandoned_possible_solutions += len_end_nodes * len_end_nodes * len_start_nodes * len_start_nodes * len_end_nodes
		if solutions_abandoned % 10000000 == 0:
			print("now abandoned {:,} partial solutions and their {:,} dependents          ".format(solutions_abandoned, abandoned_possible_solutions))
		continue
	best_traversals_for_start = best_traversals[start]

	for end in best_traversals_for_start:
		end_mins = best_traversals_for_start[end][0]
		if start_minute + end_mins + 1 + best_end_to_start + best_start_to_end > best_solution:
			solutions_abandoned += 1
			abandoned_possible_solutions += len_end_nodes * len_start_nodes * len_start_nodes * len_end_nodes
			if solutions_abandoned % 10000000 == 0:
				print("now abandoned {:,} partial solutions and their {:,} dependents          ".format(solutions_abandoned, abandoned_possible_solutions))
			continue
		end_node = best_traversals_for_start[end][1]
		end_minute = end_node & 0b000000000000001111111111
		wait_at_end_start = (end_minute + 1) % repeat_period

		for from_end in best_traversals:
			if not from_end in end_nodes:
				continue
			from_end_minute = from_end & 0b000000000000001111111111
			wait_at_end = (from_end_minute - wait_at_end_start) % repeat_period
			# waiting at the end includes the minute required to move
			#  after waiting from the end to the end-adjacent position
			wait_at_end = 700 if wait_at_end == 0 else wait_at_end
			# we can heuristically abandon any sequence that requires
			#   waiting a long time at one end
			if wait_at_end > 100 or (start_minute + end_mins + 1 + wait_at_end + best_end_to_start + best_start_to_end) > best_solution:
				solutions_abandoned += 1
				abandoned_possible_solutions += len_start_nodes * len_start_nodes * len_end_nodes
				if solutions_abandoned % 10000000 == 0:
					print("now abandoned {:,} partial solutions and their {:,} dependents          ".format(solutions_abandoned, abandoned_possible_solutions))
				continue
			best_traversals_for_from_end = best_traversals[from_end]

			for back_to_start in best_traversals_for_from_end:
				back_to_start_mins = best_traversals_for_from_end[back_to_start][0]
				if start_minute + end_mins + 1 + wait_at_end + back_to_start_mins + 1 + best_start_to_end > best_solution:
					solutions_abandoned += 1
					abandoned_possible_solutions += len_start_nodes * len_end_nodes
					if solutions_abandoned % 10000000 == 0:
						print("now abandoned {:,} partial solutions and their {:,} dependents          ".format(solutions_abandoned, abandoned_possible_solutions))
					continue
				back_to_start_node = best_traversals_for_from_end[back_to_start][1]
				back_to_start_minute = back_to_start_node & 0b000000000000001111111111
				wait_at_start_start = (back_to_start_minute + 1) % repeat_period

				for start_again in best_traversals:
					if not start_again in start_nodes:
						continue
					start_again_minute = start_again & 0b000000000000001111111111
					# waiting at the start includes the minute required to move
					#  after waiting from the start to the start-adjacent position
					wait_at_start = (start_again_minute - wait_at_start_start) % repeat_period
					wait_at_start = 700 if wait_at_start == 0 else wait_at_start
					# we can heuristically abandon any sequence that requires
					#   waiting a long time at one end
					if wait_at_start > 100 or (start_minute + end_mins + 1 + wait_at_end + back_to_start_mins + 1 + wait_at_start + best_start_to_end) > best_solution:
						solutions_abandoned += 1
						abandoned_possible_solutions += len_end_nodes
						if solutions_abandoned % 10000000 == 0:
							print("now abandoned {:,} partial solutions and their {:,} dependents          ".format(solutions_abandoned, abandoned_possible_solutions))
						continue
					best_traversals_for_start_again = best_traversals[start_again]

					for end_again in best_traversals_for_start_again:
						end_again_mins = best_traversals_for_start_again[end_again][0]

						total = start_minute + end_mins + 1 + wait_at_end + back_to_start_mins + 1 + wait_at_start + end_again_mins + 1
						#total = start_minute + end_mins + 1

						#wait_at_end_start = (end_minute + 1) % repeat_period

						#wait_at_end = 1
						#while (wait_at_end_start + wait_at_end) % repeat_period != from_end_minute:
						# 	wait_at_end += 1

						#total += wait_at_end + back_to_start_mins + 1

						#wait_at_start_start = (back_to_start_minute + 1) % repeat_period

						#wait_at_start = 1
						#while (wait_at_start_start + wait_at_start) % repeat_period != start_again_minute:
						# 	wait_at_start += 1

						#total += wait_at_start + end_again_mins + 1

						solutions_tried += 1

						if total < best_solution:
							end_again_node = best_traversals_for_start_again[end_again][1]
							end_again_minute = end_again_node & 0b000000000000001111111111
							a = (start_adjacent_pos[0], start_adjacent_pos[1], start_minute)
							b = (end_adjacent_pos[0],   end_adjacent_pos[1],   end_minute)
							a_b = end_mins
							c = (end_adjacent_pos[0],   end_adjacent_pos[1],   from_end_minute)
							d = (start_adjacent_pos[0], start_adjacent_pos[1], back_to_start_minute)
							c_d = back_to_start_mins
							e = (start_adjacent_pos[0], start_adjacent_pos[1], start_again_minute)
							f = (end_adjacent_pos[0],   end_adjacent_pos[1],   end_again_minute)
							e_f = end_again_mins
							print("from {} to {} takes {}, then {} to {} takes {}, then {} to {} takes {}, totaling {} minutes with waiting".format(a, b, a_b, c, d, c_d, e, f, e_f, total))
							best_solution = total
						#else:
						#	print("total of {} is not the best".format(total))

						if solutions_tried % 1000000 == 0:
							ts_now = time.time()
							if last_speed_timestamp > 0:
								ts_diff = ts_now - last_speed_timestamp
								tests_per_second = int(1000000 / ts_diff)
								sys.stdout.write("have tested {:,} solutions ({:.1f}%) (best={:,}) at {:,}/sec          \r".format(solutions_tried, pct_done, best_solution, tests_per_second))
								sys.stdout.flush()
							last_speed_timestamp = ts_now

print("")
print("solutions tried: {:,}".format(solutions_tried))
print("abandoned {:,} partial solutions and their {:,} dependents".format(solutions_abandoned, abandoned_possible_solutions))
print("===================================")
print("best solution: {}".format(best_solution))
