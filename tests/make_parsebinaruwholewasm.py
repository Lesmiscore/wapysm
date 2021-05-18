import requests

pycode = '''import os
import sys
import unittest
import requests
# import logging

# logging.basicConfig(level=logging.DEBUG, force=True)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.module import parse_binary_wasm_module

class TestParseBinaryWholeWasm(unittest.TestCase):'''

with requests.get("https://api.github.com/repos/wasmerio/wasmer/contents/tests/wasi-wast/wasi/unstable") as r:
    data = r.json()
    for file in data:
        if not file['download_url'].endswith('.wasm'):
            continue
        pycode += f'''
    def test_{file['name'].replace('.', '_')}(self):
        with requests.get(
                '{file['download_url']}', stream=True) as r:
            parse_binary_wasm_module(r.raw)
'''

print(pycode)
