"""Positive controls: plant a synthetic K4 built with a KNOWN Hill key / known transposition+Vigenere and the real cribs,
then confirm the cycle-2 tests DETECT it. Guards against false negatives from bugs. Run: python3 tools/validate_cycle2.py"""
import random, kryptos_text, importlib, io, contextlib
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
random.seed(7)
pt = [random.choice(AZ) for _ in range(97)]
for p, w in {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}.items():
    for i, ch in enumerate(w): pt[p - 1 + i] = ch
def run(fake):
    kryptos_text.K4 = fake
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import k4_cycle2
        importlib.reload(k4_cycle2)
    return buf.getvalue()
# Control 1: Hill 2x2, key [[3,3],[2,5]] (det 9, invertible mod 26), AZ, offset 0 (last letter left as is)
K = [[3, 3], [2, 5]]; ct = pt[:]
for s in range(0, 96, 2):
    a, b = AZ.index(pt[s]), AZ.index(pt[s+1])
    ct[s] = AZ[(K[0][0]*a + K[0][1]*b) % 26]; ct[s+1] = AZ[(K[1][0]*a + K[1][1]*b) % 26]
r = run("".join(ct)); print("Hill control:", [l for l in r.splitlines() if l.startswith("n=2 alpha=AZ offset=0")])
# Control 2: B2 model: CT = Vig_KA(T(PT)), T = columns w=7 down, key 'BERLIN' (P=6)
with contextlib.redirect_stdout(io.StringIO()):
    from k4_cycle2 import columnar, KA
perm = columnar(7); tp = [pt[s] for s in perm]; key = "BERLIN"
ct = [KA[(KA.index(c) + KA.index(key[k % 6])) % 26] for k, c in enumerate(tp)]
r = run("".join(ct)); print("Transposition control:", [l for l in r.splitlines() if "cols w=7 down:" in l and "B2" in l][:3])
