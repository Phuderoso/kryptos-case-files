"""Cycle 182 control check: positives = planted (A, B, form, L) fit at the planted q in the planted direction's run, with the planted
(c, d) mod 2 and mod 13 listed and a string-level replay equal to the planted plaintext; negatives = no fit at the planted q in either
direction (any pair, form, L). Also: no X line, END present, and the SAFE/method-2 audit run gives identical H lines.
usage: checkctl182.py plants.json outdir all.bin quadgrams.json alphafiles"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode182 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4]); D.load_alpha(sys.argv[5])
def rd(fn):
    txt = open(fn).read().strip().split("\n"); return txt, txt[-1].startswith("END"), [l.split() for l in txt if l.startswith("M ")], [l for l in txt if l.startswith("X ")]
ok_all = 0
for p in pl:
    runs = {d: rd(f"{od}/{p['name']}.{d}.txt") for d in ("f", "r")}
    same = all([l for l in runs[d][0] if l.startswith("H ")] == [l for l in rd(f"{od}/{p['name']}.{d}.safe.txt")[0] if l.startswith("H ")] for d in ("f", "r"))
    end = all(v[1] for v in runs.values()) and same; mism = sum(len(v[3]) for v in runs.values())
    atq = {d: [a for a in runs[d][2] if int(a[6]) == p["q"]] for d in runs}
    if p["kind"] == "neg":
        ok = end and not atq["f"] and not atq["r"] and not mism
        print(f"{p['name']}: NEG fits_at_q f {len(atq['f'])} r {len(atq['r'])} safe_H_same {same} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    found = dec_ok = False; best = None
    for a in atq[p["dir"]]:
        if int(a[3]) != p["L"] or a[5] != p["form"] or a[7] != p["alab"] or a[8] != p["blab"]: continue
        i2, i13 = a.index("S2"), a.index("S13"); x = p["c"] + [p["d"]]
        s2 = [list(map(int, t.split(","))) for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(","))) for t in a[i13 + 1:]]
        found |= ([v % 2 for v in x] in s2 or int(a[10]) > 32) and ([v % 13 for v in x] in s13 or int(a[12]) > 32)
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(u == "?" or u == v for u, v in zip(pt, p["pt"])): dec_ok = True; best = (s, pt, par); break
    ok = end and found and dec_ok and not mism; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq[p['dir']])} (other dir {len(atq['r' if p['dir'] == 'f' else 'f'])}) planted_params_listed {found} decode_matches_plant {dec_ok} safe_H_same {same} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} {best[2]} {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
