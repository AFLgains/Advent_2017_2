"""
Day 15:
Dueling generators
"""

from typing import List

class generator():
	def __init__(self,name,factor,divisor):
		self.name = name
		self.factor = factor
		self.divisor = divisor
		self.allowed_numbers = []

	def gen_next_value(self,prev_value: int) -> int:
		return (prev_value*self.factor) % self.divisor


def get_lowest_16(n: int) -> str:
	return '{0:032b}'.format(n)[-16:]


def judge(n1: List[int], n2: List[int]) -> int:
	"""
	Compare the lowest 16 bits of each number 
	"""
	min_length = min(len(n1),len(n2))
	pass_count = 0
	for i in range(min_length):
		pass_count += get_lowest_16(n1[i]) == get_lowest_16(n2[i])

	return pass_count


#assert '{0:032b}'.format(gen_A.gen_next_value(65)) == "00000000000100001010101101100111"
#assert '{0:032b}'.format(gen_A.gen_next_value(gen_A.gen_next_value(gen_A.gen_next_value(65)))) == "00001110101000101110001101001010"


if __name__ == "__main__":

	global_divisor = 2147483647
	gen_A  = generator(name = "GenA",factor = 16807,divisor = global_divisor)
	gen_B  = generator(name = "GenB",factor = 48271,divisor = global_divisor)
	N_rounds = 5000000
	A = 591
	B = 393 
	i = 0 
	while len(gen_A.allowed_numbers)<N_rounds or len(gen_B.allowed_numbers)<N_rounds:

		A = gen_A.gen_next_value(A)
		B = gen_B.gen_next_value(B)
		if (A%4==0):
			gen_A.allowed_numbers.append(A)
		if (B%8==0):
			gen_B.allowed_numbers.append(B)

		if (i % 100000==0):
			print(f"i: {i}, A: {len(gen_A.allowed_numbers)}, B: {len(gen_B.allowed_numbers)}")

		i +=1

	judge_count = judge(gen_A.allowed_numbers, gen_B.allowed_numbers)
	
	print(len(gen_A.allowed_numbers))
	print(len(gen_B.allowed_numbers))
	print(judge_count)
