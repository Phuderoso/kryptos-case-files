"""Cycle 13: strip (row) transpositions, hypothesis S6 of case file 10.
A secondary source (cipher.ink, Oct 2026) says the 1990 Smithsonian K4 pages were text 'cut into strips and taped
together out of order'. Model: text written in rows (strips) of width w (last strip short), strips reordered.
Only the 24 crib positions matter for every test we run, so each transposition is stored only at the crib
positions (perm[j] = carved index paired with PT position j; -1 elsewhere). Two directions:
  S/enc : carved = PT strips in a new order      (PT row r sits at carved slot sigma(r))
  S/dec : PT     = carved strips in a new order  (carved strip c sits at PT slot sigma(c))
Every assignment of distinct strips to the crib-bearing rows is enumerated, for every slot of the short strip.
Widths 9..48 (w <= 8 gives >= 13 strips and too many crib rows to enumerate; noted as a gap).
Usage: python3 tools/strip_gen.py [control]  -> data/st_perm.bin, data/st_perm.txt"""
import sys, itertools, struct
sys.path.insert(0, "tools")
from kryptos_text import K4
N = 97
CI = list(range(21, 34)) + list(range(63, 74))
def slot_starts(R, w, L, k):          # start of slot s when the short strip (len L) sits at slot k
    st = []; pos = 0
    for s in range(R): st.append(pos); pos += (L if s == k else w)
    return st
T = {}
for w in range(9, 49):
    R = -(-N // w); L = N - (R - 1) * w
    # ---- direction enc: PT rows r (row R-1 short) placed at carved slots; short placed at slot k ----
    rows = sorted({j // w for j in CI})
    for k in range(R):
        st = slot_starts(R, w, L, k)
        free = [s for s in range(R) if s != k]
        fixed = [r for r in rows if r == R - 1]; var = [r for r in rows if r != R - 1]
        for choice in itertools.permutations(free, len(var)):
            sig = dict(zip(var, choice))
            for r in fixed: sig[r] = k
            p = [-1] * N
            for j in CI: p[j] = st[sig[j // w]] + j % w
            T[f"strip{w}enc:k{k}:" + ",".join(f"{r}>{sig[r]}" for r in rows)] = p
    # ---- direction dec: carved strips c (strip R-1 short) placed at PT slots; short at PT slot k ----
    for k in range(R):
        st = slot_starts(R, w, L, k)
        def slot_of(j):
            for s in range(R - 1, -1, -1):
                if j >= st[s]: return s
        slots = sorted({slot_of(j) for j in CI})
        var = [s for s in slots if s != k]
        free = list(range(R - 1))     # full-length carved strips
        for choice in itertools.permutations(free, len(var)):
            sig = dict(zip(var, choice)); sig[k] = R - 1
            p = [-1] * N
            for j in CI:
                s = slot_of(j); p[j] = sig[s] * w + (j - st[s])
            T[f"strip{w}dec:k{k}:" + ",".join(f"{s}<{sig[s]}" for s in slots)] = p
uniq = {}
for n, p in T.items(): uniq.setdefault(tuple(p[j] for j in CI), (n, p))
with open("data/st_perm.bin", "wb") as f:
    for n, p in uniq.values(): f.write(struct.pack("<97h", *p))
open("data/st_perm.txt", "w").write("\n".join(n for n, _ in uniq.values()) + "\n")
print("strip transpositions", len(T), "distinct on the cribs", len(uniq))
