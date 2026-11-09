"""Cycle 174 independent recount (pure Python / numpy brute force, no code shared with the C tools).
Hill: every row vector (676 for n 2 linear, 17,576 for n 2 affine / n 3 linear) tried against the crib equations; a config is
consistent if each row has a solution; invertible if some combination of row solutions has det a unit mod 26.
Portax: all 13 slides per column, table built from row strings (as plant174.py).
Ragbaby: explicit enumeration of word divisions inside each crib and of the start of the word in progress (<= 20 letters), any n0.
usage (from run/): recount174.py TEXT perms.bin lo hi which [label]   -> one line per family sub-cell with counts (and RB/PX per-config lists)"""
import sys, itertools, numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CR = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
ct, pf, lo, hi, which = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
lab = sys.argv[6] if len(sys.argv) > 6 else "x"
PERM = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
def rows_space(u):
    return np.array(list(itertools.product(range(26), repeat=u)), dtype=np.int64)
SP = {u: rows_space(u) for u in (2, 3)}
def hill_counts(S, n, aff, alph, ix):
    num = {c: i for i, c in enumerate(alph)}; C = [num[c] for c in ct]
    if ix == 0: Z = [C[S[i]] for i in range(97)]; known = {i: num[c] for i, c in CR.items()}
    else: Z = C; known = {S[i]: num[c] for i, c in CR.items()}
    res = []
    for off in range(n):
        u = n + aff; X = SP[u]; ok = True; sols = []
        for r in range(n):
            eqs = [(Z[off + n * ((j - off) // n): off + n * ((j - off) // n) + n], v) for j, v in known.items()
                   if j >= off and (j - off) % n == r and off + n * ((j - off) // n + 1) <= 97]
            m = np.ones(len(X), bool)
            for z, v in eqs:
                coef = np.array(list(z) + ([1] if aff else []), dtype=np.int64); m &= (X @ coef) % 26 == v
            if not m.any(): ok = False; break
            sols.append(X[m][:, :n])
        inv = False
        if ok:
            for combo in itertools.islice(itertools.product(*sols), 200000):
                D = np.array(combo); d = int(round(np.linalg.det(D))) % 26
                if d % 2 and d % 13: inv = True; break
        res.append((off, ok, inv))
    return res
def portax_pair(x, y, k, A):
    up = [A[0:13], "".join(A[13 + (c + k) % 13] for c in range(13))]; lo_ = [A[0::2], A[1::2]]
    rx = 0 if x in up[0] else 1; cx = up[rx].index(x); ry = 0 if y in lo_[0] else 1; cy = lo_[ry].index(y)
    if cx != cy: return up[rx][cy], lo_[ry][cx]
    return up[1 - rx][cx], lo_[1 - ry][cx]
def portax_ok(S, alph, ix, p):
    if ix == 0: T = [ct[S[i]] for i in range(97)]; known = dict(CR)
    else: T = list(ct); known = {S[i]: c for i, c in CR.items()}
    for j in range(p):
        pairs = [(t, t + p) for t in range(j, 97, 2 * p) if t + p < 97 and (t in known or t + p in known)]
        if pairs and not any(all((t not in known or portax_pair(T[t], T[s], k, alph)[0] == known[t]) and
                                 (s not in known or portax_pair(T[t], T[s], k, alph)[1] == known[s]) for t, s in pairs) for k in range(13)):
            return False
    return True
def rag_fit(S, A, d):
    for st, word in ((21, "EASTNORTHEAST"), (63, "BERLINCLOCK")):
        L = len(word); s = [(d * (A.index(ct[S[st + j]]) - A.index(word[j]))) % 26 for j in range(L)]  # = n0 + w + jj + 1
        found = False
        for mask in range(1 << (L - 1)):
            starts = [st + j for j in range(1, L) if mask >> (j - 1) & 1]
            for a0 in range(st - 19, st + 1):            # start of the word in progress at the crib start
                if starts and starts[0] - a0 > 20: continue
                ws = [a0] + starts
                # letter i in word w (start ws[w]) must have s = base + w + (i - ws[w]) for one base mod 26
                base = None; good = True
                for j in range(L):
                    i = st + j; w = max(k for k in range(len(ws)) if ws[k] <= i); b = (s[j] - w - (i - ws[w])) % 26
                    if base is None: base = b
                    elif b != base: good = False; break
                if good: found = True; break
            if found: break
        if not found: return False
    return True
out = []
if which == "hill":
    tot = {}
    for q in range(lo, hi):
        S = [int(x) for x in PERM[q]]
        for n, aff in ((2, 0), (2, 1), (3, 0)):
            for nm, alph in (("AZ", AZ), ("KA", KA)):
                for ix in (0, 1):
                    for off, ok, inv in hill_counts(S, n, aff, alph, ix):
                        k = (n, aff, nm, ix, off); c = tot.setdefault(k, [0, 0, 0]); c[0] += 1; c[1] += ok; c[2] += inv
    for k, c in sorted(tot.items()): print("RH", lab, *k, *c)
elif which == "portax":
    tot = {}
    for q in range(lo, hi):
        S = [int(x) for x in PERM[q]]
        for nm, alph in (("AZ", AZ), ("KA", KA)):
            for ix in (0, 1):
                for p in range(1, 49):
                    c = tot.setdefault((nm, ix, p), [0, 0]); c[0] += 1
                    if portax_ok(S, alph, ix, p): c[1] += 1; print("PX", lab, q, nm, ix, p)
    for k, c in sorted(tot.items()): print("RP", lab, *k, *c)
elif which == "rag":
    al = [l.split() for l in open("../support/alpha172.txt")]; alist = al[:int(sys.argv[7])] if len(sys.argv) > 7 else al
    n = 0; b = 0
    for q in range(lo, hi):
        S = [int(x) for x in PERM[q]]
        for A, L in alist:
            for d in (1, -1):
                n += 1
                if rag_fit(S, A, d): b += 1; print("RB", lab, q, L, d)
    print("RR", lab, n, b)
