# python 3

import sys
import time

floor_pos = []

# boolean values
# in [y][x] order
stopped_rock_coords = []

highest_stopped_rock_pos = -1

x_level = []
for x in range(0, 7):
	x_level.append(False)

# start with 10 rows
for y in range(0, 10):
	stopped_rock_coords.append(x_level.copy())

for i in range(0, 7):
	floor_pos.append(0)

class Rock:
	# left pos is x position (from 0-6) of the pos[][] list
	# bottom pos is y position o the 
	# bottom_rel_coords is list of (x,y) positions relative to
	#   (left_pos,bottom_pos)
	# top_rel_coords is list of (x,y) positions relative to
	#   (left_pos,bottom_pos)
	#
	# maybe just use rel_coords
	# rel_coords is list of (x,y) positions relative to
	#   (left_pos,bottom_pos)
	def __init__(self, left_pos, bottom_pos, rel_coords):
		self.left_pos = left_pos
		self.bottom_pos = bottom_pos
		self.is_stopped = False
		self.rel_coords = rel_coords.copy()

	# check to see if anything hits the side wall or another Rock
	def move_left(self):
		global stopped_rock_coords
		for coord in self.rel_coords:
			y = coord[1] + self.bottom_pos
			x = coord[0] + self.left_pos - 1
			if x < 0 or stopped_rock_coords[y][x]:
				return
		self.left_pos -= 1

	# check to see if anything hits the side wall or another Rock
	def move_right(self):
		global stopped_rock_coords
		for coord in self.rel_coords:
			y = coord[1] + self.bottom_pos
			x = coord[0] + self.left_pos + 1
			if x > 6 or stopped_rock_coords[y][x]:
				return
		self.left_pos += 1

	# check to see if anything hits the floor or another Rock
	def move_down(self):
		global stopped_rock_coords
		for coord in self.rel_coords:
			y = coord[1] + self.bottom_pos - 1
			x = coord[0] + self.left_pos
			if y < 0 or stopped_rock_coords[y][x]:
				self.is_stopped = True
				return
		self.bottom_pos -= 1

	def become_one_with_the_pile(self):
		global stopped_rock_coords
		global highest_stopped_rock_pos
		for coord in self.rel_coords:
			x = coord[0] + self.left_pos
			y = coord[1] + self.bottom_pos
			stopped_rock_coords[y][x] = True
			if y > highest_stopped_rock_pos:
				highest_stopped_rock_pos = y

	def get_y_min_max_tuple(self):
		y_min = self.rel_coords[0][1] + self.bottom_pos
		y_max = 0
		for coord in self.rel_coords:
			y = coord[1] + self.bottom_pos
			y_min = min(y_min, y)
			y_max = max(y_max, y)
		return (y_min, y_max)

#|  shape:
#|
#|
#|   ####
#|
#|
class Horiz(Rock):
	def __init__(self, left_pos, bottom_pos):
		super().__init__(left_pos, bottom_pos, [(0,0),(1,0),(2,0),(3,0)])

#|  shape:
#|
#|    #
#|   ###
#|    #
#|
class Plus(Rock):
	def __init__(self, left_pos, bottom_pos):
		super().__init__(left_pos, bottom_pos, [(0,1),(1,0),(1,1),(1,2),(2,1)])

#|  shape:
#|
#|     #
#|     #
#|   ###
#|
class Ell(Rock):
	def __init__(self, left_pos, bottom_pos):
		super().__init__(left_pos, bottom_pos, [(0,0),(1,0),(2,0),(2,1),(2,2)])

#|  shape:
#|
#|    #
#|    #
#|    #
#|    #
#|
class Vert(Rock):
	def __init__(self, left_pos, bottom_pos):
		super().__init__(left_pos, bottom_pos, [(0,0),(0,1),(0,2),(0,3)])

#|  shape:
#|
#|   ##
#|   ##
#|      
class Box(Rock):
	def __init__(self, left_pos, bottom_pos):
		super().__init__(left_pos, bottom_pos, [(0,0),(1,0),(0,1),(1,1)])

jet_pattern = '<>'

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# ">>><<><>><<<>><>>..."
	jet_pattern = line

jet_idx = -1

rock = Rock(0, 0, [])

i = 0

last_rock_timestamp = -1

while i < 2022:
	if i % 100_000 == 0:
		if i % 10_000_000 == 0:
			print("dropping rock {} from position {}".format(i, highest_stopped_rock_pos + 4))
		ts_now = time.time()
		if last_rock_timestamp > 0:
			ts_diff = ts_now - last_rock_timestamp
			print("rocks per second: [{}]".format(100_000.0 / ts_diff), end='\r')
		last_rock_timestamp = ts_now

	shape_idx = i % 5
	if shape_idx == 0:
		rock = Horiz(2, highest_stopped_rock_pos + 4)
	if shape_idx == 1:
		rock = Plus(2, highest_stopped_rock_pos + 4)
	if shape_idx == 2:
		rock = Ell(2, highest_stopped_rock_pos + 4)
	if shape_idx == 3:
		rock = Vert(2, highest_stopped_rock_pos + 4)
	if shape_idx == 4:
		rock = Box(2, highest_stopped_rock_pos + 4)
	i += 1

	while not rock.is_stopped:
		jet_idx += 1
		if jet_idx >= len(jet_pattern):
			jet_idx = 0
		if jet_pattern[jet_idx] == '<':
			rock.move_left()
		else:
			rock.move_right()
		rock.move_down()

	rock.become_one_with_the_pile()

	#for y in range(len(stopped_rock_coords)-1, -1, -1):
	#	row = ''.join([' ' if x == False else '#' for x in stopped_rock_coords[y]])
	#	print('|{}|'.format(row))
	#print("+-------+")
	#print(".")
	#print("..")
	#print("...")

	while highest_stopped_rock_pos + 10 > len(stopped_rock_coords):
		stopped_rock_coords.append(x_level.copy())


print("highest_stopped_rock_pos: [{}]".format(highest_stopped_rock_pos + 1))
