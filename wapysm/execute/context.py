from typing import Callable, Dict, List, Literal, Optional
from wapysm.parser.module import WasmMemory, WasmModule
from ..opcode.numeric_generated import ConstantInstructionBase
from ..opcode import InstructionBase
from ..parser.structure import WasmFunctionType


class WasmFunctionInstance():
    " 4.2.6 Function Instances "
    functype: WasmFunctionType

class WasmLocalFunctionInstance(WasmFunctionInstance):
    module: WasmModule
    code: List[InstructionBase]

class WasmHostFunctionInstance(WasmFunctionInstance):
    hostfunc: Callable[[int], int]  # TODO: make it better


class WasmTableInstance():
    " 4.2.7 Table Instances "
    funcaddrs: List[int]
    maximum: int


WASM_PAGE_SIZE = 65536

class WasmMemoryInstance(WasmMemory):
    " 4.2.8 Memory Instances "
    pages: List[bytearray]
    maximum: Optional[int]


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
    funcs: Dict[int, WasmFunctionInstance]
    tables: Dict[int, WasmTableInstance]
    mems: Dict[int, WasmMemoryInstance]
    globals_: Dict[int, WasmGlobalInstance]

# class WasmModuleInstance():
#     " 4.2.5 Module Instances "
#     types: Dict[int, WasmFunctionType]
#     funcaddrs: Dict[int, int]
#     tableaddrs: Dict[int, int]
#     memaddrs: Dict[int, int]
#     globaladdrs: Dict[int, int]
#     exports: Dict[int, WasmExportInstance]
