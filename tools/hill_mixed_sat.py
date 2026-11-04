"""Cycle 29: Hill 2x2 with an ARBITRARY letter numbering (sigma: A-Z -> Z26 bijection),
directly on the carved K4. Exact SAT (CaDiCaL via python-sat) over sigma and the
decryption matrix M:  sigma(p_pair) = M * sigma(c_pair) mod 26, for every block pair
lying fully inside the cribs. Enumerates all solutions projected on (M, sigma of the
crib letters) up to a cap. Unit scaling sigma -> u*sigma gives 12 copies of each.
usage: python3 hill_mixed_sat.py <ciphertext_file|K4> [cap]"""
import sys, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from kryptos_text import K4
CRIBS = {21: "EASTNORTHEAST", 63: "BERLINCLOCK"}
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def crib_map():
    d = {}
    for s, w in CRIBS.items():
        for i, ch in enumerate(w): d[s + i] = ch
    return d

def solve(ct, offset, cap):
    pt = crib_map()
    pairs = [(i, i + 1) for i in range(offset, len(ct) - 1, 2) if i in pt and i + 1 in pt]
    top = [0]
    def nv():
        top[0] += 1; return top[0]
    s = {L: [nv() for _ in range(26)] for L in A}
    m = [[nv() for _ in range(26)] for _ in range(4)]
    cl = []
    def exactly_one(lits):
        cl.extend(CardEnc.equals(lits=lits, bound=1, top_id=top[0], encoding=EncType.pairwise).clauses)
    for L in A: exactly_one(s[L])
    for v in range(26): exactly_one([s[L][v] for L in A])
    for k in range(4): exactly_one(m[k])
    prod = {}
    def product(k, L):
        if (k, L) in prod: return prod[(k, L)]
        t = [nv() for _ in range(26)]; exactly_one(t)
        for a in range(26):
            for x in range(26):
                cl.append([-m[k][a], -s[L][x], t[(a * x) % 26]])
        prod[(k, L)] = t; return t
    def eq_sum(t1, t2, P):
        for i in range(26):
            for j in range(26):
                cl.append([-t1[i], -t2[j], s[P][(i + j) % 26]])
    for (i, j) in pairs:
        c1, c2, p1, p2 = ct[i], ct[j], pt[i], pt[j]
        eq_sum(product(0, c1), product(1, c2), p1)
        eq_sum(product(2, c1), product(3, c2), p2)
    # M invertible mod 26: det must be a unit. det = m0*m3 - m1*m2; forbid non-units by
    # direct enumeration of the 26^4 cells would be big; instead check after the fact.
    involved = sorted(set(ct[i] for p in pairs for i in p) | set(pt[i] for p in pairs for i in p))
    proj = [v for k in range(4) for v in m[k]] + [v for L in involved for v in s[L]]
    sols = []
    with Cadical153(bootstrap_with=cl) as S:
        while len(sols) < cap and S.solve():
            mod = set(l for l in S.get_model() if l > 0)
            M = [next(a for a in range(26) if m[k][a] in mod) for k in range(4)]
            sig = {L: next(v for v in range(26) if s[L][v] in mod) for L in A}
            sols.append((M, {L: sig[L] for L in involved}, sig))
            S.add_clause([-x for x in proj if x in mod])
    return pairs, involved, sols

def unit(d): return d % 2 == 1 and d % 13 != 0

if __name__ == "__main__":
    src = sys.argv[1]; cap = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    ct = K4 if src == "K4" else open(src).read().strip()
    for off in (0, 1):
        t = time.time()
        pairs, inv, sols = solve(ct, off, cap)
        good = [x for x in sols if unit((x[0][0] * x[0][3] - x[0][1] * x[0][2]) % 26)]
        print(f"{src} offset={off} pairs={len(pairs)} involved_letters={len(inv)} "
              f"solutions={len(sols)}{'+' if len(sols)>=cap else ''} invertibleM={len(good)} "
              f"classes(/12)={len(good)/12:.1f} time={time.time()-t:.1f}s", flush=True)
        for M, part, full in good[:3]:
            print("   M=", M, "sigma(part)=", "".join(f"{L}{part[L]} " for L in inv))
