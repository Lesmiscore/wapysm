import struct

from typing import Callable, Dict, List, Optional, Union, Literal, Tuple
from ..execute.utils import WASM_VALUE, trap
from ..parser.structure import WasmFunctionType, WasmLimits, VALTYPE_TYPE, WasmGlobalType, WasmTableType
from ..opcode import InstructionBase


class WasmType(WasmFunctionType):
    def __init__(self, argument_types: List[VALTYPE_TYPE], return_types: List[VALTYPE_TYPE], instructions: List[InstructionBase]) -> None:
        super().__init__(argument_types, return_types)
        self.instructions = instructions

    instructions: List[InstructionBase]

class WasmFunction():
    "2.5.3 Functions"
    def __init__(self, wasm_mod: 'WasmModule', typeidx: int, locals: List[Tuple[int, VALTYPE_TYPE]], body: List[InstructionBase]) -> None:
        self.wasm_mod = wasm_mod
        self.typeidx = typeidx
        self.locals = locals
        self.body = body

    # module: WasmModule
    typeidx: int
    locals: List[Tuple[int, VALTYPE_TYPE]]
    body: List[InstructionBase]

class WasmTable(WasmTableType):
    "2.5.4 Tables"

    # value is funcaddr as per 4.2.7. Table Instances
    elem_addrs: Dict[int, int]
    elem: Dict[int, 'WasmFunctionInstance']

    def __init__(self, elemtype: int, lim: WasmLimits) -> None:
        super().__init__(elemtype, lim)
        self.max = lim.maximum
        self.elem_addrs = {}
        self.elem = {}
        for i in range(lim.minimum):
            self.elem_addrs[i] = -1

    def __len__(self):
        return len(self.elem_addrs)

    def grow(self, num: int):
        lim = self.lim
        if lim.maximum is not None and lim.minimum + num > lim.maximum:
            trap(f'lim.minimum + num > lim.maximum ({lim.minimum} + {num} > {lim.maximum}) where lim.maximum != None')
        for i in range(num):
            self.elem_addrs[lim.minimum + i] = -1

class WasmGlobal():
    "2.5.6 Globals"

    def __init__(self, globaltype: WasmGlobalType, init: List[InstructionBase]) -> None:
        self.globaltype = globaltype
        self.init = init

    globaltype: WasmGlobalType
    init: List[InstructionBase]
    addr: int

class WasmElem():
    "2.5.7 Element Segments"

    def __init__(self, tableidx: int, expr: List[InstructionBase], init: List[WasmFunction]) -> None:
        self.tableidx = tableidx
        self.expr = expr
        self.init = init

    tableidx: int
    expr: List[InstructionBase]
    init: List[WasmFunction]

class WasmElemUnresolved():
    "2.5.7 Element Segments but indexes unresolved"

    def __init__(self, tableidx: int, offset: List[InstructionBase], init: List[int]) -> None:
        self.tableidx = tableidx
        self.offset = offset
        self.init = init

    tableidx: int
    offset: List[InstructionBase]
    init: List[int]

class WasmData():
    "2.5.8 Data Segments"
    def __init__(self, memidx: int, offset: List[InstructionBase], init: bytes) -> None:
        self.memidx = memidx
        self.offset = offset
        self.init = init

    memidx: int
    offset: List[InstructionBase]
    init: bytes  # was vec(byte)

class WasmImport():
    module: str
    name: str
    # int is for typeidx, WasmLimits is for memtype
    importdesc: Union[int, WasmTableType, WasmLimits, WasmGlobalType]

class WasmExport():
    name: str
    exportdesc_type: Literal['func', 'table', 'mem', 'global']
    exportdesc_idx: int

class WasmExportValue(WasmExport):
    value: 'WASM_EXPORT_RESOLVED'

class WasmCodeFunction():
    code_locals: List[Tuple[int, VALTYPE_TYPE]]
    expr: List[InstructionBase]

class WasmCodeSection():
    size: int
    code: WasmCodeFunction

class WasmGlobalSection():
    ""
    gt: WasmGlobalType
    e: List[InstructionBase]

WASM_SECTION_TYPE = Union[
    bytes,  # custom section and undefined ID
    List[WasmFunctionType],  # type section
    List[WasmImport],  # import section
    List[int],  # function section
    int,  # start section
    List[WasmTableType],  # table section
    List[WasmLimits],  # memory section
    List[WasmGlobalSection],  # global section
    List[WasmExport],  # export section
    List[WasmElemUnresolved],  # element section
    List[WasmCodeSection],  # code section
    List[WasmData],  # data section
]

