"""
groups + garbage
"""


from typing import NamedTuple, List, Dict
from collections import defaultdict
import re


def update_score(current_score: int, last_group_level: int, current_group_level: int) -> int:
	
	if current_group_level < last_group_level:
		current_score = current_score + 1*last_group_level

	return(current_score)



class string_state():
	def __init__(self):
		self.group_level = 0
		self.last_group_level = 0
		self.garbage_open = False
		self.ignore_next = False 
		self.position = 0 
		self.cum_score = 0
		self.garbage_count = 0 

	def update_state(self,next_str):

		# Get the last group level
		self.last_group_level = self.group_level



		# Update the state
		if self.ignore_next: 
			self.ignore_next = False

		elif next_str == "!":
			self.ignore_next = True			

		elif self.garbage_open and next_str == ">":

			self.garbage_open = False

		elif self.garbage_open and next_str != ">":

			self.garbage_count +=1

		elif next_str == "<" and self.garbage_open == False:

			self.garbage_open = True
		
		elif next_str == "{" and self.garbage_open == False:
			self.group_level += 1
		elif next_str == "}" and self.garbage_open == False:
			self.group_level -= 1





		self.position +=1
		self.cum_score = update_score(self.cum_score, self.last_group_level,self.group_level) 



def score(seq: str) -> int:
	state = string_state()
	for char in seq:
		state.update_state(char)
		print(f"char: {char},State Position:{state.position},Garbage Open:{state.garbage_open},ignore_next:{state.ignore_next},Group Level: {state.group_level},Score: {state.cum_score}")

	print("---\n")		

	return state.cum_score

def score_garbage(seq: str) -> int:
	state = string_state()
	for char in seq:
		state.update_state(char)
		print(f"char: {char},State Position:{state.position},Garbage Open:{state.garbage_open},ignore_next:{state.ignore_next},Group Level: {state.group_level},garbage_count: {state.garbage_count}")

	print("---\n")		

	return state.garbage_count


# PArt 1
assert score("{{{},{},{{}}}}") == 16
assert score("{}") == 1
assert score("{{{}}}") == 6
assert score("{<a>,<a>,<a>,<a>}") == 1
assert score("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
assert score("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
assert score("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3
assert score("<{!>}>")==0

# Part 2:
assert score_garbage("<>")==0
assert score_garbage("<<<<>")==3
assert score_garbage("<!!>")==0
assert score_garbage("<!!!>>")==0
assert score_garbage('<{o"i!a,<{i<a>)')==10


with open("day09.txt") as file:
	text_input = file.read()
	score(text_input)
	score_garbage(text_input)





















