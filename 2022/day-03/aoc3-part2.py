# python 3

import sys

total_item_value = 0

elf_group = []

for line in sys.stdin:
	line = line.strip()

	rucksack_len = len(line)
	if rucksack_len == 0:
		continue

	elf_group.append(line)

	if len(elf_group) == 3:
		for i in range(0, len(elf_group[0])):
			item_char = elf_group[0][i]
			if elf_group[1].find(item_char) > -1 and elf_group[2].find(item_char) > -1:

				# for built-in ord() function, thanks to https://stackoverflow.com/a/12625688/259456
				v = ord(item_char)
				# 'a' becomes 97, but has priority 1 in the rucksack
				if v > 96:
					v = v - 96
				# 'A' becomes 65, but has priority 27 in the rucksack
				else:
					v = v - 38

				#print("common item is [{}], found at [{}],[{}],[{}], with priority [{}]".format(item_char, i, elf_group[1].find(item_char), elf_group[2].find(item_char), v))

				total_item_value += v
				break

		elf_group.clear()

print(total_item_value)
