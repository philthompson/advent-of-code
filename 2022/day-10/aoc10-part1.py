# python 3

import sys

register_x = 1
cycle_counter = 0

signal_strengths_during_cycles = {20:0, 60:0, 100:0, 140:0, 180:0, 220:0}

def record_signal_strength():
	global register_x
	global cycle_counter
	global signal_strengths_during_cycles
	if cycle_counter in signal_strengths_during_cycles:
		signal_strengths_during_cycles[cycle_counter] = cycle_counter * register_x

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	if line[0:4] == 'noop':
		cycle_counter += 1
		record_signal_strength()

	elif line[0:4] == 'addx':
		cycle_counter += 1
		record_signal_strength()
		cycle_counter += 1
		record_signal_strength()
		register_x += int(line[5:])

signal_strengths_sum = 0
for c in signal_strengths_during_cycles:
	print("during cycle [{}], signal strength is [{}]".format(c, signal_strengths_during_cycles[c]))
	signal_strengths_sum += signal_strengths_during_cycles[c]

print("signal strengths sum: [{}]".format(signal_strengths_sum))