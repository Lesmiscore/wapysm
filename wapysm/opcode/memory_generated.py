# 2.4.4 Memory Instructions
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


class F32Load(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'f'
    bits: VALID_BITS = 32
    op: str = 'load'
    signed: SIGNED = None

class I32Load(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'load'
    signed: SIGNED = None

class F32Store(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'f'
    bits: VALID_BITS = 32
    op: str = 'store'
    signed: SIGNED = None

class I32Store(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'store'
    signed: SIGNED = None

class F64Load(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'f'
    bits: VALID_BITS = 64
    op: str = 'load'
    signed: SIGNED = None

class I64Load(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load'
    signed: SIGNED = None

class F64Store(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'f'
    bits: VALID_BITS = 64
    op: str = 'store'
    signed: SIGNED = None

class I64Store(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'store'
    signed: SIGNED = None

class I32Load8_s(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'load8_s'
    signed: SIGNED = 's'

class I32Load8_u(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'load8_u'
    signed: SIGNED = 'u'

class I32Load16_s(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'load16_s'
    signed: SIGNED = 's'

class I32Load16_u(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'load16_u'
    signed: SIGNED = 'u'

class I32Store8(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'store8'
    signed: SIGNED = None

class I32Store16(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 32
    op: str = 'store16'
    signed: SIGNED = None

class I64Load8_s(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load8_s'
    signed: SIGNED = 's'

class I64Load8_u(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load8_u'
    signed: SIGNED = 'u'

class I64Load16_s(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load16_s'
    signed: SIGNED = 's'

class I64Load16_u(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load16_u'
    signed: SIGNED = 'u'

class I64Load32_s(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load32_s'
    signed: SIGNED = 's'

class I64Load32_u(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'load32_u'
    signed: SIGNED = 'u'

class I64Store8(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'store8'
    signed: SIGNED = None

class I64Store16(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'store16'
    signed: SIGNED = None

class I64Store32(MemoryLoadStoreInstructionBase):
    type: INT_OR_FLOAT = 'i'
    bits: VALID_BITS = 64
    op: str = 'store32'
    signed: SIGNED = None

class MemorySize(InstructionBase):
    op: str = 'memory.size'

class MemoryGrow(InstructionBase):
    op: str = 'memory.grow'
