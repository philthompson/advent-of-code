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

print(sorted(elf_totals)[-1])
