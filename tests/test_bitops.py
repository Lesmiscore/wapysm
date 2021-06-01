import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wapysm.execute.utils import wasm_iclz, wasm_ictz, wasm_ipopcnt

class TestBitOperations(unittest.TestCase):
    def test_iclz(self):
        self.assertEqual(wasm_iclz(12, 32), 28)
        self.assertEqual(wasm_iclz(12, 64), 60)

        self.assertEqual(wasm_iclz(-12, 32), 0)
        self.assertEqual(wasm_iclz(-12, 64), 0)

        self.assertEqual(wasm_iclz(42, 32), 26)
        self.assertEqual(wasm_iclz(42, 64), 58)

        self.assertEqual(wasm_iclz(-41, 32), 0)
        self.assertEqual(wasm_iclz(-41, 64), 0)

    def test_ictz(self):
        self.assertEqual(wasm_ictz(12, 32), 2)
        self.assertEqual(wasm_ictz(12, 64), 2)

        self.assertEqual(wasm_ictz(-12, 32), 2)
        self.assertEqual(wasm_ictz(-12, 64), 2)

        self.assertEqual(wasm_ictz(42, 32), 1)
        self.assertEqual(wasm_ictz(42, 64), 1)

        self.assertEqual(wasm_ictz(-42, 32), 1)
        self.assertEqual(wasm_ictz(-42, 64), 1)

    def test_ipopcnt(self):
        self.assertEqual(wasm_ipopcnt(12, 32), 2)
        self.assertEqual(wasm_ipopcnt(12, 64), 2)

        self.assertEqual(wasm_ipopcnt(-12, 32), 29)
        self.assertEqual(wasm_ipopcnt(-12, 64), 61)

        self.assertEqual(wasm_ipopcnt(42, 32), 3)
        self.assertEqual(wasm_ipopcnt(42, 64), 3)

        self.assertEqual(wasm_ipopcnt(-41, 32), 30)
        self.assertEqual(wasm_ipopcnt(-41, 64), 62)
