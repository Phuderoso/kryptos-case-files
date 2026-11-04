"""Cycle 23: planted controls, shuffled-K4 nulls and the K4 run for ptak_score.c (blind lags 24-96)."""
import random, subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, 97)
PTS = ["SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT",
       "WEFOLLOWEDTHEOLDROADT" + "EASTNORTHEAST" + "UNTILTHESHADOWFELLACROSSTHEDO" + "BERLINCLOCK" + "ANDTHEVAULTOPENEDSLOWLY"]
assert all(len(p) == 97 for p in PTS)
def ak(src, A, mode, L, rnd):
    prim = [rnd.randrange(26) for _ in range(L)]; out = []
    for i, ch in enumerate(src):
        p = A.index(ch); k = prim[i] if i < L else A.index(src[i - L])
        out.append(A[{0: p + k, 1: k - p, 2: p - k}[mode] % 26])
    return "".join(out)
def run(text, strict, top=20):
    return subprocess.run(["./ptak_score", text, "perms97.bin", "qg.bin", "6" if strict else "8", "24", "96", str(top), str(strict)],
                          capture_output=True, text=True).stdout
jobs = []
for seed, L in ((1, 28), (2, 52), (3, 67), (4, 88), (5, 33), (6, 75)):
    rnd = random.Random(100 + seed); pi = rnd.randrange(len(perms)); P = perms[pi]
    A = rnd.choice([KA, AZ]); mode = rnd.randrange(3); model = "AB"[seed % 2]; PT = PTS[seed % 2]
    if model == "A":
        C = ak(PT, A, mode, L, rnd); carved = [None] * 97
        for i in range(97): carved[P[i]] = C[i]
        carved = "".join(carved)
    else:
        carved = ak("".join(PT[P[k]] for k in range(97)), A, mode, L, rnd)
    jobs.append(("control", f"seed={seed} model={model} tab={'KA' if A == KA else 'AZ'} mode={mode} L={L} perm={pi}", carved, (pi, L, model)))
for s in range(1, 7):
    l = list(K4); random.Random(s).shuffle(l); jobs.append(("null", f"shuffle seed={s}", "".join(l), None))
jobs.append(("K4", "carved K4", K4, None))
def work(j):
    kind, tag, text, truth = j; res = []
    for strict in (1, 0):
        out = run(text, strict).splitlines(); body = [l for l in out if not l.startswith("tests")]
        rank = None
        if truth:
            for r, l in enumerate(body, 1):
                if f"perm={truth[0]} " in l and f"L={truth[1]} " in l and f"model={truth[2]}" in l: rank = r; break
        res.append((strict, out[0], body, rank))
    return j, res
lines = []
with ThreadPoolExecutor(8) as ex:
    for (kind, tag, text, truth), res in ex.map(work, jobs):
        for strict, head, body, rank in res:
            sc = "strict" if strict else "loose"
            best = body[0] if body else "none"
            extra = (f" true config rank={rank if rank else '>20 (MISSED)'}" if truth else "")
            lines.append(f"[{kind}] {tag} [{sc}] {head};{extra}\n    best: {best}")
            if kind == "K4": lines += ["    " + b for b in body[1:10]]
        print("\n".join(lines[-2:]), flush=True)
open("ptak_score_report.txt", "w").write("\n".join(lines) + "\n")
