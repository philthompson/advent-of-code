# python 3

import sys
import json

root_tree = {'/':{}}

input_line_number = 0
parent_dir_stack_tree = [root_tree]
parent_dir_stack_name = ['/']
working_dir_tree = root_tree

for line in sys.stdin:
	input_line_number += 1
	line = line.strip()

	if len(line) == 0:
		continue

	# command
	if line[0] == '$':
		if line.find('$ cd ') == 0:
			new_dir_rel = line.split(' ')[2]

			if new_dir_rel == '..':
				parent_dir_stack_name.pop()
				working_dir_tree = parent_dir_stack_tree.pop()

			else:
				if not new_dir_rel in working_dir_tree:
					print("line {}: dir [{}] is not in working dir [{}]".format(input_line_number, new_dir_rel, parent_dir_stack_name[-1]))
				
				parent_dir_stack_tree.append(working_dir_tree)
				parent_dir_stack_name.append(new_dir_rel)
				working_dir_tree = working_dir_tree[new_dir_rel]

		# we can just ignore ls commands, i think
		#elif line.find('$ ls') == 0:

	# subdirectory is specified
	elif line.find('dir ') == 0:
		child_dir_rel = line.split(' ')[1]
		working_dir_tree[child_dir_rel] = {}

	# file is specified
	else:
		child_file_rel_split = line.split(' ')
		working_dir_tree[child_file_rel_split[1]] = int(child_file_rel_split[0])

# thanks to https://stackoverflow.com/a/3314411/259456 for nested dict pretty printing
print(json.dumps(root_tree, indent=4))

# traverse the entire thing, adding up all dirs of size <= 100000
large_dirs_sizes = []

def traverse(dir_tree, is_root):
	global large_dirs_sizes
	size_total = 0
	for child in dir_tree:
		if type(dir_tree[child]) == int:
			size_total += dir_tree[child]

		elif type(dir_tree[child]) == dict:
			print("traversing into child dir [{}]".format(child))
			size_total += traverse(dir_tree[child], False)

	if size_total <= 100000 and not is_root:
		large_dirs_sizes.append(size_total)

	return size_total

# starting at just "root_tree", instead of "root_tree['/']", works
#   but it counts the entire '/' dir as a "large directory" which
#   i'm now guessing is not supposed to happen (the problem description
#   doesn't specify this)
#traverse(root_tree, True)
traverse(root_tree['/'], True)

print(large_dirs_sizes)

large_dirs_sizes_sum = 0

for i in large_dirs_sizes:
	large_dirs_sizes_sum += i

print(large_dirs_sizes_sum)
