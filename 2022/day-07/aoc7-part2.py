# python 3

import sys
import json

total_disk_space = 70000000
desired_unused_space = 30000000
current_unused_space = -1

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
#print(json.dumps(root_tree, indent=4))

# traverse the entire thing, adding up the root dir, and also
#   tracking the size of the dirs that, if deleted, would free
#   up enough space

dir_to_delete_size = -1

def traverse(dir_tree, is_root):
	global large_dirs_sizes
	global current_unused_space
	global dir_to_delete_size
	global desired_unused_space
	size_total = 0
	for child in dir_tree:
		if type(dir_tree[child]) == int:
			size_total += dir_tree[child]

		elif type(dir_tree[child]) == dict:
			#print("traversing into child dir [{}]".format(child))
			size_total += traverse(dir_tree[child], False)

	# once we've done a single full traversal, we know
	#   the total used space and can figure out which
	#   individual dir to delete
	if current_unused_space >= 0:
		if size_total + current_unused_space > desired_unused_space:
			if dir_to_delete_size < 0 or size_total < dir_to_delete_size:
				dir_to_delete_size = size_total

	return size_total

# starting at just "root_tree", instead of "root_tree['/']", works
#   but it counts the entire '/' dir as a "large directory" which
#   i'm now guessing is not supposed to happen (the problem description
#   doesn't specify this)
#traverse(root_tree, True)
root_dir_size = traverse(root_tree['/'], True)

current_unused_space = total_disk_space - root_dir_size

print("after 1st traversal:")
print("                     root_dir_size:        [{}]".format(root_dir_size))
print("                     current_unused_space: [{}]".format(current_unused_space))
print("                     dir_to_delete_size:   [{}]".format(dir_to_delete_size))

traverse(root_tree['/'], True)

print("after 2nd traversal:")
print("                     dir_to_delete_size:   [{}]".format(dir_to_delete_size))
