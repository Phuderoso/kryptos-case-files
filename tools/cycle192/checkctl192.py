"""Cycle 192 control checker. Positive Pk passes if cmp192 reports a fit at the planted row, model, tableau pair, reduced form and (m, n)
AND decode192 finds a consistent deletion (the planted slot, or for P0 no deletion; an EQUIVALENT slot is accepted and named, I-195) whose
decryption reproduces the planted plaintext at every determined position except the deleted slot's own position. Fits at equivalent cells
(period multiples, one-tableau form equivalents, crib-offset coincidences) are listed, not failures. Negative Nk passes if the planted row
has no fit with U <= 1e-4 anywhere."""
import sys, subprocess, os
plants, d = sys.argv[1], sys.argv[2]
PTX = "THEIRONDOORFACEDDUEXXEASTNORTHEASTOFTHEFOUNTAINWHERETHEOLDWORLDBERLINCLOCKSTRUCKTHEHOURATMIDNIGHT"
CIDX = list(range(21, 34)) + list(range(63, 74))
TABS = {"AZ": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "KA": "KRYPTOSABCDEFGHIJLMNQUVWXZ"}
npass = tot = 0
for l in open(plants):
    name, row, md, exp, sl, ct = l.split(); tot += 1
    M = [x.split() for x in open(f"{d}/{name}.txt") if x.startswith("M ")]
    assert open(f"{d}/{name}.txt").read().rstrip().splitlines()[-1].startswith("END"), name
    atrow = [x for x in M if x[2] == row]
    if name.startswith("P"):
        tab, form, m, n = exp.split("_"); want = int(sl)
        hit = [x for x in atrow if x[3] == tab and x[4] == form and x[5] == md and x[6] == m and x[7] == n]
        good, how = False, ""
        if hit:
            t1, t2 = (TABS[s] for s in tab.split(">"))
            out = subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "decode192.py"), ct, "support/ctl191.bin", row, md, t1, t2, form, m, n, "100", "all"], capture_output=True, text=True).stdout
            cons = []
            for ln in out.splitlines():
                if ln.startswith("  del "):
                    dd = int(ln.split()[1]); pt = ln.split("PT=")[1].split()[0]
                    skip = CIDX[dd] if dd >= 0 else -1
                    if all(c == "?" or i == skip or c.upper() == PTX[i] for i, c in enumerate(pt)) and pt.count("?") < 97:
                        if dd not in cons: cons.append(dd)
            if cons: good = True; how = f"reproducing deletions {cons}" + ("" if want in cons else f" (planted slot {want} EQUIVALENT-ONLY)")
        U = hit[0][8] if hit else "-"
        other = [" ".join(x[3:10]) for x in atrow if x not in hit and float(x[8]) <= 1e-4]
        print(f"{name} {exp} wrong slot {sl}: {'PASS' if good else 'FAIL'} (hit {len(hit)}, U {U}, reported slot {hit[0][9] if hit else '-'}; {how}; other low-U fits at row {len(other)}: {other[:4]})"); npass += good
    else:
        low = [" ".join(x[3:10]) for x in atrow if float(x[8]) <= 1e-4]
        ok = not low; npass += ok
        print(f"{name} {exp}: {'PASS' if ok else 'FAIL'} (low-U fits at row: {low[:4]})")
print(f"controls {npass}/{tot}")
