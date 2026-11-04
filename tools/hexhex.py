"""Cycle 36 side test, 'hex inside hex' taken literally: each carved letter -> its number (A-Z or KRYPTOS order,
0- or 1-based) -> two digits in base b (b = 6..16) -> the 194-digit stream is regrouped (shift by 1 digit with wrap,
reversed, digit-complement, pairs swapped, odd/even digits split) -> pairs read back as letters. A reading is 'valid'
only if every pair is a letter (< 26). Valid readings are tested (a) directly against the 24 cribs and (b) for a
periodic Vigenere/Beaufort/variant key p<=26 over AZ/KA tableaux consistent with all cribs. Same for shuffled nulls
and for planted controls built through the inverse map."""
import random, itertools
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; N = 97
CR = [(21+i, c) for i, c in enumerate("EASTNORTHEAST")] + [(63+i, c) for i, c in enumerate("BERLINCLOCK")]
def nums(t, A, z): return [A.index(c) + z for c in t]
def regroup(d, op):
    n = len(d)
    if op == "shift1": return d[1:] + d[:1]
    if op == "shiftm1": return d[-1:] + d[:-1]
    if op == "rev": return d[::-1]
    if op == "swap": return [d[i ^ 1] for i in range(n)]
    if op == "oddeven": return d[0::2] + d[1::2]
    if op == "evenodd_inv":  # inverse of oddeven
        h = n // 2; out = [0]*n; out[0::2] = d[:h]; out[1::2] = d[h:]; return out
    raise ValueError
OPS = ["shift1", "shiftm1", "rev", "swap", "oddeven", "evenodd_inv"]
def readings(t):
    for A, an in ((AZ, "AZ"), (KA, "KA")):
        for z in (0, 1):
            for b in range(6, 17):
                if 26 + z > b*b: continue
                v = nums(t, A, z); d = []
                for x in v: d += [x // b, x % b]
                for comp in (0, 1):
                    dd = [b-1-x for x in d] if comp else d
                    for op in OPS:
                        e = regroup(dd, op); out = []
                        for i in range(0, len(e), 2):
                            x = e[i]*b + e[i+1] - z
                            if not 0 <= x < 26: break
                            out.append(A[x])
                        else: yield (an, z, b, comp, op), "".join(out)
def periodic_ok(t):
    hits = []
    for TA, tn in ((AZ, "AZ"), (KA, "KA")):
        for ty in range(3):
            ks = []
            for p, c in CR:
                ci, pi = TA.index(t[p]), TA.index(c)
                ks.append((p, (ci-pi) % 26 if ty == 0 else (ci+pi) % 26 if ty == 1 else (pi-ci) % 26))
            for P in range(1, 27):
                m = {}
                if all(m.setdefault(p % P, k) == k for p, k in ks): hits.append((tn, ty, P))
    return hits
def scan(t, label):
    nv = 0; direct = 0; per = []
    for cfg, r in readings(t):
        nv += 1
        if sum(r[p] == c for p, c in CR) >= 20: direct += 1
        h = [x for x in periodic_ok(r) if x[2] <= 20]
        if h: per.append((cfg, h[:3]))
    print(f"{label}: valid readings {nv}, direct crib >=20/24: {direct}, periodic p<=20 consistent: {len(per)}", per[:3])
    return nv, per
scan(K4, "K4")
random.seed(3636)
for k in range(10):
    l = list(K4); random.shuffle(l); scan("".join(l), f"null{k+1}")
# planted controls: English+cribs -> Vigenere KA period 7 -> inverse of a hex regroup, only when representable
book = open("/workspace/kcl/data/g84.txt").read().upper(); import re; book = re.sub("[^A-Z]", "", book)
inv = {"shift1": "shiftm1", "shiftm1": "shift1", "rev": "rev", "swap": "swap", "oddeven": "evenodd_inv"}
made = 0; tries = 0
while made < 3 and tries < 20000:
    tries += 1
    s = random.randrange(len(book)-200); pt = list(book[s:s+N]); pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    key = [random.randrange(26) for _ in range(7)]
    mid = "".join(KA[(KA.index(c) + key[i % 7]) % 26] for i, c in enumerate(pt))
    b = random.choice([6, 7, 8, 16]); op = random.choice(list(inv)); A = KA
    d = []
    for x in nums(mid, A, 0): d += [x // b, x % b]
    e = regroup(d, inv[op]); out = []
    for i in range(0, len(e), 2):
        x = e[i]*b + e[i+1]
        if x >= 26: break
        out.append(A[x])
    else:
        made += 1; ct = "".join(out); nv, per = scan(ct, f"control{made} (b={b}, op={op}, KA Vig p=7)")
        print("   recovered:", any(c[0] == ("KA", 0, b, 0, op) and ("KA", 0, 7) in h for c, h in per))
print("control tries", tries)
