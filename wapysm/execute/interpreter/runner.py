import struct
from math import ceil, copysign, floor, trunc
from typing import Callable, Dict, List, Optional, Tuple, Type, Union, cast
from wapysm.parser.module import WasmModule

from ...execute.context import WasmHostFunctionInstance, WasmLocalFunctionInstance, WasmMemoryInstance, WasmStore
from ...execute.utils import (
    WASM_VALUE, clamp, clamp_32bit, clamp_64bit,
    trap, unclamp_32bit, unclamp_64bit,
    wasm_fnearest, wasm_fsqrt,
    wasm_i32_signed_to_i64, wasm_i32_unsigned_to_i64,
    wasm_i64_to_i32, wasm_iadd, wasm_iclz, wasm_ictz,
    wasm_idiv_signed, wasm_idiv_unsigned, wasm_ieq,
    wasm_ieqz, wasm_ige_signed, wasm_ige_unsigned,
    wasm_igt_signed, wasm_igt_unsigned,
    wasm_ile_signed, wasm_ile_unsigned,
    wasm_ilt_signed, wasm_ilt_unsigned, wasm_imul,
    wasm_ine, wasm_ipopcnt, wasm_irem_signed,
    wasm_irotl, wasm_irotr, wasm_ishl,
    wasm_ishr_signed, wasm_ishr_unsigned, wasm_isub)
from ...opcode import (
    Block, BlockInstructionBase, Br, BrIf, BrTable, Call, CallIndirect, DropInstruction, IfElse, InstructionBase, Loop, Nop, Return,
    SelectInstruction, Unreachable)
