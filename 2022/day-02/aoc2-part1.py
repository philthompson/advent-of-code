# python 3

import sys

opponent_key = {'A':'rock', 'B':'paper', 'C':'scissors'}
your_key     = {'X':'rock', 'Y':'paper', 'Z':'scissors'}
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

	score += move_points[your_play]

	if your_play == opponent_play:
		score += 3
		continue

	if your_play == 'rock':
		if opponent_play == 'scissors':
			score += 6

	elif your_play == 'paper':
		if opponent_play == 'rock':
			score += 6

	elif opponent_play == 'paper':
		score += 6

print(score)
