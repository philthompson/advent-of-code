# python 3

import sys

end_of_first_message_marker = 0

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	packet_list = ['delme']
	for i in range(0, 13):
		packet_list.append(line[i])

	# start at 14th char in string (which is 13th position)
	i = 13
	while i < len(line):
		del packet_list[0]
		packet_list.append(line[i])

		packet_set = set(packet_list)

		if len(packet_set) == 14:
			end_of_first_message_marker = i + 1
			break

		i += 1

	# for this puzzle, we are only processing one line of input
	break

print(end_of_first_message_marker)

