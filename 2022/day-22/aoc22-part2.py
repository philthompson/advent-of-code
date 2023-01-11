# python 3

import sys
import time
import math
from collections import namedtuple

State = namedtuple('State', ['row', 'col', 'orig_direction', 'normal_vector', 'trans_pos'])

cube_size = int(sys.argv[1])

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
wrap_neighbors_by_rowcoldir = {}
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

def get_face_center(row, col):
	global cube_size
	row_face = math.ceil(row / cube_size)
	col_face = math.ceil(col / cube_size)
	face_row_max = row_face * cube_size
	face_row_min = ((row_face - 1) * cube_size) + 1
	face_col_max = col_face * cube_size
	face_col_min = ((col_face - 1) * cube_size) + 1
	# (center of face row, center of face col)
	cube_center = ((face_row_max + face_row_min) / 2, (face_col_max + face_col_min) / 2)
	print("(row,col) of ({},{}) belongs to face ({},{}) with cube center at {}".format(row, col, row_face, col_face, cube_center))
	return cube_center

# where degrees_counterclockwise of -90 degrees is
#   a 1/4 turn clockwise
def rotate_point_around_face_center(row, col, degrees_counterclockwise):

	degrees = degrees_counterclockwise % 360
	if degrees % 90 != 0:
		print("unsupported rotation of {}".format(degrees_counterclockwise))
		sys.exit(1)
	
	cube_center = get_face_center(row, col)
	
	row_new = row
	col_new = col
	# perform one 90 rotation
	if degrees > 0:
		# swap row and col about the face center
		row_diff = cube_center[0] - row  # 25.5 - 1 = 24.5
		col_diff = cube_center[1] - col  # 25.5 - 50 = -24.5
		row_new = cube_center[0] + col_diff # 1 = 25.5 + -24.5 = 1
		col_new = cube_center[1] - row_diff # 1 = 25.5 - 24.5 = 1
		#
		# for row=2, col=10, deg_ccw=90 ---> row=
		# row_diff = 25.5 - 2 = 23.5
		# col_diff = 25.5 - 10 = 15.5
		# row_new = 25.5 + 15.5 = 41
		# col_new = 25.5 - 23.5 = 2
		# might be right?
		#
		# for row=1, col=26, deg_ccw=90 ---> row=25, col=1
		# row_diff = 25.5 - 1 = 24.5
		# col_diff = 25.5 - 26 = -0.5
		# row_new = 25.5 + -0.5 = 25
		# col_new = 25.5 - 24.5 = 1
		# looks right
		#
		# for row=26, col=1, deg_ccw=90 ----> row=50? col=26?
		#
		# for row=50, col=26, deg_ccw=90 ----> row=25? col=50?
		degrees -= 90
	if degrees <= 0:
		return (row_new, col_new)
	# perform another 90 rotation if necessary
	return rotate_point_around_face_center(row_new, col_new, degrees)

# results of 1/4 turn about the y or x axis, as applied to 3D vector
vec_rot = {}
vec_rot[( 0, 0, 1)] = {'+x': ( 0,-1, 0), '-x': ( 0, 1, 0), '+y': ( 1, 0, 0), '-y': (-1, 0, 0)}
vec_rot[( 0, 0,-1)] = {'+x': ( 0, 1, 0), '-x': ( 0,-1, 0), '+y': (-1, 0, 0), '-y': ( 1, 0, 0)}
vec_rot[( 0, 1, 0)] = {'+x': ( 0, 0, 1), '-x': ( 0, 0,-1), '+y': ( 0, 1, 0), '-y': ( 0, 1, 0)}
vec_rot[( 0,-1, 0)] = {'+x': ( 0, 0,-1), '-x': ( 0, 0, 1), '+y': ( 0,-1, 0), '-y': ( 0,-1, 0)}
vec_rot[( 1, 0, 0)] = {'+x': ( 1, 0, 0), '-x': ( 1, 0, 0), '+y': ( 0, 0,-1), '-y': ( 0, 0, 1)}
vec_rot[(-1, 0, 0)] = {'+x': (-1, 0, 0), '-x': (-1, 0, 0), '+y': ( 0, 0, 1), '-y': ( 0, 0,-1)}

visited_positions = set()
new_row_col_dir = None

def find_matching_edge_entry(row, col, direction):
	global new_row_col_dir
	
	visited_positions = set()
	new_row_col_dir = None
	prev_trans_pos = (row,col)

	dir_vector = (0, 1, 0)
	if direction == 'r':
		dir_vector = (1, 0, 0)
	elif direction == 'd':
		dir_vector = (0, -1, 0)
	elif direction == 'l':
		dir_vector = (-1, 0, 0)

	print("finding matching wrapped edge for ({},{},{})".format(row, col, direction))
	find_matching_edge(State(row=row, col=col, orig_direction=direction, normal_vector=(0, 0, 1), trans_pos=(row,col)), dir_vector, prev_trans_pos=prev_trans_pos)
	print("matching wrapped edge for ({},{},{}) is {}".format(row, col, direction, new_row_col_dir))
	return new_row_col_dir