from ...opcode.numeric_generated import (
    VALID_BITS,
    BinaryOperatorInstructionBase,
    ConstantInstructionBase,
    CvtInstructionBase, F32Convert_i32_s,
    F32Convert_i32_u, F32Convert_i64_s,
    F32Convert_i64_u, F32Demote_f64,
    F32Reinterpret_i32, F64Convert_i32_s,
    F64Convert_i32_u, F64Convert_i64_s,
    F64Convert_i64_u, F64Promote_f32,
    F64Reinterpret_i64,
    I32Reinterpret_f32, I32Trunc_f32_s,
    I32Trunc_f32_u, I32Trunc_f64_s,
    I32Trunc_f64_u, I32Wrap_I64,
    I64Extend_i32_s, I64Extend_i32_u,
    I64Reinterpret_f64, I64Trunc_f32_s,
    I64Trunc_f32_u, I64Trunc_f64_s,
    I64Trunc_f64_u,
    RelOperatorInstructionBase,
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

WASM_LABEL_CONTINUATION = Tuple[
    Optional[BlockInstructionBase],  # instruction that triggered label block
    int,  # label
    List[InstructionBase],  # opcodes
    int,  # index of instruction we were running on
    List[WASM_VALUE],  # content of value stack at that time
    bool,  # is_loop
    List[VALTYPE_TYPE],  # result type
]


def interpret_wasm_section(
    code: List[InstructionBase],
    memory: WasmMemoryInstance,
    module: WasmModule,
    store: WasmStore,
    resulttype: List[VALTYPE_TYPE] = [],
) -> Tuple[Optional[WASM_VALUE], List[WASM_VALUE]]:
    stack: List[WASM_VALUE] = []
    current_block: Optional[BlockInstructionBase] = None
    current_label = 0
    label_stack: List[WASM_LABEL_CONTINUATION] = []
    # activation_stack: list = []
    is_loop: bool = False
    idx: int = 0

    # don't store len(code)
    while idx <= len(code) or is_loop:
        op = code[idx]
        idx += 1
        if is_loop:
            idx %= len(code)
        elif idx == len(code):
            if label_stack:
                # exit label
                # set "registers"
                current_block, current_label, code, idx, stack, is_loop, resulttype = label_stack.pop()
                # jump!
                continue
            else:
                # went out of code bounds, but no label to back
                break

        # Control Instructions
        if isinstance(op, Nop):
            continue  # do nothing
        elif isinstance(op, Unreachable):
            trap(op)
        elif isinstance(op, Block):
            # save continuation
            cont: WASM_LABEL_CONTINUATION = (
                current_block, current_label, list(code), idx, list(stack), is_loop, resulttype,
            )
            label_stack.append(cont)
            # reset "registers"
            current_block = op
            current_label = 0
            code = op.instr
            idx = 0
            stack = []
            is_loop = False
            resulttype = op.resultype
            # see you at the next continuation!
            continue
        elif isinstance(op, Loop):
            # save continuation
            cont = (
                current_block, current_label, list(code), idx, list(stack), is_loop, resulttype,
            )
            label_stack.append(cont)
            # reset "registers"
            current_block = op
            current_label = 0
            code = op.instr
            idx = 0
            stack = []
            is_loop = True  # we're in Loop instruction!
            resulttype = op.resultype
            # go!
            continue
        elif isinstance(op, IfElse):
            # save continuation
            cont = (
                current_block, current_label, list(code), idx, list(stack), is_loop, resulttype,
            )
            label_stack.append(cont)

            operand_c1: WASM_VALUE = stack.pop()

            # partially reset "registers"
            current_block = op
            current_label = 0
            # code = op.instr
            idx = 0
            stack = []
            is_loop = False
            resulttype = op.resultype

            if operand_c1[2] != 0:
                # op.instr is "then" block, so that's OK
                code = op.instr
            else:
                code = op.else_block
            # jump!
            continue
        elif isinstance(op, Br):
            # find specified label
            lbl = op.labelidx
            oldstack = list(stack)
            while label_stack:
                cont = label_stack.pop()
                if cont[1] == lbl:
                    break
            else:
                trap(f'Can\'t find label ${lbl}')
            # set "registers"
            current_block, current_label, code, idx, stack, is_loop, resulttype = cont
            stack = list(stack) + oldstack
            # jump!
            continue
        elif isinstance(op, BrIf):
            operand_c1 = stack.pop()

            if operand_c1[2] != 0:
                # find specified label
                lbl = op.labelidx
                oldstack = list(stack)
                while label_stack:
                    cont = label_stack.pop()
                    if cont[1] == lbl:
                        break
                else:
                    trap(f'Can\'t find label ${lbl}')
                # set "registers"
                current_block, current_label, code, idx, stack, is_loop, resulttype = cont
                stack = list(stack) + oldstack
                # jump!
                continue
        elif isinstance(op, BrTable):
            operand_c1 = stack.pop()
            if operand_c1[2] < len(op.labelindices):
                lbl = op.labelindices[int(operand_c1[2])]
            else:
                lbl = op.lastlabel
            # find specified label
            oldstack = list(stack)
            while label_stack:
                cont = label_stack.pop()
                if cont[1] == lbl:
                    break
            else:
                trap(f'Can\'t find label ${lbl}')
            # set "registers"
            current_block, current_label, code, idx, stack, is_loop, resulttype = cont
            stack = list(stack) + oldstack
            # jump!
            continue
        elif isinstance(op, Return):
            # is this correct?
            break
        elif isinstance(op, Call):
            func = module.funcs[op.callidx]
            interpret_wasm_section(func.body, memory, module, store, [])
        elif isinstance(op, CallIndirect):
            ta = module.tables[0].tableaddr
            tab = store.tables[ta]
            ft_expect = module.types[op.typeidx]
            operand_i = stack.pop()
            if len(tab.funcaddrs) < operand_i[2]:
                trap('funcaddrs out of range')
            a = tab.funcaddrs[len(tab.funcaddrs)]
            f = store.funcs[a]
            ft_actual = f.functype

            if ft_expect != ft_actual:
                trap('type signature mismatch')

            if isinstance(f, WasmLocalFunctionInstance):
                interpret_wasm_section(f.code, memory, f.module, store, [])
            elif isinstance(f, WasmHostFunctionInstance):
                # I forgot what should I pass here
                f.hostfunc(0)  # type: ignore
            else:
                trap(f'unknown function: {repr(f)}')

        # Constant Instruction
        elif isinstance(op, ConstantInstructionBase):
            stack.append((op.type, op.bits, op.value))

        # 4.4.1. Numeric Instructions
        elif isinstance(op, UnaryOperatorInstructionBase):
            operand_c1 = stack.pop()
            unopfunc = UNOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, unopfunc(cast(int, operand_c1[2]), op.bits)))
        elif isinstance(op, BinaryOperatorInstructionBase):
            operand_c2: WASM_VALUE = stack.pop()
            operand_c1 = stack.pop()
            biopfunc = BIOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, biopfunc(operand_c1[2], operand_c2[2], op.bits)))
        elif isinstance(op, TestOperatorInstructionBase):
            operand_c1 = stack.pop()
            testopfunc = TESTOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, testopfunc(operand_c1[2], op.bits)))
        elif isinstance(op, RelOperatorInstructionBase):
            operand_c2 = stack.pop()
            operand_c1 = stack.pop()
            relopfunc = RELOP_FUNC[f'{op.type}{op.op}']
            stack.append(clamp(op.type, op.bits, relopfunc(operand_c1[2], operand_c2[2], op.bits)))
        elif isinstance(op, CvtInstructionBase):
            operand_c1 = stack.pop()
            cvtopfunc = CVTOP_FUNC[type(op)]
            stack.append(clamp(op.type, op.bits, cvtopfunc(operand_c1[2])))

        # 4.4.2. Parametric Instructions
        elif isinstance(op, DropInstruction):
            stack.pop()
        elif isinstance(op, SelectInstruction):
            operand_c1 = stack.pop()
            operand_val2 = stack.pop()
            operand_val1 = stack.pop()
            if operand_c1[2] != 0:
                stack.append(operand_val1)
            else:
                stack.append(operand_val2)

    if resulttype:
        return stack[-1], stack
    else:
        return None, stack
