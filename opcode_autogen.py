# Auto generation script for 2.4 Instructions

import itertools

pycode = '''# 2.4.1 Numeric Instructions
# Automatically generated. DO NOT EDIT

from typing import Literal, Union
from . import InstructionBase


INT_OR_FLOAT = Literal['f', 'i']
VALID_BITS = Literal[32, 64]

class NumericInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS
    op: str


class ConstantInstructionBase(NumericInstructionBase):
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

class UnaryOperatorInstructionBase(NumericInstructionBase):
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

class BinaryOperatorInstructionBase(NumericInstructionBase):
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

# Integer only

class TestOperatorInstructionBase(NumericInstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS

class IntTestInstructionBase(TestOperatorInstructionBase):
    op: INT_TEST_OPERATORS_TYPE
    type: INT_OR_FLOAT = 'i'

# Integer only

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

class RelOperatorInstructionBase(NumericInstructionBase):
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

pycode += """
class I32Wrap_I64(NumericInstructionBase):
    bits: VALID_BITS = 32
    op: str = 'wrap_i64'
    type: INT_OR_FLOAT = 'i'
"""

for fi in ['f', 'i']:
    pycode += f"""
class I64Extend_i32_{fi}(NumericInstructionBase):
    bits: VALID_BITS = 64
    op: str = 'extend_i32_{fi}'
    type: INT_OR_FLOAT = 'i'
"""

for (nn, mm, fi) in itertools.product([32, 64], [32, 64], ['f', 'i']):
    pycode += f"""
class I{nn}Trunc_f{mm}_{fi}(NumericInstructionBase):
    bits: VALID_BITS = {nn}
    op: str = 'trunc_f{mm}_{fi}'
    type: INT_OR_FLOAT = 'i'

class F{nn}Convert_i{mm}_{fi}(NumericInstructionBase):
    bits: VALID_BITS = {nn}
    op: str = 'convert_i{mm}_{fi}'
    type: INT_OR_FLOAT = 'f'
"""

pycode += """
class F32Demote_f64(NumericInstructionBase):
    bits: VALID_BITS = 32
    op: str = 'demote_f64'
    type: INT_OR_FLOAT = 'f'

class F64Promote_f32(NumericInstructionBase):
    bits: VALID_BITS = 64
    op: str = 'promote_f32'
    type: INT_OR_FLOAT = 'f'
"""


for (nn, mm) in itertools.product([32, 64], [32, 64]):
    pycode += f"""
class I{nn}Reinterpret_f{mm}(NumericInstructionBase):
    bits: VALID_BITS = {nn}
    op: str = 'reinterpret_f{mm}'
    type: INT_OR_FLOAT = 'i'

class F{nn}Reinterpret_i{mm}(NumericInstructionBase):
    bits: VALID_BITS = {nn}
    op: str = 'reinterpret_i{mm}'
    type: INT_OR_FLOAT = 'f'
"""

print(pycode)

with open('wapysm/opcode/numeric_generated.py', 'w') as w:
    w.write(pycode)




pycode = '''# 2.4.4 Memory Instructions
# Automatically generated. DO NOT EDIT

from typing import Literal, Optional
from . import InstructionBase


INT_OR_FLOAT = Literal['f', 'i']
VALID_BITS = Literal[32, 64]
SIGNED = Optional[Literal['u', 's']]

class MemoryLoadStoreInstructionBase(InstructionBase):
    type: INT_OR_FLOAT
    bits: VALID_BITS
    op: str
    signed: SIGNED
    offset: int
    align: int

'''

for (nn, tpp, fi) in itertools.product([32, 64], ['load', 'store'], 'fi'):
    pycode += f"""
class {fi.upper()}{nn}{tpp.capitalize()}(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = '{fi}'
    bits: VALID_BITS = {nn}
    op: str = '{tpp}'
    signed: SIGNED = None
"""


for (nn, tpp, store) in itertools.product([32, 64], ['load', 'store'], [8, 16, 32]):
    if nn <= store:
        continue
    part = f"""
class I{nn}{tpp.capitalize()}{store}**SIGNED**(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = {nn}
"""
    if tpp == 'store':
        pycode += part.replace('**SIGNED**', '')
        pycode += f'''    op: str = '{tpp}{store}'\n    signed: SIGNED = None\n'''
    else:
        for signed in 'su':
            pycode += part.replace('**SIGNED**', f'_{signed}')
            pycode += f'''    op: str = '{tpp}{store}_{signed}'\n    signed: SIGNED = '{signed}'\n'''


pycode += '''
class MemorySize(InstructionBase):
    op: str = 'memory.size'

class MemoryGrow(InstructionBase):
    op: str = 'memory.grow'
'''

print(pycode)

with open('wapysm/opcode/memory_generated.py', 'w') as w:
    w.write(pycode)
