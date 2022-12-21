# python 3

import sys
import time

recursion_save_points = []

last_elimination_timestamp = -1

class Valve:
	def __init__(self, name, rate, names_connected_to):
		self.name = name
		self.rate = rate
		self.names_connected_to = names_connected_to

class Context:
	def __init__(self):
		self.sequence = []
		self.elephant_sequence = []
		self.open_valves = []
		self.location = 'AA'
		self.elephant_location = 'AA'
		self.dest_valve = 'AA'
		self.elephant_dest_valve = 'AA'
		self.saved_total_flow = -1

	def make_copy(self):
		dupe = Context()
		dupe.sequence = self.sequence.copy()
		dupe.elephant_sequence = self.elephant_sequence.copy()
		dupe.open_valves = self.open_valves.copy()
		dupe.location = self.location
		dupe.elephant_location = self.elephant_location
		dupe.dest_valve = self.dest_valve
		dupe.elephant_dest_valve = self.elephant_dest_valve
		return dupe

	def is_openable(self, loc):
		global valves
		return (not loc in self.open_valves) and valves[loc].rate > 0

	def open(self):
		global valves
		self.sequence.append('o')
		self.open_valves.append(self.location)
		return self

	def elephant_open(self):
		global valves
		self.elephant_sequence.append('o')
		self.open_valves.append(self.elephant_location)
		return self

	def wait(self):
		self.sequence.append('w')
		return self

	def elephant_wait(self):
		self.elephant_sequence.append('w')
		return self

	def move(self, valve_name):
		self.sequence.append(valve_name)
		self.location = valve_name
		return self

	def elephant_move(self, valve_name):
		self.elephant_sequence.append(valve_name)
		self.elephant_location = valve_name
		return self

	# not actually an entry in the sequence
	def new_dest_copy(self, new_dest):
		ctx = self.make_copy()
		ctx.dest_valve = new_dest
		return ctx

	# not actually an entry in the sequence
	def elephant_new_dest_copy(self, new_dest):
		ctx = self.make_copy()
		ctx.elephant_dest_valve = new_dest
		return ctx

	def get_total_flow(self):
		global valves

		if self.saved_total_flow > -1:
			return self.saved_total_flow

		#if len(self.sequence) != len(self.elephant_sequence):
		#	print("human ({}) and elephant ({}) sequences are different lengths".format(len(self.sequence), len(self.elephant_sequence)))
		#	print("h: {}".format(self.sequence))
		#	print("e: {}".format(self.elephant_sequence))
		#	sys.exit()
		all_opened = []
		total_flow = 0
		flow_rate = 0
		loc = 'AA'
		ele_loc = 'AA'
		for i in range(0, len(self.sequence)):
			total_flow += flow_rate
			if self.sequence[i] == 'o':
				#if loc in all_opened:
				#	print("human tried to open already-opened valve {}".format(loc))
				#	print("h: {}".format(self.sequence))
				#	print("e: {}".format(self.elephant_sequence))
				#	sys.exit()
				flow_rate += valves[loc].rate
			elif self.sequence[i] != 'w':
				#if self.sequence[i] not in valves[loc].names_connected_to:
				#	print("human tried to move to non-adjacent valve {}".format(self.sequence[i]))
				#	print("h: {}".format(self.sequence))
				#	print("e: {}".format(self.elephant_sequence))
				#	sys.exit()
				loc = self.sequence[i]
			if self.elephant_sequence[i] == 'o':
				#if ele_loc in all_opened:
				#	print("elephant tried to open already-opened valve {}".format(ele_loc))
				#	print("h: {}".format(self.sequence))
				#	print("e: {}".format(self.elephant_sequence))
				#	sys.exit()
				flow_rate += valves[ele_loc].rate
			elif self.elephant_sequence[i] != 'w':
				#if self.elephant_sequence[i] not in valves[ele_loc].names_connected_to:
				#	print("elephant tried to move to non-adjacent valve {}".format(self.elephant_sequence[i]))
				#	print("h: {}".format(self.sequence))
				#	print("e: {}".format(self.elephant_sequence))
				#	sys.exit()
				ele_loc = self.elephant_sequence[i]
		self.saved_total_flow = total_flow
		return total_flow

