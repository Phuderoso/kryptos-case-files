"""Cycle 175: independent recount of slip175 (numpy, different formulation, no code shared).
For each perm t and slot d the true ciphertext C' is rebuilt as a string (del: '?' inserted at d; ins: index d removed),
the crib key values are computed for all 8 (PA, CA, mode) at once, and for every p the full conflict matrix
conf[a, b] = (same residue) & (different key) is built.  Dropping crib i is consistent iff every conflict touches i,
i.e. sum of row i == total number of conflicting pairs.  checks = (#used - 1) - (#distinct residues of the others).
Counts HIST (all), HISTK (checks >= KMIN), EXPECT (sum 8*26^-checks) per p and compares them with slip175 on the same slice.
usage: recount175.py tool perms.bin n model CT lo hi [KMIN]"""
import sys, subprocess, numpy as np
tool, pf, n, model, ct, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
KMIN = int(sys.argv[8]) if len(sys.argv) > 8 else 4
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
CR = list(zip(list(range(21, 34)) + list(range(63, 74)), "EASTNORTHEAST" + "BERLINCLOCK"))
P = np.fromfile(pf, dtype=np.int16).reshape(-1, n); PM = 26; ps = np.arange(1, PM + 1)
TABS = [(pa, ca, mo) for pa in (AZ, KA) for ca in (AZ, KA) for mo in ("vig", "beau")]
H = np.zeros(PM + 1, np.int64); HK = np.zeros(PM + 1, np.int64); EX = np.zeros(PM + 1)
slots = range(98) if model == "delx" else range(97)
for t in range(lo, hi):
    perm = [int(x) for x in P[t]]
    for d in slots:
        Cp = ct[:d] + "?" + ct[d:] if model == "delx" else ct[:d] + ct[d + 1:]
        assert len(Cp) == n
        used = [(j, pl, perm[j]) for j, pl in CR if Cp[perm[j]] != "?"]; nu = len(used)
        kv = np.array([[((ca.index(Cp[u]) - pa.index(pl)) if mo == "vig" else (ca.index(Cp[u]) + pa.index(pl))) % 26 for j, pl, u in used] for pa, ca, mo in TABS])
        for ix in ("pt", "ct"):
            ids = np.array([u if ix == "ct" else j for j, pl, u in used])
            r = ids[None, :] % ps[:, None]                         # (PM, nu)
            same = r[:, :, None] == r[:, None, :]                  # (PM, nu, nu)
            np.einsum("pii->pi", same)[:] = False
            diff = kv[:, :, None] != kv[:, None, :]                # (8, nu, nu)
            conf = same[None] & diff[:, None]                      # (8, PM, nu, nu)
            tot = conf.sum(axis=(2, 3)) // 2                       # (8, PM)
            row = conf.sum(axis=3)                                 # (8, PM, nu)
            okdrop = row == tot[:, :, None]                        # (8, PM, nu)
            # checks per (p, drop): residues of the others
            chk = np.zeros((PM, nu), int)
            for pi, p in enumerate(ps):
                rr = list(r[pi])
                for i in range(nu):
                    chk[pi, i] = (nu - 1) - len(set(rr[:i] + rr[i + 1:]))
            H[1:] += okdrop.sum(axis=(0, 2)); HK[1:] += (okdrop & (chk[None] >= KMIN)).sum(axis=(0, 2))
            EX[1:] += (8.0 * 26.0 ** (-chk)).sum(axis=1)
out = subprocess.run([tool, pf, str(n), model, ct, "26", "0", str(KMIN), str(lo), str(hi)], capture_output=True, text=True).stdout
def line(k): return [l for l in out.splitlines() if l.split()[0] == k][0]
T = {k: [float(x.split(":")[1]) for x in line(k).split()[1:]] for k in ("HIST", "HISTK", "EXPECT")}
okH = list(H[1:]) == [int(x) for x in T["HIST"]]; okK = list(HK[1:]) == [int(x) for x in T["HISTK"]]
okE = all(abs(a - b) <= 1e-3 * max(abs(a), 1e-300) for a, b in zip(EX[1:], T["EXPECT"]))
print(f"{model} {pf.split('/')[-1]} {lo}-{hi}: HIST identical={okH} HISTK identical={okK} EXPECT agree(1e-3)={okE} | "
      f"python HIST p17-26 {list(H[17:])} tool {[int(x) for x in T['HIST'][16:]]}")
