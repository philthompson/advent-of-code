# python 3

import sys
import random

class Sensor:
	def __init__(self, x, y, beacon_x, beacon_y):
		self.x = x
		self.y = y
		self.beacon_x = beacon_x
		self.beacon_y = beacon_y
		self.beacon_distance = self.get_distance(self.beacon_x, self.beacon_y)

	def get_coords(self):
		return [(self.x, self.y),(self.beacon_x, self.beacon_y)]

	def get_distance(self, x, y):
		return abs(self.x - x) + abs(self.y - y)

	def get_beacon_distance(self):
		return self.beacon_distance

	def is_coord_occupied(self, x, y):
		return ((self.x == x and self.y == y) or (self.beacon_x == x and self.beacon_y == y))


# bounds
min_x = -1
max_x = -1
min_y = 0
max_y = -1

sensors = []

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
	fields = line.split(' ')
	sensors.append(Sensor(int(fields[2][2:-1]), int(fields[3][2:-1]), int(fields[8][2:-1]), int(fields[9][2:])))

# find bounds
for sensor in sensors:
	for coord in sensor.get_coords():
		if min_x == -1 or coord[0] < min_x:
			min_x = coord[0]

		if max_x == -1 or coord[0] > max_x:
			max_x = coord[0]

		if min_y == -1 or coord[1] < min_y:
			min_y = coord[1]

		if max_y == -1 or coord[1] > max_y:
			max_y = coord[1]

# more efficient: loop over all x locations along each
#   y row in question (y is restricted to 0-4000000
#   according to the puzzle)
# at every point, loop over all sensors to see if the
#   point is at or closer than any sensor's beacon
#   (x is restricted to 0-4000000 according to the puzzle)
#for y in range(0, 20 + 1):
for y in range(4000000 + 1, 0, -1):
	print("doing y row {}".format(y))
	#if y % 10 == 0:
	#	print("doing y row {}".format(y))
	#for x in range(0, 20 + 1):
	for x in range(0, 4000000 + 1):
		is_coord_eliminated = False
		for sensor in sensors:
			#if sensor.is_coord_occupied(x, y):
			#	is_coord_eliminated = True
			#	break
			if sensor.get_distance(x, y) <= sensor.get_beacon_distance():
				is_coord_eliminated = True
				break
		if not is_coord_eliminated:
			# at this point, the coordinate is not in any sensor's beacon
			#   range
			print("possible missing beacon location: ({},{})".format(x, y))
			print("tuning frequency would be [{}]".format((x * 4000000) + y))
