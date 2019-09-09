"""
Registers
""" 


TEST_INPUT = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

from typing import NamedTuple, List, Dict
from collections import defaultdict
import re

class Condition(NamedTuple):
	register: str
	comparison: str
	target: int

class Instruction(NamedTuple):
	register: str
	operation: str
	amount: int 
	condition: Condition

def parse_instruction(raw: str) -> Instruction:
	inst, cond = raw.split(" if ")
	if " inc " in inst:
		register, amount = inst.split(" inc ")
		operation = "inc"
	elif " dec " in inst:
		register, amount = inst.split(" dec ")
		operation = "dec"
	else:
		raise ValueError(f"cannot parse {inst}")

	op_rgx = "(==|!=|>=|<=|<|>)"
	cond_register, op,  cond_target = re.split(op_rgx, cond)

	return Instruction(register = register.strip(), 
						operation = operation,
						amount = int(amount),
						condition = Condition(register = cond_register.strip(),
												comparison = op,
												target = int(cond_target) ))



def meets_condition(condition: Condition, registers: Dict[str,int]) -> bool:
	value = registers.get(condition.register,0) # get the current value of the register
	target = condition.target
	op = condition.comparison

	if op == "==":
		return target == value
	elif op == "!=":
		return value != target
	elif op == "<":
		return value < target
	elif op == ">":
		return value > target
	elif op == "<=":
		return value <= target
	elif op == ">=":
		return value >= target
	else:
		raise ValueError(f"Unknown operation string {op}")



def process_instruction(instruction: Instruction, registers: Dict[str,int]) -> Dict[str,int]:
	condition = instruction.condition
	if meets_condition(condition, registers):
		register = instruction.register
		op = instruction.operation
		amount = instruction.amount
		value = registers.get(register,0) # 0 is the default incase it doesn't exist

		if op == "inc":
			registers[register] = value + amount
		elif op == "dec":
			registers[register] = value - amount 
		else:
			raise ValueError(f"Unknown operation {op}")

	return registers

def process_instructions(instructions: List[Instruction]) -> Tuple(Dict[str,int],int):

	registers: Dict[str,int] = {}
	high = 0 
	for instruction in instructions: 
		registers = process_instruction(instruction,registers)
		if len(registers)>0:
			high = max(max(registers.values()),high)
			print(high)
	return registers,high


TEST_INSTRUCTIONS = [parse_instruction(line) for line in TEST_INPUT.split("\n")]

print(process_instructions(TEST_INSTRUCTIONS))
t, high= process_instructions(TEST_INSTRUCTIONS)

print([(i,j) for i,j in t.items() if t[i] == max(t.values())])


print(high)