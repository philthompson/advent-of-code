# python 3

import sys
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

	blueprints.append(Blueprint(id=int(split[1][0:-1]), ore_robot_ore_cost=int(split[6]), clay_robot_ore_cost=int(split[12]), obsidian_robot_ore_cost=int(split[18]), obsidian_robot_clay_cost=int(split[21]), geode_robot_ore_cost=int(split[27]), geode_robot_obsidian_cost=int(split[30])))

	print("added blueprint for line:")
	print(line)
	print("tuple:")
	print(blueprints[-1]._asdict())
	print("")
	print("")


def algo(state, geode_inventory, action):
	global visited_states
	global highest_geode_count
	global active_blueprint

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

	new_wait_state = State(i_or=inv_ore, i_cl=inv_clay, i_ob=inv_obsidian, r_or=new_r_or, r_cl=new_r_cl, r_ob=new_r_ob, r_ge=new_r_ge, mins_remaining=new_mins_remaining)

	if new_wait_state in visited_states:
		if inv_geode <= visited_states[new_wait_state]:
			return
	
	visited_states[new_wait_state] = inv_geode

	# branch recursion here if we can build an ore robot
	if inv_ore >= active_blueprint.ore_robot_ore_cost:
		algo(new_wait_state, inv_geode, 'build ore robot')

	# branch recursion here if we can build a clay robot
	if inv_ore >= active_blueprint.clay_robot_ore_cost:
		algo(new_wait_state, inv_geode, 'build clay robot')

	# branch recursion here if we can build an obsidian robot
	if inv_ore >= active_blueprint.obsidian_robot_ore_cost and inv_clay >= active_blueprint.obsidian_robot_clay_cost:
		algo(new_wait_state, inv_geode, 'build obsidian robot')

	# branch recursion here if we can build a geode robot
	if inv_ore >= active_blueprint.geode_robot_ore_cost and inv_obsidian >= active_blueprint.geode_robot_obsidian_cost:
		algo(new_wait_state, inv_geode, 'build geode robot')

	# branch recursion here to wait a minute, without building a robot
	algo(new_wait_state, inv_geode, 'wait')


active_blueprint = blueprints[0]
visited_states = {}
highest_geode_count = 0

total_quality = 0

for blueprint in blueprints:
	active_blueprint = blueprint
	visited_states.clear()
	highest_geode_count = 0

	# kick off with 1 ore robot and 24 minutes remaining
	algo(State(i_or=0, i_cl=0, i_ob=0, r_or=1, r_cl=0, r_ob=0, r_ge=0, mins_remaining=24), geode_inventory=0, action='wait')

	print("for blueprint {}, the most geodes it can make is {}".format(blueprint.id, highest_geode_count))
	total_quality += blueprint.id * highest_geode_count

print("sum of quality levels: {}".format(total_quality))
