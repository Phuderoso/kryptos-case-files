"""Cycle 171 independent recount of porta171 stage 1 + periodic one-error counts (numpy/python, no code shared with porta171.c).
usage: recount171.py CT perms.bin alpha.bin STRIDE OFFSET  -> prints SUMMARY-like counts and PERIODIC rows to compare."""
import sys, numpy as np
from collections import Counter
CT, pf, af, stride, off = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
P = np.fromfile(pf, dtype=np.int16).reshape(-1, 97); A = np.fromfile(af, dtype=np.uint8).reshape(-1, 26)
CP = list(range(21, 34)) + list(range(63, 74)); CL = [ord(c) - 65 for c in "EASTNORTHEAST" + "BERLINCLOCK"]
ords = set()
for a in A:
    ords.add(bytes(a)); ords.add(bytes(np.concatenate([a[0::2], a[1::2]])))
ords = np.frombuffer(b"".join(sorted(ords)), dtype=np.uint8).reshape(-1, 26)
H = np.zeros((len(ords), 26), dtype=bool)                       # H[o, letter] = letter in first half
H[np.arange(len(ords))[:, None], ords[:, :13]] = True
POS = np.argsort(ords, axis=1)                                   # POS[o, letter] = index of letter in ordering
tot = Counter(); per = {(v, m): np.zeros(27, dtype=np.int64) for v in (1, 2) for m in 'AB'}
for p in range(off, len(P), stride):
    pm = P[p]; a = np.array(CL); b = np.array([ord(CT[pm[c]]) - 65 for c in CP]); tot['perms'] += 1
    if (a == b).sum() >= 2: tot['dead_2self'] += 1; continue
    noncross = (H[:, a] == H[:, b])                              # (nord, 24)
    nb = noncross.sum(1); surv = np.nonzero(nb <= 1)[0]
    for o in surv:
        d = int(np.argmax(noncross[o])) if nb[o] == 1 else -1
        tot['surv_ord_forced' if d >= 0 else 'surv_ord_free'] += 1
        ps = POS[o]
        for v in (1, 2):
            kv = []
            for i in range(24):
                if i == d: kv.append(None); continue
                ip, ic = ps[a[i]], ps[b[i]]; h1, h2 = (ip, ic - 13) if ip < 13 else (ic, ip - 13)
                kv.append((h2 - h1) % 13 if v == 1 else (h2 + h1) % 13)
            for m in 'AB':
                ix = [CP[i] if m == 'A' else int(pm[CP[i]]) for i in range(24)]
                for L in range(1, 27):
                    cls = {}
                    for i in range(24):
                        if kv[i] is not None: cls.setdefault(ix[i] % L, []).append(kv[i])
                    miss = sum(len(x) - Counter(x).most_common(1)[0][1] for x in cls.values())
                    if miss <= (0 if d >= 0 else 1): per[(v, m)][L] += 1
print("RECOUNT", ' '.join(f"{k} {tot[k]}" for k in ['perms', 'dead_2self', 'surv_ord_free', 'surv_ord_forced']))
for v in (1, 2):
    for m in 'AB': print(f"PERIODIC V{v}{m}", ' '.join(str(x) for x in per[(v, m)][1:]))
