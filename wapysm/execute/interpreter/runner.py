from math import ceil, copysign, floor, trunc
from typing import Callable, Dict, List, Optional, Tuple, Type, Union, cast
import struct

from ...execute.context import WasmMemoryInstance
from ...execute.utils import (
    WASM_VALUE, clamp, clamp_32bit, clamp_64bit, trap, unclamp_32bit, unclamp_64bit, wasm_fnearest,
    wasm_fsqrt, wasm_i32_signed_to_i64, wasm_i32_unsigned_to_i64, wasm_i64_to_i32, wasm_iadd, wasm_iclz, wasm_ictz,
    wasm_idiv_signed, wasm_idiv_unsigned, wasm_ieq, wasm_ieqz, wasm_ige_signed, wasm_ige_unsigned, wasm_igt_signed, wasm_igt_unsigned, wasm_ile_signed, wasm_ile_unsigned, wasm_ilt_signed, wasm_ilt_unsigned,
    wasm_imul, wasm_ine, wasm_ipopcnt, wasm_irem_signed,
    wasm_irotl, wasm_irotr, wasm_ishl,
    wasm_ishr_signed, wasm_ishr_unsigned, wasm_isub)
from ...opcode import Block, InstructionBase, Nop, Unreachable
from ...opcode.numeric_generated import (
    CvtInstructionBase,
    F32Convert_i32_s,
    F32Convert_i32_u,
    F32Convert_i64_s,
    F32Convert_i64_u,
    F32Demote_f64,
    F32Reinterpret_i32,
    F64Convert_i32_s,
    F64Convert_i32_u,
    F64Convert_i64_s,
    F64Convert_i64_u,
    F64Promote_f32,
    F64Reinterpret_i64,
    I32Reinterpret_f32,
    I32Trunc_f32_s,
    I32Trunc_f32_u,
    I32Trunc_f64_s,
    I32Trunc_f64_u,
    I32Wrap_I64,
    I64Extend_i32_s,
    I64Extend_i32_u,
    I64Reinterpret_f64,
    I64Trunc_f32_s,
    I64Trunc_f32_u,
    I64Trunc_f64_s,
    I64Trunc_f64_u,
    RelOperatorInstructionBase,
    VALID_BITS,
    BinaryOperatorInstructionBase,
    ConstantInstructionBase,
    TestOperatorInstructionBase,
    UnaryOperatorInstructionBase)
from ...parser.structure import VALTYPE_TYPE

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
    'irotl': wasm_irotl,
    'irotr': wasm_irotr,

    # Float binary operators
    'fadd': lambda a, b, _: a + b,
    'fsub': lambda a, b, _: a - b,
    'fmul': lambda a, b, _: a * b,
    'fdiv': lambda a, b, _: a / b,
    'fmin': lambda a, b, _: min(a, b),
    'fmax': lambda a, b, _: max(a, b),
    'fcopysign': lambda a, b, _: copysign(a, b),
}
TESTOP_FUNC: Dict[
    str,
    Union[
        Callable[..., bool],  # see above for expected types
    ]
] = {
    # Integer binary operators
    'ieqz': wasm_ieqz,

    # Float binary operators
    # ... none.
}
RELOP_FUNC: Dict[
    str,
    Union[
        Callable[..., bool],  # see above for expected types
    ]
] = {
    # Integer relation operators
    'ieq': wasm_ieq,
    'ine': wasm_ine,
    'ilt_u': wasm_ilt_unsigned,
    'ilt_s': wasm_ilt_signed,
    'igt_u': wasm_igt_unsigned,
    'igt_s': wasm_igt_signed,
    'ile_u': wasm_ile_unsigned,
    'ile_s': wasm_ile_signed,
    'ige_u': wasm_ige_unsigned,
    'ige_s': wasm_ige_signed,

    # Float relation operators
    'feq': lambda a, b, _: a == b,
    'fne': lambda a, b, _: a != b,
    'flt': lambda a, b, _: a < b,
    'fgt': lambda a, b, _: a > b,
    'fle': lambda a, b, _: a <= b,
    'fge': lambda a, b, _: a >= b,
}
CVTOP_FUNC: Dict[
    Type[CvtInstructionBase],
    # Callable[[Union[int, float]], Union[int, float]],
    Callable[..., Union[int, float]],  # see above for expected types
] = {
    # TO CVTOP FROM
    I32Wrap_I64: wasm_i64_to_i32,  # i64 -> i32
    I64Extend_i32_u: wasm_i32_unsigned_to_i64,
    I64Extend_i32_s: wasm_i32_signed_to_i64,

    I32Trunc_f32_u: int,
    I32Trunc_f32_s: int,
    I32Trunc_f64_u: int,
    I32Trunc_f64_s: int,
    I64Trunc_f32_u: int,
    I64Trunc_f32_s: int,
    I64Trunc_f64_u: int,
    I64Trunc_f64_s: int,

    F32Demote_f64: lambda a: struct.unpack('f<', struct.pack('f<', a))[0],
    F64Promote_f32: lambda a: struct.unpack('d<', struct.pack('d<', a))[0],

    F32Convert_i32_u: lambda a: float(clamp_32bit(a)),
    F32Convert_i32_s: lambda a: float(unclamp_32bit(a)),
    F32Convert_i64_u: lambda a: float(clamp_64bit(a)),
    F32Convert_i64_s: lambda a: float(unclamp_64bit(a)),
    F64Convert_i32_u: lambda a: float(clamp_32bit(a)),
    F64Convert_i32_s: lambda a: float(unclamp_32bit(a)),
    F64Convert_i64_u: lambda a: float(clamp_64bit(a)),
    F64Convert_i64_s: lambda a: float(unclamp_64bit(a)),

    I32Reinterpret_f32: lambda a: struct.unpack('I<', struct.pack('f<', a))[0],
    I64Reinterpret_f64: lambda a: struct.unpack('L<', struct.pack('d<', a))[0],
    F32Reinterpret_i32: lambda a: struct.unpack('f<', struct.pack('I<', a))[0],
    F64Reinterpret_i64: lambda a: struct.unpack('d<', struct.pack('L<', a))[0],
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
        elif isinstance(op, TestOperatorInstructionBase):
            operand_c1 = cast(int, stack.pop())
            testopfunc = TESTOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, testopfunc(operand_c1, op.bits)))
        elif isinstance(op, RelOperatorInstructionBase):
            operand_c2 = cast(int, stack.pop())
            operand_c1 = cast(int, stack.pop())
            relopfunc = RELOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, relopfunc(operand_c1, operand_c2, op.bits)))
        elif isinstance(op, CvtInstructionBase):
            operand_c1 = cast(int, stack.pop())
            cvtopfunc = CVTOP_FUNC[type(op)]
            stack.append(clamp(op.type, op.bits, cvtopfunc(operand_c1)))


    return stack[-1], stack
