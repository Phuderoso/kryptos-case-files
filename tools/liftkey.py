"""Cycle 38: cycle 37's lifted (mod-26) digit regrouping with a keyword layer on top, K1-K3 style.
Layer order 'post': plaintext -> lifted regroup (cycle 37) -> periodic keyword substitution -> carved text.
Layer order 'pre' : plaintext -> periodic keyword substitution -> lifted regroup -> carved text.
Substitution modes in the scheme's own alphabet (AZ or KRYPTOS): vig c=L+k, beau c=k-L, var c=L-k (mod 26).
Keys: the 22 themed keywords of cycle 37, offset 0. Each config is first checked with a cheap exact necessary
condition (digits forced by the 24 cribs must fit the carved letters); survivors are solved exactly with z3.
Shuffled-K4 nulls and planted controls go through the same code."""
import random, sys
from liftregroup import family, SCHEMES, solve, encrypt, CR, KW, AZ, N, D, inv
from kryptos_text import K4
MODES = ("vig", "beau", "var")
def sub(L, k, m): return (L + k) % 26 if m == "vig" else ((k - L) % 26 if m == "beau" else (L - k) % 26)
def unsub(c, k, m): return (c - k) % 26 if m == "vig" else ((k - c) % 26 if m == "beau" else (c + k) % 26)
def keyseq(A, kw): return [A.index(kw[i % len(kw)]) for i in range(N)]
def quick(target, cribs, perm, z, b):
    """target[i]: required (v-z) mod 26 at cipher pair i; cribs: {p: plaintext value incl z}. Necessary check."""
    ip = inv(perm); known = {}
    for p, val in cribs.items():
        known[ip[2*p]] = val // b; known[ip[2*p+1]] = val % b
    pairs = {}
    for j, d in known.items(): pairs.setdefault(j // 2, {})[j % 2] = d
    for i, kd in pairs.items():
        ok = False
        for hi in ([kd[0]] if 0 in kd else range(b)):
            for lo in ([kd[1]] if 1 in kd else range(b)):
                if (hi*b + lo - z) % 26 == target[i]: ok = True; break
            if ok: break
        if not ok: return False
    return True
def configs(ct, F):
    for (A, an, z, b) in SCHEMES:
        c = [A.index(x) for x in ct]
        for kw in KW:
            k = keyseq(A, kw)
            for m in MODES:
                # post: undo key on carved text, then plain cycle-37 problem
                t = [unsub(c[i], k[i], m) for i in range(N)]
                cr = {p: A.index(ch) + z for p, ch in CR}
                ctp = "".join(A[x] for x in t)
                for nm, p in F.items(): yield (A, an, z, b, kw, m, "post", nm, p, t, cr, ctp, None)
                # pre: cribs become keyed plaintext values
                crq = {p: sub(A.index(ch), k[p], m) + z for p, ch in CR}
                for nm, p in F.items(): yield (A, an, z, b, kw, m, "pre", nm, p, c, crq, ct, crq)
def solve_pre(ct, perm, A, z, b, crq):
    import z3
    s = z3.Solver(); x = [z3.Int(f"x{j}") for j in range(D)]
    for i in range(N):
        cc = A.index(ct[i]); opts = [v for v in range(b*b) if (v - z) % 26 == cc]
        s.add(z3.Or([z3.And(x[2*i] == v // b, x[2*i+1] == v % b) for v in opts]))
    y = [None]*D
    for j in range(D): y[perm[j]] = x[j]
    for kk in range(N):
        v = y[2*kk]*b + y[2*kk+1]; s.add(v >= z, v <= 25 + z)
    for p, val in crq.items(): s.add(y[2*p]*b + y[2*p+1] == val)
    return s.check() == z3.sat
def scan(ct, label, F, out):
    n = surv = 0; hits = []
    for (A, an, z, b, kw, m, order, nm, p, t, cr, ctp, crq) in configs(ct, F):
        n += 1
        if not quick(t, cr, p, z, b): continue
        surv += 1
        ok = solve(ctp, p, A, z, b) if order == "post" else solve_pre(ct, p, A, z, b, crq)
        if ok: hits.append((an, z, b, kw, m, order, nm))
    out.write(f"{label}: configs {n}, pass prefilter {surv}, SAT {len(hits)}\n")
    for h in hits[:40]: out.write(f"  {h}\n")
    out.flush(); return hits
def plant(seed, F):
    r = random.Random(seed)
    pt = list("WHATISHIDDENBELOWTHESTONEISONLYTHELIGHTOFAMOMENTTHEEASTNORTHEASTDOORWAYSTANDSBYTHEBERLINCLOCKANDWAITSFORTHENIGHT"[:97])
    for p, ch in CR: pt[p] = ch
    A, an, z, b = SCHEMES[r.randrange(len(SCHEMES))]; kw = r.choice(KW); m = r.choice(MODES); order = r.choice(["post", "pre"])
    nm = r.choice(list(F)); k = keyseq(A, kw)
    if order == "pre":
        q = "".join(A[sub(A.index(ch), k[i], m)] for i, ch in enumerate(pt)); ct = encrypt(q, F[nm], A, z, b)
    else:
        e = encrypt("".join(pt), F[nm], A, z, b); ct = "".join(A[sub(A.index(ch), k[i], m)] for i, ch in enumerate(e))
    return ct, (an, z, b, kw, m, order, nm)
if __name__ == "__main__":
    F = family(); mode = sys.argv[1]; out = sys.stdout
    if mode == "k4": scan(K4, "K4", F, out)
    elif mode == "null":
        r = random.Random(int(sys.argv[2])); t = list(K4); r.shuffle(t); scan("".join(t), f"null{sys.argv[2]}", F, out)
    elif mode == "control":
        ct, cfg = plant(int(sys.argv[2]), F); out.write(f"control{sys.argv[2]}: planted {cfg}\n")
        hits = scan(ct, f"control{sys.argv[2]}_scan", F, out); out.write(f"  planted config among hits: {cfg in hits}\n")
