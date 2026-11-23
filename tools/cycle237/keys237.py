"""Cycle 237 (PREREG237, I-367): look-and-say S18 rebuilt WITHOUT truncation. S18(n) = length of look-and-say term n (term 1 = '1'), exact via las_exact.py
(Conway audioactive atoms derived in code; validated against direct strings n<=45 and the OEIS A005341 b-file n<=3000).
Windows exactly as keys233.py defines them for sequences: fwd k_i = S18(1+o+i)+c, rev k_i = S18(1+o+96-i)+c, o = 0..39, c in {0,1}, mod 26;
then multiplied by a in {1,3,5,7,9,11} (as keys234.py: a * ((S18+c) mod 26) mod 26). Windows equal to any window of earlier lists (argv) or earlier here are dropped.
Writes keys237.bin / keys237.tsv (a family o c dir)."""
import sys
sys.path.insert(0, '.')
from las_exact import las_len
S = {n: las_len(n) for n in range(1, 140)}
seen = set()
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read(); seen.update(b[i:i + 97] for i in range(0, len(b), 97))
rows = []; dropped = 0
for a in (1, 3, 5, 7, 9, 11):
    for d in ('fwd', 'rev'):
        for o in range(40):
            for c in (0, 1):
                vec = [S[1 + o + i] + c for i in range(97)] if d == 'fwd' else [S[1 + o + 96 - i] + c for i in range(97)]
                t = bytes((a * (v % 26)) % 26 for v in vec)
                if t in seen: dropped += 1; continue
                seen.add(t); rows.append((a, o, c, d, t))
open('keys237.bin', 'wb').write(b''.join(r[4] for r in rows))
with open('keys237.tsv', 'w') as fh:
    for r in rows: fh.write(f'{r[0]}\tS18exact\t{r[1]}\t{r[2]}\t{r[3]}\n')
from collections import Counter
print(len(rows), 'windows;', dropped, 'dropped as duplicates;', dict(Counter(r[0] for r in rows)))
