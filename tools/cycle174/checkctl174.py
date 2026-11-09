"""Cycle 174: run hill174 / rag174 / portax174 on every planted slice and check that each positive plant is found at its
perm with its parameters (and, for Hill and Portax, decoded back to the plaintext), and that negative plants are missed.
usage (from run/): python3 ../tools/checkctl174.py ctl"""
import sys, json, subprocess
d = json.load(open(sys.argv[1] + "/plants.json")); P = d["P"]
lab = {l.split()[0]: l.split()[1] for l in open("../support/alpha172.txt")}
ok_all = True; rows = []
for p in d["plants"]:
    k = p["kind"]
    if k == "hill":
        o = subprocess.run(["./hill174", p["ct"], p["slice"], "ctl", "0", "200"], capture_output=True, text=True).stdout.split("\n")
        hits = [l.split() for l in o if l.startswith("K ")]
        mine = [h for h in hits if int(h[2]) == p["at"] and int(h[3]) == p["n"] and int(h[4]) == p["aff"] and h[5] == p["num"] and int(h[6]) == p["ix"] and int(h[7]) == p["off"]]
        n, off = p["n"], p["off"]; blk = [i for i in range(97) if off <= i < off + n * ((97 - off) // n)]
        if p["ix"] == 1:  # whole-block test on carved order: compare where decoded
            good = any(all(h[9][i] == P[i] for i in range(97) if h[9][i] != "?") and sum(c != "?" for c in h[9]) >= 90 for h in mine)
        else: good = any(all(h[9][i] == P[i] for i in blk) for h in mine)
        found = bool(mine) and good; others = len(hits) - len(mine)
    elif k == "rag":
        o = subprocess.run(["./rag174", p["ct"], "../support/alpha172.txt", p["slice"], "ctl", "0", "200"], capture_output=True, text=True).stdout.split("\n")
        hits = [l.split() for l in o if l.startswith("B ")]
        mine = [h for h in hits if int(h[2]) == p["at"] and h[3] == lab[p["alpha"]] and int(h[4]) == p["dir"]]
        found = bool(mine); others = len(hits) - len(mine)
    else:
        o = subprocess.run(["./portax174", p["ct"], p["slice"], "ctl", "0", "200", "48"], capture_output=True, text=True).stdout.split("\n")
        hits = [l.split() for l in o if l.startswith("X ")]
        cons = sum(int(l.split()[6]) for l in o if l.startswith("H "))
        mine = [h for h in hits if int(h[2]) == p["at"] and h[3] == p["num"] and int(h[4]) == p["ix"] and int(h[5]) == p["p"]]
        import numpy as np
        S = [int(x) for x in np.fromfile(p["slice"], dtype=np.int16).reshape(-1, 97)[p["at"]]]; pp = p["p"]
        pos = (lambda i: i) if p["ix"] == 0 else (lambda i: S[i])          # position in the Portax text
        cribcols = {pos(i) % pp for i in list(range(21, 34)) + list(range(63, 74))}
        chk = [i for i in range(97) if pos(i) % pp in cribcols]
        good = any(all(h[9][i] in ("?", P[i]) for i in range(97)) and sum(h[9][i] == P[i] for i in chk) >= 24 for h in mine)   # every uniquely-keyed letter decodes to the plaintext
        found = bool(mine) and good; others = cons - len(mine)
    exp = not p["neg"]; res = "PASS" if found == exp else "FAIL"; ok_all &= found == exp
    desc = {k2: p[k2] for k2 in ("n", "aff", "num", "ix", "off", "key", "dir", "alpha") if k2 in p}
    rows.append(f"{res} plant {p['id']} {k} {'NEG ' if p['neg'] else ''}{desc} q={p['q']} found={found} other_hits_in_slice={others}")
print("\n".join(rows)); print("ALL PASS" if ok_all else "SOME FAIL")
