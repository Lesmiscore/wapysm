# Part of 2.4 Instructions
# Automatically generated. DO NOT EDIT

from typing import Literal, Union
from . import InstructionBase


INT_OR_FLOAT = Literal['f', 'i']
VALID_BITS = Literal[32, 64]

class ConstantInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    value: Union[int, float]
    bits: VALID_BITS
    op: Literal['const'] = 'const'

class I32Const(ConstantInstructionBase):
    type: INT_OR_FLOAT = 'i'
    value: int = 0
    bits: VALID_BITS = 32

class I64Const(ConstantInstructionBase):
    type: INT_OR_FLOAT = 'i'
    value: int = 0
    bits: VALID_BITS = 64

class F32Const(ConstantInstructionBase):
    type: INT_OR_FLOAT = 'f'
    value: float = 0
    bits: VALID_BITS = 32

class F64Const(ConstantInstructionBase):
    type: INT_OR_FLOAT = 'f'
    value: float = 0
    bits: VALID_BITS = 64


INT_UNARY_OPERATORS_TYPE = Literal['clz', 'ctz', 'popcnt']

FLOAT_UNARY_OPERATORS_TYPE = Literal['abs', 'neg', 'sqrt', 'ceil', 'floor', 'trunc', 'nearest']

class UnaryOperatorInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntUnopInstructionBase(UnaryOperatorInstructionBase):
    op: INT_UNARY_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

class FloatUnopInstructionBase(UnaryOperatorInstructionBase):
    op: FLOAT_UNARY_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'f'

