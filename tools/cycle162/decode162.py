"""Cycle 162: language check of every model-X configuration (alphabet free per segment).  For each X line and every
boundary b allowed, list the (alphabet, mode) choices consistent on segment 1 and on segment 2, decrypt with the key
letters fixed by the cribs ('?' where a residue has no crib in its segment), and score mean log10 quadgram over fully
determined quadgrams (all, and with crib positions excluded).  Up to CAP combinations per configuration (best kept).
usage: decode162.py CT Xlines-file label"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(np.int16)
INV = np.zeros_like(AL); INV[np.arange(len(AL))[:, None], AL] = np.arange(26)
Q = np.fromfile("/home/box/kryptos_support_backup/quad.bin", dtype=np.float32)
B = np.memmap("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16, mode='r').reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"; CAP = 400
CRIBPOS = set(CI)
def score(t, skip=False):
    v = [Q[sum((ord(c) - 65) * 26 ** (3 - z) for z, c in enumerate(t[i:i + 4]))] for i in range(94)
         if '?' not in t[i:i + 4] and not (skip and any(j in CRIBPOS for j in range(i, i + 4)))]
    return (float(np.mean(v)) if v else -99.0), len(v)
def consistent(xs, ic, ip, mask):
    out = []
    for m in range(2):
        val = (ic - ip) % 26 if m == 0 else (ic + ip) % 26
        g = np.ones(len(AL), bool); res = xs % 7
        for r in range(7):
            idx = np.where(mask & (res == r))[0]
            if len(idx) > 1: g &= (val[:, idx] == val[:, idx[:1]]).all(1)
        out += [(int(a), m) for a in np.where(g)[0]]
    return out
def run(ct, fn, lab):
    rows = []
    for line in open(fn):
        f = line.split()
        if f[0] != 'X': continue
        q, d, ix, hi, lo = int(f[2]), int(f[3]), int(f[4]), int(f[5]), int(f[6])
        S = np.arange(97) if q < 0 else (np.argsort(B[q]) if d else np.array(B[q]))
        xs = np.array([S[i] if ix else i for i in CI]); ic = INV[:, [ord(ct[S[i]]) - 65 for i in CI]]; ip = INV[:, [ord(c) - 65 for c in PT]]
        bs = sorted(set([lo] + [int(x) + 1 for x in xs if lo <= x + 1 <= hi]))
        best = None; ncomb = 0
        for b in bs:
            c1 = consistent(xs, ic, ip, xs < b); c2 = consistent(xs, ic, ip, xs >= b)
            for (a1, m1) in c1[:CAP]:
                for (a2, m2) in c2[:max(1, CAP // max(1, len(c1)))]:
                    ncomb += 1; out = []
                    keys = [{}, {}]
                    for t, i in enumerate(CI):
                        seg = 0 if xs[t] < b else 1; a, m = (a1, m1) if seg == 0 else (a2, m2)
                        v = (INV[a][ord(ct[S[i]]) - 65] - INV[a][ord(PT[t]) - 65]) % 26 if m == 0 else (INV[a][ord(ct[S[i]]) - 65] + INV[a][ord(PT[t]) - 65]) % 26
                        keys[seg][int(xs[t]) % 7] = v
                    for i in range(97):
                        x = S[i] if ix else i; seg = 0 if x < b else 1; a, m = (a1, m1) if seg == 0 else (a2, m2)
                        k = keys[seg].get(int(x) % 7)
                        if k is None: out.append('?'); continue
                        y = INV[a][ord(ct[S[i]]) - 65]; out.append(chr(65 + AL[a][(y - k) % 26 if m == 0 else (k - y) % 26]))
                    t = "".join(out); sa, na = score(t); so, no = score(t, True)
                    if best is None or sa > best[0]: best = (sa, so, no, q, d, ix, b, a1, m1, a2, m2, t)
        rows.append(best + (ncomb,))
    rows.sort(key=lambda r: -r[0])
    print(f"{lab}: {len(rows)} X configs; best all {rows[0][0]:.3f} off-crib {rows[0][1]:.3f} (n {rows[0][2]})" if rows else f"{lab}: 0")
    for r in rows[:5]:
        print(f"  {r[0]:.3f} off {r[1]:.3f} n{r[2]} q{r[3]} d{r[4]} ix{r[5]} b{r[6]} a{r[7]}/{'VB'[r[8]]} a{r[9]}/{'VB'[r[10]]} combos{r[12]} {r[11]}")
if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
