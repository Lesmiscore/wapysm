import os
import sys
import unittest
import requests
# import logging

# logging.basicConfig(level=logging.DEBUG, force=True)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapysm.parser.binary.module import parse_binary_wasm_module

class TestParseBinaryWholeWasm(unittest.TestCase):
    def test_close_preopen_fd_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/close_preopen_fd.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_create_dir_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/create_dir.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_envvar_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/envvar.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_allocate_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_allocate.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_append_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_append.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_close_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_close.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_pread_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_pread.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_read_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_read.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fd_sync_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fd_sync.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_file_metadata_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/file_metadata.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fs_sandbox_test_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fs_sandbox_test.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_fseek_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/fseek.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_hello_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/hello.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_isatty_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/isatty.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_mapdir_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/mapdir.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_mapdir_with_leading_slash_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/mapdir_with_leading_slash.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_path_link_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/path_link.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_path_rename_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/path_rename.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_path_symlink_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/path_symlink.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_pipe_reverse_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/pipe_reverse.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_poll_oneoff_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/poll_oneoff.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_quine_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/quine.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_readlink_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/readlink.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_unix_open_special_files_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/unix_open_special_files.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_wasi_sees_virtual_root_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/wasi_sees_virtual_root.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)

    def test_writing_wasm(self):
        with requests.get(
                'https://raw.githubusercontent.com/wasmerio/wasmer/master/tests/wasi-wast/wasi/unstable/writing.wasm', stream=True) as r:
            parse_binary_wasm_module(r.raw)
