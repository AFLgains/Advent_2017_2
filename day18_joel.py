"""
Day 18 - Joel:
"""
from typing import List, NamedTuple, Union
from collections import defaultdict

# A defaul dict works like a normal dict, but you can initialise it with defaul values for unseen keys


class Instruction(NamedTuple):
	op: str
	args: List[str]

Program = List[Instruction]

class State:
	def __init__(self) -> None:
		self.register: Dict[str,int] = defaultdict(int)
		self.last_note: int = None
		self.current_instruction = 0 

	def get(self, name_or_value: str) -> int:
		try:
			return int(name_or_value)
		except ValueError:
			return self.register[name_or_value] 


def apply(instruction: Instruction, state: State) -> None:
	op = instruction.op
	args = instruction.args

	if op == "snd":
		# set last note to the value
		value = state.get(args[0])
		state.last_note = value
	elif op == "set":
		state.register[args[0]] = state.get(args[1])
	elif op == "add":
		register,name_or_value = args
		state.register[register] += state.get(name_or_value)
	elif op == "mul":
		register,name_or_value = args
		state.register[register] *=state.get(name_or_value)
	elif op == "mod":
		register,name_or_value = args
		state.register[register] = state.register[register] % state.get(name_or_value)
	else:
		raise ValueError(f"Uknown op: {op}")



def run(program: Program) -> int:
	"""
	Return the recovered frequency
	"""
	state = State()
	pos = 0 

	while True:
		instruction = program[pos]
		print(pos,instruction)
		print(state.__dict__)

		if instruction.op == "rcv":
			value = state.get(instruction.args[0])
			if value !=0:
				return state.last_note
			else:
				pos +=1
		elif instruction.op == "jgz":
			x,y = instruction.args
			if state.get(x) > 0:
				pos += state.get(y)
			else:
				pos +=1
		else:
			apply(instruction,state)
			pos += 1

		if pos <0 or pos > len(program):
			raise RuntimeError(f"terminated")

def parse(raw: str) -> Program:
	lines = raw.split("\n")
	fields = [line.split() for line in lines]
	return [Instruction(op = field[0],args =field[1:]) for field in fields]

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

TEST_INSTRUCTIONS = parse(TEST_INPUT)
print(run(TEST_INSTRUCTIONS))