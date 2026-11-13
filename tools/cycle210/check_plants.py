import re
off = {l.split()[0]: int(l.split()[1]) for l in open("out/plants_slices.txt")}
pairs = [tuple(map(int, l.split())) for l in open("p62.txt")]
ok = 0
for l in open("plants.tsv"):
    f = l.rstrip("\n").split("\t"); i, fam, row, d, ix, iy, form, L, segE, segB, o1, o2, key = f[:13]
    pi = pairs.index((int(ix), int(iy))); rel = int(row) - off[i]; hit = False; nsurv = 0
    for s in open(f"out/plant_{i}.txt"):
        if not s.startswith("S "): continue
        nsurv += 1
        kv = dict(t.split("=", 1) for t in s.split()[1:])
        if (int(kv["perm"]) == rel and kv["dir"] == d and int(kv["pair"]) == pi and kv["form"] == form and kv["L"] == L and kv["segE"] == segE
                and kv["segB"] == segB and kv["o1"] == o1 and kv["o2"] == o2 and all(a == "?" or a == b for a, b in zip(kv["key"], key))):
            hit = True
    ok += hit; print(i, fam, L, form, segE, segB, o1, o2, "FOUND" if hit else "MISSING", "survivors_in_slice", nsurv)
print("plants recovered", ok, "/ 12", "PASS" if ok >= 11 else "FAIL")
