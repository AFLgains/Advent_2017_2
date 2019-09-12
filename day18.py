"""
Duet
"""

from typing import NamedTuple, Dict, List, Tuple
import time



class instruction(NamedTuple):
	type_: str
	X: str 
	Y: str

def process_instruction_str(s: str) -> Dict[int, instruction]:
	instruct_dict = {}
	for i,line in enumerate(s.split("\n")):
		output  = line.split(" ")
		Y = None
		if len(output)<3:
			register,X= output[0], output[1]
		else:
			register,X,Y= output[0], output[1],output[2]
		instruct_dict[i] = instruction(type_ = register, X = X, Y = Y)
	return instruct_dict

def transform_instruction(inst: instruction,register_dict: Dict[str,int]) -> Tuple[int,int]:

	if inst.Y:
		if inst.Y.isalpha():
			Y = int(register_dict.get(inst.Y))
		else:
			Y = int(inst.Y)
	else:
		Y = inst.Y

	if inst.X.isalpha():
		curr_val = int(register_dict.get(inst.X))
	else:
		curr_val = int(inst.X)

	return curr_val, Y

class assembly():
	def __init__(self, instruction_string: str,name: int) -> None: 

		self.instruction_dict = process_instruction_str(instruction_string)
		self.register_dict: Dict[str,int] = {} # This will store our registers and their corresponding values. We can update by using the "update" method
		for reg in self.instruction_dict.values():
			if reg.X.isalpha():
				self.register_dict.update({reg.X: 0})
		self.register_dict.update({'p':name})

		self.outbox = []
		self.inbox = []
		self.wait = False
		self.send_count = 0
		self.terminated = False

	def execute_instruction(self, n: int):
			if n >= len(self.instruction_dict):
				self.terminated = True
				return -100
			else:
				assert n >=0
				current_instruction = self.instruction_dict.get(n)
				curr_val, Y = transform_instruction(current_instruction,self.register_dict)
				next_inst = n + 1

				if current_instruction.type_ == "set":
					self.register_dict.update({current_instruction.X: Y})
				elif current_instruction.type_ == "add":
					self.register_dict.update({current_instruction.X: curr_val+Y})
				elif current_instruction.type_ == "mul":
					self.register_dict.update({current_instruction.X: curr_val*Y})
				elif current_instruction.type_ == "mod":
					self.register_dict.update({current_instruction.X: curr_val % Y})
				elif current_instruction.type_ == "jgz":
					if curr_val > 0:
						next_inst = n + Y
				elif current_instruction.type_ == "snd":
					self.outbox.append(curr_val)
					self.send_count +=1

				elif current_instruction.type_ == "rcv":
					if len(self.inbox) == 0:
						self.wait = True
						next_inst = n 
					else:
						i = self.inbox.pop(0)
						self.register_dict.update({current_instruction.X: i})
						self.wait = False
							
				else: 
					raise NotImplementedError(f"Encountered unknown instruction type {current_instruction.type_}")

				return next_inst


TEST_INPUT = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

TEST_INPUT = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

TEST_INPUT = """set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 680
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""


p0 = assembly(TEST_INPUT,0)
p1 = assembly(TEST_INPUT,1)
n0 = 0
n1 = 0 
stop = False
while not stop:
	# Update the next move
	n0 = p0.execute_instruction(n0)
	n1 = p1.execute_instruction(n1)
	print(f"n0:{n0}, n1:{n1}")


	# update the inbox
	p0.inbox = p1.outbox
	p1.inbox = p0.outbox

	#time.sleep(0.1)

	# deadlock condition
	if p1.wait == True and p0.wait == True:
		print(f"Deadlock reached")
		stop = True
		

	if p1.terminated == True and p0.terminated == True:
		print(f"Both programs terminated")
		stop = True
		
print(p1.send_count)

# def execute_instruction(n: int, 
# 					   register_dict: Dict[str,int], 
# 					   instruct_dict: Dict[int,instruction],
# 					   last_sound_played: int) -> Tuple[int,int]:
	
# 	assert n >=0
# 	current_instruction = instruct_dict.get(n)
# 	print(current_instruction)
# 	curr_val, Y = transform_instruction(current_instruction,register_dict)
# 	next_inst = n + 1

# 	if current_instruction.type_ == "set":
# 		register_dict.update({current_instruction.X: Y})
# 	elif current_instruction.type_ == "add":
# 		register_dict.update({current_instruction.X: curr_val+Y})
# 	elif current_instruction.type_ == "mul":
# 		register_dict.update({current_instruction.X: curr_val*Y})
# 	elif current_instruction.type_ == "mod":
# 		register_dict.update({current_instruction.X: curr_val % Y})
# 	elif current_instruction.type_ == "snd":
# 		print(f"Register {current_instruction.X} played sound : {curr_val}")
# 		last_sound_played = curr_val
# 	elif current_instruction.type_ == "rcv":
# 		if curr_val != 0:
# 			print(f"Recovered: {last_sound_played}")
# 			next_inst = -100
# 	elif current_instruction.type_ == "jgz":
# 		if curr_val > 0:
# 			next_inst = n + Y

# 	return next_inst, last_sound_played

# def find_first_recovered(s: str):

# 	instruction_dict = process_instruction_str(s)
# 	register_dict: Dict[str,int] = {} # This will store our registers and their corresponding values. We can update by using the "update" method
	
# 	for reg in instruction_dict.values():
# 		if reg.X.isalpha():
# 			register_dict.update({reg.X: 0})
	
# 	last_sound_played = 0 
# 	inst = 0
# 	while True:
# 		inst,last_sound_played = execute_instruction(inst, register_dict, instruction_dict, last_sound_played)
# 		if inst == -100:
# 			break
# 	print(last_sound_played)





#find_first_recovered(TEST_INPUT)



