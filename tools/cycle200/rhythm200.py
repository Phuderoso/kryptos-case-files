"""Cycle 200 driver.  python3 rhythm200.py meter|run  [--corpus PATH] [--out FILE]
meter : nulls, critical values, plant power, gates, broken-meter plants; never reads K4's order (only its letter multiset).
run   : meter + K4 + K1/K2/K3 descriptive references.  Seeds are registered in PREREG200.md."""
import sys, json, time, argparse
import numpy as np
from lib200 import K4, enc, panel, shuffles, Meter, names
import plant200 as P

ap = argparse.ArgumentParser()
ap.add_argument("mode")
ap.add_argument("--corpus", default="/workspace/k4c200/sup/rk_plain.txt")
ap.add_argument("--nplant", type=int, default=150)
ap.add_argument("--nown", type=int, default=400)
ap.add_argument("--ntarget", type=int, default=300)
ap.add_argument("--seedbase", type=int, default=20000)
ap.add_argument("--out", default=None)
a = ap.parse_args()
SB = a.seedbase
t0 = time.time()
NM = names()
out = {"mode": a.mode, "seedbase": SB}

# K4 multiset meter (order of K4 is not used here: shuffles of a shuffle are the same distribution)
x4 = enc(K4)
x4multiset = np.sort(x4)                       # deliberately order-free
M = Meter(x4multiset, 10000, SB + 1, 10000, SB + 2)
ALPHA = [0.05, 0.01]
out["crit_hi"] = {str(al): M.crit_hi(al) for al in ALPHA}
out["crit_lo"] = {str(al): M.crit_lo(al) for al in ALPHA}


def own_z(s, nsh, seed):
    x = enc(s)
    P0 = panel(shuffles(x, nsh, seed)).astype(float)
    mu, sd = P0.mean(0), P0.std(0, ddof=1); sd[sd == 0] = 1
    z = (panel(x[None, :])[0] - mu) / sd
    return z


# plant power per family (own-text null, K4 held-out critical values)
txt = P.corpus(a.corpus)
fams = P.FAMILIES + ["P10_shuffled_english"]
power = {}
for fi, f in enumerate(fams):
    rng = np.random.default_rng(SB + 100 + fi)
    zmx, wins, meta = [], {}, []
    for k in range(a.nplant):
        if f == "P10_shuffled_english":
            s = "".join(rng.permutation(list(P.window(rng, txt))))
            md = {}
        else:
            s, md = P.family(f, rng, txt)
        z = own_z(s, a.nown, SB + 10000 + fi * 1000 + k)
        zmx.append(z.max()); j = int(z.argmax()); wins[NM[j]] = wins.get(NM[j], 0) + 1
        meta.append(md)
    zmx = np.array(zmx)
    row = {str(al): float(np.mean(zmx >= out["crit_hi"][str(al)])) for al in ALPHA}
    row["top_stats"] = sorted(wins.items(), key=lambda t: -t[1])[:5]
    # per-period breakdown where defined
    for key in ("p", "w", "L"):
        if meta and key in meta[0]:
            br = {}
            for md, zz in zip(meta, zmx):
                br.setdefault(md[key], []).append(zz >= out["crit_hi"]["0.05"])
            row["by_" + key] = {str(k): round(float(np.mean(v)), 2) for k, v in sorted(br.items())}
    power[f] = row
    print(f, row, flush=True)
out["power"] = power

# targeted reverse test (H_P: P arbitrary alphabets, direct): plant distribution of z(PHI_P), own null
OPEN = [8, 13, 16, 19, 20, 23, 24, 26]
tz = {}
for P_ in OPEN:
    rng = np.random.default_rng(SB + 300 + P_)
    iP = NM.index(f"PHI{P_}")
    zs = [own_z(P.arbitrary_periodic(rng, P.with_cribs(P.window(rng, txt)), P_), a.nown, SB + 50000 + P_ * 1000 + k)[iP]
          for k in range(a.ntarget)]
    tz[P_] = sorted(float(v) for v in zs)
    nulli = np.sort(M.z(panel(shuffles(x4multiset, 10000, SB + 9)))[:, iP])
    c95 = float(np.quantile(nulli, 0.95))
    print(f"H_P{P_}: plant z mean {np.mean(zs):.2f} sd {np.std(zs):.2f}; power (single-stat, alpha .05, crit {c95:.2f}) {np.mean(np.array(zs) >= c95):.2f}", flush=True)
    out.setdefault("targeted", {})[str(P_)] = dict(plant_mean=float(np.mean(zs)), plant_sd=float(np.std(zs)), crit95=c95,
                                                   power=float(np.mean(np.array(zs) >= c95)), plant_q05=float(np.quantile(zs, 0.05)),
                                                   null_mean=float(nulli.mean()), null_q05=float(np.quantile(nulli, 0.05)))

