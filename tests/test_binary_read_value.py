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
)

class TestRWBinary(unittest.TestCase):
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
