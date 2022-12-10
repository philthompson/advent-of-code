# python 3

import sys

elf_totals = []

total = 0
for line in sys.stdin:
	line = line.strip()
	if len(line) == 0:
		elf_totals.append(total)
		total = 0
		continue
	total += int(line)

elf_totals.append(total)

top_three_sum = 0
for t in sorted(elf_totals)[-3:]:
	top_three_sum += t

print(top_three_sum)
