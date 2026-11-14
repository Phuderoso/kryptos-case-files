#!/usr/bin/env python3
"""Cycle 214 part B scoring (after results214b_blind.txt was committed): Voynich detection rule.
Recovered <=> an S-line at the true perm, dir, tm, L 16, segE, segB, o1, o2 whose key agrees with the planted key at every
determined index ('?' = undetermined). Also counts off-target lines and distinct effective maps (perm,dir) vs (perm+-1, 1-dir) twins."""
import json, re, sys
T = json.load(open(sys.argv[1]))["plants"]; R = open(sys.argv[2]).read().splitlines()
lines = {}
for l in R:
    m = re.match(r"(G\d+) S perm=(\d+) dir=(\d) tm=(\d) L=(\d+) segE=(\S+) segB=(\S+) o1=(\d+) o2=(\d+) key=(\S+)", l)
    if m: lines.setdefault(m[1], []).append(m)
rec = 0; out = []
for t in sorted(T, key=lambda t: t["plant"]):
    hits = lines.get(t["plant"], []); ok = False; off = 0
    for m in hits:
        same = (int(m[2]), int(m[3]), int(m[4]), int(m[5]), m[6], m[7], int(m[8]), int(m[9])) == \
               (t["perm"], t["dir"], t["tm"], t["L"], t["segE"], t["segB"], t["o1"], t["o2"])
        keyok = all(a == "?" or a == b for a, b in zip(m[10], t["key"]))
        if same and keyok: ok = True
        elif not same: off += 1
    rec += ok
    out.append(dict(plant=t["plant"], recovered=ok, lines=len(hits), off_target=off, form=t["form"], o1=t["o1"], o2=t["o2"], perm=t["perm"]))
    print(t["plant"], "REC" if ok else "MISS", "lines", len(hits), "off-target", off, t["form"], "o1", t["o1"], "o2", t["o2"], "perm", t["perm"], t["tag"])
print("recovered", rec, "/", len(T), "->", "PASS" if rec >= 9 else "FAIL")
json.dump(dict(recovered=rec, n=len(T), per_plant=out), open(sys.argv[3], "w"), indent=1)
