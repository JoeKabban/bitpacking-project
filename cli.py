import argparse, json, random
from bitpacking.factory import make_bitpacker

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True, choices=["overlap","no_overlap","overflow"])
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--maxv", type=int, default=4095)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    random.seed(args.seed)
    arr = [random.randint(0, args.maxv) for _ in range(args.n)]

    bp = make_bitpacker(args.mode)
    bp.compress(arr)
    rec = bp.decompress(args.n)

    ok = (arr == rec)
    print(json.dumps({
        "mode": args.mode,
        "n": args.n,
        "maxv": args.maxv,
        "equal": ok,
        "k": bp.k,
        "words": len(bp.words)
    }, indent=2))
    if not ok:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
