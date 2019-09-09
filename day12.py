"""
Digital Plumber
"""

from typing import NamedTuple, Dict, List
from copy import copy

class pipe(NamedTuple):
	base: int
	children: List[int]

class program():
	pass


def process_line(line: str) -> pipe:
	parts = line.strip().split(" <-> ")
	base = parts[0]
	children = parts[1].strip().split(", ")

	return(pipe(base = int(base), children= list(map(int,children)) ))


def process_lines(str_input: str) -> Dict:
	all_pipes = {}
	for line in str_input.split("\n"):
		pipe = process_line(line)
		all_pipes[pipe.base] = pipe

	return all_pipes


def check_pipe(input_pipe: pipe, connection_dict: Dict, known_connections = set({0})) -> List:	
	
	for j in input_pipe.children:
		if j not in known_connections:
			known_connections.add(j)
			check_pipe(connection_dict[j],connection_dict,known_connections)


	return(known_connections)

def find_all_connections(str_input: str,pipe_no: int) -> List:
	"""
	Returns a list of all connections
	"""
	all_pipes = process_lines(str_input)
	connections = check_pipe(all_pipes[pipe_no],all_pipes,set({0}))

	return(connections)

def find_n_groups(str_input: str) -> int:

	n_pipes = len(process_lines(str_input))
	grp = list()
	for i in range(n_pipes):
		con = list(find_all_connections(str_input,i))
		print(f"{i}: {len(con)}")
		
		if i == 0:
			grp.append(con)
		elif not any([all([i in j for i in con]) for j in grp]):
			grp.append(con)	

	return (grp)




STR_INPUT = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
# assert len(find_all_connections(STR_INPUT,0)) == 6 
# print(find_n_groups(STR_INPUT))


with open("day12_input.txt") as f:	
	INPUT = f.read().rstrip('\n\r')
	groups = find_n_groups(INPUT)
	print(len(groups))
# 	print(con)
# 	print(len(con))