# recursive function to pathfind to associated edge
#   of other face
#
# imagine cube face-down centered on the board at
#   the position representing this cube's face
# - up from paper is positive Z
# - left to right on paper is positive X
# - down to up on paper is positive Y
#
# state is a tuple/namedtuple with:
# - row (orig position)
# - col (orig position)
# - orig_direction (r/l/u/d)
# - normal_vector (3-tuple of 0/1/-1, x, y, z,  starting pointing up (0,0,1))
# - trans_pos (translated position (not taking rotation into account) (row,col))
# - cube_center (2-tuple of current position, (row, col))
# - prev_cube_center
#
# also pass along (not in state):
# - dir_vector (movement direction, total/cumulative over all rotations so far)
# - prev_trans_pos
#
def find_matching_edge(state, dir_vector, prev_trans_pos):
	global positions_by_rowcol
	global visited_positions
	global new_row_col_dir
	global vec_rot
	global cube_size

	# if the current state has already been visited by
	#   this recursive function, terminate this sequence
	if state in visited_positions:
		return

	if new_row_col_dir != None:
		return

	# since we want to follow the flattened shape the entire
	#   time, except for the last rotation, we can terminate
	#   any sequence that has a previous translated location
	#   outside of the flattened shape
	if prev_trans_pos not in positions_by_rowcol:
		return

	# if the original face is back face-down on the paper
	#   again (the normal vector points straight up), and
	#   the original edge lies along an edge of the flattened
	#   shape, we are done
	if state.normal_vector == (0, 0, 1) and state.trans_pos not in positions_by_rowcol:
		orig_direction_degrees = {'r':0, 'd':-90, 'l':-180, 'u':-270}[state.orig_direction]
		new_direction_degrees = {(1,0,0):0, (0,-1,0):-90, (-1,0,0):-180, (0,1,0):-270}[dir_vector]
		net_degrees = new_direction_degrees - orig_direction_degrees
		print("CALC degrees: orig [{}], new [{}] -> orig degrees [{}], new degrees [{}], net [{}]".format(state.orig_direction, dir_vector, orig_direction_degrees, new_direction_degrees, net_degrees))
		new_pos = rotate_point_around_face_center(state.trans_pos[0], state.trans_pos[1], net_degrees)

		print("we have up normal_vector at new outside-the-shape position {} with final movement vector (x,y,z) of {} which combine to give us new pos {}".format(state.trans_pos, dir_vector, new_pos))

		# check that moving in new direction, from new row+col, puts us back on the board
		moved_row = new_pos[0]
		moved_col = new_pos[1]
		new_dir_name = {(1,0,0):'r', (0,-1,0):'d', (-1,0,0):'l', (0,1,0):'u'}[dir_vector]
		if new_dir_name == 'r':
			moved_col += 1
		elif new_dir_name == 'l':
			moved_col -= 1
		elif new_dir_name == 'u':
			moved_row -= 1
		elif new_dir_name == 'd':
			moved_row += 1
		else:
			print("unexpected final dir_vector of {} for state:".format(dir_vector))
			print(state._asdict())
			sys.exit(1)

		if (moved_row, moved_col) in positions_by_rowcol:
			if get_face_center(moved_row, moved_col) == get_face_center(state.row, state.col):
				print("    moving in new [{}] direction puts us back on the board, but on THE ORIGINAL FACE, so we are terminating".format(new_dir_name))
				return
			else:
				print("    moving in new [{}] direction DOES put us back on the board on a different face, so we are done".format(new_dir_name))
				new_row_col_dir = (moved_row, moved_col, new_dir_name)
				return
		else:
			print("    moving in new [{}] direction does NOT put us back on the board, so terminating".format(new_dir_name))
			return

	# otherwise, continue moving+rotating the cube
	visited_positions.add(state)
	print("normal_vector now {} at translated position {} with movement vector (x,y,z) of {}".format(state.normal_vector, state.trans_pos, dir_vector))

	# try rotating cube so the potential face location to
	#   the left is used (negative rotation around Y axis)
	# (only if we're not backtracking to where we just were)
	new_pos = (state.trans_pos[0], state.trans_pos[1] - cube_size)
	if new_pos != prev_trans_pos:
		print("simulating rotation to next face to the left")
		new_vec = vec_rot[state.normal_vector]['-y']
		new_state = state._replace(normal_vector=new_vec, trans_pos=new_pos)
		new_dir_vec = vec_rot[dir_vector]['-y']
		find_matching_edge(new_state, new_dir_vec, state.trans_pos)

	# try rotating cube so the potential face location to
	#   the right is used (positive rotation around Y axis)
	# (only if we're not backtracking to where we just were)
	new_pos = (state.trans_pos[0], state.trans_pos[1] + cube_size)
	if new_pos != prev_trans_pos:
		new_vec = vec_rot[state.normal_vector]['+y']
		print("simulating rotation to next face to the right")
		new_state = state._replace(normal_vector=new_vec, trans_pos=new_pos)
		new_dir_vec = vec_rot[dir_vector]['+y']
		find_matching_edge(new_state, new_dir_vec, state.trans_pos)

	# try rotating cube so the potential face location
	#   above is used (negative rotation around X axis)
	# (only if we're not backtracking to where we just were)
	new_pos = (state.trans_pos[0] - cube_size, state.trans_pos[1])
	if new_pos != prev_trans_pos:
		print("simulating rotation to next face above")
		new_vec = vec_rot[state.normal_vector]['-x']
		new_state = state._replace(normal_vector=new_vec, trans_pos=new_pos)
		new_dir_vec = vec_rot[dir_vector]['-x']
		find_matching_edge(new_state, new_dir_vec, state.trans_pos)

	# try rotating cube so the potential face location
	#   below is used (positive rotation around X axis)
	# (only if we're not backtracking to where we just were)
	new_pos = (state.trans_pos[0] + cube_size, state.trans_pos[1])
	if new_pos != prev_trans_pos:
		print("simulating rotation to next face below")
		new_vec = vec_rot[state.normal_vector]['+x']
		new_state = state._replace(normal_vector=new_vec, trans_pos=new_pos)
		new_dir_vec = vec_rot[dir_vector]['+x']
		find_matching_edge(new_state, new_dir_vec, state.trans_pos)



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
			sys.stdout.flush()

			if (row-1, col) in positions_by_rowcol:
				pos.neighbor_u = positions_by_rowcol[(row-1, col)]
				print("    up: ({},{})".format(row-1, col))
			else:
				wrap_neighbor = find_matching_edge_entry(row, col, 'u')
				print("find_matching_edge_entry: {}".format(wrap_neighbor))
				wrap_neighbors_by_rowcoldir[(row, col, 'u')] = wrap_neighbor
				print("    up: {} (wrap)".format(wrap_neighbor))
			
			if (row+1, col) in positions_by_rowcol:
				pos.neighbor_d = positions_by_rowcol[(row+1, col)]
				print("    dn: ({},{})".format(row+1, col))
			else:
				wrap_neighbor = find_matching_edge_entry(row, col, 'd')
				wrap_neighbors_by_rowcoldir[(row, col, 'd')] = wrap_neighbor
				print("    dn: {} (wrap)".format(wrap_neighbor))
			
			if (row, col-1) in positions_by_rowcol:
				pos.neighbor_l = positions_by_rowcol[(row, col-1)]
				print("  left: ({},{})".format(row, col-1))
			else:
				wrap_neighbor = find_matching_edge_entry(row, col, 'l')
				wrap_neighbors_by_rowcoldir[(row, col, 'l')] = wrap_neighbor
				print("  left: {} (wrap)".format(wrap_neighbor))
			
			if (row, col+1) in positions_by_rowcol:
				pos.neighbor_r = positions_by_rowcol[(row, col+1)]
				print(" right: ({},{})".format(row, col+1))
			else:
				wrap_neighbor = find_matching_edge_entry(row, col, 'r')
				wrap_neighbors_by_rowcoldir[(row, col, 'r')] = wrap_neighbor
				print(" right: {} (wrap)".format(wrap_neighbor))

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
			if (current_row, current_col, direction) in wrap_neighbors_by_rowcoldir:
				wrap = wrap_neighbors_by_rowcoldir[(current_row, current_col, direction)]
				if not positions_by_rowcol[(wrap[0], wrap[1])].is_wall:
					current_row = wrap[0]
					current_col = wrap[1]
					direction = wrap[2]
					print("      to: ({}, {}) (with new direction {})".format(current_row, current_col, direction))
				continue
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

			else:
				if not current_pos.neighbor_u.is_wall:
					current_row = current_pos.neighbor_u.row
			print("      to: ({}, {})".format(current_row, current_col))

print("current_row: {}".format(current_row))
print("current_col: {}".format(current_col))
print("direction: {}".format(direction))
print()
print((current_row * 1000) + (current_col * 4) + (0 if direction == 'r' else 1 if direction == 'd' else 2 if direction == 'l' else 3))

