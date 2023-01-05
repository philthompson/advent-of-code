# python 3

import sys
import time
from collections import namedtuple

Blueprint = namedtuple('Blueprint', ['id', 'ore_robot_ore_cost', 'clay_robot_ore_cost', 'obsidian_robot_ore_cost', 'obsidian_robot_clay_cost', 'geode_robot_ore_cost', 'geode_robot_obsidian_cost'])

State = namedtuple('State', ['i_or', 'i_cl', 'i_ob', 'r_or', 'r_cl', 'r_ob', 'r_ge', 'mins_remaining'])

blueprints = []

# the blueprints vary only in the quantities, not in the type of materials required for the different robots:
# Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 14 clay. Each geode robot costs 3 ore and 16 obsidian.
for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	split = line.split(' ')

	b = Blueprint(id=int(split[1][0:-1]), ore_robot_ore_cost=int(split[6]), clay_robot_ore_cost=int(split[12]), obsidian_robot_ore_cost=int(split[18]), obsidian_robot_clay_cost=int(split[21]), geode_robot_ore_cost=int(split[27]), geode_robot_obsidian_cost=int(split[30]))

	if b.id > 3:
		continue

	blueprints.append(b)

	print("added blueprint for line:")
	print(line)
	print("tuple:")
	print(blueprints[-1]._asdict())
	print("")
	print("")


def algo(state, geode_inventory, action):
	global states_to_try
	global visited_states
	global highest_geode_count
	global active_blueprint
	global abandoned_sequences

	new_mins_remaining = state.mins_remaining - 1

	inv_ore      = state.i_or + state.r_or
	inv_clay     = state.i_cl + state.r_cl
	inv_obsidian = state.i_ob + state.r_ob
	inv_geode = geode_inventory + state.r_ge

	new_r_or = state.r_or
	new_r_cl = state.r_cl
	new_r_ob = state.r_ob
	new_r_ge = state.r_ge

	if action == 'build ore robot':
		inv_ore -= active_blueprint.ore_robot_ore_cost
		new_r_or += 1

	elif action == 'build clay robot':
		inv_ore -= active_blueprint.clay_robot_ore_cost
		new_r_cl += 1

	elif action == 'build obsidian robot':
		inv_ore -= active_blueprint.obsidian_robot_ore_cost
		inv_clay -= active_blueprint.obsidian_robot_clay_cost
		new_r_ob += 1

	elif action == 'build geode robot':
		inv_ore -= active_blueprint.geode_robot_ore_cost
		inv_obsidian -= active_blueprint.geode_robot_obsidian_cost
		new_r_ge += 1

	if inv_geode > highest_geode_count:
		highest_geode_count = inv_geode

	if new_mins_remaining <= 0:
		return

	# we can stop if it's not possible for this sequence to ever
	#   surpass some other better sequence
	# (for now, assume we can build a new geode robot every turn)
	#if new_mins_remaining < 7:
	#	theoretical_max_geodes = inv_geode
	#	for i in range(0, new_mins_remaining):
	#		theoretical_max_geodes += (new_r_ge + i)
	#	if theoretical_max_geodes < highest_geode_count:
	#		abandoned_sequences += 1
	#		return

	# a better theoretical maximum would be to build a new geode
	#   robot ASAP, once materials are available? (this should hold
	#   when few enough minutes remain, though this is a
	#   guess-and-check thing)
	# if the current script instance has trouble, try increasing
	#   this to "< 8"
	if new_mins_remaining < 7:
		theoretical_max_geodes = inv_geode
		sim_inv_or = inv_ore
		#sim_inv_cl = inv_clay
		sim_inv_ob = inv_obsidian
		sim_r_ge = new_r_ge
		for i in range(new_mins_remaining, -1, -1):
			sim_inv_or += new_r_or
			#sim_inv_cl += new_r_cl
			sim_inv_ob += new_r_ob
			theoretical_max_geodes += sim_r_ge
			if sim_inv_or >= active_blueprint.geode_robot_ore_cost and sim_inv_ob >= active_blueprint.geode_robot_obsidian_cost:
				sim_inv_or -= active_blueprint.geode_robot_ore_cost
				sim_inv_ob -= active_blueprint.geode_robot_obsidian_cost
				sim_r_ge += 1
		if theoretical_max_geodes < highest_geode_count:
			abandoned_sequences += 1
			return



	new_wait_state = State(i_or=inv_ore, i_cl=inv_clay, i_ob=inv_obsidian, r_or=new_r_or, r_cl=new_r_cl, r_ob=new_r_ob, r_ge=new_r_ge, mins_remaining=new_mins_remaining)

	if new_wait_state in visited_states:
		if inv_geode <= visited_states[new_wait_state]:
			return
	
	visited_states[new_wait_state] = inv_geode

	# branch recursion here if we can build an ore robot
	if inv_ore >= active_blueprint.ore_robot_ore_cost:
		states_to_try[new_mins_remaining].append((new_wait_state, inv_geode, 'build ore robot'))

	# branch recursion here if we can build a clay robot
	if inv_ore >= active_blueprint.clay_robot_ore_cost:
		states_to_try[new_mins_remaining].append((new_wait_state, inv_geode, 'build clay robot'))

	# branch recursion here if we can build an obsidian robot
	if inv_ore >= active_blueprint.obsidian_robot_ore_cost and inv_clay >= active_blueprint.obsidian_robot_clay_cost:
		states_to_try[new_mins_remaining].append((new_wait_state, inv_geode, 'build obsidian robot'))

	# branch recursion here if we can build a geode robot
	if inv_ore >= active_blueprint.geode_robot_ore_cost and inv_obsidian >= active_blueprint.geode_robot_obsidian_cost:
		states_to_try[new_mins_remaining].append((new_wait_state, inv_geode, 'build geode robot'))

	# branch recursion here to wait a minute, without building a robot
	states_to_try[new_mins_remaining].append((new_wait_state, inv_geode, 'wait'))


