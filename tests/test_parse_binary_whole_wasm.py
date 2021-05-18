import os
import sys
import unittest
import requests
# import logging

# logging.basicConfig(level=logging.DEBUG, force=True)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.module import parse_binary_wasm_module

class TestParseBinaryWholeWasm(unittest.TestCase):
    def test_hello_wasm(self):
        with requests.get(
                'https://github.com/wasmerio/wasmer/raw/master/tests/wasi-wast/wasi/unstable/hello.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_path_rename_wasm(self):
        with requests.get(
                'https://github.com/wasmerio/wasmer/raw/master/tests/wasi-wast/wasi/unstable/path_rename.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)
