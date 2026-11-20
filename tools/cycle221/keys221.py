"""Cycle 221 (PREREG221, I-311): machine / signal encodings of named strings as key streams.
Writes keys221.bin (uint8 [W][97]) and keys221.tsv. Every window already in keys217.bin or keys218.bin is dropped, as are
duplicates inside this list. All keys mod 26, cyclic over the encoded string, every offset.
Families:
  IT  : ITA2 (Baudot-Murray) 5-bit code value per character, k = code mod 26; bit order as tabled (b1 = LSB) and reversed.
        Digits / punctuation use the FIGS row with FIGS (27) / LTRS (31) shift codes inserted at each case change.
  IG  : the ITA2 bit stream (tabled order, b1 first) regrouped g = 4 or 8 bits MSB-first, every bit offset, k = value mod 26.
  MC  : Morse element count per character (letters 1-4, digits 5); a digit-range periodic key (overlaps case 202, kept as a
        consistency check).
  MV  : Morse code as a binary number with a leading 1 marker (dot 0, dash 1; A .- = 0b101 = 5), k = value mod 26.
  MB  : Morse dot/dash bit stream (dot 0, dash 1, letter boundaries dropped) regrouped g = 4, 5 or 8 bits, every bit offset.
  EB  : EBCDIC (cp037) byte per character, upper and lower case, k = byte mod 26.
  EN  : EBCDIC hex nibbles (k = 0..15) and nibble pairs at every nibble offset (k = byte mod 26 at odd offsets), upper case.
  BC  : 4-bit BCD of the I-304 short digit streams regrouped g = 5, 6 or 8 bits, every bit offset (g = 4 is the plain digit key).
Spaces are dropped from the named strings except in the two coordinate strings, where ITA2 / Morse / EBCDIC encode them as written."""
import sys
from collections import Counter
ITA2 = dict(A=0x03, B=0x19, C=0x0E, D=0x09, E=0x01, F=0x0D, G=0x1A, H=0x14, I=0x06, J=0x0B, K=0x0F, L=0x12, M=0x1C,
            N=0x0C, O=0x18, P=0x16, Q=0x17, R=0x0A, S=0x05, T=0x10, U=0x07, V=0x1E, W=0x13, X=0x1D, Y=0x15, Z=0x11)
FIGS_ROW = {'1': 'Q', '2': 'W', '3': 'E', '4': 'R', '5': 'T', '6': 'Y', '7': 'U', '8': 'I', '9': 'O', '0': 'P', '.': 'M'}
FIGS, LTRS, SPACE = 0x1B, 0x1F, 0x04
MORSE = dict(A='.-', B='-...', C='-.-.', D='-..', E='.', F='..-.', G='--.', H='....', I='..', J='.---', K='-.-', L='.-..',
  M='--', N='-.', O='---', P='.--.', Q='--.-', R='.-.', S='...', T='-', U='..-', V='...-', W='.--', X='-..-', Y='-.--',
  Z='--..', **{'0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
  '8': '---..', '9': '----.', '.': '.-.-.-'})
WORDS = ['KRYPTOS', 'PALIMPSEST', 'ABSCISSA', 'BERLINCLOCK', 'EASTNORTHEAST', 'BERLIN', 'CLOCK', 'NORTHEAST',
  'SHADOW', 'LUCID', 'MEMORY', 'IQLUSION', 'UNDERGRUUND', 'DESPARATLY', 'LAYERTWO', 'IDBYROWS', 'XLAYERTWO', 'VIRTUALLY', 'INVISIBLE',
  'SANBORN', 'SCHEIDT', 'WEBSTER', 'LANGLEY', 'CIA', 'EGYPT', 'CARTER', 'TUTANKHAMUN', 'CANDLE', 'WORLDCLOCK', 'WELTZEITUHR',
  'MENGENLEHREUHR', 'HEXINSIDEHEX', '385765N77844W', '38 57 6.5 N 77 8 44 W', 'KRYPTOSABCDEFGHIJLMNQUVWXZ',
  # Morse-plate phrases at the Kryptos entrance (secondary, widely reproduced transcriptions; Sanborn's own misspelling kept)
  'VIRTUALLYINVISIBLE', 'SHADOWFORCES', 'LUCIDMEMORY', 'DIGETALINTERPRETATIU', 'TISYOURPOSITION', 'SOS', 'RQ']
