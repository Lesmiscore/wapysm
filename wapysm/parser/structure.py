from typing import Dict, List, Optional, Union, Literal

VALTYPE_NUMBERS = Literal[0x7f, 0x7e, 0x7d, 0x7c]
VALTYPE_STRINGS = Literal['i32', 'i64', 'f32', 'f64']

VALTYPE_TYPE = Union[VALTYPE_NUMBERS, VALTYPE_STRINGS]

TYPES_TO_TYPENUMBER: Dict[VALTYPE_TYPE, VALTYPE_NUMBERS] = {
    0x7f: 0x7f, 'i32': 0x7f,
    0x7e: 0x7e, 'i64': 0x7e,
    0x7d: 0x7d, 'f32': 0x7d,
    0x7c: 0x7c, 'f64': 0x7c,
}

TYPES_TO_TYPENAME: Dict[VALTYPE_TYPE, VALTYPE_STRINGS] = {
    0x7f: 'i32', 'i32': 'i32',
    0x7e: 'i64', 'i64': 'i64',
    0x7d: 'f32', 'f32': 'f32',
    0x7c: 'f64', 'f64': 'f64',
}

class WasmFunctionType():
    argument_types: List[VALTYPE_TYPE] = []
    return_types: List[VALTYPE_TYPE] = []

    def __init__(self, argument_types: List[VALTYPE_TYPE], return_types: List[VALTYPE_TYPE]) -> None:
        self.argument_types = argument_types
        self.return_types = return_types

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, WasmFunctionType):
            return False
        return self.return_types == o.return_types and self.argument_types == o.argument_types

class WasmLimits():
    minimum: int = 0
    maximum: Optional[int] = None

    def __init__(self, minimum: int, maximum: Optional[int]) -> None:
        self.minimum = minimum
        self.maximum = maximum


class WasmTableType():
    lim: WasmLimits  # = WasmLimits(0, None)
    elemtype: int = 0

    def __init__(self, elemtype: int, lim: WasmLimits) -> None:
        self.lim = lim
        self.elemtype = elemtype


class WasmGlobalType():
    t: VALTYPE_TYPE = 'i32'
    m: bool = False  # True for var (mutable), False for const(ant)

    def __init__(self, t: VALTYPE_TYPE, m: bool) -> None:
        self.t = t
        self.m = m
