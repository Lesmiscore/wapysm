from typing import Dict, List, Optional, cast
from wapysm.parser.structure import VALTYPE_TYPE, WasmFunctionType, WasmLimits, WasmTableType
from ..execute.context import WASM_HOST_FUNC
from ..parser.module import WASM_SECTION_TYPE, WasmCodeSection, WasmData, WasmElemUnresolved, WasmExport, WasmFunction, WasmGlobalSection, WasmImport, WasmModule, WasmParsedModule, WasmType


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
    locals = cast(List[VALTYPE_TYPE], [x[1] for x in sorted(code.code.code_locals)])
    module.types[typeidx] = WasmType(functype.argument_types, functype.return_types, code.code.expr)
    module.funcs[funcaddr] = WasmFunction(module, typeidx, locals, code.code.expr)
    return funcaddr


def initialize_wasm_module(parsed: WasmParsedModule, imports: Dict[str, WASM_HOST_FUNC]) -> WasmModule:
    """ (Initialization of) 4.5.3.8. Modules """
    assert parsed.version == 1
    sections: Dict[int, List[WASM_SECTION_TYPE]] = {}
    for sec in parsed.sections:
        if not sections[sec.section_id]:
            sections[sec.section_id] = []
        sections[sec.section_id].append(sec.section_content)
    types: List[WasmFunctionType] = [x for y in sections[1] for x in y]
    impos: List[WasmImport] = [x for y in sections[2] for x in y]  # noqa: F841
    funcs: List[int] = [x for y in sections[3] for x in y]
    tabls: List[WasmTableType] = [x for y in sections[4] for x in y]  # noqa: F841
    memrs: List[WasmLimits] = [x for y in sections[5] for x in y]  # noqa: F841
    glbls: List[WasmGlobalSection] = [x for y in sections[6] for x in y]  # noqa: F841
    expts: List[WasmExport] = [x for y in sections[7] for x in y]  # noqa: F841
    strts: Optional[int] = cast(List[int], sections[8])[0]  # noqa: F841
    elems: List[WasmElemUnresolved] = [x for y in sections[9] for x in y]  # noqa: F841
    codes: List[WasmCodeSection] = [x for y in sections[10] for x in y]
    datum: List[WasmData] = [x for y in sections[11] for x in y]  # noqa: F841

    assert len(types) == len(funcs)
    assert len(funcs) == len(codes)

    ret_module = WasmModule()

    func_addrs = []
    for funk, kode in zip(funcs, codes):
        func_addrs.append(allocate_function(ret_module, types[funk], funk, kode))
