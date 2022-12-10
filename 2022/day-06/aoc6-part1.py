# python 3

import sys

end_of_first_packet_marker = 0

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	# start at 4th char in string (which is 3rd position)
	i = 3
	packet_list = ['delme', line[0], line[1], line[2]]
	while i < len(line):
		del packet_list[0]
		packet_list.append(line[i])

		packet_set = set(packet_list)

		if len(packet_set) == 4:
			end_of_first_packet_marker = i + 1
			break

		i += 1

	# for this puzzle, we are only processing one line of input
	break

print(end_of_first_packet_marker)

