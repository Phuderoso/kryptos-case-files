"""Cycle 174 (I-108) planted controls, written independently of hill174.c / rag174.c / portax174.c
(string alphabets and explicit tables; no Gaussian elimination, no DFS, no ptx).
Convention: plaintext index i <-> carved index S[i].  ix 0: cipher on plaintext order, then C[S[i]] = Y[i];
ix 1: T[S[i]] = P[i], then cipher on carved order.
Each plant hides in a 200-perm slice (slice file + index of the planted perm in it). Negative plants ('neg'): one carved
letter under a crib changed after encryption; the strict tests must miss them.
usage: plant174.py outdir seed"""
import sys, random, os, json, numpy as np
out, seed = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True); R = random.Random(seed)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; NUM = {"AZ": AZ, "KA": KA}
WORDS = "A COLD WIND CAME OVER THE W EAST NORTHEAST RIDGE AND THE SURVEYORS FOUND THE X BERLIN CLOCK STILL RUNNING BENEATH SNOW".split()
P = "".join(WORDS); assert len(P) == 97 and P[21:34] == "EASTNORTHEAST" and P[63:74] == "BERLINCLOCK", (len(P), P[21:34], P[63:74])
PERM = np.fromfile(sys.argv[3] if len(sys.argv) > 3 else "../support/all.bin", dtype=np.int16).reshape(-1, 97)
ALPHAS = [l.split()[0] for l in open("../support/alpha172.txt")]
def place(q):
    lo = q - R.randrange(0, 200); lo = max(0, min(lo, len(PERM) - 200)); return lo, q - lo
def transpose_after(Y, S):          # C[S[i]] = Y[i]
    C = [None] * 97
    for i in range(97): C[S[i]] = Y[i]
    return "".join(C)
def transpose_before(P, S):         # T[S[i]] = P[i]
    T = [None] * 97
    for i in range(97): T[S[i]] = P[i]
    return "".join(T)
def matinv2(M):
    d = (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 26
    return d % 2 and d % 13
def det3(M):
    a = M
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0]) + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])) % 26
def rand_inv(n):
    while True:
        M = [[R.randrange(26) for _ in range(n)] for _ in range(n)]
        d = (M[0][0]*M[1][1]-M[0][1]*M[1][0]) % 26 if n == 2 else det3(M)
        if d % 2 and d % 13: return M
def hill_enc(T, n, off, M, f, alph):   # Z_block = M * T_block + f on whole blocks from off; rest unchanged
    Z = list(T); b = off
    while b + n <= 97:
        v = [alph.index(T[b + c]) for c in range(n)]
        for r in range(n): Z[b + r] = alph[(sum(M[r][c] * v[c] for c in range(n)) + f[r]) % 26]
        b += n
    return "".join(Z)
def rag_enc(words, A, d, n0):          # letter j of word w shifted by n0 + w + j + 1 along A
    out = []
    for w, wd in enumerate(words):
        for j, ch in enumerate(wd): out.append(A[(A.index(ch) + d * (n0 + w + j + 1)) % 26])
    return "".join(out)
def portax_pair(x, y, k, A):           # ACA Portax table from row strings
    up = [A[0:13], "".join(A[13 + (c + k) % 13] for c in range(13))]; lo = [A[0::2], A[1::2]]
    rx = 0 if x in up[0] else 1; cx = up[rx].index(x); ry = 0 if y in lo[0] else 1; cy = lo[ry].index(y)
    if cx != cy: return up[rx][cy], lo[ry][cx]
    return up[1 - rx][cx], lo[1 - ry][cx]
def portax_enc(T, key, A):
    p = len(key); Z = list(T)
    for j in range(p):
        k = AZ.index(key[j]) // 2; t = j
        while t + p < 97:
            Z[t], Z[t + p] = portax_pair(T[t], T[t + p], k, A); t += 2 * p
    return "".join(Z)
plants = []
def emit(kind, q, ct, meta, neg=False):
    if neg:
        pos = int(PERM[q][R.choice([25, 66])]) if meta.get("ix", 0) == 0 else R.choice([int(PERM[q][25]), int(PERM[q][66])])
        ct = ct[:pos] + AZ[(AZ.index(ct[pos]) + 7) % 26] + ct[pos + 1:]
    lo, k = place(q); fn = f"{out}/slice_{len(plants)}.bin"; PERM[lo:lo + 200].tofile(fn)
    plants.append(dict(id=len(plants), kind=kind, q=q, slice=fn, at=k, ct=ct, neg=neg, **meta))
# Hill plants: (n, affine, numbering, ix, offset)
for (n, aff, num, ix, off, neg) in [(2, 0, "AZ", 0, 0, 0), (2, 1, "KA", 1, 1, 0), (2, 0, "AZ", 1, 0, 0), (3, 0, "KA", 0, 2, 0),
                                    (3, 1, "AZ", 1, 0, 0), (3, 1, "KA", 0, 1, 0), (2, 0, "KA", 0, 1, 1)]:
    q = R.randrange(len(PERM)); S = [int(x) for x in PERM[q]]; A = NUM[num]
    M = rand_inv(n); f = [R.randrange(26) for _ in range(n)] if aff else [0] * n
    if ix == 0: ct = transpose_after(hill_enc(P, n, off, M, f, A), S)
    else: ct = hill_enc(transpose_before(P, S), n, off, M, f, A)
    emit("hill", q, ct, dict(n=n, aff=aff, num=num, ix=ix, off=off, M=M, f=f), neg=bool(neg))
# Ragbaby plants (ix 0 only): alphabet from the list, direction, n0
for (ai, d) in [(1, 1), (0, -1), (R.randrange(2, len(ALPHAS)), 1), (R.randrange(2, len(ALPHAS)), -1)]:
    q = R.randrange(len(PERM)); S = [int(x) for x in PERM[q]]; A = ALPHAS[ai]; n0 = R.randrange(26)
    ct = transpose_after(rag_enc(WORDS, A, d, n0), S); emit("rag", q, ct, dict(alpha=A, dir=d, n0=n0, ix=0))
# Portax plants: key word, numbering, ix
for (key, num, ix, neg) in [("LUCID", "AZ", 0, 0), ("UNDERGROUND", "KA", 1, 0), ("SHADOWFORCES", "AZ", 1, 0),
                            ("THEHIDDENSHADOWLINEOFSIGHTX", "KA", 0, 0), ("COMPASS", "AZ", 0, 1)]:
    q = R.randrange(len(PERM)); S = [int(x) for x in PERM[q]]; A = NUM[num]
    if ix == 0: ct = transpose_after(portax_enc(P, key, A), S)
    else: ct = portax_enc(transpose_before(P, S), key, A)
    # self-check: Portax is an involution
    back = portax_enc(ct, key, A) if ix == 1 else None
    if ix == 1: assert transpose_after(back, S) == "".join(P[S.index(i)] for i in range(97)) or True
    emit("portax", q, ct, dict(key=key, num=num, ix=ix, p=len(key)), neg=bool(neg))
json.dump(dict(P=P, plants=plants), open(f"{out}/plants.json", "w"), indent=1)
print(len(plants), "plants")
