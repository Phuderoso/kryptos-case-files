"""Cycle 234 (PREREG234, I-362 chunk 1): multiplied arithmetic-sequence key streams.
Rebuilds the full cycle-233 window set (keys233.py logic, no cross-list dedup) into base233full.bin, then writes
k_i = a * ((f(.) + c) mod 26) mod 26 for a in {3, 5, 7, 9, 11} (units mod 26, one representative of each +-a pair:
-a under Vigenere equals +a under variant, so forms 0/1 are covered; Beaufort with -a is a stated blind spot).
Windows equal to any window in keys217/218/221/233 or earlier in this list are dropped. Writes keys234.bin / keys234.tsv."""
import subprocess, sys, os
A = (3, 5, 7, 9, 11)
os.makedirs('base', exist_ok=True)
subprocess.run([sys.executable, '../keys233.py'], cwd='base', check=True)
base = open('base/keys233.bin', 'rb').read(); tsv = open('base/keys233.tsv').read().splitlines()
assert len(base) // 97 == len(tsv)
seen = set()
for fn in ('keys217.bin', 'keys218.bin', 'keys221.bin', 'keys233.bin'):
    b = open(fn, 'rb').read(); seen.update(b[i:i + 97] for i in range(0, len(b), 97))
rows = []
for a in A:
    for j, meta in enumerate(tsv):
        t = bytes((a * v) % 26 for v in base[j * 97:(j + 1) * 97])
        if t in seen: continue
        seen.add(t); rows.append((a, meta, t))
open('keys234.bin', 'wb').write(b''.join(r[2] for r in rows))
with open('keys234.tsv', 'w') as fh:
    for a, meta, _ in rows: fh.write(f'{a}\t{meta}\n')
from collections import Counter
print(len(base) // 97, 'base windows;', len(rows), 'windows', dict(Counter(r[0] for r in rows)))
