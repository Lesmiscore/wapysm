import io
from typing import List
from wapysm.parser.limitlength import LimitedRawIO
from wapysm.parser.binary.byteencode import read_byte, read_functype, read_leb128_unsigned, read_vector
from ...parser.module import WasmModule


class BinaryWasmModule(WasmModule):
    pass


class WasmSection():
    section_id: int
    section_content: object


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
        limited = LimitedRawIO(stream, section_id)

        if section_id == 1:  # type section
            section.section_content = read_vector(limited, read_functype)
        elif section_id == 2:  # import section
            section.section_content = stream.read(section_size)
        elif section_id == 3:  # function section
            section.section_content = stream.read(section_size)
        elif section_id == 4:  # table section
            section.section_content = stream.read(section_size)
        elif section_id == 5:  # memory section
            section.section_content = stream.read(section_size)
        elif section_id == 6:  # global section
            section.section_content = stream.read(section_size)
        elif section_id == 7:  # export section
            section.section_content = stream.read(section_size)
        elif section_id == 8:  # start section
            section.section_content = stream.read(section_size)
        elif section_id == 9:  # element section
            section.section_content = stream.read(section_size)
        elif section_id == 10:  # code section
            section.section_content = stream.read(section_size)
        elif section_id == 11:  # data section
            section.section_content = stream.read(section_size)
        else:  # custom section and undefined ID
            section.section_content = limited.read()


        sections.append(section)

    return sections

def parse_binary_wasm_module(stream: io.RawIOBase) -> BinaryWasmModule:
    module = BinaryWasmModule()
    return module
