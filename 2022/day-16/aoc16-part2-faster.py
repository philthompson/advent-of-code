# python 3

import sys
import time

last_elimination_timestamp = -1

total_minutes = 26

class Valve:
	def __init__(self, name, rate, names_connected_to):
		self.name = name
		self.rate = rate
		self.names_connected_to = names_connected_to

class Context:
	def __init__(self):
		global valve_names_with_positive_flow
		self.minutes_count = 0
		self.elephant_minutes_count = 0
		self.openable_valves_remaining = valve_names_with_positive_flow.copy()
		self.location = 'AA'
		self.elephant_location = 'AA'
		self.dest_valve = 'AA'
		self.elephant_dest_valve = 'AA'
		self.total_flow = 0

	def make_copy(self):
		dupe = Context()
		dupe.minutes_count = self.minutes_count
		dupe.elephant_minutes_count = self.elephant_minutes_count
		dupe.openable_valves_remaining = self.openable_valves_remaining.copy()
		dupe.location = self.location
		dupe.elephant_location = self.elephant_location
		dupe.dest_valve = self.dest_valve
		dupe.elephant_dest_valve = self.elephant_dest_valve
		dupe.total_flow = self.total_flow
		return dupe

	def is_openable(self, loc):
		return loc in self.openable_valves_remaining

	def open(self):
		global valves
		global total_minutes
		self.minutes_count += 1
		self.openable_valves_remaining.remove(self.location)
		self.total_flow += (total_minutes - self.minutes_count) * valves[self.location].rate
		return self

	def elephant_open(self):
		global valves
		global total_minutes
		self.elephant_minutes_count += 1
		self.openable_valves_remaining.remove(self.elephant_location)
		self.total_flow += (total_minutes - self.elephant_minutes_count) * valves[self.elephant_location].rate
		return self

	def wait(self):
		self.minutes_count += 1
		return self

	def elephant_wait(self):
		self.elephant_minutes_count += 1
		return self

	def move(self, valve_name):
		self.location = valve_name
		self.minutes_count += 1
		return self

	def elephant_move(self, valve_name):
		self.elephant_location = valve_name
		self.elephant_minutes_count += 1
		return self

	# does not increment the minute
	def new_dest_copy(self, new_dest):
		ctx = self.make_copy()
		ctx.dest_valve = new_dest
		return ctx

	# does not increment the minute
	def elephant_new_dest_copy(self, new_dest):
		ctx = self.make_copy()
		ctx.elephant_dest_valve = new_dest
		return ctx

	def is_completed(self):
		global total_minutes
		return (self.minutes_count >= total_minutes and self.elephant_minutes_count >= total_minutes) or len(self.openable_valves_remaining) == 0

def traverse(ctx):
	global best_ctx
	global valves
	global complete_sequences_eliminated
	global last_elimination_timestamp

	if ctx.is_completed():
		if ctx.total_flow > best_ctx.total_flow:
			print("completed sequence has flow {} which is better than previous best of {}".format(ctx.total_flow, best_ctx.total_flow))
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

	#########
	# human #
	#########

	human_forks = []

	# if human is done, do nothing
	if ctx.minutes_count >= 26:
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
				if len(ctx.openable_valves_remaining) == 1 and ctx.is_openable(ctx.elephant_dest_valve):
					ctx.wait()
					human_forks.append(ctx)
				for valve in ctx.openable_valves_remaining:
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
		if human_ctx.elephant_minutes_count >= 26:
			traverse(human_ctx)
			continue

		# if the human opened the last valve, or is going to, we must wait
		if len(human_ctx.openable_valves_remaining) == 0 or (len(human_ctx.openable_valves_remaining) == 1 and human_ctx.is_openable(ctx.dest_valve)):
			traverse(human_ctx.elephant_wait())

		else:

			# if valve has flow rate > 0, and is not opened, we open it here
			if human_ctx.elephant_location == human_ctx.elephant_dest_valve:
				if human_ctx.is_openable(human_ctx.elephant_location):
					traverse(human_ctx.elephant_open())

				# pick another unopened valve (only one with positive flow!) to move to
				else:
					for valve in human_ctx.openable_valves_remaining:
						traverse(human_ctx.elephant_new_dest_copy(valve))

			# continue moving toward destination valve
			else:
				next_valve = next_valve_on_route_between_valves(human_ctx.elephant_location, human_ctx.elephant_dest_valve)
				traverse(human_ctx.elephant_move(next_valve))

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

valves = {}
valve_names_with_positive_flow = set()

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
		valve_names_with_positive_flow.add(valve)

# global context that will be accessed by all
#   instances of recursive traverse() function
best_ctx = Context()

traverse(Context())

print("total flow released: [{}]".format(best_ctx.total_flow))
