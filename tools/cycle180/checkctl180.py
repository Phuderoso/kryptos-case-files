"""Cycle 180 control check: planted alphabet/type/form/L fit at the planted q with the planted (c mod 2, c mod 13 [, d]) listed,
string-level replay == planted plaintext; negatives: no fit at the planted q (any alphabet, type, form, L).
usage: checkctl180.py plants.json outdir all.bin quadgrams.json alphafile"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode180 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4]); D.load_alpha(sys.argv[5])
ok_all = 0
for p in pl:
    txt = open(f"{od}/{p['name']}.txt").read().strip().split("\n"); end = txt[-1].startswith("END")
    lines = [l.split() for l in txt if l.startswith("M ")]; atq = [a for a in lines if int(a[6]) == p["q"]]
    mism = [l for l in txt if l.startswith("X ")]
    if p["kind"] == "neg":
        ok = end and not atq and not mism
        print(f"{p['name']}: NEG fits_at_q {len(atq)} window_fits {len(lines)} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    found = dec_ok = False; best = None
    for a in atq:
        if int(a[3]) != p["L"] or a[4] != p["ty"] or a[5] != p["form"] or a[7] != p["alab"]: continue
        i2, i13 = a.index("S2"), a.index("S13")
        if p["ix"] == 0:
            x = p["c"] + [p["d"]]; s2 = [list(map(int, t.split(","))) for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(","))) for t in a[i13 + 1:]]
            found |= ([v % 2 for v in x] in s2 or int(a[10]) > 32) and ([v % 13 for v in x] in s13 or int(a[12]) > 32)
        else:
            tok2 = "c" + "".join(str(v % 2) for v in p["c"]) + "s" + "".join(str(v % 2) for v in p["seed"]) + "d" + str(p["d"] % 2)
            c13 = ",".join(str(v % 13) for v in p["c"])
            found |= (tok2 in a[i2 + 1:i13] or int(a[10]) > 32) and (any(t[1:].split("x")[0] == c13 for t in a[i13 + 1:]) or int(a[12]) > 32)
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(x == "?" or x == y for x, y in zip(pt, p["pt"])): dec_ok = True; best = (s, pt, par); break
    ok = end and found and dec_ok and not mism; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} window_fits {len(lines)} planted_params_listed {found} decode_matches_plant {dec_ok} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} {best[2]} {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
