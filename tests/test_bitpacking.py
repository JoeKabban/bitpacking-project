from bitpacking.factory import make_bitpacker

def roundtrip(mode, arr):
    bp = make_bitpacker(mode)
    bp.compress(arr)
    rec = bp.decompress(len(arr))
    assert arr == rec, f"{mode} failed"

def test_small():
    data = [0,1,2,3,4,5,6,7,8,9]
    for m in ["overlap","no_overlap","overflow"]:
        roundtrip(m,data)

def test_varied_ranges():
    arrays = [
        [0,15,3,7,8,255,16,1,0],
        [1,2,3,1024,4,5,2048],
        [0]*100 + [123456] + [7]*50
    ]
    for m in ["overlap","no_overlap","overflow"]:
        for a in arrays:
            roundtrip(m,a)

def test_get():
    arr = list(range(1000))
    for m in ["overlap","no_overlap","overflow"]:
        bp = make_bitpacker(m); bp.compress(arr)
        for i,v in enumerate(arr):
            assert bp.get(i)==v
