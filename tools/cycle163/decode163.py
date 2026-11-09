"""Cycle 163: language check of every one-error S / Z survivor of split7e.c.  For each line (q, dir, ix, alphabet(s),
modes) try every dropped crib d (and none) and every boundary b at which both segments are strictly consistent without
d; derive the key letters fixed by the remaining cribs, decrypt ('?' where a residue has no crib in its segment) and
score mean log10 quadgram over fully determined quadgrams (all, and off-crib).  Best decryption per line is kept.
usage: decode163.py CT run-files... (label taken from the lines)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(np.int16)
INV = np.zeros_like(AL); INV[np.arange(len(AL))[:, None], AL] = np.arange(26)
Q = np.fromfile("/home/box/kryptos_support_backup/quad.bin", dtype=np.float32)
B = np.memmap("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16, mode='r').reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"; CRIBPOS = set(CI)
def score(t, skip=False):
    v = [Q[sum((ord(c) - 65) * 26 ** (3 - z) for z, c in enumerate(t[i:i + 4]))] for i in range(94)
         if '?' not in t[i:i + 4] and not (skip and any(j in CRIBPOS for j in range(i, i + 4)))]
    return (float(np.mean(v)) if v else -99.0), len(v)
def kv(a, m, c, p):
    return int((INV[a][c] - INV[a][p]) % 26) if m == 0 else int((INV[a][c] + INV[a][p]) % 26)
def decode(ct, q, d, ix, a1, m1, a2, m2):
    S = np.arange(97) if q < 0 else (np.argsort(B[q]) if d else np.array(B[q]))
    xs = [int(S[i]) if ix else i for i in CI]; cs = [ord(ct[S[i]]) - 65 for i in CI]; ps = [ord(c) - 65 for c in PT]
    best = None
    for drop in range(-1, 24):
        for b in sorted(set([0] + [x + 1 for x in xs])):
            keys = [{}, {}]; ok = True
            for t in range(24):
                if t == drop: continue
                seg = 0 if xs[t] < b else 1; a, m = (a1, m1) if seg == 0 else (a2, m2)
                v = kv(a, m, cs[t], ps[t]); r = xs[t] % 7
                if keys[seg].setdefault(r, v) != v: ok = False; break
            if not ok: continue
            out = []
            for i in range(97):
                x = int(S[i]) if ix else i; seg = 0 if x < b else 1; a, m = (a1, m1) if seg == 0 else (a2, m2)
                k = keys[seg].get(x % 7)
                if k is None: out.append('?'); continue
                y = INV[a][ord(ct[S[i]]) - 65]; out.append(chr(65 + AL[a][(y - k) % 26 if m == 0 else (k - y) % 26]))
            t_ = "".join(out); sa, na = score(t_); so, no = score(t_, True)
            if best is None or sa > best[0]: best = (sa, so, no, drop, b, t_)
    return best
if __name__ == "__main__":
    ct = sys.argv[1]; rows = []
    for fn in sys.argv[2:]:
        for line in open(fn):
            f = line.split()
            if f[0] == 'S': lab, q, d, ix, a, m1, m2 = f[1], *map(int, f[2:8]); a1 = a2 = a
            elif f[0] == 'Z': lab, q, d, ix, a1, m1, a2, m2 = f[1], *map(int, f[2:9])
            else: continue
            bst = decode(ct, q, d, ix, a1, m1, a2, m2)
            rows.append((bst[0], bst[1], bst[2], f[0], q, d, ix, a1, m1, a2, m2, bst[3], bst[4], bst[5]))
    rows.sort(key=lambda r: -r[0])
    print(f"{len(rows)} survivor lines; best all {rows[0][0]:.3f} off-crib {rows[0][1]:.3f}" if rows else "0 survivor lines")
    for r in rows:
        print(f"  {r[0]:.3f} off {r[1]:.3f} n{r[2]} {r[3]} q{r[4]} d{r[5]} ix{r[6]} a{r[7]}/{'VB'[r[8]]} a{r[9]}/{'VB'[r[10]]} drop{r[11]} b{r[12]} {r[13]}")
