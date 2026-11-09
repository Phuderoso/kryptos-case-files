"""Cycle 187 control check: positives = planted (A, B, form, L) fit at the planted q in the main run of the plant's direction, planted
(c, d) mod 2 and mod 13 listed, and the independent decode (decode187.py) reproduces the planted plaintext; negatives = no fit at the
planted q in either direction. Also: no X line, END present, audit build (method 2, -DSAFE=1) H lines == main on q-2..q+3.
usage: checkctl187.py plants.json outdir all.bin alpha172.txt alpha_themed180.txt"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode187 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_alpha(sys.argv[4], sys.argv[5])
def rd(fn):
    t = open(fn).read().strip().split("\n"); return t, t[-1].startswith("END"), [l.split() for l in t if l.startswith("M ")], [l for l in t if l.startswith("X ")]
H = lambda r: [l for l in r[0] if l.startswith("H ")]
ok_all = 0
for p in pl:
    dirs = [p["dir"]] if p["kind"] == "pos" else ["f", "r"]; good = True; atq = []
    for dr in dirs:
        m, mn, sf = (rd(f"{od}/{p['name']}.{dr}.{k}.txt") for k in ("m", "mn", "safe"))
        good &= H(mn) == H(sf) and all(r[1] for r in (m, mn, sf)) and not any(r[3] for r in (m, mn, sf))
        atq += [a for a in m[2] if int(a[6]) == p["q"]]
    if p["kind"] == "neg":
        ok = good and not atq; ok_all += ok
        print(f"{p['name']}: NEG fits_at_q {len(atq)} (dirs {','.join(dirs)}) END/X/safe ok {good} -> {'PASS' if ok else 'FAIL'}"); continue
    found = dec = False; best = None
    for a in atq:
        if int(a[3]) != p["L"] or a[5] != p["form"] or a[7] != p["alab"] or a[8] != p["blab"]: continue
        L, s2, s13 = D.parse(a); x = p["c"] + [p["d"]]
        found |= ([v % 2 for v in p["c"]], p["d"] % 2) in [(c, d) for c, s, d in s2] or int(a[10]) > 32
        found &= [v % 13 for v in p["c"]] in [c for c, s, d, n in s13] or int(a[12]) > 32
        for c, d, sd, pt in D.decode_line(p["ct"], P, a):
            if pt == p["pt"]: dec = True; best = (c, d, sd, pt)
    ok = good and found and dec; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} planted_params_listed {found} decode_matches_plant {dec} END/X/safe ok {good} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decoded c {best[0]} d {best[1]} seed {best[2]} {best[3]}")
print(f"controls {ok_all}/{len(pl)}")
