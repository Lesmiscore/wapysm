from typing import IO, Optional, Tuple, Union
from io import TextIOBase, SEEK_CUR

from .bufferedreader import BufferedTextReader
from .tree import SComponent, SLabel


SIO = Union[IO[str], TextIOBase]
NUMERIC_CHARS = tuple('+-0123456789.')

def read_str_typesafe(strm: SIO, size: int = -1) -> str:
    return strm.read(size) or ''

def peek_str_typesafe(strm: BufferedTextReader, size: int = 0) -> str:
    return (strm.peek(size) or '')[:size]

def _skip_blank_chars(strm: BufferedTextReader) -> str:
    while True:
        next_chr = peek_str_typesafe(strm, 1)
        if not next_chr:
            return next_chr
        if not next_chr.isspace():
            return next_chr
        strm.seek(1, SEEK_CUR)

def _read_until(strm: BufferedTextReader, cond) -> str:
    if isinstance(cond, (tuple, list, str)):
        _oldcond = cond
        cond = lambda x: x in _oldcond

    buf = ''
    while True:
        next_chr = peek_str_typesafe(strm, 1)
        if not next_chr:
            return buf
        if not cond(next_chr):
            return buf
        buf += next_chr
        strm.seek(1, SEEK_CUR)

def _read_next_token(strm: BufferedTextReader) -> Tuple[Optional[str], Optional[str]]:
    _skip_blank_chars(strm)
    first_chr = peek_str_typesafe(strm, 1)
    if not first_chr:
        return None, None
    elif first_chr == ')':
        # end of node
        strm.seek(1, SEEK_CUR)
        return 'node_end', ')'
    elif first_chr == '(':
        # begin of node
        strm.seek(1, SEEK_CUR)
        label = _read_until(strm, lambda x: x.isspage() or x in ('(', ")"))
        return 'node_begin', '(' + label
    elif first_chr == '$':
        # label token
        strm.seek(1, SEEK_CUR)
        label = _read_until(strm, lambda x: x.isspage())
        return 'label', '$' + label
    elif first_chr in NUMERIC_CHARS:
        # numeric literal
        value = _read_until(strm, lambda x: x.isspage())
        return 'numeric', value
    elif first_chr == '"':
        # string literal
        strm.seek(1, SEEK_CUR)
        buf = '"'
        escape = False
        while True:
            first_chr = read_str_typesafe(strm, 1)
            if first_chr == '\\':
                escape = not escape
            elif first_chr == '"' and not escape:
                buf += '"'
                return 'string', buf
            else:
                escape = False
            buf += first_chr
    else:
        raise ValueError(f'Faced invalid character: {first_chr}')

def parse_tree(strm: SIO) -> SComponent:
    return SLabel("")
