"""Cycle 195 grid: K4 vs 19 shuffles (seeds 19511-19529), tab4 on all of col1. Per text: fits in full-power cells (cell E <= 0.05), printed fits
with e >= 3 and >= 4, solutions in bands 1 and 2, low-power solutions split two-tableau / one-tableau; p+ = (1 + #nulls >= K4)/20 (rank flag only)."""
import glob, math
ONE = {'AZ>AZ', 'KA>KA'}
rows = {}
for fn in sorted(glob.glob('run/grid/g_*.txt')):
    lab = fn.split('g_')[1][:-4]; L = [l.split() for l in open(fn)]
    assert L[-1][0] == 'END', fn
    st = {'FPfits': 0, 'B1': 0.0, 'B2': 0.0, 'F3': 0, 'F4': 0, 'two_sols_lp': 0.0, 'one_sols_lp': 0.0}
    for w in L:
        if w[0] == 'B' and w[2] == '1': st['B1'] = float(w[5])
        if w[0] == 'B' and w[2] == '2': st['B2'] = float(w[5])
        if w[0] == 'M':
            e = round(-math.log(float(w[8])) / math.log(26))
            if e >= 3: st['F3'] += 1
            if e >= 4: st['F4'] += 1
        if w[0] == 'H':
            if float(w[10]) <= 0.05: st['FPfits'] += int(w[8])
            else: st['one_sols_lp' if w[3] in ONE else 'two_sols_lp'] += float(w[9])
    rows[lab] = st
k = rows.pop('k4'); print(f"stat: K4 | {len(rows)} nulls min-max | p+")
for s in k:
    v = [r[s] for r in rows.values()]
    print(f"{s}: K4 {k[s]:g} | nulls {min(v):g}-{max(v):g} (median {sorted(v)[len(v)//2]:g}) | p+ {(1 + sum(1 for x in v if x >= k[s])) / 20:.2f}")
