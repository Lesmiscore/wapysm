import os
import sys
import unittest
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

keys_before_numeric = set(globals().keys())
from wapysm.opcode.numeric_generated import *  # noqa: F403, F401
keys_after_numeric = set(globals().keys())

imported_numeric_names = keys_after_numeric - keys_before_numeric

keys_before_memory = set(globals().keys())
from wapysm.opcode.memory_generated import *  # noqa: F403, F401
keys_after_memory = set(globals().keys())

imported_memory_names = keys_after_memory - keys_before_memory

class TestGeneratedNumericOpcodes(unittest.TestCase):
    def test_numeric_intfloat(self):
        for name in imported_numeric_names:
            if name.endswith('Base'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            self.assertEqual(name[0].lower(), ttp().type)

    def test_numeric_bits(self):
        for name in imported_numeric_names:
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
        for name in imported_numeric_names:
            if name.endswith('Base'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            opcode_from_name = re.sub(r'^[IF](\d+)', '', name).lower()
            self.assertEqual(opcode_from_name, ttp().op)


class TestGeneratedMemoryOpcodes(unittest.TestCase):
    def test_memory_intfloat(self):
        for name in imported_memory_names:
            if name.endswith('Base'):
                continue
            if name.startswith('Memory'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            self.assertEqual(name[0].lower(), ttp().type)

    def test_memory_bits(self):
        for name in imported_memory_names:
            if name.endswith('Base'):
                continue
            if name.startswith('Memory'):
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

    def test_memory_name(self):
        for name in imported_memory_names:
            if name.endswith('Base'):
                continue
            if name.startswith('Memory'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            opcode_from_name = re.sub(r'^[IF](\d+)', '', name).lower()
            self.assertEqual(opcode_from_name, ttp().op)

    def test_memory_sizegrow(self):
        for name in imported_memory_names:
            if name.endswith('Base'):
                continue
            if not name.startswith('Memory'):
                continue
            ttp = globals()[name]
            print(ttp)
            if not isinstance(ttp, type):
                continue
            opcode_from_name = re.sub(r'[A-Z]', r'.\g<0>', name).lower()[1:]
            self.assertEqual(opcode_from_name, ttp().op)
