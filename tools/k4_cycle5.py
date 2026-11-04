"""Cycle 5. (A) annealing, double columnar widths 10-14 x Vigenere P in {5,7} (the near setups of cycle 4), 8 restarts;
(B) K3-style grid rotations (rows of a, rotate CW, rows of b, rotate CW; also CCW and single rotation), all a,b in 2..48,
x periodic Vigenere P 1-12 AZ/KA B1/B2 -> exact crib-consistency test (deterministic, exhaustive);
(C) disrupted columnar (row r ends at the column holding key rank r mod w; triangular disruption) annealing, w 6-12;
(D) autokey inside the annealer: CT-autokey and PT-autokey (lag L 1-7, AZ/KA) after double columnar 5-9.
Planted controls for B, C, D:  python3 tools/k4_cycle5.py control | A | B | C | D"""
import sys, math, random, zlib, json, itertools
from multiprocessing import Pool
sys.path.insert(0, "tools")
import k4_anneal as KA_
from k4_anneal import AZ, KA, KN, N, quad, MONO, columnar, build, evaluate, mutate
import kryptos_text
K4 = kryptos_text.K4

# ---------- (B) rotations ----------
def rotate_cw(text, w):
    rows = [text[i:i+w] for i in range(0, len(text), w)]
    rows[-1] = rows[-1] + "\0" * (w - len(rows[-1]))
    return "".join("".join(rows[r][c] for r in reversed(range(len(rows)))) for c in range(w)).replace("\0", "")
def rotate_ccw(text, w):
    rows = [text[i:i+w] for i in range(0, len(text), w)]
    rows[-1] = rows[-1] + "\0" * (w - len(rows[-1]))
    return "".join("".join(rows[r][c] for r in range(len(rows))) for c in reversed(range(w))).replace("\0", "")
IDX = "".join(chr(0x100 + i) for i in range(N))
def perm_from(f):  # perm[k] = PT index at CT position k when CT = f(PT)
    return [ord(ch) - 0x100 for ch in f(IDX)]
def rotation_perms():
    P = {}
    for a in range(2, 49):
        for rot, name in ((rotate_cw, "cw"), (rotate_ccw, "ccw")):
            P[(name, a)] = perm_from(lambda t: rot(t, a))
            for b in range(2, 49):
                P[(name, a, b)] = perm_from(lambda t: rot(rot(t, a), b))
    return P
def consistent(perm, alpha, P, model, CT=K4):
    ct_of = [0] * N
    for k, s in enumerate(perm): ct_of[s] = k
    key = {}; n = 0
    for i, pt in KN.items():
        k = ct_of[i]; idx = (k if model == "B2" else i) % P
        v = (alpha.index(CT[k]) - alpha.index(pt)) % 26
        if idx in key:
            n += 1
            if key[idx] != v: return False, n
        key[idx] = v
    return True, n
def run_B(CT=K4, perms=None):
    perms = perms or rotation_perms(); surv = []; tests = 0
    for name, perm in perms.items():
        for an, alpha in (("AZ", AZ), ("KA", KA)):
            for P in range(1, 13):
                for model in ("B1", "B2"):
                    tests += 1; ok, n = consistent(perm, alpha, P, model, CT)
                    if ok and n >= 6: surv.append((name, an, P, model, n))
    return tests, len(perms), surv

# ---------- (C) disrupted columnar ----------
def disrupted(order, n=N):
    w = len(order); rank_col = sorted(range(w), key=lambda c: order[c])
    grid = []; i = 0; r = 0
    while i < n:  # row r filled up to and including column rank_col[r % w]
        L = rank_col[r % w] + 1; L = min(L, n - i); grid.append(list(range(i, i + L))); i += L; r += 1
    out = []
    for c in rank_col:
        out += [row[c] for row in grid if c < len(row)]
    return out

