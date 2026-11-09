"""Cycle 163: compare recount163.py lines (R ...) with split7e.c output for the same configurations (S count, Z count, X flag)."""
import sys, glob, collections
S = collections.Counter(); Z = collections.Counter(); X = set()
for f in glob.glob("run/bank_*.txt"):
    for l in open(f):
        p = l.split()
        if p[0] in "SZX": key = (p[1], int(p[2]), int(p[3]), int(p[4]))
        if p[0] == "S": S[key] += 1
        elif p[0] == "Z": Z[key] += 1
        elif p[0] == "X": X.add(key)
ok = bad = 0
for l in open(sys.argv[1]):
    if not l.startswith("R "): continue
    p = l.split(); key = (p[1], int(p[2]), int(p[3]), int(p[4]))
    s, z, x = (int(p[5].split("=")[1]), int(p[6].split("=")[1]), int(p[7].split("=")[1]))
    c = (S[key], Z[key], int(key in X))
    if c == (s, z, x): ok += 1
    else: bad += 1; print("MISMATCH", key, "recount", (s, z, x), "split7e", c)
print(f"agree {ok} / {ok + bad}")
