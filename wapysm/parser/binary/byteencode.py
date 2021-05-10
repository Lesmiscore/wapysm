# wasm-core-1 5.2

import io
import struct
from typing import Dict, List, Callable, Union, Literal


def read_byte(strm: io.RawIOBase) -> int:
    buf = strm.read(1)
    assert buf
    return struct.unpack('B', buf)[0]

def write_byte(strm: io.RawIOBase, value: int):
    strm.write(struct.pack('B', value))


def read_leb128_unsigned(stream: io.RawIOBase) -> int:
    shift = 0
    result = 0
    while True:
        i = read_byte(stream)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result

def write_leb128_unsigned(strm: io.RawIOBase, value: int):
    while True:
        towrite = value & 0x7f
        value >>= 7
        if value:
            strm.write(bytes([towrite | 0x80, ]))
        else:
            strm.write(bytes([towrite, ]))
            break


# https://en.wikipedia.org/wiki/LEB128#Signed_LEB128
def read_leb128_signed(stream: io.RawIOBase) -> int:
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

def write_leb128_signed(strm: io.RawIOBase, value: int):
    while True:
        towrite = value & 0x7f
        value >>= 7
        if (value == 0 and (value & 0x40) == 0) or (value == -1 and (value & 0x40) != 0):
            strm.write(bytes([towrite, ]))
            break
        else:
            strm.write(bytes([towrite | 0x80, ]))


def read_float32(strm: io.RawIOBase) -> float:
    buf = strm.read(4)
    assert buf
    return struct.unpack('<f', buf)[0]

def write_float32(strm: io.RawIOBase, value: float):
    strm.write(struct.pack('<f', value))


def read_float64(strm: io.RawIOBase) -> float:
    buf = strm.read(4)
    assert buf
    return struct.unpack('<d', buf)[0]

def write_float64(strm: io.RawIOBase, value: float):
    strm.write(struct.pack('<d', value))

# wasm-core-1 5.1


def read_vector(strm: io.RawIOBase, read_function: Callable[[io.RawIOBase], int]) -> List[int]:
    elements: List[int] = []
    for _ in range(read_leb128_unsigned(strm)):
        elements.append(read_function(strm))
    return elements

def write_vector(strm: io.RawIOBase, elements: List[int], write_function: Callable[[io.RawIOBase, int], None]):
    write_leb128_signed(strm, len(elements))
    for element in elements:
        write_function(strm, element)


#  5.2.4 Names

def read_utf8(strm: io.RawIOBase) -> str:
    return bytes(read_vector(strm, read_byte)).decode('utf8')


def write_utf8(strm: io.RawIOBase, value: str):
    write_vector(strm, list(value.encode('utf8')), write_byte)

# 5.3.1 Value Types

VALTYPE_NUMBERS = Literal[0x7f, 0x7e, 0x7d, 0x7c]
VALTYPE_STRINGS = Literal['i32', 'i64', 'f32', 'f64']

VALTYPE_TYPE = Union[VALTYPE_NUMBERS, VALTYPE_STRINGS]

TYPES_TO_TYPENUMBER: Dict[VALTYPE_TYPE, VALTYPE_NUMBERS] = {
    0x7f: 0x7f, 'i32': 0x7f,
    0x7e: 0x7e, 'i64': 0x7e,
    0x7d: 0x7d, 'f32': 0x7d,
    0x7c: 0x7c, 'f64': 0x7c,
}

TYPES_TO_TYPENAME: Dict[VALTYPE_TYPE, VALTYPE_STRINGS] = {
    0x7f: 'i32', 'i32': 'i32',
    0x7e: 'i64', 'i64': 'i64',
    0x7d: 'f32', 'f32': 'f32',
    0x7c: 'f64', 'f64': 'f64',
}

def read_valtype(strm: io.RawIOBase) -> VALTYPE_STRINGS:
    return TYPES_TO_TYPENAME[read_byte(strm)]  # type: ignore

def write_valtype(strm: io.RawIOBase, value: VALTYPE_TYPE):
    write_byte(strm, TYPES_TO_TYPENUMBER[value])
