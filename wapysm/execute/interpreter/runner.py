from typing import Callable, Dict, List, Optional, Tuple, Union, cast
from math import ceil, copysign, floor, trunc

from ...execute.utils import WASM_VALUE, clamp, trap, wasm_fnearest, wasm_fsqrt, wasm_iadd, wasm_iclz, wasm_ictz, wasm_idiv_signed, wasm_idiv_unsigned, wasm_imul, wasm_ipopcnt, wasm_irem_signed, wasm_ishl, wasm_ishr_signed, wasm_ishr_unsigned, wasm_isub
from ...execute.context import WasmMemoryInstance
from ...parser.structure import VALTYPE_TYPE
from ...opcode.numeric_generated import BinaryOperatorInstructionBase, ConstantInstructionBase, UnaryOperatorInstructionBase, VALID_BITS
from ...opcode import Block, InstructionBase, Nop, Unreachable


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
        # Callable[[int, int, VALID_BITS], int],
        # Callable[[float, float, VALID_BITS], float],
        # Callable[[float, int, VALID_BITS], float],
        Callable[..., Union[int, float]],  # see above for expected types
    ]
] = {
    # Integer binary operators
    'iadd': wasm_iadd,
    'isub': wasm_isub,
    'imul': wasm_imul,
    'idiv_s': wasm_idiv_signed,
    'idiv_u': wasm_idiv_unsigned,
    'irem_s': wasm_irem_signed,
    'irem_u': wasm_idiv_unsigned,
    'iand': lambda a, b, _: a & b,
    'ior': lambda a, b, _: a | b,
    'ixor': lambda a, b, _: a ^ b,

    'ishl': wasm_ishl,
    'ishr_s': wasm_ishr_signed,
    'ishr_u': wasm_ishr_unsigned,
    'irotl': lambda a, b, _: a + b,
    'irotr': lambda a, b, _: a + b,

    # Float binary operators
    'fadd': lambda a, b, _: a + b,
    'fsub': lambda a, b, _: a - b,
    'fmul': lambda a, b, _: a * b,
    'fdiv': lambda a, b, _: a / b,
    'fmin': lambda a, b, _: min(a, b),
    'fmax': lambda a, b, _: max(a, b),
    'fcopysign': lambda a, b, _: copysign(a, b),
}



def interpret_wasm_section(code: List[InstructionBase], memory: WasmMemoryInstance, label: Optional[int] = None, resulttype: List[VALTYPE_TYPE] = []) -> Tuple[WASM_VALUE, List[WASM_VALUE]]:
    stack: List[WASM_VALUE] = []
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
            stack.append((op.type, op.bits, op.value))

        # 4.4.1. Numeric Instructions
        elif isinstance(op, UnaryOperatorInstructionBase):
            operand_c1: int = cast(int, stack.pop())
            unopfunc = UNOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, unopfunc(operand_c1, op.bits)))
        elif isinstance(op, BinaryOperatorInstructionBase):
            operand_c2: int = cast(int, stack.pop())
            operand_c1 = cast(int, stack.pop())
            biopfunc = BIOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, biopfunc(operand_c1, operand_c2, op.bits)))


    return stack[-1], stack
