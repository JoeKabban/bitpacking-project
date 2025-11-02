# Bit Packing Project (Software Engineering 2025)

**Author:** Joe Kabban

---

## 1) Objective
The goal of this project was to design and evaluate different bit-packing methods to compress arrays of non-negative integers efficiently while maintaining **direct random access** to each element.  
The main motivation is to reduce the amount of data that needs to be stored or transmitted, especially when dealing with large datasets or limited bandwidth, without losing the ability to quickly read individual elements.

This project was implemented in **Python**, without using Jupyter notebooks, as required by the course.

---

## 2) Methodology
To evaluate and compare the performance of the algorithms, several aspects were measured and analyzed.

- **Bit width (k):**  
  For each dataset, the number of bits required to represent the largest value is computed as `k = max(bit_length(x))`. This determines how tightly the data can be packed.

- **Compression and decompression:**  
  Each array is converted into 32-bit words according to the chosen mode. The same function is then used to decompress the data back into integers. Both operations were timed precisely using high-resolution timers.

- **Direct access:**  
  The function `get(i)` reconstructs the *i*-th value directly from the packed words, without decompressing the entire array. This feature was verified for correctness and speed.

- **Timing protocol:**  
  Each operation (compression, decompression, access) was repeated multiple times, and the median runtime was recorded to reduce variability. The following metrics were measured:
  - `t_compress_ms` — compression time in milliseconds  
  - `t_decompress_ms` — decompression time in milliseconds  
  - `t_get_ms` — average time to access one element  
  - `orig_bits = 32 * n` and `comp_bits = 32 * (#words)`  
  - `ratio = orig_bits / comp_bits` (compression ratio)

- **Break-even bandwidth:**  
  The value `break_even_bw_MBps` estimates the minimum bandwidth at which compression remains beneficial. If the network speed is lower than this value, compression helps save total time.

---

## 3) Implemented Methods
Three different strategies were implemented to explore various trade-offs between compression ratio and speed.

### **Overlap Bit Packing**
Each value uses exactly `k` bits and may **span across 32-bit boundaries**.  
This approach achieves the best compression ratio because every bit is used efficiently.  
However, the logic is slightly more complex since values may overlap between consecutive words.

### **No Overlap Bit Packing**
Each value fits entirely inside one 32-bit word.  
This makes compression and decompression simpler and faster, but the unused bits inside words lead to a larger overall size.  
This mode is useful when speed is more important than compactness.

### **Overflow Bit Packing**
A hybrid approach where values smaller than a chosen width `k_small` are stored normally, while larger values are placed in a separate overflow array.  
The packed data stores a flag indicating whether a value is normal or overflowed.  
This can save space when only a few elements are very large, but when many values are large, the overflow structure can actually make the result bigger.

---

## 4) Tests
All automated tests passed successfully.

Testing focused on verifying the **correctness**, **stability**, and **consistency** of the three bit-packing modes (`overlap`, `no_overlap`, `overflow`).  
Each test checks three essential properties:

1. **Round-trip integrity:**  
   After compressing and decompressing an array, the result must be identical to the original (`equal = true`).  
   This ensures that no bits are lost or misaligned during packing or unpacking.

2. **Random access verification:**  
   The function `get(i)` was tested to guarantee that individual elements can be retrieved directly from the compressed data without decompressing the entire array.  
   This validates one of the key objectives of the project: efficient direct access.

3. **Consistency across modes:**  
   The same input dataset was used for all three methods to confirm that differences in size and timing come from the packing strategies themselves, not from random variations in data.

The testing framework used was **pytest**, which automatically ran all the test cases defined in `tests/test_bitpacking.py`.  

The results were:
pytest → 3 passed

Additionally, the CLI tool (`cli.py`) was executed manually with different parameters to ensure real-world usage worked correctly:

python cli.py --mode overlap --n 1000 --maxv 4095
python cli.py --mode no_overlap --n 1000 --maxv 4095
python cli.py --mode overflow --n 1000 --maxv 100000

Each execution returned `"equal": true`, confirming that compression and decompression work properly across all configurations.

Overall, the tests demonstrate that the implementation is reliable, precise, and behaves correctly under all tested conditions.

---

## 5) Benchmark Results
The program includes a benchmarking script (`bench.py`) that measures time and space performance for different input sizes and maximum values.  
A sample of the results from `results.csv` is shown below:

| size | maxv | mode        | ratio | t_compress_ms | t_decompress_ms |
|------|------|--------------|--------|----------------|-----------------|
| 1000 | 4095 | overlap      | 2.67   | 0.82           | 0.47            |
| 1000 | 4095 | no_overlap   | 2.00   | 0.49           | 0.28            |
| 1000 | 4095 | overflow     | 2.46   | 1.09           | 0.79            |

**Interpretation:**
- For **small integers (maxv = 255)**, both `overlap` and `no_overlap` achieve the same ratio (4.0).  
  The `no_overlap` version is slightly faster.
- For **medium ranges (maxv = 4095)**, `overlap` compresses better (2.67× vs 2.0×) with a minor cost in speed.
- For **large ranges (maxv = 1,000,000)**, `overlap` still offers compression (~1.6×), while `no_overlap` provides none (1.0×).  
- The `overflow` approach is only beneficial when few values are large. If many are large, it adds overhead and performs worse.

---

## 6) Findings and Discussion
- **Best compression ratio:** Achieved by the **overlap** mode, since it uses every bit efficiently.
- **Fastest execution:** The **no_overlap** mode, because it avoids cross-word bit shifts.
- **Overflow mode performance:**  
  Effective only when the data distribution has rare high values. When most values are large, the overflow area becomes counterproductive.
- **Random access:** All three modes provide constant-time access to any element, confirming that direct reading is possible without full decompression.
- **Trade-off:**  
  There is a clear balance between compression efficiency and execution time — the more compact the representation, the higher the bit manipulation cost.

---

## 7) Conclusion
The three methods were implemented, tested, and benchmarked successfully.  
Each approach serves a different purpose:
- **No Overlap** — best choice for small data ranges and simple implementation.  
- **Overlap** — best overall compression ratio and suitable for general use.  
- **Overflow** — suitable for datasets with occasional large outliers.

All tests passed and the benchmark data confirmed that the compression behaves as expected across various input sizes and value ranges.

This project demonstrates how bit-level data representation can significantly reduce memory usage while preserving random access — a fundamental technique for optimizing storage and transmission efficiency.

---

**Author:** Joe Kabban  
Université Côte d’Azur — L3 Artificial Intelligence
