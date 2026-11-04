"""Cycle 47: turning grille 10x10 (97 letters + 3 empty cells) x periodic key, exact SMT (z3).

Grille: 25 holes, one per rotation orbit of the 10x10 square; rotated clockwise 4 times.
Convention A (K3-like): plaintext written row-major into the grid (cells 97-99 empty), read through the holes
  rotation by rotation, holes in row-major order, empty cells skipped -> ciphertext.
Convention B (classic grille): plaintext written through the holes (same order), the last 3 hole slots left empty;
  grid read row-major, empty cells skipped -> ciphertext.
Substitution: Vigenere or Beaufort, A-Z or KRYPTOS numbering, periodic key of length L, applied either
  before the transposition (key index = plaintext position, 'pt') or after it (key index = ciphertext position, 'ct').
Exact: SAT means some grille and key reproduce all 24 crib letters. UNSAT excludes the whole configuration.
Usage: python3 grille_sat.py TEXT CONV SIDE TABLEAU MODE L [timeout_s]
"""
import sys, z3
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRIBS = {21 + i: ch for i, ch in enumerate("EASTNORTHEAST")}
CRIBS.update({63 + i: ch for i, ch in enumerate("BERLINCLOCK")})
N, W = 97, 10

def rot(c):
    i, j = divmod(c, W); return j * W + (W - 1 - i)

def orbits():
    orb, where = [], {}
    for i in range(5):
        for j in range(5):
            cyc = [i * W + j]
            for _ in range(3): cyc.append(rot(cyc[-1]))
            for q, c in enumerate(cyc): where[c] = (len(orb), q)
            orb.append(cyc)
    return orb, where
ORB, WHERE = orbits()

def perm_from_choice(o, conv):
    """Return ct_index_of_pt[j] for a concrete grille choice o (list of 25 values 0-3)."""
    rd = {}
    for c in range(100):
        k, q = WHERE[c]; rd[c] = (q - o[k]) % 4
    order = sorted(range(100), key=lambda c: (rd[c], c))   # hole read/write order
    if conv == "A":
        seq = [c for c in order if c < N]                    # cells read, empties skipped
        return {c: t for t, c in enumerate(seq)}             # pt j sits in cell j
    cell_of_pt = {j: order[j] for j in range(N)}
    filled = sorted(cell_of_pt.values())
    ctpos = {c: t for t, c in enumerate(filled)}
    return {j: ctpos[cell_of_pt[j]] for j in range(N)}

def encrypt(pt, o, conv, side, alpha, mode, key):
    P = [alpha.index(ch) for ch in pt]; L = len(key); Kv = [alpha.index(ch) for ch in key]
    tp = perm_from_choice(o, conv)
    def sub(x, i): return (x + Kv[i % L]) % 26 if mode == "vig" else (Kv[i % L] - x) % 26
    if side == "pt": I = [sub(P[j], j) for j in range(N)]
    else: I = P[:]
    C = [0] * N
    for j in range(N): C[tp[j]] = I[j]
    if side == "ct": C = [sub(C[t], t) for t in range(N)]
    return "".join(alpha[x] for x in C)

def build(text, conv, side, alpha, mode, L):
    s = z3.Solver()
    B = [[z3.Bool(f"b{k}_{v}") for v in range(4)] for k in range(25)]
    for k in range(25):
        s.add(z3.PbEq([(b, 1) for b in B[k]], 1))
    H = {}
    for c in range(100):
        k, q = WHERE[c]
        for r in range(4): H[c, r] = B[k][(q - r) % 4]
    def bi(x): return z3.If(x, 1, 0)
    # R(c): hole order index of cell c
    R = {}
    for c in range(100):
        terms = []
        for r in range(4):
            terms.append(z3.If(H[c, r], 25 * r + z3.Sum([bi(H[cp, r]) for cp in range(c)]) if c else z3.IntVal(25 * r), 0))
        R[c] = z3.Sum(terms)
    Cv = [alpha.index(ch) for ch in text]
    K = [z3.Int(f"k{i}") for i in range(L)]
    for kv in K: s.add(kv >= 0, kv < 26)
    def need(cls_expr_pairs):
        pass
    def keyval(t, j):
        p = alpha.index(CRIBS[j])
        return (Cv[t] - p) % 26 if mode == "vig" else (Cv[t] + p) % 26
    if conv == "A":
        for j in CRIBS:
            c = j
            # empties 97,98,99 read before c iff their rotation < c's rotation
            T = z3.Sum([z3.If(H[c, r], 25 * r + (z3.Sum([bi(H[cp, r]) for cp in range(c)]) if c else 0)
                              - z3.Sum([bi(H[e, rp]) for e in (97, 98, 99) for rp in range(r)]) if r else
                              (z3.Sum([bi(H[cp, r]) for cp in range(c)]) if c else z3.IntVal(0)), 0) for r in range(4)])
            Tj = z3.Int(f"t{j}"); s.add(Tj == T, Tj >= 0, Tj < N)
            for t in range(N):
                idx = j % L if side == "pt" else t % L
                s.add(z3.Implies(Tj == t, K[idx] == keyval(t, j)))
    else:
        E = {c: R[c] >= N for c in range(100)}
        for c in range(100):
            tc = c - (z3.Sum([bi(E[cp]) for cp in range(c)]) if c else 0)
            Tc = z3.Int(f"tc{c}"); s.add(Tc == tc)
            for j in CRIBS:
                for t in range(max(0, c - 3), min(c, N - 1) + 1):
                    idx = j % L if side == "pt" else t % L
                    s.add(z3.Implies(z3.And(R[c] == j, Tc == t), K[idx] == keyval(t, j)))
    return s, B, K

def solve(text, conv, side, tab, mode, L, timeout=120):
    alpha = KA if tab == "KA" else AZ
    s, B, K = build(text, conv, side, alpha, mode, L)
    s.set("timeout", int(timeout * 1000))
    res = s.check()
    if res == z3.sat:
        m = s.model()
        o = [next(v for v in range(4) if z3.is_true(m.eval(B[k][v]))) for k in range(25)]
        key = "".join(alpha[m.eval(kv).as_long()] for kv in K)
        return "sat", o, key
    return str(res), None, None

if __name__ == "__main__":
    name, conv, side, tab, mode, L = sys.argv[1:7]
    to = float(sys.argv[7]) if len(sys.argv) > 7 else 120
    text = K4 if name == "K4" else open(name).read().strip()
    r, o, key = solve(text, conv, side, tab, mode, int(L), to)
    print(name, conv, side, tab, mode, L, r, o if o else "", key or "", flush=True)
