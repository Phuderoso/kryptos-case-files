"""Cycle 227 (PREREG227, I-327 chunk 1): wider keyboard family. Builds geo227a.txt, geo227b.txt (4 layouts each, kb224 format:
letter A..Z -> row,colA,colB) and kb227.bin (keyboard alphabets new to the house + AZ + KA last), with a novelty check against
alpha.bin (86,731), themed144.bin and kb224.bin. usage: layouts227.py WORKDIR ALPHA_BIN THEMED_BIN"""
import sys, numpy as np, hashlib
W, ALPHA, THEMED = sys.argv[1:4]
def keyed(k):
    s = []
    for c in k + "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in s: s.append(c)
    return "".join(s)
def grid_rows(rows):  # rows: list of (string, start col) -> geo dict letter->(r,cA,cB) with cB=cA
    g = {}
    for r, (s, c0) in enumerate(rows):
        for i, ch in enumerate(s): g[ch] = (r, c0 + i, c0 + i)
    return g
def qw_fill(alpha):   # QWERTY key slots 10/9/7, row 2 colB = colA + 1 (half-key stagger as in geo224)
    g = {}
    for i, ch in enumerate(alpha):
        if i < 10: g[ch] = (0, i, i)
        elif i < 19: g[ch] = (1, i - 10, i - 10)
        else: g[ch] = (2, i - 19, i - 18)
    return g
L = {}
# Blickensderfer "Scientific" (DHIATENSOR). W: keyboard-wiki ANSI mapping ('PWFU LCMY/ ; DHIAT ENSOR ; ZXKGB VQJ,.).
L["DHIA-W"] = grid_rows([("PWFULCMY", 1), ("DHIATENSOR", 0), ("ZXKGBVQJ", 0)])
# M: No. 5 manual (Xavier Univ. scan): split between G U T | B L E, rows upper ZXKG|BVQJ, middle .PWFU|LCMY, and home DHIAT|ENSOR.
L["DHIA-M"] = grid_rows([("ZXKGBVQJ", 1), ("PWFULCMY", 1), ("DHIATENSOR", 0)])
for k in ("KRYPTOS", "PALIMPSEST", "ABSCISSA"): L[k + "-QW"] = qw_fill(keyed(k))
old = {}
for line in open(W + "/geo224.txt"):
    f = line.split(); old[f[0]] = {chr(65 + i): tuple(map(int, t.split(","))) for i, t in enumerate(f[1:])}
for nm in ("QWERTY", "QWERTZ", "AZERTY"):   # stagger-aware torus: colA := colB (row 2 shifted half a key); DVORAK skipped (colB 10)
    L[nm + "-S"] = {c: (v[0], v[2], v[2]) for c, v in old[nm].items()}
for nm, g in L.items():
    assert sorted(g) == [chr(65 + i) for i in range(26)], nm
    cells = {(v[0], v[1]) for v in g.values()}; assert len(cells) == 26 and all(0 <= v[1] <= 9 for v in g.values()), nm
order = {"a": ["DHIA-W", "DHIA-M", "KRYPTOS-QW", "PALIMPSEST-QW"], "b": ["ABSCISSA-QW", "QWERTY-S", "QWERTZ-S", "AZERTY-S"]}
for tag, names in order.items():
    with open(f"{W}/geo227{tag}.txt", "w") as f:
        for nm in names: f.write(nm + " " + " ".join("%d,%d,%d" % L[nm][chr(65 + i)] for i in range(26)) + "\n")
# keyboard alphabets: rows L->R (row order as listed), R->L, columns down / up by colA; DHIA-M also home-row-first
def reads(g, roworder=None):
    rows = sorted({v[0] for v in g.values()}); roworder = roworder or rows
    R1 = "".join(c for r in roworder for c in sorted([c for c in g if g[c][0] == r], key=lambda c: g[c][1]))
    R2 = "".join(c for r in roworder for c in sorted([c for c in g if g[c][0] == r], key=lambda c: -g[c][1]))
    C1 = "".join(c for col in range(10) for c in sorted([c for c in g if g[c][1] == col], key=lambda c: g[c][0]))
    C2 = "".join(c for col in range(10) for c in sorted([c for c in g if g[c][1] == col], key=lambda c: -g[c][0]))
    return {"R1": R1, "R2": R2, "C1": C1, "C2": C2}
cand = []
for nm in ["DHIA-W", "DHIA-M", "KRYPTOS-QW", "PALIMPSEST-QW", "ABSCISSA-QW"]:
    for k, s in reads(L[nm]).items(): cand.append((nm + "-" + k, s))
for k, s in reads(L["DHIA-M"], [2, 1, 0]).items():
    if k.startswith("R"): cand.append(("DHIA-M-H" + k, s))
prior = set()
for fn, rec in ((ALPHA, 26), (THEMED, 26), (W + "/kb224.bin", 26)):
    b = np.fromfile(fn, dtype=np.uint8).reshape(-1, rec); prior |= {bytes(r) for r in b}
keep, seen, log = [], set(), []
for nm, s in cand:
    v = bytes(ord(c) - 65 for c in s)
    if v in prior: log.append(f"drop {nm} {s} (in prior alphabet files)"); continue
    if v in seen: log.append(f"drop {nm} {s} (duplicate in this set)"); continue
    seen.add(v); keep.append((nm, s))
keep += [("AZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), ("KA", keyed("KRYPTOS"))]
arr = np.array([[ord(c) - 65 for c in s] for _, s in keep], dtype=np.uint8); arr.tofile(W + "/kb227.bin")
with open(W + "/kb227_names.txt", "w") as f:
    for nm, s in keep: f.write(f"{nm} {s}\n")
print("\n".join(log)); print(f"kept {len(keep)} alphabets ({len(keep)-2} new + AZ + KA); prior set {len(prior)}")
for t in "ab": print(t, hashlib.sha256(open(f"{W}/geo227{t}.txt", "rb").read()).hexdigest())
print("kb227.bin", hashlib.sha256(open(W + "/kb227.bin", "rb").read()).hexdigest())
