# flake8: noqa: E704,E701,E222

from math import copysign, floor, isinf, isnan, sqrt, trunc
from typing import Tuple, Union
from wapysm.opcode.numeric_generated import INT_OR_FLOAT, VALID_BITS
from ..opcode import InstructionBase
import struct

WASM_VALUE = Tuple[INT_OR_FLOAT, VALID_BITS, Union[int, float]]

class WasmTrappedException(Exception):
    def __init__(self, msg: str, op: InstructionBase, *operands: object) -> None:
        super().__init__(msg)
        self.op: InstructionBase = op
        self.operands: Tuple[object, ...] = operands

def trap(op, *operands):
    raise WasmTrappedException('trapped: %s' % repr(op), op, *operands)

def clamp(tp: INT_OR_FLOAT, bits: VALID_BITS, value: Union[int, float]) -> WASM_VALUE:
    " Fixes value to its correct size "
    if tp == 'i':
        if bits == 32:
            return (tp, bits, clamp_32bit(value))
        elif bits == 64:
            return (tp, bits, clamp_64bit(value))
        else:
            raise Exception('Invalid bits: %d' % bits)
    elif tp == 'f':
        if bits == 32:
            pack_arg = 'f<'
        elif bits == 64:
            pack_arg = 'd<'
        else:
            raise Exception('Invalid bits: %d' % bits)
        return (tp, bits, struct.unpack(pack_arg, struct.pack(pack_arg, value))[0])
    else:
        raise Exception('Invalid WASM value: %s' % repr(value))

# convert to unsigned number
def clamp_32bit(value): return value & (2**32 - 1)
def clamp_64bit(value): return value & (2**64 - 1)
def clamp_anybit(value: int, bits: VALID_BITS): return value & (2**bits - 1)

# convert to signed number
def unclamp_32bit(value: int) -> int:
    if value < 0:
        # no need to unclamp: in-Python negative numbers are not eligible
        return value
    if value & (2**31) == 0:
        # not a negative number
        return value
    # pack the number as unsigned, unpack it as signed
    return struct.unpack('i>', struct.pack('I>', value))[0]

def unclamp_64bit(value: int) -> int:
    if value < 0:
        # no need to unclamp: in-Python negative numbers are not eligible
        return value
    if value & (2**63) == 0:
        # not a negative number
        return value
    # pack the number as unsigned, unpack it as signed
    return struct.unpack('l>', struct.pack('L>', value))[0]

def unclamp_anybit(value: int, bits: VALID_BITS):
    if bits == 32:
        return unclamp_32bit(value)
    else:
        return unclamp_64bit(value)


def count_lead_and_trail_zeroes(d):
    # https://graphics.stanford.edu/~seander/bithacks.html#ZerosOnRightLinear
    if d:
        v = (d ^ (d - 1) >> 1)  # Set v's trailing 0s to 1s and zero rest
        trailing = 0
        while v:
            v >>= 1
            trailing += 1

        leading = 64
        v = d
        while v:
            v >>= 1
            leading -= 1
        return leading, trailing
    return 64, 64

def wasm_fnearest(value: float, bits: VALID_BITS) -> float:
    " 4.3.3.16 fnearest "
    # value is zero, infinity or NaN
    if isinf(value) or isnan(value) or abs(value) == 0:
        return value
    
    ipart = abs(floor(value))
    fpart = abs(value) - ipart

    if ipart == 0:  # value is less than 1.0
        return copysign(0.0, value)

    if fpart < 0.5:  # value is more than 1.0
        return ipart
    else:
        return ipart + 1.0

def wasm_fsqrt(value: float, bits: VALID_BITS) -> float:
    return sqrt(value)

def wasm_iclz(value: int, bits: VALID_BITS) -> int:
    " 4.3.2.18. iclz "
    if bits == 32:
        return wasm_iclz32(value)
    else:
        return wasm_iclz64(value)

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Integer.java#L1620
def wasm_iclz32(i: int) -> int:
    " iclz for 32-bit integer "
    # this is required because Java has 32-bit signed integer but Python don't
    i = clamp_32bit(i)

    if i <= 0:
        return 32 if i == 0 else 0
    n = 31
    if i >= 1 << 16: n -= 16; i >>= 16
    if i >= 1 <<  8: n -=  8; i >>=  8
    if i >= 1 <<  4: n -=  4; i >>=  4
    if i >= 1 <<  2: n -=  2; i >>=  2
    return n - (i >> 1)

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Long.java#L1763
def wasm_iclz64(i: int):
    " iclz for 64-bit integer "
    # this is required because Java has 64-bit signed integer but Python don't
    i = clamp_64bit(i)

    x = i >> 32
    return (32 + wasm_iclz32(i)) if x == 0 else wasm_iclz32(x)


