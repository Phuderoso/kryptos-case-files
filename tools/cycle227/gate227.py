"""Cycle 227 Gate P: run kb227 on each plant's true scope row with its geometry file and kb227.bin (printbar -99), record whether
the planted cell is reported (H line; G: right partition / layout) and its P line (known, nqnc, NC with tie = '?').
usage: gate227.py WORKDIR -> gateP227.tsv"""
import sys, subprocess
W = sys.argv[1]; npr = {1: 165065, 2: 165782}; fn = {1: "bank.bin", 2: "all.bin"}
rows = []; nf = 0; nbar = 0; nq = 0
for line in open(W + "/plants227.tsv"):
    pid, model, geo, scope, row, d, ix, p, desc, bad, ct, pt = line.rstrip("\n").split("\t")
    scope, row, d, ix, p = int(scope), int(row), int(d), int(ix), int(p)
    args = [W + "/kb227", ct, "x" if scope == 0 else W + "/" + fn[scope], W + "/kb227.bin", W + f"/geo227{geo}.txt",
            "1" if scope == 0 else str(npr[scope]), "0" if scope == 0 else str(row), model, "1000000", "24",
            W + "/qg.bin", W + "/oracle226.txt", "-99", "1000000"]
    o = subprocess.run(args, capture_output=True, text=True, env={"OMP_NUM_THREADS": "1"}).stdout
    want = dict(kv.split("=") for kv in desc.split())
    def match(h, needp):
        kv = dict(t.split("=", 1) for t in h.split()[2:] if "=" in t)
        if int(kv["perm"]) != (row if scope else -1) or int(kv["dir"]) != d: return None
        if any(kv.get(k) != v for k, v in want.items()): return None
        if model == "G": return kv
        if int(kv["ix"]) != (ix if scope else 0): return None
        if needp and int(kv["p"]) != p: return None
        if not needp and p % int(kv["p"]) != 0: return None
        return kv
    found = any(match(h, False) for h in o.splitlines() if h.startswith("H " + model))
    pl = [match(h, True) for h in o.splitlines() if h.startswith("P " + model)] if model != "G" else []
    pl = [k for k in pl if k]; kv = pl[0] if pl else {}
    nf += found
    if model != "G" and found:
        nq += 1; nbar += (kv.get("nc", "-") != "-" and float(kv["nc"]) >= -6.0)
    rows.append(f"{pid}\t{model}\t{geo}\t{scope}\t{p}\tbad={bad}\tfound={int(found)}\tknown={kv.get('known','<49')}\tnqnc={kv.get('nqnc','-')}\tnc={kv.get('nc','-')}\tpt={kv.get('pt','-')}\ttrue={pt}")
open(W + "/gateP227.tsv", "w").write("\n".join(rows) + "\n"); print("\n".join(r[:110] for r in rows))
print(f"FOUND {nf}/20; V/Q found plants over NC>=-6.0 (tie='?'): {nbar}/{nq}")
