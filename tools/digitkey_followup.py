"""Cycle 11 follow-up: for every digit-window hit (width<=10) test whether the 24 recovered digits can come from a
lagged-Fibonacci (Gromark-style) generator k_n = k_{n-L} + k_{n-L+1} mod b, L=1..8, b=width..10, any offset t,
checked inside the two consecutive crib blocks (pos 21-33 and 63-73). Also reports chance expectation per width.
Usage: python3 tools/digitkey_followup.py <digitwin output>"""
import sys
names = open("data/alpha.txt").read().split("\n")
lines = open(sys.argv[1]).read().splitlines()
pairs = int([l for l in lines if l.startswith("PAIRS")][0].split()[1])
print("pairs per mode", pairs)
for w in range(8, 11):
    p = 26 * ((w / 26) ** 24 - ((w - 1) / 26) ** 24)
    print(f"width {w}: expected by chance per mode {pairs * p:.2f}")
for l in lines:
    if l.startswith("HIST"): print(l)
fib = []
for l in lines:
    if not l.startswith("HIT"): continue
    _, a, b, mode, w, s, d = l.split(); w = int(w[2:]); d = [int(x) for x in d[2:]]
    for base in range(w, 11):
        for t in range(0, base - w + 1):
            k = [(x + t) % base for x in d]
            for L in range(1, 9):
                ok = all(all(blk[n] == (blk[n - L] + blk[n - L + 1]) % base for n in range(L, len(blk)))
                         for blk in (k[:13], k[13:]))
                if ok: fib.append((names[int(a)], names[int(b)], mode, base, t, L))
print("hits", sum(l.startswith("HIT") for l in lines), "| lagged-Fibonacci-consistent:", len(fib))
for f in fib: print("  FIB", f)
