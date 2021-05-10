# wasm-core-1 5.2

import io
import struct


def read_byte(strm: io.RawIOBase) -> int:
    buf = strm.read(1)
    assert buf
    return struct.unpack('B', buf)[0]


def write_byte(strm: io.RawIOBase, value: int):
    strm.write(struct.pack('B', value))


# wasm-core-1 5.1
