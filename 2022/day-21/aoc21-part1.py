# python 3

import sys

class MonkeyMathOpeation:
	def __init__(self, name, left_name, right_name, operator):
		self.name = name
		self.left_name = left_name
		self.right_name = right_name
		self.operator = operator

	def attempt_solve(self):
		global solved_values_by_name
		global unsolved_by_name

		if self.left_name in unsolved_by_name or self.right_name in unsolved_by_name:
			return False

		if self.operator == "+":
			solved_values_by_name[self.name] = solved_values_by_name[self.left_name] + solved_values_by_name[self.right_name]
		elif self.operator == "-":
			solved_values_by_name[self.name] = solved_values_by_name[self.left_name] - solved_values_by_name[self.right_name]
		elif self.operator == "*":
			solved_values_by_name[self.name] = solved_values_by_name[self.left_name] * solved_values_by_name[self.right_name]
		else:
			solved_values_by_name[self.name] = solved_values_by_name[self.left_name] / solved_values_by_name[self.right_name]

		return True

solved_values_by_name = {}
unsolved_by_name = {}

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
		solved_values_by_name[name] = int(line_value_fields[0])
	elif len(line_value_fields) == 3:
		unsolved_by_name[name] = MonkeyMathOpeation(name, line_value_fields[0], line_value_fields[2], line_value_fields[1])
	else:
		print("unexpected line format:")
		print(line)
		print('which yeilded the fields [{}]'.format(']['.join(line_value_fields)))
		sys.exit(1)

print("initally have [{}] value monkeys and [{}] operation monkeys".format(len(solved_values_by_name), len(unsolved_by_name)))

round = 1
while 'root' not in solved_values_by_name:
	newly_solved_names = []
	for name in unsolved_by_name:
		if unsolved_by_name[name].attempt_solve():
			newly_solved_names.append(name)
	print("after round {}, we have solved [{}] more monkeys".format(round, len(newly_solved_names)))
	for name in newly_solved_names:
		del unsolved_by_name[name]
	round += 1

print("root value is [{}]".format(solved_values_by_name['root']))


