"""Cycle 192 independent recount (shares no code with cmp192.c; written from recount191.py's literal tables). For every config (route row,
model, tableau pair, form, ordered pair m != n from the pairs file) it builds LITERALLY from letters the 26-entry tables
M_t[a] = the b with two-pass encryption of crib letter p_t under key values (a, b) == carved letter c_t, and declares a ONE-ERROR fit iff
for some d in {none, 0..23} the graph without slot d has, on every connected component with a cycle, at least one consistent value of the
component's first vertex (depth-first propagation vectorised over the 26 values; no 2-core reduction, no deduplication, no shortcut).
Output: F row model tab form m n   (one line per fitting config)
usage: recount192.py CT perms.bin rows(comma) tabpairs.txt pairs.txt"""
import sys
import numpy as np
ct, pf, rows, tf, pfile = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")], sys.argv[4], sys.argv[5]
PERM = np.fromfile(pf, dtype=np.int16).reshape(-1, 97)
CRIB = [(21 + i, ch) for i, ch in enumerate("EASTNORTHEAST")] + [(63 + i, ch) for i, ch in enumerate("BERLINCLOCK")]
TABS = [l.split() for l in open(tf) if len(l.split()) == 3]
PAIRS = [(l.split()[0], int(l.split()[1]), int(l.split()[2])) for l in open(pfile) if len(l.split()) == 3]
def step(x, k, s): return (x + k) % 26 if s == "V" else (k - x) % 26
def consistent(edges, Mt, skip):
    adj = {}
    for t, (u, v) in enumerate(edges):
        if t == skip: continue
        adj.setdefault(u, []).append(t); adj.setdefault(v, []).append(t)
    seen = set()
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
        val = {start: np.arange(26)}; alive = np.ones(26, bool); stack = [start]; done = set()
        while stack:
            x = stack.pop()
            for t in adj[x]:
                if t in done: continue
                done.add(t); u, v = edges[t]
                if u in val and v in val: alive &= Mt[t][val[u]] == val[v]
                elif u in val: val[v] = Mt[t][val[u]]; stack.append(v)
                else:
                    inv = np.zeros(26, int); inv[Mt[t]] = np.arange(26); val[u] = inv[val[v]]; stack.append(u)
        if not alive.any(): return False
    return True
for row in rows:
    S = [int(v) for v in PERM[row]]
    for T1, T2, tn in TABS:
        for form in ("VV", "VB", "BV", "BB"):
            Mt = []
            for (i, pch) in CRIB:
                c = ct[S[i]]; arr = np.full(26, -1, int)
                for a in range(26):
                    mid = T1[step(T1.index(pch), a, form[0])]
                    for b in range(26):
                        if T2[step(T2.index(mid), b, form[1])] == c: arr[a] = b
                Mt.append(arr)
            for md, m, n in PAIRS:
                pos = [i if md == "P" else S[i] for i, _ in CRIB]
                edges = [(p % m, m + p % n) for p in pos]
                if any(consistent(edges, Mt, d) for d in [-1] + list(range(24))): print(f"F {row} {md} {tn} {form} {m} {n}")
