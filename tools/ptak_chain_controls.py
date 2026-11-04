"""Cycle 22 planted controls and shuffled nulls for ptak_chain.c."""
import random, subprocess, numpy as np
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
PT = "SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT"
def ak(src, A, mode, L, rnd):
    prim = [rnd.randrange(26) for _ in range(L)]; out = []
    for i, ch in enumerate(src):
        p = A.index(ch); k = prim[i] if i < L else A.index(src[i - L])
        out.append(A[{"vig": p + k, "beau": k - p, "var": p - k}[mode] % 26])
    return "".join(out)
def run(text):
    r = subprocess.run(["./ptak_chain", text, "perms97.bin", "6"], capture_output=True, text=True).stdout
    return r
out = []
for seed, L in ((1, 3), (2, 12), (3, 30), (4, 45), (5, 20), (6, 52)):
    rnd = random.Random(seed); pi = rnd.randrange(len(perms)); P = perms[pi]
    A = rnd.choice([KA, AZ]); mode = rnd.choice(["vig", "beau", "var"]); model = "AB"[seed % 2]
    if model == "A":
        C = ak(PT, A, mode, L, rnd); carved = [None]*97
        for i in range(97): carved[P[i]] = C[i]
        carved = "".join(carved)
    else:
        Q = "".join(PT[P[k]] for k in range(97)); carved = ak(Q, A, mode, L, rnd)
    r = run(carved); hits = [l for l in r.splitlines() if l.startswith("HIT")]
    found = any(f"perm={pi} " in h and f"L={L} " in h and f"model={model}" in h for h in hits)
    out.append(f"control seed={seed} model={model} tab={'KA' if A==KA else 'AZ'} mode={mode} L={L} perm={pi}: "
               f"{'RECOVERED' if found else 'MISSED'}; hits={len(hits)}; " + r.splitlines()[-1])
    print(out[-1], flush=True)
for s in range(1, 6):
    l = list(K4); random.Random(s).shuffle(l); r = run("".join(l))
    out.append(f"null shuffle seed={s}: " + " | ".join(r.splitlines()[-2:])); print(out[-1], flush=True)
open("ptak_chain_controls.txt", "w").write("\n".join(out) + "\n")
