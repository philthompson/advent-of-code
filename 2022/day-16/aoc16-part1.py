# python 3

import sys
import random

recursion_save_points = []

class Valve:
	def __init__(self, name, rate, names_connected_to):
		self.name = name
		self.rate = rate
		self.names_connected_to = names_connected_to

class Context:
	def __init__(self):
		self.sequence = []
		self.open_valves = []
		self.total_flow_rate = 0
		self.total_flow = 0
		self.location = 'AA'
		self.dest_valve = 'AA'

	def make_copy(self):
		dupe = Context()
		dupe.sequence = self.sequence.copy()
		dupe.open_valves = self.open_valves.copy()
		dupe.total_flow_rate = self.total_flow_rate
		dupe.total_flow = self.total_flow
		dupe.location = self.location
		dupe.dest_valve = self.dest_valve
		return dupe

	def is_openable(self):
		global valves
		return (not self.location in self.open_valves) and valves[self.location].rate > 0

	def open(self):
		global valves
		self.total_flow += self.total_flow_rate
		self.sequence.append('o')
		self.open_valves.append(self.location)
		self.total_flow_rate += valves[self.location].rate
		return self

	def wait(self):
		self.total_flow += self.total_flow_rate
		self.sequence.append('w')
		return self

	def move(self, valve_name):
		self.total_flow += self.total_flow_rate
		self.sequence.append(valve_name)
		self.location = valve_name
		return self

	# not actually an entry in the sequence
	def new_dest_copy(self, new_dest):
		ctx = self.make_copy()
		ctx.dest_valve = new_dest
		return ctx

def traverse(ctx, recursion_depth):
	global best_ctx
	global recursion_save_points
	global valves
	global openable_valves
	global complete_sequences_eliminated

	if recursion_depth > 12:
		recursion_save_points.append(ctx)
		return

	if len(ctx.sequence) >= 30:
		if ctx.total_flow > best_ctx.total_flow:
			print("completed sequence has flow {} which is better than previous best of {}".format(ctx.total_flow, best_ctx.total_flow))
			best_ctx = ctx
		else:
			complete_sequences_eliminated += 1
			if complete_sequences_eliminated % 10000 == 0:
				print("complete_sequences_eliminated: [{}]".format(complete_sequences_eliminated))
		return

	# we must wait here
	if len(ctx.open_valves) == openable_valves:
		traverse(ctx.wait(), recursion_depth+1)

	else:

		# if valve has flow rate > 0, and is not opened, we open it here
		if ctx.location == ctx.dest_valve:
			if ctx.is_openable():
				traverse(ctx.open(), recursion_depth+1)

			# pick another unopened valve (only one with positive flow!) to move to
			else:
				for valve in valves:
					if valves[valve].rate > 0 and not valve in ctx.open_valves:
						traverse(ctx.new_dest_copy(valve), recursion_depth+1)

		# continue moving toward destination valve
		else:
			next_valve = next_valve_on_route_between_valves(ctx.location, ctx.dest_valve)
			traverse(ctx.move(next_valve), recursion_depth+1)

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

# global context that will be accessed by all
#   instances of recursive traverse() function
best_ctx = Context()

traverse(Context(), 0)

print("recursion_save_points: {}".format(len(recursion_save_points)))

while len(recursion_save_points) > 0:
	if len(recursion_save_points) % 1000 == 0:
		print("have {} recursion_save_points".format(len(recursion_save_points)))
		print("    best total flow: {}".format(best_ctx.total_flow))

	traverse(recursion_save_points.pop(), 0)


location = 'AA'
during_minute = 0
open_valves = []
flow_rate = 0
for step in best_ctx.sequence:
	during_minute += 1
	print("== Minute {} == ({})".format(during_minute, step))

	if len(open_valves) == 0:
		print("No valves are open.")
	else:
		print("Valves {} are open, releasing {} pressure.".format(open_valves, flow_rate))

	if step == 'w':
		pass
	elif step == 'o':
		print("You open valve {}.".format(location))
		open_valves.append(location)
		flow_rate += valves[location].rate
	else:
		print("You move to valve {}.".format(step))
		location = step

	print('')

print("total flow released: [{}]".format(best_ctx.total_flow))
