#!/usr/bin/env python3
"""QIII-R1 by SAT: unknown keyed alphabet A (same on both sides), Vigenere-type c = A[A^-1 p + s_k],
key index k = in-word position mod L (word restart). Beaufort/variant on an unknown alphabet reduce to the same
shape up to reflection for Vigenere-type; here we test the Vigenere form (Quagmire III) and the Beaufort form."""
import sys, json, time, random
sys.path.insert(0, '.')
from wr203 import *
from pysat.solvers import Glucose4
from pysat.card import CardEnc

def classes(start, crib, bnds, o, L):
    out = []
    for j, p in enumerate(crib):
        prev = [b for b in bnds if b <= j]
        out.append(((j - prev[-1]) if prev else (o + j)) % L)
    return out

def build_base():
    # x[l][a] var: letter l at alphabet position a
    X = lambda l, a: 1 + l * 26 + a
    cl = []; top = 26 * 26
    for l in range(26):
        e = CardEnc.equals([X(l, a) for a in range(26)], 1, top_id=top); top = max(top, e.nv); cl += e.clauses
    for a in range(26):
        e = CardEnc.equals([X(l, a) for l in range(26)], 1, top_id=top); top = max(top, e.nv); cl += e.clauses
    cl.append([X(0, 0)])  # fix rotation: wlog A... no: fix letter of first crib? rotation freedom: put 'A' at 0
    return X, cl, top

def sat_case(ct, pairs, mode):
    """pairs: list of (cipher letter, plain letter, class). Return True if some alphabet + shifts fit."""
    X, cl, top = build_base()
    ncls = max(k for _, _, k in pairs) + 1
    Y = lambda k, s: top + 1 + k * 26 + s
    top2 = top + ncls * 26
    cl = list(cl)
    used = sorted(set(k for _, _, k in pairs))
    for k in used:
        e = CardEnc.equals([Y(k, s) for s in range(26)], 1, top_id=top2); top2 = max(top2, e.nv); cl += e.clauses
    for c, p, k in pairs:
        ci, pi = AZ.index(c), AZ.index(p)
        for s in range(26):
            for a in range(26):
                b = (a + s) % 26 if mode == "vig" else (s - a) % 26
                cl.append([-X(pi, a), -Y(k, s), X(ci, b)])
    with Glucose4(bootstrap_with=cl) as g:
        return g.solve()

def scan(ct, Ls, mode, stop_first=False, segE=SEG_E, segB=SEG_B):
    found = {}
    for L in Ls:
        if stop_first and any(found.values()): break
        found[L] = None
        for sE, bE in segE.items():
            for sB, bB in segB.items():
                for o1 in range(L):
                    for o2 in range(L):
                        k1 = classes(CRIBS[0][0], CRIBS[0][1], bE, o1, L)
                        k2 = classes(CRIBS[1][0], CRIBS[1][1], bB, o2, L)
                        pairs = [(ct[CRIBS[0][0] + j], CRIBS[0][1][j], k1[j]) for j in range(13)] + \
                                [(ct[CRIBS[1][0] + j], CRIBS[1][1][j], k2[j]) for j in range(11)]
                        if sat_case(ct, pairs, mode):
                            found[L] = (sE, sB, o1, o2); break
                    if found[L]: break
                if found[L]: break
            if found[L]: break
    return found

if __name__ == "__main__":
    t0 = time.time()
    res = {}
    # control C3: random alphabet, R1, key "ABSCISSA" shifts, invented example text
    rng = random.Random(2031)
    A = list(AZ); rng.shuffle(A); A = "".join(A)
    W = ["DOOR", "OPENED", "AND", "WE", "WALKED", "EAST", "NORTHEAST", "UNDER", "THE", "DUST", "WE", "SAW", "A", "GREAT",
         "RUSTED", "BERLIN", "CLOCK", "STILL", "TICKING", "INSIDE", "THE", "VAULT"]
    key = [3, 17, 5, 11, 0, 9, 22, 14]
    c = ""
    for w in W:
        for j, p in enumerate(w): c += A[(A.index(p) + key[j % 8]) % 26]
    c = c[:97]
    k1 = classes(21, "EASTNORTHEAST", [4], 0, 8); k2 = classes(63, "BERLINCLOCK", [6], 0, 8)
    pairs = [(c[21 + j], "EASTNORTHEAST"[j], k1[j]) for j in range(13)] + [(c[63 + j], "BERLINCLOCK"[j], k2[j]) for j in range(11)]
    res['C3_true_config_SAT'] = sat_case(c, pairs, "vig")
    print("C3", res['C3_true_config_SAT'], time.time() - t0, flush=True)
    Ls = range(1, 14)
    for mode in ("vig", "beau"):
        f = scan(K4, Ls, mode)
        res[f'K4_{mode}'] = {L: v for L, v in f.items()}
        print(mode, f, time.time() - t0, flush=True)
    # nulls: shuffled K4, first SAT L
    rng = random.Random(203203)
    nul = []
    for i in range(int(sys.argv[1]) if len(sys.argv) > 1 else 40):
        l = list(K4); rng.shuffle(l); sh = "".join(l)
        f = scan(sh, Ls, "vig", stop_first=True)
        nul.append(min([L for L, v in f.items() if v] or [99]))
        if time.time() - t0 > 330: break
    res['null_vig_minL_SAT'] = nul
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open('results203_sat.json', 'w'), indent=1, default=str)
    print(res)
