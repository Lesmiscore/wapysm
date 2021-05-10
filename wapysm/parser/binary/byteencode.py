# wasm-core-1 5.2

import io
import struct
from ..structure import (
    VALTYPE_STRINGS, VALTYPE_TYPE,
    TYPES_TO_TYPENUMBER, TYPES_TO_TYPENAME,
    WasmFunctionType, WasmLimits, WasmTableType, WasmGlobalType,
)
from typing import List, Callable, TypeVar

BIO = io.RawIOBase
T = TypeVar('T')

def read_byte(strm: BIO) -> int:
    buf = strm.read(1)
    assert buf
    return struct.unpack('B', buf)[0]

def write_byte(strm: BIO, value: int):
    strm.write(struct.pack('B', value))


def read_leb128_unsigned(stream: BIO) -> int:
    shift = 0
    result = 0
    while True:
        i = read_byte(stream)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result

def write_leb128_unsigned(strm: BIO, value: int):
    while True:
        towrite = value & 0x7f
        value >>= 7
        if value:
            strm.write(bytes([towrite | 0x80, ]))
        else:
            strm.write(bytes([towrite, ]))
            break


# https://en.wikipedia.org/wiki/LEB128#Signed_LEB128
def read_leb128_signed(stream: BIO) -> int:
    shift = 0
    result = 0
    while True:
        i = read_byte(stream)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            if shift < 128 and (i & 0x40) != 0:
                result = result | (~0 << shift)
            break

    return result

def write_leb128_signed(strm: BIO, value: int):
    while True:
        towrite = value & 0x7f
        value >>= 7
        if (value == 0 and (value & 0x40) == 0) or (value == -1 and (value & 0x40) != 0):
            strm.write(bytes([towrite, ]))
            break
        else:
            strm.write(bytes([towrite | 0x80, ]))


def read_float32(strm: BIO) -> float:
    buf = strm.read(4)
    assert buf
    return struct.unpack('<f', buf)[0]

def write_float32(strm: BIO, value: float):
    strm.write(struct.pack('<f', value))


def read_float64(strm: BIO) -> float:
    buf = strm.read(4)
    assert buf
    return struct.unpack('<d', buf)[0]

def write_float64(strm: BIO, value: float):
    strm.write(struct.pack('<d', value))

# wasm-core-1 5.1


def read_vector(strm: BIO, read_function: Callable[[io.RawIOBase], T]) -> List[T]:
    elements: List[T] = []
    for _ in range(read_leb128_unsigned(strm)):
        elements.append(read_function(strm))
    return elements

def write_vector(strm: BIO, elements: List[T], write_function: Callable[[io.RawIOBase, T], None]):
    write_leb128_signed(strm, len(elements))
    for element in elements:
        write_function(strm, element)


#  5.2.4 Names

def read_utf8(strm: BIO) -> str:
    return bytes(read_vector(strm, read_byte)).decode('utf8')


def write_utf8(strm: BIO, value: str):
    write_vector(strm, list(value.encode('utf8')), write_byte)

# 5.3.1 Value Types

def read_valtype(strm: BIO) -> VALTYPE_STRINGS:
    return TYPES_TO_TYPENAME[read_byte(strm)]  # type: ignore

def write_valtype(strm: BIO, value: VALTYPE_TYPE):
    write_byte(strm, TYPES_TO_TYPENUMBER[value])

# 5.3.2 Result Types

def read_blocktype(strm: BIO) -> List[VALTYPE_STRINGS]:
    num = read_byte(strm)
    if num == 0x40:
        return []
    return [TYPES_TO_TYPENAME[read_byte(strm)]]  # type: ignore


# value has type of List[VALTYPE_TYPE] to allow supporting multiple return types in the future
def write_blocktype(strm: BIO, value: List[VALTYPE_TYPE]):
    if not value:
        write_byte(strm, 0x40)
        return
    if len(value) != 1:
        raise Exception('Current WASM specification does not allow multiple values for return value!')
    write_byte(strm, TYPES_TO_TYPENUMBER[value[0]])


# 5.3.3 Function Types


def read_functype(strm: BIO, strict: bool = False) -> WasmFunctionType:
    header = read_byte(strm)
    if header != 0x60:
        raise Exception(f"We're supposed to read non-functype value! ({header})")
    argument_types: List[VALTYPE_TYPE] = read_vector(strm, read_valtype)
    return_types: List[VALTYPE_TYPE] = read_vector(strm, read_valtype)
    if strict and len(return_types) < 2:
        raise Exception(f'There is more than 1 return type! ({len(return_types)})')
    return WasmFunctionType(argument_types, return_types)

def write_functype(strm: BIO, value: WasmFunctionType):
    write_byte(strm, 0x60)
    write_vector(strm, value.argument_types, write_valtype)
    write_vector(strm, value.return_types, write_valtype)


# 5.3.4 Limits

def read_limits(strm: BIO) -> WasmLimits:
    type = read_byte(strm)
    minimum = read_leb128_unsigned(strm)
    if type == 0x00:
        return WasmLimits(minimum, None)
    elif type == 0x01:
        maximum = read_leb128_unsigned(strm)
        return WasmLimits(minimum, maximum)
    else:
        raise Exception(f'Invalid type for limit: {type}, minimum: {minimum}')


def write_limits(strm: BIO, value: WasmLimits):
    write_byte(strm, 0x00 if value.maximum is None else 0x01)
    write_leb128_unsigned(strm, value.minimum)
    if value.maximum is not None:
        write_leb128_unsigned(strm, value.maximum)


# 5.3.5. Memory Types

def read_memtype(strm: BIO) -> WasmLimits:
    return read_limits(strm)

def write_memtype(strm: BIO, value: WasmLimits):
    write_limits(strm, value)


# 5.3.6 Table Types


def read_tabletype(strm: BIO) -> WasmTableType:
    # elemtype
    elemtype = read_byte(strm)
    lmt = read_limits(strm)
    return WasmTableType(elemtype, lmt)

def write_tabletype(strm: BIO, value: WasmTableType):
    write_byte(strm, value.elemtype)
    write_limits(strm, value.lim)


# 5.3.7 Global Types

def read_globaltype(strm: BIO) -> WasmGlobalType:
    vt = read_valtype(strm)
    mutability = read_byte(strm)
    return WasmGlobalType(vt, mutability == 0x01)

def write_globaltype(strm: BIO, value: WasmGlobalType):
    write_valtype(strm, value.t)
    write_byte(strm, 0x01 if value.m else 0x00)
