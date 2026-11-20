"""Cycle 226 (PREREG226, I-326 part B): re-read the case 209 (= case 205 p 20 / 21) cells with the non-crib score (NC) and the
English-oracle bar. Inputs: the cycle 223 raw col21 outputs (K4 + 168 nulls), D2-collapsed exactly as analyze223.py.
usage: reread209_226.py W223 qg.bin oracle226.txt REPO OUT.json"""
import sys, glob, json, collections, hashlib
import numpy as np
W, QG, ORA, REPO, OUT = sys.argv[1:6]
sys.path.insert(0, f"{REPO}/tools/cycle219"); sys.path.insert(0, f"{REPO}/tools/cycle223")
from plant219 import reading_order, KA, AZ, CRP, CRS
qg = np.fromfile(QG, dtype=np.float32); ora = open(ORA).read().split()
CRIB = set(range(21, 34)) | set(range(63, 74))
texts = dict(l.rstrip("\n").split("\t") for l in open(f"{W}/texts.tsv"))
def S_of(w, pi, mode, dir_):
    order = reading_order(w, list(pi), mode); sig = [0]*97
    for m, cell in enumerate(order): sig[cell] = m
    if dir_ == 0: return sig
    inv = [0]*97
    for i in range(97): inv[sig[i]] = i
    return inv
def decrypt(ct, h, pi):  # analyze223.decrypt verbatim
    w, mode, dir_, al, be, model, p, e, bad = h; A = AZ if al == 0 else KA; S = S_of(w, pi, mode, dir_)
    cls = lambda i: (i if model == 0 else S[i]) % p
    votes = collections.defaultdict(collections.Counter)
    for t, i in enumerate(CRP):
        c = A.index(ct[S[i]]); x = A.index(CRS[t]); votes[cls(i)][(c + x) % 26 if be else (c - x) % 26] += 1
    key = {r: v.most_common(1)[0][0] for r, v in votes.items()}
    P = []
    for i in range(97):
        r = cls(i)
        if r not in key: P.append("?"); continue
        c = A.index(ct[S[i]]); P.append(A[(key[r] - c) % 26] if be else A[(c - key[r]) % 26])
    return "".join(P)
def nc(mask, t):
    q = [qg[((ord(t[i])-65)*26 + ord(t[i+1])-65)*676 + (ord(t[i+2])-65)*26 + ord(t[i+3])-65] for i in range(94)
         if "?" not in mask[i:i+4] and not (CRIB & {i, i+1, i+2, i+3})]
    return (float(np.mean(q)) if len(q) >= 10 else None), len(q)
def kbin(k): return 0 if k < 49 else 1 + (k - 49) // 8
cells = {}
for lab in texts:
    if not (lab == "K4" or lab.startswith("null")): continue
    seen = {}
    for f in sorted(glob.glob(f"{W}/out/{lab}/*.raw")):
        for line in open(f):
            a = line.split()
            if a[0] != "H": continue
            bar = a.index("|"); v = tuple(int(x) for x in a[2:11]); pi = tuple(int(x) for x in a[11:bar]); j = tuple(int(x) for x in a[bar+1:])
            if v[6] not in (20, 21): continue
            key2 = (v[3], v[4], v[5], v[6], j)
            if key2 in seen: seen[key2]["raw"] += 1; continue
            D = decrypt(texts[lab], v, pi); s, nq = nc(D, D); k = 97 - D.count("?")
            h = int(hashlib.sha256(repr(key2).encode()).hexdigest(), 16) % 16
            o = [nc(D, ora[(h + 4*t) % 16])[0] for t in range(4)]
            seen[key2] = {"p": v[6], "known": k, "kbin": kbin(k), "nc": s, "nqnc": nq, "oracle": o, "raw": 1, "pt": D if lab == "K4" else ""}
    cells[lab] = list(seen.values())
nulls = [l for l in cells if l != "K4"]
res = {"inputs": {"W223": W, "n_nulls": len(nulls)}, "strata": {}, "cells": {}}
for p in (20, 21):
    for kb in range(1, 8):
        O = [x for l in nulls for c in cells[l] if c["p"] == p and c["kbin"] == kb for x in c["oracle"]]
        if not O: continue
        Os = sorted(-99 if x is None else x for x in O); n = len(Os)
        bar = Os[int(0.05 * n)] if n >= 400 and sum(x == -99 for x in Os) <= 0.05 * n else None
        NH = [c for l in nulls for c in cells[l] if c["p"] == p and c["kbin"] == kb]
        fp = (sum(1 for c in NH if c["nc"] is not None and bar is not None and c["nc"] >= bar) / len(NH)) if NH and bar is not None else None
        res["strata"][f"p{p}_k{kb}"] = {"oracle_n": n, "oracle_median": Os[n//2], "bar": bar, "null_cells": len(NH), "null_fp_rate": fp}
for p in (20, 21):
    def passes(c):
        st = res["strata"].get(f"p{p}_k{c['kbin']}"); return bool(c["kbin"] >= 1 and st and st["bar"] is not None and c["nc"] is not None and c["nc"] >= st["bar"])
    def barred(c):
        st = res["strata"].get(f"p{p}_k{c['kbin']}"); return bool(c["kbin"] >= 1 and st and st["bar"] is not None)
    K = [c for c in cells["K4"] if c["p"] == p]; kp = sum(passes(c) for c in K)
    npass = [sum(passes(c) for c in cells[l] if c["p"] == p) for l in nulls]
    ge = sum(x >= kp for x in npass); occ = sum(x > 0 for x in npass)
    top = sorted(K, key=lambda c: -(c["nc"] if c["nc"] is not None else -99))[:5]
    res["cells"][f"p{p}"] = {"K4_D2": len(K), "K4_barred": sum(barred(c) for c in K), "K4_pass": kp, "null_pass_occupancy": f"{occ}/{len(nulls)}",
        "null_pass_max": max(npass), "p_up": round((1 + ge) / (len(nulls) + 1), 4),
        "K4_top": [{k: c[k] for k in ("known", "nqnc", "nc", "oracle", "pt")} for c in top]}
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps({k: v for k, v in res.items() if k != "inputs"}, indent=1)[:6000])
