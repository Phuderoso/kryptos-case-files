"""Cycle 239 (PREREG239, I-379): audioactive DIGIT streams as key windows (case 223 tested only the length stream S18).
All streams derived from the look-and-say sequence, term 1 = '1'. Atom (element) decomposition: atoms derived in code by
las_exact.py (Conway's 92, case 223) and matched one-to-one to Conway's numbering Z 1..92 (H..U) from the Wikipedia table
(conway_table.py, las_wiki.txt); decay lists cross-checked. Families (fwd only, 97 values, mod 26):
  LSCAT    digits of T1 T2 T3 ... concatenated; k_i = d_{o+i} + c, o 0..499, c in {0,1}
  LSTERMn  digits of term n (n = 16..21) read cyclically from offset o (all offsets); k_i = d + c, c in {0,1}
  PAIRCAT  LSCAT digits in two-digit groups from offset o: k_i = (10 d_{o+2i} + d_{o+2i+1}) mod 26, o 0..399
  PAIRT21  term 21 digits cyclic in two-digit groups from offset o, o 0..407
  ELEMZ    concatenated element sequences of terms 8,9,10,...: k_i = Z_{o+i} + c (Z = atomic number 1..92), o 0..499, c {0,1}
  ELEMD1   same element stream, first digit of each element string + c, o 0..499, c {0,1}
  S18PAIR  decimal digits of S18(1) S18(2) ... concatenated, two-digit groups from offset o, o 0..399
Windows equal to any window of earlier lists (argv) or earlier here are dropped. Writes keys239.bin / keys239.tsv."""
import sys
sys.path.insert(0, '.')
import las_exact as LE
from conway_table import load
T = load()
assert set(LE.NAMES) == set(T), 'derived atoms != Conway table'
Z = {s: T[s][0] for s in T}; SYM = {s: T[s][1] for s in T}
for i, a in enumerate(LE.NAMES):   # decay lists must agree with the table
    assert [SYM[LE.NAMES[j]] for j in LE.DEC[i]] == T[a][2], a
def ev(s): return LE.ev(s)
terms = ['1']
for _ in range(24): terms.append(ev(terms[-1]))
term = lambda n: terms[n - 1]
# element sequence of term n: split term 8 (first compound term), then ordered decay
idx = {a: i for i, a in enumerate(LE.NAMES)}
seq8 = [idx[a] for a in LE.split_atom(term(8))]
assert all(LE.NAMES[a] in T for a in seq8)
els = {8: seq8}
for n in range(9, 40): els[n] = [b for a in els[n - 1] for b in LE.DEC[a]]
for n in range(8, 22): assert ''.join(LE.NAMES[a] for a in els[n]) == term(n), n
estream = []
n = 8
while len(estream) < 700: estream += els[n]; n += 1
EZ = [Z[LE.NAMES[a]] for a in estream]; ED = [int(LE.NAMES[a][0]) for a in estream]
cat = ''.join(terms); assert len(cat) > 1400
s18 = ''.join(str(LE.las_len(n)) for n in range(1, 140)); assert len(s18) > 600, len(s18)
seen = set()
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read(); seen.update(b[i:i + 97] for i in range(0, len(b), 97))
rows = []; dropped = 0
def add(fam, o, c, vec):
    global dropped
    t = bytes(v % 26 for v in vec)
    if t in seen: dropped += 1; return
    seen.add(t); rows.append((fam, o, c, t))
for o in range(500):
    for c in (0, 1): add('LSCAT', o, c, [int(cat[o + i]) + c for i in range(97)])
for n in range(16, 22):
    s = term(n)
    for o in range(len(s)):
        for c in (0, 1): add(f'LSTERM{n}', o, c, [int(s[(o + i) % len(s)]) + c for i in range(97)])
for o in range(400): add('PAIRCAT', o, 0, [10 * int(cat[o + 2 * i]) + int(cat[o + 2 * i + 1]) for i in range(97)])
s = term(21)
for o in range(len(s)): add('PAIRT21', o, 0, [10 * int(s[(o + 2 * i) % len(s)]) + int(s[(o + 2 * i + 1) % len(s)]) for i in range(97)])
for o in range(500):
    for c in (0, 1): add('ELEMZ', o, c, [EZ[o + i] + c for i in range(97)])
for o in range(500):
    for c in (0, 1): add('ELEMD1', o, c, [ED[o + i] + c for i in range(97)])
for o in range(400): add('S18PAIR', o, 0, [10 * int(s18[o + 2 * i]) + int(s18[o + 2 * i + 1]) for i in range(97)])
open('keys239.bin', 'wb').write(b''.join(r[3] for r in rows))
with open('keys239.tsv', 'w') as fh:
    for r in rows: fh.write(f'{r[0]}\t{r[1]}\t{r[2]}\n')
from collections import Counter
print(len(rows), 'windows;', dropped, 'dropped as duplicates;', dict(Counter(r[0] for r in rows)))
print('term lengths 16..21', [len(term(n)) for n in range(16, 22)], 'element stream head', [SYM[LE.NAMES[a]] for a in estream[:12]], 'Z head', EZ[:12])
