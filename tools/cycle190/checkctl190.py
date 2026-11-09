"""Check cycle 190 controls (pre-registered rule). Positive E1-E6 (one injected error at slot t): an M line at the planted perm, alphabet,
reduced form, model and (m, n) whose slot is t or any slot t' in series with t (t is a bridge of the residue graph minus t': removing
any member of a series class gives the same consistent system, and cmp190 prints the lowest), or slot -1 if t is a bridge of the full
graph (then the strict pass is blind to slot t). Series/bridge status computed here independently by connectivity (rule fixed after the
rehearsal showed E1 reported at slot 4, in series with 5, before any K4 run). S1 (no error): slot -1. Negatives D1, D2 (two errors),
N1 (three periods), N2 (random key): no M line at the planted perm with ex_after >= 5.
usage: checkctl190.py planted190.txt ctldir perms.bin"""
import sys
import numpy as np
P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); CI = list(range(21, 34)) + list(range(63, 74))
form = {"E1": "vig", "E2": "vig", "E3": "vig", "E4": "beau", "E5": "beau", "E6": "vig", "S1": "vig"}
def bridge(q, model, m, n, t, rem=None):
    S = list(range(97)) if q < 0 else [int(v) for v in P[q]]; pos = [i if model == "P" else S[i] for i in CI]
    E = [(p % m, m + p % n) for p in pos]; u0, v0 = E[t]; adj = {}
    for k, (u, v) in enumerate(E):
        if k != t and k != rem: adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    seen, st = {u0}, [u0]
    while st:
        x = st.pop()
        for y in adj.get(x, ()):
            if y not in seen: seen.add(y); st.append(y)
    return v0 not in seen
ok = tot = 0
for l in open(sys.argv[1]):
    name, q, alab, model, per, slots, ct = l.split(); q = int(q); ms = sorted(int(x) for x in per.split("/"))
    L = open(f"{sys.argv[2]}/{name}.txt").read().splitlines(); M = [x.split() for x in L if x.startswith("M")]
    ended = any(x.startswith("END") for x in L); qq = 0 if q < 0 else q; at = [x for x in M if int(x[2]) == qq]; tot += 1
    if name[0] in "ES":
        want = [-1] if slots == "-" else [int(slots)]
        if slots != "-":
            t0 = int(slots)
            if bridge(q, model, ms[0], ms[1], t0): want.append(-1)
            else: want += [r for r in range(24) if r != t0 and bridge(q, model, ms[0], ms[1], t0, r)]
        hit = [x for x in at if x[3] == alab and x[4] == form[name] and x[5] == model and int(x[6]) == ms[0] and int(x[7]) == ms[1] and int(x[8]) in want]
        good = ended and len(hit) > 0; ok += good
        print(name, "PASS" if good else "FAIL", "want slot", want, "hit", hit[:1], "fits at q (ex>=2)", len(at), "window", len(M))
    else:
        bad = [x for x in at if int(x[9]) >= 5]; good = ended and not bad; ok += good
        print(name, "PASS" if good else "FAIL", "fits at q with ex_after>=5", len(bad), "fits at q (ex>=2)", len(at), "window", len(M), bad[:2])
print(f"controls {ok}/{tot}")
