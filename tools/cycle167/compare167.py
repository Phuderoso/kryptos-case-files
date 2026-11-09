"""Cycle 167: compare shift3 n3 against recount167 on (1) every plant at its true layer for every form triple of the true
alphabet, (2) K4 and 2 nulls direct on 12 fixed alphabets x 8 triples, (3) K4 at 4 bank configurations on A-Z/KRYPTOS.
Every shift3 S line that falls inside a compared cell must match; absent lines mean n3 = 0."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from recount167 import n3
H = os.path.dirname(os.path.abspath(__file__)); A = "/home/box/kryptos_support_backup/alpha.bin"; Bf = "/home/box/kryptos_support_backup/perms97.bin"
def run(ct, q, amax, drop=-1, a_only=None):
    args = [os.path.join(H, "shift3"), ct, A, "-" if q < 0 else Bf, "x", str(max(q, 0)), str(max(q, 0) + 1), str(amax), str(drop)]
    out = {}
    for l in subprocess.run(args, capture_output=True, text=True).stdout.split("\n"):
        w = l.split()
        if w and w[0] == "S": out[(int(w[3]), int(w[4]), int(w[5]), w[6] + w[7] + w[8])] = int(w[10])
    return out
F = [f"{i&1}{(i>>1)&1}{(i>>2)&1}" for i in range(8)]
ok = tot = 0; lines = []
def cmp(tag, ct, q, d, ix, alphas, amax, drop=-1):
    global ok, tot
    o = run(ct, q, amax, drop)
    for a in alphas:
        for f in F:
            x = o.get((d, ix, a, f), 0); y = n3(ct, q, d, ix, a, f, drop); tot += 1; ok += (x == y)
            if x or y or x != y: lines.append(f"{tag} q={q} dir={d} ix={ix} a={a} forms={f} shift3={x} recount={y} {'OK' if x == y else 'DIFF'}")
for l in open(os.path.join(H, "plants167.txt")):
    w = l.split(); lab, ct, layer, q, d, a = w[0], w[1], w[3], int(w[4]), int(w[5]), int(w[6])
    drop = {"28": 7, "66": 16, "70": 20, "24": 3}[w[-1][4:]] if w[-1].startswith("err=") else -1
    cmp(lab, ct, q, d if q >= 0 else 0, 1 if layer == "carved" else 0, [a], 86731, drop)
T = dict(l.split() for l in open(os.path.join(H, "texts167.txt")))
fixed = [0, 1, 2, 3, 7, 100, 1000, 5000, 20000, 40000, 60000, 86730]
for lab in ["K4", "null1", "mnull01"]: cmp(lab, T[lab], -1, 0, 0, fixed, 86731)
for q, d, ix in [(0, 0, 0), (4000, 1, 1), (82000, 0, 1), (164000, 1, 0)]: cmp("K4bank", T["K4"], q, d, ix, [0, 1], 2)
print("\n".join(lines)); print(f"compare {ok}/{tot} cells identical")
