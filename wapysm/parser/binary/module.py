import io
from typing import List, Union
from ...opcode import InstructionBase
from ...parser.binary.byteencode import read_byte, read_bytes_typesafe, read_functype, read_globaltype, read_int32_le, read_leb128_unsigned, read_memtype, read_tabletype, read_utf8, read_valtype, read_vector, read_vector_bytes
from ...parser.binary.opcode import read_instructions
from ...parser.limitlength import LimitedRawIO
from ...parser.module import WasmData, WasmElemUnresolved, WasmExport, WasmImport, WasmModule
from ...parser.structure import VALTYPE_TYPE, WasmFunctionType, WasmGlobalType, WasmLimits, WasmTableType


class BinaryWasmModule(WasmModule):
    pass


class WasmCodeFunction():
    code_locals: List[List[VALTYPE_TYPE]]
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


def read_binary_import(stream: io.RawIOBase) -> WasmImport:
    "5.5.5 Import Section"

    wim = WasmImport()
    wim.module = read_utf8(stream)
    wim.name = read_utf8(stream)

    importdesc_type = read_byte(stream)
    if importdesc_type == 0x00:
        wim.importdesc = read_leb128_unsigned(stream)
    elif importdesc_type == 0x01:
        wim.importdesc = read_tabletype(stream)
    elif importdesc_type == 0x02:
        wim.importdesc = read_memtype(stream)
    elif importdesc_type == 0x03:
        wim.importdesc = read_globaltype(stream)

    return wim

def read_global_section(stream: io.RawIOBase) -> WasmGlobalSection:
    sect = WasmGlobalSection()
    sect.gt = read_globaltype(stream)
    sect.e = read_instructions(stream)
    return sect

def read_binary_export(stream: io.RawIOBase) -> WasmExport:
    "5.5.10 Export Section"

    wex = WasmExport()
    wex.name = read_utf8(stream)

    exportdesc_type_int = read_byte(stream)
    if exportdesc_type_int == 0x00:  # exportdesc is func
        wex.exportdesc_type = 'func'
    elif exportdesc_type_int == 0x01:  # exportdesc is table
        wex.exportdesc_type = 'table'
    elif exportdesc_type_int == 0x02:  # exportdesc is mem
        wex.exportdesc_type = 'mem'
    elif exportdesc_type_int == 0x03:  # exportdesc is global
        wex.exportdesc_type = 'global'
    wex.exportdesc_idx = read_leb128_unsigned(stream)

    return wex

def read_binary_elem(stream: io.RawIOBase) -> WasmElemUnresolved:
    "5.5.12 Element Section"

    tableidx = read_leb128_unsigned(stream)
    expr = read_instructions(stream)
    init = read_vector(stream, read_leb128_unsigned)
    return WasmElemUnresolved(tableidx, expr, init)

def read_binary_code_function(stream: io.RawIOBase) -> WasmCodeFunction:
    wcode = WasmCodeFunction()

    def read_locals_nested(stream: io.RawIOBase) -> List[VALTYPE_TYPE]:
        return read_vector(stream, read_valtype)

    wcode.code_locals = read_vector(stream, read_locals_nested)
    return wcode

def read_binary_code_section(stream: io.RawIOBase) -> WasmCodeSection:
    wcode = WasmCodeSection()
    wcode.size = read_leb128_unsigned(stream)
    wcode.code = read_binary_code_function(stream)
    return wcode

def read_binary_data_section(stream: io.RawIOBase) -> WasmData:
    memidx = read_leb128_unsigned(stream)
    expr = read_instructions(stream)
    data = read_vector_bytes(stream)
    return WasmData(memidx, expr, data)

def parse_binary_wasm_sections(stream: io.RawIOBase) -> List[WasmSection]:
    sections: List[WasmSection] = []
    while True:
        try:
            section_id = read_byte(stream)
        except AssertionError:
            break
        section_size: int = read_leb128_unsigned(stream)

        section = WasmSection()
        section.section_id = section_id
        limited = LimitedRawIO(stream, section_size)

        if section_id == 1:  # type section
            section.section_content = read_vector(limited, read_functype)
        elif section_id == 2:  # import section
            section.section_content = read_vector(limited, read_binary_import)
        elif section_id == 3:  # function section
            section.section_content = read_vector(limited, read_leb128_unsigned)
        elif section_id == 4:  # table section
            section.section_content = read_vector(limited, read_tabletype)
        elif section_id == 5:  # memory section
            section.section_content = read_vector(limited, read_memtype)
        elif section_id == 6:  # global section
            section.section_content = read_vector(limited, read_global_section)
        elif section_id == 7:  # export section
            section.section_content = read_vector(limited, read_binary_export)
        elif section_id == 8:  # start section
            section.section_content = read_vector(limited, read_leb128_unsigned)
        elif section_id == 9:  # element section
            section.section_content = read_vector(limited, read_binary_elem)
        elif section_id == 10:  # code section
            section.section_content = read_vector(limited, read_binary_code_section)
        elif section_id == 11:  # data section
            section.section_content = read_vector(limited, read_binary_data_section)
        else:  # custom section and undefined ID
            section.section_content = read_bytes_typesafe(limited)


        sections.append(section)

    return sections

def parse_binary_wasm_module(stream: io.RawIOBase) -> BinaryWasmModule:
    magic = read_bytes_typesafe(stream, 4)
    if magic != b'\x00asm':
        raise Exception('Input does not have valid WASM header')
    version = read_int32_le(stream)
    if version != 1:
        raise Exception(f'Version {version} is not supported')

    module = BinaryWasmModule()
    sections = parse_binary_wasm_sections(stream)  # noqa: F841
    return module
