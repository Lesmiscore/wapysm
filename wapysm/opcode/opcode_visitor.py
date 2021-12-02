from typing import List, Union
from . import BlockInstructionBase, IfElse, InstructionBase

def walk_topdown(op: Union[InstructionBase, List[InstructionBase]]):
    if isinstance(op, list):
        for i in op:
            yield from walk_topdown(i)
        return

    yield op

    if isinstance(op, IfElse):
        for i in op.instr:
            yield from walk_topdown(i)
        for i in op.else_block:
            yield from walk_topdown(i)
    elif isinstance(op, BlockInstructionBase):
        for i in op.instr:
            yield from walk_topdown(i)


def walk_bottomup(op: Union[InstructionBase, List[InstructionBase]]):
    if isinstance(op, list):
        for i in op:
            yield from walk_bottomup(i)
        return

    if isinstance(op, IfElse):
        for i in op.instr:
            yield from walk_bottomup(i)
        for i in op.else_block:
            yield from walk_bottomup(i)
    elif isinstance(op, BlockInstructionBase):
        for i in op.instr:
            yield from walk_bottomup(i)
    yield op
