# python 3

import sys

total_item_value = 0

for line in sys.stdin:
	line = line.strip()

	rucksack_len = len(line)
	if rucksack_len == 0:
		continue

	# assuming each rucksack (line) has even number of chars
	# and assuming each rucksack has only one match in each half
	match_found = False
	for l in range(0, int(rucksack_len/2)):
		if match_found:
			break
		for r in range(int(rucksack_len/2), rucksack_len):
			if line[l] == line[r]:
				# for built-in ord() function, thanks to https://stackoverflow.com/a/12625688/259456
				v = ord(line[l])
				# 'a' becomes 97, but has priority 1 in the rucksack
				if v > 96:
					v = v - 96
				# 'A' becomes 65, but has priority 27 in the rucksack
				else:
					v = v - 38
				#print("pos [{}] and [{}] are [{}], which has val [{}]".format(l, r, line[l], v))

				total_item_value += v
				match_found = True
				break

print(total_item_value)
