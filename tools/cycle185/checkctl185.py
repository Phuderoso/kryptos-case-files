"""Cycle 185 control check (single path: method 1, A = B list = vocabulary; audit build on q-2..q+3): positives = planted (A, B, form, L) fit at the planted q in the planted direction's run, with wild slot =
the planted error slot (t -1 for the strict plant P5) and no other slot for that configuration, the planted (c, d) mod 2 and mod 13
listed, and a string-level replay equal to the planted plaintext except at the mis-carved position; negatives = no fit at the planted
q in either direction (any pair, form, L, slot). Also: no X line, END present, and the SAFE audit build gives identical H lines on its
(narrower) window as the main build on the same rows (w20 runs), and the same set of fitting (L, form, q, A, B, slot); the M
line text differs by design (block-2 slots: one V -2 line in the main build, one line per wildcard value in the audit build).
usage: checkctl185.py plants.json outdir all.bin quadgrams.json alphafiles"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode185 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4]); D.load_alpha(sys.argv[5])
CI = list(range(21, 34)) + list(range(63, 74))
def rd(fn):
    txt = open(fn).read().strip().split("\n"); return txt, txt[-1].startswith("END"), [l.split() for l in txt if l.startswith("M ")], [l for l in txt if l.startswith("X ")]
ok_all = 0
for p in pl:
    runs = {d: rd(f"{od}/{p['name']}.{d}.txt") for d in ("r",)}; saf = {d: rd(f"{od}/{p['name']}.{d}.safe.txt") for d in ("r",)}
    w20 = {d: rd(f"{od}/{p['name']}.{d}.w20.txt") for d in ("r",)}   # same rows (q-2..q+3), main build; compare H lines and the set of (L, form, q, A, B, slot)
    same = all({tuple(a[1:11]) for a in saf[d][2]} == {tuple(a[1:11]) for a in w20[d][2]} and
               [l for l in saf[d][0] if l.startswith("H ")] == [l for l in w20[d][0] if l.startswith("H ")] for d in ("r",))
    end = all(v[1] for v in runs.values()) and all(v[1] for v in saf.values()) and same; mism = sum(len(v[3]) for v in list(runs.values()) + list(saf.values()))
    atq = {d: [a for a in runs[d][2] if int(a[6]) == p["q"]] for d in runs}
    if p["kind"] == "neg":
        ok = end and not atq["r"] and not mism
        print(f"{p['name']}: NEG fits_at_q {len(atq['r'])} safe_same {same} -> {'PASS' if ok else 'FAIL'}"); ok_all += ok; continue
    want = CI.index(p["err"][0]) if p["err"] else -1
    cfg = [a for a in atq[p["dir"]] if int(a[3]) == p["L"] and a[5] == p["form"] and a[7] == p["alab"] and a[8] == p["blab"]]
    slots = sorted({int(a[10]) for a in cfg}); found = dec_ok = False; best = None
    for a in cfg:
        if int(a[10]) != want: continue
        i2, i13 = a.index("S2"), a.index("S13"); x = p["c"] + [p["d"]]
        s2 = [list(map(int, t.split(",")))[:p["L"] + 1] for t in a[i2 + 1:i13]]; s13 = [list(map(int, t.split(",")))[:p["L"] + 1] for t in a[i13 + 1:]]
        found |= ([v % 2 for v in x] in s2 or int(a[16]) > 8) and ([v % 13 for v in x] in s13 or int(a[18]) > 8)
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(u == "?" or u == v or i in p["err"] for i, (u, v) in enumerate(zip(pt, p["pt"]))): dec_ok = True; best = (s, pt, par); break
    ok = end and found and dec_ok and not mism and slots == [want]; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq[p['dir']])} slots {slots} want {want} planted_params_listed {found} decode_matches_plant {dec_ok} safe_same {same} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} {best[2]} {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
