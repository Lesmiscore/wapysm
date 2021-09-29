import itertools
from typing import List, Optional, Union, cast

from ..utils import WASM_VALUE, typeof
from ..context import (
    WasmFunctionInstance,
    WasmStore, WasmModule)
from .runner import invoke_wasm_function

def invoke_function_external(funcaddr_or_func: Union[int, WasmFunctionInstance], store: WasmStore, exec_args: List[WASM_VALUE]) -> Optional[WASM_VALUE]:
    if isinstance(funcaddr_or_func, int):
        funcinst: WasmFunctionInstance = store.funcs[funcaddr_or_func]
    else:
        funcinst = funcaddr_or_func
    functype = funcinst.functype
    if len(functype.argument_types) != len(exec_args):
        raise Exception(f'Length of accepted arguments and given arguments differs. ({len(functype.argument_types)} vs {len(exec_args)})')
    for idx, e, v in zip(itertools.count(0), functype.argument_types, exec_args):
        if e != typeof(v):
            raise Exception(f'Argument type on index {idx} is wrong. ({e} vs {typeof(v)})')
    dummy_mod = WasmModule()
    dummy_mod.store = store
    stack: List[WASM_VALUE] = list(exec_args)
    invoke_wasm_function(funcinst, dummy_mod, store, stack)
    return stack[-1] if stack else None


def wrap_function(f: WasmFunctionInstance, store: WasmStore):
    def exec(*args):
        args_converted: List[WASM_VALUE] = []
        for a in args:
            if isinstance(a, int):
                args_converted.append(('i', 32, a))
            elif isinstance(a, float):
                args_converted.append(('f', 32, a))
            elif isinstance(a, tuple):
                args_converted.append(cast(WASM_VALUE, a))
            else:
                args_converted.append(('i', 32, -1))
        return invoke_function_external(f, store, args_converted)
    return exec
