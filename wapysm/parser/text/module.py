import subprocess
from io import BytesIO
from typing import cast, IO
from ...execute.context import WasmParsedModule
from ..binary.module import parse_binary_wasm_module


# trollface drawn here

def convert_text_to_binary(input: IO[str]) -> IO[bytes]:
    proc = subprocess.Popen(
        ['wat2wasm', '-', '-o', '/dev/stdout'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    cast(IO[bytes], proc.stdin).write(input.read().encode('utf-8'))
    return BytesIO(cast(IO[bytes], proc.stdout).read())


def parse_text_wasm_module(stream: IO[str]) -> WasmParsedModule:
    return parse_binary_wasm_module(convert_text_to_binary(stream))
