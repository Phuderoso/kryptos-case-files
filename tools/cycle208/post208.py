#!/usr/bin/env python3
"""Cycle 208 post-processing: K4 vs null cell counts per L (raw cells as wrbank prints them; doubled-Vig convention = Vig x2)."""
import glob, json, math, sys, os
D = sys.argv[1]
def hist(f):
    h = {}
    for l in open(f):
        if l.startswith("H "):
            _, tm, L, c = l.split(); h.setdefault(int(L), [0]*4)[int(tm)] += int(c)
    return h
k4 = hist(f"{D}/k4_fam_L1-22.txt"); k4.update(hist(f"{D}/k4_fam_L23-26.txt"))
nulls = [hist(f"{D}/null_{i}.txt") for i in range(1, 21)]
assert all(len(n) == 22 for n in nulls), "incomplete nulls"
rows = []
print("L  K4raw  K4dblVig  null_mean_raw  null_min  null_max  nulls>=1  P(any)_est  K4>all_nulls")
for L in range(1, 23):
    kr = sum(k4[L]); kd = kr + k4[L][0] + k4[L][2]
    nr = [sum(n[L]) for n in nulls]; m = sum(nr)/20; f = sum(x > 0 for x in nr)
    # crude chance rate: null mean cells / 8 (dir twin x Vig/variant pairing x ~2 segmentations) as distinct configs, Poisson
    p_est = 1 - math.exp(-m/8) if m > 0 else 0.0
    rows.append(dict(L=L, k4_raw=kr, k4_dblvig=kd, null_mean_raw=m, null_min=min(nr), null_max=max(nr), nulls_ge1=f, p_any_est=p_est,
                     k4_exceeds_all=kr > max(nr)))
    print(f"{L:2d} {kr:7d} {kd:8d} {m:14.2f} {min(nr):8d} {max(nr):8d} {f:6d}/20 {p_est:10.4f}  {kr>max(nr)}")
print("L23-26 K4 raw:", {L: sum(k4[L]) for L in range(23, 27)})
json.dump(rows, open(f"{D}/post208.json", "w"), indent=1)
