"""Cycle 181 control check. Positives: a fit at the planted q with the planted alphabet/type/form/L whose wild slot is the planted
error slot (strict plants: a strict line, t -1), the planted (c, d) mod 2 / mod 13 listed (M0; M1: replay only, one stream is
printed), and the string-level replay equal to the planted plaintext at every position whose carved letter was not changed;
no other slot fits at q with the planted alphabet/type/form/L (strict plants excepted). Negatives: no fit at q (any alphabet,
type, form, L, slot). usage: checkctl181.py plants.json outdir all.bin quadgrams.json alphafile"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode181 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4]); D.load_alpha(sys.argv[5])
ok_all = 0
for p in pl:
    txt = open(f"{od}/{p['name']}.txt").read().strip().split("\n"); end = txt[-1].startswith("END")
    lines = [l.split() for l in txt if l.startswith("M ")]; atq = [a for a in lines if int(a[6]) == p["q"]]
    bad = [l for l in txt if l.startswith("X ") or (l.startswith("O ") and l.split()[3] != "0")]
    if p["kind"] == "neg":
        ok = end and not atq and not bad
        print(f"{p['name']}: NEG fits_at_q {len(atq)} window_fits {len(lines)} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    want = p["err"][0] if p["err"] else -1; found = dec_ok = False; best = None; slots = set()
    for a in atq:
        if int(a[3]) != p["L"] or a[4] != p["ty"] or a[5] != p["form"] or a[7] != p["alab"]: continue
        sl = int(a[a.index("slot") + 1]); slots.add(sl)
        if sl != want: continue
        i2, i13 = a.index("S2"), a.index("S13")
        if p["ix"] == 0:
            x = p["c"] + [p["d"]]; s2 = [list(map(int, t.split(","))) for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(","))) for t in a[i13 + 1:]]
            found |= ([v % 2 for v in x] in s2 or int(a[a.index("n2") + 1]) > 8) and ([v % 13 for v in x] in s13 or int(a[a.index("n13") + 1]) > 8)
        else: found = True
        S = P[p["q"]]; changed = {int(np.where(S == S[i])[0][0]) for i in p["err"]}
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(x == "?" or x == y or i in changed for i, (x, y) in enumerate(zip(pt, p["pt"]))): dec_ok = True; best = (s, pt, par); break
    only = slots == {want}
    ok = end and found and dec_ok and only and not bad; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} window_fits {len(lines)} slots_at_q {sorted(slots)} planted_listed {found} decode_matches {dec_ok} only_planted_slot {only} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} {best[2]} {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
