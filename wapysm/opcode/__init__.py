# 2.4 Instructions
# This defines structure of all instructions,
# and not responsible for parsing binaries or texts.

from typing import List
from ..parser.structure import VALTYPE_TYPE


class InstructionBase(object):
    _debug_internal_index = 0

    def __repr__(self) -> str:
        exclude_names = ('instr', 'else_block', '_debug_internal_index')
        ddr = self.__dict__
        ddr = dict((k, v) for k, v in ddr.items() if not (k.startswith('__') or k in exclude_names))
        return f'{type(self).__name__}: {repr(ddr)}' if ddr else super().__repr__()

# 2.4.1 Numeric Instructions

# See /opcode_autogen.py and ./numeric_generated.py

# 2.4.2 Parametric Instructions

class DropInstruction(InstructionBase):
    pass

class SelectInstruction(InstructionBase):
    pass

# 2.4.3 Variable Instructions

class VariableInstructionBase(InstructionBase):
    index: int = 0

class LocalGetInstruction(VariableInstructionBase):
    pass

class LocalSetInstruction(VariableInstructionBase):
    pass

class LocalTeeInstruction(VariableInstructionBase):
    pass

class GlobalGetInstruction(VariableInstructionBase):
    pass

class GlobalSetInstruction(VariableInstructionBase):
    pass

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

class Br(BranchInstructionBase):
    "br"

class BrIf(BranchInstructionBase):
    "br_if"

class BrTable(InstructionBase):
    "br_table"
    labelindices: List[int] = []
    lastlabel: int = 0

class Return(InstructionBase):
    "return"


class CallInstructionBase(BranchInstructionBase):
    pass

class Call(CallInstructionBase):
    "call"
    callidx: int = 0

class CallIndirect(CallInstructionBase):
    "call_indirect"
    typeidx: int = 0
