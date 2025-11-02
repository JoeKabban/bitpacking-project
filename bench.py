import time, statistics as stats, random, math
from typing import Callable, List, Tuple
from bitpacking.factory import make_bitpacker

def timeit(fn: Callable[[], None], repeat=10) -> float:
    vals=[]
    for _ in range(repeat):
        t0=time.perf_counter(); fn(); vals.append(time.perf_counter()-t0)
    return stats.median(vals)

def main():
    random.seed(0)
    sizes=[1_000, 10_000, 100_000]
    maxv_list=[255, 4095, 1_000_000]
    modes=["overlap","no_overlap","overflow"]

    print("size,maxv,mode,k,words,t_compress_ms,t_get_ms,t_decompress_ms,orig_bits,comp_bits,ratio,break_even_bw_MBps")
    for n in sizes:
        for maxv in maxv_list:
            arr=[random.randint(0,maxv) for _ in range(n)]
            orig_bits=n*32
            for mode in modes:
                bp = make_bitpacker(mode)
                t_c = timeit(lambda: (bp.compress(arr)), repeat=5)*1000
                # measure get on 1000 random indices
                idx=[random.randint(0,n-1) for _ in range(min(1000,n))]
                t_g = timeit(lambda: [bp.get(i) for i in idx], repeat=5)*1000
                t_d = timeit(lambda: (bp.decompress(n)), repeat=3)*1000
                comp_bits = (len(bp.words)*32)
                ratio = orig_bits/comp_bits if comp_bits>0 else float('inf')

                
                denom = (t_c + t_d)/1000.0
                bw_star_bps = (orig_bits - comp_bits)/denom if denom>1e-9 and (orig_bits>comp_bits) else float('inf')
                bw_star_MBps = (bw_star_bps/8)/(1024*1024)

                print(f"{n},{maxv},{mode},{bp.k},{len(bp.words)},{t_c:.2f},{t_g:.2f},{t_d:.2f},{orig_bits},{comp_bits},{ratio:.3f},{bw_star_MBps:.2f}")

if __name__=="__main__":
    main()
