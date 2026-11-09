"""Cycle 193 independent recount for the SANDWICH models (adapted from recount191.py; shares no code with cmp193.c). Model 1: key a
at the plaintext index i, key b at the carved index S[i]; model 2: the reverse. For every config (route row, model, tableau pair, form, ordered pair
2 <= m, n <= MM incl. m = n)
it builds, LITERALLY from letters, the 26x26 table M_t[a][b] = (two-pass encryption of crib letter p_t with key values a then b == carved
letter c_t), using the step definitions vig x+k / beau k-x on each tableau, then counts consistent assignments of every connected component
with a cycle by depth-first propagation vectorised over the 26 values of the component's first vertex (numpy). Output per config with a fit:
F row model tab form m n sols, and per-cell totals T model tab form m n fits sols.
usage: recount191.py CT perms.bin rows(comma) tabpairs.txt MM"""
import sys
import numpy as np
ct, pf, rows, tf, MM = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")], sys.argv[4], int(sys.argv[5])
PERM = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
CRIB = [(21 + i, ch) for i, ch in enumerate("EASTNORTHEAST")] + [(63 + i, ch) for i, ch in enumerate("BERLINCLOCK")]
TABS = [l.split() for l in open(tf) if len(l.split()) == 3]
def step(x, k, s): return (x + k) % 26 if s == "V" else (k - x) % 26
for row in rows:
    S = [int(v) for v in PERM[row]]
    for md in "12":
        pa = [i if md == "1" else S[i] for i, _ in CRIB]; pb = [S[i] if md == "1" else i for i, _ in CRIB]
        for T1, T2, tn in TABS:
            for form in ("VV", "VB", "BV", "BB"):
                # literal tables: Mt[t][a] = the unique b, or -1
                Mt = []
                for (i, pch) in CRIB:
                    c = ct[S[i]]; arr = np.full(26, -1, int)
                    for a in range(26):
                        mid = T1[step(T1.index(pch), a, form[0])]
                        for b in range(26):
                            if T2[step(T2.index(mid), b, form[1])] == c: arr[a] = b
                    Mt.append(arr)
                for m in range(2, MM + 1):
                    for n in range(2, MM + 1):
                        edges = [(x % m, m + y % n) for x, y in zip(pa, pb)]
                        adj = {}
                        for t, (u, v) in enumerate(edges): adj.setdefault(u, []).append(t); adj.setdefault(v, []).append(t)
                        seen = set(); ok = True; sols = 1
                        for start in sorted(adj):
                            if start in seen: continue
                            comp, stack = [], [start]; seen.add(start)
                            while stack:
                                x = stack.pop(); comp.append(x)
                                for t in adj[x]:
                                    y = edges[t][1] if edges[t][0] == x else edges[t][0]
                                    if y not in seen: seen.add(y); stack.append(y)
                            ce = {t for x in comp for t in adj[x]}
                            if len(ce) <= len(comp) - 1: continue
                            val = {start: np.arange(26)}; alive = np.ones(26, bool); stack = [start]
                            while stack:
                                x = stack.pop()
                                for t in adj[x]:
                                    u, v = edges[t]
                                    if u in val and v in val:
                                        alive &= Mt[t][val[u]] == val[v]
                                    elif u in val:
                                        val[v] = Mt[t][val[u]]; stack.append(v)
                                    else:
                                        inv = np.full(26, 0, int); inv[Mt[t]] = np.arange(26); val[u] = inv[val[v]]; stack.append(u)
                            c = int(alive.sum()); sols *= c
                            if c == 0: ok = False; break
                        if ok: print(f"F {row} {md} {tn} {form} {m} {n} {sols}")
