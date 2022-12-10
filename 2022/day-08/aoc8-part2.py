# python 3

import sys

# read line, and append to list
#
# it's a bit more efficient to convert
#   chars to ints on the first pass,
#   rather than leaving them as strings
grid = []

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		continue

	row = []
	for i in range(0, len(line)):
		row.append(int(line[i]))

	grid.append(row)

# we'll just call the line-by-line dimension 'x' and
#   the char-by-char dimension 'y'
size_x = len(grid)
size_y = len(grid[0])

# for part 2, we will proceed to the edge of the grid,
#   in all 4 directions, from each position in the interior
#   of the grid

max_scenic_score = 0

for x in range(0, size_x - 1):
	for y in range(0, size_y - 1):
		tree_height = grid[x][y]

		trees_visible_neg_x = 0
		trees_visible_pos_x = 0
		trees_visible_neg_y = 0
		trees_visible_pos_y = 0

		# negative x (starting from x-1, proceeding until 0 (1 more than -1), with a step of -1)
		for c in range(x-1, -1, -1):
			trees_visible_neg_x += 1
			if grid[c][y] >= tree_height:
				break

		# positive x
		for c in range(x+1, size_x):
			trees_visible_pos_x += 1
			if grid[c][y] >= tree_height:
				break

		# negative y
		for c in range(y-1, -1, -1):
			trees_visible_neg_y += 1
			if grid[x][c] >= tree_height:
				break

		# positive y
		for c in range(y+1, size_y):
			trees_visible_pos_y += 1
			if grid[x][c] >= tree_height:
				break

		scenic_score = trees_visible_neg_x * trees_visible_pos_x * trees_visible_neg_y * trees_visible_pos_y
		print("tree at ({},{}), of height [{}] has score [{}]".format(x, y, tree_height, scenic_score))

		if scenic_score > max_scenic_score:
			max_scenic_score = scenic_score

print("max_scenic_score: [{}]".format(max_scenic_score))