active_blueprint = blueprints[0]
visited_states = {}
highest_geode_count = 0
abandoned_sequences = 0

total_quality = 1

# states to try (resume traversal) keyed by the
#   number of minutes remaining
states_to_try = {}

for blueprint in blueprints:
	active_blueprint = blueprint
	visited_states.clear()
	highest_geode_count = 0
	abandoned_sequences = 0
	for i in range(0, 33):
		states_to_try[i] = []

	# kick off with 1 ore robot and 32 minutes remaining
	states_to_try[32].append((State(i_or=0, i_cl=0, i_ob=0, r_or=1, r_cl=0, r_ob=0, r_ge=0, mins_remaining=32), 0, 'wait'))

	state_cleanup_counter = 0
	mins_remaining_cursor = 32

	last_speed_timestamp = -1

	while len(states_to_try[0]) > 0 or len(states_to_try[1]) > 0 or len(states_to_try[2]) > 0 or len(states_to_try[3]) > 0 or len(states_to_try[4]) > 0 or len(states_to_try[5]) > 0 or len(states_to_try[6]) > 0 or len(states_to_try[7]) > 0 or len(states_to_try[8]) > 0 or len(states_to_try[9]) > 0 or len(states_to_try[10]) > 0 or len(states_to_try[11]) > 0 or len(states_to_try[12]) > 0 or len(states_to_try[13]) > 0 or len(states_to_try[14]) > 0 or len(states_to_try[15]) > 0 or len(states_to_try[16]) > 0 or len(states_to_try[17]) > 0 or len(states_to_try[18]) > 0 or len(states_to_try[19]) > 0 or len(states_to_try[20]) > 0 or len(states_to_try[21]) > 0 or len(states_to_try[22]) > 0 or len(states_to_try[23]) > 0 or len(states_to_try[24]) > 0 or len(states_to_try[25]) > 0 or len(states_to_try[26]) > 0 or len(states_to_try[27]) > 0 or len(states_to_try[28]) > 0 or len(states_to_try[29]) > 0 or len(states_to_try[30]) > 0 or len(states_to_try[31]) > 0 or len(states_to_try[32]) > 0:
		state_cleanup_counter += 1
		if state_cleanup_counter >= 100000:
			ts_now = time.time()
			if last_speed_timestamp > 0:
				ts_diff = ts_now - last_speed_timestamp
				sys.stdout.write("visited_states:[{:,}], states_to_try:[{:,}], states/sec:[{:,}], abandoned_seq:[{:,}]        \r".format(len(visited_states), sum([len(states_to_try[i]) for i in states_to_try]), int(100000 / ts_diff), abandoned_sequences))
				sys.stdout.flush()
			last_speed_timestamp = ts_now
			state_cleanup_counter = 0
			# find max "minutes remaining" from all outstanding states to try,
			#   and get rid of previously saved states with more minutes than
			#   that
			max_mins_remaining = -1
			for i in range(0, 33):
				if len(states_to_try[i]) > 0 and i > max_mins_remaining:
					max_mins_remaining = i

			states_to_delete = []
			for old_state in visited_states:
				if old_state.mins_remaining > max_mins_remaining:
					states_to_delete.append(old_state)
			if len(states_to_delete) > 0:
				print("deleting [{:,}] old states that have more than [{}] minutes remaining                  ".format(len(states_to_delete), max_mins_remaining))
				for to_del in states_to_delete:
					del visited_states[to_del]

		breadth_first_search_found = False
		entry_point = -1

		while not breadth_first_search_found and mins_remaining_cursor >= 0:
			if len(states_to_try[mins_remaining_cursor]) > 0:
				breadth_first_search_found = True
				entry_point = states_to_try[mins_remaining_cursor].pop()
				break
			if not breadth_first_search_found:
				print("no states remaining to traverse with {} minutes remaining".format(mins_remaining_cursor))
				mins_remaining_cursor -= 1

		algo(entry_point[0], geode_inventory=entry_point[1], action=entry_point[2])

	print("for blueprint {}, the most geodes it can make is {}".format(blueprint.id, highest_geode_count))
	total_quality *= highest_geode_count

print("sum of quality levels: {}".format(total_quality))