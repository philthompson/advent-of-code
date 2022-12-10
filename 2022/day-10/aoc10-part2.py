# python 3

import sys

register_x = 1
cycle_counter = 0

# display has 6 lines of 40 pixels
display_rows = 6
line_pixels = 40

display_lines = []
for i in range(0, display_rows):
	display_lines.append([])
	for j in range(0, line_pixels):
	  display_lines[i].append(' ')

def draw_to_display():
	global register_x
	global cycle_counter
	global display_lines
	global line_pixels
	
	zero_based_cycle = cycle_counter - 1
	current_line = int(zero_based_cycle / line_pixels) % display_rows
	current_pixel = zero_based_cycle % line_pixels

	#if register_x >= cycle_counter - 1 and register_x <= cycle_counter + 1:
	#if register_x >= zero_based_cycle - 1 and register_x <= zero_based_cycle + 1:
	if register_x >= current_pixel - 1 and register_x <= current_pixel + 1:
		#print("line {} pixel {} is #".format(current_line, current_pixel))
		display_lines[current_line][current_pixel] = '#'
	else:
		#print("line {} pixel {} is .".format(current_line, current_pixel))
		display_lines[current_line][current_pixel] = '.'

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	if line[0:4] == 'noop':
		cycle_counter += 1
		draw_to_display()

	elif line[0:4] == 'addx':
		cycle_counter += 1
		draw_to_display()
		cycle_counter += 1
		draw_to_display()
		register_x += int(line[5:])

for line in display_lines:
	print(''.join(line))