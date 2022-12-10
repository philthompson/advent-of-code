# python 3

import sys

stacks = []

stacks_initialized = False

for line in sys.stdin:
	# can't just strip() here because leading spaces are important
	line = line.rstrip()

	if len(line) == 0:
		continue

	if not stacks_initialized:

		# since stacks are drawn like "[#] " (separated by a space,
		#   where the last stack has no trailing space) we can add
		#   1 to the length of the first line, then divide by 4, to
		#   find the number of stacks

		line_stacks_count = int((len(line)+1)/4)
		print("line has len: {} which contains {} stacks".format(len(line), line_stacks_count))
		if line_stacks_count > len(stacks):
			for i in range(len(stacks), line_stacks_count):
				stacks.append([])
				print("appended a new stack at pos {}".format(i))

		#if len(stacks) == 0:
		#	print("line has len: {}".format(len(line)))
		#	for i in range(0, line_stacks_count):
		#		stacks.append([])
		#	print("created {} empty stacks".format(len(stacks)))

		# if we don't have any stacks on this row, stacks are done
		#   being initialized
		if line.find('[') < 0:
			stacks_initialized = True
			for i in range(0, len(stacks)):
				print(stacks[i])
			continue

		# the Nth stack item is at postion (N*4)+1
		for i in range(0, len(stacks)):
			position = (i*4)+1
			if line[position] == ' ':
				continue

			# stacks are given top down, so every time we see an entry,
			#   insert it into the 0th position in the stack
			stacks[i].insert(0, line[position])

	# assuming all "move ..." lines are valid...
	elif line.find('move') == 0:
		line_split = line.split(' ')
		move_quantity = int(line_split[1])
		move_from = int(line_split[3]) - 1
		move_to = int(line_split[5]) - 1

		for i in range(0, move_quantity):
			item = stacks[move_from].pop()
			stacks[move_to].append(item)

stack_tops = ''

for i in range(0, len(stacks)):
	stack_tops += stacks[i][-1]

print(stack_tops)

