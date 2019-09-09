"""
Defragmentation
# Knot Hash Algorithm from day 10

Part 2:
This is exactly like the pipe problem:
We need an input that looks like the following:
i: connection 1, connection 2:
i+1: conncetion1, connection 3:

Then we can use the pipe problem code to solve the problem
"""


from typing import List, Dict, NamedTuple, Set
from day10 import twist, process_list, gen_knot_hash

TEST_KEY_STRING = "flqrgnkx"


def gen_row_hashes(s: str, N: int  = 128) -> Dict[int,str]:
	hash_inputs: Dict[int,str] = {}
	for i in range(N):
		hash_inputs[i] = s+'-'+str(i)

	return hash_inputs

def knot_hash_rows(inputs: Dict[int,str]) -> Dict[int,str]:
	hash_outputs: Dict[int,str] = {}
	for i in inputs.items():
		print(i)
		hash_outputs[i[0]] = gen_knot_hash(i[1])

	return(hash_outputs)

def convert_hex_to_bits(hex: str) -> str:
	output_string = []
	for c in hex:
		output_string.append('{0:04b}'.format(int(c, 16)))
	return "".join(output_string)


def convert_to_bits(knot_hashes: Dict[int,str]) -> Dict[int,str]:
	bit_outputs: Dict[int,str] = {}
	for i in knot_hashes.items():
		bit_outputs[i[0]] = convert_hex_to_bits(i[1])
		assert len(bit_outputs[i[0]]) == 128

	return(bit_outputs)	

def count_ones(s:str) -> int:
	"""
	This counts the number of times a one appears in a string, 
	e.g., 101110 = 4 ones
	"""
	return int(s.count('1'))

def count_grid_ones(s: str,N: int = 128) -> int:

	bits_output = convert_to_bits(knot_hash_rows(gen_row_hashes(s,N)))
	n_ones = 0
	for i in bits_output.items():
		n_ones += count_ones(i[1])
	return n_ones

def label_grid(bit: Dict[int,str]) -> Dict[int,List[int]]:
	"""
	THis will give all positions a unique ID
	"""

	grid: Dict[int,List[int]] = {}
	for i in bit.items():
		grid[i[0]] = [int(c)*ele for ele,c in enumerate(i[1],1+(len(i[1]))*i[0]) ] 

	return grid


def get_neighbours(input_row: List[int], upper: List[int], lower: List[int]) ->Dict[int,List[int]]:
	"""
	This will get a list of neighbours for every position in the input row. 
	"""
	relationships = {}

	for pos,v in enumerate(input_row):
		pos_relationship = [input_row[pos]]
		if input_row[pos] > 0:
			if pos == 0:
				if input_row[pos+1]>0:
					pos_relationship.append(input_row[pos+1])

			elif pos == len(input_row)-1:
				if input_row[pos-1]>0:
					pos_relationship.append(input_row[pos-1])

			else:
				if input_row[pos+1]>0:
					pos_relationship.append(input_row[pos+1])

				if input_row[pos-1]>0:
					pos_relationship.append(input_row[pos-1])

			if upper:
				if upper[pos]>0:
					pos_relationship.append(upper[pos])

			if lower:
				if lower[pos]>0:
					pos_relationship.append(lower[pos])

			relationships[input_row[pos]] = pos_relationship

	return relationships

def calculate_neighbour_tree(label_grid: Dict[int,List[int]]) -> Dict[int,List[int]]:
	"""
	This will calculate the neighbours for every input row
	"""
	tree = {}
	for row in label_grid.keys():
		if row ==0:
		#Beginning
			tree.update(get_neighbours(input_row = label_grid.get(row), lower = label_grid.get(row+1), upper = [] ))

		elif row == max(label_grid.keys()):
		#End
			tree.update(get_neighbours(input_row = label_grid.get(row), upper = label_grid.get(row-1), lower = []))

		else:
		#Middle			
			tree.update(get_neighbours(input_row = label_grid.get(row), upper = label_grid.get(row+1), lower = label_grid.get(row-1)))

	return tree

def reachable_from(graph: Dict[int, List[int]],source: int = 0 ) -> Set[int]:
	"""
	Suppose we had 
	1 -> 1, 2
	2 -> 2, 1, 4
	4 -> 4, 2
	i.e., 
	1 2 
	0 4
	Then:

	frontier = 1
	Reachable = ()

	program = 1, Frontier = ()
	reachable = (1)
	fo next program in 1, 2
		frontier.append(2)

	frontier = 2
	reachable = (1)

	program = 2, frontier = ()
	reachable = (1,2)
	for next program in 2,1,4
		frontier.append(4)

	frontier = 4
	reachable = (1,2)

	program = 4, frontier = () 
	reachable = (1,2,4)
	for nex proghram in 4, 2
		frontier.append()

	return (1,2,4)

	"""


	frontier = [source]
	reachable: Set[int] = set()

	while frontier: # While the frontier has something in it
		program = frontier.pop() # get the last and pop off  
		reachable.add(program)
		for next_program in graph.get(program,[]):
			if next_program not in reachable:
				frontier.append(next_program)

	return reachable


def num_groups(graph: Dict[int,List[int]]) -> int:
	num_groups = 0

	seen: Set[int] =  set()

	# Go through the nodes in the graph
	for source in graph:
		#print(source, source in seen)
		if source not in seen:
			group = reachable_from(graph, source)
			seen = seen | group
			num_groups += 1

	return(num_groups)

def find_num_groups_defreg(s: str, N: int = 128) -> int:
	graph = calculate_neighbour_tree(label_grid(convert_to_bits(knot_hash_rows(gen_row_hashes(s,N)))))

	ngrps = num_groups(graph)

	return ngrps



# unit tests
assert convert_hex_to_bits("0") == "0000"
assert convert_hex_to_bits("1") == "0001"
assert convert_hex_to_bits("f") == "1111"
assert convert_hex_to_bits("a0c20170") == "10100000110000100000000101110000"
assert count_ones('11011') == 4

test_output = convert_to_bits(knot_hash_rows(gen_row_hashes(TEST_KEY_STRING,N = 8)))

print(test_output[0][0:8])
assert test_output[0][0:8] == "11010100"
assert test_output[1][0:8] == "01010101"
assert test_output[2][0:8] == "00001010"
assert test_output[3][0:8] == "10101101"
assert test_output[4][0:8] == "01101000"
assert test_output[5][0:8] == "11001001"
assert test_output[6][0:8] == "01000100"
assert test_output[7][0:8] == "11010110"

#assert count_grid_ones(TEST_KEY_STRING) == 8108

PUZZLE_INPUT = "hfdlxzhv"

print(label_grid({0:'11111',1:'11111'}))
print(get_neighbours(input_row = [0,2,0,4,5], lower = [11,12,13,14,15],upper = [6,7,8,9,10]) )
print(num_groups(calculate_neighbour_tree(label_grid({0:'11011',1:'11001'}))))

print(find_num_groups_defreg(s = PUZZLE_INPUT))








