"""Cycle 177: independent numpy recount, written from the definitions (no code shared with gm177.c / pg177.c).
Model G, one error (err 1): over the 276 crib-slot pairs, a pair is violated iff [w_a == w_b] != [carved_a == carved_b]; slot t
repairs the fit iff every violated pair contains t; mask = set of such t (full = strict). Model GB (err 0): no violated pair.
Model PG1: >= 23 of the 24 exact predictions CA[(PA(p) + k) % 26] (vig) / CA[(k - PA(p)) % 26] (beau) hold.
Prints one line per fit:  G lab ix L pa form base q primer mask   /   P lab ix form q cfg miss   (q = index in the slice).
usage: recount177.py slice.bin cfg176.txt label=CT [label=CT ...]
env RC_L5=1: model G one-error base 10 at L 5 only, no GB/PG (the second, targeted slice)."""
import sys, os, numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CI = np.array(list(range(21, 34)) + list(range(63, 74))); PT = "EASTNORTHEASTBERLINCLOCK"
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97).astype(np.int64)
iu = np.triu_indices(24, 1); INC = np.zeros((276, 24), dtype=np.int64)
INC[np.arange(276), iu[0]] = 1; INC[np.arange(276), iu[1]] = 1
POW = (1 << np.arange(24)).astype(np.int64)
def gstreams(L, b):
    n = b ** L; pr = np.zeros((n, L), dtype=np.int64); z = np.arange(n)
    for i in range(L - 1, -1, -1): pr[:, i] = z % b; z //= b
    D = np.zeros((n, 97), dtype=np.int64); D[:, :L] = pr
    for i in range(L, 97): D[:, i] = (D[:, i - L] + D[:, i - L + 1]) % b
    return D
cfgl = []
for l in open(sys.argv[2]):
    a = l.split(); cfgl.append(a)
CN = [a[0] for a in cfgl]; CA = np.array([[AZ.index(c) for c in a[1]] for a in cfgl]); PAs = [a[2] for a in cfgl]
K = np.array([[AZ.index(c) for c in a[3]] for a in cfgl])
PV = np.array([[PA.index(p) for p in PT] for PA in PAs])                      # (nc, 24) PA index of each crib letter
for arg in sys.argv[3:]:
    lab, ct = arg.split("="); C = np.array([AZ.index(c) for c in ct])
    for (b, err, Ls) in (((10, 1, (5,)),) if os.environ.get('RC_L5') else ((10, 1, (2, 3, 4)), (7, 0, (2, 3, 4)))):
        for L in Ls:
            D = gstreams(L, b)
            for ix in (0, 1):
                for paname, PA in (("az", AZ), ("ka", KA)):
                    pv = np.array([PA.index(c) for c in PT])
                    for form in ("vig", "beau"):
                        for q, S in enumerate(P):
                            pos = CI if ix == 0 else S[CI]
                            cts = C[S[CI]]; ceq = (cts[:, None] == cts[None, :])[iu]
                            G = D[:, pos]; w = (pv + G) % 26 if form == "vig" else (G - pv) % 26
                            weq = (w[:, :, None] == w[:, None, :])[:, iu[0], iu[1]]
                            viol = (weq != ceq).astype(np.int64); tot = viol.sum(1)
                            if err == 0: idx = np.nonzero(tot == 0)[0]; masks = np.full(len(idx), 0xFFFFFF)
                            else:
                                withT = viol @ INC; feas = withT == tot[:, None]; m = feas @ POW
                                idx = np.nonzero(m)[0]; masks = m[idx]
                            for k, m in zip(idx, masks):
                                print("G", lab, ix, L, paname, form, b, q, "".join(str(x) for x in D[k, :L]), format(int(m), "06x"))
    # PG1
    for ix in (() if os.environ.get('RC_L5') else (0, 1)):
        for form in ("vig", "beau"):
            for q, S in enumerate(P):
                kk = K[:, CI] if ix == 0 else K[:, S[CI]]
                v = (PV + kk) % 26 if form == "vig" else (kk - PV) % 26
                pred = np.take_along_axis(CA, v, axis=1)
                match = pred == C[S[CI]][None, :]; nm = match.sum(1)
                for c in np.nonzero(nm >= 23)[0]:
                    miss = -1 if nm[c] == 24 else int(np.nonzero(~match[c])[0][0])
                    print("P", lab, ix, form, q, CN[c], miss)
    sys.stdout.flush()
