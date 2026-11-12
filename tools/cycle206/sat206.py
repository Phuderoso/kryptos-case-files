#!/usr/bin/env python3
"""Cycle 206 Part B (PREREG206): word-restart key R1 with two alphabets, direct, by SAT.
Models: QI (plain alphabet X unknown, cipher Y = A-Z), QII (X = A-Z, Y unknown), QIV (X, Y unknown, independent).
Vigenere form c = Y[x(p) + s_k], Beaufort form c = Y[s_k - x(p)]; k = R1 class (case 190 segmentations, offsets 0..L-1).
Only the partition of the 24 crib letters into key classes matters (each class has its own free shift), so configurations are
deduplicated by canonical partition and cached across L. Usage: sat206.py [nnulls] [walltime_s]"""
import sys, json, time, random
from pysat.solvers import Glucose4
from pysat.card import CardEnc
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
K4 = open(__file__.rsplit('/', 3)[0] + "/data/k4.txt").read().split()[0].strip()
CRIBS = [(21, "EASTNORTHEAST"), (63, "BERLINCLOCK")]
SEG_E = {"EASTNORTHEAST": [], "EAST|NORTHEAST": [4], "EASTNORTH|EAST": [9], "EAST|NORTH|EAST": [4, 9]}
SEG_B = {"BERLINCLOCK": [], "BERLIN|CLOCK": [6]}

def classes(crib, bnds, o, L):
    out = []
    for j in range(len(crib)):
        prev = [b for b in bnds if b <= j]
        out.append(((j - prev[-1]) if prev else (o + j)) % L)
    return out

def canon(cls):
    m = {}; return tuple(m.setdefault(c, len(m)) for c in cls)

def solve(pairs, model, form):
    """pairs: (cipher idx, plain idx, class). True iff some alphabets + shifts fit."""
    X = lambda l, a: 1 + l * 26 + a            # plain alphabet: letter l at position a
    Y = lambda l, a: 677 + l * 26 + a          # cipher alphabet
    ncls = max(k for _, _, k in pairs) + 1
    S = lambda k, s: 1353 + k * 26 + s
    top = 1353 + ncls * 26
    cl = []
    def perm(V):
        nonlocal top, cl
        for l in range(26):
            e = CardEnc.equals([V(l, a) for a in range(26)], 1, top_id=top); top = max(top, e.nv); cl += e.clauses
        for a in range(26):
            e = CardEnc.equals([V(l, a) for l in range(26)], 1, top_id=top); top = max(top, e.nv); cl += e.clauses
    freeX, freeY = model in ("QI", "QIV"), model in ("QII", "QIV")
    if freeX: perm(X); cl.append([X(0, 0)])            # rotation symmetry absorbed by the shifts
    else: cl += [[X(l, a) if l == a else -X(l, a)] for l in range(26) for a in range(26)]   # fixed A-Z, every cell pinned
    if freeY:
        perm(Y)
        if not freeX: cl.append([Y(0, 0)])
    else: cl += [[Y(l, a) if l == a else -Y(l, a)] for l in range(26) for a in range(26)]
    for k in sorted(set(k for _, _, k in pairs)):
        e = CardEnc.equals([S(k, s) for s in range(26)], 1, top_id=top); top = max(top, e.nv); cl += e.clauses
    for c, p, k in pairs:
        for s in range(26):
            for a in range(26):
                b = (a + s) % 26 if form == "vig" else (s - a) % 26
                cl.append([-X(p, a), -S(k, s), Y(c, b)])
    with Glucose4(bootstrap_with=cl) as g:
        return g.solve()

def partitions(L):
    seen = {}
    for sE, bE in SEG_E.items():
        for sB, bB in SEG_B.items():
            for o1 in range(L):
                for o2 in range(L):
                    cls = classes(CRIBS[0][1], bE, o1, L) + classes(CRIBS[1][1], bB, o2, L)
                    seen.setdefault(canon(cls), (sE, sB, o1, o2))
    return seen

