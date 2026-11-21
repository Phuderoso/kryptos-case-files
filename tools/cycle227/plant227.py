"""Cycle 227 Gate P (PREREG227): 20 planted ciphertexts on the NEW keyboard geometries / alphabets, seed 209548.
G 4 (DHIA-W / DHIA-M / KRYPTOS-QW / PALIMPSEST-QW / ABSCISSA-QW), V 7 (any of the 8 geometries of geo227a / geo227b),
Q 9 (kb227.bin pairs, both not in {AZ, KA}); V / Q periods 3-24; scope pid % 3 (direct / bank / all.bin); odd pids carry one wrong
carved crib letter; plaintext K1-K3 (pid % 4 in {0,1}) or Jane Eyre body (pid % 4 in {2,3}). usage: plant227.py WORKDIR"""
import sys, random, numpy as np
W = sys.argv[1]; N = 97; SEED = 209548
POS = list(range(21, 34)) + list(range(63, 74)); CRIB = "EASTNORTHEAST" + "BERLINCLOCK"
txt = "".join(c for c in open(W + "/k123_eng.txt").read().upper() if c.isalpha())
je = open(W + "/rk_plain.txt", errors="ignore").read(); je = je[je.index("CHAPTER I"):je.index("END OF THE PROJECT GUTENBERG")]
je = "".join(c for c in je.upper() if "A" <= c <= "Z")
kb = np.fromfile(W + "/kb227.bin", dtype=np.uint8).reshape(-1, 26); nA = len(kb); AZ, KA = nA - 2, nA - 1
AI = np.zeros_like(kb); [AI.__setitem__((a, kb[a, i]), i) for a in range(nA) for i in range(26)]
GEO = {}
for tag in "ab":
    for l, line in enumerate(open(f"{W}/geo227{tag}.txt")):
        f = line.split(); GEO[(tag, l)] = (f[0], [tuple(map(int, t.split(","))) for t in f[1:]])
GNEW = [("a", 0), ("a", 1), ("a", 2), ("a", 3), ("b", 0)]
banks = {1: np.fromfile(W + "/bank.bin", dtype=np.int16).reshape(-1, N), 2: np.fromfile(W + "/all.bin", dtype=np.int16).reshape(-1, N)}
R = random.Random(SEED)
out = open(W + "/plants227.tsv", "w")
for pid in range(20):
    src = txt if pid % 4 < 2 else je
    s0 = R.randrange(len(src) - N); pt = list(src[s0:s0 + N])
    for j, i in enumerate(POS): pt[i] = CRIB[j]
    P = [ord(c) - 65 for c in pt]
    scope = pid % 3
    if scope == 0: row, d, S = -1, 0, list(range(N))
    else:
        row = R.randrange(len(banks[scope])); d = R.randrange(2); perm = [int(v) for v in banks[scope][row]]
        inv = [0] * N
        for i, v in enumerate(perm): inv[v] = i
        S = perm if d == 0 else inv
    model = "G" if pid < 4 else "V" if pid < 11 else "Q"
    ix = 0 if scope == 0 else R.randrange(2)
    kidx = [i if ix == 0 else S[i] for i in range(N)]
    layer = [0] * N; geo = "a"
    if model == "G":
        geo, lay = R.choice(GNEW); part = R.randrange(2); g = GEO[(geo, lay)][1]   # colB == colA on DHIA, so parts 0 / 1
        for i in range(N):
            cls = [x for x in range(26) if g[x][part] == g[P[i]][part]]; layer[i] = R.choice(cls)
        desc = f"part={part} lay={lay}"; p = 0
    elif model == "V":
        geo, lay = R.choice(sorted(GEO)); g = GEO[(geo, lay)][1]; p = R.randrange(3, 25)
        cell = {(g[x][0], g[x][1]): x for x in range(26)}
        for r in range(p):
            idx = [i for i in range(N) if kidx[i] % p == r]
            ok = [(dr, dc) for dr in range(3) for dc in range(10)
                  if all(((g[P[i]][0] + dr) % 3, (g[P[i]][1] + dc) % 10) in cell for i in idx)]
            dr, dc = R.choice(ok)
            for i in idx: layer[i] = cell[((g[P[i]][0] + dr) % 3, (g[P[i]][1] + dc) % 10)]
        desc = f"lay={lay}"
    else:
        while True:
            x, y = R.randrange(nA), R.randrange(nA)
            if not ((x in (AZ, KA)) and (y in (AZ, KA))): break
        f, p = R.randrange(3), R.randrange(3, 25); key = [R.randrange(26) for _ in range(p)]
        for i in range(N):
            xv, k = int(AI[x, P[i]]), key[kidx[i] % p]
            layer[i] = int(kb[y, (xv + k) % 26 if f == 0 else (xv - k) % 26 if f == 1 else (k - xv) % 26])
        desc = f"X={x} Y={y} form={f}"
    carved = [0] * N
    for i in range(N): carved[S[i]] = layer[i]
    bad = -1
    if pid % 2 == 1:
        j = R.randrange(24); bad = j; c = S[POS[j]]; carved[c] = R.choice([v for v in range(26) if v != carved[c]])
    ct = "".join(chr(65 + v) for v in carved)
    out.write(f"{pid}\t{model}\t{geo}\t{scope}\t{row}\t{d}\t{ix}\t{p}\t{desc}\t{bad}\t{ct}\t{''.join(pt)}\n")
out.close()
