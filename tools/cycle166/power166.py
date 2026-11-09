"""Cycle 166 power bound: fewest independent crib checks (crib letters minus distinct (segment-key, residue) classes)
over all boundary pairs, direct positions, for models T (3 keys), R (key 1 returns), 2-segment (cycle 162) for reference,
and the chance rate per (alphabet, forms) of 26^-checks summed over boundary classes (union bound)."""
CI = list(range(21, 34)) + list(range(63, 74))
def checks(groups): return sum(len(g) - len({x % 7 for x in g}) for g in groups)
bs = sorted(set([0, 97] + CI + [x + 1 for x in CI]))
res = {}
for name in ("2seg", "T", "R"):
    seen = {}
    for b1 in bs:
        for b2 in bs:
            if b2 < b1: continue
            s1 = [x for x in CI if x < b1]; s2 = [x for x in CI if b1 <= x < b2]; s3 = [x for x in CI if x >= b2]
            if name == "2seg": key = (len(s1),); c = checks([s1, s2 + s3])
            elif name == "T": key = (len(s1), len(s2)); c = checks([s1, s2, s3])
            else: key = (len(s1), len(s2)); c = checks([s1 + s3, s2])
            seen[key] = c
    cs = list(seen.values()); forms = {"2seg": 4, "T": 8, "R": 4}[name]
    ub = forms * sum(26.0 ** -c for c in cs)
    print(f"{name}: boundary classes {len(cs)}, min checks {min(cs)}, classes at min {cs.count(min(cs))}, union-bound chance per alphabet {ub:.3g}, x86731 = {ub*86731:.3g}, x2 (AZ/KA) = {ub*2:.3g}")
