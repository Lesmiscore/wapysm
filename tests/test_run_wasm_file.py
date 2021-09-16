import os
import sys
from typing import cast
import unittest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.webassembly import WebAssembly
from wapysm.execute.utils import WASM_VALUE
from wapysm.execute.context import WasmGlobalInstance, WasmMemoryInstance, WasmTable
from wapysm.execute.interpreter.invocation import wrap_function
from wapysm.parser.structure import WasmLimits

class TestRunWasmFile(unittest.TestCase):

    def test_fail(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/fail.wasm').content
        wasm = WebAssembly.instantiate(wasm_bin, {})

        try:
            wasm.exports['fail_me']()
            raise AssertionError('This invocation must fail.')
        except Exception:
            print('Success!')

    def test_global(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/global.wasm').content
        global_ = WasmGlobalInstance()
        global_.value = ('i', 32, 0)
        global_.mut = True
        wasm = WebAssembly.instantiate(wasm_bin, {
            'js': {
                'global': global_,
            },
        })

        print(wasm.exports)
        self.assertEqual(cast(WASM_VALUE, wasm.exports['getGlobal']())[2], 0)

        global_.value = ('i', 32, 42)
        self.assertEqual(cast(WASM_VALUE, wasm.exports['getGlobal']())[2], 42)

        wasm.exports['incGlobal']()
        self.assertEqual(cast(WASM_VALUE, wasm.exports['getGlobal']())[2], 43)

        wasm.exports['incGlobal']()
        self.assertEqual(cast(WASM_VALUE, wasm.exports['getGlobal']())[2], 44)

    def test_table(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/table.wasm').content
        wasm = WebAssembly.instantiate(wasm_bin, {})

        exp_table = cast(WasmTable, wasm.module.exports[0].value)
        print(exp_table)
        print(exp_table.elem)
        elem_0 = wrap_function(exp_table.elem[0], wasm.module.store)
        elem_1 = wrap_function(exp_table.elem[1], wasm.module.store)
        self.assertEqual(cast(WASM_VALUE, elem_0())[2], 13)
        self.assertEqual(cast(WASM_VALUE, elem_1())[2], 42)

    def test_table2(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/table2.wasm').content
        tbl = WasmTable(0, WasmLimits(2, None))
        wasm = WebAssembly.instantiate(wasm_bin, {
            'js': {
                'tbl': tbl,
            }
        })

        self.assertEqual(len(tbl), 2)
        elem_0 = wrap_function(tbl.elem[0], wasm.module.store)
        elem_1 = wrap_function(tbl.elem[1], wasm.module.store)
        self.assertEqual(cast(WASM_VALUE, elem_0())[2], 42)
        self.assertEqual(cast(WASM_VALUE, elem_1())[2], 83)

    def test_memory(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/memory.wasm').content
        mem = WasmMemoryInstance(1, 1)
        wasm = WebAssembly.instantiate(wasm_bin, {
            'js': {
                'mem': mem,
            }
        })
        for i in range(10):
            mem[i * 4] = i
        self.assertEqual(wasm.exports['accumulate'](0, 10), ('i', 32, 45))
