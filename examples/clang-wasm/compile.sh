#!/bin/bash
# https://depth-first.com/articles/2019/10/16/compiling-c-to-webassembly-and-running-it-without-emscripten/
# https://surma.dev/things/c-to-webassembly/
# https://stackoverflow.com/questions/45146099/how-do-i-compile-a-c-file-to-webassembly
# https://github.com/WebAssembly/wasi-sdk
export WASI_VERSION=12
export WASI_VERSION_FULL=${WASI_VERSION}.0
export WASI_SDK_PATH=/mnt/extra-storage/wasi-sdk/wasi-sdk-"${WASI_VERSION_FULL}"
export CC="${WASI_SDK_PATH}/bin/clang --sysroot=${WASI_SDK_PATH}/share/wasi-sysroot"

set -xe
$CC script.c --compile --target=wasm32-unknown-unknown-wasm \
    --optimize=3 --output script.o
${WASI_SDK_PATH}/bin/wasm-ld --export=gauss_legendre --entry=_start --allow-undefined -o script.wasm script.o
wasm-dis script.wasm
