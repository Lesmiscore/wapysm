from typing import IO, Dict, Union
from io import BytesIO

from .execute.interpreter.invocation import wrap_function
from .execute.initialization import initialize_wasm_module, instantiate_wasm_module
from .execute.context import WASM_EXPORT_OBJECT, WasmFunctionInstance, WasmModule, WasmParsedModule
from .parser.binary.module import parse_binary_wasm_module


class WebAssembly:
    """
    WebAssembly class as in JavaScript global object.
    Method names are converted to snake case.
    """

    def __init__(self, wmod: WasmModule, parsed_module: WasmParsedModule) -> None:
        self.module = wmod
        self.raw_module = parsed_module

        # filter only functions
        self.exports = {v.name: wrap_function(v.value, wmod.store) for k, v in wmod.exports.items() if isinstance(v.value, WasmFunctionInstance)}


    @staticmethod
    def instantiate(buffer_source: Union[bytearray, bytes], import_object: Dict[str, Dict[str, WASM_EXPORT_OBJECT]]) -> 'WebAssembly':
        """
        https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/instantiate
        """
        return WebAssembly.instantiate_streaming(BytesIO(buffer_source), import_object)

    @staticmethod
    def instantiate_streaming(source: IO[bytes], import_object: Dict[str, Dict[str, WASM_EXPORT_OBJECT]]) -> 'WebAssembly':
        """
        https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/instantiateStreaming
        """
        parsed_module = parse_binary_wasm_module(source)
        module = initialize_wasm_module(parsed_module, import_object)
        instantiate_wasm_module(module, parsed_module, import_object)
        return WebAssembly(module, parsed_module)

    @staticmethod
    def compile(buffer_source: Union[bytearray, bytes]) -> WasmParsedModule:
        """
        https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/compile
        """
        return WebAssembly.compile_streaming(BytesIO(buffer_source))

    @staticmethod
    def compile_streaming(source: IO[bytes]) -> WasmParsedModule:
        """
        https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/compileStreaming
        """
        return parse_binary_wasm_module(source)
