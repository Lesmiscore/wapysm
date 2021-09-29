#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get ojichat.wasm from https://github.com/nao20010128nao/ojichat-wasm/raw/gh-pages/dfe7d4a69c0e31e2dfd6630defe17c08.wasm
from time import sleep
from threading import Thread
from wapysm.execute.initialization import initialize_wasm_module, instantiate_wasm_module
from wapysm.parser.binary.module import parse_binary_wasm_module
from wapysm.shim.golang import Go

gol = Go()
global_object = gol._global
import_object = gol.import_object

with open('ojichat.wasm', 'rb') as r:
    parsed_module = parse_binary_wasm_module(r)
    module = initialize_wasm_module(parsed_module, import_object)
    instantiate_wasm_module(module, parsed_module, import_object)

Thread(None, lambda: gol.run(module)).start()

print('Waiting for export')
while 'ojichat' not in global_object:
    sleep(1)

ojichat = global_object['ojichat']
print(ojichat)

print(ojichat({
    'targetName': 'あああ',
}))
