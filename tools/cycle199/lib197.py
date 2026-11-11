"""Cycle 197 shared Python reference (independent of cmp197.c): records, two-layer encryption/decryption, consistency check, decoding."""
import struct, itertools
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
PTC = "EASTNORTHEASTBERLINCLOCK"; CI = list(range(21, 34)) + list(range(63, 74))
K4 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
TABS = {"AZ>KA": (AZ, KA), "KA>AZ": (KA, AZ), "AZ>AZ": (AZ, AZ), "KA>KA": (KA, KA)}
def load_perm(fn, N, q):
    with open(fn, "rb") as f:
        f.seek(q * N * 2); return list(struct.unpack(f"<{N}h", f.read(N * 2)))
def carved_of(cidx, kind, d):
    """carved index of C' index cidx, or -1 if dropped."""
    if kind == "del": return cidx if cidx < d else (-1 if cidx == d else cidx - 1)
    if kind == "ins": return cidx if cidx < d else cidx + 1
    return cidx
def perm_record(out, kind, d):
    c = [out[i] for i in CI]
    return [CI[:], c, [carved_of(x, kind, d) for x in c]]
def keyval_add(form, alph, p, c):
    x, z = alph.index(p), alph.index(c)
    return (z - x) % 26 if form == "vig" else (z + x) % 26
def enc_add(form, alph, p, K):
    x = alph.index(p); return alph[(x + K) % 26] if form == "vig" else alph[(K - x) % 26]
def dec_add(form, alph, c, K):
    z = alph.index(c); return alph[(z - K) % 26] if form == "vig" else alph[(K - z) % 26]
def enc_two(tab, form, p, a, b):
    T1, T2 = TABS[tab]; s1 = -1 if form[0] == "B" else 1; s2 = -1 if form[1] == "B" else 1
    y = (s1 * T1.index(p) + a) % 26; z = (s2 * T2.index(T1[y]) + b) % 26; return T2[z]
def dec_two(tab, form, c, a, b):
    T1, T2 = TABS[tab]; s1 = -1 if form[0] == "B" else 1; s2 = -1 if form[1] == "B" else 1
    w = (s2 * (T2.index(c) - b)) % 26; y = T1.index(T2[w]); return T1[(s1 * (y - a)) % 26]
def components(edges, m, n):
    adj = {}
    for (u, v, t) in edges:
        adj.setdefault(("a", u), []).append((("b", v), t)); adj.setdefault(("b", v), []).append((("a", u), t))
    seen, comps = set(), []
    for s in adj:
        if s in seen: continue
        comp, st = [], [s]; seen.add(s)
        while st:
            x = st.pop(); comp.append(x)
            for (y, t) in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        comps.append(comp)
    return adj, comps
def solve_bij(edges, m, n, fwd, bwd):
    """fwd(t, aval) -> bval, bwd(t, bval) -> aval. Returns (ok, list of per-component solution lists)."""
    adj, comps = components(edges, m, n); out = []
    for comp in comps:
        sols = []
        root = comp[0]
        for rv in range(26):
            val = {root: rv}; st = [root]; good = True
            while st and good:
                x = st.pop()
                for (y, t) in adj[x]:
                    w = fwd(t, val[x]) if x[0] == "a" else bwd(t, val[x])
                    if y in val:
                        if val[y] != w: good = False; break
                    else: val[y] = w; st.append(y)
            if good: sols.append(val)
        if not sols: return False, []
        out.append(sols)
    return True, out
def rec_from_file(fn, q):
    for line in open(fn):
        w = list(map(int, line.split()))
        if w[0] == q: return [w[2:26], w[2:26], w[26:50]]
    raise KeyError(q)
def kind_from_map(fn, q):
    for line in open(fn):
        i, tags = line.split(" ", 1)
        if int(i) == q: t = tags.strip().split(";")[0].split(); return t[1], int(t[2]), [x for x in tags.strip().split(";")]
    raise KeyError(q)
def decode(ct, out, N, kind, d, rec, model, solver, ab, form, m, n, maxsol=8):
    """Returns list of (N-letter plaintext with '?') for every consistent key combination (capped), [] if inconsistent."""
    kp, kc, cv = rec; pos = kp if model in "PD" else kc
    edges = [(pos[t] % m, pos[t] % n, t) for t in range(24) if cv[t] >= 0]
    if solver == "A":
        alph = AZ if ab == "AZ" else KA if ab == "KA" else ab
        K = {t: keyval_add(form, alph, PTC[t], ct[cv[t]]) for t in range(24) if cv[t] >= 0}
        fwd = lambda t, x: (K[t] - x) % 26; bwd = fwd
    else:
        def fwd(t, a):
            for b in range(26):
                if enc_two(ab, form, PTC[t], a, b) == ct[cv[t]]: return b
        def bwd(t, b):
            for a in range(26):
                if enc_two(ab, form, PTC[t], a, b) == ct[cv[t]]: return a
    ok, comps = solve_bij(edges, m, n, fwd, bwd)
    if not ok: return []
    adj, cl = components(edges, m, n)
    cid = {x: i for i, c in enumerate(cl) for x in c}
    cyc = [len({t for x in c for (_, t) in adj[x]}) > len(c) - 1 for c in cl]
    if solver == "A": combos = [[s[0]] for s in comps]; combos = [tuple(s[0] for s in comps)]
    else:
        lists = [s if cyc[i] else [s[0]] for i, s in enumerate(comps)]
        combos = list(itertools.islice(itertools.product(*lists), maxsol))
    res = []
    for combo in combos:
        val = {}
        for c in combo: val.update(c)
        pt = []
        for k in range(N):
            c = out[k]; j = carved_of(c, kind, d); i = k if model in "PD" else c
            u, v = ("a", i % m), ("b", i % n)
            if j < 0 or u not in cid or v not in cid: pt.append("?"); continue
            if solver == "A":
                if cid[u] != cid[v]: pt.append("?"); continue
                pt.append(dec_add(form, alph, ct[j], (val[u] + val[v]) % 26))
            else:
                if not (cyc[cid[u]] and cyc[cid[v]]): pt.append("?"); continue
                pt.append(dec_two(ab, form, ct[j], val[u], val[v]))
        res.append("".join(pt))
    return res
