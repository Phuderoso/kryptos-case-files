"""Cycle 191 control checker. Positive Pk passes if cmp191 reports a fit at the planted row, model, tableau pair, reduced form and (m, n)
AND decode191's logic (literal re-encryption check) reproduces the planted plaintext at every determined position for at least one
reported solution. Fits at equivalent cells (multiples of the planted periods, or the planted pair in a one-tableau cell; I-195-style
equivalence) are listed, not counted against the plant. Negative Nk passes if the planted row has no fit with E_config <= 1e-4 anywhere."""
import sys, subprocess, os
plants, d = sys.argv[1], sys.argv[2]
PTX = "THEIRONDOORFACEDDUEXXEASTNORTHEASTOFTHEFOUNTAINWHERETHEOLDWORLDBERLINCLOCKSTRUCKTHEHOURATMIDNIGHT"
TABS = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
npass = 0; tot = 0
for l in open(plants):
    name, row, md, exp, ct = l.split(); tot += 1
    M = [x.split() for x in open(f"{d}/{name}.txt") if x.startswith("M ")]
    atrow = [x for x in M if x[2] == row]
    if name.startswith("P"):
        tab, form, m, n = exp.split("_")
        hit = [x for x in atrow if x[3] == tab and x[4] == form and x[5] == md and x[6] == m and x[7] == n]
        good = False
        if hit:
            t1, t2 = (TABS[s] for s in tab.split(">"))
            out = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "decode191.py"), ct, "support/ctl191.bin", row, md, t1, t2, form, m, n, "200"], capture_output=True, text=True).stdout
            for ln in out.splitlines():
                if "PT=" in ln:
                    pt = ln.split("PT=")[1].split()[0]
                    if all(c == "?" or c.upper() == PTX[i] for i, c in enumerate(pt)) and pt.count("?") < 97: good = True; break
        other = [" ".join(x[3:9]) for x in atrow if x not in hit and float(x[8]) <= 1e-4]
        print(f"{name} {exp}: {'PASS' if good else 'FAIL'} (hit {len(hit)}; other low-E fits at row {len(other)}: {other[:4]})"); npass += good
    else:
        low = [" ".join(x[3:9]) for x in atrow if float(x[8]) <= 1e-4]
        ok = not low; npass += ok
        print(f"{name} {exp}: {'PASS' if ok else 'FAIL'} (low-E fits at row: {low[:4]})")
print(f"controls {npass}/{tot}")
