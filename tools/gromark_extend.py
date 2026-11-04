"""Cycle 10 (B3): general Gromark feasibility (any plain+cipher alphabets; and plain=A-Z) beyond Bean's base10/len5."""
import sys; sys.path.insert(0, "tools")
import gromark_alphabet as g
from k4_anneal import AZ
from kryptos_text import K4
CI = [i for i, _ in g.CR]
for b in range(5, 11):
    for L in (4, 5, 6):
        if b ** L > 1_000_000: continue
        prim, K = g.keys(b, L); gen = az = 0; ex = []
        for r in range(len(prim)):
            k = K[r, CI]
            if g.feasible(K4, k)[0]:
                gen += 1; ex.append("".join(map(str, prim[r])))
                if g.feasible(K4, k, AZ)[0]: az += 1
        print(f"base {b:2d} primer {L}: {b**L:>8,} primers; feasible any-alphabets {gen}; with plain A-Z {az}; e.g. {ex[:3]}", flush=True)
