from typing import Callable, Dict, List, Optional, Union, Literal, Tuple
from ..execute.utils import WASM_VALUE
from ..parser.structure import WasmFunctionType, WasmLimits, VALTYPE_TYPE, WasmGlobalType, WasmTableType
from ..opcode import InstructionBase


class WasmType(WasmFunctionType):
    def __init__(self, argument_types: List[VALTYPE_TYPE], return_types: List[VALTYPE_TYPE], instructions: List[InstructionBase]) -> None:
        super().__init__(argument_types, return_types)
        self.instructions = instructions

    instructions: List[InstructionBase]

class WasmFunction():
    "2.5.3 Functions"
    def __init__(self, wasm_mod: 'WasmModule', typeidx: int, locals: List[VALTYPE_TYPE], body: List[InstructionBase]) -> None:
        self.wasm_mod = wasm_mod
        self.typeidx = typeidx
        self.locals = locals
        self.body = body

    # module: WasmModule
    typeidx: int
    locals: List[VALTYPE_TYPE]
    body: List[InstructionBase]

class WasmTable(WasmTableType):
    "2.5.4 Tables"

    # value is funcaddr as per 4.2.7. Table Instances
    elem: Dict[int, int]

    def __init__(self, elemtype: int, lim: WasmLimits) -> None:
        super().__init__(elemtype, lim)
        self.max = lim.maximum

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



WASM_HOST_FUNC = Callable[['WasmStore', WasmModule, Dict[int, WASM_VALUE]], int]

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
    pages: List[bytearray]
    maximum: Optional[int]

    def __init__(self, minimum: int, maximum: Optional[int]) -> None:
        super().__init__(minimum, maximum)
        self.pages = []
        for _ in range(minimum):
            self.pages.append(bytearray(WASM_PAGE_SIZE))

    def __len__(self):
        return len(self.pages) * WASM_PAGE_SIZE

    def __getitem__(self, key: int) -> int:
        begin_index, begin_offset = divmod(key, WASM_PAGE_SIZE)
        return self.pages[begin_index][begin_offset]

    def __setitem__(self, key: int, value: int):
        begin_index, begin_offset = divmod(key, WASM_PAGE_SIZE)
        self.pages[begin_index][begin_offset] = value

    def trim(self, begin: int, length: int) -> bytearray:
        begin_index, begin_offset = divmod(begin, WASM_PAGE_SIZE)
        end_index, end_offset = divmod(begin + length, WASM_PAGE_SIZE)
        if end_offset == 0:
            end_offset = WASM_PAGE_SIZE
            end_index = end_index - 1

        if begin_index == end_index:
            # not spans page
            return self.pages[begin_index][begin_offset:end_offset]
        else:
            # spans page
            return self.pages[begin_index][begin_offset:WASM_PAGE_SIZE] + self.pages[end_index][0:end_offset]


class WasmGlobalInstance():
    " 4.2.9 Global Instances "
    value: WASM_VALUE
    mut: bool  # True if mutable, False if not

WASM_EXPORT_OBJECT = Union[WASM_HOST_FUNC, WasmTable, WasmMemoryInstance, WasmGlobalInstance]
WASM_EXPORT_RESOLVED = Union[WasmFunctionInstance, WasmTable, WasmMemoryInstance, WasmGlobalInstance]

class WasmStore():
    " 4.2.3 Store "
    funcs: Dict[int, WasmFunctionInstance]
    tables: Dict[int, WasmTable]
    mems: Dict[int, WasmMemoryInstance]
    globals_: Dict[int, WasmGlobalInstance]
