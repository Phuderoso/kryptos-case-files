"""Cycle 162 independent recount (no scans, no prefilter): for a configuration (text, perm q, dir, ix) test every
alphabet, both modes per segment and every distinct boundary b straight from the definition (each segment: all cribs
in one residue class mod 7 imply one key value).  Prints S count (alphabet, m1, m2 with some b), Z count (AZ/KA cross),
X flag (alphabet free per segment).  usage: recount162.py LABEL CT q dir ix [drop]  (q = -1: identity)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(np.int16)
INV = np.zeros_like(AL); INV[np.arange(len(AL))[:, None], AL] = np.arange(26)
B = np.fromfile("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16).reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def run(lab, ct, q, d, ix, drop=-1):
    s = list(range(97)) if q < 0 else (list(B[q]) if d == 0 else list(np.argsort(B[q])))
    cr = [(s[CI[t]] if ix else CI[t], ord(ct[s[CI[t]]]) - 65, ord(PT[t]) - 65) for t in range(24) if t != drop]
    xs = np.array([c[0] for c in cr]); ic = INV[:, [c[1] for c in cr]]; ip = INV[:, [c[2] for c in cr]]
    val = [(ic - ip) % 26, (ic + ip) % 26]          # Vig, Beau key values, shape (NA, n)
    res = xs % 7
    def ok(mask, m):                                 # consistency of the cribs selected by mask, all alphabets
        g = np.ones(len(AL), bool)
        for r in range(7):
            idx = np.where(mask & (res == r))[0]
            if len(idx) > 1: g &= (val[m][:, idx] == val[m][:, idx[:1]]).all(1)
        return g
    bs = sorted(set([0] + [int(x) + 1 for x in xs]))
    S = np.zeros((len(AL), 2, 2), bool); Z = set(); X = False
    for b in bs:
        o1 = [ok(xs < b, m) for m in range(2)]; o2 = [ok(xs >= b, m) for m in range(2)]
        for m1 in range(2):
            for m2 in range(2):
                S[:, m1, m2] |= o1[m1] & o2[m2]
                for a1, a2 in ((0, 1), (1, 0)):
                    if o1[m1][a1] and o2[m2][a2]: Z.add((a1, m1, a2, m2))
        if (o1[0] | o1[1]).any() and (o2[0] | o2[1]).any(): X = True
    print(f"R {lab} {q} {d} {ix} drop={drop} S={int(S.sum())} Z={len(Z)} X={int(X)}")
if __name__ == "__main__":
    a = sys.argv; run(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]) if len(a) > 6 else -1)
