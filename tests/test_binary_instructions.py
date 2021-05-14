import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.instruction import opcode_table

class TestBinaryInstructions(unittest.TestCase):
    def test_opcode_table(self):
        self.assertEqual(len(opcode_table), len(set(opcode_table.keys())))
        self.assertEqual(len(opcode_table), len(set(opcode_table.values())))
