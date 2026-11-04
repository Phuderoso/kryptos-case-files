"""Cycle 45 controls: planted K4-like texts (English + cribs at official positions) encrypted with a running key
from this cycle's texts under a rail/Redefence/AMSCO permutation from cycle 44's files, both layer orders,
incl. KRYPTOS-alphabet tableaux; plus 3 shuffled-K4 nulls. Same conventions as bookrk.c (cycle 35)."""
import random, re, numpy as np
from kryptos_text import K4, KA
random.seed(45); N = 97; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms = np.fromfile("all.bin", dtype=np.int16).reshape(-1, N)
tags = open("/workspace/k4c44/perms_A.txt").read().split("\n")[:-1] + open("/workspace/k4c44/perms_B.txt").read().split("\n")[:-1]
texts = dict(l.split() for l in open("texts.txt"))
def enc(p, k, md):
    ty, ap, ac, ak = md % 3, (md//3) & 1, (md//6) & 1, (md//12) & 1
    Ap, Ac, Ak = (KA if ap else AZ), (KA if ac else AZ), (KA if ak else AZ)
    pi, kv = Ap.index(p), Ak.index(k)
    ci = (pi + kv) % 26 if ty == 0 else (kv - pi) % 26 if ty == 1 else (pi - kv) % 26
    return Ac[ci]
book = re.sub("[^A-Z]", "", open("/workspace/kcl/data/g84.txt").read().upper())
# perm picks: one rail/Redefence (indices 1-73240), two AMSCO
nA = 422433
plans = [("carter1", 7, "B", random.randrange(1, 73240)), ("c34_K3pt", 16, 'A', random.randrange(nA, len(perms))),
         ("kjv_john_rev", 4, 'B', random.randrange(nA, len(perms)))]
out = open("controls_planted.txt", "w")
for n, (tn, md, model, pi) in enumerate(plans, 1):
    s = random.randrange(len(book) - 200); pt = list(book[s:s+N])
    pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    T = texts[tn]; o = random.randrange(len(T) - N); P = perms[pi]
    car = [None]*N
    for i in range(N):
        if model == 'A': car[P[i]] = enc(pt[i], T[o+i], md)
        else: car[i] = enc(pt[P[i]], T[o+i], md)
    open(f"ctl_{n}.txt", "w").write("".join(car))
    lo = max(0, pi - 10000); hi = min(len(perms), lo + 20000)
    perms[lo:hi].tofile(f"ctl_{n}_slice.bin")
    out.write(f"ctl_{n}: text={tn} mode={md} model={model} perm={pi} ({tags[pi]}) slice_start={lo} expect_slice_perm={pi-lo} offset={o} pt={''.join(pt)}\n")
for k in range(1, 4):
    l = list(K4); random.shuffle(l); open(f"null_{k}.txt", "w").write("".join(l))
