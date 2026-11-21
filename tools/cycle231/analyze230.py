#!/usr/bin/env python3
"""Cycle 230 analysis (PREREG230): gate P (plants), recount R, K4 / null tables, cluster rule, beam decode of survivors.
usage (from w/): analyze230.py"""
import sys, re, struct, glob, json, math, collections
import numpy as np
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CRP = list(range(21, 34)) + list(range(63, 74)); CRS = "EASTNORTHEASTBERLINCLOCK"; CRSET = set(CRP)
QG = np.fromfile("qg.bin", dtype=np.float32); assert QG.size == 26**4
def alph(fn):
    b = open(fn, "rb").read(); return [list(b[i:i+26]) for i in range(0, len(b), 26)]
ALPHA = alph("alpha.bin"); THEMED = alph("themed144.bin")
def row(fn, q):
    with open(fn, "rb") as f: f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
def wilson(k, n, z=1.959964):
    ph = k / n; d = 1 + z*z/n; c = (ph + z*z/(2*n))/d; hw = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n))/d
    return (round(max(0, c-hw), 3), round(min(1, c+hw), 3))
LINE = re.compile(r"S perm=(-?\d+) dir=(\d+) X=(\d+) Y=(\d+) form=(\d) w=(\d+) pop=(\d+) k=([A-Z]+)")
def parse(fn):
    out = []; T = None
    for l in open(fn):
        m = LINE.match(l)
        if m: out.append(tuple(int(m.group(i)) for i in range(1, 8)) + (m.group(8),))
        elif l.startswith("T "): T = int(re.search(r"survivors=(\d+)", l).group(1))
    return out, T
def kvals(ct, fam, q, d, xi, yi, form, tabs, off=0):
    """24 crib shifts, independent re-derivation."""
    if fam == "direct": S = list(range(97))
    else:
        P = row(fam + ".bin", q + off); S = P if d == 0 else [P.index(i) for i in range(97)]
    X, Y = tabs[xi], tabs[yi]; xinv = {v: i for i, v in enumerate(X)}; yinv = {v: i for i, v in enumerate(Y)}
    ks = []
    for t, i in enumerate(CRP):
        x = xinv[ord(CRS[t]) - 65]; y = yinv[ord(ct[S[i]]) - 65]
        ks.append((y - x) % 26 if form == 0 else (x - y) % 26 if form == 1 else (y + x) % 26)
    return ks, S, X, Y
def width_pop(ks):
    s = sorted(set(ks)); n = len(s); best = 26
    for a in range(n):  # minimal circular arc covering the set
        gap_end = s[a - 1]; w = (gap_end - s[a]) % 26 + 1; best = min(best, w)
    return best, len(s)
def decrypt_with(ct, S, X, Y, form, k, i):
    yv = Y.index(ord(ct[S[i]]) - 65)
    x = (yv - k) % 26 if form == 0 else (yv + k) % 26 if form == 1 else (k - yv) % 26
    return X[x]
def beam(ct, S, X, Y, form, kset, B=3000):
    cand = []
    for i in range(97):
        if i in CRSET: cand.append([CRS[CRP.index(i)]])
        else: cand.append(sorted({chr(65 + decrypt_with(ct, S, X, Y, form, k, i)) for k in kset}))
    beams = [("", 0.0)]
    for i in range(97):
        nb = []
        for s, sc in beams:
            for ch in cand[i]:
                ns = s + ch; add = 0.0
                if i >= 3 and not (CRSET & {i-3, i-2, i-1, i}):
                    a = ns[-4:]; add = float(QG[((ord(a[0])-65)*26 + ord(a[1])-65)*676 + (ord(a[2])-65)*26 + ord(a[3])-65])
                nb.append((ns, sc + add))
        nb.sort(key=lambda t: -t[1]); beams = nb[:B]
    s, sc = beams[0]; nq = sum(1 for i in range(3, 97) if not (CRSET & {i-3, i-2, i-1, i}))
    return s, sc / nq
def ncmean(P):
    q = [float(QG[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65]) for i in range(94) if not (CRSET & {i, i+1, i+2, i+3})]
    return sum(q) / len(q)
