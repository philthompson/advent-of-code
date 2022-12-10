# python 3

import sys

knots_x = []
knots_y = []

tail_positions = set()

for i in range(0, 10):
	knots_x.append(0)
	knots_y.append(0)

tail_positions.add("{},{}".format(knots_x[-1], knots_y[-1]))

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	distance = int(line[2:])

	for step in range(0, distance):
		# first move the "head" knot
		if line[0] == 'R':
			knots_x[0] += 1
		elif line[0] == 'L':
			knots_x[0] -= 1
		elif line[0] == 'U':
			knots_y[0] += 1
		elif line[0] == 'D':
			knots_y[0] -= 1
		else:
			print("invalid direction on line [{}]".format(line))
			continue

		# move each knot down the rope in succession, using
		#   index 1-9 inclusive
		for k in range(1, 10):

			if abs(knots_x[k-1] - knots_x[k]) > 1:
				# check y as well, to possibly move diagonally
				if knots_y[k-1] > knots_y[k]:
					knots_y[k] += 1
				elif knots_y[k-1] < knots_y[k]:
					knots_y[k] -= 1
				if knots_x[k-1] > knots_x[k]:
					knots_x[k] += 1
				elif knots_x[k-1] < knots_x[k]:
					knots_x[k] -= 1
			elif abs(knots_y[k-1] - knots_y[k]) > 1:
				# check x as well, to possibly move diagonally
				if knots_x[k-1] > knots_x[k]:
					knots_x[k] += 1
				elif knots_x[k-1] < knots_x[k]:
					knots_x[k] -= 1
				if knots_y[k-1] > knots_y[k]:
					knots_y[k] += 1
				elif knots_y[k-1] < knots_y[k]:
					knots_y[k] -= 1

		tail_positions.add("{},{}".format(knots_x[-1], knots_y[-1]))

print(tail_positions)
print("total of {} tail positions".format(len(tail_positions)))