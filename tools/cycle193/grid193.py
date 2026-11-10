"""Cycle 193 grid: K4 vs 19 shuffles (seeds 19311-19329), tab4 on all_s512. Per text: fits with e >= 3 and >= 4, solutions in bands 1 and 2,
split into two-tableau (AZ>KA, KA>AZ) and one-tableau (AZ>AZ, KA>KA) from the M/H lines; p+ = (1 + #nulls >= K4)/20 (rank flag only)."""
import glob, math
ONE = {'AZ>AZ', 'KA>KA'}
rows = {}
for fn in sorted(glob.glob('run/grid/g512_*.txt')):
    lab = fn.split('g512_')[1][:-4]; L = [l.split() for l in open(fn)]
    assert L[-1][0] == 'END', fn
    st = {'B1': 0.0, 'B2': 0.0, 'F3': 0, 'F4': 0, 'two_sols': 0.0, 'one_sols': 0.0}
    for w in L:
        if w[0] == 'B' and w[2] == '1': st['B1'] = float(w[5])
        if w[0] == 'B' and w[2] == '2': st['B2'] = float(w[5])
        if w[0] == 'M':
            e = round(-math.log(float(w[8])) / math.log(26))
            if e >= 3: st['F3'] += 1
            if e >= 4: st['F4'] += 1
        if w[0] == 'H' and float(w[10]) <= 26 ** -0.5 * 324 and float(w[10]) > 0:
            st['one_sols' if w[3] in ONE else 'two_sols'] += float(w[9])
    rows[lab] = st
k = rows.pop('k4'); print("stat: K4 | nulls min-max | p+")
for s in k:
    v = [r[s] for r in rows.values()]
    print(f"{s}: K4 {k[s]:g} | nulls {min(v):g}-{max(v):g} (median {sorted(v)[len(v)//2]:g}) | p+ {(1 + sum(1 for x in v if x >= k[s])) / 20:.2f}")
