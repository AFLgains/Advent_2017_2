"""
Day 19:
A series of tubes
"""
from typing import List, Dict, NamedTuple, Tuple
from collections import defaultdict

def parse_maze(s: str) -> Dict[int, List[str]]:
	dot_input = [line.replace(" ",".") for line in s.split("\n")]
	assert all([len(d) == len(dot_input[0]) for d in dot_input]) == True
	return {i: [j.replace(".","") for j in dot] for i,dot in enumerate(dot_input)}

class Packet(NamedTuple):
	direction: str # up, down, left, right
	letters: List[str] = []
	row:int =0
	col:int = 0

def maze_step(packet: Packet, maze: Dict[int, List[str]],direction_register: Dict[str,int]) -> Tuple[Packet,bool]:
	
	terminate: bool = False
	row: int = packet.row
	col: int = packet.col
	direction: str = packet.direction
	letters: List[str] = packet.letters
	cur_symbol = maze.get(row)[col]
	print(packet)

	next_direction = direction # in generatl, the next direction will be the same as the current direction
	if cur_symbol == "|": 
		if direction == "up":
			next_row = row-1
			next_col = col
		elif direction == "down":
			next_row = row+1
			next_col = col
		elif direction == "right":
			next_row = row
			next_col = col+1
		elif direction == "left":
			next_row = row
			next_col = col-1
		else: 
			raise ValueError(f"Unknown Direction {direction}")
	elif cur_symbol == "-": 
		if direction == "right":
			next_row = row
			next_col = col+1
		elif direction == "left":
			next_row = row
			next_col = col-1
		elif direction == "up":
			next_row = row-1
			next_col = col
		elif direction == "down":
			next_row = row+1
			next_col = col
		else: 
			raise ValueError(f"Unknown Direction {direction}")
	elif cur_symbol == "+":
		if direction == "down" or direction == "up":
			next_row = row
			if col == 0:
				next_col = col + 1
				next_direction = "right"
			elif maze.get(next_row)[col-1] == "":
				next_col = col + 1
				next_direction = "right"
			else:
				next_col = col - 1
				next_direction = "left"
		else:
			next_col = col
			if row == 0:
				next_row = row + 1
				next_direction = "down"
			if maze.get(row-1)[next_col] == "":
				next_row = row + 1
				next_direction = "down"
			else:
				next_row = row - 1
				next_direction = "up"

	elif cur_symbol.isalpha():
		
		letters.append(cur_symbol)
		next_direction = direction

		if direction == "up":
			next_col = col
			next_row = row - 1
		elif direction == "down":
			next_col = col
			next_row = row + 1
		elif direction == "left":
			next_col = col-1
			next_row = row
		elif direction == "right":
			next_col = col+1
			next_row = row
		else:
			raise ValueError(f"Unknown direction {direction}")
	elif cur_symbol == "":
		terminate = True
		return packet, terminate

	else:
		raise ValueError(f"Unknown synmbol encountered {cur_symbol}")

	# termination conditions
	if next_col < 0 or next_col >= len(maze.get(0)) or next_row <0 or next_row > max(maze.keys()):
		terminate = True

	direction_register[direction] +=1
	packet = Packet(row =next_row,col = next_col, direction = next_direction, letters = letters)
	
	return packet, terminate



def traverse_maze(maze_string:str) -> List[str]:
	direction_register = defaultdict(int)
	Maze = parse_maze(maze_string)
	initial_col = Maze.get(0).index("|")
	P = Packet(direction = "down",col = initial_col)
	while True:
		P,terminate = maze_step(P, Maze,direction_register)
		if terminate:
			print(direction_register)
			print(sum(direction_register.values()))
			return "".join(P.letters)


MAZE_INPUT = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """

with open("day19_input.txt") as f:
	MAZE_INPUT = f.read()

if __name__ == "__main__":
	print(traverse_maze(MAZE_INPUT))
