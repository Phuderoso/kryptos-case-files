"""Cycle 236 (PREREG236, I-374 compass-point key streams, new family): "boxing the compass" as key material.
Writes keys236.bin (uint8 [W][97]) and keys236.tsv (family, variant, offset, conv). Windows already present in the key files given as
argv (keys217/218/221/233/234) are dropped, as are duplicates.
Source texts (32-point mariner's compass, standard English names, e.g. Bowditch, American Practical Navigator, Table of points):
  R32 full names clockwise from NORTH; R16 the 16-point rose; R8 the 8-point rose; A32 / A16 the standard abbreviations
  (N, NBE, NNE, NEBN, ...). Each is read clockwise (cw) and anticlockwise (acw, order of points reversed, names unchanged),
  as a cyclic letter stream, every character offset; and the whole letter string reversed (rev).
Letter -> key value conv: AZ0 (A=0), AZ1 (A=1), KA0 (index in KRYPTOSABCDEFGHIJLMNQUVWXZ), KA1 (that index + 1).
Numeric streams (cyclic, every offset, c in {0,1}): D32 bearings of the 32 points in whole degrees (floor of 11.25 n), cw and acw;
  L32 / L16 letter counts of the point names (word-length rhythm of the boxed compass), cw and acw."""
import sys
P32 = ['NORTH', 'NORTHBYEAST', 'NORTHNORTHEAST', 'NORTHEASTBYNORTH', 'NORTHEAST', 'NORTHEASTBYEAST', 'EASTNORTHEAST', 'EASTBYNORTH',
       'EAST', 'EASTBYSOUTH', 'EASTSOUTHEAST', 'SOUTHEASTBYEAST', 'SOUTHEAST', 'SOUTHEASTBYSOUTH', 'SOUTHSOUTHEAST', 'SOUTHBYEAST',
       'SOUTH', 'SOUTHBYWEST', 'SOUTHSOUTHWEST', 'SOUTHWESTBYSOUTH', 'SOUTHWEST', 'SOUTHWESTBYWEST', 'WESTSOUTHWEST', 'WESTBYSOUTH',
       'WEST', 'WESTBYNORTH', 'WESTNORTHWEST', 'NORTHWESTBYWEST', 'NORTHWEST', 'NORTHWESTBYNORTH', 'NORTHNORTHWEST', 'NORTHBYWEST']
A32 = ['N', 'NBE', 'NNE', 'NEBN', 'NE', 'NEBE', 'ENE', 'EBN', 'E', 'EBS', 'ESE', 'SEBE', 'SE', 'SEBS', 'SSE', 'SBE',
       'S', 'SBW', 'SSW', 'SWBS', 'SW', 'SWBW', 'WSW', 'WBS', 'W', 'WBN', 'WNW', 'NWBW', 'NW', 'NWBN', 'NNW', 'NBW']
P16, A16 = P32[0::2], A32[0::2]; P8 = P32[0::4]
KA = 'KRYPTOSABCDEFGHIJLMNQUVWXZ'
CONV = {'AZ0': lambda ch: ord(ch) - 65, 'AZ1': lambda ch: ord(ch) - 64, 'KA0': lambda ch: KA.index(ch), 'KA1': lambda ch: KA.index(ch) + 1}
assert sorted(KA) == [chr(65 + i) for i in range(26)] and len(P32) == 32 and P32[6] == 'EASTNORTHEAST'
seen = set()
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read()
    for i in range(0, len(b), 97): seen.add(b[i:i + 97])
rows = []
def add(fam, var, o, conv, vec):
    t = bytes(v % 26 for v in vec)
    if t in seen: return
    seen.add(t); rows.append((fam, var, o, conv, t))
for fam, pts in (('R32', P32), ('R16', P16), ('R8', P8), ('A32', A32), ('A16', A16)):
    for var in ('cw', 'acw', 'rev'):
        if var == 'cw': s = ''.join(pts)
        elif var == 'acw': s = ''.join([pts[0]] + pts[:0:-1])
        else: s = ''.join(pts)[::-1]
        L = len(s)
        for cv, f in CONV.items():
            for o in range(L): add(fam, var, o, cv, [f(s[(o + i) % L]) for i in range(97)])
D32 = [int(11.25 * n) for n in range(32)]
for fam, seq in (('D32', D32), ('L32', [len(x) for x in P32]), ('L16', [len(x) for x in P16])):
    for var in ('cw', 'acw'):
        q = seq if var == 'cw' else [seq[0]] + seq[:0:-1]
        if fam == 'D32' and var == 'acw': q = [(360 - d) % 360 for d in D32]
        L = len(q)
        for o in range(L):
            for c in (0, 1): add(fam, var, o, f'c{c}', [q[(o + i) % L] + c for i in range(97)])
open('keys236.bin', 'wb').write(b''.join(r[4] for r in rows))
with open('keys236.tsv', 'w') as fh:
    for r in rows: fh.write(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n')
from collections import Counter
print(len(rows), 'windows', dict(Counter(r[0] for r in rows)))
