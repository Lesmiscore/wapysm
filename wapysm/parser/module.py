# Section 2.5 Modules

from typing import List, Literal, Optional, Tuple, Union
from ..opcode import InstructionBase
from .structure import VALTYPE_TYPE, WasmFunctionType, WasmGlobalType, WasmLimits, WasmTableType


class WasmType(WasmFunctionType):
    def __init__(self, argument_types: List[VALTYPE_TYPE], return_types: List[VALTYPE_TYPE], instructions: List[InstructionBase]) -> None:
        super().__init__(argument_types, return_types)
        self.instructions = instructions

    instructions: List[InstructionBase]

class WasmFunction():
    "2.5.3 Functions"
    def __init__(self, wasm_mod, typeidx: int, locals: List[VALTYPE_TYPE], body: List[InstructionBase]) -> None:
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
    def __init__(self, elemtype: int, lim: WasmLimits) -> None:
        super().__init__(elemtype, lim)

class WasmMemory(WasmLimits):
    """
    2.5.5 Memories
    Itself is "type"
    """
    def __init__(self, minimum: int, maximum: Optional[int]) -> None:
        super().__init__(minimum, maximum)

class WasmGlobal():
    "2.5.6 Globals"

    def __init__(self, globaltype: WasmGlobalType, init: List[InstructionBase]) -> None:
        self.globaltype = globaltype
        self.init = init

    globaltype: WasmGlobalType
    init: List[InstructionBase]

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

    def __init__(self, tableidx: int, expr: List[InstructionBase], init: List[int]) -> None:
        self.tableidx = tableidx
        self.expr = expr
        self.init = init

    tableidx: int
    expr: List[InstructionBase]
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

class WasmSection():
    section_id: int
    section_content: Union[
        bytes,  # custom section and undefined ID
        List[WasmFunctionType],  # type section
        List[WasmImport],  # import section
        List[int],  # function section and start section
        List[WasmTableType],  # table section
        List[WasmLimits],  # memory section
        List[WasmGlobalSection],  # global section
        List[WasmExport],  # export section
        List[WasmElemUnresolved],  # element section
        List[WasmCodeSection],  # code section
        List[WasmData],  # data section
    ]

class WasmParsedModule():
    version: int
    sections: List[WasmSection]

class WasmModule():
    # These types are temporary and subject to change
    types: List[WasmType]
    funcs: List[WasmFunction]
    tables: List[WasmTable]
    mems: List[WasmMemory]
    globals: List[WasmGlobal]
    elem: List[WasmElem]
    data: List[WasmData]
    start: Optional[WasmFunction]
    imports: List[WasmImport]
    exports: List[WasmExport]
