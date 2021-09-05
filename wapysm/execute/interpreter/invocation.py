import itertools
from typing import List, Optional
from wapysm.parser.structure import VALTYPE_TYPE

from ...execute.utils import WASM_VALUE, typeof
from ...execute.context import (
    WasmFunctionInstance,
    WasmStore, WasmModule)
from .runner import invoke_wasm_function

def invoke_function_external(funcaddr: int, store: WasmStore, rettype: List[VALTYPE_TYPE], exec_args: List[WASM_VALUE]) -> Optional[WASM_VALUE]:
    funcinst: WasmFunctionInstance = store.funcs[funcaddr]
    functype = funcinst.functype
    if len(functype.argument_types) != len(exec_args):
        raise Exception(f'Length of accepted arguments and given arguments differs. ({len(functype.argument_types)} vs {len(exec_args)})')
    for idx, e, v in zip(itertools.count(0), functype.argument_types, exec_args):
        if e != typeof(v):
            raise Exception(f'Argument type on index {idx} is wrong. ({e} vs {typeof(v)})')
    dummy_mod = WasmModule()
    dummy_mod.store = store
    stack: List[WASM_VALUE] = []
    invoke_wasm_function(funcinst, dummy_mod, store, rettype, stack)
    return stack[0] if stack else None
