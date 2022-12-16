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

#y_row_in_question = 10
y_row_in_question = 2000000


max_sensor_beacon_distance = 0

for sensor in sensors:
	dist = sensor.get_beacon_distance()
	if dist > max_sensor_beacon_distance:
		max_sensor_beacon_distance = dist

print("max sensor beacon distance: [{}]".format(max_sensor_beacon_distance))

row_empty_coords_count = 0

print("x range: {} - {} (inclusive)".format(min_x, max_x))

# more efficient: loop over all x locations along the
#   y row in question
# at every point, loop over all sensors to see if the
#   point is at or closer than any sensor's beacon
# expand bounds by twice the maximum distance any sensor is from
#   its closest beacon
for x in range(min_x - (2 * max_sensor_beacon_distance), max_x + 1 + (2 * max_sensor_beacon_distance)):
	if x % 100000 == 0:
		print("checking x coord [{}]".format(x))
	for sensor in sensors:
		if sensor.is_coord_occupied(x, y_row_in_question):
			continue
		if sensor.get_distance(x, y_row_in_question) <= sensor.get_beacon_distance():
			row_empty_coords_count += 1
			break

print("row {} has [{}] empty coords".format(y_row_in_question, row_empty_coords_count))
