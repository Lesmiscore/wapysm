import os
import sys
from typing import Dict, List
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from wapysm.parser.structure import WasmFunctionType
from wapysm.execute.interpreter.invocation import wrap_function
from wapysm.execute.utils import WASM_VALUE
from wapysm.execute.initialization import initialize_wasm_module, instantiate_wasm_module
from wapysm.execute.context import WasmHostFunctionInstance, WasmModule, WasmStore
from wapysm.parser.binary.module import parse_binary_wasm_module

def just_print(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]) -> None:
    print(args[0][2])

hfunc = WasmHostFunctionInstance()
hfunc.hostfunc = just_print
hfunc.functype = WasmFunctionType(['i32'], [])

import_object = {
    'env': {
        'print_console': hfunc,
    }
}

with open('script.wasm', 'rb') as source:
    parsed_module = parse_binary_wasm_module(source)
module = initialize_wasm_module(parsed_module, import_object)
instantiate_wasm_module(module, parsed_module, import_object)

wfunc = wrap_function(module.named_exports['gauss_legendre'], module.store)
wfunc(1)
wfunc(2)
wfunc(3)
