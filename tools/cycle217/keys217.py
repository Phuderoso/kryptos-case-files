"""Cycle 217 (PREREG217, I-304): named numeric streams read two digits at a time, k = (10a + b + s) mod 26, s in {0, -1}.
Writes keys217.bin (uint8 [W][97], key value at key index 0..96) and keys217.tsv (id, stream, offset, shift, cyclic).
Long streams: first 700 digits (integer part included), offsets 0..399. Short named streams: cyclic, every offset 0..L-1.
Duplicate 97-vectors are dropped (first label kept)."""
import mpmath, sys
mpmath.mp.dps = 760
def digits(x):
    s = mpmath.nstr(x, 740, strip_zeros=False).replace('.', '')
    return s[:700]
LONG = {'pi': mpmath.pi, 'e': mpmath.e, 'sqrt2': mpmath.sqrt(2), 'sqrt3': mpmath.sqrt(3), 'sqrt5': mpmath.sqrt(5),
        'phi': (1 + mpmath.sqrt(5)) / 2, 'ln2': mpmath.log(2)}
SHORT = {  # sourced facts: K2 plaintext coordinates; Kryptos dedication 1990-11-03; Berlin Wall opened 1989-11-09;
           # Carter's tomb (K3 scene) opened 1922-11-26, steps found 1922-11-04; 1986 / 1989 named in I-304
  'K2coord_raw': '38576577844', 'K2coord_pad': '38570650770844', 'K2lat': '385765', 'K2lon': '77844',
  'ded_mdy': '11031990', 'ded_dmy': '03111990', 'ded_ymd': '19901103', 'ded_short': '1131990',
  'wall_mdy': '11091989', 'wall_dmy': '09111989', 'wall_ymd': '19891109', 'wall_short': '1191989',
  'tomb_mdy': '11261922', 'tomb_dmy': '26111922', 'tomb_ymd': '19221126', 'steps_mdy': '11041922', 'steps_dmy': '04111922',
  'y1986': '1986', 'y1989': '1989', 'y1990': '1990', 'y1922': '1922', 'y1986_1989': '19861989'}
rows, seen = [], set()
def add(name, vec, off, s, cyc):
    t = bytes(vec)
    if t in seen: return
    seen.add(t); rows.append((name, off, s, cyc, t))
for name, x in LONG.items():
    d = digits(x); assert len(d) == 700
    for off in range(400):
        for s in (0, -1):
            add(name, [(10 * int(d[off + 2 * t]) + int(d[off + 2 * t + 1]) + s) % 26 for t in range(97)], off, s, 0)
for name, d in SHORT.items():
    L = len(d)
    for off in range(L):
        for s in (0, -1):
            add(name, [(10 * int(d[(off + 2 * t) % L]) + int(d[(off + 2 * t + 1) % L]) + s) % 26 for t in range(97)], off, s, 1)
with open('keys217.bin', 'wb') as f:
    for r in rows: f.write(r[4])
with open('keys217.tsv', 'w') as f:
    f.write('id\tstream\toffset\tshift\tcyclic\n')
    for i, r in enumerate(rows): f.write(f'{i}\t{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n')
print('windows', len(rows), 'pi head', digits(mpmath.pi)[:12], 'ln2 head', digits(mpmath.log(2))[:8])
