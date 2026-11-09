"""Cycle 163 independent one-error recount (no scans, no drop-aware shortcut): for a configuration (text, perm q, dir, ix),
for every dropped crib d (and none) and every boundary b, test every alphabet and both modes per segment straight from
the definition (each segment: all remaining cribs in one residue class mod 7 imply one key value); union over d and b.
Prints S1e count (alphabet, m1, m2), Z1e count (AZ/KA cross tuples), X1e flag.  Uses recount162-style numpy code but no
code from split7e.c.  usage: recount163.py LABEL CT q dir ix   (q = -1: identity)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(np.int16)
INV = np.zeros_like(AL); INV[np.arange(len(AL))[:, None], AL] = np.arange(26)
B = np.memmap("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16, mode='r').reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def run(lab, ct, q, d, ix):
    s = list(range(97)) if q < 0 else (list(B[q]) if d == 0 else list(np.argsort(B[q])))
    cr = [(s[CI[t]] if ix else CI[t], ord(ct[s[CI[t]]]) - 65, ord(PT[t]) - 65) for t in range(24)]
    xs = np.array([c[0] for c in cr]); ic = INV[:, [c[1] for c in cr]]; ip = INV[:, [c[2] for c in cr]]
    val = [(ic - ip) % 26, (ic + ip) % 26]; res = xs % 7
    def ok(mask, m):
        g = np.ones(len(AL), bool)
        for r in range(7):
            idx = np.where(mask & (res == r))[0]
            if len(idx) > 1: g &= (val[m][:, idx] == val[m][:, idx[:1]]).all(1)
        return g
    bs = sorted(set([0] + [int(x) + 1 for x in xs]))
    S = np.zeros((len(AL), 2, 2), bool); Z = set(); X = False; drops = set()
    for drop in range(-1, 24):
        keep = np.arange(24) != drop
        for b in bs:
            o1 = [ok(keep & (xs < b), m) for m in range(2)]; o2 = [ok(keep & (xs >= b), m) for m in range(2)]
            for m1 in range(2):
                for m2 in range(2):
                    h = o1[m1] & o2[m2]
                    if h.any(): drops.add(drop)
                    S[:, m1, m2] |= h
                    for a1, a2 in ((0, 1), (1, 0)):
                        if o1[m1][a1] and o2[m2][a2]: Z.add((a1, m1, a2, m2))
            if (o1[0] | o1[1]).any() and (o2[0] | o2[1]).any(): X = True
    print(f"R {lab} {q} {d} {ix} S1e={int(S.sum())} Z1e={len(Z)} X1e={int(X)} alphas={sorted(set(np.where(S.any((1,2)))[0].tolist()))[:6]} drops_with_S={sorted(drops)[:8]}")
if __name__ == "__main__":
    a = sys.argv; run(a[1], a[2], int(a[3]), int(a[4]), int(a[5]))
