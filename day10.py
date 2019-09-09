"""
Twists
"""

from typing import List, Tuple
from functools import reduce

# Part 1


def twist(seq: List[int], current_position: int, length: int,skip: int):
	"""
	Return a twisted list
	i.e. segmented and reversed
	"""

	assert current_position <= len(seq) # the index must be inside the sequence

	# Create a copy
	seq = seq[:]

	first_index = current_position
	end_index = current_position+length

	# get the sub_seq
	sub_seq = [seq[i % len(seq) ] for i  in range(first_index,end_index)]

	# revervse
	rev_sub_seq = sub_seq[::-1]

	# remake the List
	for j,idx  in enumerate(range(first_index,end_index)):
		seq[idx % len(seq)] = rev_sub_seq[j]

	# Debugging information
	#print(f"seq {seq}, rev_seq {rev_sub_seq}, position {current_position}, next position {(current_position+length+skip) % len(seq)}, skip {skip}")

	# Return
	return seq, (current_position+length+skip) % len(seq)


def process_list(seq: List[int], 
				lengths: List[int],
				current_position: int = 0,
				skip: int = 0) -> int:

	# 1. for increment lengths
	for L in lengths:
		seq,current_position = twist(seq, current_position, L,skip)
		skip +=1

	return(seq, current_position,skip)


TEST_INPUT_LIST = [0,1,2,3,4]
TEST_INPUT_LENGTHS = [3, 4, 1, 5]


seq,_,_ = process_list(TEST_INPUT_LIST,TEST_INPUT_LENGTHS);
assert seq[0]*seq[1] == 12


INPUT = [157,222,1,2,177,254,0,228,159,140,249,187,255,51,76,30]
#INPUT = [199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192]
seq,_,_ = process_list(list(range(0,256)),INPUT)
#print(seq[0]*seq[1])


# Part 2:
def gen_knot_hash(INPUT_STR:str, nRounds: int = 64) -> str:

	length = list()
	for c in INPUT_STR:
		length.append(ord(c))
	INPUT_LENGTH = length + [17,31,73,47,23]
	pos,skip = 0,0
	sparse_hash = list(range(0,256))
	for _ in range(nRounds):
		sparse_hash,pos,skip = process_list(sparse_hash,INPUT_LENGTH,pos,skip)


	assert len(set(sparse_hash)) == len(sparse_hash)
	assert max(sparse_hash) == 255

	dense_hash = list()
	for j in range(16):
		dense_hash.append(reduce(lambda i,j : int(i) ^ int(j),sparse_hash[(0+j*16):(16+j*16) ] ) ) 

	output  = [ str(hex(i)[2:]).zfill(2) for i in dense_hash]
	#print(output)
	return("".join(output))


#print(gen_knot_hash("1,2,3"))
#print(gen_knot_hash(""))

assert gen_knot_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
assert gen_knot_hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
assert gen_knot_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
assert gen_knot_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"


#print(gen_knot_hash("157,222,1,2,177,254,0,228,159,140,249,187,255,51,76,30"))

