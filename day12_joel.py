"""
Digital plumber
===============
Joel's approach is to use a graph search
"""

from typing import List, Tuple, Dict, Set

def process_line(line: str) -> Tuple[int,List[int]]:


	parts = line.strip().split(" <-> ")
	base = parts[0]
	children = parts[1].strip().split(", ")

	return(int(base), list(map(int,children)))


def build_graph(lines: List[str]) -> Dict[int,List[int]]:
	graph: Dict[int,Listp[int]] = {}
	for line in lines:
		source, targets = process_line(line)
		graph[source] = targets
	return graph


def reachable_from(graph: Dict[int, List[int]],source: int = 0 ) -> Set[int]:
	frontier = [source]
	reachable: Set[int] = set()

	while frontier:
		program = frontier.pop() # get the last and pop off  
		reachable.add(program)
		for next_program in graph.get(program,[]):
			if next_program not in reachable:
				frontier.append(next_program)


	return reachable

TEST_INPUT = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

TEST_GRAPH = build_graph(TEST_INPUT.split("\n"))
print(reachable_from(TEST_GRAPH))


def num_groups(graph: Dict[int,List[int]]):
	num_groups = 0

	seen: Set[int] =  set()

	# Go through the nodes in the graph
	for source in graph:
		print(source, source in seen)
		if source not in seen:
			group = reachable_from(graph, source)
			seen = seen | group
			num_groups += 1

	return(num_groups)
print(num_groups(TEST_GRAPH))



