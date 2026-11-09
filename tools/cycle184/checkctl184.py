"""Cycle 184 control check: positives = planted (A, B, form, L) fit at the planted q in the method-1 run, with the planted (c, d)
mod 2 and mod 13 listed and a string-level replay equal to the planted plaintext; negatives = no fit at the planted q (any pair, form,
L). Also: no X line, END present, method 0 H lines == method 1 H lines (q +- 200), audit build (method 2, -DSAFE=1) H lines == method 1
on q-2..q+3.   usage: checkctl184.py plants.json outdir all.bin quadgrams.json alphafile"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode184 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4]); D.load_alpha(sys.argv[5])
def rd(fn):
    txt = open(fn).read().strip().split("\n"); return txt, txt[-1].startswith("END"), [l.split() for l in txt if l.startswith("M ")], [l for l in txt if l.startswith("X ")]
H = lambda r: [l for l in r[0] if l.startswith("H ")]
ok_all = 0
for p in pl:
    m1, m0, m1n, sf = (rd(f"{od}/{p['name']}.{k}.txt") for k in ("m1", "m0", "m1n", "safe"))
    same = H(m1) == H(m0) and H(m1n) == H(sf); end = all(r[1] for r in (m1, m0, m1n, sf)); mism = sum(len(r[3]) for r in (m1, m0, m1n, sf))
    atq = [a for a in m1[2] if int(a[6]) == p["q"]]; atq0 = [a for a in m0[2] if int(a[6]) == p["q"]]
    if p["kind"] == "neg":
        ok = end and same and not atq and not atq0 and not mism
        print(f"{p['name']}: NEG fits_at_q m1 {len(atq)} m0 {len(atq0)} H_same(m0,safe) {same} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    found = dec_ok = False; best = None
    for a in atq:
        if int(a[3]) != p["L"] or a[5] != p["form"] or a[7] != p["alab"] or a[8] != p["blab"]: continue
        i2, i13 = a.index("S2"), a.index("S13"); x = p["c"] + [p["d"]]
        s2 = [list(map(int, t.split(","))) for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(","))) for t in a[i13 + 1:]]
        found |= ([v % 2 for v in x] in s2 or int(a[10]) > 32) and ([v % 13 for v in x] in s13 or int(a[12]) > 32)
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(u == "?" or u == v for u, v in zip(pt, p["pt"])): dec_ok = True; best = (s, pt, par); break
    ok = end and same and found and dec_ok and not mism; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} planted_params_listed {found} decode_matches_plant {dec_ok} H_same(m0,safe) {same} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} {best[2]} {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
