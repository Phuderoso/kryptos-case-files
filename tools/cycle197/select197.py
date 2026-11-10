"""Cycle 197: text-free pair selection for the decimation stage (structure pass on every 32nd perm of dec98/dec96 (solver A) and
every 8th of the M = N subsets (solver B); the E column is structure-only, independent of the text). Scaled cell E = sample E x
(family size / sample size). Pairs with scaled cell E <= 0.10 are run; the registered full-power label uses the EXACT cell E printed by
the run (<= 0.05). Writes pairsA_{del,ins}.txt and pairsB_{del,ins}.txt."""
import sys
fam = {"del": (170258, 5321, 4116, 515), "ins": (168858, 5277, 3072, 384)}
for kind, (NA, SA, NB, SB) in fam.items():
    for solver, fn, scale in (("A", f"work/structA_{kind}.txt", NA / SA), ("B", f"work/structB_{kind}.txt", NB / SB)):
        best = {}
        for line in open(fn):
            w = line.split()
            if w[0] != "H": continue
            md, m, n = w[3], int(w[6]), int(w[7]); E = float(w[-1]) * scale
            best[(md, m, n)] = max(best.get((md, m, n), 0), E)
        sel = sorted(k for k, E in best.items() if E <= 0.10)
        with open(f"repo/tools/cycle197/pairs{solver}_{kind}.txt", "w") as f:
            for (md, m, n) in sel: f.write(f"{md} {m} {n}\n")
        print(kind, solver, {md: sum(1 for k in sel if k[0] == md) for md in "PC"}, "lcm max", max((m * n // __import__('math').gcd(m, n)) for (_, m, n) in sel) if sel else 0)
