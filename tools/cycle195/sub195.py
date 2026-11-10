"""Cycle 195 support subsets (text-free). col1_s8.bin = every 8th row of col1.bin (meter/probe); col2_s32.bin = every 32nd row of col2.bin;
col1_th.bin = col1 rows whose keyword is in gen195's THEMED list (C3); ctl195.bin = control rows:
 0 col1 KRYPTOS/enc, 1 col1 PALIMPSEST/enc, 2 col1 LODESTONE/inv, 3 col1 first width-14 order /enc, 4 col2 KRYPTOS+PALIMPSEST/enc,
 5 all.bin row 12345 (a K3-law route; for the cross-family negative), 6 col1 BERLIN/inv.  Row labels printed to ctl195_index.txt."""
import numpy as np, re
S = 'support/'
TH = set(re.search(r'THEMED = """(.*?)"""', open('tools/gen195.py').read(), re.S).group(1).split())
c1 = np.fromfile(S + 'col1.bin', dtype=np.int16).reshape(-1, 97); c2 = np.fromfile(S + 'col2.bin', dtype=np.int16).reshape(-1, 97)
A = np.fromfile(S + 'all.bin', dtype=np.int16).reshape(-1, 97)
i1 = [l.split()[1] for l in open(S + 'col1_index.txt')]; i2 = [l.split()[1] for l in open(S + 'col2_index.txt')]
c1[::8].tofile(S + 'col1_s8.bin'); c2[::32].tofile(S + 'col2_s32.bin')
th = [q for q, lab in enumerate(i1) if lab.split('/')[0] in TH]; c1[th].tofile(S + 'col1_th.bin')
with open(S + 'col1_th_index.txt', 'w') as f:
    for k, q in enumerate(th): f.write(f"{k} {q} {i1[q]}\n")
w14 = next(q for q, lab in enumerate(i1) if len(lab.split('/')[0]) == 14 and lab.endswith('/enc'))
sel = [('col1', i1.index('KRYPTOS/enc')), ('col1', i1.index('PALIMPSEST/enc')), ('col1', i1.index('LODESTONE/inv')), ('col1', w14),
       ('col2', i2.index('KRYPTOS+PALIMPSEST/enc')), ('all', 12345), ('col1', i1.index('BERLIN/inv'))]
rows = [ {'col1': c1, 'col2': c2, 'all': A}[b][q] for b, q in sel ]
np.array(rows, dtype=np.int16).tofile(S + 'ctl195.bin')
with open(S + 'ctl195_index.txt', 'w') as f:
    for k, (b, q) in enumerate(sel): f.write(f"{k} {b} {q} {(i1 if b == 'col1' else i2)[q] if b != 'all' else 'route'}\n")
print(len(th), 'themed col1 rows;', open(S + 'ctl195_index.txt').read())
