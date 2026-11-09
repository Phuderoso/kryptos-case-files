"""Cycle 166 independent recount (no greedy, no prefix/suffix scans): for one configuration (text, perm q, dir, ix,
optional dropped crib) test every alphabet, every boundary pair 0 <= b1 <= b2 <= 97 and every form per segment straight
from the definition (in each key's segment set, all cribs of one residue mod 7 imply one key value).
T: three independent keys (any fit, incl. degenerate two-segment ones).  R: key 1 on [0,b1) and [b2,97) (one table).
Prints sets compared with split3's T alphabets (any T line) and R (alphabet, m1, m2) triples.
usage: recount166.py LABEL CT q dir ix amax [drop]   (q = -1: identity)"""
import sys, numpy as np
AL = np.fromfile("/home/box/kryptos_support_backup/alpha.bin", dtype=np.uint8).reshape(-1, 26).astype(np.int16)
INV = np.zeros_like(AL); INV[np.arange(len(AL))[:, None], AL] = np.arange(26)
B = np.memmap("/home/box/kryptos_support_backup/perms97.bin", dtype=np.int16, mode='r').reshape(-1, 97)
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
def run(lab, ct, q, d, ix, amax, drop=-1):
    s = list(range(97)) if q < 0 else ([int(x) for x in B[q]] if d == 0 else [int(x) for x in np.argsort(B[q])])
    cr = [(s[CI[t]] if ix else CI[t], ord(ct[s[CI[t]]]) - 65, ord(PT[t]) - 65) for t in range(24) if t != drop]
    xs = np.array([c[0] for c in cr]); inv = INV[:amax]
    ic = inv[:, [c[1] for c in cr]]; ip = inv[:, [c[2] for c in cr]]
    val = [(ic - ip) % 26, (ic + ip) % 26]; res = xs % 7; cache = {}
    def ok(mask, m):
        k = (mask.tobytes(), m)
        if k not in cache:
            g = np.ones(amax, bool)
            for r in range(7):
                idx = np.where(mask & (res == r))[0]
                if len(idx) > 1: g &= (val[m][:, idx] == val[m][:, idx[:1]]).all(1)
            cache[k] = g
        return cache[k]
    T = np.zeros(amax, bool); Rt = np.zeros((amax, 2, 2), bool)
    for b1 in range(98):
        for b2 in range(b1, 98):
            s1, s2, s3 = xs < b1, (xs >= b1) & (xs < b2), xs >= b2
            o2 = ok(s2, 0) | ok(s2, 1)
            T |= (ok(s1, 0) | ok(s1, 1)) & o2 & (ok(s3, 0) | ok(s3, 1))
            for m1 in range(2):
                u = ok(s1 | s3, m1)
                for m2 in range(2): Rt[:, m1, m2] |= u & ok(s2, m2)
    Ta = sorted(np.where(T)[0].tolist()); Ra = sorted(tuple(map(int, x)) for x in zip(*np.where(Rt)))
    return Ta, Ra
if __name__ == "__main__":
    a = sys.argv; Ta, Ra = run(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]), int(a[7]) if len(a) > 7 else -1)
    print("RT", a[1], a[3], a[4], a[5], "drop=" + (a[7] if len(a) > 7 else "-1"), "T", len(Ta), ",".join(map(str, Ta[:50])), "R", len(Ra), ";".join("%d.%d.%d" % x for x in Ra[:50]))
