"""Cycle 192 decoder (one-error): for one config (route row, model, tableau pair, form, m, n) and every deletion d in {none, slot 0..23},
enumerate every key assignment consistent with the remaining 23 (or 24) crib bijections on the residues they touch (cyclic components
exhaustively; tree components left '?'), and print the decryption at every position whose two key residues are determined. Every
consistent deletion is printed (I-195). The deleted slot's own plaintext position is decrypted too (it shows what the carved letter gives).
usage: decode192.py CT perms.bin row model T1 T2 form m n [maxsol] [slots: all|comma list]"""
import sys, itertools
import numpy as np
ct, pf, row, md, T1, T2, form, m, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], int(sys.argv[8]), int(sys.argv[9])
maxsol = int(sys.argv[10]) if len(sys.argv) > 10 else 20
slots = [-1] + list(range(24)) if len(sys.argv) <= 11 or sys.argv[11] == "all" else [int(x) for x in sys.argv[11].split(",")]
S = [int(v) for v in np.fromfile(pf, dtype=np.int16).reshape(-1, 97)[row]]
CRIB = [(21 + i, ch) for i, ch in enumerate("EASTNORTHEAST")] + [(63 + i, ch) for i, ch in enumerate("BERLINCLOCK")]
def step(x, k, s): return (x + k) % 26 if s == "V" else (k - x) % 26
def ok(pch, c, a, b): return T2[step(T2.index(T1[step(T1.index(pch), a, form[0])]), b, form[1])] == c
def solve_all(edges):
    adj = {}
    for e in edges: adj.setdefault(e[0], []).append(e); adj.setdefault(e[1], []).append(e)
    comps, seen = [], set()
    for v in sorted(adj):
        if v in seen: continue
        st, comp = [v], []; seen.add(v)
        while st:
            x = st.pop(); comp.append(x)
            for e in adj[x]:
                y = e[1] if e[0] == x else e[0]
                if y not in seen: seen.add(y); st.append(y)
        comps.append(comp)
    out = []
    for comp in comps:
        ne = len({id(e) for x in comp for e in adj[x]})
        if ne <= len(comp) - 1: continue
        sols = []
        for rho in range(26):
            val = {comp[0]: rho}; st = [comp[0]]; good = True
            while st and good:
                x = st.pop()
                for (u, v, pch, c) in adj[x]:
                    if u in val and v in val:
                        if not ok(pch, c, val[u], val[v]): good = False; break
                    elif u in val:
                        val[v] = [b for b in range(26) if ok(pch, c, val[u], b)][0]; st.append(v)
                    else:
                        val[u] = [a for a in range(26) if ok(pch, c, a, val[v])][0]; st.append(u)
            if good: sols.append(val)
        if not sols: return None
        out.append(sols)
    return out
edges0 = []
for t, (i, pch) in enumerate(CRIB):
    pos = i if md == "P" else S[i]; edges0.append((pos % m, m + pos % n, pch, ct[S[i]], t))
for d in slots:
    edges = [e[:4] for e in edges0 if e[4] != d]
    sols = solve_all(edges)
    if sols is None: continue
    print(f"CONSISTENT deletion {d}: row {row} {md} {form} m {m} n {n}: solutions per cyclic component {[len(s) for s in sols]}")
    cnt = 0
    for combo in itertools.product(*sols):
        key = {}
        for dd in combo: key.update(dd)
        pt = []
        for i in range(97):
            pos = i if md == "P" else S[i]; u, v = pos % m, m + pos % n
            if u in key and v in key:
                z = ct[S[i]]; c0 = [p for p in T1 if ok(p, z, key[u], key[v])][0]
                pt.append(c0 if (21 <= i <= 33 or 63 <= i <= 73) else c0.lower())
            else: pt.append("?")
        akey = "".join(T1[key[u]] if u in key else "?" for u in range(m)); bkey = "".join(T2[key[m + v]] if m + v in key else "?" for v in range(n))
        print(f"  del {d} a={akey} b={bkey} PT={''.join(pt)}  known {97 - pt.count('?')}/97"); cnt += 1
        if cnt >= maxsol: break
