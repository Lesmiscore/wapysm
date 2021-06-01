from typing import Callable, Dict, List, Optional, Tuple, Union, cast
from math import ceil, floor, trunc

from ...execute.utils import trap, wasm_fnearest, wasm_fsqrt, wasm_iclz, wasm_ictz, wasm_ipopcnt
from ...execute.context import WasmMemoryInstance
from ...parser.structure import VALTYPE_TYPE
from ...opcode.numeric_generated import BinaryOperatorInstructionBase, ConstantInstructionBase, UnaryOperatorInstructionBase, VALID_BITS
from ...opcode import Block, InstructionBase, Nop, Unreachable


I_OR_F = {
    'i': int,
    'f': float,
}

UNOP_FUNC: Dict[
    str,
    Union[
        Callable[[int, VALID_BITS], int],
        Callable[[float, VALID_BITS], float],
        Callable[[Union[int, float], VALID_BITS], Union[int, float]],
    ]
] = {
    # Integer unary operators
    'iclz': wasm_iclz,
    'ictz': wasm_ictz,
    'ipopcnt': wasm_ipopcnt,

    # Float unary operators
    'fabs': lambda x, _: abs(x),
    'fneg': lambda x, _: -x,
    'fsqrt': wasm_fsqrt,
    'fceil': lambda x, _: ceil(x),
    'ffloor': lambda x, _: floor(x),
    'ftrunc': lambda x, _: trunc(x),
    'fnearest': wasm_fnearest,
}
BIOP_FUNC: Dict[
    str,
    Union[
        Callable[[int, int, VALID_BITS], int],
        Callable[[float, float, VALID_BITS], float],
        Callable[[float, int, VALID_BITS], float],
        # Callable[[Union[int, float], Union[int, float], VALID_BITS], Union[int, float]],
    ]
] = {}

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
            trap(op)
        elif isinstance(op, Block):
            stack.append(interpret_wasm_section(op.instr, memory, 0, op.resultype)[0])
        # TODO: not yet completed

        # Constant Instruction
        elif isinstance(op, ConstantInstructionBase):
            stack.append(op.value)

        # 4.4.1. Numeric Instructions
        elif isinstance(op, UnaryOperatorInstructionBase):
            operand_c1: int = cast(int, stack.pop())
            unopfunc = UNOP_FUNC[f'{op.type}{op.op}']
            stack.append(unopfunc(operand_c1, op.bits))
        elif isinstance(op, BinaryOperatorInstructionBase):
            operand_c2: int = cast(int, stack.pop())
            operand_c1 = cast(int, stack.pop())
            biopfunc = BIOP_FUNC[f'{op.type}{op.op}']
            stack.append(biopfunc(operand_c1, operand_c2, op.bits))


    return None, stack
