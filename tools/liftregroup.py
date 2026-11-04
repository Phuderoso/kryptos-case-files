"""Cycle 37: 'hex inside hex', mod-26 version. Model: plaintext letter -> number n (A-Z or KRYPTOS order, 0/1-based)
-> two base-b digits (b = 10 decimal, 16 hex) -> the 194-digit stream is transposed by a digit-level permutation
(rotations, reversal, odd/even split, columnar widths 2-40 plain and keyword-keyed, and inverses) -> regrouped into
pairs -> pair value v (0..b*b-1) -> cipher letter A[(v - z) mod 26]. Unlike cycle 36's literal regrouping this is
valid for any plaintext. Decryption is a constraint problem: each carved letter has 4 (decimal) or 10 (hex) possible
lifted pair values; the permuted digits must regroup into plaintext pairs that are letters, and the 24 crib letters
are fixed. Solved exactly with z3 per configuration. Shuffled nulls and planted controls run through the same code."""
import random, sys, itertools, z3
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; N = 97; D = 2*N
CR = [(21+i, c) for i, c in enumerate("EASTNORTHEAST")] + [(63+i, c) for i, c in enumerate("BERLINCLOCK")]
KW = ["KRYPTOS","PALIMPSEST","ABSCISSA","BERLIN","CLOCK","SHADOW","LUCID","MEMORY","SANBORN","SCHEIDT","LANGLEY",
      "EASTNORTHEAST","BERLINCLOCK","HEX","DIGIT","REGROUP","LAYER","IQLUSION","UNDERGRUUND","DESPARATLY","EGYPT","CARTER"]
def colperm(n, w, order):  # read columns of a width-w row-filled grid in 'order'; returns list: out[j] = src index
    return [r*w + c for c in order for r in range((n - c + w - 1)//w) if r*w + c < n]
def kworder(k):
    k = k[:]; return sorted(range(len(k)), key=lambda i: (k[i], i))
def inv(p): q = [0]*len(p); [q.__setitem__(s, j) for j, s in enumerate(p)]; return q
def family():
    F = {"id": list(range(D)), "rev": list(range(D))[::-1]}
    for s in range(1, D): F[f"rot{s}"] = [(j + s) % D for j in range(D)]
    oe = list(range(0, D, 2)) + list(range(1, D, 2)); F["oddeven"] = oe; F["oddeven_inv"] = inv(oe)
    for w in range(2, 41):
        p = colperm(D, w, list(range(w))); F[f"col{w}"] = p; F[f"col{w}_inv"] = inv(p)
    for k in KW:
        o = kworder(k); w = len(k); p = colperm(D, w, [o.index(i) for i in range(w)])
        p2 = colperm(D, w, o)
        for nm, pp in ((f"kw_{k}", p), (f"kw2_{k}", p2)):
            F[nm] = pp; F[nm + "_inv"] = inv(pp)
    return F
SCHEMES = [(A, an, z, b) for A, an in ((AZ, "AZ"), (KA, "KA")) for z in (0, 1) for b in (10, 16)]
def encrypt(pt, perm, A, z, b):
    d = []
    for c in pt: x = A.index(c) + z; d += [x // b, x % b]
    e = [d[perm[j]] for j in range(D)]  # cipher digit j comes from plaintext digit perm[j]
    return "".join(A[(e[2*i]*b + e[2*i+1] - z) % 26] for i in range(N))
def solve(ct, perm, A, z, b, want_model=False):
    s = z3.Solver(); x = [z3.Int(f"x{j}") for j in range(D)]  # cipher digits
    for i in range(N):
        c = A.index(ct[i]); opts = [v for v in range(b*b) if (v - z) % 26 == c]
        s.add(z3.Or([z3.And(x[2*i] == v // b, x[2*i+1] == v % b) for v in opts]))
    y = [None]*D
    for j in range(D): y[perm[j]] = x[j]   # plaintext digit perm[j] = cipher digit j
    for k in range(N):
        v = y[2*k]*b + y[2*k+1]
        s.add(v >= z, v <= 25 + z)
    for p, ch in CR: s.add(y[2*p]*b + y[2*p+1] == A.index(ch) + z)
    r = s.check()
    if r == z3.sat and want_model:
        m = s.model(); return "".join(A[m.eval(y[2*k]*b + y[2*k+1]).as_long() - z] for k in range(N))
    return r == z3.sat
def scan(ct, label, F, out):
    hits = []
    for (A, an, z, b) in SCHEMES:
        for nm, p in F.items():
            if solve(ct, p, A, z, b): hits.append((an, z, b, nm))
    out.write(f"{label}: configs {len(SCHEMES)*len(F)}, SAT {len(hits)}\n")
    for h in hits[:40]: out.write(f"  {h}\n")
    out.flush(); return hits
if __name__ == "__main__":
    F = family(); mode = sys.argv[1]; out = sys.stdout
    if mode == "k4": scan(K4, "K4", F, out)
    elif mode == "null":
        r = random.Random(int(sys.argv[2])); t = list(K4); r.shuffle(t); scan("".join(t), f"null{sys.argv[2]}", F, out)
    elif mode == "control":
        r = random.Random(int(sys.argv[2]))
        pt = ("WHATISHIDDENBELOWTHESTONEISONLYTHELIGHTOFAMOMENTTHEEASTNORTHEASTDOORWAYSTANDSBYTHEBERLINCLOCKANDWAITSFORTHENIGHT")
        pt = list(pt[:97]); 
        for p, ch in CR: pt[p] = ch
        pt = "".join(pt); A, an, z, b = SCHEMES[r.randrange(len(SCHEMES))]; nm = r.choice(list(F)); ct = encrypt(pt, F[nm], A, z, b)
        ok = solve(ct, F[nm], A, z, b); out.write(f"control{sys.argv[2]}: planted ({an},{z},{b},{nm}) recovered={ok}\n")
        hits = scan(ct, f"control{sys.argv[2]}_scan", F, out)
        out.write(f"  planted config among hits: {(an,z,b,nm) in hits}\n")