# ---------- (D) autokey ----------
def eval_autokey(CT, perm, alpha, L, mode):
    """B2 order: X = T(PT) is the substitution input at CT position k.  CT-autokey: key_k = CT[k-L] (primer for k<L).
    PT-autokey: key_k = X[k-L].  X[k] = CT[k] - key_k.  Cribs fix X at ct_of[i]."""
    ct_of = [0] * N
    for k, s in enumerate(perm): ct_of[s] = k
    known = {ct_of[i]: alpha.index(p) for i, p in KN.items()}
    c = [alpha.index(ch) for ch in CT]; X = [None] * N; conflicts = 0
    if mode == "ctak":
        prim = {}
        for k in range(N):
            if k >= L: X[k] = (c[k] - c[k-L]) % 26
        for k, v in known.items():
            if k >= L: conflicts += X[k] != v
            else: prim[k] = (c[k] - v) % 26
        for k in range(L):
            kv = prim.get(k)
            if kv is None: kv = max(range(26), key=lambda q: MONO[alpha[(c[k]-q) % 26]])
            X[k] = (c[k] - kv) % 26
    else:  # PT-autokey: X[k] = c[k] - X[k-L]; chains by residue mod L
        for r in range(L):
            chain = list(range(r, N, L)); anchors = [j for j, k in enumerate(chain) if k in known]
            if anchors:
                j0 = anchors[0]; vals = {j0: known[chain[j0]]}
                for j in range(j0 + 1, len(chain)): vals[j] = (c[chain[j]] - vals[j-1]) % 26
                for j in range(j0 - 1, -1, -1): vals[j] = (c[chain[j+1]] - vals[j+1]) % 26
                for j in anchors[1:]: conflicts += vals[j] != known[chain[j]]
                for j, k in enumerate(chain): X[k] = vals[j]
            else:
                best = None
                for p0 in range(26):
                    v = [None] * len(chain); v[0] = (c[chain[0]] - p0) % 26
                    for j in range(1, len(chain)): v[j] = (c[chain[j]] - v[j-1]) % 26
                    s = sum(MONO[alpha[x]] for x in v)
                    if best is None or s > best[0]: best = (s, v)
                for j, k in enumerate(chain): X[k] = best[1][j]
    pt = [""] * N
    for k in range(N): pt[perm[k]] = alpha[X[k]]
    pt = "".join(pt)
    return quad(pt) - 40 * conflicts, conflicts, pt, None

# ---------- generic annealer ----------
def anneal(args):
    CT, family, widths, an, P, model, seed, iters = args
    alpha = AZ if an == "AZ" else KA; rng = random.Random(seed)
    keys = [rng.sample(range(w), w) for w in widths]
    def perm_of(ks): return disrupted(ks[0]) if family == "disrupted" else build("double", ks)
    def ev(ks):
        p = perm_of(ks)
        return eval_autokey(CT, p, alpha, P, model) if model in ("ctak", "ptak") else evaluate(CT, p, alpha, P, model)
    cur = ev(keys); best = (cur, keys)
    for it in range(iters):
        T = 5.0 * (1 - it / iters) + 0.05
        nk = mutate("double", keys, rng); r = ev(nk)
        if r[0] > cur[0] or rng.random() < math.exp((r[0] - cur[0]) / T):
            keys, cur = nk, r
            if cur[0] > best[0][0]: best = (cur, [list(k) for k in keys])
    (sc, conf, pt, _), bk = best
    return dict(family=family, widths=widths, alpha=an, P=P, model=model, score=round(sc, 1), conflicts=conf,
                per_quad=round((sc + 40 * conf) / (N - 3), 3), keys=bk, pt=pt)
def seed(*a): return zlib.crc32(repr(a).encode())
def report(R, label):
    R.sort(key=lambda r: -r["score"]); zc = [r for r in R if r["conflicts"] == 0]
    print(f"[{label}] runs {len(R)}; min conflicts {min(r['conflicts'] for r in R)}; runs at 0 conflicts {len(zc)}; "
          f"best per_quad at 0 conflicts {max([r['per_quad'] for r in zc], default=None)}")
    for r in R[:5]: print("   ", json.dumps(r))

