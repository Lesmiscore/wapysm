import os
import sys
from typing import cast
import unittest
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.webassembly import WebAssembly
from wapysm.execute.context import WasmTable
from wapysm.execute.interpreter.invocation import wrap_function

class TestRunWasmFile(unittest.TestCase):
    def test_table(self):
        wasm_bin = requests.get('https://github.com/mdn/webassembly-examples/raw/master/js-api-examples/table.wasm').content
        wasm = WebAssembly.instantiate(wasm_bin, {})

        exp_table = cast(WasmTable, wasm.module.exports[0].value)
        print(exp_table)
        print(exp_table.elem)
        elem_0 = wrap_function(exp_table.elem[0], wasm.module.store, ['i32'])
        elem_1 = wrap_function(exp_table.elem[1], wasm.module.store, ['i32'])
        print(elem_0())
        print(elem_1())
