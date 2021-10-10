from typing import Callable, Dict, List, Optional, Union, cast
from ..execute.utils import WASM_VALUE, lenlen, trap
from ..execute.interpreter.runner import interpret_wasm_section, invoke_wasm_function
from ..execute.context import WASM_EXPORT_OBJECT, WASM_HOST_FUNC, WasmGlobalInstance, WasmHostFunctionInstance, WasmLocalFunctionInstance, WasmMemoryInstance, WasmStore
from ..parser.structure import WasmFunctionType, WasmLimits, WasmTableType
from .context import WASM_PAGE_SIZE, WASM_SECTION_TYPE, WasmCodeSection, WasmData, WasmElemUnresolved, WasmExport, WasmExportValue, WasmFunction, WasmFunctionInstance, WasmGlobalSection, WasmImport, WasmModule, WasmParsedModule, WasmTable, WasmType


def _next_addr(module: WasmModule) -> int:
    current = getattr(module, '__addrs', 0)
    alloc = current + 1
    setattr(module, '__addrs', alloc)
    return alloc


def allocate_function(
    module: WasmModule,
    functype: WasmFunctionType,
    typeidx: int,
    code: WasmCodeSection,
) -> int:
    funcaddr = _next_addr(module)
    wf = WasmFunction(module, typeidx, code.code.code_locals, code.code.expr)
    localfunc = WasmLocalFunctionInstance()
    localfunc.module = module
    localfunc.wf = wf
    localfunc.functype = WasmType(functype.argument_types, functype.return_types, code.code.expr)
    module.types[typeidx] = localfunc.functype
    module.funcaddrs[len(module.funcaddrs)] = funcaddr
    module.store.funcs[funcaddr] = localfunc
    return funcaddr


def allocate_host_function(
    module: WasmModule,
    code: Union[WASM_HOST_FUNC, WasmFunctionInstance],
) -> int:
    funcaddr = _next_addr(module)
    if isinstance(code, WasmFunctionInstance):
        localfunc = code
    else:
        localfunc = WasmHostFunctionInstance()
        localfunc.hostfunc = code
        localfunc.functype = WasmType([], ['i32'], [])
    module.funcaddrs[len(module.funcaddrs)] = funcaddr
    module.store.funcs[funcaddr] = localfunc
    return funcaddr


def allocate_table(
    module: WasmModule,
    tbl: WasmTableType,
) -> int:
    tableaddr = _next_addr(module)
    table = WasmTable(tbl.elemtype, tbl.lim)
    table.elem_addrs = {n: 0 for n in range(tbl.lim.minimum)}
    module.tableaddrs[len(module.tableaddrs)] = tableaddr
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


def initialize_wasm_module(parsed: WasmParsedModule, externval: Dict[str, Dict[str, WASM_EXPORT_OBJECT]]) -> WasmModule:
    """ (Initialization of) 4.5.3.8. Modules """
    assert parsed.version == 1
    sections: Dict[int, List[WASM_SECTION_TYPE]] = {}
    for s in range(12):
        sections[s] = []
    for sec in parsed.sections:
        sections[sec.section_id].append(sec.section_content)
    types: List[WasmFunctionType] = [x for y in sections[1] for x in cast(List[WasmFunctionType], y)]
    impts: List[WasmImport] = [x for y in sections[2] for x in cast(List[WasmImport], y)]  # noqa: F841
    funcs: List[int] = [x for y in sections[3] for x in cast(List[int], y)]
    tabls: List[WasmTableType] = [x for y in sections[4] for x in cast(List[WasmTableType], y)]
    memrs: List[WasmLimits] = [x for y in sections[5] for x in cast(List[WasmLimits], y)]
    glbls: List[WasmGlobalSection] = [x for y in sections[6] for x in cast(List[WasmGlobalSection], y)]
    expts: List[WasmExport] = [x for y in sections[7] for x in cast(List[WasmExport], y)]
    codes: List[WasmCodeSection] = [x for y in sections[10] for x in cast(List[WasmCodeSection], y)]

    # assert len(types) == len(funcs)
    assert len(funcs) == len(codes)
    assert len(impts) < lenlen(externval)

    ret_module = WasmModule()
    ret_module.store = WasmStore()

    func_addrs = []
    table_addrs = []
    mem_addrs = []
    global_addrs = []
    # allocate imported objects
    for imp in impts:
        v = externval[imp.module][imp.name]
        if isinstance(v, Callable):
            func_addrs.append(allocate_host_function(ret_module, cast(WASM_HOST_FUNC, v)))
        elif isinstance(v, WasmFunctionInstance):
            func_addrs.append(allocate_host_function(ret_module, v))
        elif isinstance(v, WasmTable):
            table_addrs.append(allocate_external_table(ret_module, v))
        elif isinstance(v, WasmMemoryInstance):
            mem_addrs.append(allocate_external_memory(ret_module, v))
        elif isinstance(v, WasmGlobalInstance):
            global_addrs.append(allocate_external_global(ret_module, v))

    # allocate local objects
    for funk, kode in zip(funcs, codes):
        func_addrs.append(allocate_function(ret_module, types[funk], funk, kode))

    for tabl in tabls:
        table_addrs.append(allocate_table(ret_module, tabl))

    for memr in memrs:
        mem_addrs.append(allocate_memory(ret_module, memr))

    for glbl in glbls:
        global_addrs.append(allocate_global(ret_module, glbl))

    # process exports
    for exp in expts:
        wme = WasmExportValue()
        wme.exportdesc_type = exp.exportdesc_type
        wme.exportdesc_idx = exp.exportdesc_idx
        wme.name = exp.name
        if exp.exportdesc_type == 'func':
            wme.value = ret_module.store.funcs[func_addrs[exp.exportdesc_idx]]
        elif exp.exportdesc_type == 'table':
            wme.value = ret_module.store.tables[table_addrs[exp.exportdesc_idx]]
        elif exp.exportdesc_type == 'mem':
            wme.value = ret_module.store.mems[mem_addrs[exp.exportdesc_idx]]
        elif exp.exportdesc_type == 'global':
            wme.value = ret_module.store.globals_[global_addrs[exp.exportdesc_idx]]
        ret_module.exports[len(ret_module.exports)] = wme

    # D O N E
    return ret_module


