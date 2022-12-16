# python 3

import sys
import random

class Sensor:
	def __init__(self, x, y, beacon_x, beacon_y):
		self.x = x
		self.y = y
		self.beacon_x = beacon_x
		self.beacon_y = beacon_y

	def get_coords(self):
		return [(self.x, self.y),(self.beacon_x, self.beacon_y)]

	def get_distance(self, x, y):
		return abs(self.x - x) + abs(self.y - y)

	def get_beacon_distance(self):
		return self.get_distance(self.beacon_x, self.beacon_y)

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

# using [y][x] to make it easier to print in the
#   correct orientation
arena = []

# create entire empty arena, as 2D list
for y in range(min_y, max_y + 1):
	at_y = []
	for x in range(min_x, max_x + 1):
		at_y.append('.')
	arena.append(at_y)

# populate coordinates of all sensors and beacons, and
#   use each sensor-beacon pair to mark all "empty"
#   coordinates where unknown beacons cannot be located
for sensor in sensors:
	arena[sensor.y - min_y][sensor.x - min_x] = 'S'
	arena[sensor.beacon_y - min_y][sensor.beacon_x - min_x] = 'B'

	beacon_dist = sensor.get_beacon_distance()

	for x in range(sensor.x - beacon_dist, sensor.x + beacon_dist + 1):
		if x < min_x or x > max_x:
			continue
		for y in range(sensor.y - beacon_dist, sensor.y + beacon_dist + 1):
			if y < min_y or y > max_y:
				continue
			if sensor.is_coord_occupied(x, y):
				continue
			if sensor.get_distance(x, y) > beacon_dist:
				continue
			# this coordinate is not occuped by a sensor or beacon, and
			#   is at, or closer than, the sensor beacon's distance
			#   from the sensor
			# therefore, it cannot be occpied by an unknown sensor
			arena[y - min_y][x - min_x] = '#'

for y in arena:
	print(''.join(y))


y_row_in_question = 10
y_row_in_question = 2000000

row_empty_coords_count = 0
for x in arena[y_row_in_question - min_y]:
	if x == '#':
		row_empty_coords_count += 1

print("row {} (translated to y={}) has [{}] empty coords".format(y_row_in_question, y_row_in_question - min_y, row_empty_coords_count))