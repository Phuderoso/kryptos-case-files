"""Cycle 218 (PREREG218, I-306): byte / hex regrouping keys ("hex inside hex") and three-digit groups of the I-304 streams.
Writes keys218.bin (uint8 [W][97], key value at key index 0..96) and keys218.tsv (id, family, source, offset, shift, cyclic).
Families (all keys mod 26, every cyclic offset, duplicates of each other AND of cycle 217's keys217.bin dropped):
  B  : ASCII byte values of a named string (upper case; lower case too), k = byte mod 26
  N  : hex nibbles of the ASCII string, k = nibble (0..15)
  NP : hex nibble pairs read at every nibble offset, k = (16a + b) mod 26 (odd offsets straddle bytes)
  D2 : decimal ASCII codes written as one digit string (e.g. K=75 R=82 -> '7582...'), two digits at a time, k = (10a+b) mod 26
  D3 : same digit string, three digits at a time, k = (100a+10b+c) mod 26
  T3 : I-304 long streams (pi, e, sqrt2, sqrt3, sqrt5, phi, ln2; first 900 digits) three digits at a time, offsets 0..199, s in {0,-1};
       I-304 short named streams three digits at a time, cyclic, every offset, s in {0,-1}."""
import mpmath, sys
mpmath.mp.dps = 960
def digits(x):
    return mpmath.nstr(x, 940, strip_zeros=False).replace('.', '')[:900]
LONG = {'pi': mpmath.pi, 'e': mpmath.e, 'sqrt2': mpmath.sqrt(2), 'sqrt3': mpmath.sqrt(3), 'sqrt5': mpmath.sqrt(5),
        'phi': (1 + mpmath.sqrt(5)) / 2, 'ln2': mpmath.log(2)}
SHORT = {'K2coord_raw': '38576577844', 'K2coord_pad': '38570650770844', 'K2lat': '385765', 'K2lon': '77844',
  'ded_mdy': '11031990', 'ded_dmy': '03111990', 'ded_ymd': '19901103', 'ded_short': '1131990',
  'wall_mdy': '11091989', 'wall_dmy': '09111989', 'wall_ymd': '19891109', 'wall_short': '1191989',
  'tomb_mdy': '11261922', 'tomb_dmy': '26111922', 'tomb_ymd': '19221126', 'steps_mdy': '11041922', 'steps_dmy': '04111922',
  'y1986': '1986', 'y1989': '1989', 'y1990': '1990', 'y1922': '1922', 'y1986_1989': '19861989'}
# Named strings (sourced: K1-K3 keywords, K1-K3 plaintext words incl. misspellings, the published K4 cribs/clue words,
# the sculptor/encryption consultant/site names, K2 coordinates as text, K3's scene, Sanborn's 2025 clue themes)
WORDS = ['KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'BERLINCLOCK', 'EASTNORTHEAST', 'BERLIN', 'CLOCK', 'NORTHEAST',
  'SHADOW', 'LUCID', 'MEMORY', 'IQLUSION', 'UNDERGRUUND', 'DESPARATLY', 'LAYERTWO', 'IDBYROWS', 'XLAYERTWO', 'VIRTUALLY', 'INVISIBLE',
  'SANBORN', 'SCHEIDT', 'WEBSTER', 'LANGLEY', 'CIA', 'EGYPT', 'CARTER', 'TUTANKHAMUN', 'CANDLE', 'WORLDCLOCK', 'WELTZEITUHR',
  'MENGENLEHREUHR', 'HEXINSIDEHEX', '385765N77844W', '38 57 6.5 N 77 8 44 W', 'KRYPTOSABCDEFGHIJLMNQUVWXZ']
rows, seen = [], set()
k217 = open(sys.argv[1], 'rb').read() if len(sys.argv) > 1 else b''
for i in range(0, len(k217), 97): seen.add(k217[i:i + 97])
n217 = len(seen)
def add(fam, src, vec, off, s, cyc):
    t = bytes(vec)
    if t in seen: return
    seen.add(t); rows.append((fam, src, off, s, cyc, t))
def cyc_groups(fam, src, vals, g, base, s_list):
    L = len(vals)
    for off in range(L):
        for s in s_list:
            v = []
            for t in range(97):
                x = 0
                for j in range(g): x = x * base + vals[(off + g * t + j) % L]
                v.append((x + s) % 26)
            add(fam, src, v, off, s, 1)
for w in WORDS:
    for case, ww in (('U', w), ('l', w.lower())):
        b = list(ww.encode())
        cyc_groups('B', case + ':' + w, b, 1, 256, (0,))
        nib = [int(h, 16) for h in ww.encode().hex()]
        if case == 'U':
            cyc_groups('N', case + ':' + w, nib, 1, 16, (0,))
        cyc_groups('NP', case + ':' + w, nib, 2, 16, (0,))
        dd = [int(c) for c in ''.join(str(x) for x in b)]
        cyc_groups('D2', case + ':' + w, dd, 2, 10, (0,))
        cyc_groups('D3', case + ':' + w, dd, 3, 10, (0,))
for name, x in LONG.items():
    d = [int(c) for c in digits(x)]; assert len(d) == 900
    for off in range(200):
        for s in (0, -1):
            add('T3', name, [(100 * d[off + 3 * t] + 10 * d[off + 3 * t + 1] + d[off + 3 * t + 2] + s) % 26 for t in range(97)], off, s, 0)
for name, d in SHORT.items():
    cyc_groups('T3', name, [int(c) for c in d], 3, 10, (0, -1))
with open('keys218.bin', 'wb') as f:
    for r in rows: f.write(r[5])
with open('keys218.tsv', 'w') as f:
    f.write('id\tfamily\tsource\toffset\tshift\tcyclic\n')
    for i, r in enumerate(rows): f.write(f'{i}\t{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\n')
from collections import Counter
print('windows', len(rows), 'dropped-as-in-217', n217, dict(Counter(r[0] for r in rows)), 'pi head', digits(mpmath.pi)[:12])
