"""Cycle 167: power of the segment-shift model at the direct crib positions.  For every boundary pair with three non-empty
segments, checks = equations - rank (rank = touched nodes - components of the graph key residue <-> segment shift).
Union bound per alphabet and form triple: sum 26^-checks over pairs; x 8 triples x 86,731 alphabets = expected chance fits.
Also for 2000 random 24-position sets (proxy for bank layers)."""
import random
def stats(pos):
    pos = sorted(pos); n = len(pos); r = [p % 7 for p in pos]; mn = 99; ub = 0.0
    for e1 in range(1, n - 1):
        for e2 in range(e1 + 1, n):
            par = list(range(10))
            def fd(x):
                while par[x] != x: x = par[x]
                return x
            nodes = set(); comps = 0
            for i in range(n):
                s = 0 if i < e1 else (1 if i < e2 else 2); a, b = r[i], 7 + s; nodes |= {a, b}
                ra, rb = fd(a), fd(b)
                if ra != rb: par[ra] = rb
            rank = len(nodes) - len({fd(x) for x in nodes}); ch = n - rank; mn = min(mn, ch); ub += 26.0 ** -ch
    return mn, ub
CRIB = list(range(21, 34)) + list(range(63, 74))
mn, ub = stats(CRIB)
print(f"direct: fewest checks {mn}, union bound per alphabet per triple {ub:.3g}, x8 x86731 = {ub*8*86731:.3g} chance fits per text")
rng = random.Random(16799); M = []; U = []
for _ in range(300):
    m, u = stats(rng.sample(range(97), 24)); M.append(m); U.append(u)
M.sort(); U.sort()
print(f"random 24-position layers (300): fewest checks min {M[0]} median {M[150]}; union bound median {U[150]:.3g}, max {U[-1]:.3g};"
      f" x8x2 (A-Z/KA) x660,260 configs median {U[150]*16*660260:.3g} chance fits per text")
for nm, mm in [("two segments k|k+d (subset of case 150)", None)]: pass
