"""Cycle 173: run anom173 on every planted slice and check the plant is found at its slot (t=100, d, tableau, mode, idx, p)
with crib-fixed key letters equal to the planted key. ctl10 (two anomalies) must be MISSED. usage: checkctl173.py ctl_dir tool"""
import sys, subprocess, re
D, tool = sys.argv[1], sys.argv[2]; ok = 0; tot = 0; lines = []
for l in open(f"{D}/plants.txt"):
    f = dict(x.split("=", 1) for x in l.split()[1:] if "=" in x); name = l.split()[0]
    model = "del" if f["model"] == "neg" else f["model"]; ct = open(f"{D}/{name}.txt").read().strip()
    out = subprocess.run([tool, f"{D}/{name}_slice.bin", f["n"], model, ct, "26", "26", "0", "200"], capture_output=True, text=True).stdout
    open(f"{D}/{name}_out.txt", "w").write(out)
    p = int(f["p"]); key = f["key"]; found = False
    for h in out.splitlines():
        m = re.match(r"HIT t=(\d+) d=(\d+) PA=(\w+) CA=(\w+) mode=(\w+) idx=(\w+) p=(\d+) key=(\S+)", h)
        if not m: continue
        t, d, pa, ca, mo, ix, pp, k = m.groups()
        if (int(t), int(d), pa, ca, mo, ix, int(pp)) == (100, int(f["d"]), f["PA"], f["CA"], f["mode"], f["idx"], p) and all(a in "?" + b for a, b in zip(k, key)):
            found = True; kk = k
    exp_miss = f["model"] == "neg"; good = found != exp_miss; tot += 1; ok += good
    nh = sum(1 for h in out.splitlines() if h.startswith("HIT") and f" p={p} " in h)
    lines.append(f"{name} {f['model']} p={p} {'FOUND key=' + kk if found else 'MISSED'} {'(expected miss)' if exp_miss else ''} hits_at_p_in_slice={nh} -> {'PASS' if good else 'FAIL'}")
print("\n".join(lines)); print(f"CONTROLS {ok}/{tot} PASS")
