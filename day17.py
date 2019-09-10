"""
Spinlock	
"""

from typing import List, Tuple

def step_forward(list_: List[int], n: int,current_position: int) -> Tuple[int,int]:
	final_position = (current_position + n) % len(list_)
	return final_position, list_[final_position]

assert step_forward([1,2,3,4,5],3,0) == (3,4)
assert step_forward([1,2,3,4,5],3,3) == (1,2)
assert step_forward([1,2,3,4,5],5,0) == (0,1)


# n = 314
# current_position = 0
# for i in range(1,50000000+1):
# 	current_position = (current_position + n) % i + 1
# 	if current_position == 1:
# 		print(i)


TEST_STEPS = 314
N_INSERTIONS = 10
pos_ = 0 
L = [0]
for i in range(1,N_INSERTIONS+1):
	pos_,_ = step_forward(L,TEST_STEPS,pos_)
	pos_ = pos_+ 1
	if pos_==1:
		print(f"i: {i}")
	L.insert(pos_,i)


# #print(f"L: {L}, current position: {pos_}")
# print(len(L))
# print(L[pos_])
# print(L[pos_+1])