def first_sat(ct, model, form, Lmax, cache, deadline):
    cp = [(AZ.index(ct[CRIBS[0][0] + j]), AZ.index(CRIBS[0][1][j])) for j in range(13)] + \
         [(AZ.index(ct[CRIBS[1][0] + j]), AZ.index(CRIBS[1][1][j])) for j in range(11)]
    log = {}
    for L in range(1, Lmax + 1):
        parts = partitions(L); hit = None; n = 0
        for pt, cfg in parts.items():
            if time.time() > deadline: log[L] = f"STOPPED (budget) after {n}/{len(parts)} partitions"; return None, log
            if pt not in cache: cache[pt] = solve([(c, p, k) for (c, p), k in zip(cp, pt)], model, form)
            n += 1
            if cache[pt]: hit = cfg; break
        log[L] = {"partitions": len(parts), "SAT": hit}
        if hit: return L, log
    return None, log

if __name__ == "__main__":
    nn = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    wall = float(sys.argv[2]) if len(sys.argv) > 2 else 240
    t0 = time.time(); res = {}
    # controls C2 (QIV, random X, Y) and C2b (QII), key shifts L 8, invented text, true configuration must be SAT
    rng = random.Random(2062)
    W = ["AND", "THE", "GREY", "LIGHT", "TURNED", "EAST", "NORTHEAST", "OVER", "THE", "WALL", "AND", "A", "MAN", "STOOD", "BY", "THAT",
         "BERLIN", "CLOCK", "WAITING", "FOR", "THE", "SIGNAL"]
    key = [3, 17, 5, 11, 0, 9, 22, 14]
    for name, model in (("C2", "QIV"), ("C2b", "QII"), ("C2c", "QI")):
        Xa = list(AZ); Ya = list(AZ)
        if model in ("QIV", "QI"): rng.shuffle(Xa)
        if model in ("QIV", "QII"): rng.shuffle(Ya)
        c = ""
        for w in W:
            for j, p in enumerate(w): c += Ya[(Xa.index(p) + key[j % 8]) % 26]
        k1 = classes("EASTNORTHEAST", [4], 0, 8); k2 = classes("BERLINCLOCK", [6], 0, 8)
        pairs = [(AZ.index(c[21 + j]), AZ.index("EASTNORTHEAST"[j]), k) for j, k in enumerate(k1)] + \
                [(AZ.index(c[63 + j]), AZ.index("BERLINCLOCK"[j]), k) for j, k in enumerate(k2)]
        res[name] = solve(pairs, model, "vig"); print(name, model, "true config SAT:", res[name], flush=True)
    # gate G-mono: at L = 1 every model is a monoalphabetic map and K4's crib has N->Q and O->Q, so L = 1 must be UNSAT
    pt1 = tuple([0] * 24)
    cp = [(AZ.index(K4[21 + j]), AZ.index("EASTNORTHEAST"[j])) for j in range(13)] + [(AZ.index(K4[63 + j]), AZ.index("BERLINCLOCK"[j])) for j in range(11)]
    res["G_mono_L1_UNSAT"] = {m + "_" + f: not solve([(c, p, 0) for c, p in cp], m, f) for m in ("QI", "QII", "QIV") for f in ("vig", "beau")}
    print("G-mono", res["G_mono_L1_UNSAT"], flush=True)
    assert res["C2"] and res["C2b"] and res["C2c"] and all(res["G_mono_L1_UNSAT"].values()), "controls/gates failed"
    deadline = t0 + wall
    for model in ("QI", "QII", "QIV"):
        for form in ("vig", "beau"):
            cache = {}
            L, log = first_sat(K4, model, form, 13, cache, deadline)
            res[f"K4_{model}_{form}"] = {"first_SAT_L": L, "log": log}
            print("K4", model, form, "first SAT L =", L, {k: (v if isinstance(v, str) else (v['partitions'], bool(v['SAT']))) for k, v in log.items()}, round(time.time() - t0, 1), flush=True)
    rng = random.Random(206207)
    nulls = [rng.sample(K4, 97) for _ in range(nn)]
    for model in ("QI", "QII", "QIV"):
        for form in ("vig", "beau"):
            out = []
            for sh in nulls:
                L, log = first_sat("".join(sh), model, form, 13, {}, deadline)
                out.append(L if L else ("stopped" if any(isinstance(v, str) for v in log.values()) else ">13"))
            res[f"null_{model}_{form}"] = out
            print("null", model, form, out, round(time.time() - t0, 1), flush=True)
    res["seconds"] = round(time.time() - t0, 1)
    json.dump(res, open("results206_sat.json", "w"), indent=1, default=str)
