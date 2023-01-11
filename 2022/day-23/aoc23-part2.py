# python 3

import sys
from collections import deque

# (row,col)
occupied_pos_by_rowcol = set()

# (row,col)
proposed_pos_by_rowcol = {}

row = -1

for line in sys.stdin:
	row += 1
	line = line.rstrip()

	if len(line) == 0:
		continue

	for i in range(0, len(line)):
		if line[i] == '#':
			occupied_pos_by_rowcol.add((row, i))


directions_consideration_order = deque(['n', 's', 'w', 'e'])

round_num = 0
elves_moved = 1

while elves_moved > 0:
	round_num += 1
	elves_moved = 0

	for elf in occupied_pos_by_rowcol:
		nwest = (elf[0]-1,elf[1]-1)
		north = (elf[0]-1,elf[1])
		neast = (elf[0]-1,elf[1]+1)
		west = (elf[0],elf[1]-1)
		east = (elf[0],elf[1]+1)
		swest = (elf[0]+1,elf[1]-1)
		south = (elf[0]+1,elf[1])
		seast = (elf[0]+1,elf[1]+1)
		if nwest not in occupied_pos_by_rowcol and north not in occupied_pos_by_rowcol and neast not in occupied_pos_by_rowcol and west not in occupied_pos_by_rowcol and east not in occupied_pos_by_rowcol and swest not in occupied_pos_by_rowcol and south not in occupied_pos_by_rowcol and seast not in occupied_pos_by_rowcol:
			continue
		for direction in directions_consideration_order:
			if direction == 'n':
				if nwest not in occupied_pos_by_rowcol and north not in occupied_pos_by_rowcol and neast not in occupied_pos_by_rowcol:
					if north not in proposed_pos_by_rowcol:
						proposed_pos_by_rowcol[north] = []
					proposed_pos_by_rowcol[north].append(elf)
					break
			
			elif direction == 's':
				if swest not in occupied_pos_by_rowcol and south not in occupied_pos_by_rowcol and seast not in occupied_pos_by_rowcol:
					if south not in proposed_pos_by_rowcol:
						proposed_pos_by_rowcol[south] = []
					proposed_pos_by_rowcol[south].append(elf)
					break

			elif direction == 'e':
				if neast not in occupied_pos_by_rowcol and east not in occupied_pos_by_rowcol and seast not in occupied_pos_by_rowcol:
					if east not in proposed_pos_by_rowcol:
						proposed_pos_by_rowcol[east] = []
					proposed_pos_by_rowcol[east].append(elf)
					break

			else:
				if nwest not in occupied_pos_by_rowcol and west not in occupied_pos_by_rowcol and swest not in occupied_pos_by_rowcol:
					if west not in proposed_pos_by_rowcol:
						proposed_pos_by_rowcol[west] = []
					proposed_pos_by_rowcol[west].append(elf)
					break

	for new_pos in proposed_pos_by_rowcol:
		elves = proposed_pos_by_rowcol[new_pos]
		if len(elves) == 1:
			occupied_pos_by_rowcol.remove(elves[0])
			occupied_pos_by_rowcol.add(new_pos)
			elves_moved += 1

	print("during round {}, {} elves moved".format(round_num, elves_moved))

	proposed_pos_by_rowcol = {}

	# move first item to end of list
	directions_consideration_order.rotate(-1)
