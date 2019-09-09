"""
Joel's solution to day 10 
Approach: 
 - We have a state and we are iterating on the state
"""

from typing import NamedTuple, List


class State(NamedTuple):
	numbers: List[int]
	pos: int = 0
	skip_size: int = 0

def step(state: State, length: int) -> State:
	numbers = state.numbers
	skip_size = state.skip_size
	N = len(numbers)
	start = state.pos
	end = state.pos + length

	# get the sub_seq
	sub_seq = [numbers[i % N ] for i  in range(start,end)]

	# revervse
	rev_sub_seq = sub_seq[::-1]

	# remake the List
	for j,idx  in enumerate(range(start,end)):
		numbers[idx % N] = rev_sub_seq[j]

	return State(numbers, (start + length + skip_size) % N , skip_size+1)

TEST_STATE = State(list(range(256)))
state = TEST_STATE
for l in [157,222,1,2,177,254,0,228,159,140,249,187,255,51,76,30]:
	print("Length", l)
	state = step(state,l)
	print(state)

print(state.numbers[0]*state.numbers[1])