def instantiate_wasm_module(module: WasmModule, parsed: WasmParsedModule, externval: Dict[str, Dict[str, WASM_EXPORT_OBJECT]]):
    """ (Instantiation of) 4.5.3.8. Modules """

    sections: Dict[int, List[WASM_SECTION_TYPE]] = {}
    for s in range(12):
        sections[s] = []
    for sec in parsed.sections:
        sections[sec.section_id].append(sec.section_content)
    strts: Optional[int] = cast(int, next(iter(sections[8]), None))  # noqa: F841
    elems: List[WasmElemUnresolved] = [x for y in sections[9] for x in cast(List[WasmElemUnresolved], y)]  # noqa: F841
    datum: List[WasmData] = [x for y in sections[11] for x in cast(List[WasmData], y)]  # noqa: F841

    # 4. ?
    for addr, exp in module.exports.items():
        if exp.exportdesc_type == 'func' and not isinstance(exp.value, WasmFunctionInstance):
            trap(f'addr {addr}: {exp.exportdesc_type} expected but {exp.value}')
        elif exp.exportdesc_type == 'table' and not isinstance(exp.value, WasmTable):
            trap(f'addr {addr}: {exp.exportdesc_type} expected but {exp.value}')
        elif exp.exportdesc_type == 'mem' and not isinstance(exp.value, WasmMemoryInstance):
            trap(f'addr {addr}: {exp.exportdesc_type} expected but {exp.value}')
        elif exp.exportdesc_type == 'global' and not isinstance(exp.value, WasmGlobalInstance):
            trap(f'addr {addr}: {exp.exportdesc_type} expected but {exp.value}')

    eo: List[int] = []
    for elem in elems:
        eoval_wv, _ = interpret_wasm_section(elem.offset, module, module.store, {}, ['i32'])
        assert eoval_wv
        assert eoval_wv[0] == 'i', eoval_wv[1] == 32
        eoval = eoval_wv[2]
        eo.append(cast(int, eoval))
        tableidx = elem.tableidx
        tableaddr = module.tableaddrs[tableidx]
        tableinst = module.store.tables[tableaddr]
        eend = eoval + len(elem.init)
        if eend > len(tableinst.elem_addrs):
            trap(f'eend > len(tableinst.elem): {eend} > {len(tableinst.elem_addrs)}')

    do = []
    for data in datum:
        doval_wv, _ = interpret_wasm_section(data.offset, module, module.store, {}, ['i32'])
        assert doval_wv
        assert doval_wv[0] == 'i', doval_wv[1] == 32
        doval = doval_wv[2]
        do.append(cast(int, doval))
        memidx = data.memidx
        memaddr = module.memaddrs[memidx]
        meminst = module.store.mems[memaddr]
        dend = doval + len(data.init)
        if dend > len(meminst) * WASM_PAGE_SIZE:
            trap(f'dend > len(meminst) * WASM_PAGE_SIZE: {dend} > {len(meminst) * WASM_PAGE_SIZE}')


    for idx, elem in enumerate(elems):
        tableidx = elem.tableidx
        tableaddr = module.tableaddrs[tableidx]
        tableinst = module.store.tables[tableaddr]
        for jdx, funcidx in enumerate(elem.init):
            funcaddr = module.funcaddrs[funcidx]
            tableinst.elem_addrs[eo[idx] + jdx] = funcaddr
            tableinst.elem[eo[idx] + jdx] = module.store.funcs[funcaddr]

    for idx, data in enumerate(datum):
        memidx = data.memidx
        memaddr = module.memaddrs[memidx]
        meminst = module.store.mems[memaddr]
        for jdx, b in enumerate(data.init):
            meminst[do[idx] + jdx] = b

    if strts is not None:
        # start section itself is funcaddr for now
        funcaddr = module.funcaddrs[strts]
        func = module.store.funcs[funcaddr]
        invoke_wasm_function(func, module, module.store, [], [], [])
