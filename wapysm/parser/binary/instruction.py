# 5.4 Instructions
import logging
from typing import IO, Dict, List, Literal, Set, Tuple, Type, cast

from wapysm.opcode.opcode_visitor import walk_bottomup
from .byteencode import read_blocktype, read_byte, read_float32, read_float64, read_leb128_unsigned, read_vector

from ...opcode import (
    Block, BlockInstructionBase, Br, BrIf, BrTable, BranchInstructionBase, Call, CallIndirect,
    DropInstruction, GlobalGetInstruction,
    GlobalSetInstruction, IfElse, InstructionBase,
    LocalGetInstruction, LocalSetInstruction,
    LocalTeeInstruction, Loop, Nop, Return,
    SelectInstruction, Unreachable, VariableInstructionBase
)
from ...opcode.memory_generated import (
    F32Load, F32Store, F64Load, F64Store,
    I32Load, I32Load8_s, I32Load8_u,
    I32Load16_s, I32Load16_u, I32Store,
    I32Store8, I32Store16, I64Load,
    I64Load8_s, I64Load8_u, I64Load16_s,
    I64Load16_u, I64Load32_s, I64Load32_u,
    I64Store, I64Store8, I64Store16,
    I64Store32, MemoryGrow, MemoryLoadStoreInstructionBase, MemorySize
)
from ...opcode.numeric_generated import (
    ConstantInstructionBase, F32Abs, F32Add, F32Ceil, F32Const,
    F32Convert_i32_s, F32Convert_i32_u,
    F32Convert_i64_s, F32Convert_i64_u,
    F32Copysign, F32Demote_f64, F32Div,
    F32Eq, F32Floor, F32Ge, F32Gt, F32Le,
    F32Lt, F32Max, F32Min, F32Mul, F32Ne,
    F32Nearest, F32Neg,
    F32Reinterpret_i32, F32Sqrt, F32Sub,
    F32Trunc, F64Abs, F64Add, F64Ceil,
    F64Const, F64Convert_i32_s,
    F64Convert_i32_u, F64Convert_i64_s,
    F64Convert_i64_u, F64Copysign, F64Div,
    F64Eq, F64Floor, F64Ge, F64Gt, F64Le,
    F64Lt, F64Max, F64Min, F64Mul, F64Ne,
    F64Nearest, F64Neg, F64Promote_f32,
    F64Reinterpret_i64, F64Sqrt, F64Sub,
    F64Trunc, I32Add, I32And, I32Clz,
    I32Const, I32Ctz, I32Div_s, I32Div_u,
    I32Eq, I32Eqz, I32Ge_s, I32Ge_u, I32Gt_s, I32Gt_u,
    I32Le_s, I32Le_u, I32Lt_s, I32Lt_u,
    I32Mul, I32Ne, I32Or, I32Popcnt,
    I32Reinterpret_f32, I32Rem_s,
    I32Rem_u, I32Rotl, I32Rotr, I32Shl,
    I32Shr_s, I32Shr_u, I32Sub,
    I32Trunc_f32_s, I32Trunc_f32_u,
    I32Trunc_f64_s, I32Trunc_f64_u,
    I32Wrap_I64, I32Xor, I64Add, I64And,
    I64Clz, I64Const, I64Ctz, I64Div_s,
    I64Div_u, I64Eq, I64Eqz,
    I64Extend_i32_s, I64Extend_i32_u,
    I64Ge_s, I64Ge_u, I64Gt_s, I64Gt_u,
    I64Le_s, I64Le_u, I64Lt_s, I64Lt_u,
    I64Mul, I64Ne, I64Or, I64Popcnt,
    I64Reinterpret_f64, I64Rem_s,
    I64Rem_u, I64Rotl, I64Rotr, I64Shl,
    I64Shr_s, I64Shr_u, I64Sub,
    I64Trunc_f32_s, I64Trunc_f32_u,
    I64Trunc_f64_s, I64Trunc_f64_u,
    I64Xor
)

logger = logging.getLogger('wapysm.parser.binary.instruction')

