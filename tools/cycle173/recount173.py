"""Cycle 173: independent brute-force recount of anom173 (pure Python, string tableaux, dict per residue class).
For a slice of perms, rebuild the true-ciphertext letters under each anomaly slot directly from the definition
(del: C' = carved with an unknown letter inserted at d; ins: C' = carved minus index d; chg: crib d unchecked; swp: carved d<->d+1),
and list every consistent (t, d, PA, CA, mode, idx, p). Compares the set with anom173's HIT lines (PPRINT = 26).
usage: recount173.py tool perms.bin n model CT lo hi"""
import sys, subprocess, numpy as np
tool, pf, n, model, ct, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
T = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CR = list(zip(list(range(21, 34)) + list(range(63, 74)), "EASTNORTHEAST" + "BERLINCLOCK"))
P = np.fromfile(pf, dtype=np.int16).reshape(-1, n)
mine = set()
slots = {"del": range(98), "ins": range(97), "chg": range(24), "swp": range(96), "none": range(1)}[model]
for t in range(lo, hi):
    perm = [int(x) for x in P[t]]
    for d in slots:
        if model == "del": C = ct[:d] + "?" + ct[d:]
        elif model == "ins": C = ct[:d] + ct[d + 1:]
        elif model == "swp": C = ct[:d] + ct[d + 1] + ct[d] + ct[d + 2:]
        else: C = ct
        assert len(C) == n
        cr = [(j, pl) for k, (j, pl) in enumerate(CR) if not (model == "chg" and k == d)]
        for pa in "AZ", "KA":
            for ca in "AZ", "KA":
                for mo in "vig", "beau":
                    for ix in "pt", "ct":
                        for p in range(1, 27):
                            key = {}; ok = True
                            for j, pl in cr:
                                c = C[perm[j]]
                                if c == "?": continue
                                k = (T[ca].index(c) - T[pa].index(pl)) % 26 if mo == "vig" else (T[ca].index(c) + T[pa].index(pl)) % 26
                                r = (perm[j] if ix == "ct" else j) % p
                                if key.setdefault(r, k) != k: ok = False; break
                            if ok: mine.add((t, d, pa, ca, mo, ix, p))
out = subprocess.run([tool, pf, str(n), model, ct, "26", "26", str(lo), str(hi)], capture_output=True, text=True).stdout
theirs = set()
for l in out.splitlines():
    if l.startswith("HIT"):
        f = dict(x.split("=") for x in l.split()[1:])
        theirs.add((int(f["t"]), int(f["d"]), f["PA"], f["CA"], f["mode"], f["idx"], int(f["p"])))
print(f"{model} slice {lo}-{hi}: python {len(mine)} tool {len(theirs)} identical={mine == theirs}")
