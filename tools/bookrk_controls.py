"""Cycle 35 (bookrk_controls.py) controls: planted K4-like texts (English + cribs at the official positions) encrypted with a
Carter/Smith running key under a random transposition, both layer orders, incl. mixed-alphabet tableaux;
plus 6 shuffled-K4 nulls. Same conventions as bookrk.c."""
import random, re, numpy as np
from kryptos_text import K4, KA
random.seed(35); N = 97; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
perms = np.fromfile("perms97.bin", dtype=np.int16).reshape(-1, N)
texts = dict(l.split() for l in open("texts.txt"))
def enc(p, k, md):
    ty, ap, ac, ak = md % 3, (md//3) & 1, (md//6) & 1, (md//12) & 1
    Ap, Ac, Ak = (KA if ap else AZ), (KA if ac else AZ), (KA if ak else AZ)
    pi, kv = Ap.index(p), Ak.index(k)
    ci = (pi + kv) % 26 if ty == 0 else (kv - pi) % 26 if ty == 1 else (pi - kv) % 26
    return Ac[ci]
book = re.sub("[^A-Z]", "", open("/workspace/kcl/data/g84.txt").read().upper())
plans = [("carter1", 7, 'B'), ("carter1_rev", 16, 'A'), ("smith", 4, 'B'), ("carter1", 21, 'B')]
out = open("controls_planted.txt", "w")
for n, (tn, md, model) in enumerate(plans, 1):
    s = random.randrange(len(book) - 200); pt = list(book[s:s+N])
    pt[21:34] = "EASTNORTHEAST"; pt[63:74] = "BERLINCLOCK"
    T = texts[tn]; o = random.randrange(len(T) - N); pi = random.randrange(1, len(perms)); P = perms[pi]
    car = [None]*N
    for i in range(N):
        if model == 'A': car[P[i]] = enc(pt[i], T[o+i], md)
        else: car[i] = enc(pt[P[i]], T[o+i], md)
    open(f"ctl_{n}.txt", "w").write("".join(car))
    out.write(f"ctl_{n}: text={tn} mode={md} model={model} perm={pi} offset={o} pt={''.join(pt)}\n")
for k in range(1, 7):
    l = list(K4); random.shuffle(l); open(f"null_{k}.txt", "w").write("".join(l))
