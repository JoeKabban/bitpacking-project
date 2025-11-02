from typing import List, Tuple
from .base import BitPacking, bits_needed

class BitPackingOverflow(BitPacking):
    """
    Fixed-width units: 1 flag bit + DATA bits.
    flag=0 -> store small value in DATA bits (k_small)
    flag=1 -> store index into overflow list in DATA bits
    DATA = max(k_small, ceil_log2(m_overflow)) so every unit is same width.
    """
    def __init__(self, k_small: int | None = None):
        super().__init__()
        self.k_small_req = k_small
        self.data_bits = 0
        self.k_small = 0
        self.m_overflow = 0
        self.overflow: List[int] = []

    def _prep_scheme(self, arr: List[int]) -> None:
        if self.k_small_req is not None:
            self.k_small = self.k_small_req
        else:
            
            self.k_small = min(bits_needed(max(arr) if arr else 0), 12)

        
        self.overflow = []
        for v in arr:
            if bits_needed(v) > self.k_small:
                self.overflow.append(v)
        self.m_overflow = len(self.overflow)
        m_bits = max(1, bits_needed(self.m_overflow - 1)) if self.m_overflow > 0 else 1
        self.data_bits = max(self.k_small, m_bits)
        self.k = 1 + self.data_bits  
        self.n = len(arr)

    def compress(self, arr: List[int]) -> None:
        self._prep_scheme(arr)
        self.words = []
        bitpos = 0
        ov_idx = 0
        
        for v in arr:
            if bits_needed(v) <= self.k_small:
                flag = 0
                payload = v  
            else:
                flag = 1
                payload = ov_idx
                ov_idx += 1
            unit = (flag & 1) | (payload << 1)
            self._write_bits(bitpos, self.k, unit)
            bitpos += self.k
        
        if self.m_overflow:
            
            self.words.append(0xFACEB00C)
            for v in self.overflow:
                self.words.append(v)

    def _read_unit(self, i: int) -> Tuple[int, int]:
        unit = self._read_bits(i * self.k, self.k)
        flag = unit & 1
        payload = unit >> 1
        return flag, payload

    def decompress(self, out_len: int) -> List[int]:
        res: List[int] = []
        
        cut = len(self.words)
        for j in range(len(self.words) - 1, -1, -1):
            if self.words[j] == 0xFACEB00C:
                cut = j
                break
        
        overflow_vals = self.words[cut + 1 :] if cut < len(self.words) else []
        for i in range(out_len):
            flag, payload = self._read_unit(i)
            if flag == 0:
                
                mask = (1 << self.k_small) - 1
                res.append(payload & mask)
            else:
                res.append(overflow_vals[payload])
        return res

    def get(self, i: int) -> int:
        
        cut = len(self.words)
        for j in range(len(self.words) - 1, -1, -1):
            if self.words[j] == 0xFACEB00C:
                cut = j
                break
        overflow_vals = self.words[cut + 1 :] if cut < len(self.words) else []
        flag, payload = self._read_unit(i)
        if flag == 0:
            return payload & ((1 << self.k_small) - 1)
        return overflow_vals[payload]
