"""Cycle 212 plant check: case 197's 12 plants (plants.tsv, alph8 indices) + 8 new plants (plants212.tsv, themed-144 indices),
each run through wrj (144 alphabets, 'all' pairs, L 1-16) on a 101-row slice of its family around the true row.
Hit = an S line at the true (row, dir, X, Y, form, L, segE, segB, o1, o2) whose key matches the planted key at every determined index."""
import sys
OUT = sys.argv[1]
A8 = [l.split()[0] for l in open("alph8.txt")]; A144 = [l.split()[0] for l in open("alpha_themed180.txt")]
off = {l.split()[0]: int(l.split()[1]) for l in open(f"{OUT}/plants_slices.txt")}
tot = ok = 0; rows = []
for fn, AL, tag in (("plants.tsv", A8, "c197"), ("plants212.tsv", A144, "new")):
    for l in open(fn):
        f = l.rstrip("\n").split("\t"); i, fam, row, d, ix, iy, form, L, segE, segB, o1, o2, key = f[:13]
        pid = f"{tag}_{i}"; rel = int(row) - off[pid]; X, Y = AL[int(ix)], AL[int(iy)]; hit = False; ns = 0; offrow = set()
        for s in open(f"{OUT}/plant_{pid}.txt"):
            if not s.startswith("S "): continue
            ns += 1; kv = dict(t.split("=", 1) for t in s.split()[1:])
            if int(kv["perm"]) != rel: offrow.add(int(kv["perm"]) + off[pid])
            if (int(kv["perm"]) == rel and kv["dir"] == d and kv["X"] == X and kv["Y"] == Y and kv["form"] == form and kv["L"] == L
                    and kv["segE"] == segE and kv["segB"] == segB and kv["o1"] == o1 and kv["o2"] == o2
                    and all(a == "?" or a == b for a, b in zip(kv["key"], key))):
                hit = True
        tot += 1; ok += hit
        print(pid, fam, "L", L, form, segE, segB, o1, o2, "FOUND" if hit else "MISSING", "survivor_lines", ns, "off_row_lines_rows", sorted(offrow)[:6])
print("plants recovered", ok, "/", tot, "PASS" if ok >= 19 else "FAIL")
