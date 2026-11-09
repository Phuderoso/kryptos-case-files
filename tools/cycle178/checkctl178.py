"""Cycle 178 control check: planted parameters among the listed solutions at the planted q, replayed decode == planted plaintext,
negatives missed at their planted q. usage: checkctl178.py plants.json outdir all.bin quadgrams.json"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode178 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4])
ok_all = 0
for p in pl:
    lines = [l.split() for l in open(f"{od}/{p['name']}.txt") if l.startswith("M ")]
    end = open(f"{od}/{p['name']}.txt").read().strip().split("\n")[-1].startswith("END")
    atq = [a for a in lines if int(a[6]) == p["q"]]
    if p["kind"] == "neg":
        ok = end and not atq; print(f"{p['name']}: NEG fits_at_q {len(atq)} fits_in_window {len(lines)} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    L = p["L"]; found = False; dec_ok = False; best = None
    for a in atq:
        if p["mode"] == 0:
            if int(a[3]) != L or a[4] != p["pa"] or a[5] != p["form"]: continue
            i2, i13 = a.index("S2"), a.index("S13"); x = p["c"] + [p["d"]]
            s2 = [list(map(int, t.split(","))) for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(","))) for t in a[i13 + 1:]]
            found |= ([v % 2 for v in x] in s2 or int(a[8]) > 32) and ([v % 13 for v in x] in s13 or int(a[10]) > 32)
        elif p["mode"] == 1:
            if int(a[3]) != L or a[4] != p["pa"] or a[5] != p["form"]: continue
            i2, i13 = a.index("S2"), a.index("S13")
            tok2 = "c" + "".join(str(v % 2) for v in p["c"]) + "s" + "".join(str(v % 2) for v in p["seed"]) + "d" + str(p["d"] % 2)
            c13 = ",".join(str(v % 13) for v in p["c"])
            found |= (tok2 in a[i2 + 1:i13] or int(a[8]) > 32) and (any(t[1:].split("x")[0] == c13 for t in a[i13 + 1:]) or int(a[10]) > 32)
        else:
            cm = sum(v << j for j, v in enumerate(p["c"]))
            found |= int(a[3]) == L and a[4] == p["pa"] and a[5] == p["form"] and a[7] == p["word"] and a[8] == p["nb"] and a[9] == f"c{cm}" and a[10] == f"d{p['d']}"
        r = D.decode_line(p["ct"], P, a)
        for s, pt, par in r:
            if all(x == "?" or x == y for x, y in zip(pt, p["pt"])):
                dec_ok = True; best = (s, pt, par, a[2], a[3]); break
    ok = end and found and dec_ok; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} window_fits {len(lines)} planted_params_listed {found} decode_matches_plant {dec_ok} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} [{best[3]} L{best[4]} {best[2]}] {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
