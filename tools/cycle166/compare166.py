"""Cycle 166: split3 vs recount166 on a fixed list of configurations (same alphabet range).  Writes one line each."""
import subprocess, random, sys, os, glob
H = os.path.dirname(os.path.abspath(__file__)); A = "/home/box/kryptos_support_backup/alpha.bin"; Bf = "/home/box/kryptos_support_backup/perms97.bin"
sys.path.insert(0, H); from recount166 import run
texts = dict(l.split() for l in open(os.path.join(H, "texts166.txt")))
for l in open(os.path.join(H, "plants166.txt")): f = l.split(); texts[f[0]] = f[1]
cfgs = [(lab, -1, 0, 0, 86731, -1) for lab in texts if not lab.startswith(('p', 'e'))]
cfgs += [(lab, -1, 0, 0, 86731, dr) for lab in ("K4", "null1", "mnull01", "mnull15") for dr in (0, 12, 23)]
for l in open(os.path.join(H, "plants166.txt")):
    f = l.split(); q = int(f[4]); dr = {"err=28": 7, "err=66": 16, "err=70": 20, "err=24": 3}.get(f[-1], -1)
    for ix in ([0] if f[3] == "direct" else [0 if f[3] == "Q" else 1]): cfgs.append((f[0], q, int(f[5]), ix, 86731, dr))
W = sys.argv[1]; hits = set()
for fn in glob.glob(os.path.join(W, "BA_K4_*.txt")):
    for l in open(fn):
        f = l.split()
        if f[0] == "T": hits.add((int(f[2]), int(f[3]), int(f[4])))
for q, d, ix in sorted(hits)[:12]: cfgs.append(("K4", q, d, ix, 2, -1))
rng = random.Random(16699)
for _ in range(12): cfgs.append(("K4", rng.randrange(165065), rng.randrange(2), rng.randrange(2), 2, -1))
for _ in range(3): cfgs.append(("K4", rng.randrange(826) * 200, rng.randrange(2), rng.randrange(2), 86731, -1))
ok = 0
for lab, q, d, ix, amax, dr in cfgs:
    ct = texts[lab]
    if q < 0: out = subprocess.run([os.path.join(H, "split3"), ct, A, "-", lab, "0", "1", str(amax), str(dr)], capture_output=True, text=True).stdout
    else: out = subprocess.run([os.path.join(H, "split3"), ct, A, Bf, lab, str(q), str(q + 1), str(amax), str(dr)], capture_output=True, text=True).stdout
    Tc, Rc = set(), set()
    for l in out.splitlines():
        f = l.split()
        if f[0] in "TR" and int(f[3]) == d and int(f[4]) == ix:
            if f[0] == "T": Tc.add(int(f[5]))
            else: Rc.add((int(f[5]), int(f[6]), int(f[7])))
    Ta, Ra = run(lab, ct, q, d, ix, amax, dr); same = Tc == set(Ta) and Rc == set(Ra); ok += same
    print(f"CMP {lab} q={q} dir={d} ix={ix} amax={amax} drop={dr} C:T={len(Tc)} R={len(Rc)} PY:T={len(Ta)} R={len(Ra)} {'SAME' if same else 'DIFF'}", flush=True)
print(f"TOTAL {ok}/{len(cfgs)} identical")
