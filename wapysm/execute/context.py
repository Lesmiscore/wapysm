from typing import Any, Callable, List, Literal
from ..opcode.numeric_generated import ConstantInstructionBase
from ..opcode import InstructionBase
from ..parser.structure import WasmFunctionType


class WasmFunctionInstance():
    " 4.2.6 Function Instances "
    functype: WasmFunctionType

class WasmLocalFunctionInstance(WasmFunctionInstance):
    module: Any  # WasmModuleInstance
    code: List[InstructionBase]

class WasmHostFunctionInstance(WasmFunctionInstance):
    hostfunc: Callable[[int], int]


class WasmTableInstance():
    " 4.2.7 Table Instances "
    funcaddrs: List[int]
    maximum: int


WASM_PAGE_SIZE = 65536

class WasmMemoryInstance():
    " 4.2.8 Memory Instances "
    data: bytearray
    maximum: int


class WasmGlobalInstance():
    " 4.2.9 Global Instances "
    value: ConstantInstructionBase
    mut: bool  # True if mutable, False if not

class WasmExportInstance():
    " 4.2.10 Export Instances "
    name: str  # UTF-8
    externval_type: Literal['func', 'table', 'mem', 'global']
    externval_addr: int


class WasmStore():
    " 4.2.3 Store "
    funcs: WasmFunctionInstance
    tables: WasmTableInstance
    mems: WasmMemoryInstance
    globals_: WasmGlobalInstance

class WasmModuleInstance():
    " 4.2.5 Module Instances "
    types: WasmFunctionType
    funcaddrs: int
    tableaddrs: int
    memaddrs: int
    globaladdrs: int
    exports: WasmExportInstance
