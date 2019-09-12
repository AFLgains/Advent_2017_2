"""
Day 18 - Joel:
"""
from typing import List, NamedTuple, Dict
from collections import defaultdict, deque

# A defaul dict works like a normal dict, but you can initialise it with defaul values for unseen keys


class Instruction(NamedTuple):
	op: str
	args: List[str]

Program = List[Instruction]

class State:
	def __init__(self,program_id: int) -> None:
		self.register: Dict[str,int] = defaultdict(int)
		self.register['p'] = program_id
		self.queue: deque = deque()
		self.other_state: 'State' = None
		self.pos = 0
		self.sent_a_value = 0

	def enqueue(self, value: int) -> None:
		self.queue.append(value)

	def dequeue(self) -> int:
		if self.queue:
			return self.queue.popleft()
		else:
			return None

	def get(self, name_or_value: str) -> int:
		try:
			return int(name_or_value)
		except ValueError:
			return self.register[name_or_value] 


def step(program: Program, state: State) -> bool:

	instruction = program[state.pos]
	op = instruction.op
	args = instruction.args

	if op == "rcv":
		# Get the value out of the queue
		register, = args
		value = state.dequeue()
		if value == None:
			return False
		else:
			state.register[register] = value
			state.pos +=1 
			return True
	elif op == "snd":
		# set last note to the value
		value = state.get(args[0])
		state.other_state.enqueue(state.get(name_or_value))
		state.sent_a_value += 1
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
	elif instruction.op == "jgz":
		x,y = instruction.args
		if state.get(x) > 0:
			state.pos += state.get(y)
			return True
	else:
		raise ValueError(f"Uknown op: {op}")
	state.pos += 1
	return True

def run(program: Program) -> int:
	"""
	Return the recovered frequency
	"""
	state0 = State(program_id = 0)
	state1 = State(program_id = 1)

	state0.other_state = state1
	state1.other_state = state0

	while True:
		step1 = step(program, state1)
		step0 = step(program, state0)	

		if not step1 and not step0:
			# deadlock
			print("deadlock")
			return state1.sent_a_value


def parse(raw: str) -> Program:
	lines = raw.split("\n")
	fields = [line.split() for line in lines]
	return [Instruction(op = field[0],args =field[1:]) for field in fields]

class Copy:
	def __init__(self, program: Program,program_id:int) -> None:
		self.state = State()

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