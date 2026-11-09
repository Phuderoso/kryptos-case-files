"""Cycle 191 decoder: for one config (route row, model, tableau pair, form, m, n) enumerate every key assignment consistent with the
24 cribs on the residues the cribs touch (cyclic components exhaustively; tree components by one free value each, printed as all 26 if
asked, else left '?'), and print the decryption of all 97 letters at positions whose two key residues are both determined.
usage: decode191.py CT perms.bin row model T1 T2 form m n [maxsol]"""
import sys, itertools
import numpy as np
ct, pf, row, md, T1, T2, form, m, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], int(sys.argv[8]), int(sys.argv[9])
maxsol = int(sys.argv[10]) if len(sys.argv) > 10 else 20
S = [int(v) for v in np.fromfile(pf, dtype=np.int16).reshape(-1, 97)[row]]
CRIB = [(21 + i, ch) for i, ch in enumerate("EASTNORTHEAST")] + [(63 + i, ch) for i, ch in enumerate("BERLINCLOCK")]
def step(x, k, s): return (x + k) % 26 if s == "V" else (k - x) % 26
def ok(pch, c, a, b): return T2[step(T2.index(T1[step(T1.index(pch), a, form[0])]), b, form[1])] == c
edges = []
for i, pch in CRIB:
    pos = i if md == "P" else S[i]; edges.append((pos % m, m + pos % n, pch, ct[S[i]]))
verts = sorted({e[0] for e in edges} | {e[1] for e in edges})
# brute-force-by-propagation over all assignments of the touched vertices: enumerate component roots
adj = {}
for e in edges: adj.setdefault(e[0], []).append(e); adj.setdefault(e[1], []).append(e)
comps, seen = [], set()
for v in verts:
    if v in seen: continue
    st, comp = [v], []; seen.add(v)
    while st:
        x = st.pop(); comp.append(x)
        for e in adj[x]:
            y = e[1] if e[0] == x else e[0]
            if y not in seen: seen.add(y); st.append(y)
    comps.append(comp)
def solve(comp):
    out = []
    for rho in range(26):
        val = {comp[0]: rho}; st = [comp[0]]; good = True
        while st and good:
            x = st.pop()
            for (u, v, pch, c) in adj[x]:
                if u in val and v in val:
                    if not ok(pch, c, val[u], val[v]): good = False; break
                elif u in val:
                    bs = [b for b in range(26) if ok(pch, c, val[u], b)]; val[v] = bs[0]; st.append(v)
                else:
                    as_ = [a for a in range(26) if ok(pch, c, a, val[v])]; val[u] = as_[0]; st.append(u)
        if good: out.append(val)
    return out
cyc = [c for c in comps if len({id(e) for x in c for e in adj[x]}) > len(c) - 1]
tree = [c for c in comps if c not in cyc]
sols = [solve(c) for c in cyc]
print(f"config row {row} {md} {form} m {m} n {n}: components {len(comps)} cyclic {len(cyc)} (solutions per cyclic component {[len(s) for s in sols]}); tree components {len(tree)} left free")
cnt = 0
for combo in itertools.product(*sols):
    key = {}
    for d in combo: key.update(d)
    pt = []
    for i in range(97):
        pos = i if md == "P" else S[i]; u, v = pos % m, m + pos % n
        if u in key and v in key:
            a, b = key[u], key[v]; z = ct[S[i]]
            cand = [p for p in T1 if ok(p, z, a, b)]; pt.append(cand[0].lower() if not (21 <= i <= 33 or 63 <= i <= 73) else cand[0])
        else: pt.append("?")
    akey = "".join(T1[key[u]] if u in key else "?" for u in range(m)); bkey = "".join(T2[key[m + v]] if m + v in key else "?" for v in range(n))
    print(f"a={akey} b={bkey} PT={''.join(pt)}  known {97 - pt.count('?')}/97"); cnt += 1
    if cnt >= maxsol: break
