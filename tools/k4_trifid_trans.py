"""Cycle 21 (2): Trifid (arbitrary 27-symbol cube) behind or in front of a transposition, periods 1..20,
both Trifid orientations, over the cycle-19 transposition family (all column orders w<=8, K3-style single/double
rotations w 2..49, inverses). Cheap exact prefilter (union-find contradictions: two symbols forced onto the same
cube cell, or >9 symbols forced onto one digit value of an axis), then CaDiCaL on survivors."""
import sys, random, json, multiprocessing as mp
import numpy as np
from k4_autokey_trans import family
from k4_trifid_sat import equalities, consistent, CRIB, trifid_enc, SYM
from kryptos_text import K4
PER = range(1, 21)
def prefilter(eq):
    par = {}
    def f(x):
        while par.setdefault(x, x) != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in eq:
        ra, rb = f(a), f(b)
        if ra != rb: par[ra] = rb
    syms = {s for (a, b) in eq for s in (a[0], b[0])}
    sig = {}
    for s in syms:
        k = tuple(f((s, ax)) for ax in range(3))
        if k in sig: return False
        sig[k] = s
    cnt = {}
    for s in syms:
        for ax in range(3):
            r = f((s, ax)); cnt.setdefault((r, ax), set()).add(s)
    if any(len(v) > 9 for v in cnt.values()): return False
    return True
def work(args):
    text, perm, tag = args; hits = []; pre = 0
    n = len(text)
    # layer order A: K4 = T(Trifid(P)) -> Trifid ciphertext = text[perm]; cribs stay
    ctA = "".join(text[i] for i in perm)
    # layer order B: K4 = Trifid(T(P)) -> intermediate plaintext position perm^-1; crib i moves to position j where perm[j]==i
    inv = {int(v): j for j, v in enumerate(perm)}
    cribB = {inv[i]: c for i, c in CRIB.items()}
    for order, ct, crib in (("A", ctA, CRIB), ("B", text, cribB)):
        for p in PER:
            for o in (0, 1):
                eq = equalities(ct, crib, p, o)
                if prefilter(eq):
                    pre += 1
                    if consistent(ct, crib, p, o)[0]: hits.append((tag, order, p, o))
    return hits, pre
def run(text, label, fam):
    with mp.Pool(8) as pool:
        H = []; P = 0
        for h, pr in pool.imap_unordered(work, [(text, p, t) for p, t in fam], chunksize=200):
            H += h; P += pr
    print(f"{label}: {len(fam)} transpositions x 20 periods x 2 orientations x 2 layer orders; prefilter survivors {P}; SAT-consistent {len(H)} {H[:10]}", flush=True)
    return H
if __name__ == "__main__":
    fam = family(97)
    if len(sys.argv) > 1: fam = fam[:int(sys.argv[1])]
    out = {"K4": run(K4, "K4", fam)}
    rng = random.Random(2121)
    for r in range(3):
        l = list(K4); rng.shuffle(l); out[f"null{r}"] = run("".join(l), f"shuffled-K4 null {r}", fam)
    # planted controls: Trifid then a transposition from the family (order A) and transposition then Trifid (order B)
    pt = list("X" * 97); filler = list("THEWALLFELLINTHENIGHTANDWEWALKEDTOWARDTHESQUAREUNDERTHEOLDWORLDCLOCKWHEREPEOPLESANGANDCRIEDLOUDLY" * 2)
    for i in range(97): pt[i] = filler.pop(0) if i not in CRIB else CRIB[i]
    pt = "".join(pt)
    for seed, (order, p) in enumerate((("A", 7), ("B", 5), ("A", 13))):
        cube = list(SYM); rng.shuffle(cube); idx = rng.randrange(len(fam)); perm, tag = fam[idx]
        inv = [0] * 97
        for j, v in enumerate(perm): inv[int(v)] = j
        if order == "A":
            mid = trifid_enc(pt, cube, p); ct = "".join(mid[inv[k]] for k in range(97))  # so that ct[perm] == mid
        else:
            tp = "".join(pt[int(perm[j])] for j in range(97)); ct = trifid_enc(tp, cube, p)
        h, _ = work((ct, perm, tag))
        hit = any(x[1] == order and x[2] == p and x[3] == 0 for x in h)
        print(f"planted control order {order} period {p} transposition {tag}: recovered={hit}; consistent combos at the true transposition {h}", flush=True)
        out[f"control{seed}"] = {"order": order, "p": p, "tag": tag, "hits": h, "recovered": hit}
    json.dump(out, open("../analysis/trifid_trans_results.json", "w"), indent=1)
