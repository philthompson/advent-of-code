# python 3
#
# this one picks the starting digit
#
# this one works from left to right, finding
#   one digit at a time
#

import sys

total = 0

def snafu_to_decimal(snafu):
	magnitude = len(snafu)

	quantity = 0

	for right in range(0, magnitude):
		power = magnitude - right - 1
		char = snafu[right]
		if char == '2':
			quantity += (5**power) * 2
		elif char == '1':
			quantity += (5**power)
		elif char == '-':
			quantity -= (5**power)
		elif char == '=':
			quantity -= (5**power) * 2

	return quantity

def snafu_list_to_decimal(snafu):
	return snafu_to_decimal(''.join(snafu))

# since the first/leftmost digit must be
#   '1' or '2', we can find the smallest and
#   largest values that can be made with each
#   magnitude of snafu value
#
# for example:
# 1 is 1,     and 2 is 2
# 1= is 3,    and 22   is 12
# 1== is 13,  and 222  is 62
# 1=== is 63, and 2222 is 312
# ...
#
def decimal_to_snafu(decimal):
	magnitude = 1
	largest = ['2']
	smallest = ['1']

	while snafu_list_to_decimal(largest) < decimal:
		magnitude += 1
		largest.append('2')
		smallest.append('=')

	smallest_starting_with_2 = ''.join(largest).replace('2','=').replace('=','2',1)
	largest_starting_with_1 = ''.join(smallest).replace('=','2')

	if decimal <= snafu_to_decimal(largest_starting_with_1):
		print("it defintely starts with '1', and is <= {}".format(largest_starting_with_1))
		algo(smallest, 1, decimal)
	elif decimal >= snafu_to_decimal(smallest_starting_with_2):
		print("it defintely starts with '2', and is >= {}".format(smallest_starting_with_2))
		smallest[0] = '2'
		algo(smallest, 1, decimal)


# working from left to right:
# if smaller than 22===, it may be:
#                 21===
# if smaller than 21===, it may be:
#                 20===
def algo(digits, place, goal):
	for char in ['2','1','0','-','=']:
		digits[place] = char
		decimal = snafu_to_decimal(digits)
		if goal == decimal:
			print("{} -> {}".format(''.join(digits), goal))
			sys.exit(0)
		if goal > decimal:
			break

	place += 1
	if place >= len(digits):
		return

	algo(digits, place, goal)

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	quantity = snafu_to_decimal(line)

	print("{} -> {:,}".format(line, quantity))
	total += quantity

print("total is: {:,}".format(total))

decimal_to_snafu(total)