def planted_pt():
    eng = ("WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKETWELVEANDTHEN")
    pt = list(eng[:N])
    for i, ch in KN.items(): pt[i] = ch
    return "".join(pt)
def enc_periodic(pt, perm, alpha, key):
    return "".join(alpha[(alpha.index(pt[perm[k]]) + alpha.index(key[k % len(key)])) % 26] for k in range(N))

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "control":
        pt = planted_pt(); print("planted PT:", pt, f"(quad/char {quad(pt)/(N-3):.3f})")
        # B: rotation (cw, 8, 13) + KA Vigenere 'BERLIN' (P=6, B2) -> must be found by exhaustive test
        perms = rotation_perms(); p = perms[("cw", 8, 13)]
        t, n, s = run_B(enc_periodic(pt, p, KA, "BERLIN"), perms)
        print(f"[control B] tests {t}; planted ('cw',8,13) KA P6 B2 recovered: {any(x[0]==('cw',8,13) and x[1]=='KA' and x[2]==6 and x[3]=='B2' for x in s)}; total survivors {len(s)}")
        # C: disrupted columnar w=8 + AZ Vigenere 'KEY' (P=3, B2)
        o = [5, 2, 7, 0, 3, 6, 1, 4]; CT = enc_periodic(pt, disrupted(o), AZ, "KEY")
        with Pool() as pool: R = pool.map(anneal, [(CT, "disrupted", (8,), "AZ", 3, "B2", s, 20000) for s in range(16)])
        report(R, "control C disrupted w8 AZ P3"); print("    planted order recovered:", sum(r["keys"][0] == o for r in R), "/16")
        # D: PT-autokey L=4 KA after double columnar (5,7)
        o1, o2 = [2, 0, 4, 1, 3], [4, 1, 6, 0, 3, 5, 2]; perm = build("double", [o1, o2])
        X = [KA.index(pt[perm[k]]) for k in range(N)]; prim = [KA.index(ch) for ch in "CODE"]
        CT = "".join(KA[(X[k] + (prim[k] if k < 4 else X[k-4])) % 26] for k in range(N))
        with Pool() as pool: R = pool.map(anneal, [(CT, "double", (5, 7), "KA", 4, "ptak", s, 20000) for s in range(16)])
        report(R, "control D PT-autokey L4 KA, double (5,7)"); print("    planted keys recovered:", sum(r["keys"] == [o1, o2] for r in R), "/16")
    elif what == "A":
        J = [(K4, "double", (a, b), an, P, m, seed("A", a, b, an, P, m, s), 20000)
             for a in range(10, 15) for b in range(5, 15) for an in ("AZ", "KA") for P in (5, 7) for m in ("B1", "B2") for s in range(8)
             if a >= b or b >= 10]
        with Pool() as pool: R = pool.map(anneal, J, chunksize=8)
        report(R, "A double columnar w 10-14 x P{5,7}")
    elif what == "B":
        t, n, s = run_B(); print(f"[B] rotation perms {n}; tests {t}; survivors with >=6 constraints: {len(s)}")
        for x in s[:30]: print("   ", x)
    elif what == "C":
        J = [(K4, "disrupted", (w,), an, P, m, seed("C", w, an, P, m, s), 20000)
             for w in range(6, 13) for an in ("AZ", "KA") for P in range(1, 8) for m in ("B1", "B2") for s in range(4)]
        with Pool() as pool: R = pool.map(anneal, J, chunksize=8)
        report(R, "C disrupted columnar w 6-12")
    elif what == "D":
        J = [(K4, "double", (a, b), an, L, m, seed("D", a, b, an, L, m, s), 15000)
             for a in range(5, 10) for b in range(5, 10) for an in ("AZ", "KA") for L in range(1, 8) for m in ("ctak", "ptak") for s in range(2)]
        with Pool() as pool: R = pool.map(anneal, J, chunksize=8)
        report(R, "D autokey (CT/PT) after double columnar 5-9")
