# python 3

import sys
import time
from collections import namedtuple

class BoardPos:
	def __init__(self, row, col, is_wall):
		self.row = row
		self.col = col
		self.is_wall = is_wall
		self.neighbor_u = None
		self.neighbor_d = None
		self.neighbor_l = None
		self.neighbor_r = None

positions_by_rowcol = {}
minmax_by_row = {}
minmax_by_col = {}

row_cursor = 1
max_row = -1
max_col = -1

parse_moves = False

all_moves = None

for line in sys.stdin:
	line = line.rstrip()

	if len(line) == 0:
		parse_moves = True
		continue

	if parse_moves:
		all_moves = line
	else:
		for i in range(0, len(line)):
			col_cursor = i + 1
			if line[i] == ' ':
				continue
			positions_by_rowcol[(row_cursor, col_cursor)] = BoardPos(row=row_cursor, col=col_cursor, is_wall=(line[i] == '#'))
			print("board position ({},{}) is [{}]".format(row_cursor, col_cursor, line[i]))
			
			max_row = max(row_cursor, max_row)
			max_col = max(col_cursor, max_col)

			if row_cursor in minmax_by_row:
				minmax_by_row[row_cursor] = (min(col_cursor, minmax_by_row[row_cursor][0]), max(col_cursor, minmax_by_row[row_cursor][1]))
			else:
				minmax_by_row[row_cursor] = (col_cursor, col_cursor)

			if col_cursor in minmax_by_col:
				minmax_by_col[col_cursor] = (min(row_cursor, minmax_by_col[col_cursor][0]), max(row_cursor, minmax_by_col[col_cursor][1]))
			else:
				minmax_by_col[col_cursor] = (row_cursor, row_cursor)

		row_cursor += 1

move_text_idx = 0

moves = []

# split move instruction line into separate moves
while True:
	move = ''

	while move_text_idx < len(all_moves):
		move = move + all_moves[move_text_idx]

		move_text_idx += 1

		if move_text_idx >= len(all_moves) or move == 'L' or move == 'R' or all_moves[move_text_idx] == 'L' or all_moves[move_text_idx] == 'R':
			break

	if move == 'L' or move == 'R':
		moves.append(move)
	else:
		moves.append(int(move))

	if move_text_idx >= len(all_moves):
		break

current_row = None
current_col = None

# set neighbors for all positions, and find starting position
for row in range(1, max_row+1):
	for col in range(1, max_col+1):
		if (row, col) in positions_by_rowcol:
			pos = positions_by_rowcol[(row, col)]

			# starting position is lowest-numbered row and column that isn't a wall
			if not pos.is_wall and (current_row == None or current_col == None):
				current_row = row
				current_col = col

			print("finding neighbors for ({},{})".format(row, col))

			if (row-1, col) in positions_by_rowcol:
				pos.neighbor_u = positions_by_rowcol[(row-1, col)]
				print("    up: ({},{})".format(row-1, col))
			else:
				pos.neighbor_u = positions_by_rowcol[(minmax_by_col[col][1], col)]
				print("    up: ({},{}) (wrap)".format(minmax_by_col[col][1], col))
			
			if (row+1, col) in positions_by_rowcol:
				pos.neighbor_d = positions_by_rowcol[(row+1, col)]
				print("    dn: ({},{})".format(row+1, col))
			else:
				pos.neighbor_d = positions_by_rowcol[(minmax_by_col[col][0], col)]
				print("    dn: ({},{}) (wrap)".format(minmax_by_col[col][0], col))
			
			if (row, col-1) in positions_by_rowcol:
				pos.neighbor_l = positions_by_rowcol[(row, col-1)]
				print("  left: ({},{})".format(row, col-1))
			else:
				pos.neighbor_l = positions_by_rowcol[(row, minmax_by_row[row][1])]
				print("  left: ({},{}) (wrap)".format(row, minmax_by_row[row][1]))
			
			if (row, col+1) in positions_by_rowcol:
				pos.neighbor_r = positions_by_rowcol[(row, col+1)]
				print(" right: ({},{})".format(row, col+1))
			else:
				pos.neighbor_r = positions_by_rowcol[(row, minmax_by_row[row][0])]
				print(" right: ({},{}) (wrap)".format(row, minmax_by_row[row][0]))

# perform all moves
direction = 'r'

for move in moves:
	if move == 'R':
		print("doing {} turn, from {} to ".format(move, direction), end='')
		if direction == 'r':
			direction = 'd'
		elif direction == 'd':
			direction = 'l'
		elif direction == 'l':
			direction = 'u'
		else:
			direction = 'r'
		print(direction)

	elif move == 'L':
		print("doing {} turn, from {} to ".format(move, direction), end='')
		if direction == 'r':
			direction = 'u'
		elif direction == 'd':
			direction = 'r'
		elif direction == 'l':
			direction = 'd'
		else:
			direction = 'l'
		print(direction)

	else:
		print("moving {} {} spaces:".format(direction, move))
		print("    from: ({}, {})".format(current_row, current_col))
		for i in range(0, move):
			current_pos = positions_by_rowcol[(current_row, current_col)]
			if direction == 'r':
				if not current_pos.neighbor_r.is_wall:
					current_col = current_pos.neighbor_r.col

			elif direction == 'd':
				if not current_pos.neighbor_d.is_wall:
					current_row = current_pos.neighbor_d.row

			elif direction == 'l':
				if not current_pos.neighbor_l.is_wall:
					current_col = current_pos.neighbor_l.col

			elif not current_pos.neighbor_u.is_wall:
				current_row = current_pos.neighbor_u.row
			print("      to: ({}, {})".format(current_row, current_col))

print("current_row: {}".format(current_row))
print("current_col: {}".format(current_col))
print("direction: {}".format(direction))
print()
print((current_row * 1000) + (current_col * 4) + (0 if direction == 'r' else 1 if direction == 'd' else 2 if direction == 'l' else 3))

