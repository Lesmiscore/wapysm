# Auto generation script for 2.4 Instructions

import itertools

pycode = '''# Part of 2.4 Instructions
# Automatically generated. DO NOT EDIT

from typing import List, Literal, Union
from . import InstructionBase


INT_OR_FLOAT = Literal['f', 'i']
VALID_BITS = Literal[32, 64]

class ConstantInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    value: Union[int, float]
    bits: VALID_BITS
    op: Literal['const'] = 'const'
'''

for (fi, bits) in itertools.product(['int', 'float'], [32, 64]):
    name = f'{fi[0].upper()}{bits}Const'
    pycode += f'''
class {name}(ConstantInstructionBase):
    type: INT_OR_FLOAT = '{fi[0]}'
    value: {fi} = 0
    bits: VALID_BITS = {bits}
'''


pycode += """

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
"""

for (bits, unop) in itertools.product([32, 64], ['clz', 'ctz', 'popcnt']):
    name = f'I{bits}{unop.capitalize()}'
    pycode += f'''
class {name}(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'i'
    op: INT_UNARY_OPERATORS_TYPE = '{unop}'
    bits: VALID_BITS = {bits}
'''

for (bits, unop) in itertools.product([32, 64], ['abs', 'neg', 'sqrt', 'ceil', 'floor', 'trunc', 'nearest']):
    name = f'F{bits}{unop.capitalize()}'
    pycode += f'''
class {name}(UnaryOperatorInstructionBase):
    type: INT_OR_FLOAT = 'f'
    op: FLOAT_UNARY_OPERATORS_TYPE = '{unop}'
    bits: VALID_BITS = {bits}
'''


pycode += """

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

"""

for (bits, biop) in itertools.product(
        [32, 64],
        ['add', 'sub', 'mul', 'div_s', 'div_u', 'rem_s', 'rem_u', 'and', 'or', 'xor', 'shl', 'shr_s', 'shr_u', 'rotl', 'rotr']):
    name = f'I{bits}{biop.capitalize()}'
    pycode += f'''
class {name}(IntBiopInstructionBase):
    op: INT_BINARY_OPERATORS_TYPE = '{biop}'
    bits: VALID_BITS = {bits}
'''

for (bits, biop) in itertools.product(
        [32, 64],
        ['add', 'sub', 'mul', 'div', 'min', 'max', 'copysign']):
    name = f'F{bits}{biop.capitalize()}'
    pycode += f'''
class {name}(FloatBiopInstructionBase):
    op: FLOAT_BINARY_OPERATORS_TYPE = '{biop}'
    bits: VALID_BITS = {bits}
'''


pycode += """

INT_TEST_OPERATORS_TYPE = Literal['eqn']

# Float only

class TestOperatorInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntTestInstructionBase(TestOperatorInstructionBase):
    op: INT_TEST_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

# Float only

"""

for (bits, biop) in itertools.product([32, 64], ['eqn']):
    name = f'I{bits}{biop.capitalize()}'
    pycode += f'''
class {name}(IntTestInstructionBase):
    op: INT_TEST_OPERATORS_TYPE = '{biop}'
    bits: VALID_BITS = {bits}
'''


pycode += """

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
"""

for (bits, unop) in itertools.product([32, 64], [
        'eq', 'ne',
        'lt_u', 'lt_s',
        'gt_u', 'gt_s',
        'le_u', 'le_s',
        'ge_u', 'ge_s']):
    name = f'I{bits}{unop.capitalize()}'
    pycode += f'''
class {name}(IntRelInstructionBase):
    op: INT_REL_OPERATORS_TYPE = '{unop}'
    bits: VALID_BITS = {bits}
'''

for (bits, unop) in itertools.product([32, 64], ['eq', 'ne', 'lt', 'gt', 'le', 'ge']):
    name = f'F{bits}{unop.capitalize()}'
    pycode += f'''
class {name}(FloatRelInstructionBase):
    op: FLOAT_REL_OPERATORS_TYPE = '{unop}'
    bits: VALID_BITS = {bits}
'''


print(pycode)

with open('wapysm/opcode/auto.py', 'w') as w:
    w.write(pycode)
