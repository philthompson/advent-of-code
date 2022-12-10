# python 3

import sys

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0
tail_positions = set()
tail_positions.add("{},{}".format(tail_x, tail_y))

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	distance = int(line[2:])

	for step in range(0, distance):
		if line[0] == 'R':
			head_x += 1
		elif line[0] == 'L':
			head_x -= 1
		elif line[0] == 'U':
			head_y += 1
		elif line[0] == 'D':
			head_y -= 1
		else:
			print("invalid direction on line [{}]".format(line))
			continue

		if abs(head_x - tail_x) > 1:
			# check y as well, to possibly move diagonally
			if head_y > tail_y:
				tail_y += 1
			elif head_y < tail_y:
				tail_y -= 1
			if head_x > tail_x:
				tail_x += 1
			elif head_x < tail_x:
				tail_x -= 1
		elif abs(head_y - tail_y) > 1:
			# check x as well, to possibly move diagonally
			if head_x > tail_x:
				tail_x += 1
			elif head_x < tail_x:
				tail_x -= 1
			if head_y > tail_y:
				tail_y += 1
			elif head_y < tail_y:
				tail_y -= 1

		tail_positions.add("{},{}".format(tail_x, tail_y))

print(tail_positions)
print("total of {} tail positions".format(len(tail_positions)))