def kset_of(ks, w):
    s = sorted(set(ks))
    if w is None: return s
    # minimal arc covering
    best = None
    for a in range(len(s)):
        st = s[a]; ww = (s[a-1] - st) % 26 + 1
        if best is None or ww < best[0]: best = (ww, st)
    return [(best[1] + t) % 26 for t in range(best[0])]
def decode_line(ct, fam, line, tabs, off=0, crit="W"):
    q, d, xi, yi, form, w, pop, kl = line
    ks, S, X, Y = kvals(ct, fam, q, d, xi, yi, form, tabs, off)
    assert width_pop(ks) == (w, pop), "recount mismatch"
    ksn = [ord(c) - 65 for c in kl]; assert ksn == ks
    ks_set = kset_of(ks, w) if (w <= 9 and crit == "W") else sorted(set(ks))
    return beam(ct, S, X, Y, form, ks_set)

def gate_P():
    rows = [l.rstrip("\n").split("\t") for l in open("plants230.tsv")]
    ok = 0; res = []
    for pid, fam, q, d, xi, yi, form, typ, size, ct, pt in rows:
        q, d, xi, yi, form = int(q), int(d), int(xi), int(yi), int(form)
        lines, T = parse(f"P/{pid}.txt")
        off = int(open(f"P/{pid}.off").read()) if fam != "direct" else 0
        truth = (q - off if fam != "direct" else -1, d, xi, yi, form)
        found = [l for l in lines if l[:5] == truth]
        # also accept same (X,Y,form) with another row/dir having the identical crib key string (inverse twin / equivalent row)
        tabs = ALPHA if fam == "direct" else THEMED
        rec = bool(found)
        dec = None
        if found:
            tx = pt; l = found[0]
            fm = "bank" if fam == "bank" else "all" if fam == "all" else "direct"
            # beam decode (window arcs for 'w', observed set for 'd')
            ks, S, X, Y = kvals(ct, fm, l[0], l[1], l[2], l[3], l[4], tabs, off)
            kset = kset_of(ks, l[5]) if typ == "w" else sorted(set(ks))
            bs, sc = beam(ct, S, X, Y, l[4], kset)
            true_sc = ncmean(pt); same = sum(1 for i in range(97) if i not in CRSET and bs[i] == pt[i]) / 73
            dec = (round(sc, 3), round(true_sc, 3), round(same, 3), same >= 0.9 or sc >= true_sc - 1e-9)
        res.append((pid, fam, typ, size, rec, len(lines), T, dec)); ok += rec
        print("PLANT", pid, fam, typ, size, "found" if rec else "MISSED", "survivor lines", len(lines), "T", T, "decode", dec)
    n = len(rows); dr = sum(1 for r in res if r[7] and r[7][3])
    print(f"GATE P recovered {ok}/{n} Wilson {wilson(ok, n)} (pass >= 19/20); decode-read {dr}/{ok}")
def table():
    nulls = [l.strip() for l in open("nulls230.txt")]; k4 = open("k4.txt").read().strip()
    print("scope crit  K4 | null counts (1/20 scale) | null-equivalent")
    for sc in ("direct", "bank", "all"):
        k4l, k4T = parse(f"R/k4_{sc}.txt")
        def cnt(lines, crit): return sum(1 for l in lines if (l[5] <= 9 if crit == "W9" else l[5] <= 10 if crit == "W10" else l[5] <= 8 if crit == "W8" else l[6] <= 6 if crit == "D6" else l[6] <= 5))
        for crit in ("W8", "W9", "W10", "D5", "D6"):
            nc_ = [cnt(parse(f"R/null{i}_{sc}.txt")[0], crit) for i in range(10)]
            print(sc, crit, "K4", cnt(k4l, crit), "| nulls", nc_, "| sum*20/10 per-null-equiv", round(sum(nc_) * 20 / 10, 1))
        print(sc, "K4 T", k4T, "nullT", [parse(f"R/null{i}_{sc}.txt")[1] for i in range(10)])
if __name__ == "__main__":
    gate_P(); table()
