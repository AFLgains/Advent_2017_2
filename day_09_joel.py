"""
Joel's Answer to question 9
"""

from typing import NamedTuple

class StreamMetrics(NamedTuple):
	score: int
	garbage: int

def score(stream: str) -> int:
	total_score = 0 
	depth = 0
	in_garbage = False
	negated = False

	garbage_count = 0 

	for c in stream:
		print(c, total_score, depth, in_garbage, negated)
		if negated: 
			negated = False
		elif c == "!":
			negated = True
		elif in_garbage:
			if c == ">":
				in_garbage = False
			else:
				garbage_count+=1
		elif c == "<":
			in_garbage=True
		elif c == "{":
			depth +=1
			total_score += depth
		elif c == "}":
			depth -=1

	return StreamMetrics(total_score, garbage_count)


# assert score("{}")==1
# assert score("{{{},{},{{}}}}") == 16
# assert score("{}") == 1
# assert score("{{{}}}") == 6
# assert score("{<a>,<a>,<a>,<a>}") == 1
# assert score("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
# assert score("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
assert score("{{<a!>},{<a!>},{<a!>},{<ab>}}").score == 3
#assert score("<{!>}>")==0

assert score("<>").garbage==0
assert score("<<<<>").garbage==3
assert score("<!!>").garbage==0
assert score("<!!!>>").garbage==0
assert score('<{o"i!a,<{i<a>)').garbage==10

with open("day09.txt") as file:
	text_input = file.read()
	print(score(text_input).score)
	print(score(text_input).garbage)
