"""
Hex Grid
"""

from typing import NamedTuple
from numpy import abs

class hex(NamedTuple):
	"""
	We will be using cubic coordinates
	+x = n-s
	+y = ne-sw
	+z = se-nw
	"""
	x: int = 0
	y: int = 0
	z: int = 0


def hex_distance(hex_1: hex, hex_2: hex) -> int:
	"""
	Give you the mimum distance between two hex at location
	hex_1 and hex_2
	"""
	return (abs(hex_1.x - hex_2.x) + abs(hex_1.y - hex_2.y) + abs(hex_1.z - hex_2.z)) / 2 

def step(hex_input: hex,direction: str) -> hex:
	x = hex_input.x
	y = hex_input.y
	z = hex_input.z

	if direction == "n":
		y+=1
		z-=1
	elif direction == "s":
		y-=1
		z+=1
	elif direction == "se":
		x+=1
		y-=1
	elif direction == "nw":
		x-=1
		y+=1
	elif direction == "ne":
		x+=1
		z-=1
	elif direction == "sw":
		x-=1
		z+=1
	else:
		raise ValueError(f"Unrecognised Direction {direction}")

	return(hex(x,y,z))

def find_steps(instructions:str) -> int:

	pos = hex()
	max_dist = float('-inf')
	for direction in instructions.split(","):
		pos = step(pos,direction)
		if hex_distance(hex(),pos) > max_dist:
			max_dist = hex_distance(hex(),pos)
	print(max_dist)
	return(hex_distance(hex(),pos))


# Unit tests
assert find_steps("ne,ne,ne")== 3
assert find_steps("ne,ne,sw,sw") == 0 
assert find_steps("ne,ne,s,s") == 2
assert find_steps("se,sw,se,sw,sw") == 3

with open("day11.txt") as f:
	INPUT_TEXT = f.read().rstrip('\n\r')
	print(find_steps(INPUT_TEXT))



