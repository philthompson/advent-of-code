# python 3

import sys
import random

# turns out this isn't needed?
compare_stack = []

compare_L_orig = ''
compare_R_orig = ''

compare_L = -1
compare_R = -1

pair_index = 1

prev_correct_order_index_sum = 0
correct_order_index_sum = 0

def take_next_token(input_stream):
	if input_stream[0] == '[':
		return ('open-list', input_stream[1:])
	elif input_stream[0] == ']':
		if len(input_stream) > 1 and input_stream[1] == ',':
			return ('close-list', input_stream[2:])
		else:
			return ('close-list', input_stream[1:])
	else:
		i = 0
		while input_stream[i] in '0123456789':
			i += 1
		value = int(input_stream[0:i])
		if input_stream[i] == ',':
			i += 1
		return (value, input_stream[i:])

for line in sys.stdin:
	line = line.strip()

	if len(line) == 0:
		compare_L = -1
		compare_R = -1
		pair_index += 1
		prev_correct_order_index_sum = correct_order_index_sum
		continue

	if compare_L == -1:
		compare_L = line
		compare_L_orig = line
		continue

	if compare_R == -1:
		compare_R = line
		compare_R_orig = line

	if compare_L == -1 or compare_R == -1:
		print("compare_R was just set, and compare_L is not set, which should not happen")
		sys.exit(1)

	compare_stack = []
	compare_completed = False

	skip_L_token = False
	skip_R_token = False

	while not compare_completed:

		if len(compare_L) == 0 or len(compare_R) == 0:
			print("orig lines:")
			print(compare_L_orig)
			print(compare_R_orig)
			print("now with L: \"{}\" and R: \"{}\"".format(compare_L, compare_R))
			print("compare_stack:")
			print(compare_stack)
			if len(compare_L) > 0:
				# right list ran out of items first, so the order is not correct
				print("right ran out of items")
				compare_completed = True
			elif len(compare_R) > 0:
				# left list ran out of items first, so the order is correct
				print("left ran out of items")
				correct_order_index_sum += pair_index
				compare_completed = True
			print("----------------------------------------")
			if compare_completed:
				continue

		if not skip_L_token:
			token_L = take_next_token(compare_L)
			compare_L = token_L[1]

		if not skip_R_token:
			token_R = take_next_token(compare_R)
			compare_R = token_R[1]

		skip_L_token = False
		skip_R_token = False

		if type(token_L[0]) == int and type(token_R[0]) == int:
			if token_L[0] < token_R[0]:
				print("left [{}] < right [{}], so this pair is in correct order".format(token_L[0], token_R[0]))
				correct_order_index_sum += pair_index
				compare_completed = True

			elif token_L[0] > token_R[0]:
				print("left [{}] > right [{}], so this pair is in correct order".format(token_L[0], token_R[0]))
				# the "left" (first) packet is greater than the "right" (second) one, so
				#   they are out of order.  thus, this pair's index is not added to the
				#   running sum, and we can just continue onto the next pair
				compare_completed = True

			# if both tokens are ints, but are the same, then we
			#   proceed to the next token
			else:
				print("left [{}] == right [{}], so comparing next token".format(token_L[0], token_R[0]))

		elif token_L[0] == 'open-list' and token_R[0] == 'open-list':
			print("left [{}] == right [{}], so comparing next token".format(token_L[0], token_R[0]))
			compare_stack.append('list')

		elif token_L[0] == 'open-list' and type(token_R[0]) == int:
			print("left has [{}] and right has [{}], so wrapping right in list".format(token_L[0], token_R[0]))
			compare_stack.append('list')
			# insert ']' into right stream, and skip the right's next token taking
			compare_R = ']' + compare_R
			skip_R_token = True

		elif type(token_L[0]) == int and token_R[0] == 'open-list':
			print("left has [{}] and right has [{}], so wrapping left in list".format(token_L[0], token_R[0]))
			compare_stack.append('list')
			# insert ']' into left stream, and skip the left's next token taking
			compare_L = ']' + compare_L
			skip_L_token = True

		elif token_L[0] == 'close-list' and token_R[0] == 'close-list':
			print("left [{}] == right [{}], so comparing next token".format(token_L[0], token_R[0]))
			compare_stack.pop()

		elif token_L[0] == 'close-list' and (type(token_R[0]) == int or token_R[0] != 'close-list'):
			print("left has [{}] and right has [{}], so left ran out of items first and thus the pair is in the correct order".format(token_L[0], token_R[0]))
			correct_order_index_sum += pair_index
			compare_completed = True

		elif (type(token_L[0]) == int or token_L[0] != 'close-list') and token_R[0] == 'close-list':
			print("left has [{}] and right has [{}], so right ran out of items first and thus the pair is NOT in the correct order".format(token_L[0], token_R[0]))
			# the right list ran out of items while the left had more
			#   items in its list, so the packets are not in the
			#   correct order.  thus, this pair's index is not added
			#   to the running sum, and we can just continue onto the
			#   next pair
			compare_completed = True

		elif len(compare_stack) > 0 and compare_stack[-1] == 'list' and len(compare_L) == 0 and len(compare_R) > 0:
			# left list ran out of items first, so the order is correct
			correct_order_index_sum += pair_index
			compare_completed = True
			print("left ran out of items, in expected line of code")

		#else:
		#	print("len(compare_stack): {}".format(len(compare_stack)))
		#	print("compare_stack[-1]: {}".format(compare_stack[-1]))
		#	print("len(compare_L): {}".format(len(compare_L)))
		#	print("len(compare_R): {}".format(len(compare_R)))
		#	# right list ran out of items first, so the order is not correct
		#	print("right ran out of items?")
		#	compare_completed = True

		elif len(compare_stack) > 0 and compare_stack[-1] == 'list' and len(compare_L) > 0 and len(compare_R) == 0:
			# right list ran out of items first, so the order is not correct
			compare_completed = True
			print("right ran out of items, in expected line of code")

	print("orig lines for pair [{}]:".format(pair_index))
	if correct_order_index_sum == prev_correct_order_index_sum:
		print("in correct order")
	else:
		print("NOT in correct order")
	print(compare_L_orig)
	print(compare_R_orig)
	print("correct order sum is now: [{}]".format(correct_order_index_sum))
	print("----------------------------------------")
