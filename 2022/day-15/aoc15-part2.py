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

# enforce that ranges do not overlap (min and max can be equal)
class RemoveableIntRange:
	def __init__(self, min_val, max_val):
		self.ranges = [(min_val, max_val)]

	def remove(self, min_val, max_val):
		new_ranges = []
		for range_atom in self.ranges:
			if range_atom[1] < min_val:
				new_ranges.append(range_atom)
			elif range_atom[0] > max_val:
				new_ranges.append(range_atom)
			elif range_atom[0] < min_val and range_atom[1] > max_val:
				new_ranges.append((range_atom[0], min_val-1))
				new_ranges.append((max_val+1, range_atom[1]))
			elif range_atom[1] == min_val:
				if range_atom[0] == min_val:
					continue
				new_ranges.append((range_atom[0], min_val-1))
			elif range_atom[1] > min_val:
				if range_atom[0] >= min_val:
					continue
				new_ranges.append((range_atom[0], min_val-1))
			elif range_atom[0] == max_val:
				if range_atom[1] == max_val:
					continue
				new_ranges.append((max_val+1, range_atom[1]))
			elif range_atom[0] < max_val:
				if range_atom[1] <= max_val:
					continue
				new_ranges.append((max_val+1, range_atom[1]))
		self.ranges = new_ranges

	def is_empty(self):
		return len(self.ranges) == 0

	def to_string(self):
		range_strings = []
		for range_atom in self.ranges:
			range_strings.append("[{}-{}]".format(range_atom[0], range_atom[1]))
		return ','.join(range_strings)

	def get_one_value(self):
		for range_atom in self.ranges:
			return range_atom[0]

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

for y in range(0, 4000000 + 1):
	#print("doing y row {}".format(y))

	# first, eliminate sensors for each entire row of x-positions
	#   by using the x-position of the sensor -- if the row is always
	#   farther from the sensor than its beacon, we can ignore that
	#   sensor for this row
	row_near_sensors = []
	for sensor in sensors:
		if sensor.get_distance(sensor.x, y) <= sensor.get_beacon_distance():
			row_near_sensors.append(sensor)

	if y % 100000 == 0:
		print("using {} of {} sensors for row {}".format(len(row_near_sensors), len(sensors), y))

	# then, use binary search to find edges for each sensor along
	#   each row?
	# it might work better to use the fact that the eliminated
	#   area is always a diamond shape, centered the x- and y-
	#   positions of the sensor

	possible_x_values = RemoveableIntRange(0, 4000000)

	for sensor in row_near_sensors:
		# when we move 1 y unit up or down from the sensor, the x
		#   elimination boundary also moves 1 unit
		sensor_elim_min_x = sensor.x - sensor.get_beacon_distance() + abs(sensor.y - y)
		sensor_elim_max_x = sensor.x + sensor.get_beacon_distance() - abs(sensor.y - y)

		possible_x_values.remove(sensor_elim_min_x, sensor_elim_max_x)

		if possible_x_values.is_empty():
			break

	if not possible_x_values.is_empty():
		print("possible missing beacon locations:")
		print(possible_x_values.to_string())
		possible_x = possible_x_values.get_one_value()
		print("possible missing beacon location: ({},{})".format(possible_x, y))
		print("tuning frequency would be [{}]".format((possible_x * 4000000) + y))
