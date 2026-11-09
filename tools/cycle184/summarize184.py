"""Cycle 184 summary: per text, fits and mod-2 passes from the H lines; overflow / mismatch lines; method-0 / audit agreement;
labels; grid by empirical rank (I-152).   usage: summarize184.py outdir nulls184.txt"""
import sys, statistics as st
od, nf = sys.argv[1:3]; nulls = [l.split()[0] for l in open(nf)]
def read(fn):
    H = {}; ok = False; bad = []
    for l in open(fn):
        a = l.split()
        if not a: continue
        if a[0] == "H": H[(int(a[3]), a[5])] = dict(pass2=int(a[11]), fits=int(a[13]))
        elif a[0] == "O" and (a[3] != "0" or a[5] != "0"): bad.append(l.strip())
        elif a[0] == "X": bad.append(l.strip())
        elif a[0] == "END": ok = True
    return H, ok, bad
Hl = lambda fn: [l for l in open(fn) if l.startswith("H ")]
H, ok, bad = read(f"{od}/k4.full.txt")
print("== K4 full set (165,782 perms x 352,538,176 ordered (A, B) vocabulary pairs x Vig/Beau, key on the plaintext index)")
for L in range(1, 5): print(f"K4 L{L} fits vig {H[(L,'vig')]['fits']} beau {H[(L,'beau')]['fits']} mod-2 passes {H[(L,'vig')]['pass2']}")
print(f"END {ok} bad {bad}")
print("method 0 (CSR union map) vs method 1 (syndrome join), K4 all_s64, H lines identical:", Hl(f"{od}/k4.s64m0.txt") == Hl(f"{od}/k4.s64m1.txt"))
print("audit build (method 2, -DSAFE=1) vs method 1, K4 all_s2048, H lines identical:", Hl(f"{od}/k4.s2ksafe.txt") == Hl(f"{od}/k4.s2km1.txt"))
for f in ("k4.s64m0", "k4.s64m1", "k4.s2km1", "k4.s2ksafe"):
    h, o, b = read(f"{od}/{f}.txt"); print(f"  {f}: fits {sum(v['fits'] for v in h.values())} END {o} bad {b}")
print("== all_s512 (K4 + 19 nulls), L 1-4")
rows = {}
for lab in ["k4"] + nulls:
    h, o, b = read(f"{od}/{lab}.s512.txt"); rows[lab] = (sum(v["fits"] for v in h.values()), h[(4, "vig")]["pass2"], o, b)
    print(lab, f"fits {rows[lab][0]} pass2_L4 {rows[lab][1]}{'' if o else ' NO-END'}{' BAD' if b else ''}")
print("== grid (empirical rank among 20 texts; F = fits L 1-4 (scored only if not all-zero); D1 = mod-2 passes at L 4 (every L <= 4 by nesting))")
ps = []
for nm, i in (("F", 0), ("D1", 1)):
    v = {l: rows[l][i] for l in rows}; k = v["k4"]; nv = [v[l] for l in nulls]
    if nm == "F" and all(x == 0 for x in v.values()): print("F: all zero (reported, not scored)"); continue
    pp = (1 + sum(x >= k for x in nv)) / 20; pm = (1 + sum(x <= k for x in nv)) / 20; ps.append((pp, pm))
    print(f"{nm}: K4 {k} nulls {min(nv)}-{max(nv)} mean {st.mean(nv):.1f} SD {st.stdev(nv):.1f} p+ {pp:.2f} p- {pm:.2f}")
if ps: print(f"grid p+ {min(p for p, _ in ps):.2f} / p- {min(m for _, m in ps):.2f}  [no multiplicity correction; floor 0.05]")
