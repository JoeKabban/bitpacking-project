# Bit Packing Project (Software Engineering 2025)

**Author:** Joe Kabban

---

## 1) Objective
Design and evaluate bit-packing methods to compress arrays of non-negative integers while preserving **direct random access** to any element (via `get(i)`). The aim is to reduce transmitted size and keep operations fast.

---

## 2) Methodology (what I measured and how)
- **Bit width (k):** For each dataset, `k = max(bit_length(x))` over the input array.
- **Direct access:** `get(i)` reconstructs the i-th value from packed words without full decompression.
- **Timing protocol:** Used high-resolution timers and took the **median** of several runs to reduce noise. Reported:
  - `t_compress_ms`, `t_decompress_ms`, `t_get_ms`
  - `orig_bits = 32 * n`, `comp_bits = 32 * (#words)`, and `ratio = orig_bits / comp_bits`
- **Break-even bandwidth:** Reported as `break_even_bw_MBps`. Compression helps if the actual link speed is **below** this value (i.e., savings in bits outweigh compress/decompress overhead).

---

## 3) Implemented Methods
- **Overlap Bit Packing**  
  Values use exactly `k` bits and may **span across 32-bit words**. Best compression ratio, slightly higher bit-twiddling cost.

- **No Overlap Bit Packing**  
  Values **never cross 32-bit boundaries**; each is placed in a fixed slot within a word. Simpler and often faster, but can waste padding bits → larger output.

- **Overflow Bit Packing**  
  Choose a small width `k_small` and store values that don’t fit into an **overflow area**; in-band entries carry a flag + payload (either value or overflow index). Good only when **few** values are large outliers.

---

## 4) Tests
All automated tests passed:
- `compress()` + `decompress()` round-trip equals original
- `get(i)` returns the correct element without full decompression

