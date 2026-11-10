"""Cycle 198 independent recount (no cores, no union-find, no dedup): a config fits iff its usable crib constraints are consistent with
all slots, or with some single slot t removed, checked directly by BFS (lib197.solve_bij; solver A with the additive shift freedom, one
root). Records qlo..qhi of the direct record file; pairs from a file ('P m n'). Prints per-cell fit counts: R solver alph|tab form m n fits.
usage: recount198.py CT recs.txt qlo qhi pairsA pairsB"""
import sys
from lib198 import *
ct, recf, qlo, qhi, pa, pb = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
recs = [list(map(int, l.split())) for l in open(recf)][qlo:qhi]
def pairs(fn): return [(int(w[1]), int(w[2])) for w in (l.split() for l in open(fn)) if w and w[0] == "P"]
PA, PB = pairs(pa), pairs(pb)
def consA(cons, m, n):
    # cons: list of (u, v, K): a[u] + b[v] = K; BFS with one free root per component
    adj = {}
    for (u, v, K) in cons: adj.setdefault(("a", u), []).append((("b", v), K)); adj.setdefault(("b", v), []).append((("a", u), K))
    val = {}
    for s in adj:
        if s in val: continue
        val[s] = 0; st = [s]
        while st:
            x = st.pop()
            for (y, K) in adj[x]:
                w = (K - val[x]) % 26
                if y in val:
                    if val[y] != w: return False
                else: val[y] = w; st.append(y)
    return True
res = {}
for w in recs:
    kp, cv = w[2:26], w[26:50]; use = [t for t in range(24) if cv[t] >= 0]
    for ab, alph in (("AZ", AZ), ("KA", KA)):
        for form in ("vig", "beau"):
            K = {t: keyval_add(form, alph, PTC[t], ct[cv[t]]) for t in use}
            for (m, n) in PA:
                cons = [(kp[t] % m, kp[t] % n, K[t]) for t in use]
                ok = consA(cons, m, n) or any(consA(cons[:i] + cons[i + 1:], m, n) for i in range(len(cons)))
                key = ("A", ab, form, m, n); res[key] = res.get(key, 0) + ok
    for tab in ("AZ>KA", "KA>AZ"):
        for form in ("VV", "VB", "BV", "BB"):
            fw = {}; bw = {}
            for t in use:
                f = [None] * 26; g = [None] * 26
                for a in range(26):
                    for b in range(26):
                        if enc_two(tab, form, PTC[t], a, b) == ct[cv[t]]: f[a] = b; g[b] = a
                fw[t] = f; bw[t] = g
            for (m, n) in PB:
                def ok_with(sl):
                    E = [(kp[t] % m, kp[t] % n, t) for t in sl]
                    return solve_bij(E, m, n, lambda t, a: fw[t][a], lambda t, b: bw[t][b])[0]
                ok = ok_with(use) or any(ok_with(use[:i] + use[i + 1:]) for i in range(len(use)))
                key = ("B", tab, form, m, n); res[key] = res.get(key, 0) + ok
for k in sorted(res): print("R", *k, res[k])
