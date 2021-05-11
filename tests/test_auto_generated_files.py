import os
import sys
import unittest
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

keys_before_import = set(globals().keys())
from wapysm.opcode.auto import *  # noqa: F403, F401
keys_after_import = set(globals().keys())

imported_names = keys_after_import - keys_before_import

class TestGeneratedOpcodes(unittest.TestCase):
    def test_numeric_intfloat(self):
        for name in imported_names:
            if name.endswith('Base'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            self.assertEqual(name[0].lower(), ttp().type)

    def test_numeric_bits(self):
        for name in imported_names:
            if name.endswith('Base'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            match = re.search(r'^[IF](\d+)', name)
            if not match:
                raise Exception(name)
            bit = int(match.group(1))
            # All non-base numeric opcode class must have bits field
            self.assertEqual(bit, ttp().bits)

    def test_numeric_name(self):
        for name in imported_names:
            if name.endswith('Base'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            opcode_from_name = re.sub(r'^[IF](\d+)', '', name).lower()
            self.assertEqual(opcode_from_name, ttp().op)
