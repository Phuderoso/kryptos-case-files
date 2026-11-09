"""Cycle 190 independent decoder for one-error fits (breadth-first propagation; shares no code with cmp190.c).
Same as decode189.py but the crib slot `slot` (0-23; -1 = none) is left out of the equations. Decodes every plaintext position whose
residues mod m and mod n lie in one component; prints the letter the key implies at the deleted crib slot (the 'corrected' crib).
Inside a series class every deleted slot gives a consistent system but a different decode, so slot 'all' prints every consistent deletion.
usage: decode190.py CT perms.bin q alphabet form model m n slot|all   (q = -1: identity)"""
import sys
import numpy as np
ct, pf, q, T, form, model, m, n, slot = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], int(sys.argv[7]), int(sys.argv[8]), sys.argv[9]
S = list(range(97)) if q < 0 else [int(v) for v in np.fromfile(pf, dtype=np.int16).reshape(-1, 97)[q]]
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def run(slot, only_ok):
    adj = {}
    for t, i in enumerate(CI):
        if t == slot: continue
        pos = i if model == "P" else S[i]; xp, xc = T.index(PT[t]), T.index(ct[S[i]])
        K = (xc - xp) % 26 if form == "vig" else (xc + xp) % 26
        u, v = ("a", pos % m), ("b", pos % n); adj.setdefault(u, []).append((v, K)); adj.setdefault(v, []).append((u, K))
    val, comp, ok = {}, {}, True
    for s0 in adj:
        if s0 in val: continue
        val[s0] = 0; comp[s0] = s0; st = [s0]
        while st:
            x = st.pop()
            for y, K in adj[x]:
                want = (val[x] - K) % 26 if x[0] == "a" else (val[x] + K) % 26
                if y not in val: val[y] = want; comp[y] = s0; st.append(y)
                elif val[y] != want: ok = False
    out = []
    for i in range(97):
        pos = i if model == "P" else S[i]; u, v = ("a", pos % m), ("b", pos % n)
        if u in val and v in val and comp[u] == comp[v]:
            K = (val[u] - val[v]) % 26; xc = T.index(ct[S[i]]); out.append(T[(xc - K) % 26] if form == "vig" else T[(K - xc) % 26])
        else: out.append("?")
    pt = "".join(out); agree = sum(pt[i] == PT[t] for t, i in enumerate(CI))
    fix = "" if slot < 0 else f" slot {slot} (pt {CI[slot]}, crib '{PT[slot]}') decodes to '{pt[CI[slot]]}'"
    if ok or not only_ok: print("consistent" if ok else "INCONSISTENT", "cribs", agree, "/24 decoded", 97 - pt.count("?"), pt + fix)
for sl in (range(-1, 24) if slot == "all" else [int(slot)]): run(sl, slot == "all")
