"""
Dancing programs
"""

from typing import NamedTuple, Dict, List

class dance_move(NamedTuple):
	dance_type: str
	subjects: str


def process_instructions(s: str) -> Dict[int,dance_move]:
	instruction = {}
	for i,dance in enumerate(s.split(",")):
		instruction[i] = dance_move(dance_type = dance[0], subjects =dance[1:])
	return instruction

def apply_move(dance: dance_move, program_line: List[str]):

	program_line = program_line[:]

	if dance.dance_type == 's':
		n = int(dance.subjects)
		l2 = program_line[:-n]
		program_line = program_line[-n:]
		program_line.extend(l2)

	elif dance.dance_type == "x":
		
		# Swap the two positions
		pos1,pos2 = list(map(int,dance.subjects.split("/"))) 
		program_line[pos1], program_line[pos2] = program_line[pos2], program_line[pos1] 

	elif dance.dance_type == "p":

		pos1_name,pos2_name = dance.subjects.split("/")
		pos1 = program_line.index(pos1_name)
		pos2 = program_line.index(pos2_name)
		program_line[pos1], program_line[pos2] = program_line[pos2], program_line[pos1] 

	else:
		raise NotImplementedError(f"Unown instruction {dance.dance_type}")

	return program_line

def apply_n_moves(moves:str,program_input:List[str],n:int = 1) -> List[str]:
	
	move_dict = process_instructions(moves)
	history_dict = {}

	for i in range(n):
		if history_dict.get("".join(program_input)):
			program_input = [c for c in history_dict.get("".join(program_input))]
		else:
			input_ = program_input
			for move in move_dict.keys():
				program_input = apply_move(move_dict.get(move), program_input)
			history_dict["".join(input_)] = "".join(program_input)
	return "".join(program_input)	

def get_full_dict(moves:str,program_input:List[str]) -> Dict[str,str]:
	
	move_dict = process_instructions(moves)
	history_dict = {}
	original_input = program_input

	while True:
		if history_dict.get("".join(program_input)):
			program_input = [c for c in history_dict.get("".join(program_input))]
		else:
			input_ = program_input
			for move in move_dict.keys():
				program_input = apply_move(move_dict.get(move), program_input)
			history_dict["".join(input_)] = "".join(program_input)
			if program_input == original_input:
				break

	return history_dict

def find_nth_lineup(history_dict: Dict[str,str], n: int) -> str:
	N = n % len(history_dict)
	return list(history_dict.values())[N-1]


# TEST_INPUT = """s1,x3/4,pe/b"""
# PROGRAM_INPUT = ['a','b','c','d','e']
# full_dict = get_full_dict(TEST_INPUT, PROGRAM_INPUT)
# for u in range(1,6):
# 	assert find_nth_lineup(full_dict,u) == apply_n_moves(TEST_INPUT,PROGRAM_INPUT,n = u)

PROGRAM_INPUT = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

with open("day16_input.txt") as f:
	DANCE_MOVE_INPUT = f.read()
	full_dict = get_full_dict(DANCE_MOVE_INPUT, PROGRAM_INPUT)
	print(find_nth_lineup(full_dict,1000000000))

