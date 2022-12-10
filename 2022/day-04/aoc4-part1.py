# python 3

import sys

pairs_with_fully_contained = 0

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	elves = line.split(',')

	elves[0] = elves[0].split('-')
	elves[1] = elves[1].split('-')

	elf_a_lo = int(elves[0][0])
	elf_a_hi = int(elves[0][1])
	elf_b_lo = int(elves[1][0])
	elf_b_hi = int(elves[1][1])

	if   elf_a_lo <= elf_b_lo and elf_a_hi >= elf_b_hi:
		pairs_with_fully_contained += 1
		print(line)
	elif elf_b_lo <= elf_a_lo and elf_b_hi >= elf_a_hi:
		pairs_with_fully_contained += 1
		print(line)

print(pairs_with_fully_contained)
