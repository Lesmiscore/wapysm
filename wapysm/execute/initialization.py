from typing import Callable, Dict, List, Optional, cast
from ..execute.utils import WASM_VALUE
from ..execute.interpreter.runner import interpret_wasm_section
from ..execute.context import WASM_EXPORT_OBJECT, WASM_HOST_FUNC, WasmGlobalInstance, WasmHostFunctionInstance, WasmLocalFunctionInstance, WasmMemoryInstance, WasmStore
from ..parser.structure import VALTYPE_TYPE, WasmFunctionType, WasmLimits, WasmTableType
from ..parser.module import WASM_SECTION_TYPE, WasmCodeSection, WasmData, WasmElemUnresolved, WasmExport, WasmFunction, WasmGlobalSection, WasmImport, WasmModule, WasmParsedModule, WasmTable, WasmType


def _next_addr(module: WasmModule) -> int:
    current = getattr(module, '__addrs', 0)
    alloc = current + 1
    setattr(module, '__addrs', alloc)
    return alloc


def allocate_function(
    # FIXME: absolutely wrong code
    module: WasmModule,
    functype: WasmFunctionType,
    typeidx: int,
    code: WasmCodeSection,
) -> int:
    funcaddr = _next_addr(module)
    locals = cast(List[VALTYPE_TYPE], [x[1] for x in sorted(code.code.code_locals)])
    wf = WasmFunction(module, typeidx, locals, code.code.expr)
    localfunc = WasmLocalFunctionInstance()
    localfunc.module = module
    localfunc.wf = wf
    localfunc.functype = WasmType(functype.argument_types, functype.return_types, code.code.expr)
    module.types[typeidx] = localfunc.functype
    module.funcaddrs[len(module.funcaddrs)] = funcaddr
    module.store.funcs[funcaddr] = localfunc
    return funcaddr


def allocate_host_function(
    # FIXME: absolutely wrong code
    module: WasmModule,
    code: WASM_HOST_FUNC,
) -> int:
    funcaddr = _next_addr(module)
    localfunc = WasmHostFunctionInstance()
    localfunc.hostfunc = code
    localfunc.functype = WasmType([], ['i32'], code.code.expr)
    module.funcaddrs[len(module.funcaddrs)] = funcaddr
    module.store.funcs[funcaddr] = localfunc
    return funcaddr


def allocate_table(
    module: WasmModule,
    tbl: WasmTableType,
) -> int:
    tableaddr = _next_addr(module)
    table = WasmTable(tbl.elemtype, tbl.lim)
    module.tableaddrs[len(module.tableaddrs)] = tableaddr
    # module.tables[tableaddr] = table
    module.store.tables[tableaddr] = table
    return tableaddr


def allocate_external_table(
    module: WasmModule,
    table: WasmTable,
) -> int:
    tableaddr = _next_addr(module)
    module.tableaddrs[len(module.tableaddrs)] = tableaddr
    module.store.tables[tableaddr] = table
    return tableaddr


def allocate_memory(
    module: WasmModule,
    size: WasmLimits,
) -> int:
    memaddr = _next_addr(module)
    mem = WasmMemoryInstance(size.minimum, size.maximum)
    module.memaddrs[len(module.memaddrs)] = memaddr
    module.store.mems[memaddr] = mem
    return memaddr


def allocate_external_memory(
    module: WasmModule,
    mem: WasmMemoryInstance,
) -> int:
    memaddr = _next_addr(module)
    module.memaddrs[len(module.memaddrs)] = memaddr
    module.store.mems[memaddr] = mem
    return memaddr


def allocate_global(
    module: WasmModule,
    section: WasmGlobalSection,
) -> int:
    globaddr = _next_addr(module)
    globl = WasmGlobalInstance()
    globl.mut = section.gt.m
    globl.value = cast(WASM_VALUE, interpret_wasm_section(section.e, module, module.store, {}, [section.gt.t])[0])
    module.globaladdrs[len(module.globaladdrs)] = globaddr
    module.store.globals_[globaddr] = globl
    return globaddr

def allocate_external_global(
    module: WasmModule,
    globl: WasmGlobalInstance,
) -> int:
    globaddr = _next_addr(module)
    module.globaladdrs[len(module.globaladdrs)] = globaddr
    module.store.globals_[globaddr] = globl
    return globaddr


def initialize_wasm_module(parsed: WasmParsedModule, externval: Dict[str, WASM_EXPORT_OBJECT]) -> WasmModule:
    """ (Initialization of) 4.5.3.8. Modules """
    assert parsed.version == 1
    sections: Dict[int, List[WASM_SECTION_TYPE]] = {}
    for sec in parsed.sections:
        if not sections[sec.section_id]:
            sections[sec.section_id] = []
        sections[sec.section_id].append(sec.section_content)
    types: List[WasmFunctionType] = [x for y in sections[1] for x in cast(List[WasmFunctionType], y)]
    impos: List[WasmImport] = [x for y in sections[2] for x in cast(List[WasmImport], y)]  # noqa: F841
    funcs: List[int] = [x for y in sections[3] for x in cast(List[int], y)]
    tabls: List[WasmTableType] = [x for y in sections[4] for x in cast(List[WasmTableType], y)]
    memrs: List[WasmLimits] = [x for y in sections[5] for x in cast(List[WasmLimits], y)]
    glbls: List[WasmGlobalSection] = [x for y in sections[6] for x in cast(List[WasmGlobalSection], y)]
    expts: List[WasmExport] = [x for y in sections[7] for x in cast(List[WasmExport], y)]  # noqa: F841
    strts: Optional[int] = cast(List[int], sections[8])[0]  # noqa: F841
    elems: List[WasmElemUnresolved] = [x for y in sections[9] for x in cast(List[WasmElemUnresolved], y)]  # noqa: F841
    codes: List[WasmCodeSection] = [x for y in sections[10] for x in cast(List[WasmCodeSection], y)]
    datum: List[WasmData] = [x for y in sections[11] for x in cast(List[WasmData], y)]  # noqa: F841

    # assert len(types) == len(funcs)
    assert len(funcs) == len(codes)

    ret_module = WasmModule()
    ret_module.store = WasmStore()

    func_addrs = []
    table_addrs = []
    mem_addrs = []
    global_addrs = []
    # allocate imported objects
    for _, v in sorted(externval.items()):
        if isinstance(v, Callable):
            func_addrs.append(allocate_host_function(ret_module, cast(WASM_HOST_FUNC, v)))
        elif isinstance(v, WasmTable):
            table_addrs.append(allocate_external_table(ret_module, v))
        elif isinstance(v, WasmMemoryInstance):
            mem_addrs.append(allocate_external_memory(ret_module, v))
        elif isinstance(v, WasmGlobalInstance):
            table_addrs.append(allocate_external_global(ret_module, v))

    # allocate local objects
    for funk, kode in zip(funcs, codes):
        func_addrs.append(allocate_function(ret_module, types[funk], funk, kode))

    for tabl in tabls:
        table_addrs.append(allocate_table(ret_module, tabl))

    for memr in memrs:
        mem_addrs.append(allocate_memory(ret_module, memr))

    for glbl in glbls:
        global_addrs.append(allocate_global(ret_module, glbl))

    return ret_module
