"""Cycle 175 planted controls (IDEAS I-111 + I-113), written independently of slip175.c / hill175.c (string alphabets,
direct encryption from the definitions, no index tables or shared code).
Two-slip plants: periodic key on a (PA, CA) tableau, c = CA[(PA.index(p) + k) % 26] (vig) or CA[(k - PA.index(p)) % 26] (beau),
key at plaintext index (pt) or true-ciphertext index (ct); K3-law decimation of the n-letter true ciphertext C';
then on the copper: del (C' 98 letters, letter d left off) or ins (C' 96, extra letter at carved index d), AND the carved letter
under crib j changed. 'strict' = del without the crib change. 'neg' = del + TWO changed crib letters (must be missed).
Hill plants: encryption Z = E.X + f (mod 26) on blocks of n = 4 at offset off (letters outside whole blocks copied), E random
invertible; ix 0 Hill on the plaintext order then transposition (C[S[i]] = Y[i]); ix 1 transposition (X[S[i]] = P[i]) then Hill.
Hill 'neg' = one carved crib letter altered.  Each plant is hidden at slot 100 of a 200-perm slice.
usage: plant175.py outdir seed"""
import sys, random, os, json, numpy as np
out, seed = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True); R = random.Random(seed)
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; TAB = {"AZ": AZ, "KA": KA}
CRP = list(range(21, 34)) + list(range(63, 74)); CRL = "EASTNORTHEAST" + "BERLINCLOCK"
BASE = ("ACOLDWINDCAMEOVERTHEW" + "EASTNORTHEAST" + "RIDGEANDTHESURVEYORSFOUNDTHEX" + "BERLINCLOCK" + "STILLRUNNINGBENEATHSNOWX")
def ptext(n):
    s = BASE[:n]; assert len(s) == n and all(s[j] == c for j, c in zip(CRP, CRL)); return s
FAM = {98: "support/dec98.bin", 96: "support/dec96.bin", 97: "support/all.bin"}
KEYS = {5: "LUCID", 6: "SHADOW", 7: "COMPASS", 9: "ABSCISSAS", 10: "PALIMPSEST", 11: "UNDERGROUND", 13: "MAGNETICFIELD", 16: "ILLUMINATIONLAMP"}
plan = [("delx", "pt", "vig", "KA", "KA", 7), ("delx", "ct", "beau", "AZ", "KA", 11), ("delx", "pt", "vig", "AZ", "AZ", 16),
        ("insx", "ct", "vig", "KA", "AZ", 6), ("insx", "pt", "beau", "KA", "KA", 13), ("insx", "ct", "vig", "AZ", "AZ", 10),
        ("strict", "pt", "beau", "KA", "AZ", 9), ("neg", "ct", "vig", "KA", "KA", 5)]
def sub(t, key, PA, CA, beau):
    return "".join(CA[((AZ.index(key[i % len(key)]) - PA.index(c)) if beau else (PA.index(c) + AZ.index(key[i % len(key)]))) % 26] for i, c in enumerate(t))
def bump(ch): return AZ[(AZ.index(ch) + 1 + R.randrange(25)) % 26]
rows = []
for nn, (model, ix, mode, pa, ca, p) in enumerate(plan):
    n = 96 if model == "insx" else 98
    PERM = np.fromfile(FAM[n], dtype=np.int16).reshape(-1, n); q = R.randrange(100, len(PERM) - 100); perm = [int(x) for x in PERM[q]]
    P = ptext(n); key = KEYS[p]; PA, CA = TAB[pa], TAB[ca]; beau = mode == "beau"
    if ix == "pt":
        s = sub(P, key, PA, CA, beau); C = [None] * n
        for j in range(n): C[perm[j]] = s[j]
    else:
        T = [None] * n
        for j in range(n): T[perm[j]] = P[j]
        C = list(sub("".join(T), key, PA, CA, beau))
    C = "".join(C)
    if model == "insx":
        d = R.randrange(97); carved = C[:d] + R.choice(AZ) + C[d:]
        def cpos(u): return u if u < d else u + 1
    else:
        under = [perm[j] for j in CRP]
        d = R.choice([x for x in range(98) if x not in under]); carved = C[:d] + C[d + 1:]
        def cpos(u): return u if u < d else u - 1
    ch = []
    if model in ("delx", "insx"): ch = [R.randrange(24)]
    elif model == "neg": ch = R.sample(range(24), 2)
    cv = list(carved)
    for k in ch: x = cpos(perm[CRP[k]]); cv[x] = bump(cv[x])
    carved = "".join(cv); assert len(carved) == 97
    PERM[q - 100:q + 100].tofile(f"{out}/ctl{nn}_slice.bin"); open(f"{out}/ctl{nn}.txt", "w").write(carved + "\n")
    rows.append(dict(name=f"ctl{nn}", kind="slip", model=model, n=n, q=q, d=d, drop=ch, PA=pa, CA=ca, mode=mode, idx=ix, p=p, key=key))
# ---- Hill n = 4 plants
def det_int(M):
    M = [r[:] for r in M]; n = len(M)
    if n == 1: return M[0][0]
    return sum((-1) ** c * M[0][c] * det_int([r[:c] + r[c + 1:] for r in M[1:]]) for c in range(n))
def rand_inv(n):
    while True:
        E = [[R.randrange(26) for _ in range(n)] for _ in range(n)]
        if det_int(E) % 2 and det_int(E) % 13: return E
HP = [(0, "AZ", 0, 0), (1, "KA", 1, 1), (0, "KA", 1, 3), (1, "AZ", 0, 2), ("neg", "AZ", 0, 1)]
PERM = np.fromfile(FAM[97], dtype=np.int16).reshape(-1, 97)
for hn, (aff, num, ix, off) in enumerate(HP):
    neg = aff == "neg"; aff = 0 if neg else aff; nm = TAB[num]; n = 4
    q = R.randrange(100, len(PERM) - 100); S = [int(x) for x in PERM[q]]; P = ptext(97)
    E = rand_inv(n); f = [R.randrange(26) for _ in range(n)] if aff else [0] * n
    def hill(X):
        v = [nm.index(c) for c in X]; o = list(X)
        for b in range((97 - off) // n):
            blk = v[off + n * b: off + n * b + n]
            for r in range(n): o[off + n * b + r] = nm[(sum(E[r][c] * blk[c] for c in range(n)) + f[r]) % 26]
        return "".join(o)
    if ix == 0:
        Y = hill(P); C = [None] * 97
        for i in range(97): C[S[i]] = Y[i]
        C = "".join(C)
    else:
        X = [None] * 97
        for i in range(97): X[S[i]] = P[i]
        C = hill("".join(X))
    if neg:
        x = S[CRP[4]]; C = C[:x] + bump(C[x]) + C[x + 1:]
    name = f"hctl{hn}"; PERM[q - 100:q + 100].tofile(f"{out}/{name}_slice.bin"); open(f"{out}/{name}.txt", "w").write(C + "\n")
    rows.append(dict(name=name, kind="hill", neg=neg, aff=aff, num=num, ix=ix, off=off, q=q, E=E, f=f, pt=P))
json.dump(rows, open(f"{out}/plants.json", "w"), indent=0)
for r in rows: print({k: v for k, v in r.items() if k not in ("pt", "E")})
