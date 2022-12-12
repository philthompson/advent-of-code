# python 3

import sys

class Monkey:
	def __init__(self, start_items, operation_desc, test_divisor, true_dest_monkey, false_dest_monkey):
		self.items = start_items.copy()
		if not operation_desc.startswith("Operation: new = old "):
			print("unexpected operation description: [{}]".format(operation_desc))
			sys.exit(1)
		self.operation_desc = operation_desc
		self.test_divisor = test_divisor
		self.true_dest_monkey = true_dest_monkey
		self.false_dest_monkey = false_dest_monkey
		self.items_inspected = 0

	def do_turn(self, all_monkeys):
		for item in self.items:
			self.items_inspected += 1
			# peform inspection of item, which changes its worry value
			new_item = self.do_operation(item)
			# your relief the item isn't damaged reduces its worry value to 1/3 (rounded down to nearest int)
			new_item = int(new_item / 3)
			# perform test
			if new_item % self.test_divisor == 0:
				all_monkeys[self.true_dest_monkey].catch_item(new_item)
			else:
				all_monkeys[self.false_dest_monkey].catch_item(new_item)
		# each monkey ends its turn with an empty items list, right?
		self.items = []

	def catch_item(self, item_value):
		self.items.append(item_value)

	# parse the "Operation: " description and execute it
	def do_operation(self, old):
		value = old
		parts = self.operation_desc.split(' ')
		if parts[5] != 'old':
			value = int(parts[5])

		if parts[4] == '+':
			return old + value
		elif parts[4] == '*':
			return old * value
		else:
			print("unexpected operation description: [{}]".format(self.operation_desc))
			sys.exit(1)

	def get_items_inspected(self):
		return self.items_inspected


monkeys = {}

monkey_index = -1
start_items = []
operation_desc = ''
test_divisor = -1
true_dest_monkey = -1
false_dest_monkey = -1

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# "Monkey 0:"
	if line.startswith('Monkey'):
		# create the previous monkey, if any
		if monkey_index >= 0:
			print("creating monkey [{}]".format(monkey_index))
			monkeys[monkey_index] = Monkey(start_items, operation_desc, test_divisor, true_dest_monkey, false_dest_monkey)
			start_items = []
			operation_desc = ''
			test_divisor = -1
			true_dest_monkey = -1
			false_dest_monkey = -1
		monkey_index = int(line[7:-1])
		print("now reading monkey [{}] parameters".format(monkey_index))

	# "Starting items: 74, 73, 57, 77, 74"
	elif line.startswith('Starting items:'):
		start_items = [int(i.rstrip(',')) for i in line[16:].split(' ')]

	# "Operation: new = old * 11"
	elif line.startswith('Operation: '):
		operation_desc = line

	# "Test: divisible by 19"
	elif line.startswith('Test: divisible by '):
		test_divisor = int(line[19:])

	# "If true: throw to monkey 6"
	elif line.startswith('If true: '):
		true_dest_monkey = int(line.split(' ')[5])

	# "If false: throw to monkey 7"
	elif line.startswith('If false: '):
		false_dest_monkey = int(line.split(' ')[5])

	else:
		print("unexpected input line: [{}]".format(line))
		sys.exit(1)

# create the previous monkey, if any
if monkey_index >= 0:
	print("creating monkey [{}]".format(monkey_index))
	monkeys[monkey_index] = Monkey(start_items, operation_desc, test_divisor, true_dest_monkey, false_dest_monkey)

for round_num in range(1, 21):
	print("starting round [{}]".format(round_num))
	for monkey_index in monkeys:
		#print("monkey [{}] doing turn".format(monkey_index))
		monkeys[monkey_index].do_turn(monkeys)

monkey_inspections = []

for monkey_index in monkeys:
	print("monkey [{}] inspected [{}] items".format(monkey_index, monkeys[monkey_index].get_items_inspected()))
	monkey_inspections.append(monkeys[monkey_index].get_items_inspected())

monkey_inspections.sort()
print("product of two highest inspection counts: [{}]".format(monkey_inspections[-1] * monkey_inspections[-2]))