# python 3

import sys
import time
from collections import namedtuple

MonkeyMathOperation = namedtuple('MonkeyMathOperation', ['name', 'left_name', 'right_name', 'operator'])

class MonkeyNode:
	def __init__(self, is_done, value, left, right, operator):
		self.is_done = is_done
		self.value = value
		self.left = left
		self.right = right
		self.operator = operator
		self.parents = []
		if self.left != None:
			self.left.parents.append(self)
			self.right.parents.append(self)

	def compute(self):
		global root_node
		global humn_node
		#global is_root_solved

		if not self.left.is_done:
			self.left.compute()

		if not self.right.is_done:
			self.right.compute()

		if self == root_node:
			if self.left.value == self.right.value:
				print("humn value is [{}]".format(humn_node.value))
				sys.exit()
			# stop this brute force guess sequence
			#is_root_solved = True
			return

		if self.operator == "+":
			self.value = self.left.value + self.right.value
		elif self.operator == "-":
			self.value = self.left.value - self.right.value
		elif self.operator == "*":
			self.value = self.left.value * self.right.value
		else:
			self.value = self.left.value / self.right.value

		self.is_done = True

	# change this node's value, and all values that depend on this node
	def reset(self):
		if self.left != None and self.right != None:
			self.compute()
		for parent in self.parents:
			parent.reset()


tree_nodes_by_name = {}
unplaced_by_name = {}

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# monkeys have a value:
	# "dbpl: 5"
	# or an operation:
	# "root: pppw + sjmn"

	colon_idx = line.find(':')

	name = line[0:colon_idx]

	line_value_fields = line[colon_idx+2:].split(' ')

	if len(line_value_fields) == 1:
		tree_nodes_by_name[name] = MonkeyNode(is_done=True, value=int(line_value_fields[0]), left=None, right=None, operator=None)
	elif len(line_value_fields) == 3:
		unplaced_by_name[name] = MonkeyMathOperation(name, line_value_fields[0], line_value_fields[2], line_value_fields[1])
	else:
		print("unexpected line format:")
		print(line)
		print('which yeilded the fields [{}]'.format(']['.join(line_value_fields)))
		sys.exit(1)

root_node = None

# build the tree
while len(unplaced_by_name) > 0:
	newly_placed_names = []
	for name, operation in unplaced_by_name.items():
		if operation.left_name not in tree_nodes_by_name or operation.right_name not in tree_nodes_by_name:
			continue

		tree_nodes_by_name[name] = MonkeyNode(is_done=False, value=None, left=tree_nodes_by_name[operation.left_name], right=tree_nodes_by_name[operation.right_name], operator=operation.operator)

		newly_placed_names.append(name)
	for name in newly_placed_names:
		del unplaced_by_name[name]

root_node = tree_nodes_by_name['root']
humn_node = tree_nodes_by_name['humn']

# i assume we need to initially compute everything, before resetting
#   the humn value
root_node.compute()

# use a set to count number of unique values seen
root_left_values = set()
root_right_values = set()
is_binary_searchable = True

for guess in [1, 5, 10, 50, 100, 500, 100000, 500000, 1000000, 5000000]:
	humn_node.value = guess
	humn_node.reset()
	root_node.compute()
	if not root_node.left.is_done or not root_node.right.is_done:
		print("cannot compute the root value for humn value [{}]".format(guess))
		sys.exit(1)
	root_left_values.add(root_node.left.value)
	root_right_values.add(root_node.right.value)

# see whether right or left value changes
if len(root_right_values) > 1 and len(root_left_values) > 1:
	is_binary_searchable = False

absolute_max_guess = 10000000000000000
guess_min = 1
guess_max = absolute_max_guess

# if both values change, do brute force algorithm below
# if only one values changes, perform binary search
if is_binary_searchable:
	# start with guess of 1.  note right and left values, which is bigger
	# double the guess until the other one is bigger?
	guess = 1

	humn_node.value = guess
	humn_node.reset()
	root_node.compute()

	left_initially_bigger = root_node.left.value > root_node.right.value
	print("after guessing [1], left_initially_bigger is [{}]".format(left_initially_bigger))

	# find binary search bounds
	while (root_node.left.value > root_node.right.value) == left_initially_bigger:
		guess_min = guess
		guess *= 2
		guess_max = guess
		humn_node.value = guess
		humn_node.reset()
		root_node.compute()
		print("after guessing [{}], left bigger is [{}]".format(guess, root_node.left.value > root_node.right.value))
		if guess >= absolute_max_guess:
			break

	print("binary searching from {} to {}".format(guess_min, guess_max))

	# binary search here
	while abs(guess_max - guess_min) > 100:
		guess = int((guess_max - guess_min) / 2) + guess_min

		humn_node.value = guess
		humn_node.reset()
		root_node.compute()

		if (root_node.left.value > root_node.right.value) == left_initially_bigger:
			guess_min = guess
		else:
			guess_max = guess

else:
	print("not binary searchable?")

print("guessing all values from {} to {}".format(guess_min, guess_max))

last_speed_timestamp = -1
brute_guess = guess_min

while brute_guess < guess_max:

	ts_now = time.time()
	if last_speed_timestamp > 0:
		ts_diff = ts_now - last_speed_timestamp
		print("starting guess with humn value of {:,} at {:,} guesses/sec".format(brute_guess, int(1000000 / ts_diff)))
	last_speed_timestamp = ts_now

	for i in range(0, 1000000):
		#is_root_solved = False

		humn_node.value = brute_guess
		# this apparently eventually re-computes the root
		#   node, so we don't need to make a separate call
		#   for that
		humn_node.reset()

		brute_guess += 1

