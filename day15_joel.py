"""
Joel's solution to generator problem
"""

from typing import Iterator, Callable
import itertools

class Generator:
	MOD = 2147483647

	def __init__(self,factor: int, prev: int,test: Callable[[int],bool] = None) -> None:
		# Callable is a function from int to bool
		self.factor = factor
		self.prev = prev
		self.test = test or (lambda _: True) # a function that always returns true

	def next(self) -> int:
		passed_test = False
		while not passed_test:
			next_value = (self.factor * self.prev) % self.MOD
			self.prev = next_value
			passed_test = self.test(next_value)
		return next_value
		

	def __call__(self) -> Iterator[int]:
		"""
		Explanation of this code
		------------------------
		1. __call__
		__call__ allows the class's instance to be 
		called as a function, after initialising it.
		e.g. a = A()

		a() will return the __call__

		2. Iterator
		An iterator object is something that will loop 
		through values and execute the statement inside
		e.g. for x in Iterator():
			do something. 

		the Do something is the in the while. 

		3. while True...
				Yield x

		For iterators / generators

		The code below will generator forever.
		Over each generation, it will
		a. Calculate the next_value
		b. Yield the next_value
		c. Update the previous value

		the key word "Next" will work to increment by 1. 
		"""
		while True:
			next_value = (self.factor * self.prev) % self.MOD
			yield next_value
			self.prev = next_value

def count_matches(gen_a: Generator, gen_b: Generator, n: int = 40000000) -> int:
	count = 0
	for i in range(n):
		if i % 100000==0:
			print(i)
		a = gen_a.next()
		b = gen_b.next()
		if a % 65536 == b % 65536:
			count +=1

	return count

if __name__ == "__main__":
	GEN_A = Generator(16807, 289,lambda x: x % 4 == 0)
	GEN_B = Generator(48271, 629, lambda x: x % 8 == 0)	
	print(count_matches(GEN_A, GEN_B,n = 5000000))

	