def traverse(ctx, recursion_depth):
	global best_ctx
	global recursion_save_points
	global valves
	global valves_with_positive_flow
	global openable_valves
	global complete_sequences_eliminated
	global last_elimination_timestamp

	if recursion_depth > 12:
		recursion_save_points.append(ctx)
		return

	if len(ctx.sequence) >= 26 and len(ctx.elephant_sequence) >= 26:
		if ctx.get_total_flow() > best_ctx.get_total_flow():
			print("completed sequence has flow {} which is better than previous best of {}".format(ctx.get_total_flow(), best_ctx.get_total_flow()))
			best_ctx = ctx
		else:
			complete_sequences_eliminated += 1
			if complete_sequences_eliminated % 1_000_000 == 0:
				ts_now = time.time()
				if last_elimination_timestamp > 0:
					ts_diff = ts_now - last_elimination_timestamp
					print("sequences per second: [{}]".format(1_000_000.0 / ts_diff))
				last_elimination_timestamp = ts_now
				print("complete_sequences_eliminated: [{}]".format(complete_sequences_eliminated))
		return

	# we both must wait here
	if len(ctx.open_valves) == openable_valves:
		if len(ctx.sequence) < 26:
			ctx.wait()
		if len(ctx.elephant_sequence) < 26:
			ctx.elephant_wait()
		traverse(ctx, recursion_depth+1)

	else:

		#########
		# human #
		#########

		human_forks = []

		# if human is done, do nothing
		if len(ctx.sequence) >= 26:
			human_forks.append(ctx)

		else:
			# if valve has flow rate > 0, and is not opened, we open it here
			if ctx.location == ctx.dest_valve:
				if ctx.is_openable(ctx.location):
					ctx.open()
					human_forks.append(ctx)

				# pick another unopened valve (only one with positive flow!) to move to
				else:
					# if the elephant is at/moving to the last openable valve,
					#   we must wait
					if len(ctx.open_valves) + 1 == openable_valves and ctx.is_openable(ctx.elephant_dest_valve):
						ctx.wait()
						human_forks.append(ctx)
					for valve in valves_with_positive_flow:
						if not valve in ctx.open_valves and valve != ctx.elephant_dest_valve:
							human_forks.append(ctx.new_dest_copy(valve))

			# continue moving toward destination valve
			else:
				next_valve = next_valve_on_route_between_valves(ctx.location, ctx.dest_valve)
				ctx.move(next_valve)
				human_forks.append(ctx)

		############
		# elephant #
		############

		for human_ctx in human_forks:
			if len(human_ctx.elephant_sequence) >= 26:
				traverse(human_ctx, recursion_depth+1)
				continue

			# if the human opened the last valve, or is going to, we must wait
			if len(human_ctx.open_valves) == openable_valves or (len(human_ctx.open_valves) + 1 == openable_valves and human_ctx.is_openable(ctx.dest_valve)):
				traverse(human_ctx.elephant_wait(), recursion_depth+1)

			else:

				# if valve has flow rate > 0, and is not opened, we open it here
				if human_ctx.elephant_location == human_ctx.elephant_dest_valve:
					if human_ctx.is_openable(human_ctx.elephant_location):
						traverse(human_ctx.elephant_open(), recursion_depth+1)

					# pick another unopened valve (only one with positive flow!) to move to
					else:
						for valve in valves_with_positive_flow:
							if not valve in human_ctx.open_valves and valve != human_ctx.dest_valve:
								traverse(human_ctx.elephant_new_dest_copy(valve), recursion_depth+1)

				# continue moving toward destination valve
				else:
					next_valve = next_valve_on_route_between_valves(human_ctx.elephant_location, human_ctx.elephant_dest_valve)
					traverse(human_ctx.elephant_move(next_valve), recursion_depth+1)