class I32Clz(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'clz'
    bits: VALID_BITS = 32

class I32Ctz(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'ctz'
    bits: VALID_BITS = 32

class I32Popcnt(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'popcnt'
    bits: VALID_BITS = 32

class I64Clz(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'clz'
    bits: VALID_BITS = 64

class I64Ctz(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'ctz'
    bits: VALID_BITS = 64

class I64Popcnt(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = 'popcnt'
    bits: VALID_BITS = 64

class F32Abs(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'abs'
    bits: VALID_BITS = 32

class F32Neg(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'neg'
    bits: VALID_BITS = 32

class F32Sqrt(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'sqrt'
    bits: VALID_BITS = 32

class F32Ceil(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'ceil'
    bits: VALID_BITS = 32

class F32Floor(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'floor'
    bits: VALID_BITS = 32

class F32Trunc(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'trunc'
    bits: VALID_BITS = 32

class F32Nearest(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'nearest'
    bits: VALID_BITS = 32

class F64Abs(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'abs'
    bits: VALID_BITS = 64

class F64Neg(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'neg'
    bits: VALID_BITS = 64

class F64Sqrt(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'sqrt'
    bits: VALID_BITS = 64

class F64Ceil(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'ceil'
    bits: VALID_BITS = 64

class F64Floor(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'floor'
    bits: VALID_BITS = 64

class F64Trunc(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'trunc'
    bits: VALID_BITS = 64

class F64Nearest(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = 'nearest'
    bits: VALID_BITS = 64


INT_BINARY_OPERATORS_TYPE = Literal[
    'add', 'sub', 'mul', 'div_s', 'div_u', 'rem_s', 'rem_u',
    'and', 'or', 'xor', 'shl', 'shr_s', 'shr_u', 'rotl', 'rotr']

FLOAT_BINARY_OPERATORS_TYPE = Literal[
    'add', 'sub', 'mul', 'div', 'min', 'max', 'copysign']

class BinaryOperatorInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntBiopInstructionBase(BinaryOperatorInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

class FloatBiopInstructionBase(BinaryOperatorInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'f'


class I32Add(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'add'
    bits: VALID_BITS = 32

class I32Sub(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'sub'
    bits: VALID_BITS = 32

class I32Mul(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'mul'
    bits: VALID_BITS = 32

class I32Div_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'div_s'
    bits: VALID_BITS = 32

class I32Div_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'div_u'
    bits: VALID_BITS = 32

class I32Rem_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rem_s'
    bits: VALID_BITS = 32

class I32Rem_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rem_u'
    bits: VALID_BITS = 32

class I32And(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'and'
    bits: VALID_BITS = 32

class I32Or(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'or'
    bits: VALID_BITS = 32

class I32Xor(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'xor'
    bits: VALID_BITS = 32

class I32Shl(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shl'
    bits: VALID_BITS = 32

class I32Shr_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shr_s'
    bits: VALID_BITS = 32

class I32Shr_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shr_u'
    bits: VALID_BITS = 32

class I32Rotl(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rotl'
    bits: VALID_BITS = 32

class I32Rotr(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rotr'
    bits: VALID_BITS = 32

class I64Add(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'add'
    bits: VALID_BITS = 64

class I64Sub(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'sub'
    bits: VALID_BITS = 64

class I64Mul(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'mul'
    bits: VALID_BITS = 64

class I64Div_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'div_s'
    bits: VALID_BITS = 64

class I64Div_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'div_u'
    bits: VALID_BITS = 64

class I64Rem_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rem_s'
    bits: VALID_BITS = 64

class I64Rem_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rem_u'
    bits: VALID_BITS = 64

class I64And(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'and'
    bits: VALID_BITS = 64

class I64Or(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'or'
    bits: VALID_BITS = 64

class I64Xor(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'xor'
    bits: VALID_BITS = 64

class I64Shl(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shl'
    bits: VALID_BITS = 64

class I64Shr_s(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shr_s'
    bits: VALID_BITS = 64

class I64Shr_u(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'shr_u'
    bits: VALID_BITS = 64

class I64Rotl(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rotl'
    bits: VALID_BITS = 64

class I64Rotr(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = 'rotr'
    bits: VALID_BITS = 64

class F32Add(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'add'
    bits: VALID_BITS = 32

class F32Sub(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'sub'
    bits: VALID_BITS = 32

class F32Mul(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'mul'
    bits: VALID_BITS = 32

class F32Div(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'div'
    bits: VALID_BITS = 32

class F32Min(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'min'
    bits: VALID_BITS = 32

class F32Max(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'max'
    bits: VALID_BITS = 32

class F32Copysign(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'copysign'
    bits: VALID_BITS = 32

class F64Add(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'add'
    bits: VALID_BITS = 64

class F64Sub(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'sub'
    bits: VALID_BITS = 64

class F64Mul(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'mul'
    bits: VALID_BITS = 64

class F64Div(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'div'
    bits: VALID_BITS = 64

class F64Min(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'min'
    bits: VALID_BITS = 64

class F64Max(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'max'
    bits: VALID_BITS = 64

class F64Copysign(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = 'copysign'
    bits: VALID_BITS = 64


INT_TEST_OPERATORS_TYPE = Literal['eqn']

# Integer only

class TestOperatorInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntTestInstructionBase(TestOperatorInstructionBase):
    op: INT_TEST_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

# Integer only


class I32Eqn(IntTestInstructionBase):
    op: INT_TEST_OPERATORS_TYPE = 'eqn'
    bits: VALID_BITS = 32

class I64Eqn(IntTestInstructionBase):
    op: INT_TEST_OPERATORS_TYPE = 'eqn'
    bits: VALID_BITS = 64


INT_REL_OPERATORS_TYPE = Literal[
    'eq', 'ne',
    'lt_u', 'lt_s',
    'gt_u', 'gt_s',
    'le_u', 'le_s',
    'ge_u', 'ge_s']

FLOAT_REL_OPERATORS_TYPE = Literal['eq', 'ne', 'lt', 'gt', 'le', 'ge']

class RelOperatorInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntRelInstructionBase(RelOperatorInstructionBase):
    op: INT_REL_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

class FloatRelInstructionBase(RelOperatorInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'f'

class I32Eq(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'eq'
    bits: VALID_BITS = 32

class I32Ne(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ne'
    bits: VALID_BITS = 32

class I32Lt_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'lt_u'
    bits: VALID_BITS = 32

class I32Lt_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'lt_s'
    bits: VALID_BITS = 32

class I32Gt_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'gt_u'
    bits: VALID_BITS = 32

class I32Gt_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'gt_s'
    bits: VALID_BITS = 32

class I32Le_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'le_u'
    bits: VALID_BITS = 32

class I32Le_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'le_s'
    bits: VALID_BITS = 32

class I32Ge_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ge_u'
    bits: VALID_BITS = 32

class I32Ge_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ge_s'
    bits: VALID_BITS = 32

class I64Eq(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'eq'
    bits: VALID_BITS = 64

class I64Ne(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ne'
    bits: VALID_BITS = 64

class I64Lt_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'lt_u'
    bits: VALID_BITS = 64

class I64Lt_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'lt_s'
    bits: VALID_BITS = 64

class I64Gt_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'gt_u'
    bits: VALID_BITS = 64

class I64Gt_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'gt_s'
    bits: VALID_BITS = 64

class I64Le_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'le_u'
    bits: VALID_BITS = 64

class I64Le_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'le_s'
    bits: VALID_BITS = 64

class I64Ge_u(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ge_u'
    bits: VALID_BITS = 64

class I64Ge_s(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = 'ge_s'
    bits: VALID_BITS = 64

class F32Eq(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'eq'
    bits: VALID_BITS = 32

class F32Ne(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'ne'
    bits: VALID_BITS = 32

class F32Lt(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'lt'
    bits: VALID_BITS = 32

class F32Gt(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'gt'
    bits: VALID_BITS = 32

class F32Le(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'le'
    bits: VALID_BITS = 32

class F32Ge(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'ge'
    bits: VALID_BITS = 32

class F64Eq(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'eq'
    bits: VALID_BITS = 64

class F64Ne(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'ne'
    bits: VALID_BITS = 64

class F64Lt(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'lt'
    bits: VALID_BITS = 64

class F64Gt(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'gt'
    bits: VALID_BITS = 64

class F64Le(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'le'
    bits: VALID_BITS = 64

class F64Ge(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = 'ge'
    bits: VALID_BITS = 64

class I32Wrap_I64(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'wrap_i64'
    type: INT_OR_FLOAT = 'i'

class I64Extend_i32_f(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'extend_i32_f'
    type: INT_OR_FLOAT = 'i'

class I64Extend_i32_i(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'extend_i32_i'
    type: INT_OR_FLOAT = 'i'

class I32Trunc_f32_f(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'trunc_f32_f'
    type: INT_OR_FLOAT = 'i'

class F32Convert_i32_f(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'convert_f32_f'
    type: INT_OR_FLOAT = 'f'

class I32Trunc_f32_i(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'trunc_f32_i'
    type: INT_OR_FLOAT = 'i'

class F32Convert_i32_i(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'convert_f32_i'
    type: INT_OR_FLOAT = 'f'

class I32Trunc_f64_f(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'trunc_f64_f'
    type: INT_OR_FLOAT = 'i'

class F32Convert_i64_f(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'convert_f64_f'
    type: INT_OR_FLOAT = 'f'

class I32Trunc_f64_i(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'trunc_f64_i'
    type: INT_OR_FLOAT = 'i'

class F32Convert_i64_i(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'convert_f64_i'
    type: INT_OR_FLOAT = 'f'

class I64Trunc_f32_f(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'trunc_f32_f'
    type: INT_OR_FLOAT = 'i'

class F64Convert_i32_f(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'convert_f32_f'
    type: INT_OR_FLOAT = 'f'

class I64Trunc_f32_i(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'trunc_f32_i'
    type: INT_OR_FLOAT = 'i'

class F64Convert_i32_i(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'convert_f32_i'
    type: INT_OR_FLOAT = 'f'

class I64Trunc_f64_f(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'trunc_f64_f'
    type: INT_OR_FLOAT = 'i'

class F64Convert_i64_f(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'convert_f64_f'
    type: INT_OR_FLOAT = 'f'

class I64Trunc_f64_i(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'trunc_f64_i'
    type: INT_OR_FLOAT = 'i'

class F64Convert_i64_i(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'convert_f64_i'
    type: INT_OR_FLOAT = 'f'

class F32Demote_f64(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'demote_f64'
    type: INT_OR_FLOAT = 'f'

class F64Promote_f32(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'promote_f32'
    type: INT_OR_FLOAT = 'f'

class I32Reinterpret_f32(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'reinterpret_f32'
    type: INT_OR_FLOAT = 'i'

class F32Reinterpret_i32(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'reinterpret_i32'
    type: INT_OR_FLOAT = 'f'

class I32Reinterpret_f64(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'reinterpret_f64'
    type: INT_OR_FLOAT = 'i'

class F32Reinterpret_i64(InstructionBase):
    bits: VALID_BITS = 32
    op: str = 'reinterpret_i64'
    type: INT_OR_FLOAT = 'f'

class I64Reinterpret_f32(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'reinterpret_f32'
    type: INT_OR_FLOAT = 'i'

class F64Reinterpret_i32(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'reinterpret_i32'
    type: INT_OR_FLOAT = 'f'

class I64Reinterpret_f64(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'reinterpret_f64'
    type: INT_OR_FLOAT = 'i'

class F64Reinterpret_i64(InstructionBase):
    bits: VALID_BITS = 64
    op: str = 'reinterpret_i64'
    type: INT_OR_FLOAT = 'f'
