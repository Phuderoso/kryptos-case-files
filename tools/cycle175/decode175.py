"""Cycle 175: decode and English-score (mean log10 quadgram over off-crib windows without '?', as decode173.py)
 (a) every slip175 HIT line: rebuild C' (delx: '?' at d; insx: index d removed), decrypt with the crib-fixed key; asserts every
     crib except the dropped one reads back;  (b) every hill175 K line (the decode is in the line).
usage: decode175.py slip CT perms.bin n model quadgrams.json label hitfile
       decode175.py hill quadgrams.json label kfile"""
import sys, json, re, numpy as np
T = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CRIB = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
CK = sorted(CRIB)
def scorer(qf):
    J = json.load(open(qf)); Q = J["q"]; fl = J["floor"]
    def score(s):
        v = [Q.get(s[i:i + 4], fl) for i in range(len(s) - 3) if "?" not in s[i:i + 4] and not any(i + k in CRIB for k in range(4))]
        return (sum(v) / len(v), len(v)) if v else (-99, 0)
    return score
rows = []
if sys.argv[1] == "slip":
    ct, pf, n, model, qf, lab, hf = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
    score = scorer(qf); P = np.fromfile(pf, dtype=np.int16).reshape(-1, n)
    for l in open(hf):
        m = re.match(r"HIT t=(\d+) d=(\d+) drop=(\d+) PA=(\w+) CA=(\w+) mode=(\w+) idx=(\w+) p=(\d+) info=(\d) key=(\S+)", l)
        if not m: continue
        t, d, dr, pa, ca, mo, ix, p, info, key = m.groups(); t, d, dr, p = int(t), int(d), int(dr), int(p); PA, CA = T[pa], T[ca]
        perm = [int(x) for x in P[t]]; C = ct[:d] + "?" + ct[d:] if model == "delx" else ct[:d] + ct[d + 1:]
        out = []
        for j in range(n):
            u = perm[j]; c = C[u]; k = key[(u if ix == "ct" else j) % p]
            if c == "?" or k == "?": out.append("?"); continue
            kv = ord(k) - 65; out.append(PA[(CA.index(c) - kv) % 26] if mo == "vig" else PA[(kv - CA.index(c)) % 26])
        s = "".join(out)
        bad = [j for j, c in CRIB.items() if s[j] != c and s[j] != "?" and j != CK[dr]]
        assert not bad, (l, s)
        sc, nw = score(s); rows.append((sc, nw, lab, model, f"t={t} d={d} drop={dr} {pa}->{ca} {mo} {ix} p={p} info={info} key={key}", s))
else:
    qf, lab, kf = sys.argv[2], sys.argv[3], sys.argv[4]; score = scorer(qf)
    for l in open(kf):
        w = l.split()
        if w[0] != "K": continue
        sc, nw = score(w[10]); rows.append((sc, nw, lab, "hill", "q=%s n=%s aff=%s %s ix=%s off=%s ninv=%s checks=%s" % tuple(w[2:10]), w[10]))
rows.sort(key=lambda r: -r[0])
for r in rows: print("%.3f %d %s %s %s %s" % r)
