"""Cycle 164 independent recount: brute-force Python check of q4ak's consistency counts (no 26x26 tables,
no chain sorting, string alphabets).  Per configuration it walks every residue class from the first crib
forward through the carved letters and checks every later crib (PT feed), or checks every crib at q >= L
against the ciphertext letter L places earlier (CT feed).  Prints H lines in q4ak's format.
usage: recount164.py CT plain.txt cipher.txt label plo phi LMAX"""
import sys
import numpy as np
from plant164 import keyed
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
ct, f1, f2, lab, plo, phi, LMAX = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
def lst(fn):
    out = []
    for w in open(fn).read().split():
        a = keyed(w)
        if a not in [x[1] for x in out]: out.append((w, a))
    return out
L1, L2 = lst(f1), lst(f2)
B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
def dec(X, Y, Z, f, c, k):
    y, z = Y.index(c), Z.index(k)
    return X[(y - z if f == 0 else z - y if f == 1 else y + z) % 26]
H = {}
for q in range(plo, phi):
    for d in (0, 1):
        S = list(B[q]) if d == 0 else list(np.argsort(B[q]))
        for ix in (0, 1):
            if ix == 0: kp = CI; lay = [ct[S[i]] for i in range(97)]
            else: kp = [S[i] for i in CI]; lay = list(ct)
            known = {kp[t]: PT[t] for t in range(24)}
            for _, X in L1:
                for _, Y in L2:
                    if X == Y: continue
                    for zY in (0, 1):
                        Z = Y if zY else X
                        for f in range(3):
                            for L in range(1, LMAX + 1):
                                # CT feed
                                ok = all(dec(X, Y, Z, f, lay[j], lay[j - L]) == p for j, p in known.items() if j >= L)
                                if ok: H[("CT", zY, f, ix, L)] = H.get(("CT", zY, f, ix, L), 0) + 1
                                # PT feed
                                ok = True
                                for r in range(L):
                                    v = None
                                    for j in range(r, 97, L):
                                        if v is not None: v = dec(X, Y, Z, f, lay[j], v)
                                        if j in known:
                                            if v is not None and v != known[j]: ok = False; break
                                            v = known[j]
                                    if not ok: break
                                if ok: H[("PT", zY, f, ix, L)] = H.get(("PT", zY, f, ix, L), 0) + 1
for fe in ("PT", "CT"):
    for zY in (0, 1):
        for f in range(3):
            for ix in (0, 1):
                print(f"H {lab} feed={fe} {['zX','zY'][zY]} {['vig','beau','var'][f]} ix={['pt','carved'][ix]} " + " ".join(str(H.get((fe, zY, f, ix, L), 0)) for L in range(1, LMAX + 1)))