OPCODE_TABLE: Dict[int, Type[InstructionBase]] = {
    # 5.4.1 Control Instructions
    0x00: Unreachable,
    0x01: Nop,
    0x02: Block,
    0x03: Loop,
    0x04: IfElse,
    # 0x05: IfElse, // else branch
    # 0x0B: End, // end
    0x0C: Br,
    0x0D: BrIf,
    0x0E: BrTable,
    0x0F: Return,
    0x10: Call,
    0x11: CallIndirect,

    # 5.4.2 Parametric Instructions
    0x1A: DropInstruction,
    0x1B: SelectInstruction,

    # 5.4.3 Variable Instructions
    0x20: LocalGetInstruction,
    0x21: LocalSetInstruction,
    0x22: LocalTeeInstruction,
    0x23: GlobalGetInstruction,
    0x24: GlobalSetInstruction,

    # 5.4.4 Memory Instructions
    0x28: I32Load,
    0x29: I64Load,
    0x2A: F32Load,
    0x2B: F64Load,
    0x2C: I32Load8_s,
    0x2D: I32Load8_u,
    0x2E: I32Load16_s,
    0x2F: I32Load16_u,
    0x30: I64Load8_s,
    0x31: I64Load8_u,
    0x32: I64Load16_s,
    0x33: I64Load16_u,
    0x34: I64Load32_s,
    0x35: I64Load32_u,
    0x36: I32Store,
    0x37: I64Store,
    0x38: F32Store,
    0x39: F64Store,
    0x3A: I32Store8,
    0x3B: I32Store16,
    0x3C: I64Store8,
    0x3D: I64Store16,
    0x3E: I64Store32,
    0x3F: MemorySize,
    0x40: MemoryGrow,

    # 5.4.5 Numeric Instructions
    # const instructions
    0x41: I32Const,
    0x42: I64Const,
    0x43: F32Const,
    0x44: F64Const,
    # other numeric instructions
    0x45: I32Eqz,
    0x46: I32Eq,
    0x47: I32Ne,
    0x48: I32Lt_s,
    0x49: I32Lt_u,
    0x4A: I32Gt_s,
    0x4B: I32Gt_u,
    0x4C: I32Le_s,
    0x4D: I32Le_u,
    0x4E: I32Ge_s,
    0x4F: I32Ge_u,

    0x50: I64Eqz,
    0x51: I64Eq,
    0x52: I64Ne,
    0x53: I64Lt_s,
    0x54: I64Lt_u,
    0x55: I64Gt_s,
    0x56: I64Gt_u,
    0x57: I64Le_s,
    0x58: I64Le_u,
    0x59: I64Ge_s,
    0x5A: I64Ge_u,

    0x5B: F32Eq,
    0x5C: F32Ne,
    0x5D: F32Lt,
    0x5E: F32Gt,
    0x5F: F32Le,
    0x60: F32Ge,

    0x61: F64Eq,
    0x62: F64Ne,
    0x63: F64Lt,
    0x64: F64Gt,
    0x65: F64Le,
    0x66: F64Ge,

    0x67: I32Clz,
    0x68: I32Ctz,
    0x69: I32Popcnt,
    0x6A: I32Add,
    0x6B: I32Sub,
    0x6C: I32Mul,
    0x6D: I32Div_s,
    0x6E: I32Div_u,
    0x6F: I32Rem_s,
    0x70: I32Rem_u,
    0x71: I32And,
    0x72: I32Or,
    0x73: I32Xor,
    0x74: I32Shl,
    0x75: I32Shr_s,
    0x76: I32Shr_u,
    0x77: I32Rotl,
    0x78: I32Rotr,

    0x79: I64Clz,
    0x7A: I64Ctz,
    0x7B: I64Popcnt,
    0x7C: I64Add,
    0x7D: I64Sub,
    0x7E: I64Mul,
    0x7F: I64Div_s,
    0x80: I64Div_u,
    0x81: I64Rem_s,
    0x82: I64Rem_u,
    0x83: I64And,
    0x84: I64Or,
    0x85: I64Xor,
    0x86: I64Shl,
    0x87: I64Shr_s,
    0x88: I64Shr_u,
    0x89: I64Rotl,
    0x8A: I64Rotr,

    0x8B: F32Abs,
    0x8C: F32Neg,
    0x8D: F32Ceil,
    0x8E: F32Floor,
    0x8F: F32Trunc,
    0x90: F32Nearest,
    0x91: F32Sqrt,
    0x92: F32Add,
    0x93: F32Sub,
    0x94: F32Mul,
    0x95: F32Div,
    0x96: F32Min,
    0x97: F32Max,
    0x98: F32Copysign,

    0x99: F64Abs,
    0x9A: F64Neg,
    0x9B: F64Ceil,
    0x9C: F64Floor,
    0x9D: F64Trunc,
    0x9E: F64Nearest,
    0x9F: F64Sqrt,
    0xA0: F64Add,
    0xA1: F64Sub,
    0xA2: F64Mul,
    0xA3: F64Div,
    0xA4: F64Min,
    0xA5: F64Max,
    0xA6: F64Copysign,

    0xA7: I32Wrap_I64,
    0xA8: I32Trunc_f32_s,
    0xA9: I32Trunc_f32_u,
    0xAA: I32Trunc_f64_s,
    0xAB: I32Trunc_f64_u,
    0xAC: I64Extend_i32_s,
    0xAD: I64Extend_i32_u,
    0xAE: I64Trunc_f32_s,
    0xAF: I64Trunc_f32_u,
    0xB0: I64Trunc_f64_s,
    0xB1: I64Trunc_f64_u,
    0xB2: F32Convert_i32_s,
    0xB3: F32Convert_i32_u,
    0xB4: F32Convert_i64_s,
    0xB5: F32Convert_i64_u,
    0xB6: F32Demote_f64,
    0xB7: F64Convert_i32_s,
    0xB8: F64Convert_i32_u,
    0xB9: F64Convert_i64_s,
    0xBA: F64Convert_i64_u,
    0xBB: F64Promote_f32,
    0xBC: I32Reinterpret_f32,
    0xBD: I64Reinterpret_f64,
    0xBE: F32Reinterpret_i32,
    0xBF: F64Reinterpret_i64,
}


