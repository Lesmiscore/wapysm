import io
from typing import Optional


class LimitedRawIO(io.RawIOBase):
    def __init__(self, base: io.RawIOBase, length: int) -> None:
        super().__init__()
        self.base = base
        self.length = length
        self.remaining = length

    def read(self, __size: int = -1) -> Optional[bytes]:
        if self.remaining < 0:
            return b''
        if __size == -1:
            return self.readall()
        if self.remaining < __size:
            __size = self.remaining
        result = self.base.read(__size)
        if not result:
            return result
        self.remaining -= len(result)
        return result

    def readall(self) -> bytes:
        if self.remaining < 0:
            return b''
        result = self.base.read(self.remaining)
        if not result:
            return b''
        self.remaining = 0
        return result
