"""Cycle 174 Ragbaby recount: for each Ragbaby plant, the Python enumeration (recount174.rag_fit) on the planted perm and
its 4 slice neighbours x (planted alphabet + 5 others from the list) x both directions, compared with rag174 per config."""
import json, subprocess, random, sys, numpy as np, importlib.util
sys.argv = ["x", "A" * 97, "../support/all.bin", "0", "0", "none"]
spec = importlib.util.spec_from_file_location("rc", "../tools/recount174.py"); rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
d = json.load(open("ctl/plants.json")); R = random.Random(1741)
AL = [l.split() for l in open("../support/alpha172.txt")]; lab = {a: b for a, b in AL}
n = agree = 0; pos = 0
for p in d["plants"]:
    if p["kind"] != "rag": continue
    rc.ct = p["ct"]; P = np.fromfile(p["slice"], dtype=np.int16).reshape(-1, 97)
    alphas = [p["alpha"]] + [AL[R.randrange(len(AL))][0] for _ in range(5)]
    open("rec/rag_alph.txt", "w").write("".join(f"{a} {lab[a]}\n" for a in alphas))
    lo, hi = max(0, p["at"] - 2), min(200, p["at"] + 3)
    o = subprocess.run(["./rag174", p["ct"], "rec/rag_alph.txt", p["slice"], "r", str(lo), str(hi)], capture_output=True, text=True).stdout
    chits = {(int(w.split()[2]), w.split()[3], int(w.split()[4])) for w in o.splitlines() if w.startswith("B ")}
    for q in range(lo, hi):
        S = [int(x) for x in P[q]]
        for a in alphas:
            for dd in (1, -1):
                py = rc.rag_fit(S, a, dd); c = (q, lab[a], dd) in chits; n += 1; agree += py == c; pos += py
print(f"Ragbaby recount: {n} configs, agree {agree}, positives {pos}")
