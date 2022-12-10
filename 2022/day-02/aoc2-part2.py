# python 3

import sys

opponent_key = {'A':'rock', 'B':'paper', 'C':'scissors'}
your_key     = {'X':'lose', 'Y':'draw', 'Z':'win'}
move_points = {'rock':1, 'paper':2, 'scissors':3}

score = 0
for line in sys.stdin:
	line = line.strip()
	if len(line) == 0:
		continue

	opponent_play = line[0]
	your_play = line[2]

	opponent_play = opponent_key[opponent_play]
	your_play = your_key[your_play]

	if your_play == 'draw':
		score += 3
		score += move_points[opponent_play]
		continue

	if your_play == 'win':
		score += 6
		if opponent_play == 'rock':
			score += move_points['paper']
		elif opponent_play == 'paper':
			score += move_points['scissors']
		else:
			score += move_points['rock']

	else:
		if opponent_play == 'rock':
			score += move_points['scissors']
		elif opponent_play == 'paper':
			score += move_points['rock']
		else:
			score += move_points['paper']

print(score)
