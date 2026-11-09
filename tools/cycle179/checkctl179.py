"""Cycle 179 control check: positives must be found at the planted q, with the planted error slot among the fitting slots
(strict plants: reported as strict), and a replayed decode equal to the planted plaintext on every determined position except
the mis-carved letters; negatives must be missed at the planted q.  usage: checkctl179.py plants.json outdir all.bin quadgrams.json"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import decode179 as D
pl = json.load(open(sys.argv[1])); od = sys.argv[2]; P = np.fromfile(sys.argv[3], dtype=np.int16).reshape(-1, 97); D.load_qg(sys.argv[4])
ok_all = 0
for p in pl:
    txt = open(f"{od}/{p['name']}.txt").read().strip().split("\n"); end = txt[-1].startswith("END")
    lines = [l.split() for l in txt if l.startswith("M ")]; atq = [a for a in lines if int(a[6]) == p["q"]]
    if p["kind"] == "neg":
        ok = end and not atq; ok_all += ok
        print(f"{p['name']}: NEG fits_at_q {len(atq)} (L {sorted(set(int(a[3]) for a in atq))}) window_fits {len(lines)} -> {'PASS' if ok else 'FAIL'}"); continue
    L = p["L"]; mine = [a for a in atq if int(a[3]) == L and a[4] == p["pa"] and a[5] == p["form"]]
    slots = sorted(set(int(a[10]) for a in mine))
    strict = [l for l in txt if l.startswith(f"H ") and l.split()[3] == str(L) and l.split()[4] == p["pa"] and l.split()[5] == p["form"]]
    slot_ok = (p["errs"][0] in slots) if p["errs"] else (len(slots) == 24)    # strict fit -> every slot fits
    dec_ok = False; best = None; bad = set(p["errs"])
    for a in mine:
        for s, pt, par in D.decode_line(p["ct"], P, a):
            if all(x == "?" or x == y or i in bad for i, (x, y) in enumerate(zip(pt, p["pt"]))) and sum(x != "?" for x in pt) >= 76:
                dec_ok = True; best = (s, pt, par); break
        if dec_ok: break
    ok = end and bool(mine) and slot_ok and dec_ok; ok_all += ok
    print(f"{p['name']}: fits_at_q {len(atq)} cell_lines {len(mine)} slots {slots[:6]}{'...' if len(slots) > 6 else ''} planted_slot_ok {slot_ok} decode_matches {dec_ok} -> {'PASS' if ok else 'FAIL'}")
    if best: print(f"   decode score {best[0]:.3f} [{best[2]}] {best[1]}")
print(f"controls {ok_all}/{len(pl)}")
