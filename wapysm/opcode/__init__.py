# 2.4 Instructions
# This defines structure of all instructions,
# and not responsible for parsing binaries or texts.

from typing import List
from wapysm.parser.structure import VALTYPE_TYPE


class InstructionBase(object):
    pass

# 2.4.1 Numeric Instructions

# See /opcode_autogen.py and ./numeric_generated.py

# 2.4.2 Parametric Instructions

class DropInstruction(InstructionBase):
    pass

class SelectInstruction(InstructionBase):
    pass

# 2.4.3 Variable Instructions

class LocalGetInstruction(InstructionBase):
    localidx: int = 0

class LocalSetInstruction(InstructionBase):
    localidx: int = 0

class LocalTeeInstruction(InstructionBase):
    localidx: int = 0

class GlobalGetInstruction(InstructionBase):
    localidx: int = 0

class GlobalSetInstruction(InstructionBase):
    localidx: int = 0

# 2.4.4 Memory Instructions

# See /opcode_autogen.py and ./memory_generated.py

# 2.4.5 Control Instructions

class Unreachable(InstructionBase):
    "unreachable"

class Nop(InstructionBase):
    "nop"

class BlockInstructionBase(InstructionBase):
    resultype: List[VALTYPE_TYPE] = []
    instr: List[InstructionBase] = []

class Block(BlockInstructionBase):
    "block"

class Loop(BlockInstructionBase):
    "loop"

class IfElse(BlockInstructionBase):
    "if_else"
    else_block: List[InstructionBase] = []


class BranchInstructionBase(InstructionBase):
    labelidx: int = 0

class Br(BlockInstructionBase):
    "br"

class BrIf(BlockInstructionBase):
    "br_if"

class BrTable(BlockInstructionBase):
    "br_table"
    labelindices: List[int] = []

class Return(BlockInstructionBase):
    "return"


class CallInstructionBase(BranchInstructionBase):
    pass

class Call(CallInstructionBase):
    "call"
    callidx: int = 0

class CallIndirect(CallInstructionBase):
    "call_indirect"
    typeidx: int = 0
