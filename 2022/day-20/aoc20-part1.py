# python 3

import sys

class NumVal:
	def __init__(self, value, prev_neighbor, next_neighbor):
		self.value = value
		self.prev_neighbor = prev_neighbor
		self.next_neighbor = next_neighbor

	def insert_after(self, target):
		global first
		# inserting D after target B
		#   AB^C
		#   ABDC
		# first, connect our prev to our next, and vice versa
		self.prev_neighbor.next_neighbor = self.next_neighbor
		self.next_neighbor.prev_neighbor = self.prev_neighbor
		# then, set our prev/next
		self.prev_neighbor = target
		self.next_neighbor = target.next_neighbor
		# lastly, insert after target
		target.next_neighbor.prev_neighbor = self
		target.next_neighbor = self

	def do_moves(self):
		if self.value == 0:
			return
		elif self.value > 0:
			cursor = self
			i = 0
			while i < self.value:
				cursor = cursor.next_neighbor
				# skip over ourselves
				if cursor == self:
					i -= 1
				i += 1
			self.insert_after(cursor)
		else:
			cursor = self
			i = 0
			while i < -self.value:
				cursor = cursor.prev_neighbor
				# skip over ourselves
				if cursor == self:
					i -= 1
				i += 1
			self.insert_after(cursor.prev_neighbor)


original_order = []

first_val = True

prev_val = -1

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	the_val = NumVal(int(line), prev_val, -1)

	if first_val:
		first_val = False
	else:
		prev_val.next_neighbor = the_val

	original_order.append(the_val)

	prev_val = the_val

# set the last value's "next_neighbor"
original_order[-1].next_neighbor = original_order[0]

# set the first value's "prev_neighbor"
original_order[0].prev_neighbor = original_order[-1]


for val in original_order:	
	val.do_moves()

##################################
# find Nth values after 0 value
##################################

values_to_find = {}
values_to_find[1000] = -1
values_to_find[2000] = -1
values_to_find[3000] = -1
all_found = False
found_values_sum = 0

# start anywhere, then proceed until we find the 0
cursor = original_order[0]
after_zero_index = -1

while not all_found:

	if after_zero_index < 0 and cursor.value == 0:
		after_zero_index = 0
	elif after_zero_index >= 0:
		after_zero_index += 1
		#print("after_zero_index: {} -- cursor is at ({})".format(after_zero_index, cursor.value))
		if after_zero_index in values_to_find:
			#print("^^^^")
			values_to_find[after_zero_index] = cursor.value
			found_values_sum += cursor.value
			all_found = True
			for k, v in values_to_find.items():
				if v == -1:
					all_found = False

	cursor = cursor.next_neighbor

print("")
print(values_to_find)
print("found values sum: {}".format(found_values_sum))
