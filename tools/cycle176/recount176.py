"""Cycle 176: independent numpy recount of model G (ordinary Gromark, arbitrary cipher alphabet), written from the definition:
fit <=> for all crib pairs (a,b): [w_a == w_b] == [carved_a == carved_b]; w = PA(p)+d (vig) / d-PA(p) (beau).
Counts every (perm, primer, PA, form, ix) fit on a perm slice and prints per (text, ix, L) totals in gm176's H format, so the two
outputs can be compared line by line.   usage: recount176.py slice.bin Lmin Lmax label=CT [label=CT ...]"""
import sys, numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CI = list(range(21, 34)) + list(range(63, 74)); PT = "EASTNORTHEASTBERLINCLOCK"
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97); Lmin, Lmax = int(sys.argv[2]), int(sys.argv[3])
iu = np.triu_indices(24, 1)
for arg in sys.argv[4:]:
    lab, ct = arg.split("="); C = np.array([AZ.index(c) for c in ct])
    for ix in (0, 1):
        for L in range(Lmin, Lmax + 1):
            n = 10 ** L; pr = np.array([[int(c) for c in str(k).zfill(L)] for k in range(n)], dtype=np.int64)
            D = np.zeros((n, 97), dtype=np.int64); D[:, :L] = pr
            for i in range(L, 97): D[:, i] = (D[:, i - L] + D[:, i - L + 1]) % 10
            for paname, PA in (("az", AZ), ("ka", KA)):
                pv = np.array([PA.index(c) for c in PT])
                for form in ("vig", "beau"):
                    tot = 0
                    for S in P:
                        pos = np.array(CI) if ix == 0 else S[CI]
                        cts = C[S[CI]]; ceq = (cts[:, None] == cts[None, :])[iu]
                        G = D[:, pos]; w = (pv + G) % 26 if form == "vig" else (G - pv) % 26
                        weq = (w[:, :, None] == w[:, None, :])[:, iu[0], iu[1]]
                        tot += int(np.all(weq == ceq, axis=1).sum())
                    print("R", lab, ix, L, paname, form, n, n * len(P), tot, flush=True)
