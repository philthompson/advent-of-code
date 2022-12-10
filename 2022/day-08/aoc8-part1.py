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

# naive algorithm is to proceed to the edge of the grid,
#   in all 4 directions, from each position in the interior
#   of the grid

visible_trees = 0

for x in range(1, size_x - 1):
	for y in range(1, size_y - 1):
		tree_height = grid[x][y]

		tree_visible_neg_x = True
		tree_visible_pos_x = True
		tree_visible_neg_y = True
		tree_visible_pos_y = True

		# negative x
		for c in range(0, x):
			if grid[c][y] >= tree_height:
				tree_visible_neg_x = False
				break

		# positive x
		for c in range(x+1, size_x):
			if grid[c][y] >= tree_height:
				tree_visible_pos_x = False
				break

		# negative y
		for c in range(0, y):
			if grid[x][c] >= tree_height:
				tree_visible_neg_y = False
				break

		# positive y
		for c in range(y+1, size_y):
			if grid[x][c] >= tree_height:
				tree_visible_pos_y = False
				break

		if tree_visible_neg_x or tree_visible_pos_x or tree_visible_neg_y or tree_visible_pos_y:
			print("tree at ({},{}), of height [{}] is visible".format(x, y, tree_height))
			visible_trees += 1

print("visible interior trees: [{}]".format(visible_trees))

exterior_trees = size_x + size_x + size_y + size_y - 4
print("size_x: [{}], size_y: [{}], therefore [{}] visible exterior trees".format(size_x, size_y, exterior_trees))

print("total visible trees: {}".format(exterior_trees + visible_trees))