"""
Joel's answer to number 11.
He did it through eliminating steps (scales better)

i.e., 
	n + s = 0 
	nw + se = 0 
	ne + sw = 0 
	sw + se = s
	nw + ne = n

what happens is you can boil it down to two adjacent directions
"""

from typing import NamedTuple, List, Dict
from collections import defaultdict
from copy import copy

def eliminate_opposites(count: Dict[str,int]) -> bool:
	eliminated = False
	n_s = min(counts['n'],counts['s'])
	ne_sw = min(counts['ne'],counts['sw'])
	nw_se = min(counts['nw'],counts['se'])

	if n_s >0 or ne_sw >0 or nw_se >0:
		counts['n']  -= n_s
		counts['s']  -= n_s
		counts['ne'] -= ne_sw
		counts['sw'] -= ne_sw
		counts['nw'] -= nw_se
		counts['se'] -= nw_se
		return True
	else:
		return False

def _condense(counts: Dict[str,int],minus1: str, minus2:str, plus: str) -> bool:
	"""
	n+se = ne etc,...
	"""
	eliminate = min(counts[minus1],counts[minus2])
	if eliminate > 0:
		counts[minus1] -= eliminate
		counts[minus2] -= eliminate
		counts[plus] += eliminate
		return True
	else:
		return False

def condense(counts: Dict[str,int]) -> bool:
	condensed = False
	for m1, m2, p in [
		('n','se','ne'),
		('ne','s','se'),
		('se','sw','s'),
		('s','nw','sw'),
		('sw','n','nw'),
		('nw','ne','n')]:
		condensed = condensed or _condense(counts,m1,m2,p)

def total(counts: Dict[str,int]) -> int:
	counts_ = copy(counts) # copy

	while True: 
		if not eliminate_opposites(counts_) and not condense(counts_):
			break

	print(counts_)
	return(sum(counts_.values()))



with open("day11.txt") as f:
	INPUT_TEXT = f.read().rstrip('\n\r').split(",")

	counts: Dict[str,int] = defaultdict(int)



	max_dist = float('-inf')
	for move in INPUT_TEXT:
		counts[move] += 1
		dist = total(counts)
		dist = total(counts)
		if dist > max_dist:
		 	max_dist = dist
		print(f"{move} dist = {dist}, max_dist = {max_dist}")

	#print(distance(counts))

	#print(distance(counts))



