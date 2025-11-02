from .overlap import BitPackingOverlap
from .no_overlap import BitPackingNoOverlap
from .overflow import BitPackingOverflow

def make_bitpacker(mode: str):
    m = mode.lower()
    if m in ("overlap", "o"):
        return BitPackingOverlap()
    if m in ("no_overlap", "no", "n"):
        return BitPackingNoOverlap()
    if m in ("overflow", "of"):
        return BitPackingOverflow()
    raise ValueError(f"Unknown mode: {mode}")