# Instruction without operands can be cached
_INSTRUCTIONS_WITHOUT_OPERANDS: Set[int] = {x for rgn in [
    (0x00, 0x01),  # unreachable and nop
    [0x0F],  # return
    (0x1A, 0x1B),  # drop and select
    (0x3F, 0x40),  # memory.*
    range(0x45, 0xBF + 1),  # "All other numeric instructions" in 5.4.5. Numeric Instructions
] for x in rgn}
_INSTRUCTION_CACHE: Dict[int, InstructionBase] = {}

READ_FINISH_REASON = Literal['eof', 'else', 'end']

_ENABLE_WASM_STACKTRACE = True

def _read_instructions(stream: IO[bytes]) -> Tuple[READ_FINISH_REASON, List[InstructionBase]]:
    result: List[InstructionBase] = []
    while True:
        try:
            opcode = read_byte(stream)
        except IndexError:
            break
        logger.debug('going to parse instruction 0x%02X' % opcode)

        if opcode == 0x0B:  # end of block
            return 'end', result
        elif opcode == 0x05:  # end of if block, but else comes next
            return 'else', result
        elif opcode not in OPCODE_TABLE:
            raise Exception('Unknown opcode: 0x%02X' % opcode)
        elif opcode in _INSTRUCTIONS_WITHOUT_OPERANDS:
            if _ENABLE_WASM_STACKTRACE:
                inst = OPCODE_TABLE[opcode]()
            else:
                inst = _INSTRUCTION_CACHE.get(opcode) or OPCODE_TABLE[opcode]()
                _INSTRUCTION_CACHE[opcode] = inst
            result.append(inst)
        elif opcode == 0x10:
            inst = Call()
            inst.callidx = read_leb128_unsigned(stream)
            result.append(inst)
        elif opcode == 0x11:
            inst = CallIndirect()
            inst.typeidx = read_leb128_unsigned(stream)
            read_byte(stream)  # dummy byte?
            result.append(inst)

        # Block instructions
        elif opcode == 0x02 or opcode == 0x03:  # block .. end or loop .. end
            inst = cast(BlockInstructionBase, OPCODE_TABLE[opcode]())
            inst.resultype = read_blocktype(stream)
            cause, inst.instr = _read_instructions(stream)
            if cause != 'end':
                raise Exception(f'"block" or "loop" instruction must end with "end" instruction. was: {cause}')
            result.append(inst)
        elif opcode == 0x04:  # if .. (else ..) end
            inst = IfElse()
            inst.resultype = read_blocktype(stream)
            cause, inst.instr = _read_instructions(stream)
            if cause == 'else':
                cause, inst.else_block = _read_instructions(stream)
            if cause != 'end':
                raise Exception(f'"if" branch instruction must end with "end" opcode even if it contains "else" block. was: {cause}')
            result.append(inst)
        elif opcode == 0x0C or opcode == 0x0D:  # br*
            inst = cast(BranchInstructionBase, OPCODE_TABLE[opcode]())
            inst.labelidx = read_leb128_unsigned(stream)
            result.append(inst)
        elif opcode == 0x0E:  # br_table
            inst = BrTable()
            inst.labelindices = read_vector(stream, read_leb128_unsigned)
            inst.lastlabel = read_leb128_unsigned(stream)
            result.append(inst)

        # Variable Instructions
        elif 0x20 <= opcode and opcode <= 0x24:  # local.* and global.*
            inst = cast(VariableInstructionBase, OPCODE_TABLE[opcode]())
            inst.index = read_leb128_unsigned(stream)
            result.append(inst)

        # Memory Instructions (except memory.* which is handled above)
        elif 0x28 <= opcode and opcode <= 0x3E:  # i32.load ~ i64.store
            inst = cast(MemoryLoadStoreInstructionBase, OPCODE_TABLE[opcode]())
            inst.align = read_leb128_unsigned(stream)
            inst.offset = read_leb128_unsigned(stream)
            result.append(inst)

        # Numeric Instructions (except instructions without operands)
        elif opcode == 0x41 or opcode == 0x42:
            inst = cast(ConstantInstructionBase, OPCODE_TABLE[opcode]())
            inst.value = read_leb128_unsigned(stream)
            result.append(inst)
        elif opcode == 0x43:
            inst = F32Const()
            inst.value = read_float32(stream)
            result.append(inst)
        elif opcode == 0x44:
            inst = F64Const()
            inst.value = read_float64(stream)
            result.append(inst)

        # what else?
        else:
            raise Exception('Unreachable 0x%02X' % opcode)

    return 'eof', result


if _ENABLE_WASM_STACKTRACE:
    def read_instructions(stream: IO[bytes]) -> Tuple[READ_FINISH_REASON, List[InstructionBase]]:
        a, b = _read_instructions(stream)
        for i in walk_bottomup(b):
            if not isinstance(i, BlockInstructionBase):
                continue
            for idx, op in enumerate(i.instr):
                op._debug_internal_index = idx
            for idx, op in enumerate(getattr(i, 'else_block', ())):
                op._debug_internal_index = idx
        return a, b
else:
    read_instructions = _read_instructions