class WasmSection():
    section_id: int
    section_content: WASM_SECTION_TYPE

class WasmParsedModule():
    version: int
    sections: List[WasmSection]

class WasmModule():
    # These types are temporary and subject to change
    def __init__(self) -> None:
        self.types = {}
        self.funcaddrs = {}
        self.tableaddrs = {}
        self.memaddrs = {}
        self.globaladdrs = {}
        self.elem = {}
        self.data = {}
        self.start = None
        self.imports = {}
        self.exports = {}

    types: Dict[int, WasmType]
    funcaddrs: Dict[int, int]
    tableaddrs: Dict[int, int]
    memaddrs: Dict[int, int]
    globaladdrs: Dict[int, int]

    elem: Dict[int, WasmElem]
    data: Dict[int, WasmData]
    start: Optional[WasmFunction]
    imports: Dict[int, WasmImport]
    exports: Dict[int, WasmExportValue]

    store: 'WasmStore'

    @property
    def named_exports(self) -> Dict[str, 'WASM_EXPORT_RESOLVED']:
        return {a.name: a.value for _, a in self.exports.items()}



# store, module, locals, arguments
WASM_HOST_FUNC = Callable[['WasmStore', WasmModule, Dict[int, WASM_VALUE], List[WASM_VALUE]], Optional[WASM_VALUE]]

class WasmFunctionInstance():
    " 4.2.6 Function Instances "
    functype: WasmFunctionType

class WasmLocalFunctionInstance(WasmFunctionInstance):
    module: WasmModule
    wf: WasmFunction

class WasmHostFunctionInstance(WasmFunctionInstance):
    hostfunc: WASM_HOST_FUNC


WASM_PAGE_SIZE = 65536

class WasmMemory(WasmLimits):
    """
    2.5.5 Memories
    Itself is "type"
    """
    def __init__(self, minimum: int, maximum: Optional[int]) -> None:
        super().__init__(minimum, maximum)

class WasmMemoryInstance(WasmMemory):
    " 4.2.8 Memory Instances "
    data: bytearray
    maximum: Optional[int]

    def __init__(self, minimum: int, maximum: Optional[int]) -> None:
        super().__init__(minimum, maximum)
        self.data = bytearray(minimum * WASM_PAGE_SIZE)

    def __len__(self):
        return len(self.data) * WASM_PAGE_SIZE

    def __getitem__(self, key: int) -> int:
        return self.data[key]

    def __setitem__(self, key: int, value: int):
        self.data[key] = value

    def trim(self, begin: int, length: int) -> bytearray:
        return self.data[begin:begin + length]

    def set_int64(self, addr: int, v: int):
        self.data[addr:addr + 8] = struct.pack('<L', v)

    def get_int64(self, addr: int) -> int:
        return struct.unpack('<L', self.trim(addr, 8))[0]

    def set_int32(self, addr: int, v: int):
        self.data[addr:addr + 4] = struct.pack('<I', v)

    def get_int32(self, addr: int) -> int:
        return struct.unpack('<I', self.trim(addr, 8))[0]


    def set_float64(self, addr: int, v: float):
        self.data[addr:addr + 8] = struct.pack('<d', v)

    def get_float64(self, addr: int) -> float:
        return struct.unpack('<d', self.trim(addr, 8))[0]

    def set_float32(self, addr: int, v: float):
        self.data[addr:addr + 4] = struct.pack('<f', v)

    def get_float32(self, addr: int) -> float:
        return struct.unpack('<f', self.trim(addr, 8))[0]


class WasmGlobalInstance():
    " 4.2.9 Global Instances "
    value: WASM_VALUE
    mut: bool  # True if mutable, False if not

WASM_EXPORT_OBJECT = Union[WASM_HOST_FUNC, WasmTable, WasmMemoryInstance, WasmGlobalInstance]
WASM_EXPORT_RESOLVED = Union[WasmFunctionInstance, WasmTable, WasmMemoryInstance, WasmGlobalInstance]

class WasmStore():
    " 4.2.3 Store "
    def __init__(self) -> None:
        self.funcs = {}
        self.tables = {}
        self.mems = {}
        self.globals_ = {}

    funcs: Dict[int, WasmFunctionInstance]
    tables: Dict[int, WasmTable]
    mems: Dict[int, WasmMemoryInstance]
    globals_: Dict[int, WasmGlobalInstance]
