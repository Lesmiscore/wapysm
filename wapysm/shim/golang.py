# https://github.com/golang/go/blob/master/misc/wasm/wasm_exec.js

# import threading
import secrets
import os
import sys
import time

from math import isnan
from typing import Callable, Dict, List, cast
from .utils import reflect_delete_prop, reflect_get, reflect_set
from ..execute.interpreter.invocation import wrap_function
from ..execute.utils import WASM_VALUE
from ..execute.context import WasmFunctionInstance, WasmMemoryInstance, WasmModule, WasmStore

NAN_HEAD = 0x7FF80000

class Go():
    mem: WasmMemoryInstance
    _values: list
    _go_ref_counts: list
    _ids: dict
    _id_pool: list
    _inst: WasmModule
    exited: bool

    def __init__(self) -> None:
        self.argv = ('js',)
        self.env = {}
        # exit
        self._pending_event = None
        self._scheduled_timeouts = {}
        self._next_callback_timeout_id = 1

        def load_value(addr: int):
            # it's always little endian
            f = self.mem.get_float64(addr)
            if f == 0:
                return None
            if not isnan(f):
                return f

            value_id = self.mem.get_int32(addr)
            return self._values[value_id]

        def store_value(addr: int, v):
            if isinstance(v, (int, float)) and v != 0:
                if isnan(v):
                    self.mem.set_int32(addr + 4, NAN_HEAD)
                    self.mem.set_int32(addr, 0)
                else:
                    self.mem.set_float64(addr, v)
                return

            if v is None:
                self.mem.set_float64(addr, 0)
                return

            fhv = id(v)
            if fhv in self._ids:
                obj_id = self._ids[fhv]
            else:
                if self._id_pool:
                    obj_id = self._id_pool.pop()
                else:
                    obj_id = len(self._values)
                self._values[obj_id] = v
                self._go_ref_counts[obj_id] = 0
                self._ids[fhv] = obj_id

            self._go_ref_counts[obj_id] += 1

            type_flag = 0
            if isinstance(v, (dict, list)):
                type_flag = 1
            elif isinstance(v, (str, bytes)):
                type_flag = 2
            # elif isinstance(v, Symbol):
            #     type_flag = 3
            elif isinstance(v, (Callable, WasmFunctionInstance)):
                type_flag = 4
            self.mem.set_int32(addr + 4, NAN_HEAD or type_flag)
            self.mem.set_int32(addr, obj_id)

        def load_slice(addr: int) -> bytearray:
            begin = self.mem.get_int64(addr)
            length = self.mem.get_int64(addr + 8)
            return self.mem.trim(begin, length)

        def load_slice_of_values(addr) -> list:
            begin = self.mem.get_int64(addr)
            length = self.mem.get_int64(addr + 8)
            a = []
            for i in range(length):
                a.append(load_value(begin + i * 8))
            return a

        def load_string(addr) -> str:
            begin = self.mem.get_int64(addr)
            length = self.mem.get_int64(addr + 8)
            return self.mem.trim(begin, length).decode()

        def _golangimport_runtime_wasmexit(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            code = self.mem.get_int32(sp + 8)
            self.exited = True
            delattr(self, '_inst')
            delattr(self, '_values')
            delattr(self, '_goRefCounts')
            delattr(self, '_ids')
            delattr(self, '_idPool')
            self.exit(code)

        def _golangimport_runtime_wasmwrite(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            fd = self.mem.get_int64(sp + 8)
            p = self.mem.get_int64(sp + 16)
            n = self.mem.get_int32(sp + 24)

            os.write(fd, bytes(self.mem.trim(p, n)))

        def _golangimport_runtime_resetmemorydataview(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            # sp = int(args[0][2])
            self.mem = ws.mems[0]

        def _golangimport_runtime_nanotime1(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            self.mem.set_int64(sp + 8, time.time_ns())

        def _golangimport_runtime_walltime(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            time_ms = time.time_ns() / 1000
            self.mem.set_int64(sp + 8, int(time_ms / 1000))
            self.mem.set_int32(sp + 16, int((time_ms % 1000) * 1000000))

        def _golangimport_runtime_scheduletimeoutevent(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            ctid = self._next_callback_timeout_id
            self._next_callback_timeout_id += 1

            def timeout_callback():
                self._resume()
                while ctid in self._scheduled_timeouts:
                    sys.stderr.write('scheduleTimeoutEvent: missed timeout event\n')
                    self._resume()

            self._scheduled_timeouts[ctid] = self.setTimeout(timeout_callback, self.mem.get_int64(sp + 8) + 1)
            self.mem.set_int32(sp + 16, ctid)

        def _golangimport_runtime_cleartimeoutevent(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            ctid = self.mem.get_int32(sp + 8)
            self.clearTimeout(self._scheduled_timeouts[ctid])

        def _golangimport_runtime_getrandomdata(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            sl = load_slice(sp + 8)
            sl[:] = secrets.token_bytes(len(sl))

        def _golangimport_syscall_js_finalizeref(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            ctid = self.mem.get_int32(sp + 8)
            self._go_ref_counts[ctid] -= 1
            if self._go_ref_counts[ctid] == 0:
                v = self._values[ctid]
                del self._values[ctid]
                del self._go_ref_counts[ctid]
                del self._ids[id(v)]
                del self._id_pool[ctid]

        def _golangimport_syscall_js_stringval(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            store_value(sp + 24, load_string(sp + 8))

        def _golangimport_syscall_js_valueget(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            result = reflect_get(load_value(sp + 8), load_string(sp + 16))
            sp_raw = wrap_function(cast(WasmFunctionInstance, self._inst.named_exports['getsp']), self._inst.store)()
            assert sp_raw
            sp = int(sp_raw[2])
            store_value(sp + 32, result)

        def _golangimport_syscall_js_valueset(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            reflect_set(load_value(sp + 8), load_string(sp + 16), load_value(sp + 32))

        def _golangimport_syscall_js_valuedelete(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            reflect_delete_prop(load_value(sp + 8), load_string(sp + 16))

        def _golangimport_syscall_js_valueindex(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            store_value(sp + 24, reflect_get(load_value(sp + 8), self.mem.get_int64(sp + 16)))

        def _golangimport_syscall_js_valuesetindex(ws: WasmStore, wm: WasmModule, lc: Dict[int, WASM_VALUE], args: List[WASM_VALUE]):
            sp = int(args[0][2])
            reflect_set(load_value(sp + 8), self.mem.get_int64(sp + 16), load_value(sp + 24))

        # imcomplete

        self.import_object = {
            'go': {
                'runtime.wasmExit': _golangimport_runtime_wasmexit,
                'runtime.wasmWrite': _golangimport_runtime_wasmwrite,
                'runtime.resetMemoryDataView': _golangimport_runtime_resetmemorydataview,
                'runtime.nanotime1': _golangimport_runtime_nanotime1,
                'runtime.walltime': _golangimport_runtime_walltime,
                'runtime.scheduleTimeoutEvent': _golangimport_runtime_scheduletimeoutevent,
                'runtime.clearTimeoutEvent': _golangimport_runtime_cleartimeoutevent,
                'runtime.getRandomData': _golangimport_runtime_getrandomdata,
                'syscall/js.finalizeRef': _golangimport_syscall_js_finalizeref,
                'syscall/js.stringVal': _golangimport_syscall_js_stringval,
                'syscall/js.valueGet': _golangimport_syscall_js_valueget,
                'syscall/js.valueSet': _golangimport_syscall_js_valueset,
                'syscall/js.valueDelete': _golangimport_syscall_js_valuedelete,
                'syscall/js.valueIndex': _golangimport_syscall_js_valueindex,
                'syscall/js.valueSetIndex': _golangimport_syscall_js_valuesetindex,
            }
        }

    def exit(self, code):
        if code != 0:
            print('exit code:', code)


    def setTimeout(self, callback, timeout, *args):
        pass

    def clearTimeout(self, id):
        pass