# Dijkstra's, written from prose description at:
#   https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
def next_valve_on_route_between_valves(from_valve, to_valve):
	global next_valve_from_valve_to_valve
	global valves

	route_from_nodes = {}

	if from_valve == to_valve:
		return from_valve

	# check cache
	if from_valve in next_valve_from_valve_to_valve:
		if to_valve in next_valve_from_valve_to_valve[from_valve]:
			return next_valve_from_valve_to_valve[from_valve][to_valve]
	else:
		next_valve_from_valve_to_valve[from_valve] = {}

	unvisited_valves = set()
	for valve in valves:
		unvisited_valves.add(valve)

	tentative_distances = {}

	for valve in valves:
		tentative_distances[valve] = 1_000_000_000

	tentative_distances[from_valve] = 0
	current_valve = from_valve

	while len(unvisited_valves) > 0:

		for neighbor in valves[current_valve].names_connected_to:
			if not neighbor in unvisited_valves:
				continue
			neighbor_distance = tentative_distances[current_valve] + 1
			if neighbor_distance < tentative_distances[neighbor]:
				tentative_distances[neighbor] = neighbor_distance
				route_from_nodes[neighbor] = current_valve

		unvisited_valves.remove(current_valve)

		# we are done once the to_valve is visited
		if to_valve not in unvisited_valves:
			break

		# set the new "current" valve to the unvisited with shortest tentative distance
		tentative_dists = [tentative_distances[x] for x in unvisited_valves]
		tentative_dists.sort()
		#print('for selecting next "current", tentative_dists: {}'.format(tentative_dists))
		current_valve = -1
		for unvisited in unvisited_valves:
			if tentative_distances[unvisited] == tentative_dists[0]:
				#print('  unvisited [{}] has the smallest tentative distance {}, so it is the new "current"'.format(unvisited, tentative_distances[unvisited]))
				current_valve = unvisited
				break

	route = [to_valve]
	cursor = to_valve
	while cursor != from_valve:
		prev = route_from_nodes[cursor]
		route.insert(0, prev)
		cursor = prev

	if to_valve != route[-1]:
		print("the pathfinding goal [{}] is not the last entry in the route from [{}]: {}".format(to_valve, from_valve, route))
	if from_valve != route[0]:
		print("the pathfinding start [{}] is not the first entry in the route to [{}]: {}".format(from_valve, to_valve, route))
	
	# store result in cache:
	# since the first entry in the route is the start valve, the next
	#  entry is what we want
	next_valve_from_valve_to_valve[from_valve][to_valve] = route[1]

	return route[1]

openable_valves = 0
valves = {}
valves_with_positive_flow = {}

# calculate once, and store for quick lookup:
# next_valve_from_valve_to_valve[from][to] = next
next_valve_from_valve_to_valve = {}

complete_sequences_eliminated = 0

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
	fields = line.split(' ')
	valves[fields[1]] = Valve(fields[1], int(fields[4][5:-1]), [i.replace(',','') for i in fields[9:]])

for valve in valves:
	if valves[valve].rate > 0:
		openable_valves += 1
		valves_with_positive_flow[valve] = valves[valve]

# global context that will be accessed by all
#   instances of recursive traverse() function
best_ctx = Context()

traverse(Context(), 0)

print("recursion_save_points: {}".format(len(recursion_save_points)))

while len(recursion_save_points) > 0:
	if len(recursion_save_points) % 50000 == 0:
		print("have {} recursion_save_points".format(len(recursion_save_points)))
		print("    best total flow: {}".format(best_ctx.get_total_flow()))

	traverse(recursion_save_points.pop(), 0)


h_loc = 'AA'
e_loc = 'AA'
during_minute = 0
open_valves = []
flow_rate = 0
for i in range(0, len(best_ctx.sequence)):
	h_step = best_ctx.sequence[i]
	e_step = best_ctx.elephant_sequence[i]
	during_minute += 1
	print("== Minute {} ==".format(during_minute))

	if len(open_valves) == 0:
		print("No valves are open.")
	else:
		print("Valves {} are open, releasing {} pressure.".format(open_valves, flow_rate))

	if h_step == 'o':
		print("You open valve {}.".format(h_loc))
		open_valves.append(h_loc)
		flow_rate += valves[h_loc].rate
	elif h_step != 'w':
		print("You move to valve {}.".format(h_step))
		h_loc = h_step

	if e_step == 'o':
		print("The elephant opens valve {}.".format(e_loc))
		open_valves.append(e_loc)
		flow_rate += valves[e_loc].rate
	elif e_step != 'w':
		print("The elephant moves to valve {}.".format(e_step))
		e_loc = e_step

	print('')

print("total flow released: [{}]".format(best_ctx.get_total_flow()))