SHORT = {'K2coord_raw': '38576577844', 'K2coord_pad': '38570650770844', 'K2lat': '385765', 'K2lon': '77844',
  'ded_mdy': '11031990', 'ded_dmy': '03111990', 'ded_ymd': '19901103', 'ded_short': '1131990',
  'wall_mdy': '11091989', 'wall_dmy': '09111989', 'wall_ymd': '19891109', 'wall_short': '1191989',
  'tomb_mdy': '11261922', 'tomb_dmy': '26111922', 'tomb_ymd': '19221126', 'steps_mdy': '11041922', 'steps_dmy': '04111922',
  'y1986': '1986', 'y1989': '1989', 'y1990': '1990', 'y1922': '1922', 'y1986_1989': '19861989'}
seen = set()
for fn in sys.argv[1:]:
    b = open(fn, 'rb').read()
    for i in range(0, len(b), 97): seen.add(b[i:i + 97])
nprev = len(seen); rows = []
def add(fam, src, vec, off):
    t = bytes(vec)
    if t in seen: return
    seen.add(t); rows.append((fam, src, off, t))
def cyc_vals(fam, src, vals):
    L = len(vals)
    for off in range(L): add(fam, src, [vals[(off + t) % L] % 26 for t in range(97)], off)
def cyc_bits(fam, src, bits, g):
    L = len(bits)
    for off in range(L):
        v = []
        for t in range(97):
            x = 0
            for j in range(g): x = 2 * x + bits[(off + g * t + j) % L]
            v.append(x % 26)
        add(fam, src, v, off)
def ita2(w):
    out, figs = [], False
    for c in w:
        if c == ' ': out.append(SPACE); continue
        if c in FIGS_ROW:
            if not figs: out.append(FIGS); figs = True
            out.append(ITA2[FIGS_ROW[c]])
        else:
            if figs: out.append(LTRS); figs = False
            out.append(ITA2[c])
    if figs: out.append(LTRS)  # cyclic stream returns to letters
    return out
rev5 = lambda v: int(format(v, '05b')[::-1], 2)
for w in WORDS:
    s = w if ' ' in w and w[0].isdigit() else w.replace(' ', '')
    it = ita2(s)
    cyc_vals('IT', 'b1lsb:' + w, it); cyc_vals('IT', 'b1msb:' + w, [rev5(v) for v in it])
    bits = [(v >> j) & 1 for v in it for j in range(5)]  # b1 (LSB) first, as punched
    for g in (4, 8): cyc_bits('IG', f'g{g}:' + w, bits, g)
    ms = [MORSE[c] for c in s if c != ' ']
    cyc_vals('MC', w, [len(m) for m in ms])
    cyc_vals('MV', w, [int('1' + m.replace('.', '0').replace('-', '1'), 2) for m in ms])
    mb = [1 if ch == '-' else 0 for m in ms for ch in m]
    for g in (4, 5, 8): cyc_bits('MB', f'g{g}:' + w, mb, g)
    for case, ww in (('U', s), ('l', s.lower())):
        cyc_vals('EB', case + ':' + w, list(ww.encode('cp037')))
    nib = [int(h, 16) for h in s.encode('cp037').hex()]
    cyc_vals('EN', 'nib:' + w, nib)
    L = len(nib)
    for off in range(L): add('EN', 'pair:' + w, [(16 * nib[(off + 2 * t) % L] + nib[(off + 2 * t + 1) % L]) % 26 for t in range(97)], off)
for name, d in SHORT.items():
    bits = [(int(c) >> (3 - j)) & 1 for c in d for j in range(4)]
    for g in (5, 6, 8): cyc_bits('BC', f'g{g}:' + name, bits, g)
with open('keys221.bin', 'wb') as f:
    for r in rows: f.write(r[3])
with open('keys221.tsv', 'w') as f:
    f.write('id\tfamily\tsource\toffset\n')
    for i, r in enumerate(rows): f.write(f'{i}\t{r[0]}\t{r[1]}\t{r[2]}\n')
print('windows', len(rows), 'prior-distinct', nprev, dict(Counter(r[0] for r in rows)))
