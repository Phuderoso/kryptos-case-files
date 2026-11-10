"""Cycle 194 control checker (one-error sandwich; adapted from checkctl192/193). Inputs: run/ctl/<name>_t2.txt (cmp194, tab2, all forms) and
<name>_t1.txt (cmp194, one-tableau stacks, forms VV/VB only: BB = VV and BV = VB exactly, I-195 equivalents listed not counted).
Positive Pk (one wrong letter on a 2-core slot s): passes if cmp194 reports a fit at the planted row, model, tableau pair, (reduced) form and
(m, n), AND decode194 with deletion s is CONSISTENT and reproduces the planted plaintext at every determined position except the corrupted
crib position. P0 (no error): fit with slot -1 (strict) and deletion -1 reproduces everything. PD (error on a pendant edge): must fit
STRICTLY (slot -1) and deletion of the pendant slot reproduces the rest; the strict decryption is wrong on the pendant edge's residue
class -> reported as 'undetectable error', the expected outcome, not a miss. A plant whose wrong letter still leaves its component consistent
(a bijection cycle keeps a root value with probability ~1 - 1/e when r = 1) is reported at slot -1 by the solver; it passes if deletion s reproduces.
Negatives: pass if the planted row has no fit with U <= 1e-4 anywhere."""
import sys, subprocess, os
plants, d = sys.argv[1], sys.argv[2]
PTX = "THEIRONDOORFACEDDUEXXEASTNORTHEASTOFTHEFOUNTAINWHERETHEOLDWORLDBERLINCLOCKSTRUCKTHEHOURATMIDNIGHT"
TABS = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
CI = list(range(21, 34)) + list(range(63, 74))
RED = {"VV": "VV", "BB": "VV", "VB": "VB", "BV": "VB"}
npass = tot = 0
for l in open(plants):
    if l.startswith("#"): continue
    name, row, md, exp, slot, ct = l.split(); slot = int(slot); tot += 1
    M = [x.split() for f in ("t2", "t1") for x in open(f"{d}/{name}_{f}.txt") if x.startswith("M ")]
    atrow = [x for x in M if x[2] == row]
    if name.startswith("P"):
        tab, form, m, n = exp.split("_"); one = tab in ("AZ>AZ", "KA>KA"); f2 = RED[form] if one else form
        hit = [x for x in atrow if x[3] == tab and x[4] == f2 and x[5] == md and x[6] == m and x[7] == n]
        good = False; note = ""
        if hit:
            t1, t2 = (TABS[s] for s in tab.split(">")); dd = max(slot, -1)
            out = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "decode194.py"), ct, "support/ctl191.bin", row, md, t1, t2, form, m, n, "200", str(dd)], capture_output=True, text=True).stdout
            bad = {CI[slot]} if slot >= 0 else set()
            for ln in out.splitlines():
                if "PT=" in ln:
                    pt = ln.split("PT=")[1].split()[0]
                    if pt.count("?") < 97 and all(c == "?" or c.upper() == PTX[i] or i in bad for i, c in enumerate(pt)):
                        good = True
                        break
            if name == "PD" and good:   # what the strict decryption (no deletion) shows: the pendant residue is set from the wrong letter
                o2 = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "decode194.py"), ct, "support/ctl191.bin", row, md, t1, t2, form, m, n, "1", "-1"], capture_output=True, text=True).stdout
                pt = [ln.split("PT=")[1].split()[0] for ln in o2.splitlines() if "PT=" in ln][0]
                bad = [i for i, c in enumerate(pt) if c != "?" and c.upper() != PTX[i]]
                note = f" -> undetectable error (expected): strict fit; the strict decryption is wrong at {len(bad)} positions {bad[:8]} (the pendant edge's residue class), right elsewhere"
            if name in ("P0", "PD") and not any(x[9] == "-1" for x in hit): good = False; note += " (no strict fit)"
        other = [" ".join(x[3:10]) for x in atrow if x not in hit and float(x[8]) <= 1e-4]
        print(f"{name} {exp} slot {slot}: {'PASS' if good else 'FAIL'} (hit {len(hit)}, reported slots {sorted({x[9] for x in hit})}; other low-U fits at row {len(other)}: {other[:4]}){note}"); npass += good
    else:
        low = [" ".join(x[3:10]) for x in atrow if float(x[8]) <= 1e-4]
        ok = not low; npass += ok
        print(f"{name} {exp}: {'PASS' if ok else 'FAIL'} (low-U fits at row: {low[:4]})")
print(f"controls {npass}/{tot}")
