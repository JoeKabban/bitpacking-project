from typing import List
from .base import BitPacking, bits_needed

class BitPackingNoOverlap(BitPacking):
    
    def compress(self, arr: List[int]) -> None:
        self.n = len(arr)
        self.k = max(1, max(bits_needed(x) for x in arr) if arr else 1)
        per_word = max(1, 32 // self.k)
        self.words = []
        widx, slot = 0, 0
        self._ensure(0)
        for v in arr:
            if slot == per_word:
                widx += 1
                slot = 0
                self._ensure(widx)
            pos = slot * self.k
            self.words[widx] |= (v & ((1 << self.k) - 1)) << pos
            slot += 1

    def decompress(self, out_len: int) -> List[int]:
        res: List[int] = []
        per_word = max(1, 32 // self.k)
        mask = (1 << self.k) - 1
        for i in range(out_len):
            widx = i // per_word
            slot = i % per_word
            word = self.words[widx] if widx < len(self.words) else 0
            res.append((word >> (slot * self.k)) & mask)
        return res

    def get(self, i: int) -> int:
        per_word = max(1, 32 // self.k)
        mask = (1 << self.k) - 1
        widx = i // per_word
        slot = i % per_word
        word = self.words[widx]
        return (word >> (slot * self.k)) & mask
