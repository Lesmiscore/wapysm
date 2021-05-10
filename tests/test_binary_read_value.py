import io
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.byteencode import (
    read_leb128_unsigned,
    write_leb128_unsigned,
    read_leb128_signed,
    write_leb128_signed,

    WasmLimits,
    read_limits,
    write_limits,
)

class TestLeb128(unittest.TestCase):
    def test_read_leb128_unsigned(self):
        stream = io.BytesIO(b'\xe5\x8e\x26')
        self.assertEqual(read_leb128_unsigned(stream), 624485)

    def test_write_leb128_unsigned(self):
        stream = io.BytesIO(b'')
        write_leb128_unsigned(stream, 624485)
        self.assertEqual(stream.getvalue(), b'\xe5\x8e\x26')

    def test_read_leb128_signed(self):
        stream = io.BytesIO(b'\xc0\xbb\x78')
        self.assertEqual(read_leb128_signed(stream), -123456)

    def test_write_leb128_signed(self):
        stream = io.BytesIO(b'')
        write_leb128_signed(stream, -123456)
        self.assertEqual(stream.getvalue(), b'\xc0\xbb\x78')


class TestLimits(unittest.TestCase):
    def test_read_limits_min(self):
        stream = io.BytesIO(b'\x00\xe5\x8e\x26')
        lmt = read_limits(stream)
        self.assertEqual(lmt.minimum, 624485)
        self.assertEqual(lmt.maximum, None)

    def test_read_limits_max(self):
        stream = io.BytesIO(b'\x01\xe5\x8e\x26\xe4\x8c\xca\x81\x0f')
        lmt = read_limits(stream)
        self.assertEqual(lmt.minimum, 624485)
        self.assertEqual(lmt.maximum, 4029843044)


    def test_write_limits_min(self):
        lmt = WasmLimits(624485, None)
        stream = io.BytesIO()
        write_limits(stream, lmt)
        self.assertEqual(stream.getvalue(), b'\x00\xe5\x8e\x26')

    def test_write_limits_max(self):
        lmt = WasmLimits(624485, 4029843044)
        stream = io.BytesIO()
        write_limits(stream, lmt)
        self.assertEqual(stream.getvalue(), b'\x01\xe5\x8e\x26\xe4\x8c\xca\x81\x0f')
