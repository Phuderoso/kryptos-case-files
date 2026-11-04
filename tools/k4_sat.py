"""Cycle 11 (3): exact SAT (pysat/CaDiCaL, one-hot) satisfiability of structured cipher families under the 24 cribs,
with BOTH the plain alphabet PA and the cipher alphabet CA unknown (independent permutations).
Model: CApos(c_i) = PApos(p_i) + k_i (mod 26). Only letters touching the cribs get variables (any injective partial
map extends to a full permutation, so this is exact). Global shift symmetry broken by PApos(first crib letter)=0.
Families: F1 periodic key period P (Quagmire IV with unknown alphabets; includes Quag I/II/III & plain Vigenere as
special cases); F2 Gromark base b primer L (digits 0..b-1, k_j=k_{j-L}+k_{j-L+1} mod b); F3 progressive a+s*i;
F4 plaintext autokey lag L (key = PApos of plaintext L back; only crib->crib links constrain, primer free);
F5 ciphertext autokey lag L (key = CApos of ciphertext L back).
UNSAT = proof the family cannot produce the cribs. SAT = only 'not excluded'.  Run: python3 tools/k4_sat.py [control]"""
import sys, time, random, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
sys.path.insert(0, "tools")
from kryptos_text import K4
from k4_anneal import AZ, KN
N = 97; CR = sorted(KN.items())
class M:
    def __init__(s):
        s.pool = IDPool(); s.cl = []
    def onehot(s, name, dom):
        v = [s.pool.id((name, x)) for x in range(dom)]
        s.cl += CardEnc.equals(v, 1, vpool=s.pool, encoding=EncType.seqcounter).clauses; return v
    def amo(s, lits): s.cl += CardEnc.atmost(lits, 1, vpool=s.pool, encoding=EncType.seqcounter).clauses
def alphabets(m, CT):
    pl = sorted(set(p for _, p in CR)); cl = sorted(set(CT[i] for i, _ in CR))
    pa = {c: m.onehot(("pa", c), 26) for c in pl}; ca = {c: m.onehot(("ca", c), 26) for c in cl}
    for v in range(26):
        m.amo([pa[c][v] for c in pl]); m.amo([ca[c][v] for c in cl])
    m.cl.append([pa[pl[0]][0]])
    return pa, ca
def rel(m, ca_c, pa_p, kv, kdom):   # ca = pa + k mod 26 ; kv list of one-hot vars, value w -> shift w
    for u in range(26):
        for w in range(kdom):
            m.cl.append([-pa_p[u], -kv[w], ca_c[(u + w) % 26]])
def solve(m, tl=120):
    with Cadical153(bootstrap_with=m.cl) as s:
        t = time.time(); r = s.solve(); return ("SAT" if r else "UNSAT"), round(time.time() - t, 2)
def periodic(CT, P):
    m = M(); pa, ca = alphabets(m, CT); key = [m.onehot(("k", j), 26) for j in range(P)]
    for i, p in CR: rel(m, ca[CT[i]], pa[p], key[i % P], 26)
    return m
def gromark(CT, b, L):
    m = M(); pa, ca = alphabets(m, CT); k = [m.onehot(("g", j), b) for j in range(74)]
    for j in range(L, 74):
        for x in range(b):
            for y in range(b): m.cl.append([-k[j - L][x], -k[j - L + 1][y], k[j][(x + y) % b]])
    for i, p in CR: rel(m, ca[CT[i]], pa[p], k[i], b)
    return m
def progressive(CT):
    m = M(); pa, ca = alphabets(m, CT); a = m.onehot("a", 26); st = m.onehot("s", 26)
    for i, p in CR:
        kv = m.onehot(("pk", i), 26)
        for x in range(26):
            for y in range(26): m.cl.append([-a[x], -st[y], kv[(x + y * i) % 26]])
        rel(m, ca[CT[i]], pa[p], kv, 26)
    return m
def autokey(CT, L, kind):
    m = M(); pa, ca = alphabets(m, CT)
    for i, p in CR:
        j = i - L
        if kind == "pt" and j in KN: kv = pa[KN[j]]
        elif kind == "ct" and j >= 0:
            c = CT[j]; kv = ca[c] if c in ca else m.onehot(("cx", c), 26)
            if c not in ca:
                ca[c] = kv
        else: continue
        rel(m, ca[CT[i]], pa[p], kv, 26)
    # ensure added ct letters are injective too
    for v in range(26): m.amo([ca[c][v] for c in ca])
    return m
def plant(kind):
    rng = random.Random(11); PA = "".join(rng.sample(AZ, 26)); CA = "".join(rng.sample(AZ, 26))
    eng = ("WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKEX")
    pt = list(eng[:N])
    for i, ch in KN.items(): pt[i] = ch
    if kind == "periodic7": k = [[3, 14, 15, 9, 2, 6, 5][i % 7] for i in range(N)]
    elif kind == "gromark":
        k = [2, 7, 1, 8, 2]
        while len(k) < N: k.append((k[-5] + k[-4]) % 10)
    return "".join(CA[(PA.index(p) + k[i]) % 26] for i, p in enumerate(pt))
if __name__ == "__main__":
    ctl = len(sys.argv) > 1 and sys.argv[1] == "control"
    jobs = []
    if ctl:
        C1 = plant("periodic7"); C2 = plant("gromark")
        print("CONTROL A: planted Quagmire-IV, random PA/CA, period 7 -> expect P=7 SAT (and its multiples)")
        for P in range(1, 15): jobs.append((f"A periodic P={P}", periodic(C1, P)))
        print("CONTROL B: planted Gromark b10 primer 27182, random PA/CA -> expect b10L5 SAT")
        jobs += [("B gromark b10 L5", gromark(C2, 10, 5)), ("B gromark b10 L4", gromark(C2, 10, 4)), ("B gromark b5 L5", gromark(C2, 5, 5))]
    else:
        for P in range(1, 27): jobs.append((f"F1 periodic (Quag-IV, unknown PA+CA) P={P}", periodic(K4, P)))
        for b in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 26):
            for L in (2, 3, 4, 5, 6, 7):
                jobs.append((f"F2 Gromark base {b} primer {L}", gromark(K4, b, L)))
        jobs.append(("F3 progressive a+s*i", progressive(K4)))
        for L in range(1, 50): jobs.append((f"F4 PT-autokey lag {L}", autokey(K4, L, "pt")))
        for L in range(1, 50): jobs.append((f"F5 CT-autokey lag {L}", autokey(K4, L, "ct")))
    for name, m in jobs:
        r, dt = solve(m); print(f"{name}: {r} ({dt}s)", flush=True)
