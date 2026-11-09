"""Cycle 189 independent decoder (breadth-first propagation; shares no code with cmp189.c). Given CT, perm row, alphabet, form,
model, m, n: solve a[u] - b'[v] = K on the crib graph (component roots set to 0), then decode every plaintext position whose
residues mod m and mod n lie in one component; other positions print '?'. Reports crib agreement and the count of decoded letters.
usage: decode189.py CT perms.bin q alphabet form model m n   (q = -1: identity)"""
import sys
import numpy as np
ct, pf, q, T, form, model, m, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], int(sys.argv[7]), int(sys.argv[8])
S = list(range(97)) if q < 0 else [int(v) for v in np.fromfile(pf, dtype=np.int16).reshape(-1, 97)[q]]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
adj = {}
for t, i in enumerate(CI):
    pos = i if model == "P" else S[i]; xp, xc = T.index(PT[t]), T.index(ct[S[i]])
    K = (xc - xp) % 26 if form == "vig" else (xc + xp) % 26
    u, v = ("a", pos % m), ("b", pos % n); adj.setdefault(u, []).append((v, K)); adj.setdefault(v, []).append((u, K))
val, comp, ok = {}, {}, True
for s in adj:
    if s in val: continue
    val[s] = 0; comp[s] = s; st = [s]
    while st:
        x = st.pop()
        for y, K in adj[x]:
            want = (val[x] - K) % 26 if x[0] == "a" else (val[x] + K) % 26     # a - b' = K
            if y not in val: val[y] = want; comp[y] = s; st.append(y)
            elif val[y] != want: ok = False
out = []
for i in range(97):
    pos = i if model == "P" else S[i]; u, v = ("a", pos % m), ("b", pos % n)
    if u in val and v in val and comp[u] == comp[v]:
        K = (val[u] - val[v]) % 26; xc = T.index(ct[S[i]]); out.append(T[(xc - K) % 26] if form == "vig" else T[(K - xc) % 26])
    else: out.append("?")
pt = "".join(out); agree = sum(pt[i] == PT[t] for t, i in enumerate(CI))
print("consistent" if ok else "INCONSISTENT", "cribs", agree, "/24 decoded", 97 - pt.count("?"), pt)