def wasm_ictz(value: int, bits: VALID_BITS) -> int:
    " 4.3.2.19. ictz "
    if bits == 32:
        return wasm_ictz32(value)
    else:
        return wasm_ictz64(value)

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Integer.java#L1647
def wasm_ictz32(i):
    # this is required because Java has 32-bit signed integer but Python don't
    i = clamp_32bit(i)

    if i == 0: return 32
    n = 31

    y = clamp_32bit(i << 16)
    if y != 0: n = n - 16; i = y

    y = clamp_32bit(i << 8)
    if y != 0: n = n - 8; i = y

    y = clamp_32bit(i << 4)
    if y != 0: n = n - 4; i = y

    y = clamp_32bit(i << 2)
    if y != 0: n = n - 2; i = y

    return n - (clamp_32bit(i << 1) >> 31)

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Long.java#L1784
def wasm_ictz64(i):
    # this is required because Java has 64-bit signed integer but Python don't
    i = clamp_64bit(i)

    if i == 0: return 64
    n = 63

    y = clamp_32bit(i)
    if y != 0:
        n = n - 32
        x = y
    else:
        x = i >> 32

    y = clamp_32bit(x << 16)
    if y != 0: n = n -16; x = y

    y = clamp_32bit(x << 8)
    if y != 0: n = n - 8; x = y

    y = clamp_32bit(x << 4)
    if y != 0: n = n - 4; x = y

    y = clamp_32bit(x << 2)
    if y != 0: n = n - 2; x = y

    return n - (clamp_32bit(x << 1) >> 31)


def wasm_ipopcnt(value: int, bits: VALID_BITS) -> int:
    " 4.3.2.20. ipopcnt "
    if bits == 32:
        return wasm_ipopcnt32(value)
    else:
        return wasm_ipopcnt64(value)

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Integer.java#L1670
def wasm_ipopcnt32(i: int) -> int:
    # this is required because Java has 32-bit signed integer but Python don't
    i = clamp_32bit(i)

    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    i = (i + (i >> 4)) & 0x0f0f0f0f
    i = i + (i >> 8)
    i = i + (i >> 16)
    return i & 0x3f

# https://github.com/AdoptOpenJDK/openjdk-jdk11/blob/master/src/java.base/share/classes/java/lang/Long.java#L1808
def wasm_ipopcnt64(i: int) -> int:
    # this is required because Java has 64-bit signed integer but Python don't
    i = clamp_64bit(i)

    i = i - ((i >> 1) & 0x5555555555555555)
    i = (i & 0x3333333333333333) + ((i >> 2) & 0x3333333333333333)
    i = (i + (i >> 4)) & 0x0f0f0f0f0f0f0f0f
    i = i + (i >> 8)
    i = i + (i >> 16)
    i = i + (i >> 32)
    return i & 0x7f


def wasm_iadd(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.3. iadd "
    return clamp_anybit(a + b, bits)

def wasm_isub(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.4. isub "
    return clamp_anybit(a - b, bits)

def wasm_imul(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.5. imul "
    return clamp_anybit(a * b, bits)


def wasm_idiv_unsigned(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.6. idiv_u "
    if b == 0:
        trap('DIV/0!', a, b)
    return clamp_anybit(a, bits) // clamp_anybit(b, bits)

def wasm_idiv_signed(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.7. idiv_s "
    if b == 0:
        trap('DIV/0!', a, b)
    return unclamp_anybit(a, bits) // unclamp_anybit(b, bits)


def wasm_irem_unsigned(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.8. irem_u "
    if b == 0:
        trap('DIV/0!', a, b)
    return a - wasm_imul(b, wasm_idiv_unsigned(a, b, bits), bits)

def wasm_irem_signed(a: int, b: int, bits: VALID_BITS) -> int:
    " 4.3.2.9. irem_s "
    if b == 0:
        trap('DIV/0!', a, b)
    return a - wasm_imul(b, wasm_idiv_signed(a, b, bits), bits)
