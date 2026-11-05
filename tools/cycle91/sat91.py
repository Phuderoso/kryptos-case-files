"""Cycle 91 (adapted from cycle 83): W-FREE 92-letter text, W as null, all layers on a 25-letter W-less alphabet:
Playfair square omits W; outer periodic key on a W-less KA or A-Z tableau (mod 25). Cribs at 20-32 and 60-70.
Original cycle 83 notes follow.
Cycle 83: Playfair with an ARBITRARY 5x5 square (any 25 of the 26 letters, any placement) as the inner layer,
periodic Vigenere/Beaufort/variant on a KA or A-Z tableau as the outer layer, p 1-8.  Exact SAT (CaDiCaL 1.5.3 via
PySAT): square, omitted letter and outer key are all free variables.  Constraints:
  * all 13 Playfair pairs touching a crib (11 full + 2 half pairs, the unknown partner a free letter) must Playfair-encrypt to the inner letters (row / column / rectangle rule);
  * every inner letter (all 97 positions; the key is fixed everywhere because p <= 13) must be in the square;
  * every inner pair (Playfair output) has two different letters.
Symmetry break: Playfair is invariant under cyclic row and column shifts, so E sits at cell (0,0).
usage: sat83.py CT p tab(KA|AZ) mode(0 vig,1 beau,2 var) align(0|1)  -> prints SAT/UNSAT (+ a witness)"""
import sys, itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from kryptos_text import KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import os
CARD = os.environ.get('CARD', '1') == '1'
SOLVER = os.environ.get('SOLVER', 'cadical153')
CRIB = {**{20 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{60 + i: c for i, c in enumerate("BERLINCLOCK")}}

def build(ct, p, tab, mode, a, extra=None):
    T = (KA if tab == "KA" else AZ).replace("W", ""); M = len(T)
    n = [0]
    def nv():
        n[0] += 1; return n[0]
    cl = []
    X = [[nv() for _ in range(25)] for _ in range(26)]       # letter L in cell
    IN = [nv() for _ in range(26)]
    R = [[nv() for _ in range(5)] for _ in range(26)]
    C = [[nv() for _ in range(5)] for _ in range(26)]
    K = [[nv() for _ in range(M)] for _ in range(p)]
    I = [[nv() for _ in range(26)] for _ in range(len(ct))]
    def exactly1(lits):
        enc = CardEnc.equals(lits=lits, bound=1, top_id=n[0], encoding=EncType.seqcounter)
        n[0] = max(n[0], enc.nv); cl.extend(enc.clauses)
    def atmost1(lits):
        enc = CardEnc.atmost(lits=lits, bound=1, top_id=n[0], encoding=EncType.seqcounter)
        n[0] = max(n[0], enc.nv); cl.extend(enc.clauses)
    for L in range(26):
        atmost1(X[L])
        cl.append([-IN[L]] + X[L]); [cl.append([-x, IN[L]]) for x in X[L]]
        for r in range(5):
            cells = [X[L][r * 5 + c] for c in range(5)]
            cl.append([-R[L][r]] + cells); [cl.append([-x, R[L][r]]) for x in cells]
            cells = [X[L][c * 5 + r] for c in range(5)]
            cl.append([-C[L][r]] + cells); [cl.append([-x, C[L][r]]) for x in cells]
    for cell in range(25): exactly1([X[L][cell] for L in range(26)])
    if CARD:  # redundant: each row / column holds exactly 5 letters, each placed letter one row and one column
        for r in range(5):
            for VV in (R, C):
                enc = CardEnc.equals(lits=[VV[L][r] for L in range(26)], bound=5, top_id=n[0], encoding=EncType.seqcounter)
                n[0] = max(n[0], enc.nv); cl.extend(enc.clauses)
        for L in range(26):
            for VV in (R, C):
                enc = CardEnc.atmost(lits=VV[L], bound=1, top_id=n[0], encoding=EncType.pairwise); cl.extend(enc.clauses)
                cl.append([-IN[L]] + VV[L])
    cl.append([-IN[22]])  # W omitted (W-null model)
    cl.append([X[4][0]])                    # E at (0,0)
    for L in set(CRIB.values()): cl.append([IN[ord(L) - 65]])
    for r in range(p): exactly1(K[r])
    # inner letter from ciphertext and key: vig c=q+k, beau c=k-q, var c=q-k (indices in T)
    for i, ch in enumerate(ct):
        c = T.index(ch)
        for k in range(M):
            q = (c - k) % M if mode == 0 else (k - c) % M if mode == 1 else (c + k) % M
            cl.append([-K[i % p][k], I[i][ord(T[q]) - 65]])
        exactly1(I[i])
        for L in range(26): cl.append([-I[i][L], IN[L]])
    for i in range(a, len(ct) - 1, 2):
        for L in range(26): cl.append([-I[i][L], -I[i + 1][L]])
    # crib pairs: every Playfair pair holding at least one crib letter; an unknown plaintext partner is a free letter
    npairs = 0
    def vec(LET):
        RR = [nv() for _ in range(5)]; CC = [nv() for _ in range(5)]
        for L in range(26):
            for r in range(5):
                cl.append([-LET[L], -R[L][r], RR[r]]); cl.append([-LET[L], R[L][r], -RR[r]])
                cl.append([-LET[L], -C[L][r], CC[r]]); cl.append([-LET[L], C[L][r], -CC[r]])
        return RR, CC
    for i in range(a, len(ct) - 1, 2):
        if not (i in CRIB or i + 1 in CRIB): continue
        npairs += 1
        PV = []
        for j in (i, i + 1):
            if j in CRIB:
                L0 = ord(CRIB[j]) - 65; PV.append((R[L0], C[L0], [L0]))
            else:
                PL = [nv() for _ in range(26)]; exactly1(PL)
                for L in range(26): cl.append([-PL[L], IN[L]])
                RR, CC = vec(PL); PV.append((RR, CC, PL))
        # plaintext pair letters differ (doubled letters are split before Playfair)
        (RA, CA, la), (RB, CB, lb) = PV
        if len(la) == 1 and len(lb) > 1: cl.append([-lb[la[0]]])
        if len(lb) == 1 and len(la) > 1: cl.append([-la[lb[0]]])
        RU, CU = vec(I[i]); RV, CV = vec(I[i + 1])
        for r1 in range(5):
            for r2 in range(5):
                for c1 in range(5):
                    for c2 in range(5):
                        pre = [-RA[r1], -RB[r2], -CA[c1], -CB[c2]]
                        if r1 == r2 and c1 == c2: cl.append(pre); continue
                        if r1 == r2:
                            cons = [RU[r1], RV[r1], CU[(c1 + 1) % 5], CV[(c2 + 1) % 5]]
                        elif c1 == c2:
                            cons = [CU[c1], CV[c1], RU[(r1 + 1) % 5], RV[(r2 + 1) % 5]]
                        else:
                            cons = [RU[r1], CU[c2], RV[r2], CV[c1]]
                        for x in cons: cl.append(pre + [x])
    return cl, X, IN, K, I, npairs

def solve(ct, p, tab, mode, a):
    cl, X, IN, K, I, npairs = build(ct, p, tab, mode, a)
    with Solver(name=SOLVER, bootstrap_with=cl) as s:
        if not s.solve(): return False, None, npairs
        m = set(x for x in s.get_model() if x > 0)
        sq = "".join(chr(65 + L) for cell in range(25) for L in range(26) if X[L][cell] in m)
        T = (KA if tab == "KA" else AZ).replace("W", "")
        key = "".join(T[k] for r in range(p) for k in range(len(T)) if K[r][k] in m)
        return True, (sq, key), npairs

if __name__ == "__main__":
    ct, p, tab, mode, a = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    ok, w, npairs = solve(ct, p, tab, mode, a)
    print("SAT" if ok else "UNSAT", npairs, w or "")
