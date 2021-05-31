from typing import Tuple
from ..opcode import InstructionBase


class WasmTrappedException(Exception):
    def __init__(self, msg: str, op: InstructionBase, *operands: object) -> None:
        super().__init__(msg)
        self.op: InstructionBase = op
        self.operands: Tuple[object, ...] = operands


def trap(op, *operands):
    raise WasmTrappedException('trapped: %s' % repr(op), op, *operands)
