from typing import List
from .base import BitPacking, bits_needed

class BitPackingOverlap(BitPacking):
    # allows spanning across 32-bit words
    def compress(self, arr: List[int]) -> None:
        self.n = len(arr)
        self.k = max(1, max(bits_needed(x) for x in arr) if arr else 1)
        self.words = []
        bitpos = 0
        for v in arr:
            self._write_bits(bitpos, self.k, v)
            bitpos += self.k

    def decompress(self, out_len: int) -> List[int]:
        res = []
        bitpos = 0
        for _ in range(out_len):
            res.append(self._read_bits(bitpos, self.k))
            bitpos += self.k
        return res

    def get(self, i: int) -> int:
        return self._read_bits(i * self.k, self.k)
