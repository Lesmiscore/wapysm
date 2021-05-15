import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.instruction import OPCODE_TABLE

class TestBinaryInstructions(unittest.TestCase):
    def test_opcode_table(self):
        self.assertEqual(len(OPCODE_TABLE), len(set(OPCODE_TABLE.keys())))
        self.assertEqual(len(OPCODE_TABLE), len(set(OPCODE_TABLE.values())))
