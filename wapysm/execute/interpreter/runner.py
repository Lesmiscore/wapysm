from typing import List, Optional, Tuple
from ...execute.context import WasmMemoryInstance
from ...parser.structure import VALTYPE_TYPE
from ...opcode.numeric_generated import ConstantInstructionBase, UnaryOperatorInstructionBase
from ...opcode import Block, InstructionBase, Nop, Unreachable


I_OR_F = {
    'i': int,
    'f': float,
}

def interpret_wasm_section(code: List[InstructionBase], memory: WasmMemoryInstance, label: Optional[int] = None, resulttype: List[VALTYPE_TYPE] = []) -> Tuple[object, List[object]]:
    stack: List[object] = []
    idx: int = 0

    while idx < len(code):
        op = code[idx]
        idx += 1

        # Control Instructions
        if isinstance(op, Nop):
            continue  # do nothing
        elif isinstance(op, Unreachable):
            raise Exception('trapped: ')
        elif isinstance(op, Block):
            stack.append(interpret_wasm_section(op.instr, memory, 0, op.resultype)[0])
        # TODO: not yet completed

        # Constant Instruction
        elif isinstance(op, ConstantInstructionBase):
            stack.append(op.value)

        # 4.4.1. Numeric Instructions
        elif isinstance(op, UnaryOperatorInstructionBase):
            operand_c1 = stack.pop()
            operand_c1
            op.op


    return None, stack
