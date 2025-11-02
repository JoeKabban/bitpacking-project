from abc import ABC, abstractmethod
from typing import List, Tuple

def bits_needed(x: int) -> int:
    return 1 if x == 0 else x.bit_length()

class BitPacking(ABC):
    def __init__(self):
        self.n = 0
        self.k = 0
        self.words: List[int] = []

    @abstractmethod
    def compress(self, arr: List[int]) -> None: ...

    @abstractmethod
    def decompress(self, out_len: int) -> List[int]: ...

    @abstractmethod
    def get(self, i: int) -> int: ...

    
    def _ensure(self, idx: int):
        while len(self.words) <= idx:
            self.words.append(0)

    def _write_bits(self, bitpos: int, width: int, value: int):
        widx = bitpos // 32
        woff = bitpos % 32
        self._ensure(widx)
        take = min(width, 32 - woff)
        mask = (1 << take) - 1
        self.words[widx] |= (value & mask) << woff
        remain = width - take
        if remain > 0:
            self._ensure(widx + 1)
            self.words[widx + 1] |= (value >> take) & ((1 << remain) - 1)

    def _read_bits(self, bitpos: int, width: int) -> int:
        widx = bitpos // 32
        woff = bitpos % 32
        low = 0
        if widx < len(self.words):
            low = self.words[widx] >> woff
        hi = 0
        if woff + width > 32 and (widx + 1) < len(self.words):
            hi_bits = (self.words[widx + 1] & ((1 << ((woff + width) - 32)) - 1))
            low |= hi_bits << (32 - woff)
        return low & ((1 << width) - 1)
