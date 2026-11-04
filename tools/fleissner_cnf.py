"""Cycle 48: turning grille 10x10, convention B (classic Fleissner direction), exact SAT (pysat/CaDiCaL).
Plaintext j is written into the j-th hole slot (rotation r = j//25, holes in row-major order within a rotation);
the last 3 slots of rotation 4 stay empty; the grid is read row-major, empty cells skipped. A periodic
Vigenere/Beaufort key (A-Z or KRYPTOS numbering) acts before ('pt': key index = plaintext position) or after
('ct': key index = ciphertext position) the transposition. Unary sequential counters give each cell's rank inside
its rotation and the number of empty cells before it, so every crib letter becomes clauses. UNSAT excludes the
whole configuration (all 4^25 grilles x all 26^L keys). Usage: python3 fleissner_cnf.py TEXT|K4 SIDE TAB MODE L
"""
import sys, time
from pysat.solvers import Solver
from pysat.card import CardEnc
from grille_sat import K4, KA, AZ, CRIBS, WHERE, ORB, N

def solve(text, side, alpha, mode, L):
    C = [alpha.index(ch) for ch in text]
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    cl = []
    X = [[new() for o in range(4)] for k in range(25)]
    for k in range(25):
        enc = CardEnc.equals(lits=X[k], bound=1, top_id=nv[0]); nv[0] = max(nv[0], enc.nv); cl += enc.clauses
    TRUE = new(); cl.append([TRUE])
    def op(c, r):
        k, q = WHERE[c]; return X[k][(q - r) % 4]
    # A[r][c][t]: at least t opens of rotation r among cells < c (t = 0..26)
    A = [[None] * 101 for r in range(4)]
    for r in range(4):
        A[r][0] = [TRUE] + [-TRUE] * 26
        for c in range(100):
            prev = A[r][c]; o = op(c, r); cur = [TRUE]
            for t in range(1, 27):
                v = new(); cur.append(v)
                # v <-> prev[t] or (prev[t-1] and o)
                cl += [[-prev[t], v], [-prev[t - 1], -o, v], [-v, prev[t], prev[t - 1]], [-v, prev[t], o]]
            A[r][c + 1] = cur
    # empties: open in rotation 3 with rank >= 22
    EM = []
    for c in range(100):
        e = new(); o = op(c, 3); a = A[3][c][22]
        cl += [[-e, o], [-e, a], [e, -o, -a]]; EM.append(e)
    cl.append([A[3][100][25]])  # sanity (always true)
    D = [None] * 101
    D[0] = [TRUE] + [-TRUE] * 4
    for c in range(100):
        prev = D[c]; cur = [TRUE]
        for t in range(1, 5):
            v = new(); cur.append(v)
            cl += [[-prev[t], v], [-prev[t - 1], -EM[c], v], [-v, prev[t], prev[t - 1]], [-v, prev[t], EM[c]]]
        D[c + 1] = cur
    cl.append([-D[100][4]])
    K = [[new() for v in range(26)] for i in range(L)]
    for i in range(L):
        enc = CardEnc.equals(lits=K[i], bound=1, top_id=nv[0]); nv[0] = max(nv[0], enc.nv); cl += enc.clauses
    for j, ch in CRIBS.items():
        P = alpha.index(ch); r, t = divmod(j, 25)
        for c in range(100):
            for e in range(4):
                T = c - e
                base = [-op(c, r), -A[r][c][t], A[r][c][t + 1], -D[c][e], D[c][e + 1]]
                if T < 0 or T >= N: cl.append(base); continue
                idx = (j if side == "pt" else T) % L
                v = (C[T] - P) % 26 if mode == "vig" else (C[T] + P) % 26
                cl.append(base + [K[idx][v]])
    s = Solver(name="cadical153", bootstrap_with=cl)
    ok = s.solve()
    res = None
    if ok:
        m = set(x for x in s.get_model() if x > 0)
        o = [next(q for q in range(4) if X[k][q] in m) for k in range(25)]
        key = "".join(alpha[next(v for v in range(26) if K[i][v] in m)] for i in range(L))
        res = (o, key)
    s.delete()
    return ok, res

if __name__ == "__main__":
    src, side, tab, mode, L = sys.argv[1:6]; L = int(L)
    text = K4 if src == "K4" else open(src).read().strip()
    alpha = AZ if tab == "AZ" else KA
    t0 = time.time(); ok, res = solve(text, side, alpha, mode, L)
    out = f"{src} {side} {tab} {mode} L={L} {'SAT' if ok else 'UNSAT'} {time.time()-t0:.1f}s"
    if ok:
        from grille_sat import encrypt, perm_from_choice
        o, key = res
        # verify by real decryption consistency on cribs
        tp = perm_from_choice(o, "B"); Cv = [alpha.index(x) for x in text]; Kv = [alpha.index(x) for x in key]
        good = 0
        for j, ch in CRIBS.items():
            T = tp[j]; kidx = (j if side == "pt" else T) % L
            p = (Cv[T] - Kv[kidx]) % 26 if mode == "vig" else (Kv[kidx] - Cv[T]) % 26
            good += alpha[p] == ch
        out += f" grille={''.join(map(str,o))} key={key} verified={good}/24"
    print(out, flush=True)
