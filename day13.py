"""
Packet scanners

We will solve this by creating a state of the firewall and then 
incrementing that state forward based on the last state
"""

from typing import Dict, List, NamedTuple, Tuple



class firewall_layer():
	def __init__(self,depth: int, range: int):
		self.depth = depth
		self.range = range
		self.scanner_pos = 0
		self.direction = 1 # 1 = down, 0 = up

	def step(self):
		if self.scanner_pos == self.range-1:
			self.direction = 0 
		elif self.scanner_pos == 0:
			self.direction = 1
		
		if self.direction == 1:
			self.scanner_pos +=1
		else: 
			self.scanner_pos -=1

class firewall():
	def __init__(self):
		self.layers: Dict[firewall_layer]  = list() 

	def layer_add(self, layer: firewall_layer):
		self.layers.append(layer)

	def increment(self):
		for l in self.layers:
			l.step()

	def severity(self, packet_position):
		for l in self.layers:
			if l.depth == packet_position and l.scanner_pos==0:
				return 1
		return 0




class packet():
	def __init__(self):
		self.position: int = -1


def process_layer(layer: str) -> firewall_layer:
	tmp = list(map(int,layer.split(": ")))
	return firewall_layer(depth = tmp[0],range = tmp[1])

def process_input(firewall_string: str) -> firewall:
	"""
	Create a firewall objecty
	"""
	my_firewall = firewall() 
	for layer_str in firewall_string.split("\n"):
		print(layer_str)
		my_firewall.layer_add(process_layer(layer_str))

	return my_firewall	


def step_packet(pack: packet, fw: firewall, sev: int, is_delay: int = True ) -> int:
	"""
	Move the packet, through the firewall and 
	calculate the severity (if any)
	Steps consist of moving the packet first, then the scanner
	If the packet moves into the scanner before it moves, then you
	are caught, otherwise not caught.
	Therefore, you calculate the severity after the packet moves
	but before we increment the firewall state
	"""
	if not is_delay:
		pack.position +=1
		sev += fw.severity(pack.position)

	fw.increment()

	#print(f"Packet position: {pack.position}, Severity: {sev}")
	#print({l.depth: l.scanner_pos for l in fw.layers})
	#print({l.depth: l.direction for l in fw.layers})
		

	return sev

def firewall_severity(fw: firewall, delay:int = 0, scanner_states: List[Dict] = [] ):
	"""
	The delay delays the packet entering into the firewall until a certain time
	"""

	mypacket = packet()
	severity = 0 
	max_depth = max([layer.depth for layer in fw.layers])
	counter = 0

	if scanner_states:
		for l in fw.layers:
			l.scanner_pos = scanner_states[0][l.depth]
			l.direction = scanner_states[1][l.depth]

	state_after_delay = scanner_states
	if delay > 0:
		for i in range(delay):
			_ = step_packet(mypacket, fw, severity,True) 
		
		state_after_delay = [{l.depth: l.scanner_pos for l in fw.layers},{l.depth: l.direction for l in fw.layers}]



	while True:
		severity = step_packet(mypacket, fw, severity,False)
		if mypacket.position >= max_depth:
			break
		counter += 1

	return severity, state_after_delay


FIREWALL = """0: 3
1: 2
2: 4
4: 4
6: 5
8: 8
10: 6
12: 6
14: 8
16: 6
18: 6
20: 8
22: 12
24: 8
26: 8
28: 12
30: 8
32: 12
34: 9
36: 14
38: 12
40: 12
42: 12
44: 14
46: 14
48: 10
50: 14
52: 12
54: 14
56: 12
58: 17
60: 10
64: 14
66: 14
68: 12
70: 12
72: 18
74: 14
78: 14
82: 14
84: 24
86: 14
94: 14"""
fw  = process_input(FIREWALL)

delay = 0
while True:
	if all([(delay+ 2*(l.range-1)+l.depth) % (2*(l.range-1)) != 0 for l in fw.layers]):
		break
	else:
		delay += 1389

	if delay % 1000 == 0:
		print(delay)


def position_after_n_steps(n_steps: int, layer_range: int) -> int:

	if (n_steps // layer_range) % 2 == 0: # If it's even, then on the way back
		return (layer_range ) - n_steps%layer_range -1
	else:
		return n_steps%layer_range -1

# 2*(x-1) - pos

# (2) 2,4,6,8
# (3) 4,8,12,16
# (14 in the 94th position ) 2*13 - 94 + 26*x = delay where delay is an integer > 0  
# -68+26*x = delay
# x = (delay+68) % 26 == 0 




#assert firewall_severity(fw,delay = 10)[0] == 0 
#fw  = process_input(TEST_FIREWALL)
#assert firewall_severity(fw,delay = 0)[0] == 24 


#fw  = process_input(TEST_FIREWALL)
#_, state_after_10  = firewall_severity(fw,delay = 10)

#fw  = process_input(TEST_FIREWALL)
#score, _  = firewall_severity(fw,delay = 0,scanner_states = state_after_10)
#print(score)

# with open("day13_input.txt") as f:
	
# 	FIREWALL = f.read()

# 	#FIREWALL = TEST_FIREWALL

# 	print(FIREWALL)


# 	print(delay)