# broken-meter plants (I-230): K4's multiset rearranged by greedy swaps (seed SB+3), up and down
def rearr(sign, seed, iters=4000):
    rng = np.random.default_rng(seed)
    x = rng.permutation(x4multiset)
    def score(v):
        zz = M.z(panel(v[None, :]))[0]
        return (zz.max() if sign > 0 else -zz[NM.index('SA16')])
    sc = score(x)
    for _ in range(iters):
        i, j = rng.integers(0, 97, 2)
        if x[i] == x[j]:
            continue
        x[i], x[j] = x[j], x[i]
        s2 = score(x)
        if s2 >= sc:
            sc = s2
        else:
            x[i], x[j] = x[j], x[i]
    return x
hi = rearr(+1, SB + 3); lo = rearr(-1, SB + 4)
zh = M.z(panel(hi[None, :]))[0]; zl = M.z(panel(lo[None, :]))[0]
out["meter_hi"] = dict(zmax=float(zh.max()), zmin=float(zh.min()), passes=bool(zh.max() > out["crit_hi"]["0.01"]))
iSA = NM.index("SA16")
P1n = M.z(panel(shuffles(x4multiset, 10000, SB + 8)))[:, iSA]
out["meter_lo"] = dict(zmax=float(zl.max()), zmin=float(zl.min()), zSA16=float(zl[iSA]), crit_SA16_lo01=float(np.quantile(P1n, 0.01)),
                       passes=bool(zl[iSA] < np.quantile(P1n, 0.01)))
print("meter", out["meter_hi"], out["meter_lo"], flush=True)

if a.mode == "run":
    z = M.z(panel(x4[None, :]))[0]
    j, jm = int(z.argmax()), int(z.argmin())
    out["K4"] = dict(zmax=float(z.max()), arg=NM[j], raw=int(panel(x4[None, :])[0][j]), mu=float(M.mu[j]), sd=float(M.sd[j]),
                     p_hi=float(M.p_hi(z.max())), zmin=float(z.min()), argmin=NM[jm], p_lo=float(M.p_lo(z.min())),
                     top5=[(NM[i], round(float(z[i]), 3)) for i in np.argsort(-z)[:5]],
                     bottom5=[(NM[i], round(float(z[i]), 3)) for i in np.argsort(z)[:5]],
                     panel=[int(v) for v in panel(x4[None, :])[0]])
    for P_ in OPEN:
        iP = NM.index(f"PHI{P_}"); zk = float(z[iP]); arr = np.array(tz[P_])
        nulli = M.z(panel(shuffles(x4, 10000, SB + 9)))[:, iP]
        out["targeted"][str(P_)].update(K4_z=zk, K4_raw=int(panel(x4[None, :])[0][iP]), q_rev=float(np.mean(arr <= zk)),
                                        p_sig=float((1 + np.sum(nulli >= zk)) / (1 + len(nulli))))
        print("K4 H_P", P_, out["targeted"][str(P_)], flush=True)
    # held-out false-call gate on the K4 winner statistic (I-233a): fresh nulls, seed SB+5
    P5 = M.z(panel(shuffles(x4, 10000, SB + 5)))
    out["K4"]["winner_heldout_tail"] = float(np.mean(P5[:, j] >= z[j]))
    out["K4"]["winner_heldout_maxtail"] = float(np.mean(P5.max(1) >= z[j]))
    print("K4", {k: v for k, v in out["K4"].items() if k != "panel"}, flush=True)
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from kryptos_text import K1, K2, K3
    refs = {}
    for nm, s in (("K1", K1), ("K2", K2.replace("?", "")), ("K3", K3.replace("?", ""))):
        xs = enc(s); Mr = Meter(xs, 3000, SB + 6, 3000, SB + 7)
        zr = Mr.z(panel(xs[None, :]))[0]; jr = int(zr.argmax())
        refs[nm] = dict(n=len(s), zmax=float(zr.max()), arg=NM[jr], p_hi=float(Mr.p_hi(zr.max())),
                        top5=[(NM[i], round(float(zr[i]), 2)) for i in np.argsort(-zr)[:5]])
        print(nm, refs[nm], flush=True)
    out["refs"] = refs

out["seconds"] = round(time.time() - t0, 1)
print("seconds", out["seconds"])
if a.out:
    json.dump(out, open(a.out, "w"), indent=1)
