"""Cycle 173: decrypt every anom173 HIT (p <= 21) with its crib-fixed key ('?' = class without a crib) and score English:
mean log10 quadgram over off-crib windows without '?' (as decode172.py). Asserts the cribs read back.
usage: decode173.py CT perms.bin n model quadgrams.json label hitfile"""
import sys, json, re, numpy as np
ct, pf, n, model, qf, lab, hf = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
T = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
J = json.load(open(qf)); Q = J["q"]; floor = J["floor"]
P = np.fromfile(pf, dtype=np.int16).reshape(-1, n)
def score(s):
    v = [Q.get(s[i:i + 4], floor) for i in range(len(s) - 3) if "?" not in s[i:i + 4] and not any(i + k in CRIB for k in range(4))]
    return sum(v) / len(v) if v else -99
rows = []
for l in open(hf):
    m = re.match(r"HIT t=(\d+) d=(\d+) PA=(\w+) CA=(\w+) mode=(\w+) idx=(\w+) p=(\d+) key=(\S+)", l)
    if not m: continue
    t, d, pa, ca, mo, ix, p, key = m.groups(); t, d, p = int(t), int(d), int(p); PA, CA = T[pa], T[ca]; perm = [int(x) for x in P[t]]
    if model == "del": C = ct[:d] + "?" + ct[d:]
    elif model == "ins": C = ct[:d] + ct[d + 1:]
    elif model == "swp": C = ct[:d] + ct[d + 1] + ct[d] + ct[d + 2:]
    else: C = ct
    out = []
    for j in range(n):
        u = perm[j]; c = C[u]; k = key[(u if ix == "ct" else j) % p]
        if c == "?" or k == "?": out.append("?"); continue
        kv = ord(k) - 65
        out.append(PA[(CA.index(c) - kv) % 26] if mo == "vig" else PA[(kv - CA.index(c)) % 26])
    s = "".join(out)
    bad = [j for j, c in CRIB.items() if s[j] != c and s[j] != "?" and not (model == "chg" and sorted(CRIB)[d] == j)]
    assert not bad, (l, s)
    rows.append((score(s), lab, model, t, d, pa, ca, mo, ix, p, key, s.count("?"), s))
rows.sort(reverse=True)
for r in rows: print("%.3f %s %s t=%d d=%d %s->%s %s %s p=%d key=%s unk=%d %s" % r)
