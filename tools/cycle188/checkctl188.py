"""Cycle 188 control check: positives = planted (A, B, form, L) fit at the planted q in the main run of the plant's direction with the
planted free slot t (t = -1 for the error-free plant), planted c mod 2 and mod 13 listed, and the independent decode (decode188.py)
reproduces the planted plaintext on every position except the erroneous slot's; negatives = no fit at the planted q in either
direction. Also: no X line, END present, audit build (method 2, -DSAFE=1) H lines == main on q-2..q+3.
usage: checkctl188.py plants.json outdir all.bin alpha172.txt alpha_themed180.txt"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode188 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_alpha(sys.argv[4], sys.argv[5])
CI = D.CI
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
    found = dec = False; best = None; ex = CI[p["t"]] if p["t"] >= 0 else -1
    for a in atq:
        if int(a[3]) != p["L"] or a[5] != p["form"] or a[7] != p["alab"] or a[8] != p["blab"] or int(a[10]) != p["t"]: continue
        L, t, s2, s13 = D.parse(a)
        f2 = ([v % 2 for v in p["c"]], p["d"] % 2) in [(c, d) for c, s, d in s2] or int(a[14]) > 32
        f13 = [v % 13 for v in p["c"]] in [c for c, s, d, n in s13] or int(a[16]) > 32
        found |= f2 and f13
        for c, d, sd, tt, pt in D.decode_line(p["ct"], P, a):
            if all(pt[i] == p["pt"][i] for i in range(97) if i != ex): dec = True; best = (c, d, sd, tt, pt)
    ok = good and found and dec; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} slot {p['t']} planted_params_listed {found} decode_matches_plant {dec} END/X/safe ok {good} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decoded c {best[0]} d {best[1]} seed {best[2]} t {best[3]} {best[4]}")
print(f"controls {ok_all}/{len(pl)}")
